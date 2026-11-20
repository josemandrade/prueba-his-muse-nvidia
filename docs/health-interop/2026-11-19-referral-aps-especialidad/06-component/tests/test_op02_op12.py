"""Tests de OP-2 (registrar la decisión de triaje, PI-1) y OP-12
(notificar un cambio de estado) + Provenance.

Fuente: operations.md (OP-2, OP-12), communication.fsh,
mapping.md ("Correcciones R4"): `Task.owner` es 0..1, el servicio
que acepta; el profesional que acepta va como agente de Provenance
en la entrada de aceptación. `Communication.topic` es CodeableConcept
(el nombre codificado de la transición); el enlace al Task es
`basedOn` y el aviso legible es `payload.contentString`.
"""

import unittest
from datetime import datetime, timedelta, timezone

from derivacion.builders import build_communication, build_provenance, build_task
from tests.golden import assert_golden

TZ = timezone(timedelta(hours=-3))
NOW = datetime(2026, 11, 21, 9, 0, tzinfo=TZ)


class TestCommunicationBuilder(unittest.TestCase):
    def test_acceptance_notification_matches_golden(self):
        assert_golden(
            self,
            build_communication(
                resource_id="notificacion-aceptacion-ref-2026-0001",
                notification_id="NOTIF-2026-0001",
                patient_id="maria-gonzalez",
                task_id="tarea-ref-2026-0001",
                trigger="accepted",
                sender_role_code="aps-admin",
                sender_role_id="rol-admin-aps",
                recipient_type="Patient",
                recipient_id="maria-gonzalez",
                sent=NOW,
                medium="phone",
                message="Su derivación a cardiología fue aceptada. Le ofreceremos una cita en los próximos días.",
                delivery_outcome="delivered",
            ),
            "Communication-notificacion-aceptacion-ref-2026-0001",
        )

    def test_sender_must_be_a_named_role(self):
        with self.assertRaises(ValueError):
            build_communication(
                resource_id="notif-x",
                notification_id="NOTIF-X",
                patient_id="maria-gonzalez",
                task_id="tarea-ref-2026-0001",
                trigger="accepted",
                sender_role_code="nurse",
                sender_role_id="rol-enfermera",
                recipient_type="Patient",
                recipient_id="maria-gonzalez",
                sent=NOW,
                medium="phone",
                message="x",
            )

    def test_medium_must_be_a_local_channel(self):
        with self.assertRaises(ValueError):
            build_communication(
                resource_id="notif-x",
                notification_id="NOTIF-X",
                patient_id="maria-gonzalez",
                task_id="tarea-ref-2026-0001",
                trigger="accepted",
                sender_role_code="aps-admin",
                sender_role_id="rol-admin-aps",
                recipient_type="Patient",
                recipient_id="maria-gonzalez",
                sent=NOW,
                medium="smoke-signal",
                message="x",
            )

    def test_delivery_outcome_must_be_local_value(self):
        with self.assertRaises(ValueError):
            build_communication(
                resource_id="notif-x",
                notification_id="NOTIF-X",
                patient_id="maria-gonzalez",
                task_id="tarea-ref-2026-0001",
                trigger="accepted",
                sender_role_code="aps-admin",
                sender_role_id="rol-admin-aps",
                recipient_type="Patient",
                recipient_id="maria-gonzalez",
                sent=NOW,
                medium="phone",
                message="x",
                delivery_outcome="maybe",
            )


class TestProvenanceBuilder(unittest.TestCase):
    def test_acceptance_provenance(self):
        provenance = build_provenance(
            resource_id="provenance-aceptacion-ref-2026-0001",
            task_id="tarea-ref-2026-0001",
            actor_role_id="rol-triaje",
            role_code="triage-clinician",
            recorded=NOW,
        )
        self.assertEqual(provenance["resourceType"], "Provenance")
        self.assertEqual(
            provenance["target"],
            [{"reference": "Task/tarea-ref-2026-0001"}],
        )
        agent = provenance["agent"][0]
        self.assertEqual(
            agent["type"]["coding"][0]["code"], "triage-clinician"
        )
        self.assertEqual(
            agent["who"], {"reference": "PractitionerRole/rol-triaje"}
        )
        self.assertEqual(provenance["recorded"], "2026-11-21T09:00:00-03:00")


class TestOwnerRule(unittest.TestCase):
    def test_owner_is_the_service_not_the_professional(self):
        # Corrección R4 (paso 5): Task.owner 0..1, el servicio que
        # acepta; el profesional va como agente de Provenance.
        task = build_task(
            resource_id="tarea-x",
            referral_id="REF-X",
            patient_id="maria-gonzalez",
            requester_role_id="rol-medico-aps",
            service_request_id="ref-x",
            case_state="accepted",
            description="appointment offer",
            now=NOW,
            owner_service_id="servicio-cardiologia",
        )
        self.assertEqual(
            task["owner"],
            {"reference": "HealthcareService/servicio-cardiologia"},
        )


if __name__ == "__main__":
    unittest.main()
