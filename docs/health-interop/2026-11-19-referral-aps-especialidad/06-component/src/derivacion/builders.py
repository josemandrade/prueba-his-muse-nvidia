"""Constructores de los recursos de la guía (perfiles `Derivacion*`).

Cada constructor emite el JSON del perfil con sus valores fijos
(`meta.profile`, códigos, cardinalidades) y valida sus entradas.
Nada aquí re-inventa un perfil: los valores vienen de
`input/fsh/*.fsh` y de los ejemplos compilados por SUSHI, que son
los goldens de los tests.
"""

from derivacion.constants import (
    APPOINTMENT_ID_SYSTEM,
    CHANNELS,
    COUNTER_REFERRAL_ID_SYSTEM,
    DELIVERY_OUTCOMES,
    ENCOUNTER_ID_SYSTEM,
    ICD10CM_CHRONIC_SYSTOLIC_HF,
    ICD10CM_SYSTEM,
    LOINC_CONSULT_NOTE,
    LOINC_SYSTEM,
    MATCH_BASES,
    MPI_SYSTEM,
    NOTIFICATION_ID_SYSTEM,
    ORGANIZATION_APS_SYSTEM,
    ORGANIZATION_HUB_SYSTEM,
    ORGANIZATION_SPECIALTY_SYSTEM,
    REFERRAL_ID_SYSTEM,
    ROLES,
    RUN_SYSTEM,
    SERVICE_ID_SYSTEM,
    SNOMED_SYSTOLIC_HEART_FAILURE,
    SNOMED_SYSTEM,
    code_system_url,
    extension_url,
    profile_url,
    value_set_url,
)

ROLE_DISPLAYS = {
    "aps-doctor": "APS doctor",
    "aps-admin": "APS admin",
    "triage-clinician": "Triage clinician",
    "specialty-scheduler": "Specialty scheduler",
    "specialist": "Specialist",
    "hub-operator": "Hub operator",
}

SPECIALTY_DISPLAYS = {"cardiologia": "Cardiology"}


def ref(resource_type, resource_id):
    return {"reference": f"{resource_type}/{resource_id}"}


def coding(system, code, display=None):
    entry = {"code": code, "system": system}
    if display is not None:
        entry["display"] = display
    return entry


def codeable(codings, text=None):
    concept = {"coding": codings}
    if text is not None:
        concept["text"] = text
    return concept


def meta(profile_name):
    return {"profile": [profile_url(profile_name)]}


def extension(url, value_key, value):
    return {"url": url, value_key: value}


def _require(value, message):
    if not value:
        raise ValueError(message)
    return value


# ---------------------------------------------------------------------------
# Recursos base (sin perfil propio en la guía)
# ---------------------------------------------------------------------------


def build_practitioner(resource_id, run, family, given, gender=None):
    """Practitioner base R4 (la persona; el rol es DerivacionRol)."""
    practitioner = {
        "resourceType": "Practitioner",
        "id": resource_id,
        "identifier": [
            {"system": RUN_SYSTEM, "value": run},
        ],
        "name": [
            {"use": "official", "family": family, "given": [given]},
        ],
    }
    if gender is not None:
        practitioner["gender"] = gender
    return practitioner


def build_organization(resource_id, system, value, name):
    """Organization base R4 (APS, especialidad o hub)."""
    return {
        "resourceType": "Organization",
        "id": resource_id,
        "identifier": [{"system": system, "value": value}],
        "name": name,
        "active": True,
    }


def build_endpoint(resource_id, organization_id, address, name=None):
    """Endpoint base R4 (connectionType = hl7-fhir-rest)."""
    endpoint = {
        "resourceType": "Endpoint",
        "id": resource_id,
        "status": "active",
        "connectionType": {
            "code": "hl7-fhir-rest",
            "system": "http://terminology.hl7.org/CodeSystem/endpoint-connection-type",
            "display": "HL7 FHIR",
        },
        "managingOrganization": ref("Organization", organization_id),
        "payloadType": [
            {
                "coding": [
                    {
                        "code": "any",
                        "system": "http://terminology.hl7.org/CodeSystem/endpoint-payload-type",
                        "display": "Any",
                    }
                ]
            }
        ],
        "address": address,
    }
    if name is not None:
        endpoint["name"] = name
    return endpoint


# ---------------------------------------------------------------------------
# Perfiles propios de la guía
# ---------------------------------------------------------------------------


def build_patient(
    resource_id,
    run,
    family,
    given,
    birth_date,
    telecom,
    mpi_key=None,
    gender=None,
    address_text=None,
    preferred_channel=None,
):
    """DerivacionPaciente: RUN + clave MPI + contacto obligatorio (C12)."""
    _require(telecom, "los datos de contacto son obligatorios (C12)")
    if preferred_channel is not None and preferred_channel not in CHANNELS:
        raise ValueError(f"canal desconocido: {preferred_channel!r}")
    # El golden ordena los identificadores RUN primero, MPI después.
    identifiers = [{"system": RUN_SYSTEM, "value": run}]
    if mpi_key is not None:
        identifiers.append({"system": MPI_SYSTEM, "value": mpi_key})
    patient = {
        "resourceType": "Patient",
        "id": resource_id,
        "meta": meta("DerivacionPaciente"),
        "identifier": identifiers,
        "name": [
            {"use": "official", "family": family, "given": [given]},
        ],
        "birthDate": birth_date,
        "telecom": telecom,
    }
    extensions = []
    if preferred_channel is not None:
        extensions.append(
            extension(
                extension_url("preferred-contact-channel"),
                "valueCode",
                preferred_channel,
            )
        )
    if extensions:
        patient["extension"] = extensions
    if gender is not None:
        patient["gender"] = gender
    if address_text is not None:
        patient["address"] = [{"use": "home", "text": address_text}]
    return patient


def build_practitioner_role(resource_id, practitioner_id, organization_id, role):
    """DerivacionRol: el rol que un profesional tiene en la derivación."""
    if role not in ROLES:
        raise ValueError(f"rol desconocido: {role!r} (seis roles, C1)")
    return {
        "resourceType": "PractitionerRole",
        "id": resource_id,
        "meta": meta("DerivacionRol"),
        "practitioner": ref("Practitioner", practitioner_id),
        "organization": ref("Organization", organization_id),
        "code": [
            codeable(
                [
                    coding(
                        code_system_url("rol"),
                        role,
                        ROLE_DISPLAYS[role],
                    )
                ]
            )
        ],
        "active": True,
    }


def build_healthcare_service(
    resource_id,
    service_code,
    organization_id,
    endpoint_id=None,
    active=True,
):
    """DerivacionServicio: el servicio de especialidad (directorio)."""
    if service_code not in SPECIALTY_DISPLAYS:
        raise ValueError(
            f"servicio desconocido: {service_code!r} (catálogo local)"
        )
    service = {
        "resourceType": "HealthcareService",
        "id": resource_id,
        "meta": meta("DerivacionServicio"),
        "identifier": [
            {"system": SERVICE_ID_SYSTEM, "value": service_code},
        ],
        "providedBy": ref("Organization", organization_id),
        "type": [
            codeable(
                [
                    coding(
                        code_system_url("especialidad"),
                        service_code,
                        SPECIALTY_DISPLAYS[service_code],
                    )
                ]
            )
        ],
        "name": SPECIALTY_DISPLAYS[service_code],
        "active": active,
    }
    if endpoint_id is not None:
        service["endpoint"] = [ref("Endpoint", endpoint_id)]
    return service


# ---------------------------------------------------------------------------
# OP-1: ServiceRequest + Task + Bundle de transacción
# ---------------------------------------------------------------------------

CASE_STATE_DISPLAYS = {
    "requested": "Requested",
    "received": "Received",
    "accepted": "Accepted",
    "rejected": "Rejected",
    "scheduled": "Scheduled",
    "completed": "Completed",
    "counter-referred": "Counter-referred",
    "no-show": "No-show",
    "cancelled": "Cancelled",
}

# Plazo SLA → nombre de la extensión del Task.
DEADLINE_EXTENSIONS = {
    "acceptance": "sla-acceptance-deadline",
    "offer": "sla-offer-deadline",
    "confirmation": "sla-confirmation-deadline",
    "counterreferral": "sla-counterreferral-deadline",
    "retriage": "sla-retriage-deadline",
}

# Conteo del Task → (nombre de la extensión, mínimo, máximo).
COUNT_EXTENSIONS = {
    "decline": ("offer-decline-count", 0, 2),
    "chase": ("offer-chase-count", 0, 2),
    "rescheduling": ("rescheduling-count", 0, 1),
}


def _iso(value):
    """Un datetime a ISO con zona (o la cadena tal cual)."""
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


def build_service_request(
    resource_id,
    referral_id,
    patient_id,
    requester_role_id,
    service_code,
    reason_snomed,
    reason_text,
    priority,
    authored_on,
    aps_encounter_id=None,
    supporting_info_ids=None,
    note_text=None,
    status="active",
    performer_service_id=None,
    reason_display=None,
):
    """DerivacionSolicitud: la derivación que APS crea (OP-1)."""
    if priority not in ("routine", "urgent"):
        raise ValueError(f"prioridad desconocida: {priority!r} (routine | urgent)")
    if not str(reason_snomed).isdigit():
        raise ValueError(f"el motivo es SNOMED CT: {reason_snomed!r} no es un código")
    if service_code not in SPECIALTY_DISPLAYS:
        raise ValueError(
            f"servicio desconocido: {service_code!r} (catálogo local)"
        )
    request = {
        "resourceType": "ServiceRequest",
        "id": resource_id,
        "meta": meta("DerivacionSolicitud"),
        "identifier": [
            {"system": REFERRAL_ID_SYSTEM, "value": referral_id},
        ],
        "status": status,
        "intent": "order",
        "code": codeable(
            [
                coding(
                    code_system_url("especialidad"),
                    service_code,
                    SPECIALTY_DISPLAYS[service_code],
                )
            ]
        ),
        "subject": ref("Patient", patient_id),
        "authoredOn": _iso(authored_on),
        "requester": ref("PractitionerRole", requester_role_id),
        "performerType": codeable(
            [
                coding(
                    code_system_url("especialidad"),
                    service_code,
                    SPECIALTY_DISPLAYS[service_code],
                )
            ]
        ),
        "reasonCode": [
            codeable(
                [
                    coding(
                        "http://snomed.info/sct",
                        reason_snomed,
                        reason_display,
                    )
                ],
                text=reason_text,
            )
        ],
        "priority": priority,
    }
    if aps_encounter_id is not None:
        request["encounter"] = ref("Encounter", aps_encounter_id)
    if performer_service_id is not None:
        request["performer"] = [ref("HealthcareService", performer_service_id)]
    if supporting_info_ids:
        request["supportingInfo"] = [
            ref("Observation", observation_id)
            for observation_id in supporting_info_ids
        ]
    if note_text is not None:
        request["note"] = [{"text": note_text}]
    return request


def build_task(
    resource_id,
    referral_id,
    patient_id,
    requester_role_id,
    service_request_id,
    case_state,
    description,
    now,
    deadlines=None,
    counts=None,
    owner_service_id=None,
    status_reason=None,
    relevant_history_ids=None,
):
    """DerivacionTarea: el registro de estado del flujo de trabajo.

    `case_state` es uno de los nueve estados del caso; `Task.status`
    es el valor grueso R4 que corresponde (lifecycle.md). `deadlines`
    es un dict plazo → datetime; `counts` es un dict conteo → entero
    (con sus invariantes de rango). `status_reason` es un dict con
    `code`/`display` (motivo de rechazo) o `text` ("patient deceased").
    """
    from derivacion.constants import CASE_STATE_TO_TASK_STATUS, CASE_STATES

    if case_state not in CASE_STATES:
        raise ValueError(f"estado del caso desconocido: {case_state!r}")
    extensions = []
    for key, value in (deadlines or {}).items():
        if value is None:
            continue
        extensions.append(
            extension(
                extension_url(DEADLINE_EXTENSIONS[key]),
                "valueDateTime",
                _iso(value),
            )
        )
    for key, value in (counts or {}).items():
        name, minimum, maximum = COUNT_EXTENSIONS[key]
        if not minimum <= value <= maximum:
            raise ValueError(
                f"el conteo {key} debe estar entre {minimum} y {maximum}: {value}"
            )
        extensions.append(
            extension(extension_url(name), "valueInteger", value)
        )
    task = {
        "resourceType": "Task",
        "id": resource_id,
        "meta": meta("DerivacionTarea"),
        "identifier": [
            {"system": REFERRAL_ID_SYSTEM, "value": referral_id},
        ],
        "status": CASE_STATE_TO_TASK_STATUS[case_state],
        "businessStatus": codeable(
            [
                coding(
                    code_system_url("estado-referencia"),
                    case_state,
                    CASE_STATE_DISPLAYS[case_state],
                )
            ]
        ),
        "intent": "order",
        "code": codeable(
            [
                coding(
                    code_system_url("task-code"),
                    "referral-workflow",
                    "Referral workflow",
                )
            ]
        ),
        "focus": ref("ServiceRequest", service_request_id),
        "for": ref("Patient", patient_id),
        "authoredOn": _iso(now),
        "lastModified": _iso(now),
        "requester": ref("PractitionerRole", requester_role_id),
        "description": description,
    }
    if extensions:
        task["extension"] = extensions
    if owner_service_id is not None:
        task["owner"] = ref("HealthcareService", owner_service_id)
    if status_reason is not None:
        if "code" in status_reason:
            task["statusReason"] = codeable(
                [
                    coding(
                        status_reason.get("system", code_system_url("motivo-rechazo")),
                        status_reason["code"],
                        status_reason.get("display"),
                    )
                ]
            )
        else:
            task["statusReason"] = {"text": status_reason["text"]}
    if relevant_history_ids:
        task["relevantHistory"] = [
            ref("Provenance", history_id)
            for history_id in relevant_history_ids
        ]
    return task


def build_transaction_bundle(resources, resource_id=None):
    """Bundle de tipo transaction (OP-1): POST por recurso, en orden."""
    import uuid

    bundle = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "fullUrl": f"urn:uuid:{uuid.uuid4()}",
                "resource": resource,
                "request": {
                    "method": "POST",
                    "url": resource["resourceType"],
                },
            }
            for resource in resources
        ],
    }
    if resource_id is not None:
        bundle["id"] = resource_id
    return bundle


# ---------------------------------------------------------------------------
# OP-2 / OP-12: Communication + Provenance
# ---------------------------------------------------------------------------

CHANNEL_DISPLAYS = {
    "phone": "Phone",
    "in-person": "In person",
    "system-message": "System message",
}


def build_communication(
    resource_id,
    notification_id,
    patient_id,
    task_id,
    trigger,
    sender_role_code,
    sender_role_id,
    recipient_type,
    recipient_id,
    sent,
    medium,
    message=None,
    delivery_outcome=None,
    document_id=None,
    sender_type="PractitionerRole",
):
    """DerivacionNotificacion: el registro de un aviso enviado (OP-12).

    `trigger` es el nombre codificado de la transición que disparó el
    envío (p. ej. "accepted"); va en `topic` (CodeableConcept, R4 —
    la corrección del paso 5: `topic` NO es una referencia). El enlace
    al Task es `basedOn`; el aviso legible es `payload.contentString`.
    El emisor es un rol nombrado (C5/Q3); el destinatario es el paciente
    o un rol nombrado (PractitionerRole) — el perfil
    DerivacionNotificacion no admite Organization como `recipient`
    (C3, revisión experta del paso 6).
    """
    if sender_role_code not in ROLES:
        raise ValueError(f"emisor no nombrado: {sender_role_code!r} (C5/Q3)")
    if medium not in CHANNELS:
        raise ValueError(f"canal desconocido: {medium!r} (lista local)")
    if delivery_outcome is not None and delivery_outcome not in DELIVERY_OUTCOMES:
        raise ValueError(f"resultado de entrega desconocido: {delivery_outcome!r}")
    if recipient_type not in ("Patient", "PractitionerRole"):
        raise ValueError(
            f"destinatario no admitido por DerivacionNotificacion: "
            f"{recipient_type!r} (solo Patient o PractitionerRole)")
    _require(trigger, "la notificación necesita la transición que la disparó")
    communication = {
        "resourceType": "Communication",
        "id": resource_id,
        "meta": meta("DerivacionNotificacion"),
        "identifier": [
            {"system": NOTIFICATION_ID_SYSTEM, "value": notification_id},
        ],
        "status": "completed",
        "category": [
            codeable(
                [
                    coding(
                        "http://terminology.hl7.org/CodeSystem/communication-category",
                        "notification",
                        "Notification",
                    )
                ]
            )
        ],
        "subject": ref("Patient", patient_id),
        "basedOn": [ref("Task", task_id)],
        "topic": {"text": trigger},
        "sender": ref(sender_type, sender_role_id),
        "recipient": [ref(recipient_type, recipient_id)],
        "sent": _iso(sent),
        "medium": [
            codeable(
                [
                    coding(
                        code_system_url("canal"),
                        medium,
                        CHANNEL_DISPLAYS[medium],
                    )
                ]
            )
        ],
    }
    payload = []
    if message is not None:
        payload.append({"contentString": message})
    if document_id is not None:
        payload.append(
            {"contentReference": ref("DocumentReference", document_id)}
        )
    if payload:
        communication["payload"] = payload
    if delivery_outcome is not None:
        communication["extension"] = [
            extension(
                extension_url("delivery-outcome"),
                "valueCode",
                delivery_outcome,
            )
        ]
    return communication


def build_provenance(
    resource_id,
    task_id,
    actor_role_id,
    role_code,
    recorded,
    agent_type="PractitionerRole",
):
    """Provenance de una transición del Task (OP-2, OP-8, re-apertura).

    El agente es el rol que hizo la transición (p. ej. el clínico de
    triaje en la aceptación); el profesional que acepta va aquí, no
    en `Task.owner` (corrección R4 del paso 5). El operador del hub
    actúa como PractitionerRole (`rol-operador-hub`, C3).
    """
    if role_code not in ROLES:
        raise ValueError(f"rol desconocido: {role_code!r} (seis roles, C1)")
    return {
        "resourceType": "Provenance",
        "id": resource_id,
        "target": [ref("Task", task_id)],
        "recorded": _iso(recorded),
        "agent": [
            {
                "type": codeable(
                    [coding(code_system_url("rol"), role_code, ROLE_DISPLAYS[role_code])]
                ),
                "who": ref(agent_type, actor_role_id),
            }
        ],
        "activity": {
            "system": "http://terminology.hl7.org/CodeSystem/v3-DataOperation",
            "code": "UPDATE",
            "display": "revise",
        },
    }


# ---------------------------------------------------------------------------
# OP-3: Appointment + AppointmentResponse + Encounter + Slot/Schedule
# ---------------------------------------------------------------------------

SLOT_STATUSES = {"free", "busy", "busy-unavailable", "busy-tentative", "entered-in-error"}


def build_location(resource_id, name, address_text, organization_id):
    """Location base R4 (la consulta de la especialidad)."""
    return {
        "resourceType": "Location",
        "id": resource_id,
        "name": name,
        "address": {"text": address_text},
        "managingOrganization": ref("Organization", organization_id),
    }


def build_schedule(resource_id, service_id, start, end, comment=None):
    """Schedule base R4 (la agenda del servicio)."""
    schedule = {
        "resourceType": "Schedule",
        "id": resource_id,
        "actor": [ref("HealthcareService", service_id)],
        "planningHorizon": {
            "start": _iso(start),
            "end": _iso(end),
        },
    }
    if comment is not None:
        schedule["comment"] = comment
    return schedule


def build_slot(resource_id, schedule_id, start, end, status="free"):
    """Slot base R4 (un hueco de la agenda)."""
    if status not in SLOT_STATUSES:
        raise ValueError(f"estado de Slot desconocido: {status!r}")
    return {
        "resourceType": "Slot",
        "id": resource_id,
        "schedule": ref("Schedule", schedule_id),
        "status": status,
        "start": _iso(start),
        "end": _iso(end),
    }


def build_appointment(
    resource_id,
    appointment_id,
    service_request_id,
    slot_id,
    patient_id,
    specialist_role_id,
    location_id,
    service_code,
    start,
    end,
    created,
    offer_number,
    status="proposed",
    patient_instruction=None,
):
    """DerivacionCita: la oferta y la reserva de la cita.

    `status` sigue la cadena proposed → pending → booked → arrived →
    fulfilled (la validación de la transición vive en
    `transitions.py`, no aquí). `offer_number` es el contador por
    derivación: cada oferta es un Appointment NUEVO.
    """
    if service_code not in SPECIALTY_DISPLAYS:
        raise ValueError(
            f"servicio desconocido: {service_code!r} (catálogo local)"
        )
    appointment = {
        "resourceType": "Appointment",
        "id": resource_id,
        "meta": meta("DerivacionCita"),
        "extension": [
            extension(
                extension_url("offer-number"), "valueInteger", offer_number
            )
        ],
        "identifier": [
            {"system": APPOINTMENT_ID_SYSTEM, "value": appointment_id},
        ],
        "status": status,
        "basedOn": [ref("ServiceRequest", service_request_id)],
        "slot": [ref("Slot", slot_id)],
        "created": _iso(created),
        "start": _iso(start),
        "end": _iso(end),
        "participant": [
            {
                "actor": ref("Patient", patient_id),
                "status": "needs-action",
            },
            {
                "actor": ref("PractitionerRole", specialist_role_id),
                "status": "accepted",
            },
            {
                "actor": ref("Location", location_id),
                "status": "accepted",
            },
        ],
        "serviceType": [
            codeable(
                [
                    coding(
                        code_system_url("especialidad"),
                        service_code,
                        SPECIALTY_DISPLAYS[service_code],
                    )
                ]
            )
        ],
    }
    if patient_instruction is not None:
        appointment["patientInstruction"] = patient_instruction
    return appointment


def build_appointment_response(
    resource_id, appointment_id, patient_id, participant_status="accepted"
):
    """AppointmentResponse base R4 (la decisión de la paciente)."""
    if participant_status not in (
        "accepted",
        "declined",
        "tentative",
        "needs-action",
    ):
        raise ValueError(
            f"participantStatus desconocido: {participant_status!r}"
        )
    return {
        "resourceType": "AppointmentResponse",
        "id": resource_id,
        "appointment": ref("Appointment", appointment_id),
        "actor": ref("Patient", patient_id),
        "participantStatus": participant_status,
    }


def build_encounter(
    resource_id,
    encounter_id,
    patient_id,
    service_request_id,
    appointment_id,
    specialist_role_id,
    service_code,
    start,
    end,
    status="planned",
):
    """DerivacionEncuentro: la visita (existe desde la reserva).

    `status` sigue planned → in-progress → finished (R4 no tiene
    `scheduled`; el valor es `planned`). En un no-show NO hay
    Encounter: el no-show vive solo en el Appointment.
    """
    if service_code not in SPECIALTY_DISPLAYS:
        raise ValueError(
            f"servicio desconocido: {service_code!r} (catálogo local)"
        )
    return {
        "resourceType": "Encounter",
        "id": resource_id,
        "meta": meta("DerivacionEncuentro"),
        "identifier": [
            {"system": ENCOUNTER_ID_SYSTEM, "value": encounter_id},
        ],
        "status": status,
        "class": {
            "code": "AMB",
            "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
            "display": "Ambulatory",
        },
        "subject": ref("Patient", patient_id),
        "basedOn": [ref("ServiceRequest", service_request_id)],
        "appointment": [ref("Appointment", appointment_id)],
        "period": {"start": _iso(start), "end": _iso(end)},
        "participant": [
            {"individual": ref("PractitionerRole", specialist_role_id)}
        ],
        "serviceType": codeable(
            [
                coding(
                    code_system_url("especialidad"),
                    service_code,
                    SPECIALTY_DISPLAYS[service_code],
                )
            ]
        ),
    }


# ---------------------------------------------------------------------------
# OP-6: contrareferencia (Composition + DocumentReference + Condition
# + CarePlan + Bundle de documento)
# ---------------------------------------------------------------------------


def build_condition(
    resource_id,
    patient_id,
    encounter_id,
    text,
    note_text=None,
    icd10cm_code=ICD10CM_CHRONIC_SYSTOLIC_HF,
    icd10cm_display="Chronic systolic (congestive) heart failure",
    snomed_code=SNOMED_SYSTOLIC_HEART_FAILURE,
    snomed_display="Systolic heart failure",
):
    """DerivacionDiagnostico: el diagnóstico de egreso de la visita."""
    condition = {
        "resourceType": "Condition",
        "id": resource_id,
        "meta": meta("DerivacionDiagnostico"),
        "clinicalStatus": codeable(
            [
                coding(
                    "http://terminology.hl7.org/CodeSystem/condition-clinical",
                    "active",
                    "Active",
                )
            ]
        ),
        "verificationStatus": codeable(
            [
                coding(
                    "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                    "confirmed",
                    "Confirmed",
                )
            ]
        ),
        "code": codeable(
            [
                coding(ICD10CM_SYSTEM, icd10cm_code, icd10cm_display),
                coding(SNOMED_SYSTEM, snomed_code, snomed_display),
            ],
            text=text,
        ),
        "subject": ref("Patient", patient_id),
        "encounter": ref("Encounter", encounter_id),
    }
    if note_text is not None:
        condition["note"] = [{"text": note_text}]
    return condition


def build_care_plan(
    resource_id,
    patient_id,
    encounter_id,
    specialist_role_id,
    condition_id,
    activities,
    service_request_id,
):
    """DerivacionPlanSeguimiento: el plan de seguimiento para APS.

    `activities` es la lista de descripciones de las actividades del
    plan; el último elemento es siempre la referencia a la solicitud
    original (el plan cierra el ciclo de la derivación).
    """
    return {
        "resourceType": "CarePlan",
        "id": resource_id,
        "meta": meta("DerivacionPlanSeguimiento"),
        "status": "active",
        "intent": "plan",
        "subject": ref("Patient", patient_id),
        "encounter": ref("Encounter", encounter_id),
        "author": ref("PractitionerRole", specialist_role_id),
        "addresses": [ref("Condition", condition_id)],
        "activity": [
            {"detail": {"description": text, "status": "active"}}
            for text in activities
        ]
        + [{"reference": ref("ServiceRequest", service_request_id)}],
    }


def _composition_section(title, text, entry_type=None, entry_id=None):
    section = {
        "title": title,
        "code": {"text": title},
        "text": {
            "status": "generated",
            "div": f'<div xmlns="http://www.w3.org/1999/xhtml">{text}</div>',
        },
    }
    if entry_type is not None:
        section["entry"] = [ref(entry_type, entry_id)]
    return section


def build_composition(
    resource_id,
    referral_id,
    patient_id,
    encounter_id,
    specialist_role_id,
    condition_id,
    care_plan_id,
    date,
    diagnosis_section,
    plan_section,
    follow_up_indications,
    follow_up_plan,
    counter_referral_id="CR-2026-0001",
):
    """DerivacionContrareferencia: el documento de contrareferencia.

    Las cuatro secciones se distinguen por `title` (corrección C1
    del paso 5: el discriminador de slicing es `title`, no `code`).
    El estado es `final`: el perfil fija el valor, un borrador es
    una Composition sin este perfil (C7 del paso 5).
    """
    return {
        "resourceType": "Composition",
        "id": resource_id,
        "meta": meta("DerivacionContrareferencia"),
        "status": "final",
        "type": codeable(
            [coding(LOINC_SYSTEM, LOINC_CONSULT_NOTE, "Consult note")]
        ),
        "title": "Counter-referral",
        "section": [
            _composition_section(
                "Diagnosis", diagnosis_section, "Condition", condition_id),
            _composition_section(
                "Plan", plan_section, "CarePlan", care_plan_id),
            _composition_section("Follow-up indications", follow_up_indications),
            _composition_section(
                "Follow-up plan for APS", follow_up_plan, "CarePlan", care_plan_id),
        ],
        "extension": [
            extension(
                extension_url("referral-identifier"),
                "valueIdentifier",
                {"system": REFERRAL_ID_SYSTEM, "value": referral_id},
            )
        ],
        "identifier": {
            "system": COUNTER_REFERRAL_ID_SYSTEM,
            "value": counter_referral_id,
        },
        "subject": ref("Patient", patient_id),
        "encounter": ref("Encounter", encounter_id),
        "date": _iso(date),
        "author": [ref("PractitionerRole", specialist_role_id)],
    }


def build_document_reference(
    resource_id,
    composition_id,
    patient_id,
    encounter_id,
    service_request_id,
    specialist_role_id,
    date,
    period_start,
    period_end,
    counter_referral_id="CR-2026-0001",
):
    """DerivacionDocumento: el registro del documento enviado."""
    return {
        "resourceType": "DocumentReference",
        "id": resource_id,
        "meta": meta("DerivacionDocumento"),
        "status": "current",
        "type": codeable(
            [coding(LOINC_SYSTEM, LOINC_CONSULT_NOTE, "Consult note")]
        ),
        "content": [
            {
                "attachment": {
                    "contentType": "application/fhir+json",
                    "url": f"Composition/{composition_id}",
                }
            }
        ],
        "masterIdentifier": {
            "system": COUNTER_REFERRAL_ID_SYSTEM,
            "value": counter_referral_id,
        },
        "subject": ref("Patient", patient_id),
        "author": [ref("PractitionerRole", specialist_role_id)],
        "date": _iso(date),
        "context": {
            "encounter": [ref("Encounter", encounter_id)],
            "related": [ref("ServiceRequest", service_request_id)],
            "period": {
                "start": _iso(period_start),
                "end": _iso(period_end),
            },
        },
    }


def build_document_bundle(
    composition,
    document_reference,
    condition,
    care_plan,
    timestamp,
    resource_id=None,
):
    """Bundle de tipo document (OP-6): la Composition va primera."""
    bundle = {
        "resourceType": "Bundle",
        "type": "document",
        "timestamp": _iso(timestamp),
        "entry": [
            {
                "fullUrl": f"{resource['resourceType']}/{resource['id']}",
                "resource": resource,
            }
            for resource in (
                composition,
                document_reference,
                condition,
                care_plan,
            )
        ],
    }
    if resource_id is not None:
        bundle["id"] = resource_id
    return bundle


# ---------------------------------------------------------------------------
# OP-11: suscripción a los cambios de estado
# ---------------------------------------------------------------------------


def build_subscription(resource_id, referral_id, endpoint, reason=None,
                       status="active"):
    """Subscription base R4 (OP-11, sin perfil propio en la guía).

    `criteria` es exactamente el de operations.md: el Task de la
    derivación, por el identificador de su ServiceRequest. El canal
    es rest-hook con payload FHIR JSON.
    """
    return {
        "resourceType": "Subscription",
        "id": resource_id,
        "status": status,
        "reason": reason or "Cambios de estado de la derivación",
        "criteria": (
            f"Task?focus:ServiceRequest.identifier={referral_id}"
        ),
        "channel": {
            "type": "rest-hook",
            "endpoint": endpoint,
            "payload": "application/fhir+json",
        },
    }
