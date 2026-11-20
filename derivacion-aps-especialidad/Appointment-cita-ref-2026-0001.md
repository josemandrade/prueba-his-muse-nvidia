# Cita de la derivación REF-2026-0001 (proposed) - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Cita de la derivación REF-2026-0001 (proposed)**

## Example Appointment: Cita de la derivación REF-2026-0001 (proposed)

Profile: [Cita de la derivación](StructureDefinition-derivacion-cita.md)

**Número de oferta (de esta derivación)**: 1

**identifier**: `http://especialidad.example.org/appointment`/CITA-2026-0001

**status**: Proposed

**serviceType**: Cardiology

**start**: 2026-12-02 10:00:00-0300

**end**: 2026-12-02 10:30:00-0300

**slot**: [Slot: status = busy; start = 2026-12-02 10:00:00-0300; end = 2026-12-02 10:30:00-0300](Slot-slot-cardiologia-1.md)

**created**: 2026-11-24 11:00:00-0300

**patientInstruction**: Ayuno no necesario. Traer los exámenes previos.

**basedOn**: [ServiceRequest Cardiology](ServiceRequest-ref-2026-0001.md)

> **participant****actor**: [María González (official) Female, DoB: 1968-04-15 ( http://www.registrocivil.cl/run#11111111-1)](Patient-maria-gonzalez.md)**status**: Needs Action

> **participant****actor**: [Carlos Rojas (official) (http://www.registrocivil.cl/run#33333333-3): Specialist at Servicio de Cardiología (http://especialidad.example.org/organization#CARDIOLOGIA)](PractitionerRole-rol-especialista.md)**status**: Accepted

> **participant****actor**: [Consulta de Cardiología](Location-location-cardiologia.md)**status**: Accepted



## Resource Content

```json
{
  "resourceType" : "Appointment",
  "id" : "cita-ref-2026-0001",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-cita"]
  },
  "extension" : [{
    "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-offer-number",
    "valueInteger" : 1
  }],
  "identifier" : [{
    "system" : "http://especialidad.example.org/appointment",
    "value" : "CITA-2026-0001"
  }],
  "status" : "proposed",
  "serviceType" : [{
    "coding" : [{
      "system" : "https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-especialidad",
      "code" : "cardiologia",
      "display" : "Cardiology"
    }]
  }],
  "start" : "2026-12-02T10:00:00-03:00",
  "end" : "2026-12-02T10:30:00-03:00",
  "slot" : [{
    "reference" : "Slot/slot-cardiologia-1"
  }],
  "created" : "2026-11-24T11:00:00-03:00",
  "patientInstruction" : "Ayuno no necesario. Traer los exámenes previos.",
  "basedOn" : [{
    "reference" : "ServiceRequest/ref-2026-0001"
  }],
  "participant" : [{
    "actor" : {
      "reference" : "Patient/maria-gonzalez"
    },
    "status" : "needs-action"
  },
  {
    "actor" : {
      "reference" : "PractitionerRole/rol-especialista"
    },
    "status" : "accepted"
  },
  {
    "actor" : {
      "reference" : "Location/location-cardiologia"
    },
    "status" : "accepted"
  }]
}

```
