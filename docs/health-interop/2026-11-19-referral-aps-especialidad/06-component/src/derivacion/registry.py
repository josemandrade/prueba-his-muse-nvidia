"""Registro local en memoria: MPI (OP-9) y directorio de servicios (OP-10).

La guía define las interacciones FHIR (PIXm ITI-83 / PDQm ITI-78 /
mCSD ITI-90); sin MPI ni directorio reales, el componente las ejecuta
contra este registro local, sembrado con el ejemplo trabajado. Sin
identidad resuelta no se crea la derivación.
"""

from derivacion.builders import (
    build_endpoint,
    build_healthcare_service,
    build_organization,
    build_patient,
    build_practitioner,
    build_practitioner_role,
)
from derivacion.constants import MPI_SYSTEM, RUN_SYSTEM


class IdentityNotFound(ValueError):
    """La identidad no se resolvió en el MPI (OP-9)."""


class ServiceNotFound(ValueError):
    """El servicio no está en el catálogo local o no acepta (OP-10)."""


class Registry:
    """Pacientes (MPI), servicios, endpoints y roles del registro local."""

    def __init__(self):
        self.patients = {}
        self.services = {}
        self.endpoints = {}
        self.practitioners = {}
        self.roles = {}

    def add_patient(self, patient):
        self.patients[patient["id"]] = patient

    def add_service(self, service):
        self.services[service["id"]] = service

    def add_endpoint(self, endpoint):
        self.endpoints[endpoint["id"]] = endpoint

    def add_practitioner(self, practitioner):
        self.practitioners[practitioner["id"]] = practitioner

    def add_role(self, role):
        self.roles[role["id"]] = role

    def _mpi_key_of(self, patient):
        for identifier in patient.get("identifier", []):
            if identifier.get("system") == MPI_SYSTEM:
                return identifier["value"]
        return None

    def resolve_identity_by_identifier(self, system, value):
        """PIXm ITI-83 (`$ihe-pix`): devuelve la clave MPI.

        Acepta el RUN o la propia clave MPI. Sin cruce, lanza
        `IdentityNotFound`: sin identidad resuelta no se crea la
        derivación.
        """
        for patient in self.patients.values():
            for identifier in patient.get("identifier", []):
                if identifier.get("system") == system and identifier.get(
                    "value"
                ) == value:
                    return {
                        "patient_id": patient["id"],
                        "mpi_key": self._mpi_key_of(patient),
                    }
        raise IdentityNotFound(f"sin cruce de identidad para {system}|{value}")

    def find_patient_by_demographics(self, family, given=None):
        """PDQm ITI-78: encuentra pacientes por demográficos."""
        found = []
        for patient in self.patients.values():
            for name in patient.get("name", []):
                if name.get("family") != family:
                    continue
                if given is not None and given not in name.get("given", []):
                    continue
                found.append(
                    {
                        "patient_id": patient["id"],
                        "mpi_key": self._mpi_key_of(patient),
                    }
                )
        return found

    def find_service(self, service_code):
        """mCSD ITI-90: el servicio solicitado y su endpoint.

        El hub solo enruta a servicios que el directorio lista como
        aceptantes (`active = true`).
        """
        for service in self.services.values():
            for type_ in service.get("type", []):
                for coding in type_.get("coding", []):
                    if coding.get("code") == service_code:
                        if not service.get("active"):
                            raise ServiceNotFound(
                                f"el servicio {service_code!r} no acepta "
                                "derivaciones"
                            )
                        return service
        raise ServiceNotFound(
            f"el servicio {service_code!r} no está en el catálogo local"
        )

    def endpoint_for_service(self, service_id):
        service = self.services[service_id]
        for endpoint_ref in service.get("endpoint", []):
            endpoint_id = endpoint_ref["reference"].split("/", 1)[1]
            return self.endpoints[endpoint_id]
        raise ServiceNotFound(f"el servicio {service_id!r} no tiene endpoint")


def seed_worked_example():
    """El registro sembrado con el ejemplo trabajado de la guía."""
    registry = Registry()
    registry.add_patient(
        build_patient(
            resource_id="maria-gonzalez",
            mpi_key="MPI-2026-0042",
            run="11111111-1",
            family="González",
            given="María",
            birth_date="1968-04-15",
            gender="female",
            telecom=[
                {"system": "phone", "value": "+56 9 1111 1111", "use": "mobile"}
            ],
            address_text="Calle Ejemplo 123, Los Aromos",
            preferred_channel="phone",
        )
    )
    registry.add_service(
        build_healthcare_service(
            resource_id="servicio-cardiologia",
            service_code="cardiologia",
            organization_id="org-cardiologia",
            endpoint_id="endpoint-cardiologia",
        )
    )
    registry.add_endpoint(
        build_endpoint(
            resource_id="endpoint-cardiologia",
            organization_id="org-cardiologia",
            address="https://especialidad.example.org/fhir",
            name="Cardiology FHIR endpoint",
        )
    )
    # Operador del hub (C3, revisión experta del paso 6): el rol
    # `hub-operator` existe en el DerivacionRolCS de la guía, pero sus
    # ejemplos no lo materializan; el componente lo siembra aquí para
    # que emisor y destinatario del hub sean un PractitionerRole, como
    # exige DerivacionNotificacion. RUN sintético sin puntos, como los
    # demás profesionales ficticios de la guía (22222222-2, 33333333-3).
    registry.add_practitioner(
        build_practitioner(
            resource_id="operador-hub",
            run="44444444-4",
            family="Díaz",
            given="Jorge",
            gender="male",
        )
    )
    registry.add_role(
        build_practitioner_role(
            resource_id="rol-operador-hub",
            practitioner_id="operador-hub",
            organization_id="org-hub",
            role="hub-operator",
        )
    )
    return registry
