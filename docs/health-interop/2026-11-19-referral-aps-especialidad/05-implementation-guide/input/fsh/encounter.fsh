// Encuentro de especialidad (la visita).
// Perfil propio de esta guía, sobre el recurso base Encounter de FHIR
// R4. El encuentro existe desde la reserva (planned); no se crea en la
// asistencia. En un no-show NO hay encuentro: el no-show vive solo en
// la cita.

Profile: DerivacionEncuentro
Parent: Encounter
Id: derivacion-encuentro
Title: "Encuentro de especialidad"
Description: "La visita atendida en la especialidad. Perfil propio de esta guía, sobre el recurso base Encounter de FHIR R4. La cita es la reserva; la visita es el encuentro — nunca ambas a la vez sin regla, y la regla aquí es: reserva = Appointment, visita = Encounter."
* identifier 1..*
* identifier ^short = "Creado por la especialidad"
* status 1..1
* status ^short = "planned → in-progress → finished (R4 no tiene 'scheduled'; el valor es 'planned')"
* class 1..1
* class = http://terminology.hl7.org/CodeSystem/v3-ActCode#AMB (exactly)
* class ^short = "AMB (ambulatorio): consulta de especialidad ambulatoria"
* subject 1..1
* subject only Reference(DerivacionPaciente)
* basedOn 1..*
* basedOn only Reference(DerivacionSolicitud)
* basedOn ^short = "La derivación a la que pertenece esta visita"
* appointment 0..1
* appointment only Reference(DerivacionCita)
* appointment ^short = "La reserva de la que nace esta visita"
* period 0..1
* period ^short = "Periodo real de la visita"
* participant 0..*
* participant.individual only Reference(DerivacionRol)
* participant.individual ^short = "El especialista que atendió, en su rol"
* serviceType 1..1
* serviceType from DerivacionEspecialidad (example)
* serviceType ^short = "El servicio de especialidad (catálogo local)"
