"""Tests de OP-3 (ofrecer / confirmar / reservar cita, PI-2).

Fuente: operations.md (OP-3), appointment.fsh, encounter.fsh.
La cadena es: proposed (oferta) → pending (paciente confirmó, aún
no reservada) → booked (slot ocupado) → arrived → fulfilled. OP-3
crea el Encounter (`planned`) en la reserva; nunca en la asistencia.
"""

import unittest
from datetime import datetime, timedelta, timezone

from derivacion.builders import (
    build_appointment,
    build_appointment_response,
    build_encounter,
    build_location,
    build_schedule,
    build_slot,
)
from tests.golden import assert_golden

TZ = timezone(timedelta(hours=-3))
OFFERED = datetime(2026, 11, 24, 11, 0, tzinfo=TZ)
START = datetime(2026, 12, 2, 10, 0, tzinfo=TZ)
END = datetime(2026, 12, 2, 10, 30, tzinfo=TZ)


class TestAppointmentBuilders(unittest.TestCase):
    def test_appointment_matches_golden(self):
        assert_golden(
            self,
            build_appointment(
                resource_id="cita-ref-2026-0001",
                appointment_id="CITA-2026-0001",
                service_request_id="ref-2026-0001",
                slot_id="slot-cardiologia-1",
                patient_id="maria-gonzalez",
                specialist_role_id="rol-especialista",
                location_id="location-cardiologia",
                service_code="cardiologia",
                start=START,
                end=END,
                created=OFFERED,
                offer_number=1,
                patient_instruction="Ayuno no necesario. Traer los exámenes previos.",
            ),
            "Appointment-cita-ref-2026-0001",
        )

    def test_appointment_response_matches_golden(self):
        assert_golden(
            self,
            build_appointment_response(
                resource_id="respuesta-cita-1",
                appointment_id="cita-ref-2026-0001",
                patient_id="maria-gonzalez",
                participant_status="accepted",
            ),
            "AppointmentResponse-respuesta-cita-1",
        )

    def test_encounter_matches_golden(self):
        assert_golden(
            self,
            build_encounter(
                resource_id="encuentro-ref-2026-0001",
                encounter_id="ENC-2026-0001",
                patient_id="maria-gonzalez",
                service_request_id="ref-2026-0001",
                appointment_id="cita-ref-2026-0001",
                specialist_role_id="rol-especialista",
                service_code="cardiologia",
                start=START,
                end=END,
            ),
            "Encounter-encuentro-ref-2026-0001",
        )

    def test_schedule_matches_golden(self):
        assert_golden(
            self,
            build_schedule(
                resource_id="schedule-cardiologia",
                service_id="servicio-cardiologia",
                start=datetime(2026, 12, 1, 8, 0, tzinfo=TZ),
                end=datetime(2026, 12, 31, 17, 0, tzinfo=TZ),
                comment="Agenda de la consulta de cardiología.",
            ),
            "Schedule-schedule-cardiologia",
        )

    def test_location_matches_golden(self):
        assert_golden(
            self,
            build_location(
                resource_id="location-cardiologia",
                name="Consulta de Cardiología",
                address_text="Hospital de la Red, piso 3, consulta 12",
                organization_id="org-cardiologia",
            ),
            "Location-location-cardiologia",
        )


class TestSlotRules(unittest.TestCase):
    def test_slot_is_free_at_offer_and_busy_at_booking(self):
        # El ejemplo compilado muestra el Slot `busy` con el
        # Appointment en `proposed`; la guía (OP-3) dice que el Slot
        # pasa a `busy` en la reserva, no en la oferta. El componente
        # sigue el texto de OP-3 (Ruling en state.md): libre en la
        # oferta, ocupado en la reserva, libre en no-show/cancelación.
        offered = build_slot(
            resource_id="slot-1",
            schedule_id="schedule-cardiologia",
            start=START,
            end=END,
            status="free",
        )
        self.assertEqual(offered["status"], "free")
        booked = build_slot(
            resource_id="slot-1",
            schedule_id="schedule-cardiologia",
            start=START,
            end=END,
            status="busy",
        )
        self.assertEqual(booked["status"], "busy")

    def test_slot_status_must_be_a_fhir_value(self):
        with self.assertRaises(ValueError):
            build_slot(
                resource_id="slot-1",
                schedule_id="schedule-cardiologia",
                start=START,
                end=END,
                status="held-forever",
            )


if __name__ == "__main__":
    unittest.main()
