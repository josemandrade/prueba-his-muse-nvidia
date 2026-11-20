"""Tests de working_days.py y evaluator.py: plazos SLA R1–R5.

Fuente: rules.md (R1–R5) y lifecycle.md (los plazos no son estados:
un incumplimiento dispara una escalada, nunca un cambio de estado).
Las fechas del ejemplo trabajado: creación 2026-11-19 (jueves).
"""

import unittest
from datetime import date, datetime, timezone, timedelta

from derivacion.evaluator import evaluate_escalations, sla_deadlines
from derivacion.working_days import add_working_days, deadline_at, working_days_between

TZ = timezone(timedelta(hours=-3))


def dt(year, month, day, hour=9, minute=30):
    return datetime(year, month, day, hour, minute, tzinfo=TZ)


class TestWorkingDays(unittest.TestCase):
    def test_add_5_working_days_from_thursday(self):
        # 19 nov 2026 es jueves: 20 (1), 23 (2), 24 (3), 25 (4), 26 (5).
        self.assertEqual(add_working_days(date(2026, 11, 19), 5), date(2026, 11, 26))

    def test_add_2_working_days_skips_weekend(self):
        self.assertEqual(add_working_days(date(2026, 11, 19), 2), date(2026, 11, 23))

    def test_add_10_working_days(self):
        # Aceptación vie 20 nov: 23,24,25,26,27,30,1,2,3,4 dic.
        self.assertEqual(add_working_days(date(2026, 11, 20), 10), date(2026, 12, 4))

    def test_add_3_working_days(self):
        self.assertEqual(add_working_days(date(2026, 11, 24), 3), date(2026, 11, 27))

    def test_add_zero_is_same_day(self):
        self.assertEqual(add_working_days(date(2026, 11, 19), 0), date(2026, 11, 19))

    def test_deadline_at_1700(self):
        self.assertEqual(
            deadline_at(date(2026, 11, 26)),
            datetime(2026, 11, 26, 17, 0, tzinfo=TZ),
        )

    def test_working_days_between(self):
        self.assertEqual(
            working_days_between(date(2026, 11, 19), date(2026, 11, 26)), 5
        )
        self.assertEqual(
            working_days_between(date(2026, 11, 20), date(2026, 11, 23)), 1
        )


class TestSlaDeadlines(unittest.TestCase):
    def test_acceptance_deadline_matches_guide_example(self):
        # El ejemplo compilado: creación 2026-11-19T09:30 → plazo
        # 2026-11-26T17:00:00-03:00 (5 días hábiles, routine).
        deadlines = sla_deadlines(created=dt(2026, 11, 19), priority="routine")
        self.assertEqual(
            deadlines["acceptance"],
            datetime(2026, 11, 26, 17, 0, tzinfo=TZ),
        )

    def test_acceptance_deadline_urgent_is_2_days(self):
        deadlines = sla_deadlines(created=dt(2026, 11, 19), priority="urgent")
        self.assertEqual(
            deadlines["acceptance"],
            datetime(2026, 11, 23, 17, 0, tzinfo=TZ),
        )

    def test_offer_deadline_10_days_from_acceptance(self):
        deadlines = sla_deadlines(
            created=dt(2026, 11, 19),
            priority="routine",
            accepted_at=dt(2026, 11, 20, 11, 0),
        )
        self.assertEqual(
            deadlines["offer"], datetime(2026, 12, 4, 17, 0, tzinfo=TZ)
        )

    def test_confirmation_deadline_3_days_from_offer(self):
        deadlines = sla_deadlines(
            created=dt(2026, 11, 19),
            priority="routine",
            accepted_at=dt(2026, 11, 20, 11, 0),
            offered_at=dt(2026, 11, 24, 11, 0),
        )
        self.assertEqual(
            deadlines["confirmation"],
            datetime(2026, 11, 27, 17, 0, tzinfo=TZ),
        )

    def test_counterreferral_deadline_from_encounter_finished(self):
        deadlines = sla_deadlines(
            created=dt(2026, 11, 19),
            priority="routine",
            encounter_finished_at=dt(2026, 12, 2, 10, 30),
        )
        self.assertEqual(
            deadlines["counterreferral"],
            datetime(2026, 12, 9, 17, 0, tzinfo=TZ),
        )

    def test_retriage_deadline_from_rejection(self):
        deadlines = sla_deadlines(
            created=dt(2026, 11, 19),
            priority="routine",
            rejected_at=dt(2026, 11, 20, 15, 0),
        )
        self.assertEqual(
            deadlines["retriage"], datetime(2026, 11, 27, 17, 0, tzinfo=TZ)
        )

    def test_no_deadline_without_its_trigger(self):
        deadlines = sla_deadlines(created=dt(2026, 11, 19), priority="routine")
        self.assertIsNone(deadlines["offer"])
        self.assertIsNone(deadlines["confirmation"])
        self.assertIsNone(deadlines["counterreferral"])
        self.assertIsNone(deadlines["retriage"])


class TestEscalations(unittest.TestCase):
    def _state(self, **overrides):
        state = {
            "case_state": "requested",
            "priority": "routine",
            "created_at": dt(2026, 11, 19),
            "accepted_at": None,
            "offered_at": None,
            "offer_open": False,
            "chase_count": 0,
            "encounter_finished_at": None,
            "rejected_at": None,
            "retriage_decided": False,
            "counter_referral_sent": False,
            "escalations_fired": set(),
        }
        state.update(overrides)
        return state

    def test_r1_fires_after_acceptance_deadline(self):
        actions = evaluate_escalations(
            self._state(), now=dt(2026, 11, 27, 9, 0)
        )
        self.assertEqual([a["rule"] for a in actions], ["R1"])
        self.assertEqual(actions[0]["action"], "escalate-specialty-notify-aps")

    def test_r1_does_not_fire_before_deadline(self):
        self.assertEqual(
            evaluate_escalations(self._state(), now=dt(2026, 11, 26, 16, 0)),
            [],
        )

    def test_r1_fires_once(self):
        state = self._state(escalations_fired={"R1"})
        self.assertEqual(
            evaluate_escalations(state, now=dt(2026, 11, 27, 9, 0)), []
        )

    def test_r1_disarmed_by_triage_decision(self):
        state = self._state(case_state="accepted", accepted_at=dt(2026, 11, 20, 11, 0))
        self.assertEqual(
            evaluate_escalations(state, now=dt(2026, 11, 27, 9, 0)), []
        )

    def test_r2_fires_after_offer_deadline(self):
        state = self._state(
            case_state="accepted",
            accepted_at=dt(2026, 11, 20, 11, 0),
        )
        actions = evaluate_escalations(state, now=dt(2026, 12, 5, 9, 0))
        self.assertEqual([a["rule"] for a in actions], ["R2"])

    def test_r3_chases_patient(self):
        state = self._state(
            case_state="accepted",
            accepted_at=dt(2026, 11, 20, 11, 0),
            offered_at=dt(2026, 11, 24, 11, 0),
            offer_open=True,
            chase_count=0,
        )
        actions = evaluate_escalations(state, now=dt(2026, 11, 28, 9, 0))
        self.assertEqual([a["rule"] for a in actions], ["R3"])
        self.assertEqual(actions[0]["action"], "chase-patient")

    def test_r3_returns_to_retriage_after_second_chase(self):
        state = self._state(
            case_state="accepted",
            accepted_at=dt(2026, 11, 20, 11, 0),
            offered_at=dt(2026, 11, 24, 11, 0),
            offer_open=True,
            chase_count=2,
        )
        actions = evaluate_escalations(state, now=dt(2026, 11, 28, 9, 0))
        self.assertEqual(actions[0]["action"], "return-to-retriage")

    def test_r4_fires_after_counterreferral_deadline(self):
        state = self._state(
            case_state="completed",
            encounter_finished_at=dt(2026, 12, 2, 10, 30),
        )
        actions = evaluate_escalations(state, now=dt(2026, 12, 10, 9, 0))
        self.assertEqual([a["rule"] for a in actions], ["R4"])

    def test_r4_disarmed_by_sending_counterreferral(self):
        state = self._state(
            case_state="counter-referred",
            encounter_finished_at=dt(2026, 12, 2, 10, 30),
            counter_referral_sent=True,
        )
        self.assertEqual(
            evaluate_escalations(state, now=dt(2026, 12, 10, 9, 0)), []
        )

    def test_r5_fires_after_retriage_deadline(self):
        state = self._state(
            case_state="rejected",
            rejected_at=dt(2026, 11, 20, 15, 0),
            retriage_decided=False,
        )
        actions = evaluate_escalations(state, now=dt(2026, 11, 28, 9, 0))
        self.assertEqual([a["rule"] for a in actions], ["R5"])
        self.assertEqual(actions[0]["recipients"], ["aps-admin"])

    def test_r5_fires_after_scheduling_failure_return(self):
        # C1 (revisión experta): el retorno por fallo de agendamiento
        # (segundo rechazo o R3) también dispara el plazo de re-triaje;
        # antes el evaluador no recibía `retriage_return_at` y R5 no
        # se evaluaba nunca en este camino.
        state = self._state(
            case_state="rejected",
            rejected_at=None,
            retriage_return_at=dt(2026, 11, 24, 15, 0),
            retriage_decided=False,
        )
        self.assertEqual(
            evaluate_escalations(state, now=dt(2026, 12, 1, 9, 0)), []
        )
        actions = evaluate_escalations(state, now=dt(2026, 12, 2, 9, 0))
        self.assertEqual([a["rule"] for a in actions], ["R5"])
        self.assertEqual(actions[0]["recipients"], ["aps-admin"])

    def test_evaluation_never_changes_state(self):
        state = self._state()
        evaluate_escalations(state, now=dt(2026, 11, 27, 9, 0))
        self.assertEqual(state["case_state"], "requested")
        self.assertEqual(state["escalations_fired"], set())


if __name__ == "__main__":
    unittest.main()
