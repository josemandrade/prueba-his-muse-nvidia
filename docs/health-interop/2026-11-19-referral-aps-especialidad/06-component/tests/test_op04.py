"""Tests de OP-4 (re-ofertar / re-agendar, PI-2) y del motor de flujo.

Fuente: operations.md (OP-4), lifecycle.md, BPMN Parte B (gateway
`First decline?`, `Chased twice?`), R3 del evaluador SLA.
"""

import unittest
from datetime import datetime, timedelta, timezone

from derivacion.evaluator import sla_deadlines
from derivacion.registry import seed_worked_example
from derivacion.workflow import (
    IdentityNotFoundError,
    Referral,
    ServiceNotFoundError,
    WorkflowError,
)

TZ = timezone(timedelta(hours=-3))


def dt(year, month, day, hour=9, minute=0):
    return datetime(year, month, day, hour, minute, tzinfo=TZ)


CREATED = dt(2026, 11, 19, 9, 30)
ROUTED = dt(2026, 11, 19, 10, 0)
ACCEPTED = dt(2026, 11, 21, 9, 0)
OFFERED = dt(2026, 11, 24, 11, 0)
START = dt(2026, 12, 2, 10, 0)
END = dt(2026, 12, 2, 10, 30)


def make_accepted():
    """Una derivación aceptada, lista para la oferta (OP-1 + OP-2)."""
    registry = seed_worked_example()
    referral = Referral.create(
        registry, "REF-2026-0001", "maria-gonzalez", "rol-medico-aps",
        "cardiologia", "84114007", "routine", authored_on=CREATED,
        now=CREATED)
    referral.route(now=ROUTED)
    referral.triage(
        "accepted", now=ACCEPTED, service_id="servicio-cardiologia",
        specialist_role_id="rol-especialista")
    return referral


def make_offered(referral=None):
    referral = referral or make_accepted()
    referral.offer_appointment(
        "slot-cardiologia-1", "schedule-cardiologia", START, END,
        now=OFFERED,
        patient_instruction="Ayuno no necesario. Traer los exámenes previos.")
    return referral


def make_booked(referral=None):
    referral = make_offered(referral)
    referral.respond_to_offer("accepted", now=dt(2026, 11, 25, 9, 0))
    referral.book_appointment(now=dt(2026, 11, 25, 10, 0))
    return referral


def task_extensions(task):
    return {
        ext["url"].rsplit("/", 1)[-1].removeprefix("derivacion-"):
            ext.get("valueDateTime", ext.get("valueInteger"))
        for ext in task.get("extension", [])
    }


class TestCreateGuards(unittest.TestCase):
    def test_create_blocks_unresolved_identity(self):
        with self.assertRaises(IdentityNotFoundError):
            Referral.create(
                seed_worked_example(), "REF-2026-0002", "paciente-fantasma",
                "rol-medico-aps", "cardiologia", "84114007", "routine",
                authored_on=CREATED, now=CREATED)

    def test_create_blocks_unknown_service(self):
        with self.assertRaises(ServiceNotFoundError):
            Referral.create(
                seed_worked_example(), "REF-2026-0002", "maria-gonzalez",
                "rol-medico-aps", "neurologia", "84114007", "routine",
                authored_on=CREATED, now=CREATED)

    def test_acceptance_carries_offer_deadline_not_acceptance(self):
        referral = make_accepted()
        extensions = task_extensions(referral.task)
        self.assertIn("sla-offer-deadline", extensions)
        self.assertNotIn("sla-acceptance-deadline", extensions)
        self.assertEqual(referral.task["owner"]["reference"],
                         "HealthcareService/servicio-cardiologia")
        self.assertEqual(referral.task["businessStatus"]["coding"][0]["code"],
                         "accepted")

    def test_acceptance_notification_shape_matches_golden(self):
        referral = make_accepted()
        note = [n for n in referral.notifications
                if n["topic"]["text"] == "accepted"][0]
        self.assertEqual(note["sender"]["reference"],
                         "PractitionerRole/rol-admin-aps")
        self.assertEqual(note["recipient"][0]["reference"],
                         "Patient/maria-gonzalez")
        self.assertEqual(note["medium"][0]["coding"][0]["code"], "phone")


class TestTriageReject(unittest.TestCase):
    def test_reject_opens_retriage_then_decision_closes(self):
        registry = seed_worked_example()
        referral = Referral.create(
            registry, "REF-2026-0001", "maria-gonzalez", "rol-medico-aps",
            "cardiologia", "84114007", "routine", authored_on=CREATED,
            now=CREATED)
        referral.route(now=ROUTED)
        referral.triage("rejected", now=ACCEPTED, reason_code="capacity",
                        reason_display="Capacity")
        self.assertEqual(referral.case_state, "rejected")
        self.assertEqual(
            referral.task["statusReason"]["coding"][0]["code"], "capacity")
        self.assertEqual(referral.service_request["status"], "active")
        self.assertIn("sla-retriage-deadline",
                      task_extensions(referral.task))
        referral.decide_retriage("resolve-in-aps", now=dt(2026, 11, 23, 9, 0))
        self.assertEqual(referral.service_request["status"], "revoked")
        self.assertTrue(referral.retriage_decided)
        # C5 (revisión experta): la decisión de re-triaje deja su
        # entrada de Provenance (actor: médico de APS).
        self.assertEqual(len(referral.history), 3)
        provenance = referral.history[-1]
        self.assertEqual(provenance["resourceType"], "Provenance")
        self.assertEqual(provenance["agent"][0]["who"]["reference"],
                         "PractitionerRole/rol-medico-aps")
        self.assertEqual(provenance["agent"][0]["type"]["coding"][0]["code"],
                         "aps-doctor")
        with self.assertRaises(WorkflowError):
            referral.decide_retriage("new-referral", now=dt(2026, 11, 23, 10, 0))


class TestDeclineAndReoffer(unittest.TestCase):
    def test_first_decline_allows_one_reoffer(self):
        referral = make_offered()
        referral.respond_to_offer("declined", now=dt(2026, 11, 25, 9, 0))
        self.assertEqual(referral.case_state, "accepted")
        self.assertEqual(referral.counts["decline"], 1)
        self.assertEqual(referral.current_appointment["status"], "cancelled")
        referral.offer_appointment(
            "slot-cardiologia-2", "schedule-cardiologia",
            dt(2026, 12, 3, 10, 0), dt(2026, 12, 3, 10, 30),
            now=dt(2026, 11, 25, 10, 0))
        self.assertEqual(referral.offer_number, 2)
        self.assertEqual(referral.current_appointment["status"], "proposed")
        # El conteo de decline NO se reinicia en la re-oferta: es el
        # conteo del ciclo, no de la oferta suelta (Ruling 11.8).
        self.assertEqual(referral.counts["decline"], 1)
        # El de chase sí se reinicia en cada oferta.
        self.assertEqual(referral.counts["chase"], 0)

    def test_second_decline_returns_to_retriage(self):
        referral = make_offered()
        referral.respond_to_offer("declined", now=dt(2026, 11, 25, 9, 0))
        referral.offer_appointment(
            "slot-cardiologia-2", "schedule-cardiologia",
            dt(2026, 12, 3, 10, 0), dt(2026, 12, 3, 10, 30),
            now=dt(2026, 11, 25, 10, 0))
        referral.respond_to_offer("declined", now=dt(2026, 11, 26, 9, 0))
        self.assertEqual(referral.case_state, "rejected")
        self.assertEqual(referral.counts["decline"], 2)
        expected = sla_deadlines(
            created=CREATED, priority="routine",
            retriage_return_at=dt(2026, 11, 26, 9, 0))["retriage"]
        self.assertEqual(
            task_extensions(referral.task)["sla-retriage-deadline"],
            expected.isoformat())
        # La solicitud sigue activa hasta que APS decida (mapeo §2).
        self.assertEqual(referral.service_request["status"], "active")
        self.assertFalse(referral.retriage_decided)
        referral.decide_retriage("new-referral", now=dt(2026, 11, 27, 9, 0))
        self.assertEqual(referral.service_request["status"], "revoked")

    def test_r5_fires_after_second_decline_return(self):
        # C1 (revisión experta): tras el retorno por segundo rechazo,
        # el plazo de re-triaje corre desde el retorno y R5 escala a
        # APS cuando vence (rules.md R5).
        referral = make_offered()
        referral.respond_to_offer("declined", now=dt(2026, 11, 25, 9, 0))
        referral.offer_appointment(
            "slot-cardiologia-2", "schedule-cardiologia",
            dt(2026, 12, 3, 10, 0), dt(2026, 12, 3, 10, 30),
            now=dt(2026, 11, 25, 10, 0))
        referral.respond_to_offer("declined", now=dt(2026, 11, 26, 9, 0))
        self.assertEqual(referral.case_state, "rejected")
        deadline = sla_deadlines(
            created=CREATED, priority="routine",
            retriage_return_at=dt(2026, 11, 26, 9, 0))["retriage"]
        self.assertEqual(
            referral.apply_sla_actions(
                now=deadline - timedelta(days=1)), [])
        applied = referral.apply_sla_actions(
            now=deadline + timedelta(days=1))
        self.assertEqual([a["rule"] for a in applied], ["R5"])
        self.assertEqual(applied[0]["action"], "escalate-aps")


class TestChaseAndR3(unittest.TestCase):
    def test_two_chases_then_r3_returns_to_retriage(self):
        referral = make_offered()
        self.assertEqual(referral.chase_offer(now=dt(2026, 11, 26, 9, 0)), 1)
        self.assertEqual(referral.chase_offer(now=dt(2026, 11, 27, 9, 0)), 2)
        with self.assertRaises(WorkflowError):
            referral.chase_offer(now=dt(2026, 11, 27, 10, 0))
        self.assertEqual(
            len([n for n in referral.notifications
                 if n["topic"]["text"] == "chase"]), 2)
        # Vencido el plazo de confirmación (2026-11-27 17:00) con dos
        # persecuciones sin confirmar: R3 devuelve al re-triaje.
        applied = referral.apply_sla_actions(now=dt(2026, 11, 28, 9, 0))
        self.assertEqual([a["rule"] for a in applied], ["R3"])
        self.assertEqual(applied[0]["action"], "return-to-retriage")
        self.assertEqual(referral.case_state, "rejected")
        self.assertIn("sla-retriage-deadline",
                      task_extensions(referral.task))

    def test_r5_fires_after_r3_return(self):
        # C1 (revisión experta): tras el retorno por R3, el plazo de
        # re-triaje también corre desde el retorno y R5 escala a APS.
        referral = make_offered()
        referral.chase_offer(now=dt(2026, 11, 26, 9, 0))
        referral.chase_offer(now=dt(2026, 11, 27, 9, 0))
        applied = referral.apply_sla_actions(now=dt(2026, 11, 28, 9, 0))
        self.assertEqual(applied[0]["action"], "return-to-retriage")
        deadline = sla_deadlines(
            created=dt(2026, 11, 19, 9, 30), priority="routine",
            retriage_return_at=dt(2026, 11, 28, 9, 0))["retriage"]
        self.assertEqual(
            referral.apply_sla_actions(
                now=deadline - timedelta(days=1)), [])
        applied = referral.apply_sla_actions(
            now=deadline + timedelta(days=1))
        self.assertEqual([a["rule"] for a in applied], ["R5"])
        self.assertEqual(applied[0]["action"], "escalate-aps")

    def test_r3_chases_after_deadline_before_return(self):
        referral = make_offered()
        applied = referral.apply_sla_actions(now=dt(2026, 11, 28, 9, 0))
        self.assertEqual(applied[0]["action"], "chase-patient")
        self.assertEqual(referral.counts["chase"], 1)
        # La segunda evaluación vuelve a perseguir (R3 no se marca
        # como disparada tras una persecución: el conteo manda).
        applied = referral.apply_sla_actions(now=dt(2026, 11, 28, 10, 0))
        self.assertEqual(applied[0]["action"], "chase-patient")
        self.assertEqual(referral.counts["chase"], 2)
        applied = referral.apply_sla_actions(now=dt(2026, 11, 28, 11, 0))
        self.assertEqual(applied[0]["action"], "return-to-retriage")
        self.assertEqual(referral.case_state, "rejected")

    def test_no_sla_action_before_deadline(self):
        referral = make_offered()
        self.assertEqual(
            referral.apply_sla_actions(now=dt(2026, 11, 25, 9, 0)), [])


class TestEscalationRecipients(unittest.TestCase):
    def test_r1_escalation_goes_to_named_roles(self):
        # C3 (revisión experta): la escalación R1 va al responsable
        # de la decisión pendiente (clínico de triaje), no a la
        # Organization de la especialidad; el emisor es el operador
        # del hub como PractitionerRole.
        registry = seed_worked_example()
        referral = Referral.create(
            registry, "REF-2026-0001", "maria-gonzalez", "rol-medico-aps",
            "cardiologia", "84114007", "routine", authored_on=CREATED,
            now=CREATED)
        referral.route(now=ROUTED)
        applied = referral.apply_sla_actions(now=dt(2026, 11, 27, 9, 0))
        self.assertEqual([a["rule"] for a in applied], ["R1"])
        escalation = [n for n in referral.notifications
                      if n["topic"]["text"] == "escalation-acceptance"][0]
        self.assertEqual(escalation["recipient"][0]["reference"],
                         "PractitionerRole/rol-triaje")
        self.assertEqual(escalation["sender"]["reference"],
                         "PractitionerRole/rol-operador-hub")
        notify_aps = [n for n in referral.notifications
                      if n["topic"]["text"]
                      == "escalation-acceptance-notify-aps"][0]
        self.assertEqual(notify_aps["recipient"][0]["reference"],
                         "PractitionerRole/rol-admin-aps")

    def test_organization_recipient_is_rejected(self):
        # C3: el builder no admite Organization como destinatario
        # (DerivacionNotificacion solo admite Patient y
        # PractitionerRole).
        from derivacion.builders import build_communication
        with self.assertRaises(ValueError):
            build_communication(
                resource_id="notificacion-x",
                notification_id="NOTIF-2026-0001-99",
                patient_id="maria-gonzalez",
                task_id="tarea-ref-2026-0001",
                trigger="accepted",
                sender_role_code="aps-admin",
                sender_role_id="rol-admin-aps",
                recipient_type="Organization",
                recipient_id="org-cardiologia",
                sent=dt(2026, 11, 19, 9, 30),
                medium="phone")


class TestBookAndReschedule(unittest.TestCase):
    def test_booking_creates_encounter_and_notifies_aps(self):
        referral = make_booked()
        self.assertEqual(referral.case_state, "scheduled")
        self.assertEqual(referral.current_appointment["status"], "booked")
        self.assertEqual(referral.slots["slot-cardiologia-1"]["status"], "busy")
        self.assertEqual(referral.encounter["status"], "planned")
        self.assertEqual(
            referral.encounter["appointment"][0]["reference"],
            "Appointment/cita-ref-2026-0001")
        booked = [n for n in referral.notifications
                  if n["topic"]["text"] == "booked"]
        self.assertEqual(len(booked), 1)
        self.assertEqual(booked[0]["sender"]["reference"],
                         "PractitionerRole/rol-operador-hub")
        self.assertEqual(booked[0]["recipient"][0]["reference"],
                         "PractitionerRole/rol-admin-aps")

    def test_reschedule_before_visit_keeps_same_appointment(self):
        referral = make_booked()
        referral.reschedule_before_visit(
            "slot-cardiologia-9", "schedule-cardiologia",
            dt(2026, 12, 4, 11, 0), dt(2026, 12, 4, 11, 30),
            now=dt(2026, 11, 26, 9, 0))
        appointment = referral.current_appointment
        self.assertEqual(appointment["id"], "cita-ref-2026-0001")
        self.assertEqual(appointment["status"], "booked")
        self.assertEqual(appointment["slot"][0]["reference"],
                         "Slot/slot-cardiologia-9")
        self.assertEqual(referral.slots["slot-cardiologia-1"]["status"], "free")
        self.assertEqual(referral.slots["slot-cardiologia-9"]["status"], "busy")
        self.assertEqual(referral.encounter["period"]["start"],
                         dt(2026, 12, 4, 11, 0).isoformat())
        self.assertEqual(referral.offer_number, 1)
        self.assertEqual(referral.case_state, "scheduled")


if __name__ == "__main__":
    unittest.main()
