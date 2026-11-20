"""Tests de los escenarios end-to-end (Plan task 11.13) y del CLI.

Los tres recorridos de la guía con el ejemplo trabajado. El Bundle
PI-0 y el Bundle PI-3 se comparan contra sus goldens de SUSHI.
"""

import json
import tempfile
import unittest
from pathlib import Path

from derivacion.cli import main, run_scenario
from derivacion.registry import seed_worked_example
from derivacion.scenarios import (
    accepted_scenario,
    no_show_scenario,
    rejected_scenario,
    summary,
)
from derivacion.workflow import Referral
from tests.golden import assert_golden
from tests.test_op01 import normalize_bundle
from tests.test_op04 import CREATED


class TestScenarios(unittest.TestCase):
    def test_accepted_scenario_closes_the_loop(self):
        referral = accepted_scenario()
        self.assertEqual(referral.case_state, "counter-referred")
        self.assertEqual(referral.task["status"], "completed")
        self.assertEqual(referral.service_request["status"], "completed")
        self.assertEqual(referral.check_invariants(), [])
        self.assertEqual(
            [a["status"] for a in referral.appointments], ["fulfilled"])
        self.assertEqual(
            [e["status"] for e in referral.encounters], ["finished"])
        assert_golden(self, referral.counter_referral_bundle,
                      "Bundle-bundle-pi3-ref-2026-0001")

    def test_pi0_bundle_matches_golden(self):
        registry = seed_worked_example()
        referral = Referral.create(
            registry, "REF-2026-0001", "maria-gonzalez", "rol-medico-aps",
            "cardiologia", "84114007", "routine", authored_on=CREATED,
            aps_encounter_id="aps-encounter-2026-11-19",
            supporting_info_ids=["ecg-2026-11-19", "ntprobnp-2026-11-19"],
            note_text="Disnea de esfuerzo y edema de tobillos de dos semanas de evolución.",
            now=CREATED)
        assert_golden(self, referral.transaction_bundle(),
                      "Bundle-bundle-pi0-ref-2026-0001",
                      normalize=normalize_bundle)

    def test_rejected_scenario_closes_as_rejected(self):
        referral = rejected_scenario()
        self.assertEqual(referral.case_state, "rejected")
        self.assertEqual(referral.service_request["status"], "revoked")
        self.assertTrue(referral.retriage_decided)
        self.assertEqual(referral.check_invariants(), [])
        self.assertEqual(referral.appointments, [])

    def test_no_show_scenario_closes_as_no_show(self):
        referral = no_show_scenario()
        self.assertEqual(referral.case_state, "no-show")
        self.assertEqual(referral.task["status"], "failed")
        self.assertEqual(referral.service_request["status"], "revoked")
        self.assertEqual(
            [a["status"] for a in referral.appointments],
            ["noshow", "noshow"])
        self.assertEqual(
            [e["status"] for e in referral.encounters],
            ["planned", "planned"])
        self.assertEqual(referral.counts["rescheduling"], 1)
        self.assertEqual(referral.check_invariants(), [])

    def test_summary_reports_invariants(self):
        result = summary(accepted_scenario())
        self.assertEqual(result["case_state"], "counter-referred")
        self.assertEqual(result["invariant_violations"], [])


class TestCli(unittest.TestCase):
    def test_cli_accepted_writes_examples(self):
        with tempfile.TemporaryDirectory() as tmp:
            referral, written = run_scenario("accepted", tmp)
            self.assertEqual(referral.case_state, "counter-referred")
            files = {p.name for p in Path(tmp).iterdir()}
            self.assertIn("summary.json", files)
            self.assertIn("Bundle-bundle-pi3-ref-2026-0001.json", files)
            self.assertIn("Task-tarea-ref-2026-0001.json", files)
            self.assertIn("ServiceRequest-ref-2026-0001.json", files)
            data = json.loads((Path(tmp) / "summary.json").read_text())
            self.assertEqual(data["case_state"], "counter-referred")
            self.assertEqual(data["invariant_violations"], [])
            self.assertEqual(len(written), len(files) - 1)

    def test_cli_main_returns_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                main(["rejected", "--out", tmp]), 0)
            data = json.loads((Path(tmp) / "summary.json").read_text())
            self.assertEqual(data["case_state"], "rejected")

    def test_cli_unknown_scenario_exits_nonzero(self):
        with self.assertRaises(SystemExit):
            main(["inexistente", "--out", "/tmp"])


if __name__ == "__main__":
    unittest.main()
