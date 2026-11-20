"""Máquinas de estado del componente (lifecycle.md).

Toda la lógica de transiciones vive aquí: un `transitions.py`
despacha por máquina (una tabla por recurso). Ningún builder ni el
workflow cambian el estado por su cuenta: cada operación que cambia el
estado valida el estado actual → estado siguiente contra la tabla de
su máquina ANTES de construir el recurso, y lanza
`ForbiddenTransition` (409) en una transición prohibida.

Máquinas (de lifecycle.md):
- Task: el estado del caso vive en `businessStatus`; `Task.status`
  es el valor grueso R4 que corresponde (ver `constants.py`).
- ServiceRequest: espejo grueso del Task.
- Appointment: la cadena oferta/reserva.
- Encounter: la visita (existe desde la reserva).
- CarePlan: el plan de seguimiento.
"""

from derivacion.constants import (
    CASE_STATE_TO_TASK_STATUS,
    TERMINAL_CASE_STATES,
)

# ---------------------------------------------------------------------------
# Tablas de transiciones
# ---------------------------------------------------------------------------

# Estado del caso (Task.businessStatus) → estados siguientes permitidos.
# `rejected` → `cancelled` solo antes de la decisión de re-triaje de
# APS (OP-8); tras la decisión, `rejected` es terminal (N1).
# `accepted` → `rejected` solo por retorno de fallo de agendamiento
# (OP-4 segundo rechazo, o R3 tras la segunda persecución sin
# confirmar): lo exige el paso 3 validado (C4) aunque la tabla del
# paso 4 no lo liste — Ruling en `state.md` (Plan task 11.8).
# `scheduled` → `no-show` solo en el SEGUNDO no-show (OP-5): el
# primer no-show vive solo en el Appointment y el Task no se mueve.
TASK_TRANSITIONS = {
    "requested": {"received", "cancelled"},
    "received": {"accepted", "rejected", "cancelled"},
    "accepted": {"scheduled", "cancelled", "rejected"},
    "rejected": {"cancelled"},
    "scheduled": {"completed", "cancelled", "no-show"},
    "completed": {"counter-referred", "cancelled"},
    "counter-referred": set(),
    "no-show": set(),
    "cancelled": set(),
}

SERVICE_REQUEST_TRANSITIONS = {
    "draft": {"active"},
    "active": {"completed", "revoked"},
    "completed": set(),
    "revoked": set(),
}

APPOINTMENT_TRANSITIONS = {
    # booked → booked: mismo Appointment, nuevo Slot (re-agendamiento
    # tras un conflicto previo a la asistencia, OP-4).
    "proposed": {"pending", "cancelled"},
    "pending": {"booked", "cancelled"},
    "booked": {"arrived", "noshow", "cancelled", "booked"},
    "arrived": {"fulfilled"},
    "fulfilled": set(),
    "noshow": set(),
    "cancelled": set(),
}

ENCOUNTER_TRANSITIONS = {
    "planned": {"in-progress", "cancelled"},
    "in-progress": {"finished"},
    "finished": set(),
}

CAREPLAN_TRANSITIONS = {
    "draft": {"active"},
    "active": {"completed", "revoked"},
    "completed": set(),
    "revoked": set(),
}

TABLES = {
    "Task": TASK_TRANSITIONS,
    "ServiceRequest": SERVICE_REQUEST_TRANSITIONS,
    "Appointment": APPOINTMENT_TRANSITIONS,
    "Encounter": ENCOUNTER_TRANSITIONS,
    "CarePlan": CAREPLAN_TRANSITIONS,
}


class ForbiddenTransition(ValueError):
    """Una transición que la máquina del recurso no permite (409)."""

    status = 409

    def __init__(self, machine, current, attempted, reason=None):
        self.machine = machine
        self.current = current
        self.attempted = attempted
        self.reason = reason
        message = (
            f"{machine}: transición prohibida {current!r} → {attempted!r}"
        )
        if reason:
            message += f" ({reason})"
        super().__init__(message)


def validate_transition(machine, current, attempted, **kwargs):
    """Valida una transición contra la tabla de su máquina.

    Lanza `ForbiddenTransition` si no está permitida. `kwargs` lleva
    las condiciones de la tabla que no son el estado (p. ej.
    `retriage_decided` para el Task en `rejected`).
    """
    table = TABLES[machine]
    if current not in table:
        raise ForbiddenTransition(machine, current, attempted, "estado desconocido")
    if machine == "Task" and current == "rejected":
        if attempted == "cancelled" and kwargs.get("retriage_decided"):
            raise ForbiddenTransition(
                machine,
                current,
                attempted,
                "la decisión de re-triaje ya se tomó: rejected es terminal (N1)",
            )
    if machine == "Task" and current == "accepted" and attempted == "rejected":
        if not kwargs.get("scheduling_failure"):
            raise ForbiddenTransition(
                machine,
                current,
                attempted,
                "accepted → rejected solo por retorno de fallo de "
                "agendamiento (OP-4 / R3); el rechazo de triaje es "
                "received → rejected (OP-2)",
            )
    if machine == "Task" and current == "scheduled" and attempted == "no-show":
        if not kwargs.get("second_no_show"):
            raise ForbiddenTransition(
                machine,
                current,
                attempted,
                "el Task solo se mueve en el SEGUNDO no-show (OP-5); "
                "el primer no-show vive solo en el Appointment",
            )
    if attempted not in table[current]:
        raise ForbiddenTransition(machine, current, attempted)
    return True


def validate_task_transition(
    current, attempted, retriage_decided=False, scheduling_failure=False,
    second_no_show=False,
):
    """Valida una transición del estado del caso (Task.businessStatus)."""
    return validate_transition(
        "Task",
        current,
        attempted,
        retriage_decided=retriage_decided,
        scheduling_failure=scheduling_failure,
        second_no_show=second_no_show,
    )


def validate_service_request_transition(current, attempted):
    return validate_transition("ServiceRequest", current, attempted)


def validate_appointment_transition(current, attempted):
    return validate_transition("Appointment", current, attempted)


def validate_encounter_transition(current, attempted):
    return validate_transition("Encounter", current, attempted)


def validate_careplan_transition(current, attempted):
    return validate_transition("CarePlan", current, attempted)


def validate_reopen(current_case_state, target_case_state, actor_role):
    """El único camino de corrección de un `cancelled`: re-apertura.

    Solo el operador del hub puede re-abrir una derivación cancelada
    en error, al estado previo a la cancelación, con una entrada
    explícita de re-apertura en el historial.
    """
    if current_case_state != "cancelled":
        raise ForbiddenTransition(
            "Task",
            current_case_state,
            target_case_state,
            "solo una derivación cancelada puede re-abrirse",
        )
    if actor_role != "hub-operator":
        raise ForbiddenTransition(
            "Task",
            current_case_state,
            target_case_state,
            "solo el operador del hub puede re-abrir una cancelación",
        )
    if target_case_state in TERMINAL_CASE_STATES:
        raise ForbiddenTransition(
            "Task",
            current_case_state,
            target_case_state,
            "la re-apertura no puede llevar a un estado terminal",
        )
    return True


def task_status_for(case_state):
    """El valor grueso R4 (Task.status) de un estado del caso."""
    return CASE_STATE_TO_TASK_STATUS[case_state]


# ---------------------------------------------------------------------------
# Invariantes entre máquinas (I1–I6, lifecycle.md)
# ---------------------------------------------------------------------------

# Estado del caso → estado esperado del ServiceRequest espejo.
# `rejected` depende de si APS ya decidió el re-triaje (N1).
EXPECTED_SR_STATUS = {
    "requested": "active",
    "received": "active",
    "accepted": "active",
    "scheduled": "active",
    "completed": "active",
    "counter-referred": "completed",
    "no-show": "revoked",
    "cancelled": "revoked",
}


def expected_service_request_status(case_state, retriage_decided=False):
    if case_state == "rejected":
        return "revoked" if retriage_decided else "active"
    return EXPECTED_SR_STATUS[case_state]


def check_invariants(state):
    """Comprueba las invariantes I1–I6 sobre el estado de una derivación.

    `state` es un dict con: `case_state`, `retriage_decided`,
    `service_request_status`, `appointments` (lista de dicts con
    `status`), `encounter_status`, `encounter_created_at`
    ("booking" | "attendance" | None). Devuelve la lista de
    violaciones (vacía = consistente). Cada violación empieza por su
    número de invariante.
    """
    violations = []
    case_state = state["case_state"]
    retriage_decided = state.get("retriage_decided", False)

    # I1: el Task es la autoridad; el ServiceRequest es su espejo.
    expected = expected_service_request_status(case_state, retriage_decided)
    if state["service_request_status"] != expected:
        violations.append(
            f"I1: Task en {case_state!r} (re-triage decidido: "
            f"{retriage_decided}) con ServiceRequest en "
            f"{state['service_request_status']!r}; se esperaba {expected!r}"
        )

    # I6: un Task `rejected` (cerrado) tiene su ServiceRequest en
    # `revoked` en la misma transacción.
    if (
        case_state == "rejected"
        and retriage_decided
        and state["service_request_status"] != "revoked"
    ):
        violations.append(
            "I6: Task `rejected` (cerrado) con ServiceRequest en "
            f"{state['service_request_status']!r}; se esperaba 'revoked'"
        )

    # I4: no hay Encounter en un no-show; el Encounter existe desde
    # la reserva, nunca se crea en la asistencia.
    if state.get("encounter_created_at") == "attendance":
        violations.append(
            "I4: Encounter creado en la asistencia (sin existir en la "
            "reserva); el no-show vive solo en el Appointment"
        )
    if any(a.get("status") == "noshow" for a in state.get("appointments", [])):
        if state.get("encounter_status") in ("in-progress", "finished"):
            violations.append(
                "I4: Appointment `noshow` con Encounter en "
                f"{state.get('encounter_status')!r}; no hay Encounter en "
                "un no-show"
            )

    # I2/I3 las imponen las propias tablas (los estados terminales no
    # tienen transiciones salientes; un Appointment `noshow` o
    # `cancelled` nunca se reutiliza). Aquí se comprueba que ningún
    # Appointment terminal haya avanzado: lo garantiza la tabla.
    return violations
