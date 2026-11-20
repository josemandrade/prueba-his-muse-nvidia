"""Tests de OP-5 (asistencia / no-show, PI-2).

Fuente: operations.md (OP-5), lifecycle.md, mapeo §5/§6, I4.
"""

import unittest
from datetime import datetime, timedelta, timezone

from derivacion.workflow import Referral, WorkflowError
from tests.test_op04 import (
    TZ,
    dt,
    make_accepted,
    make_booked,
    make_offered,
    task_extensions,
)


class TestAttendance(unittest.TestCase):
    def test_arrival_then_finish_completes_the_visit(self):
        referral = make_booked()
        referral.record_arrival(now=dt(2026, 12, 2, 10, 0))
        self.assertEqual(referral.current_appointment["status"], "arrived")
        self.assertEqual(referral.encounter["status"], "in-progress")
        # El Task NO avanza con la llegada: avanza con el fin (C9).
        self.assertEqual(referral.case_state, "scheduled")
        referral.finish_encounter(now=dt(2026, 12, 2, 10, 30))
        self.assertEqual(referral.current_appointment["status"], "fulfilled")
        self.assertEqual(referral.encounter["status"], "finished")
        self.assertEqual(referral.case_state, "completed")
        self.assertIn("sla-counterreferral-deadline",
                      task_extensions(referral.task))
        self.assertEqual(referral.service_request["status"], "active")
        self.assertEqual(referral.check_invariants(), [])

    def test_finish_without_arrival_is_forbidden(self):
        referral = make_booked()
        with self.assertRaises(Exception):
            referral.finish_encounter(now=dt(2026, 12, 2, 10, 30))

    def test_arrival_without_booking_is_forbidden(self):
        referral = make_offered()
        with self.assertRaises(WorkflowError):
            referral.record_arrival(now=dt(2026, 12, 2, 10, 0))


class TestNoShow(unittest.TestCase):
    def test_first_no_show_keeps_task_and_frees_slot(self):
        referral = make_booked()
        referral.record_no_show(now=dt(2026, 12, 2, 10, 15))
        appointment = referral.current_appointment
        self.assertEqual(appointment["status"], "noshow")
        self.assertEqual(appointment["cancelationReason"]["text"],
                         "patient did not attend")
        self.assertEqual(referral.slots["slot-cardiologia-1"]["status"], "free")
        # El Task no se mueve en el primer no-show.
        self.assertEqual(referral.case_state, "scheduled")
        # El conteo mide re-agendamientos: aún no se usó ninguno.
        self.assertEqual(referral.counts["rescheduling"], 0)
        # El Encounter planned queda como está (Ruling 11.9); I4 no
        # lo marca como violación.
        self.assertEqual(referral.encounter["status"], "planned")
        self.assertEqual(referral.check_invariants(), [])
        note = [n for n in referral.notifications
                if n["topic"]["text"] == "no-show"][0]
        self.assertEqual(note["sender"]["reference"],
                         "PractitionerRole/rol-especialista")
        self.assertEqual(note["recipient"][0]["reference"],
                         "PractitionerRole/rol-admin-aps")

    def test_reschedule_after_first_no_show_starts_a_new_cycle(self):
        referral = make_booked()
        referral.record_no_show(now=dt(2026, 12, 2, 10, 15))
        referral.reschedule_after_no_show(
            "slot-cardiologia-2", "schedule-cardiologia",
            dt(2026, 12, 9, 10, 0), dt(2026, 12, 9, 10, 30),
            now=dt(2026, 12, 3, 9, 0))
        self.assertEqual(referral.offer_number, 2)
        self.assertEqual(referral.current_appointment["status"], "proposed")
        # Ciclo nuevo (N5): los conteos de decline/chase se reinician;
        # el de re-agendamiento, no.
        self.assertEqual(referral.counts["decline"], 0)
        self.assertEqual(referral.counts["chase"], 0)
        self.assertEqual(referral.counts["rescheduling"], 1)
        self.assertEqual(referral.case_state, "scheduled")
        # La reserva del re-agendamiento crea un Encounter NUEVO; el
        # planned de la cita perdida queda en la historia.
        referral.respond_to_offer("accepted", now=dt(2026, 12, 4, 9, 0))
        referral.book_appointment(now=dt(2026, 12, 4, 10, 0))
        self.assertEqual(len(referral.encounters), 2)
        self.assertEqual(referral.encounter["id"],
                         "encuentro-ref-2026-0001-oferta-2")
        self.assertEqual(referral.encounters[0]["status"], "planned")
        self.assertEqual(referral.encounter["status"], "planned")

    def test_second_no_show_closes_the_referral(self):
        referral = make_booked()
        referral.record_no_show(now=dt(2026, 12, 2, 10, 15))
        referral.reschedule_after_no_show(
            "slot-cardiologia-2", "schedule-cardiologia",
            dt(2026, 12, 9, 10, 0), dt(2026, 12, 9, 10, 30),
            now=dt(2026, 12, 3, 9, 0))
        referral.respond_to_offer("accepted", now=dt(2026, 12, 4, 9, 0))
        referral.book_appointment(now=dt(2026, 12, 4, 10, 0))
        referral.record_no_show(now=dt(2026, 12, 9, 10, 15))
        self.assertEqual(referral.case_state, "no-show")
        self.assertEqual(referral.task["status"], "failed")
        self.assertEqual(referral.service_request["status"], "revoked")
        self.assertEqual(referral.check_invariants(), [])
        with self.assertRaises(WorkflowError):
            referral.reschedule_after_no_show(
                "slot-cardiologia-3", "schedule-cardiologia",
                dt(2026, 12, 16, 10, 0), dt(2026, 12, 16, 10, 30),
                now=dt(2026, 12, 10, 9, 0))

    def test_no_show_without_booking_is_forbidden(self):
        referral = make_offered()
        with self.assertRaises(WorkflowError):
            referral.record_no_show(now=dt(2026, 12, 2, 10, 15))


if __name__ == "__main__":
    unittest.main()
