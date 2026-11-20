"""Tests de transitions.py: las 5 máquinas + invariantes I1–I6.

Fuente: lifecycle.md. Cada transición permitida tiene su test y cada
transición prohibida tiene su test de transición prohibida.
"""

import unittest

from derivacion.transitions import (
    ForbiddenTransition,
    check_invariants,
    validate_appointment_transition,
    validate_careplan_transition,
    validate_encounter_transition,
    validate_service_request_transition,
    validate_task_transition,
)


class TestTaskMachine(unittest.TestCase):
    def test_happy_path(self):
        for current, nxt in [
            ("requested", "received"),
            ("received", "accepted"),
            ("accepted", "scheduled"),
            ("scheduled", "completed"),
            ("completed", "counter-referred"),
        ]:
            validate_task_transition(current, nxt)

    def test_requested_cannot_be_accepted_before_received(self):
        with self.assertRaises(ForbiddenTransition):
            validate_task_transition("requested", "accepted")

    def test_received_cannot_be_scheduled_before_triage(self):
        with self.assertRaises(ForbiddenTransition):
            validate_task_transition("received", "scheduled")

    def test_accepted_cannot_complete_before_visit(self):
        with self.assertRaises(ForbiddenTransition):
            validate_task_transition("accepted", "completed")

    def test_accepted_to_rejected_only_on_scheduling_failure(self):
        # Ruling (Plan task 11.8): el retorno por fallo de
        # agendamiento mueve accepted → rejected; un rechazo de
        # triaje es received → rejected (OP-2), nunca accepted.
        with self.assertRaises(ForbiddenTransition):
            validate_task_transition("accepted", "rejected")
        validate_task_transition(
            "accepted", "rejected", scheduling_failure=True
        )

    def test_scheduled_no_show_is_not_a_task_transition(self):
        # El no-show vive en el Appointment; el Task no se mueve en el
        # primer no-show (lifecycle.md).
        with self.assertRaises(ForbiddenTransition):
            validate_task_transition("scheduled", "no-show")

    def test_scheduled_to_no_show_only_on_second_no_show(self):
        # El Task sí se mueve en el segundo no-show (OP-5).
        validate_task_transition(
            "scheduled", "no-show", second_no_show=True)

    def test_completed_cannot_go_back_to_scheduled(self):
        with self.assertRaises(ForbiddenTransition):
            validate_task_transition("completed", "scheduled")

    def test_terminal_counter_referred_rejects_everything(self):
        for nxt in ("scheduled", "accepted", "cancelled", "requested"):
            with self.assertRaises(ForbiddenTransition):
                validate_task_transition("counter-referred", nxt)

    def test_terminal_no_show_rejects_everything(self):
        with self.assertRaises(ForbiddenTransition):
            validate_task_transition("no-show", "scheduled")

    def test_rejected_can_be_cancelled_before_retriage_decision(self):
        validate_task_transition("rejected", "cancelled")

    def test_rejected_cannot_be_cancelled_after_retriage_decision(self):
        with self.assertRaises(ForbiddenTransition):
            validate_task_transition("rejected", "cancelled", retriage_decided=True)

    def test_rejected_never_advances(self):
        for nxt in ("scheduled", "completed", "counter-referred", "accepted"):
            with self.assertRaises(ForbiddenTransition):
                validate_task_transition("rejected", nxt)

    def test_cancelled_has_no_outgoing_transition(self):
        with self.assertRaises(ForbiddenTransition):
            validate_task_transition("cancelled", "requested")

    def test_cancelled_can_be_reopened_only_by_hub_operator(self):
        from derivacion.transitions import validate_reopen

        validate_reopen("cancelled", "scheduled", actor_role="hub-operator")
        with self.assertRaises(ForbiddenTransition):
            validate_reopen("cancelled", "scheduled", actor_role="aps-admin")
        with self.assertRaises(ForbiddenTransition):
            validate_reopen("requested", "scheduled", actor_role="hub-operator")

    def test_forbidden_carries_409(self):
        try:
            validate_task_transition("counter-referred", "scheduled")
        except ForbiddenTransition as err:
            self.assertEqual(err.status, 409)
            self.assertEqual(err.machine, "Task")
            self.assertEqual(err.current, "counter-referred")
            self.assertEqual(err.attempted, "scheduled")
        else:
            self.fail("no se lanzó ForbiddenTransition")


class TestServiceRequestMachine(unittest.TestCase):
    def test_happy_path(self):
        validate_service_request_transition("draft", "active")
        validate_service_request_transition("active", "completed")
        validate_service_request_transition("active", "revoked")

    def test_draft_cannot_complete(self):
        with self.assertRaises(ForbiddenTransition):
            validate_service_request_transition("draft", "completed")

    def test_active_cannot_go_back_to_draft_or_on_hold(self):
        for nxt in ("draft", "on-hold"):
            with self.assertRaises(ForbiddenTransition):
                validate_service_request_transition("active", nxt)

    def test_terminal_states_reject_everything(self):
        for current in ("completed", "revoked"):
            with self.assertRaises(ForbiddenTransition):
                validate_service_request_transition(current, "active")


class TestAppointmentMachine(unittest.TestCase):
    def test_happy_path(self):
        for current, nxt in [
            ("proposed", "pending"),
            ("pending", "booked"),
            ("booked", "arrived"),
            ("arrived", "fulfilled"),
        ]:
            validate_appointment_transition(current, nxt)

    def test_proposed_cannot_be_booked_before_confirmation(self):
        with self.assertRaises(ForbiddenTransition):
            validate_appointment_transition("proposed", "booked")

    def test_pending_cannot_go_back_to_proposed_or_noshow(self):
        for nxt in ("proposed", "noshow"):
            with self.assertRaises(ForbiddenTransition):
                validate_appointment_transition("pending", nxt)

    def test_booked_can_change_slot_staying_booked(self):
        # Re-agendamiento tras un conflicto previo a la asistencia:
        # mismo Appointment, nuevo Slot (OP-4).
        validate_appointment_transition("booked", "booked")

    def test_booked_cannot_go_back_to_proposed_or_pending(self):
        for nxt in ("proposed", "pending"):
            with self.assertRaises(ForbiddenTransition):
                validate_appointment_transition("booked", nxt)

    def test_noshow_never_reused(self):
        for nxt in ("booked", "arrived", "fulfilled"):
            with self.assertRaises(ForbiddenTransition):
                validate_appointment_transition("noshow", nxt)

    def test_arrived_only_goes_to_fulfilled(self):
        with self.assertRaises(ForbiddenTransition):
            validate_appointment_transition("arrived", "cancelled")


class TestEncounterMachine(unittest.TestCase):
    def test_happy_path(self):
        validate_encounter_transition("planned", "in-progress")
        validate_encounter_transition("in-progress", "finished")

    def test_planned_cannot_finish_before_starting(self):
        with self.assertRaises(ForbiddenTransition):
            validate_encounter_transition("planned", "finished")

    def test_in_progress_cannot_be_cancelled_or_unstarted(self):
        for nxt in ("planned", "cancelled"):
            with self.assertRaises(ForbiddenTransition):
                validate_encounter_transition("in-progress", nxt)

    def test_finished_is_terminal(self):
        with self.assertRaises(ForbiddenTransition):
            validate_encounter_transition("finished", "in-progress")


class TestCarePlanMachine(unittest.TestCase):
    def test_happy_path(self):
        validate_careplan_transition("draft", "active")
        validate_careplan_transition("active", "completed")
        validate_careplan_transition("active", "revoked")

    def test_active_cannot_go_back_to_draft(self):
        with self.assertRaises(ForbiddenTransition):
            validate_careplan_transition("active", "draft")

    def test_terminal_states_reject_everything(self):
        for current in ("completed", "revoked"):
            with self.assertRaises(ForbiddenTransition):
                validate_careplan_transition(current, "active")


class TestInvariants(unittest.TestCase):
    def _state(self, **overrides):
        state = {
            "case_state": "accepted",
            "retriage_decided": False,
            "service_request_status": "active",
            "appointments": [],
            "encounter_status": None,
            "encounter_created_at": None,
        }
        state.update(overrides)
        return state

    def test_i1_consistent_accepted_active(self):
        self.assertEqual(check_invariants(self._state()), [])

    def test_i1_task_accepted_with_sr_revoked_is_inconsistent(self):
        violations = check_invariants(
            self._state(service_request_status="revoked")
        )
        self.assertTrue(any(v.startswith("I1") for v in violations))

    def test_i6_rejected_closed_with_sr_active_is_inconsistent(self):
        violations = check_invariants(
            self._state(
                case_state="rejected",
                retriage_decided=True,
                service_request_status="active",
            )
        )
        self.assertTrue(any(v.startswith("I6") for v in violations))

    def test_i6_rejected_pending_with_sr_active_is_consistent(self):
        self.assertEqual(
            check_invariants(
                self._state(
                    case_state="rejected",
                    retriage_decided=False,
                    service_request_status="active",
                )
            ),
            [],
        )

    def test_i1_counter_referred_requires_sr_completed(self):
        violations = check_invariants(
            self._state(
                case_state="counter-referred",
                service_request_status="active",
            )
        )
        self.assertTrue(any(v.startswith("I1") for v in violations))

    def test_i4_no_encounter_on_noshow(self):
        # Un Encounter creado en la asistencia es inconsistente.
        violations = check_invariants(
            self._state(
                case_state="scheduled",
                appointments=[{"status": "noshow"}],
                encounter_status="in-progress",
                encounter_created_at="attendance",
            )
        )
        self.assertTrue(any(v.startswith("I4") for v in violations))

    def test_i4_encounter_from_booking_is_consistent(self):
        self.assertEqual(
            check_invariants(
                self._state(
                    case_state="scheduled",
                    encounter_status="planned",
                    encounter_created_at="booking",
                )
            ),
            [],
        )


if __name__ == "__main__":
    unittest.main()
