"""Tests de OP-9 (resolver identidad, PIXm/PDQm) y OP-10 (encontrar
servicio/endpoint, mCSD ITI-90) + builders base.

Fuente: operations.md (OP-9, OP-10), valuesets.fsh, examples.fsh.
El MPI y el directorio son un registro local en memoria sembrado con
el ejemplo trabajado (sin MPI ni directorio reales, la guía define
las interacciones FHIR; el componente las ejecuta contra el registro
local). Sin identidad resuelta no se crea la derivación.
"""

import unittest

from derivacion.builders import (
    build_endpoint,
    build_healthcare_service,
    build_organization,
    build_patient,
    build_practitioner,
    build_practitioner_role,
)
from derivacion.registry import (
    IdentityNotFound,
    Registry,
    ServiceNotFound,
    seed_worked_example,
)
from tests.golden import assert_golden

MARIA = {
    "resource_id": "maria-gonzalez",
    "mpi_key": "MPI-2026-0042",
    "run": "11111111-1",
    "family": "González",
    "given": "María",
    "birth_date": "1968-04-15",
    "gender": "female",
    "telecom": [{"system": "phone", "value": "+56 9 1111 1111", "use": "mobile"}],
    "address_text": "Calle Ejemplo 123, Los Aromos",
    "preferred_channel": "phone",
}


class TestPatientBuilder(unittest.TestCase):
    def test_patient_matches_golden(self):
        assert_golden(
            self, build_patient(**MARIA), "Patient-maria-gonzalez"
        )

    def test_patient_without_contact_is_rejected(self):
        # C12: los datos de contacto son obligatorios; sin ellos la
        # creación se bloquea.
        with self.assertRaises(ValueError):
            build_patient(**{**MARIA, "telecom": []})


class TestRoleServiceBuilders(unittest.TestCase):
    def test_practitioner_matches_golden(self):
        assert_golden(
            self,
            build_practitioner(
                resource_id="medico-aps",
                run="22222222-2",
                family="Pérez",
                given="Ana",
                gender="female",
            ),
            "Practitioner-medico-aps",
        )

    def test_practitioner_role_matches_golden(self):
        assert_golden(
            self,
            build_practitioner_role(
                resource_id="rol-medico-aps",
                practitioner_id="medico-aps",
                organization_id="org-cesfam-los-aromos",
                role="aps-doctor",
            ),
            "PractitionerRole-rol-medico-aps",
        )

    def test_practitioner_role_with_unknown_role_is_rejected(self):
        with self.assertRaises(ValueError):
            build_practitioner_role(
                resource_id="rol-x",
                practitioner_id="medico-aps",
                organization_id="org-cesfam-los-aromos",
                role="nurse",
            )

    def test_service_matches_golden(self):
        assert_golden(
            self,
            build_healthcare_service(
                resource_id="servicio-cardiologia",
                service_code="cardiologia",
                organization_id="org-cardiologia",
                endpoint_id="endpoint-cardiologia",
            ),
            "HealthcareService-servicio-cardiologia",
        )

    def test_endpoint_matches_golden(self):
        assert_golden(
            self,
            build_endpoint(
                resource_id="endpoint-cardiologia",
                organization_id="org-cardiologia",
                address="https://especialidad.example.org/fhir",
                name="Cardiology FHIR endpoint",
            ),
            "Endpoint-endpoint-cardiologia",
        )

    def test_organization_matches_golden(self):
        assert_golden(
            self,
            build_organization(
                resource_id="org-cesfam-los-aromos",
                system="http://aps.losaromos.example.org/organization",
                value="CESFAM-LOS-AROMOS",
                name="CESFAM Los Aromos",
            ),
            "Organization-org-cesfam-los-aromos",
        )


class TestRegistryIdentity(unittest.TestCase):
    def setUp(self):
        self.registry = seed_worked_example()

    def test_resolve_by_run_returns_mpi_key(self):
        found = self.registry.resolve_identity_by_identifier(
            "http://www.registrocivil.cl/run", "11111111-1"
        )
        self.assertEqual(found["mpi_key"], "MPI-2026-0042")
        self.assertEqual(found["patient_id"], "maria-gonzalez")

    def test_resolve_by_mpi_key_returns_patient(self):
        found = self.registry.resolve_identity_by_identifier(
            "http://mpi.red.example.org", "MPI-2026-0042"
        )
        self.assertEqual(found["patient_id"], "maria-gonzalez")

    def test_unresolved_identity_raises(self):
        with self.assertRaises(IdentityNotFound):
            self.registry.resolve_identity_by_identifier(
                "http://www.registrocivil.cl/run", "99999999-9"
            )

    def test_find_by_demographics(self):
        found = self.registry.find_patient_by_demographics(
            family="González", given="María"
        )
        self.assertEqual([p["patient_id"] for p in found], ["maria-gonzalez"])

    def test_find_by_demographics_no_match(self):
        self.assertEqual(
            self.registry.find_patient_by_demographics(family="Noexiste"),
            [],
        )


class TestRegistryDirectory(unittest.TestCase):
    def setUp(self):
        self.registry = seed_worked_example()

    def test_find_cardiology_service(self):
        service = self.registry.find_service("cardiologia")
        self.assertEqual(service["resourceType"], "HealthcareService")
        self.assertEqual(service["id"], "servicio-cardiologia")
        endpoint = self.registry.endpoint_for_service("servicio-cardiologia")
        self.assertEqual(
            endpoint["address"], "https://especialidad.example.org/fhir"
        )

    def test_service_not_in_catalogue_raises(self):
        with self.assertRaises(ServiceNotFound):
            self.registry.find_service("oftalmologia")

    def test_inactive_service_is_not_routable(self):
        registry = Registry()
        registry.add_service(
            build_healthcare_service(
                resource_id="servicio-x",
                service_code="cardiologia",
                organization_id="org-cardiologia",
                endpoint_id="endpoint-cardiologia",
                active=False,
            )
        )
        with self.assertRaises(ServiceNotFound):
            registry.find_service("cardiologia")


if __name__ == "__main__":
    unittest.main()
