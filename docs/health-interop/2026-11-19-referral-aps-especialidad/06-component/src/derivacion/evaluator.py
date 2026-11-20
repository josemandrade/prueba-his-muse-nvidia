"""Reglas SLA R1–R5 (rules.md): evaluación, no cambio de estado.

El evaluador toma el estado de una derivación y una fecha (`now`) y
devuelve las escaladas que vencen. NUNCA cambia el estado: un
incumplimiento de plazo dispara una escalada, nunca un cambio de
estado (lifecycle.md). El workflow aplica la acción devuelta
(registra la escalada como disparada, envía la notificación, o
devuelve la derivación al re-triaje en R3 tras la segunda
persecución).

Reglas (rules.md):
- R1 aceptación: creación + 5 días hábiles (2 si es urgente).
- R2 oferta de cita: aceptación + 10 días hábiles.
- R3 confirmación: oferta + 3 días hábiles (perseguir hasta 2 veces;
  tras la segunda sin confirmar → re-triaje de APS).
- R4 contrareferencia: encuentro + 5 días hábiles.
- R5 re-triaje: rechazo (o retorno por fallo de agendamiento) + 5 días.
"""

from derivacion.constants import MAX_CHASE_COUNT, SLA_WORKING_DAYS
from derivacion.working_days import deadline_after


def sla_deadlines(
    created,
    priority,
    accepted_at=None,
    offered_at=None,
    encounter_finished_at=None,
    rejected_at=None,
    retriage_return_at=None,
):
    """Calcula los plazos SLA de una derivación.

    `created` es obligatorio; cada plazo sin su disparador es None.
    `priority` es `routine` o `urgent` (urgent reduce a la mitad el
    plazo de aceptación: 2 días hábiles).
    """
    acceptance_days = (
        SLA_WORKING_DAYS["acceptance_urgent"]
        if priority == "urgent"
        else SLA_WORKING_DAYS["acceptance"]
    )
    deadlines = {
        "acceptance": deadline_after(created, acceptance_days),
        "offer": (
            deadline_after(accepted_at, SLA_WORKING_DAYS["offer"])
            if accepted_at
            else None
        ),
        "confirmation": (
            deadline_after(offered_at, SLA_WORKING_DAYS["confirmation"])
            if offered_at
            else None
        ),
        "counterreferral": (
            deadline_after(
                encounter_finished_at, SLA_WORKING_DAYS["counterreferral"]
            )
            if encounter_finished_at
            else None
        ),
        "retriage": None,
    }
    retriage_trigger = rejected_at or retriage_return_at
    if retriage_trigger:
        deadlines["retriage"] = deadline_after(
            retriage_trigger, SLA_WORKING_DAYS["retriage"]
        )
    return deadlines


def evaluate_escalations(state, now):
    """Devuelve las escaladas SLA que vencen a `now`.

    `state` es un dict con: `case_state`, `priority`, `created_at`,
    `accepted_at`, `offered_at`, `offer_open`, `chase_count`,
    `encounter_finished_at`, `rejected_at`, `retriage_return_at`,
    `retriage_decided`,
    `counter_referral_sent`, `escalations_fired` (set de reglas ya
    disparadas). No modifica `state` ni el estado del caso.
    """
    deadlines = sla_deadlines(
        created=state["created_at"],
        priority=state["priority"],
        accepted_at=state.get("accepted_at"),
        offered_at=state.get("offered_at"),
        encounter_finished_at=state.get("encounter_finished_at"),
        rejected_at=state.get("rejected_at"),
        retriage_return_at=state.get("retriage_return_at"),
    )
    fired = state.get("escalations_fired", set())
    actions = []

    def due(rule, deadline):
        return deadline is not None and now > deadline and rule not in fired

    case_state = state["case_state"]

    # R1: sin decisión de triaje y vencido el plazo de aceptación.
    if case_state in ("requested", "received") and due("R1", deadlines["acceptance"]):
        actions.append(
            {
                "rule": "R1",
                "action": "escalate-specialty-notify-aps",
                "recipients": ["specialty", "aps-admin"],
                "deadline": deadlines["acceptance"],
            }
        )

    # R2: aceptada sin oferta y vencido el plazo de oferta.
    if case_state == "accepted" and due("R2", deadlines["offer"]):
        actions.append(
            {
                "rule": "R2",
                "action": "escalate-specialty-notify-aps",
                "recipients": ["specialty", "aps-admin"],
                "deadline": deadlines["offer"],
            }
        )

    # R3: oferta abierta sin confirmar y vencido el plazo de
    # confirmación. Perseguir hasta 2 veces; tras la segunda sin
    # confirmar, la derivación vuelve al re-triaje de APS.
    if (
        case_state == "accepted"
        and state.get("offer_open")
        and due("R3", deadlines["confirmation"])
    ):
        if state.get("chase_count", 0) >= MAX_CHASE_COUNT:
            actions.append(
                {
                    "rule": "R3",
                    "action": "return-to-retriage",
                    "recipients": ["aps-admin"],
                    "deadline": deadlines["confirmation"],
                }
            )
        else:
            actions.append(
                {
                    "rule": "R3",
                    "action": "chase-patient",
                    "recipients": ["patient"],
                    "deadline": deadlines["confirmation"],
                }
            )

    # R4: visita hecha sin contrareferencia y vencido su plazo.
    if (
        case_state == "completed"
        and not state.get("counter_referral_sent")
        and due("R4", deadlines["counterreferral"])
    ):
        actions.append(
            {
                "rule": "R4",
                "action": "escalate-specialty-notify-aps",
                "recipients": ["specialty", "aps-admin"],
                "deadline": deadlines["counterreferral"],
            }
        )

    # R5: rechazada sin decisión de re-triaje y vencido su plazo.
    if (
        case_state == "rejected"
        and not state.get("retriage_decided")
        and due("R5", deadlines["retriage"])
    ):
        actions.append(
            {
                "rule": "R5",
                "action": "escalate-aps",
                "recipients": ["aps-admin"],
                "deadline": deadlines["retriage"],
            }
        )

    return actions
