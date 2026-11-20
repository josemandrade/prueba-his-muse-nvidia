// Plan de seguimiento para APS.
// Perfil propio de esta guía, sobre el recurso base CarePlan de FHIR
// R4. Es la parte de la contrareferencia sobre la que actúa APS:
// controles, exámenes, o una nueva derivación si hace falta otra
// especialidad.

Profile: DerivacionPlanSeguimiento
Parent: CarePlan
Id: derivacion-plan-seguimiento
Title: "Plan de seguimiento para APS"
Description: "El plan de seguimiento que el especialista deja a APS. Perfil propio de esta guía, sobre el recurso base CarePlan de FHIR R4. Una actualización del plan es una versión nueva, nunca una sobrescritura silenciosa."
* status 1..1
* status = #active (exactly)
* intent 1..1
* intent = #plan (exactly)
* subject 1..1
* subject only Reference(DerivacionPaciente)
* encounter 0..1
* encounter only Reference(DerivacionEncuentro)
* author 0..1
* author only Reference(DerivacionRol)
* author ^short = "El especialista, en su rol"
* addresses 1..*
* addresses only Reference(DerivacionDiagnostico)
* addresses ^short = "El diagnóstico al que responde este plan"
* activity 0..*
* activity.reference only Reference(ServiceRequest or Appointment or Task)
* activity.reference ^short = "La solicitud de seguimiento / la cita de control / la tarea (reference O detail, nunca ambos)"
* replaces 0..*
* replaces ^short = "La versión anterior de este plan, en una actualización"
* basedOn 0..*
