"""Tests de OP-7 (consulta de estado, PI-4) y OP-8 (cancelación, PI-0…PI-3).

Fuente: operations.md (OP-7, OP-8), lifecycle.md, spec §3.7, N1.
"""

import unittest

from derivacion.transitions import ForbiddenTransition
from derivacion.workflow import Referral, WorkflowError
from tests.test_op04 import dt, make_accepted, make_booked, make_offered
from tests.test_op06 import SENT, make_completed


class TestStatusQuery(unittest.TestCase):
    def test_query_returns_state_last_change_and_next_step(self):
        referral = make_booked()
        status = referral.query_status(now=dt(2026, 12, 1, 9, 0))
        self.assertEqual(status["referral_id"], "REF-2026-0001")
        self.assertEqual(status["case_state"], "scheduled")
        self.assertEqual(status["task_status"], "ready")
        # Spec §3.7: estado actual, último cambio, próximo paso.
        self.assertEqual(status["next_step"], "visit")
        self.assertIsNotNone(status["last_modified"])
        self.assertEqual(status["last_transition"]["actor"],
                         "specialty-scheduler")
        self.assertEqual(status["service_request_status"], "active")
        self.assertFalse(status["offer_open"])
        self.assertEqual(status["counts"]["decline"], 0)

    def test_query_is_read_only(self):
        referral = make_booked()
        before = referral.query_status(now=dt(2026, 12, 1, 9, 0))
        after = referral.query_status(now=dt(2026, 12, 1, 9, 5))
        self.assertEqual(before["case_state"], after["case_state"])
        self.assertEqual(before["task_status"], after["task_status"])
        self.assertEqual(len(referral.notifications), 5)  # created, accepted,
        # offer, offer-notify-aps, booked: la consulta no notifica.


class TestCancel(unittest.TestCase):
    def test_cancel_after_acceptance_notifies_all_parties(self):
        referral = make_accepted()
        task = referral.cancel(
            now=dt(2026, 11, 22, 9, 0), reason_text="patient deceased")
        self.assertEqual(referral.case_state, "cancelled")
        self.assertEqual(task["status"], "cancelled")
        self.assertEqual(task["statusReason"]["text"], "patient deceased")
        self.assertEqual(referral.service_request["status"], "revoked")
        triggers = [n["topic"]["text"] for n in referral.notifications]
        self.assertIn("cancelled", triggers)
        self.assertIn("cancelled-notify-aps", triggers)
        self.assertIn("cancelled-notify-specialty", triggers)
        cancelled = [n for n in referral.notifications
                     if n["topic"]["text"] == "cancelled"][0]
        self.assertEqual(cancelled["sender"]["reference"],
                         "PractitionerRole/rol-operador-hub")
        self.assertEqual(cancelled["recipient"][0]["reference"],
                         "Patient/maria-gonzalez")

    def test_cancel_booked_visit_frees_slot_and_cancels_encounter(self):
        referral = make_booked()
        referral.cancel(
            now=dt(2026, 11, 26, 9, 0), reason_text="patient request")
        self.assertEqual(referral.current_appointment["status"], "cancelled")
        self.assertEqual(
            referral.current_appointment["cancelationReason"]["text"],
            "patient request")
        self.assertEqual(referral.slots["slot-cardiologia-1"]["status"], "free")
        self.assertEqual(referral.encounter["status"], "cancelled")
        self.assertEqual(referral.case_state, "cancelled")

    def test_cancel_after_counter_referral_sent_is_forbidden(self):
        referral = make_completed()
        referral.send_counter_referral(now=SENT)
        with self.assertRaises(WorkflowError):
            referral.cancel(now=dt(2026, 12, 3, 11, 0),
                            reason_text="patient request")

    def test_cancel_terminal_states_is_forbidden(self):
        referral = make_completed()
        referral.send_counter_referral(now=SENT)
        referral.acknowledge_counter_referral(now=dt(2026, 12, 3, 11, 0))
        with self.assertRaises(WorkflowError):
            referral.cancel(now=dt(2026, 12, 3, 12, 0),
                            reason_text="patient request")

    def test_cancel_without_reason_is_forbidden(self):
        referral = make_accepted()
        with self.assertRaises(WorkflowError):
            referral.cancel(now=dt(2026, 11, 22, 9, 0))

    def test_cancel_rejected_after_retriage_decision_is_forbidden(self):
        from derivacion.registry import seed_worked_example
        from tests.test_op04 import CREATED, ROUTED, ACCEPTED
        registry = seed_worked_example()
        referral = Referral.create(
            registry, "REF-2026-0001", "maria-gonzalez", "rol-medico-aps",
            "cardiologia", "84114007", "routine", authored_on=CREATED,
            now=CREATED)
        referral.route(now=ROUTED)
        referral.triage("rejected", now=ACCEPTED, reason_code="capacity")
        referral.decide_retriage("resolve-in-aps", now=dt(2026, 11, 23, 9, 0))
        with self.assertRaises(ForbiddenTransition):
            referral.cancel(now=dt(2026, 11, 23, 10, 0),
                            reason_text="patient request")


class TestReopen(unittest.TestCase):
    def _cancelled_in_received(self):
        from derivacion.registry import seed_worked_example
        from tests.test_op04 import CREATED, ROUTED
        registry = seed_worked_example()
        referral = Referral.create(
            registry, "REF-2026-0001", "maria-gonzalez", "rol-medico-aps",
            "cardiologia", "84114007", "routine", authored_on=CREATED,
            now=CREATED)
        referral.route(now=ROUTED)
        referral.cancel(now=dt(2026, 11, 20, 9, 0),
                        reason_text="duplicate referral")
        return referral

    def test_reopen_by_hub_operator_restores_pre_cancel_state(self):
        referral = self._cancelled_in_received()
        referral.reopen("received", now=dt(2026, 11, 20, 10, 0))
        self.assertEqual(referral.case_state, "received")
        self.assertEqual(referral.service_request["status"], "active")
        self.assertIsNone(referral.task.get("statusReason"))
        provenance = referral.history[-1]
        self.assertEqual(provenance["agent"][0]["who"]["reference"],
                         "PractitionerRole/rol-operador-hub")
        self.assertEqual(provenance["agent"][0]["type"]["coding"][0]["code"],
                         "hub-operator")
        # Tras la re-apertura, una cancelación legítima posterior es
        # una segunda entrada (C9 del paso 3).
        referral.cancel(now=dt(2026, 11, 20, 11, 0),
                        reason_text="patient request")
        self.assertEqual(referral.case_state, "cancelled")

    def test_reopen_by_other_role_is_forbidden(self):
        referral = self._cancelled_in_received()
        with self.assertRaises(ForbiddenTransition):
            referral.reopen("received", now=dt(2026, 11, 20, 10, 0),
                            actor_role="aps-admin")

    def test_reopen_to_other_state_is_forbidden(self):
        referral = self._cancelled_in_received()
        with self.assertRaises(WorkflowError):
            referral.reopen("accepted", now=dt(2026, 11, 20, 10, 0))

    def test_reopen_when_not_cancelled_is_forbidden(self):
        referral = make_accepted()
        with self.assertRaises(ForbiddenTransition):
            referral.reopen("received", now=dt(2026, 11, 22, 9, 0))


if __name__ == "__main__":
    unittest.main()
