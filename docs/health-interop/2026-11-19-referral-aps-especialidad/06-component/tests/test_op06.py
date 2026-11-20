"""Tests de OP-6 (contrareferencia, PI-3).

Fuente: operations.md (OP-6), lifecycle.md, sequences.md diagrama 5.
El Task pasa a `counter-referred` con el acuse de recibo de APS, no
con el envío: el envío deja el Task en `completed` (con
`counter_referral_sent`) y bloquea la cancelación (OP-8).
"""

import unittest

from derivacion.builders import (
    build_care_plan,
    build_composition,
    build_condition,
    build_document_bundle,
    build_document_reference,
)
from derivacion.workflow import WorkflowError
from tests.golden import assert_golden
from tests.test_op04 import dt, make_booked, task_extensions

SENT = dt(2026, 12, 3, 10, 0)
START = dt(2026, 12, 2, 10, 0)
END = dt(2026, 12, 2, 10, 30)


def make_completed():
    referral = make_booked()
    referral.record_arrival(now=START)
    referral.finish_encounter(now=END)
    return referral


def diagnosis_kwargs():
    return {
        "resource_id": "diagnostico-ref-2026-0001",
        "patient_id": "maria-gonzalez",
        "encounter_id": "encuentro-ref-2026-0001",
        "text": "Insuficiencia cardiaca sistólica crónica (FEVI 35%)",
        "note_text": "FEVI 35% por ecocardiograma. Sin isquemia aguda en el ECG.",
    }


def care_plan_kwargs():
    return {
        "resource_id": "plan-ref-2026-0001",
        "patient_id": "maria-gonzalez",
        "encounter_id": "encuentro-ref-2026-0001",
        "specialist_role_id": "rol-especialista",
        "condition_id": "diagnostico-ref-2026-0001",
        "activities": [
            "Control en APS en 2 semanas: presión arterial, peso, síntomas.",
            "NT-proBNP de control en 3 meses.",
        ],
        "service_request_id": "ref-2026-0001",
    }


def composition_kwargs():
    return {
        "resource_id": "contrareferencia-ref-2026-0001",
        "referral_id": "REF-2026-0001",
        "patient_id": "maria-gonzalez",
        "encounter_id": "encuentro-ref-2026-0001",
        "specialist_role_id": "rol-especialista",
        "condition_id": "diagnostico-ref-2026-0001",
        "care_plan_id": "plan-ref-2026-0001",
        "date": SENT,
        "diagnosis_section": "Chronic systolic heart failure, LVEF 35% (ICD-10-CM I50.22).",
        "plan_section": "Start heart-failure treatment; control in APS in 2 weeks.",
        "follow_up_indications": "Blood pressure, weight and symptoms at each APS control; NT-proBNP in 3 months.",
        "follow_up_plan": "APS follow-up as in the CarePlan; new referral to cardiology if dyspnoea worsens.",
    }


def document_reference_kwargs():
    return {
        "resource_id": "documento-ref-2026-0001",
        "composition_id": "contrareferencia-ref-2026-0001",
        "patient_id": "maria-gonzalez",
        "encounter_id": "encuentro-ref-2026-0001",
        "service_request_id": "ref-2026-0001",
        "specialist_role_id": "rol-especialista",
        "date": SENT,
        "period_start": START,
        "period_end": END,
    }


class TestCounterReferralBuilders(unittest.TestCase):
    def test_condition_matches_golden(self):
        assert_golden(self, build_condition(**diagnosis_kwargs()),
                      "Condition-diagnostico-ref-2026-0001")

    def test_care_plan_matches_golden(self):
        assert_golden(self, build_care_plan(**care_plan_kwargs()),
                      "CarePlan-plan-ref-2026-0001")

    def test_composition_matches_golden(self):
        assert_golden(self, build_composition(**composition_kwargs()),
                      "Composition-contrareferencia-ref-2026-0001")

    def test_document_reference_matches_golden(self):
        assert_golden(self, build_document_reference(**document_reference_kwargs()),
                      "DocumentReference-documento-ref-2026-0001")

    def test_document_bundle_matches_golden(self):
        bundle = build_document_bundle(
            build_composition(**composition_kwargs()),
            build_document_reference(**document_reference_kwargs()),
            build_condition(**diagnosis_kwargs()),
            build_care_plan(**care_plan_kwargs()),
            timestamp=SENT,
            resource_id="bundle-pi3-ref-2026-0001",
        )
        assert_golden(self, bundle, "Bundle-bundle-pi3-ref-2026-0001")


class TestCounterReferralWorkflow(unittest.TestCase):
    def test_send_then_acknowledge_closes_the_loop(self):
        referral = make_completed()
        bundle = referral.send_counter_referral(now=SENT)
        assert_golden(self, bundle, "Bundle-bundle-pi3-ref-2026-0001")
        # El envío no mueve el Task: sigue `completed`, pero la
        # contrareferencia ya se envió (R4 se desarma).
        self.assertEqual(referral.case_state, "completed")
        self.assertTrue(referral.counter_referral_sent)
        self.assertEqual(referral.service_request["status"], "active")
        self.assertNotIn("sla-counterreferral-deadline",
                         task_extensions(referral.task))
        # El acuse de recibo de APS cierra el ciclo.
        referral.acknowledge_counter_referral(now=dt(2026, 12, 3, 11, 0))
        self.assertEqual(referral.case_state, "counter-referred")
        self.assertEqual(referral.task["status"], "completed")
        self.assertEqual(referral.service_request["status"], "completed")
        self.assertEqual(referral.check_invariants(), [])
        receipt = [n for n in referral.notifications
                   if n["topic"]["text"] == "counter-referral-receipt"][0]
        self.assertEqual(
            receipt["payload"][0]["contentReference"]["reference"],
            "DocumentReference/documento-ref-2026-0001")
        # C3 (revisión experta): el acuse va al operador del hub como
        # PractitionerRole, no a la Organization del hub.
        self.assertEqual(receipt["recipient"][0]["reference"],
                         "PractitionerRole/rol-operador-hub")
        self.assertEqual(receipt["sender"]["reference"],
                         "PractitionerRole/rol-admin-aps")
        informed = [n for n in referral.notifications
                    if n["topic"]["text"] == "counter-referred"]
        self.assertEqual(len(informed), 1)
        self.assertEqual(informed[0]["recipient"][0]["reference"],
                         "Patient/maria-gonzalez")

    def test_acknowledge_without_send_is_forbidden(self):
        referral = make_completed()
        with self.assertRaises(WorkflowError):
            referral.acknowledge_counter_referral(now=SENT)

    def test_send_before_visit_is_forbidden(self):
        referral = make_booked()
        with self.assertRaises(WorkflowError):
            referral.send_counter_referral(now=SENT)

    def test_r4_escalates_while_counter_referral_unsent(self):
        referral = make_completed()
        applied = referral.apply_sla_actions(now=dt(2026, 12, 10, 9, 0))
        self.assertEqual([a["rule"] for a in applied], ["R4"])
        self.assertEqual(referral.case_state, "completed")


if __name__ == "__main__":
    unittest.main()
