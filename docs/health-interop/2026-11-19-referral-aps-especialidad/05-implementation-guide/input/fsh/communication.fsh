// Notificación (registro de un envío).
// Perfil propio de esta guía, sobre el recurso base Communication de
// FHIR R4. Una notificación es un registro de algo ya enviado, no el
// contenido del mensaje en sí. Los emisores están nombrados (C5/Q3).

Profile: DerivacionNotificacion
Parent: Communication
Id: derivacion-notificacion
Title: "Notificación"
Description: "El registro de una notificación enviada en un cambio de estado de la derivación. Perfil propio de esta guía, sobre el recurso base Communication de FHIR R4. Una notificación enviada por error se corrige con una notificación nueva, nunca borrando el registro."
* identifier 1..*
* identifier ^short = "Creado por el emisor"
* status 1..1
* status = #completed (exactly)
* status ^short = "completed = enviada; el resultado de la entrega es la extensión delivery-outcome"
* category 0..*
* category = http://terminology.hl7.org/CodeSystem/communication-category#notification "Notification"
* subject 1..1
* subject only Reference(DerivacionPaciente)
* basedOn 1..*
* basedOn only Reference(DerivacionTarea)
* basedOn ^short = "La clave de unión: la derivación sobre la que se notifica"
* topic 0..1
* topic ^short = "La transición que disparó el envío (p. ej. 'accepted', en texto codificado); el enlace al Task es basedOn, y el aviso legible es payload.contentString"
* sender 1..1
* sender only Reference(DerivacionRol or Organization)
* sender ^short = "Emisor nombrado (C5/Q3): admin APS / agendador (vía hub) / especialista / hub"
* recipient 1..*
* recipient only Reference(DerivacionPaciente or DerivacionRol)
* recipient ^short = "Paciente / admin APS / médico APS / especialidad"
* sent 1..1
* medium 1..*
* medium from DerivacionCanal (example)
* medium ^short = "Canal (lista local: teléfono / presencial / mensaje del sistema)"
* payload 0..*
* payload.contentString ^short = "El aviso en texto legible (p. ej. 'state changed to accepted')"
* payload.contentReference only Reference(DerivacionDocumento)
* payload.contentReference ^short = "El documento, en el acuse de recibo de la contrareferencia"
* extension contains DerivacionDeliveryOutcome named deliveryOutcome 0..1
* extension[deliveryOutcome] ^short = "delivered | failed. Un envío fallido se reintenta; nunca cambia el estado de la derivación."
