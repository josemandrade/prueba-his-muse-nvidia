// Solicitud de derivación.
// Perfil propio de esta guía, sobre el recurso base ServiceRequest de
// FHIR R4. En R4 no existe ReferralRequest: la derivación es un
// ServiceRequest con intent = order.

Profile: DerivacionSolicitud
Parent: ServiceRequest
Id: derivacion-solicitud
Title: "Solicitud de derivación"
Description: "La derivación que APS crea y el hub enruta: una solicitud de un servicio de especialidad. Perfil propio de esta guía, sobre el recurso base ServiceRequest de FHIR R4. El estado de la derivación NO vive aquí (vive en DerivacionTarea); ServiceRequest.status es solo un espejo grueso."
* identifier 1..*
* identifier ^short = "Identificador de la derivación, creado por APS; persistente hasta que se cierra el ciclo (el identificador persistente de 360X)"
* status 1..1
* intent 1..1
* intent = #order (exactly)
* code 1..1
* code from DerivacionEspecialidad (example)
* code ^short = "El servicio solicitado (catálogo local de especialidades)"
* subject 1..1
* subject only Reference(DerivacionPaciente)
* encounter 0..1
* encounter only Reference(Encounter)
* encounter ^short = "El encuentro de APS que creó la derivación (existe en el EHR de APS)"
* authoredOn 1..1
* requester 1..1
* requester only Reference(DerivacionRol)
* requester ^short = "El médico de APS, en su rol"
* performerType 0..1
* performerType from DerivacionEspecialidad (example)
* performerType ^short = "La especialidad solicitada (catálogo local)"
* performer 0..*
* performer only Reference(DerivacionServicio)
* performer ^short = "El servicio, una vez enrutado"
* reasonCode 1..*
* reasonCode ^short = "Motivo de la derivación: SNOMED CT (p. ej. 84114007 insuficiencia cardiaca) + nota en texto libre"
* priority 1..1
* priority ^short = "routine | urgent (C6/Q6); urgent reduce a la mitad el plazo de aceptación"
* supportingInfo 0..*
* supportingInfo ^short = "Resumen clínico de APS y exámenes relevantes (Observation con LOINC, DocumentReference)"
* note 0..*
