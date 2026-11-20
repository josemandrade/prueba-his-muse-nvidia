"""Motor del flujo de derivación (OP-1…OP-12).

El `Referral` es la unidad de trabajo: guarda los recursos FHIR de
una derivación (ServiceRequest, Task, Appointment, Encounter,
Communication, Provenance…) y aplica las transiciones del ciclo de
vida con sus guardas (`transitions.py`), los plazos SLA
(`evaluator.py`) y los conteos (decline/chase/re-scheduling).

Reglas que este motor hace cumplir (guía + decisiones del caso):

- La identidad debe estar resuelta antes de crear (OP-9): el
  paciente tiene que existir en el registro MPI; si no, la creación
  se rechaza. El servicio tiene que estar en el directorio (OP-10).
- El Task es el centro: `businessStatus` es el estado del caso; cada
  transición valida la tabla de `transitions.py` y deja una entrada
  de Provenance con el rol que la hizo.
- Los plazos SLA nunca cambian el estado: un vencimiento dispara una
  escalación (hub → especialidad + APS) o el retorno a re-triaje
  (R3), nunca un cierre por tiempo.
- Los conteos de decline/chase pertenecen al ciclo de oferta actual:
  el de decline NO se reinicia en la re-oferta tras un rechazo (si
  no, el gateway "First decline?" del BPMN nunca vería el segundo
  rechazo); se reinicia solo cuando empieza un ciclo nuevo tras un
  no-show (N5). El de chase se reinicia en cada oferta. El de
  re-agendamiento no se reinicia nunca (0–1).
- El retorno por fallo de agendamiento mueve `accepted` →
  `rejected` (Ruling en `state.md`, Plan task 11.8): lo exige el
  paso 3 validado (C4) aunque la tabla del paso 4 no lo liste.
"""

from datetime import datetime

from derivacion.builders import (
    build_appointment,
    build_appointment_response,
    build_care_plan,
    build_communication,
    build_composition,
    build_condition,
    build_document_bundle,
    build_document_reference,
    build_encounter,
    build_provenance,
    build_service_request,
    build_slot,
    build_subscription,
    build_task,
    build_transaction_bundle,
)
from derivacion.constants import (
    MAX_CHASE_COUNT,
    MAX_DECLINE_COUNT,
    MAX_RESCHEDULING_COUNT,
    NOTIFICATION_SENDERS,
    REJECTION_REASONS,
)
from derivacion.evaluator import evaluate_escalations, sla_deadlines
from derivacion.registry import ServiceNotFound
from derivacion.transitions import (
    ForbiddenTransition,
    check_invariants,
    validate_appointment_transition,
    validate_encounter_transition,
    validate_service_request_transition,
    validate_reopen,
    validate_task_transition,
)
from derivacion.working_days import SANTIAGO

# Roles → recurso que los representa en las notificaciones. El
# operador del hub es un PractitionerRole (`rol-operador-hub`, código
# `hub-operator` del DerivacionRolCS de la guía); el componente lo
# materializa en el registro sembrado porque los ejemplos de la guía
# no lo incluyen (C3, revisión experta del paso 6).
ROLE_RESOURCES = {
    "aps-doctor": ("PractitionerRole", "rol-medico-aps"),
    "aps-admin": ("PractitionerRole", "rol-admin-aps"),
    "triage-clinician": ("PractitionerRole", "rol-triaje"),
    "specialty-scheduler": ("PractitionerRole", "rol-agendador"),
    "specialist": ("PractitionerRole", "rol-especialista"),
    "hub-operator": ("PractitionerRole", "rol-operador-hub"),
}

# Destinatario de cada notificación → recurso. Los destinatarios son
# siempre un rol nombrado (PractitionerRole) o el paciente: el perfil
# DerivacionNotificacion solo admite Patient y DerivacionRol como
# `recipient` (C3, revisión experta del paso 6). "hub" es el operador
# del hub (acuse de recibo, OP-6); la "especialidad" como
# organización ya no es destinataria: cada escalada va al responsable
# de la acción pendiente (triaje, agendador o especialista, según
# NOTIFICATION_SENDERS).
RECIPIENT_RESOURCES = {
    "patient": ("Patient", None),  # el id va en el paciente de la derivación
    "aps-admin": ("PractitionerRole", "rol-admin-aps"),
    "specialty-scheduler": ("PractitionerRole", "rol-agendador"),
    "triage-clinician": ("PractitionerRole", "rol-triaje"),
    "specialist": ("PractitionerRole", "rol-especialista"),
    "hub": ("PractitionerRole", "rol-operador-hub"),
}

# Descripción del Task por estado: el próximo paso esperado.
DESCRIPTIONS = {
    "requested": "acceptance decision",
    "received": "acceptance decision",
    "accepted": "appointment offer",
    "rejected": "retriage decision",
    "scheduled": "visit",
    "completed": "counter-referral",
    "counter-referred": None,
    "no-show": None,
    "cancelled": None,
}


class IdentityNotFoundError(ValueError):
    """La identidad no está resuelta en el MPI (OP-9 bloquea)."""


class ServiceNotFoundError(ValueError):
    """El servicio no está en el directorio local (OP-10 bloquea)."""


class WorkflowError(ValueError):
    """La operación no aplica en el estado actual de la derivación."""


class Referral:
    """Una derivación APS → especialidad, con sus recursos FHIR."""

    def __init__(self, registry, referral_id, patient_id, service_code):
        self.registry = registry
        self.referral_id = referral_id
        self.patient_id = patient_id
        self.service_code = service_code
        self.priority = "routine"
        self.service_request = None
        self.task = None
        self.appointments = []
        self.appointment_responses = []
        self.encounters = []
        self.slots = {}
        self.encounter = None
        self.notifications = []
        self.history = []
        self.subscriptions = []
        self.case_state = None
        self.retriage_decided = False
        self.offer_open = False
        self.offer_confirmed = False
        self.offer_number = 0
        self.counts = {"decline": 0, "chase": 0, "rescheduling": 0}
        self.deadlines = {}
        self.escalations_fired = set()
        self.created_at = None
        self.accepted_at = None
        self.offered_at = None
        self.encounter_finished_at = None
        self.rejected_at = None
        self.retriage_return_at = None
        self.counter_referral_sent = False
        self._seq = 0

    # -- identificadores derivados -------------------------------------

    @property
    def sr_id(self):
        return self.referral_id.lower()

    @property
    def task_id(self):
        return f"tarea-{self.sr_id}"

    @property
    def current_appointment(self):
        return self.appointments[-1] if self.appointments else None

    def _next_id(self, kind):
        self._seq += 1
        return f"{kind}-{self.sr_id}-{self._seq}"

    def _now(self, now):
        return now if now is not None else datetime.now(SANTIAGO)

    def _recompute_deadlines(self):
        """Recalcula los cinco plazos SLA desde los disparadores.

        Un plazo satisfecho o sin disparador no viaja en el Task: la
        aceptación solo mientras no hay decisión, la oferta solo en
        `accepted`, la confirmación solo con la oferta abierta, la
        contrareferencia solo en `completed` sin enviar, el re-triaje
        solo en `rejected` sin decidir.
        """
        self.deadlines = sla_deadlines(
            created=self.created_at,
            priority=self.priority,
            accepted_at=self.accepted_at,
            offered_at=self.offered_at,
            encounter_finished_at=self.encounter_finished_at,
            rejected_at=self.rejected_at,
            retriage_return_at=self.retriage_return_at,
        )
        if self.case_state not in ("requested", "received"):
            self.deadlines["acceptance"] = None
        if self.case_state != "accepted":
            self.deadlines["offer"] = None
        if not self.offer_open:
            self.deadlines["confirmation"] = None
        if not (self.case_state == "completed"
                and not self.counter_referral_sent):
            self.deadlines["counterreferral"] = None
        if not (self.case_state == "rejected"
                and not self.retriage_decided):
            self.deadlines["retriage"] = None

    # -- construcción del Task -----------------------------------------

    def _rebuild_task(self, now):
        """Reconstruye el Task desde el estado actual del flujo.

        Los conteos en cero no viajan como extensiones (el ejemplo
        de la guía no los lleva): solo aparecen cuando son > 0.
        """
        self.task = build_task(
            resource_id=self.task_id,
            referral_id=self.referral_id,
            patient_id=self.patient_id,
            requester_role_id="rol-medico-aps",
            service_request_id=self.sr_id,
            case_state=self.case_state,
            description=DESCRIPTIONS[self.case_state],
            now=self._now(now),
            deadlines=self.deadlines or None,
            counts={k: v for k, v in self.counts.items() if v != 0} or None,
            owner_service_id=getattr(self, "_owner_service_id", None),
            status_reason=getattr(self, "_status_reason", None),
            relevant_history_ids=[p["id"] for p in self.history] or None,
        )

    def _record_transition(self, new_state, now, actor_role_id, role_code,
                           **guard_kwargs):
        """Valida la transición, cambia el estado y deja Provenance."""
        validate_task_transition(
            self.case_state, new_state,
            retriage_decided=self.retriage_decided, **guard_kwargs)
        self.case_state = new_state
        self._rebuild_task(now)
        provenance = build_provenance(
            resource_id=self._next_id("provenance"),
            task_id=self.task_id,
            actor_role_id=actor_role_id,
            role_code=role_code,
            recorded=self._now(now),
        )
        self.history.append(provenance)
        self._notify_subscribers(new_state, now)
        return provenance

    # -- notificaciones (OP-12) y suscripciones (OP-11) -----------------

    def _notify(self, trigger, now, message=None, medium="phone",
                document_id=None):
        """Construye la Communication del trigger y la registra."""
        sender_code, recipient_code = NOTIFICATION_SENDERS[trigger]
        sender_type, sender_id = ROLE_RESOURCES[sender_code]
        recipient_type, recipient_id = RECIPIENT_RESOURCES[recipient_code]
        if recipient_code == "patient":
            recipient_id = self.patient_id
        notification = build_communication(
            resource_id=self._next_id("notificacion"),
            notification_id=(
                f"NOTIF-{self.referral_id[4:]}-{len(self.notifications) + 1:02d}"
            ),
            patient_id=self.patient_id,
            task_id=self.task_id,
            trigger=trigger,
            sender_role_code=sender_code,
            sender_role_id=sender_id,
            recipient_type=recipient_type,
            recipient_id=recipient_id,
            sent=self._now(now),
            medium=medium,
            message=message,
            delivery_outcome="delivered",
            document_id=document_id,
            sender_type=sender_type,
        )
        self.notifications.append(notification)
        return notification

    def _notify_subscribers(self, new_state, now):
        """OP-11: avisa a los suscriptores activos del cambio de estado."""
        for subscription in self.subscriptions:
            if subscription.get("_active", True):
                subscription.setdefault("notifications", []).append(
                    {"state": new_state, "at": self._now(now).isoformat()}
                )

    def _evaluator_state(self):
        """El dict de estado que `evaluate_escalations` espera."""
        return {
            "case_state": self.case_state,
            "priority": self.priority,
            "created_at": self.created_at,
            "accepted_at": self.accepted_at,
            "offered_at": self.offered_at,
            "offer_open": self.offer_open,
            "chase_count": self.counts["chase"],
            "encounter_finished_at": self.encounter_finished_at,
            "rejected_at": self.rejected_at,
            "retriage_return_at": self.retriage_return_at,
            "retriage_decided": self.retriage_decided,
            "counter_referral_sent": self.counter_referral_sent,
            "escalations_fired": self.escalations_fired,
        }

    # -- OP-1: crear + enrutar -----------------------------------------

    @classmethod
    def create(cls, registry, referral_id, patient_id, requester_role_id,
               service_code, reason_code, priority, authored_on,
               service_id=None, aps_encounter_id=None,
               supporting_info_ids=None, note_text=None, now=None,
               reason_text="Suspected heart failure: exertional dyspnoea, ankle oedema",
               reason_display="Heart failure (disorder)"):
        """Crea la derivación (ServiceRequest + Task `requested`).

        La identidad debe estar resuelta (OP-9) y el servicio en el
        directorio (OP-10); si no, se rechaza antes de crear nada.
        """
        if patient_id not in registry.patients:
            raise IdentityNotFoundError(
                f"identidad no resuelta en el MPI: {patient_id!r} (OP-9)")
        try:
            service = registry.find_service(service_code)
        except ServiceNotFound as exc:
            raise ServiceNotFoundError(str(exc)) from exc
        referral = cls(registry, referral_id, patient_id, service_code)
        referral.priority = priority
        referral._service_id = service_id or service["id"]
        referral._sr_kwargs = {
            "resource_id": referral.sr_id,
            "referral_id": referral_id,
            "patient_id": patient_id,
            "requester_role_id": requester_role_id,
            "service_code": service_code,
            "reason_snomed": reason_code,
            "reason_text": reason_text,
            "reason_display": reason_display,
            "priority": priority,
            "authored_on": authored_on,
            "aps_encounter_id": aps_encounter_id,
            "supporting_info_ids": supporting_info_ids,
            "note_text": note_text,
            "performer_service_id": referral._service_id,
        }
        referral.created_at = referral._now(now)
        referral.case_state = "requested"
        referral._recompute_deadlines()
        referral.service_request = build_service_request(**referral._sr_kwargs)
        referral._rebuild_task(referral.created_at)
        referral._notify(
            "created", referral.created_at,
            "Su derivación a cardiología fue creada y enviada a la "
            "especialidad.")
        return referral

    def route(self, now=None):
        """OP-1 (enrutamiento): el hub recibe la derivación."""
        self._record_transition(
            "received", now, "rol-admin-aps", "aps-admin")
        return self.task

    def transaction_bundle(self):
        """OP-1: Bundle transaction con la solicitud + el Task."""
        return build_transaction_bundle(
            [self.service_request, self.task],
            resource_id=f"bundle-pi0-{self.sr_id}",
        )

    # -- OP-2: triaje ---------------------------------------------------

    def triage(self, decision, now=None, triage_role_id="rol-triaje",
               service_id=None, specialist_role_id=None,
               reason_code=None, reason_display=None):
        """Acepta o rechaza la derivación (PI-1).

        Aceptar nombra el servicio (owner) y el profesional (agente
        de Provenance, no `Task.owner` — corrección R4 del paso 5).
        Rechazar exige un motivo de la lista local y abre el plazo
        de re-triaje de 5 días hábiles.
        """
        now = self._now(now)
        if self.case_state != "received":
            raise WorkflowError(
                f"el triaje exige estado received, no {self.case_state!r}")
        if decision == "accepted":
            if service_id is None or specialist_role_id is None:
                raise WorkflowError(
                    "aceptar nombra el servicio y el profesional (OP-2)")
            self._owner_service_id = service_id
            self.accepted_at = now
            self._record_transition(
                "accepted", now, triage_role_id, "triage-clinician")
            self._recompute_deadlines()
            self._rebuild_task(now)
            self._notify(
                "accepted", now,
                "Su derivación a cardiología fue aceptada. "
                "Le ofreceremos una cita en los próximos días.")
        elif decision == "rejected":
            if reason_code not in REJECTION_REASONS:
                raise WorkflowError(
                    f"motivo de rechazo desconocido: {reason_code!r} "
                    f"(lista local: {REJECTION_REASONS})")
            self._status_reason = {
                "code": reason_code, "display": reason_display or reason_code}
            self.rejected_at = now
            self._record_transition(
                "rejected", now, triage_role_id, "triage-clinician")
            self._recompute_deadlines()
            self._rebuild_task(now)
            self._notify(
                "rejected", now,
                "Su derivación a cardiología fue rechazada por la "
                "especialidad. Su médico APS revisará los próximos pasos.")
        else:
            raise WorkflowError(f"decisión de triaje desconocida: {decision!r}")
        return self.task

    def decide_retriage(self, outcome, now=None):
        """Cierra la derivación como `rejected` tras la decisión de APS.

        `outcome`: "new-referral" | "different-specialty" |
        "resolve-in-aps". Un reenvío es una derivación NUEVA (OP-1);
        aquí solo se cierra esta. El ServiceRequest se revoca en la
        misma transacción (I6).
        """
        now = self._now(now)
        if self.case_state != "rejected":
            raise WorkflowError(
                f"el re-triaje exige estado rejected, no {self.case_state!r}")
        if self.retriage_decided:
            raise WorkflowError("la decisión de re-triaje ya se tomó (N1)")
        if outcome not in ("new-referral", "different-specialty", "resolve-in-aps"):
            raise WorkflowError(f"resultado de re-triaje desconocido: {outcome!r}")
        self.retriage_decided = True
        self._recompute_deadlines()
        self._rebuild_task(now)
        validate_service_request_transition(
            self.service_request["status"], "revoked")
        self.service_request = build_service_request(
            **{**self._sr_kwargs, "status": "revoked"})
        # La decisión de APS queda auditada: cada transición deja una
        # entrada de Provenance con el rol que actúa (C5, revisión
        # experta del paso 6). El Task no cambia de estado aquí, así
        # que no pasa por `_record_transition`.
        self.history.append(build_provenance(
            resource_id=self._next_id("provenance"),
            task_id=self.task_id,
            actor_role_id="rol-medico-aps",
            role_code="aps-doctor",
            recorded=now,
        ))
        return outcome

    # -- OP-3: ofrecer / confirmar / reservar ---------------------------

    def offer_appointment(self, slot_id, schedule_id, start, end, now=None,
                          scheduler_role_id="rol-agendador",
                          location_id="location-cardiologia",
                          patient_instruction=None):
        """Ofrece una cita (Appointment `proposed`, Slot `free`).

        Cada oferta es un Appointment NUEVO (`offer-number` +1). El
        conteo de chase se reinicia en cada oferta; el de decline NO
        se reinicia en la re-oferta tras un rechazo (Ruling en
        `state.md`, Plan task 11.8): pertenece al ciclo de oferta.
        """
        now = self._now(now)
        if self.case_state == "accepted":
            pass
        elif self.case_state == "scheduled":
            # Solo como re-agendamiento tras un no-show (OP-4): la
            # cita actual está en `noshow`. Empieza un ciclo nuevo
            # (N5): los conteos de decline y chase se reinician.
            current = self.current_appointment
            if current is None or current["status"] != "noshow":
                raise WorkflowError(
                    "re-agendar exige una cita en noshow (OP-4)")
            self.counts["decline"] = 0
            # El re-agendamiento en sí: consume el único permitido (N5).
            self.counts["rescheduling"] += 1
        else:
            raise WorkflowError(
                f"ofrecer exige accepted o scheduled (tras no-show), "
                f"no {self.case_state!r}")
        self.offer_number += 1
        self.counts["chase"] = 0
        appointment_id = (
            f"cita-{self.sr_id}"
            if self.offer_number == 1
            else f"cita-{self.sr_id}-oferta-{self.offer_number}"
        )
        appointment = build_appointment(
            resource_id=appointment_id,
            appointment_id=f"CITA-{self.referral_id[4:]}"
            + (f"-{self.offer_number}" if self.offer_number > 1 else ""),
            service_request_id=self.sr_id,
            slot_id=slot_id,
            patient_id=self.patient_id,
            specialist_role_id="rol-especialista",
            location_id=location_id,
            service_code=self.service_code,
            start=start,
            end=end,
            created=now,
            offer_number=self.offer_number,
            status="proposed",
            patient_instruction=patient_instruction,
        )
        slot = build_slot(
            resource_id=slot_id,
            schedule_id=schedule_id,
            start=start,
            end=end,
            status="free",
        )
        self.appointments.append(appointment)
        self.slots[slot_id] = slot
        self.offered_at = now
        self.offer_open = True
        self.offer_confirmed = False
        self._recompute_deadlines()
        self._rebuild_task(now)
        self._notify(
            "offer", now,
            "Le ofrecemos una cita de cardiología. Por favor, confirme "
            "su asistencia en los próximos 3 días hábiles.")
        self._notify(
            "offer-notify-aps", now,
            "Se ofreció una cita de cardiología a la paciente; "
            "pendiente de confirmación.")
        return appointment

    def respond_to_offer(self, response, now=None):
        """La paciente confirma o rechaza la oferta abierta (OP-3/OP-4).

        Confirmar: AppointmentResponse `accepted`, Appointment →
        `pending`. Rechazar: AppointmentResponse `declined`, el
        Appointment pasa a `cancelled`; el primer rechazo deja la
        derivación en `accepted` para una re-oferta; el segundo
        devuelve la derivación al re-triaje de APS.
        """
        now = self._now(now)
        appointment = self.current_appointment
        if not self.offer_open or appointment is None:
            raise WorkflowError("no hay ninguna oferta abierta")
        if appointment["status"] != "proposed":
            raise WorkflowError(
                f"la oferta está en {appointment['status']!r}, no proposed")
        if response == "accepted":
            validate_appointment_transition("proposed", "pending")
            appointment["status"] = "pending"
            self.appointment_responses.append(build_appointment_response(
                resource_id=self._next_id("respuesta-cita"),
                appointment_id=appointment["id"],
                patient_id=self.patient_id,
                participant_status="accepted",
            ))
            self.offer_open = False
            self.offer_confirmed = True
            self._recompute_deadlines()
            self._rebuild_task(now)
        elif response == "declined":
            validate_appointment_transition("proposed", "cancelled")
            appointment["status"] = "cancelled"
            self.appointment_responses.append(build_appointment_response(
                resource_id=self._next_id("respuesta-cita"),
                appointment_id=appointment["id"],
                patient_id=self.patient_id,
                participant_status="declined",
            ))
            self.counts["decline"] += 1
            self.offer_open = False
            self.offer_confirmed = False
            self._recompute_deadlines()
            self._rebuild_task(now)
            if self.counts["decline"] >= MAX_DECLINE_COUNT:
                self.return_to_retriage(now, reason="second-decline")
        else:
            raise WorkflowError(f"respuesta a la oferta desconocida: {response!r}")
        return appointment

    def chase_offer(self, now=None):
        """Persigue la confirmación de la oferta abierta (R3, OP-12).

        Hasta 2 persecuciones por oferta; la llamada queda registrada
        como Communication (`chase`). El retorno a re-triaje tras la
        segunda persecución sin confirmar lo hace `apply_sla_actions`
        cuando vence el plazo, no la persecución en sí.
        """
        now = self._now(now)
        if not self.offer_open:
            raise WorkflowError("no hay ninguna oferta abierta que perseguir")
        if self.counts["chase"] >= MAX_CHASE_COUNT:
            raise WorkflowError("ya se persiguió dos veces esta oferta (R3)")
        self.counts["chase"] += 1
        self._rebuild_task(now)
        self._notify(
            "chase", now,
            "Le recordamos confirmar su cita de cardiología; si no "
            "confirma, la derivación volverá a su médico APS.")
        return self.counts["chase"]

    def book_appointment(self, now=None, scheduler_role_id="rol-agendador"):
        """Reserva la cita confirmada (Appointment `booked`, Slot `busy`).

        Crea el Encounter (`planned`) y mueve el Task a `scheduled`.
        El Slot de la oferta pasa a `busy` aquí, no en la oferta
        (Ruling en `state.md`, Plan task 11.7).
        """
        now = self._now(now)
        appointment = self.current_appointment
        if not self.offer_confirmed or appointment is None:
            raise WorkflowError("reservar exige una oferta confirmada")
        if appointment["status"] != "pending":
            raise WorkflowError(
                f"la cita está en {appointment['status']!r}, no pending")
        validate_appointment_transition("pending", "booked")
        appointment["status"] = "booked"
        slot_id = appointment["slot"][0]["reference"].split("/", 1)[1]
        slot = self.slots[slot_id]
        slot["status"] = "busy"
        # Un Encounter por cita reservada: el id deriva del
        # Appointment (la primera es la del ejemplo de la guía).
        encounter_id_value = appointment["identifier"][0]["value"].replace(
            "CITA-", "ENC-")
        self.encounter = build_encounter(
            resource_id=f"encuentro-{appointment['id'][len('cita-'):]}",
            encounter_id=encounter_id_value,
            patient_id=self.patient_id,
            service_request_id=self.sr_id,
            appointment_id=appointment["id"],
            specialist_role_id="rol-especialista",
            service_code=self.service_code,
            start=self._parse_dt(appointment["start"]),
            end=self._parse_dt(appointment["end"]),
            status="planned",
        )
        self.encounters.append(self.encounter)
        if self.case_state == "accepted":
            self._record_transition(
                "scheduled", now, scheduler_role_id, "specialty-scheduler")
        else:
            # Re-reserva tras un no-show: el Task ya está en
            # `scheduled` y no hay transición que registrar.
            self._rebuild_task(now)
        self._recompute_deadlines()
        self._rebuild_task(now)
        self._notify(
            "booked", now,
            "La cita de cardiología quedó reservada; la paciente tiene "
            "fecha y hora.", medium="system-message")
        return appointment

    @staticmethod
    def _parse_dt(value):
        return datetime.fromisoformat(value)

    # -- OP-4: re-ofertar / re-agendar -----------------------------------

    def reschedule_before_visit(self, slot_id, schedule_id, start, end,
                                now=None):
        """Conflicto antes de la cita: MISMO Appointment, nuevo Slot.

        La cita ya reservada cambia de hueco; el Slot viejo vuelve a
        `free` y el Encounter actualiza su periodo. No es una oferta
        nueva: no toca `offer-number` ni los conteos.
        """
        now = self._now(now)
        appointment = self.current_appointment
        if appointment is None or appointment["status"] != "booked":
            raise WorkflowError(
                "re-agendar por conflicto exige una cita reservada (booked)")
        old_slot_id = appointment["slot"][0]["reference"].split("/", 1)[1]
        self.slots[old_slot_id]["status"] = "free"
        appointment["slot"] = [{"reference": f"Slot/{slot_id}"}]
        appointment["start"] = start.isoformat()
        appointment["end"] = end.isoformat()
        self.slots[slot_id] = build_slot(
            resource_id=slot_id, schedule_id=schedule_id,
            start=start, end=end, status="busy")
        self.encounter["period"] = {
            "start": start.isoformat(), "end": end.isoformat()}
        self._rebuild_task(now)
        return appointment

    def return_to_retriage(self, now=None, reason="second-decline"):
        """Devuelve la derivación al re-triaje de APS (OP-4 / R3).

        El Task pasa a `rejected` con el plazo de re-triaje desde el
        retorno; la solicitud sigue `active` hasta que APS decida
        (mapeo §2). `reason`: "second-decline" | "unconfirmed-after-chase".
        """
        now = self._now(now)
        if self.case_state != "accepted":
            raise WorkflowError(
                f"el retorno a re-triaje exige accepted, no {self.case_state!r}")
        self.retriage_return_at = now
        self._record_transition(
            "rejected", now, "rol-agendador", "specialty-scheduler",
            scheduling_failure=True)
        self._recompute_deadlines()
        self._rebuild_task(now)
        self._notify(
            "escalation-retriage", now,
            f"La derivación vuelve al re-triaje de APS ({reason}); "
            "el plazo de re-triaje es de 5 días hábiles.",
            medium="system-message")
        return self.task

    # -- SLA: evaluar y aplicar (R1–R5) -----------------------------------

    def apply_sla_actions(self, now=None):
        """Evalúa los plazos SLA y aplica las acciones vencidas.

        Las escalaciones crean una Communication y se marcan como
        disparadas (una vez por plazo, nunca se re-arman). El retorno
        a re-triaje de R3 mueve el Task; una escalación nunca cambia
        el estado del caso.
        """
        now = self._now(now)
        applied = []
        for action in evaluate_escalations(self._evaluator_state(), now):
            rule = action["rule"]
            if action["action"] == "return-to-retriage":
                if self.case_state == "accepted" and self.offer_open:
                    self.return_to_retriage(
                        now, reason="unconfirmed-after-chase")
                    applied.append(action)
                    # El cambio de estado desarma R3; no va a
                    # `escalations_fired`.
            elif action["action"] == "chase-patient":
                if self.offer_open:
                    self.chase_offer(now)
                    applied.append(action)
                    # R3 NO va a `escalations_fired`: la persecución
                    # se sigue por el conteo de chase, no por la
                    # regla disparada — si no, la segunda persecución
                    # y el retorno nunca se evaluarían.
            else:
                # Escalación: una Communication por destinatario.
                trigger = {
                    ("R1", "specialty"): "escalation-acceptance",
                    ("R1", "aps-admin"): "escalation-acceptance-notify-aps",
                    ("R2", "specialty"): "escalation-offer",
                    ("R2", "aps-admin"): "escalation-offer-notify-aps",
                    ("R4", "specialty"): "escalation-counterreferral",
                    ("R4", "aps-admin"): "escalation-counterreferral-notify-aps",
                    ("R5", "aps-admin"): "escalation-retriage",
                }
                for recipient in action["recipients"]:
                    self._notify(
                        trigger[(rule, recipient)], now,
                        f"Escalación {rule}: plazo vencido sin avance; "
                        "revisar la derivación.",
                        medium="system-message")
                applied.append(action)
                # Una escalación dispara una sola vez por plazo.
                self.escalations_fired.add(rule)
        return applied

    # -- OP-5: asistencia / no-show ---------------------------------------

    def record_arrival(self, now=None):
        """La paciente llega: Appointment → `arrived`, Encounter → `in-progress`."""
        now = self._now(now)
        appointment = self.current_appointment
        if self.case_state != "scheduled" or appointment is None:
            raise WorkflowError("registrar asistencia exige una cita reservada")
        validate_appointment_transition(appointment["status"], "arrived")
        validate_encounter_transition(self.encounter["status"], "in-progress")
        appointment["status"] = "arrived"
        self.encounter["status"] = "in-progress"
        self._rebuild_task(now)
        return appointment

    def finish_encounter(self, now=None):
        """La visita termina: Encounter → `finished`, Task → `completed`.

        El Task avanza cuando el Encounter llega a `finished` (C9 del
        paso 4), no cuando la cita llega a `arrived`. Desde aquí corre
        el plazo de la contrareferencia (5 días hábiles, R4).
        """
        now = self._now(now)
        appointment = self.current_appointment
        if self.case_state != "scheduled" or appointment is None:
            raise WorkflowError("terminar el encuentro exige una visita en curso")
        validate_encounter_transition(self.encounter["status"], "finished")
        validate_appointment_transition(appointment["status"], "fulfilled")
        self.encounter["status"] = "finished"
        appointment["status"] = "fulfilled"
        self.encounter_finished_at = now
        self._record_transition(
            "completed", now, "rol-especialista", "specialist")
        self._recompute_deadlines()
        self._rebuild_task(now)
        return self.encounter

    def record_no_show(self, now=None):
        """La paciente no asiste: Appointment → `noshow`, Slot → `free`.

        El no-show vive solo en el Appointment: el Task no se mueve
        en el primer no-show (la derivación se re-agenda) y pasa a
        `no-show` en el segundo, cerrando la derivación; el
        ServiceRequest se revoca en ese momento (I1). El Encounter
        `planned` de la cita perdida queda como está — la guía no
        define un estado `cancelled` de encuentro para el no-show
        (mapeo §6) — y se conserva en `encounters` como historia
        (Ruling en `state.md`, Plan task 11.9).
        """
        now = self._now(now)
        appointment = self.current_appointment
        if self.case_state != "scheduled" or appointment is None:
            raise WorkflowError("registrar no-show exige una cita reservada")
        validate_appointment_transition(appointment["status"], "noshow")
        appointment["status"] = "noshow"
        appointment["cancelationReason"] = {"text": "patient did not attend"}
        slot_id = appointment["slot"][0]["reference"].split("/", 1)[1]
        self.slots[slot_id]["status"] = "free"
        self._notify(
            "no-show", now,
            "La paciente no asistió a su cita de cardiología; "
            "corresponde re-agendar o cerrar la derivación.")
        # El conteo mide re-agendamientos (0–1), no no-shows: el
        # primer no-show deja el Task en `scheduled` (queda un
        # re-agendamiento); el segundo lo cierra.
        if self.counts["rescheduling"] >= MAX_RESCHEDULING_COUNT:
            self._record_transition(
                "no-show", now, "rol-especialista", "specialist",
                second_no_show=True)
            validate_service_request_transition(
                self.service_request["status"], "revoked")
            self.service_request = build_service_request(
                **{**self._sr_kwargs, "status": "revoked"})
        self._recompute_deadlines()
        self._rebuild_task(now)
        return appointment

    def reschedule_after_no_show(self, slot_id, schedule_id, start, end,
                                 now=None, scheduler_role_id="rol-agendador",
                                 location_id="location-cardiologia"):
        """Re-agenda tras el primer no-show (OP-4): oferta NUEVA.

        La oferta re-agendada pasa por el mismo ciclo
        confirmar/perseguir (N5), con su propio presupuesto de
        decline/chase. Tras el segundo no-show ya no hay
        re-agendamiento: el Task está en `no-show` y es terminal.
        """
        return self.offer_appointment(
            slot_id, schedule_id, start, end, now=now,
            scheduler_role_id=scheduler_role_id, location_id=location_id)

    # -- invariantes -------------------------------------------------------

    def check_invariants(self):
        """Comprueba I1–I6 sobre el estado actual (ver `transitions.py`)."""
        return check_invariants({
            "case_state": self.case_state,
            "retriage_decided": self.retriage_decided,
            "service_request_status": self.service_request["status"],
            "appointments": self.appointments,
            "encounter_status": (
                self.encounter["status"] if self.encounter else None),
            "encounter_created_at": "booking" if self.encounter else None,
        })

    # -- OP-6: contrareferencia -------------------------------------------

    def send_counter_referral(
        self, now=None, specialist_role_id="rol-especialista",
        counter_referral_id="CR-2026-0001",
        diagnosis_text="Insuficiencia cardiaca sistólica crónica (FEVI 35%)",
        diagnosis_note="FEVI 35% por ecocardiograma. Sin isquemia aguda en el ECG.",
        plan_activities=None,
        diagnosis_section="Chronic systolic heart failure, LVEF 35% (ICD-10-CM I50.22).",
        plan_section="Start heart-failure treatment; control in APS in 2 weeks.",
        follow_up_indications="Blood pressure, weight and symptoms at each APS control; NT-proBNP in 3 months.",
        follow_up_plan="APS follow-up as in the CarePlan; new referral to cardiology if dyspnoea worsens.",
    ):
        """Envía la contrareferencia (Bundle de documento, PI-3).

        Construye Condition + CarePlan + Composition +
        DocumentReference y el Bundle (`type = document`, la
        Composition primera). El envío NO mueve el Task: sigue en
        `completed`, pero desarma R4 y bloquea la cancelación (OP-8);
        el Task pasa a `counter-referred` con el acuse de recibo de
        APS (`acknowledge_counter_referral`).
        """
        now = self._now(now)
        if self.case_state != "completed":
            raise WorkflowError(
                f"enviar la contrareferencia exige completed, "
                f"no {self.case_state!r}")
        if self.counter_referral_sent:
            raise WorkflowError("la contrareferencia ya se envió (OP-6)")
        if plan_activities is None:
            plan_activities = [
                "Control en APS en 2 semanas: presión arterial, peso, síntomas.",
                "NT-proBNP de control en 3 meses.",
            ]
        encounter_id = self.encounter["id"]
        period = self.encounter["period"]
        self.condition = build_condition(
            resource_id=f"diagnostico-{self.sr_id}",
            patient_id=self.patient_id,
            encounter_id=encounter_id,
            text=diagnosis_text,
            note_text=diagnosis_note,
        )
        self.care_plan = build_care_plan(
            resource_id=f"plan-{self.sr_id}",
            patient_id=self.patient_id,
            encounter_id=encounter_id,
            specialist_role_id=specialist_role_id,
            condition_id=self.condition["id"],
            activities=plan_activities,
            service_request_id=self.sr_id,
        )
        self.composition = build_composition(
            resource_id=f"contrareferencia-{self.sr_id}",
            referral_id=self.referral_id,
            patient_id=self.patient_id,
            encounter_id=encounter_id,
            specialist_role_id=specialist_role_id,
            condition_id=self.condition["id"],
            care_plan_id=self.care_plan["id"],
            date=now,
            diagnosis_section=diagnosis_section,
            plan_section=plan_section,
            follow_up_indications=follow_up_indications,
            follow_up_plan=follow_up_plan,
            counter_referral_id=counter_referral_id,
        )
        self.document_reference = build_document_reference(
            resource_id=f"documento-{self.sr_id}",
            composition_id=self.composition["id"],
            patient_id=self.patient_id,
            encounter_id=encounter_id,
            service_request_id=self.sr_id,
            specialist_role_id=specialist_role_id,
            date=now,
            period_start=period["start"],
            period_end=period["end"],
            counter_referral_id=counter_referral_id,
        )
        self.counter_referral_bundle = build_document_bundle(
            self.composition,
            self.document_reference,
            self.condition,
            self.care_plan,
            timestamp=now,
            resource_id=f"bundle-pi3-{self.sr_id}",
        )
        self.counter_referral_sent = True
        self._recompute_deadlines()
        self._rebuild_task(now)
        return self.counter_referral_bundle

    def acknowledge_counter_referral(self, now=None,
                                     aps_admin_role_id="rol-admin-aps"):
        """APS acusa recibo de la contrareferencia (OP-6) y cierra el ciclo.

        Registra la Communication de acuse (`basedOn` → Task,
        `payload.contentReference` → DocumentReference), informa a la
        paciente, mueve el Task a `counter-referred` y el
        ServiceRequest a `completed`.
        """
        now = self._now(now)
        if self.case_state != "completed":
            raise WorkflowError(
                f"acusar recibo exige completed, no {self.case_state!r}")
        if not self.counter_referral_sent:
            raise WorkflowError(
                "no hay contrareferencia enviada que acusar (OP-6)")
        self._notify(
            "counter-referral-receipt", now, medium="system-message",
            document_id=self.document_reference["id"])
        self._notify(
            "counter-referred", now,
            "Su contrareferencia de cardiología llegó a su CESFAM; "
            "su médico APS tiene el diagnóstico y el plan de seguimiento.")
        self._record_transition(
            "counter-referred", now, aps_admin_role_id, "aps-admin")
        validate_service_request_transition(
            self.service_request["status"], "completed")
        self.service_request = build_service_request(
            **{**self._sr_kwargs, "status": "completed"})
        self._recompute_deadlines()
        self._rebuild_task(now)
        return self.task

    # -- OP-7: consulta de estado (solo lectura) --------------------------

    def query_status(self, now=None):
        """Consulta de estado (PI-4): estado actual, último cambio y
        próximo paso esperado (spec §3.7). Solo lectura: no cambia el
        estado, no notifica, no crea recursos. Ningún perfil IHE
        cubre la consulta de estado del flujo (revisión del paso 4).
        """
        now = self._now(now)
        last = self.history[-1] if self.history else None
        return {
            "referral_id": self.referral_id,
            "case_state": self.case_state,
            "task_status": self.task["status"],
            "last_modified": self.task.get("lastModified"),
            "last_transition": (
                {
                    "recorded": last["recorded"],
                    "actor": last["agent"][0]["type"]["coding"][0]["code"],
                    "actor_id": last["agent"][0]["who"]["reference"],
                }
                if last
                else None
            ),
            "next_step": DESCRIPTIONS[self.case_state],
            "service_request_status": self.service_request["status"],
            "offer_open": self.offer_open,
            "counts": dict(self.counts),
            "deadlines": {
                key: value.isoformat()
                for key, value in self.deadlines.items()
                if value is not None
            },
            "queried_at": now.isoformat(),
        }

    # -- OP-8: cancelación y re-apertura -----------------------------------

    def cancel(self, now=None, actor_role_id="rol-admin-aps",
               role_code="aps-admin", reason_text=None):
        """Cancela la derivación en cualquier punto antes de completarse.

        Cualquier parte puede cancelar (APS, paciente, especialidad);
        el motivo es obligatorio y viaja en `Task.statusReason`. La
        cita reservada pasa a `cancelled` y su Slot vuelve a `free`;
        el Encounter `planned` pasa a `cancelled` (lifecycle.md). Una
        cancelación tras empezar la visita se registra solo en el
        Task, no cancelando el Encounter. No se puede cancelar tras
        enviar la contrareferencia, ni un estado terminal, ni un
        `rejected` con la decisión de re-triaje ya tomada (N1).
        """
        now = self._now(now)
        if self.case_state in ("counter-referred", "no-show", "cancelled"):
            raise WorkflowError(
                f"no se puede cancelar un estado terminal "
                f"{self.case_state!r} (OP-8)")
        if self.counter_referral_sent:
            raise WorkflowError(
                "no se puede cancelar tras enviar la contrareferencia (OP-8)")
        if not reason_text:
            raise WorkflowError("la cancelación exige un motivo (OP-8)")
        validate_task_transition(
            self.case_state, "cancelled",
            retriage_decided=self.retriage_decided)
        self._pre_cancel_state = self.case_state
        self._status_reason = {"text": reason_text}
        appointment = self.current_appointment
        if appointment is not None and appointment["status"] in (
            "proposed", "pending", "booked"
        ):
            validate_appointment_transition(appointment["status"], "cancelled")
            appointment["status"] = "cancelled"
            appointment["cancelationReason"] = {"text": reason_text}
            slot_id = appointment["slot"][0]["reference"].split("/", 1)[1]
            self.slots[slot_id]["status"] = "free"
        if self.encounter is not None and self.encounter["status"] == "planned":
            validate_encounter_transition("planned", "cancelled")
            self.encounter["status"] = "cancelled"
        self._record_transition(
            "cancelled", now, actor_role_id, role_code)
        validate_service_request_transition(
            self.service_request["status"], "revoked")
        self.service_request = build_service_request(
            **{**self._sr_kwargs, "status": "revoked"})
        self.offer_open = False
        self.offer_confirmed = False
        self._recompute_deadlines()
        self._rebuild_task(now)
        self._notify(
            "cancelled", now,
            f"Su derivación a cardiología fue cancelada: {reason_text}.",
            medium="system-message")
        self._notify(
            "cancelled-notify-aps", now,
            f"Derivación cancelada: {reason_text}.",
            medium="system-message")
        self._notify(
            "cancelled-notify-specialty", now,
            f"Derivación cancelada: {reason_text}.",
            medium="system-message")
        return self.task

    def reopen(self, target_case_state, now=None, actor_role="hub-operator"):
        """Re-abre una derivación cancelada en error (único camino de
        corrección de un `cancelled`, paso 3 §13).

        Solo el operador del hub, solo al estado previo a la
        cancelación, nunca a un estado terminal. El ServiceRequest
        vuelve a `active`; la cita cancelada NO se restaura (el
        agendador debe re-ofertar) — Ruling en `state.md` (Plan task
        11.11). Una cancelación legítima posterior es una segunda
        entrada (C9 del paso 3).
        """
        now = self._now(now)
        validate_reopen(self.case_state, target_case_state, actor_role)
        if target_case_state != getattr(self, "_pre_cancel_state", None):
            raise WorkflowError(
                "la re-apertura vuelve al estado previo a la cancelación, "
                f"no a {target_case_state!r}")
        self.case_state = target_case_state
        self._status_reason = None
        self._recompute_deadlines()
        self._rebuild_task(now)
        provenance = build_provenance(
            resource_id=self._next_id("provenance"),
            task_id=self.task_id,
            actor_role_id="rol-operador-hub",
            role_code="hub-operator",
            recorded=now,
        )
        self.history.append(provenance)
        self._notify_subscribers(target_case_state, now)
        self.service_request = build_service_request(
            **{**self._sr_kwargs, "status": "active"})
        return self.task

    # -- OP-11: suscripción a los cambios de estado -------------------------

    def subscribe(self, endpoint, now=None):
        """Suscribe un endpoint a los cambios de estado del Task (OP-11).

        El hub notifica en cada transición del Task (ver
        `_notify_subscribers`). La suscripción puede crearse en
        cualquier estado de la derivación.
        """
        subscription = build_subscription(
            resource_id=self._next_id("suscripcion"),
            referral_id=self.referral_id,
            endpoint=endpoint,
        )
        subscription["_active"] = True
        subscription["notifications"] = []
        self.subscriptions.append(subscription)
        return subscription

    def unsubscribe(self, subscription_id, now=None):
        """Da de baja una suscripción (OP-11): deja de notificar."""
        for subscription in self.subscriptions:
            if subscription["id"] == subscription_id:
                subscription["status"] = "off"
                subscription["_active"] = False
                return subscription
        raise WorkflowError(
            f"suscripción desconocida: {subscription_id!r} (OP-11)")
