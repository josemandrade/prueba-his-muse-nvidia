"""Constantes de la guía: canonical, sistemas, códigos y ValueSets.

Fuente: `05-implementation-guide/sushi-config.yaml` (canonical),
`input/fsh/valuesets.fsh` (listas locales) y
`input/fsh/extensions.fsh` (extensiones). Nada aquí se inventa: cada
valor viene de la guía validada.
"""

CANONICAL = "https://josemandrade.github.io/prueba-his-muse-nvidia"

# Perfiles propios de la guía (12), sobre recursos base FHIR R4.
PROFILES = {
    "DerivacionPaciente": "derivacion-paciente",
    "DerivacionRol": "derivacion-rol",
    "DerivacionServicio": "derivacion-servicio",
    "DerivacionSolicitud": "derivacion-solicitud",
    "DerivacionTarea": "derivacion-tarea",
    "DerivacionCita": "derivacion-cita",
    "DerivacionEncuentro": "derivacion-encuentro",
    "DerivacionDiagnostico": "derivacion-diagnostico",
    "DerivacionPlanSeguimiento": "derivacion-plan-seguimiento",
    "DerivacionContrareferencia": "derivacion-contrareferencia",
    "DerivacionDocumento": "derivacion-documento",
    "DerivacionNotificacion": "derivacion-notificacion",
}


def profile_url(name):
    """URL canónica del perfil `Derivacion*`."""
    return f"{CANONICAL}/StructureDefinition/{PROFILES[name]}"


def code_system_url(name):
    """URL canónica de un CodeSystem local (`Derivacion*CS`)."""
    return f"{CANONICAL}/CodeSystem/derivacion-{name}"


def value_set_url(name):
    """URL canónica de un ValueSet local (`Derivacion*`)."""
    return f"{CANONICAL}/ValueSet/derivacion-{name}"


def extension_url(name):
    """URL canónica de una extensión propia de la guía."""
    return f"{CANONICAL}/StructureDefinition/derivacion-{name}"


# Los nueve estados del caso (spec §3.1), en Task.businessStatus.
CASE_STATES = [
    "requested",
    "received",
    "accepted",
    "rejected",
    "scheduled",
    "completed",
    "counter-referred",
    "no-show",
    "cancelled",
]

# Estado grueso R4 (Task.status) que corresponde a cada estado del caso.
CASE_STATE_TO_TASK_STATUS = {
    "requested": "requested",
    "received": "received",
    "accepted": "accepted",
    "rejected": "rejected",
    "scheduled": "ready",
    "completed": "in-progress",
    "counter-referred": "completed",
    "no-show": "failed",
    "cancelled": "cancelled",
}

# Estados terminales del Task (lifecycle.md).
TERMINAL_CASE_STATES = {"counter-referred", "rejected", "no-show", "cancelled"}

# Los seis roles del caso (C1).
ROLES = [
    "aps-doctor",
    "aps-admin",
    "triage-clinician",
    "specialty-scheduler",
    "specialist",
    "hub-operator",
]

# Motivos de rechazo (lista local de la especialidad).
REJECTION_REASONS = ["missing-exam", "wrong-specialty", "capacity"]

# Canales de notificación (lista local).
CHANNELS = ["phone", "in-person", "system-message"]

# Especialidades / servicios (catálogo local).
SPECIALTIES = ["cardiologia"]

# Resultado de la entrega de una notificación.
DELIVERY_OUTCOMES = ["delivered", "failed"]

# Base del cruce de identidad del MPI.
MATCH_BASES = ["identifier", "demographics"]

# Códigos de terminología del ejemplo trabajado.
SNOMED_HEART_FAILURE = "84114007"  # Heart failure (disorder)
SNOMED_SYSTOLIC_HEART_FAILURE = "417996009"  # Systolic heart failure
ICD10CM_SYSTEM = "http://hl7.org/fhir/sid/icd-10-cm"
ICD10CM_CHRONIC_SYSTOLIC_HF = "I50.22"  # Chronic systolic (congestive) heart failure
SNOMED_SYSTEM = "http://snomed.info/sct"
LOINC_SYSTEM = "http://loinc.org"
LOINC_ECG = "11524-6"  # EKG study
LOINC_NT_PROBNP = "33762-6"  # NT-proBNP
LOINC_CONSULT_NOTE = "11488-4"  # Consult note
LOINC_CARDIOLOGY_CONSULT_NOTE = "34099-2"  # Cardiology consult note
LOINC_REFERRAL_NOTE = "57133-1"  # Referral note

# Sistemas de identificadores (sintéticos, de los ejemplos de la guía).
MPI_SYSTEM = "http://mpi.red.example.org"
RUN_SYSTEM = "http://www.registrocivil.cl/run"
REFERRAL_ID_SYSTEM = "http://aps.losaromos.example.org/referral"
APPOINTMENT_ID_SYSTEM = "http://especialidad.example.org/appointment"
ENCOUNTER_ID_SYSTEM = "http://especialidad.example.org/encounter"
COUNTER_REFERRAL_ID_SYSTEM = "http://especialidad.example.org/counter-referral"
NOTIFICATION_ID_SYSTEM = "http://aps.losaromos.example.org/notification"
SERVICE_ID_SYSTEM = "http://especialidad.example.org/service"
ORGANIZATION_APS_SYSTEM = "http://aps.losaromos.example.org/organization"
ORGANIZATION_SPECIALTY_SYSTEM = "http://especialidad.example.org/organization"
ORGANIZATION_HUB_SYSTEM = "http://hub.example.org/organization"

# Plazos SLA en días hábiles (rules.md R1–R5).
SLA_WORKING_DAYS = {
    "acceptance": 5,  # 2 si es urgente
    "acceptance_urgent": 2,
    "offer": 10,
    "confirmation": 3,
    "counterreferral": 5,
    "retriage": 5,
}

# Límites de los conteos del Task (extensiones, con invariantes R4).
MAX_DECLINE_COUNT = 2  # un re-oferta por rechazo: 2 rechazos → re-triaje
MAX_CHASE_COUNT = 2  # dos persecuciones por oferta
MAX_RESCHEDULING_COUNT = 1  # un solo re-agendamiento por derivación

# Emisores nombrados (C5/Q3): disparador → (emisor, destinatario).
# La creación la informa el administrativo de APS a la paciente; la
# aceptación/rechazo igual; la oferta la envía el agendador vía hub
# (y se notifica al administrativo de APS); el resultado de la
# contrareferencia lo informa el administrativo de APS.
NOTIFICATION_SENDERS = {
    "created": ("aps-admin", "patient"),
    "accepted": ("aps-admin", "patient"),
    "rejected": ("aps-admin", "patient"),
    "offer": ("specialty-scheduler", "patient"),
    "offer-notify-aps": ("specialty-scheduler", "aps-admin"),
    "counter-referred": ("aps-admin", "patient"),
    "no-show": ("specialist", "aps-admin"),
    "escalation-offer": ("hub-operator", "specialty-scheduler"),
    "escalation-offer-notify-aps": ("hub-operator", "aps-admin"),
    "escalation-counterreferral": ("hub-operator", "specialist"),
    "escalation-counterreferral-notify-aps": ("hub-operator", "aps-admin"),
    "escalation-acceptance": ("hub-operator", "triage-clinician"),
    "escalation-acceptance-notify-aps": ("hub-operator", "aps-admin"),
    "escalation-retriage": ("hub-operator", "aps-admin"),
    "cancelled": ("hub-operator", "patient"),
    "cancelled-notify-aps": ("hub-operator", "aps-admin"),
    "cancelled-notify-specialty": ("hub-operator", "specialty-scheduler"),
    # Añadido por el componente (Plan task 11.10) desde el diagrama
    # de secuencia 5, fila 4: el acuse de recibo de APS es una
    # Communication (basedOn → Task, contentReference → el documento).
    "counter-referral-receipt": ("aps-admin", "hub"),
    # Añadidos por el componente (Plan task 11.8) desde los diagramas
    # de secuencia del paso 5, que registran Communication en estos
    # eventos aunque la tabla original no los listara: la reserva se
    # notifica a APS (diagrama 3, fila 10) y cada persecución de
    # confirmación queda registrada (diagrama 3, fila 5).
    "booked": ("hub-operator", "aps-admin"),
    "chase": ("specialty-scheduler", "patient"),
}
