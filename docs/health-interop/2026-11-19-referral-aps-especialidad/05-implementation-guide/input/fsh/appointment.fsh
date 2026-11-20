// Cita (oferta / reserva).
// Perfil propio de esta guía, sobre el recurso base Appointment de FHIR
// R4. La cadena de estados es: proposed (oferta) → pending (paciente
// confirmó, aún no reservada) → booked (slot ocupado) → arrived →
// fulfilled. Una re-oferta es un Appointment NUEVO, nunca el mismo.

Profile: DerivacionCita
Parent: Appointment
Id: derivacion-cita
Title: "Cita de la derivación"
Description: "La oferta y la reserva de la cita de especialidad. Perfil propio de esta guía, sobre el recurso base Appointment de FHIR R4. La decisión del paciente vive en el AppointmentResponse, no en la cita; una cita cancelada o no asistida nunca se reutiliza."
* identifier 1..*
* identifier ^short = "Creado por la especialidad. Una re-oferta es un Appointment NUEVO (nuevo identificador)."
* status 1..1
* status ^short = "proposed → pending → booked → arrived → fulfilled; cancelled / noshow son terminales"
* basedOn 1..*
* basedOn only Reference(DerivacionSolicitud)
* basedOn ^short = "La clave de unión: la derivación a la que pertenece esta cita"
* slot 0..*
* slot only Reference(Slot)
* created 0..1
* created ^short = "Fecha de la oferta"
* start 0..1
* end 0..1
* participant 1..*
* participant ^short = "Paciente + especialista + lugar"
* serviceType 0..*
* serviceType from DerivacionEspecialidad (example)
* patientInstruction 0..1
* appointmentType 0..1
* extension contains DerivacionOfferNumber named offerNumber 0..1
* extension[offerNumber] ^short = "Contador por derivación: 1ª oferta, re-oferta (2ª), etc."
