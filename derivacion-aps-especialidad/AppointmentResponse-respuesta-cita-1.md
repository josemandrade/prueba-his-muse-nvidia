# Respuesta de la paciente a la oferta (accepted) - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Respuesta de la paciente a la oferta (accepted)**

## Example AppointmentResponse: Respuesta de la paciente a la oferta (accepted)

**appointment**: [Appointment: extension = 1; identifier = http://especialidad.example.org/appointment#CITA-2026-0001; status = proposed; serviceType = Cardiology; start = 2026-12-02 10:00:00-0300; end = 2026-12-02 10:30:00-0300; created = 2026-11-24 11:00:00-0300; patientInstruction = Ayuno no necesario. Traer los exámenes previos.](Appointment-cita-ref-2026-0001.md)

**actor**: [María González (official) Female, DoB: 1968-04-15 ( http://www.registrocivil.cl/run#11111111-1)](Patient-maria-gonzalez.md)

**participantStatus**: Accepted



## Resource Content

```json
{
  "resourceType" : "AppointmentResponse",
  "id" : "respuesta-cita-1",
  "appointment" : {
    "reference" : "Appointment/cita-ref-2026-0001"
  },
  "actor" : {
    "reference" : "Patient/maria-gonzalez"
  },
  "participantStatus" : "accepted"
}

```
