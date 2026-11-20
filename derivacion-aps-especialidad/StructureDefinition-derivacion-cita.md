# Cita de la derivación - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Cita de la derivación**

## Resource Profile: Cita de la derivación 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-cita | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionCita |

 
La oferta y la reserva de la cita de especialidad. Perfil propio de esta guía, sobre el recurso base Appointment de FHIR R4. La decisión del paciente vive en el AppointmentResponse, no en la cita; una cita cancelada o no asistida nunca se reutiliza. 

**Usages:**

* Refer to this Profile: [Encuentro de especialidad](StructureDefinition-derivacion-encuentro.md)
* Examples for this Profile: [Appointment/cita-ref-2026-0001](Appointment-cita-ref-2026-0001.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-cita.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-cita.csv), [Excel](StructureDefinition-derivacion-cita.xlsx), [Schematron](StructureDefinition-derivacion-cita.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-cita",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-cita",
  "version" : "0.1.0",
  "name" : "DerivacionCita",
  "title" : "Cita de la derivación",
  "status" : "draft",
  "date" : "2026-11-20T12:39:48+00:00",
  "description" : "La oferta y la reserva de la cita de especialidad. Perfil propio de esta guía, sobre el recurso base Appointment de FHIR R4. La decisión del paciente vive en el AppointmentResponse, no en la cita; una cita cancelada o no asistida nunca se reutiliza.",
  "fhirVersion" : "4.0.1",
  "mapping" : [{
    "identity" : "workflow",
    "uri" : "http://hl7.org/fhir/workflow",
    "name" : "Workflow Pattern"
  },
  {
    "identity" : "rim",
    "uri" : "http://hl7.org/v3",
    "name" : "RIM Mapping"
  },
  {
    "identity" : "ical",
    "uri" : "http://ietf.org/rfc/2445",
    "name" : "iCalendar"
  },
  {
    "identity" : "w5",
    "uri" : "http://hl7.org/fhir/fivews",
    "name" : "FiveWs Pattern Mapping"
  },
  {
    "identity" : "v2",
    "uri" : "http://hl7.org/v2",
    "name" : "HL7 v2 Mapping"
  }],
  "kind" : "resource",
  "abstract" : false,
  "type" : "Appointment",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/Appointment",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "Appointment",
      "path" : "Appointment"
    },
    {
      "id" : "Appointment.extension",
      "path" : "Appointment.extension",
      "slicing" : {
        "discriminator" : [{
          "type" : "value",
          "path" : "url"
        }],
        "ordered" : false,
        "rules" : "open"
      }
    },
    {
      "id" : "Appointment.extension:offerNumber",
      "path" : "Appointment.extension",
      "sliceName" : "offerNumber",
      "short" : "Contador por derivación: 1ª oferta, re-oferta (2ª), etc.",
      "min" : 0,
      "max" : "1",
      "type" : [{
        "code" : "Extension",
        "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-offer-number"]
      }]
    },
    {
      "id" : "Appointment.identifier",
      "path" : "Appointment.identifier",
      "short" : "Creado por la especialidad. Una re-oferta es un Appointment NUEVO (nuevo identificador).",
      "min" : 1
    },
    {
      "id" : "Appointment.status",
      "path" : "Appointment.status",
      "short" : "proposed → pending → booked → arrived → fulfilled; cancelled / noshow son terminales"
    },
    {
      "id" : "Appointment.serviceType",
      "path" : "Appointment.serviceType",
      "binding" : {
        "strength" : "example",
        "valueSet" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/ValueSet/derivacion-especialidad"
      }
    },
    {
      "id" : "Appointment.created",
      "path" : "Appointment.created",
      "short" : "Fecha de la oferta"
    },
    {
      "id" : "Appointment.basedOn",
      "path" : "Appointment.basedOn",
      "short" : "La clave de unión: la derivación a la que pertenece esta cita",
      "min" : 1,
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-solicitud"]
      }]
    },
    {
      "id" : "Appointment.participant",
      "path" : "Appointment.participant",
      "short" : "Paciente + especialista + lugar"
    }]
  }
}

```
