// Registro de estado del flujo de trabajo de la derivación — el CENTRO.
// Perfil propio de esta guía, sobre el recurso base Task de FHIR R4.
// Una derivación es una solicitud (ServiceRequest) más este registro;
// el estado vive aquí, no en el estado de la solicitud.

Profile: DerivacionTarea
Parent: Task
Id: derivacion-tarea
Title: "Tarea de derivación (registro de estado)"
Description: "El registro de estado del flujo de trabajo de una derivación: lleva el estado del caso, los relojes SLA y los conteos de los ciclos. Es el centro del grafo de recursos y lo primero que lee cada paso posterior. Perfil propio de esta guía, sobre el recurso base Task de FHIR R4."
* identifier 1..*
* identifier ^short = "El mismo valor que ServiceRequest.identifier: la clave de unión entre solicitud y registro"
* status 1..1
* status ^short = "El valor grueso de R4; el estado del caso vive en businessStatus"
* businessStatus 1..1
* businessStatus from DerivacionEstadoReferencia (example)
* businessStatus ^short = "El estado del caso, textual (los nueve estados de DerivacionEstadoReferencia)"
* intent 1..1
* intent = #order (exactly)
* code 0..1
* code from DerivacionTaskCode (example)
* code ^short = "referral-workflow: este Task es siempre un registro de flujo de trabajo de derivación"
* focus 1..1
* focus only Reference(DerivacionSolicitud)
* focus ^short = "La solicitud sobre la que trabaja este Task"
* for 1..1
* for only Reference(DerivacionPaciente)
* requester 0..1
* requester only Reference(DerivacionRol)
* owner 0..1
* owner only Reference(DerivacionServicio)
* owner ^short = "El servicio que acepta (es el responsable del trabajo); el profesional que acepta se registra como agente de Provenance en la entrada de aceptación del historial"
* description 0..1
* description ^short = "El próximo paso esperado (p. ej. 'acceptance decision', 'appointment offer')"
* statusReason 0..1
* statusReason from DerivacionMotivoRechazo (example)
* statusReason ^short = "Motivo de rechazo o de cancelación (incl. 'patient deceased')"
* relevantHistory 0..*
* relevantHistory only Reference(Provenance)
* relevantHistory ^short = "Historial de estados (solo añadir; nunca se edita un estado)"
* lastModified 0..1
* note 0..*
* extension contains
    DerivacionSlaAcceptanceDeadline named slaAcceptanceDeadline 0..1 and
    DerivacionSlaOfferDeadline named slaOfferDeadline 0..1 and
    DerivacionSlaCounterreferralDeadline named slaCounterreferralDeadline 0..1 and
    DerivacionSlaRetriageDeadline named slaRetriageDeadline 0..1 and
    DerivacionSlaConfirmationDeadline named slaConfirmationDeadline 0..1 and
    DerivacionOfferDeclineCount named offerDeclineCount 0..1 and
    DerivacionOfferChaseCount named offerChaseCount 0..1 and
    DerivacionReschedulingCount named reschedulingCount 0..1
