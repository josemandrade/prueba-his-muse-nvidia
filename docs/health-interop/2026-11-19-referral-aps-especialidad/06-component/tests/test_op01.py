"""Tests de OP-1 (crear derivación, PI-0): ServiceRequest + Task +
Bundle de transacción.

Fuente: operations.md (OP-1), lifecycle.md, examples.fsh.
La derivación viaja como recursos: ServiceRequest + Task en un Bundle
de tipo transaction.
"""

import unittest
from datetime import datetime, timedelta, timezone

from derivacion.builders import (
    build_service_request,
    build_task,
    build_transaction_bundle,
)
from tests.golden import assert_golden

TZ = timezone(timedelta(hours=-3))
CREATED = datetime(2026, 11, 19, 9, 30, tzinfo=TZ)


def normalize_bundle(resource):
    """Normaliza los fullUrl urn:uuid: del Bundle (UUIDs frescos)."""
    import copy

    resource = copy.deepcopy(resource)
    mapping = {}
    for entry in resource.get("entry", []):
        full_url = entry.get("fullUrl", "")
        if full_url.startswith("urn:uuid:"):
            if full_url not in mapping:
                mapping[full_url] = f"urn:uuid:{len(mapping) + 1}"
            entry["fullUrl"] = mapping[full_url]
    return resource


class TestServiceRequestBuilder(unittest.TestCase):
    def test_service_request_matches_golden(self):
        assert_golden(
            self,
            build_service_request(
                resource_id="ref-2026-0001",
                referral_id="REF-2026-0001",
                patient_id="maria-gonzalez",
                aps_encounter_id="aps-encounter-2026-11-19",
                requester_role_id="rol-medico-aps",
                service_code="cardiologia",
                reason_snomed="84114007",
                reason_display="Heart failure (disorder)",
                reason_text="Suspected heart failure: exertional dyspnoea, ankle oedema",
                priority="routine",
                authored_on=CREATED,
                supporting_info_ids=["ecg-2026-11-19", "ntprobnp-2026-11-19"],
                note_text="Disnea de esfuerzo y edema de tobillos de dos semanas de evolución.",
                performer_service_id="servicio-cardiologia",
            ),
            "ServiceRequest-ref-2026-0001",
        )

    def test_priority_must_be_routine_or_urgent(self):
        with self.assertRaises(ValueError):
            build_service_request(
                resource_id="ref-x",
                referral_id="REF-X",
                patient_id="maria-gonzalez",
                aps_encounter_id=None,
                requester_role_id="rol-medico-aps",
                service_code="cardiologia",
                reason_snomed="84114007",
                reason_text="x",
                priority="stat",
                authored_on=CREATED,
            )

    def test_reason_must_be_snomed(self):
        with self.assertRaises(ValueError):
            build_service_request(
                resource_id="ref-x",
                referral_id="REF-X",
                patient_id="maria-gonzalez",
                aps_encounter_id=None,
                requester_role_id="rol-medico-aps",
                service_code="cardiologia",
                reason_snomed="no-un-codigo",
                reason_text="x",
                priority="routine",
                authored_on=CREATED,
            )


class TestTaskBuilder(unittest.TestCase):
    def test_task_matches_golden(self):
        assert_golden(
            self,
            build_task(
                resource_id="tarea-ref-2026-0001",
                referral_id="REF-2026-0001",
                patient_id="maria-gonzalez",
                requester_role_id="rol-medico-aps",
                service_request_id="ref-2026-0001",
                case_state="requested",
                description="acceptance decision",
                now=CREATED,
                deadlines={
                    "acceptance": datetime(2026, 11, 26, 17, 0, tzinfo=TZ)
                },
            ),
            "Task-tarea-ref-2026-0001",
        )

    def test_task_status_follows_case_state(self):
        task = build_task(
            resource_id="tarea-x",
            referral_id="REF-X",
            patient_id="maria-gonzalez",
            requester_role_id="rol-medico-aps",
            service_request_id="ref-x",
            case_state="scheduled",
            description="appointment offer",
            now=CREATED,
        )
        self.assertEqual(task["status"], "ready")
        self.assertEqual(task["businessStatus"]["coding"][0]["code"], "scheduled")

    def test_unknown_case_state_is_rejected(self):
        with self.assertRaises(ValueError):
            build_task(
                resource_id="tarea-x",
                referral_id="REF-X",
                patient_id="maria-gonzalez",
                requester_role_id="rol-medico-aps",
                service_request_id="ref-2026-0001",
                case_state="waiting",
                description="x",
                now=CREATED,
            )


class TestTransactionBundle(unittest.TestCase):
    def test_bundle_pi0_matches_golden(self):
        service_request = build_service_request(
            resource_id="ref-2026-0001",
            referral_id="REF-2026-0001",
            patient_id="maria-gonzalez",
            aps_encounter_id="aps-encounter-2026-11-19",
            requester_role_id="rol-medico-aps",
            service_code="cardiologia",
            reason_snomed="84114007",
            reason_display="Heart failure (disorder)",
            reason_text="Suspected heart failure: exertional dyspnoea, ankle oedema",
            priority="routine",
            authored_on=CREATED,
            supporting_info_ids=["ecg-2026-11-19", "ntprobnp-2026-11-19"],
            note_text="Disnea de esfuerzo y edema de tobillos de dos semanas de evolución.",
            performer_service_id="servicio-cardiologia",
        )
        task = build_task(
            resource_id="tarea-ref-2026-0001",
            referral_id="REF-2026-0001",
            patient_id="maria-gonzalez",
            requester_role_id="rol-medico-aps",
            service_request_id="ref-2026-0001",
            case_state="requested",
            description="acceptance decision",
            now=CREATED,
            deadlines={"acceptance": datetime(2026, 11, 26, 17, 0, tzinfo=TZ)},
        )
        bundle = build_transaction_bundle(
            [service_request, task], resource_id="bundle-pi0-ref-2026-0001"
        )
        assert_golden(
            self,
            bundle,
            "Bundle-bundle-pi0-ref-2026-0001",
            normalize=normalize_bundle,
        )

    def test_bundle_entries_are_posts_in_order(self):
        bundle = build_transaction_bundle(
            [
                {"resourceType": "ServiceRequest", "id": "a"},
                {"resourceType": "Task", "id": "b"},
            ]
        )
        self.assertEqual(bundle["type"], "transaction")
        self.assertEqual(
            [e["request"] for e in bundle["entry"]],
            [
                {"method": "POST", "url": "ServiceRequest"},
                {"method": "POST", "url": "Task"},
            ],
        )


if __name__ == "__main__":
    unittest.main()
