"""Escenarios end-to-end del componente (Plan task 11.13).

Los tres recorridos de la guía con el ejemplo trabajado (María
González, 58, RUN sintético 11.111.111-1, CESFAM Los Aromos →
cardiología, REF-2026-0001, sospecha de insuficiencia cardiaca):
aceptado (creación → contrareferencia), rechazado (triaje →
re-triaje) y no-show (dos ausencias → cierre). Fechas fijas para
que los ejemplos generados sean deterministas.

El CLI (`derivacion.cli`) ejecuta un escenario y vuelca sus recursos
en `examples/<escenario>/`.
"""

from datetime import datetime, timedelta, timezone

from derivacion.registry import seed_worked_example
from derivacion.workflow import Referral

TZ = timezone(timedelta(hours=-3))


def dt(year, month, day, hour=9, minute=0):
    return datetime(year, month, day, hour, minute, tzinfo=TZ)


CREATED = dt(2026, 11, 19, 9, 30)
ROUTED = dt(2026, 11, 19, 10, 0)
TRIAGE = dt(2026, 11, 21, 9, 0)
OFFERED = dt(2026, 11, 24, 11, 0)
CONFIRMED = dt(2026, 11, 25, 9, 0)
BOOKED = dt(2026, 11, 25, 10, 0)
VISIT_START = dt(2026, 12, 2, 10, 0)
VISIT_END = dt(2026, 12, 2, 10, 30)
SENT = dt(2026, 12, 3, 10, 0)
ACKNOWLEDGED = dt(2026, 12, 3, 11, 0)


def _create():
    registry = seed_worked_example()
    referral = Referral.create(
        registry, "REF-2026-0001", "maria-gonzalez", "rol-medico-aps",
        "cardiologia", "84114007", "routine", authored_on=CREATED,
        aps_encounter_id="aps-encounter-2026-11-19",
        supporting_info_ids=["ecg-2026-11-19", "ntprobnp-2026-11-19"],
        note_text="Disnea de esfuerzo y edema de tobillos de dos semanas de evolución.",
        now=CREATED)
    referral.route(now=ROUTED)
    return referral


def _accept(referral):
    referral.triage(
        "accepted", now=TRIAGE, service_id="servicio-cardiologia",
        specialist_role_id="rol-especialista")
    return referral


def _offer_and_book(referral, slot_id="slot-cardiologia-1",
                    start=VISIT_START, end=VISIT_END,
                    offered=OFFERED, confirmed=CONFIRMED, booked=BOOKED):
    referral.offer_appointment(
        slot_id, "schedule-cardiologia", start, end, now=offered,
        patient_instruction="Ayuno no necesario. Traer los exámenes previos.")
    referral.respond_to_offer("accepted", now=confirmed)
    referral.book_appointment(now=booked)
    return referral


def accepted_scenario():
    """Recorrido aceptado: creación → contrareferencia acusada."""
    referral = _accept(_create())
    _offer_and_book(referral)
    referral.record_arrival(now=VISIT_START)
    referral.finish_encounter(now=VISIT_END)
    referral.send_counter_referral(now=SENT)
    referral.acknowledge_counter_referral(now=ACKNOWLEDGED)
    return referral


def rejected_scenario():
    """Recorrido rechazado: triaje rechaza, APS resuelve en APS."""
    referral = _create()
    referral.triage("rejected", now=TRIAGE, reason_code="capacity",
                    reason_display="Capacity")
    referral.decide_retriage("resolve-in-aps", now=dt(2026, 11, 23, 9, 0))
    return referral


def no_show_scenario():
    """Recorrido no-show: dos ausencias cierran la derivación."""
    referral = _accept(_create())
    _offer_and_book(referral)
    referral.record_no_show(now=dt(2026, 12, 2, 10, 15))
    referral.reschedule_after_no_show(
        "slot-cardiologia-2", "schedule-cardiologia",
        dt(2026, 12, 9, 10, 0), dt(2026, 12, 9, 10, 30),
        now=dt(2026, 12, 3, 9, 0))
    referral.respond_to_offer("accepted", now=dt(2026, 12, 4, 9, 0))
    referral.book_appointment(now=dt(2026, 12, 4, 10, 0))
    referral.record_no_show(now=dt(2026, 12, 9, 10, 15))
    return referral


SCENARIOS = {
    "accepted": accepted_scenario,
    "rejected": rejected_scenario,
    "no-show": no_show_scenario,
}


def all_resources(referral):
    """Todos los recursos FHIR del escenario, en orden de creación."""
    resources = [referral.service_request, referral.task]
    resources.extend(referral.appointments)
    resources.extend(referral.appointment_responses)
    resources.extend(referral.slots.values())
    resources.extend(referral.encounters)
    resources.extend(referral.notifications)
    resources.extend(referral.history)
    # Las suscripciones llevan contabilidad interna (`_active`,
    # `notifications`) que NO es FHIR: al exportar se vuelca una
    # copia sin esas claves (C4, revisión experta del paso 6).
    resources.extend(
        {k: v for k, v in sub.items() if k not in ("_active", "notifications")}
        for sub in referral.subscriptions
    )
    # El operador del hub es un recurso de directorio sembrado (C3):
    # las notificaciones lo referencian como emisor/destinatario y los
    # ejemplos deben llevarlo para ser autocontenidos.
    resources.extend(referral.registry.practitioners.values())
    resources.extend(referral.registry.roles.values())
    for attr in ("condition", "care_plan", "composition",
                 "document_reference"):
        resource = getattr(referral, attr, None)
        if resource is not None:
            resources.append(resource)
    return resources


def summary(referral):
    """Resumen del escenario: estados, conteos y violaciones de I1–I6."""
    return {
        "referral_id": referral.referral_id,
        "case_state": referral.case_state,
        "task_status": referral.task["status"],
        "service_request_status": referral.service_request["status"],
        "counts": dict(referral.counts),
        "appointments": [
            {"id": a["id"], "status": a["status"]}
            for a in referral.appointments
        ],
        "encounters": [
            {"id": e["id"], "status": e["status"]}
            for e in referral.encounters
        ],
        "notifications": len(referral.notifications),
        "history": len(referral.history),
        "invariant_violations": referral.check_invariants(),
    }
