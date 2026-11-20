# Encuentro de especialidad - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Encuentro de especialidad**

## Resource Profile: Encuentro de especialidad 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-encuentro | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionEncuentro |

 
La visita atendida en la especialidad. Perfil propio de esta guía, sobre el recurso base Encounter de FHIR R4. La cita es la reserva; la visita es el encuentro — nunca ambas a la vez sin regla, y la regla aquí es: reserva = Appointment, visita = Encounter. 

**Usages:**

* Refer to this Profile: [Contrareferencia](StructureDefinition-derivacion-contrareferencia.md), [Diagnóstico de la contrareferencia](StructureDefinition-derivacion-diagnostico.md), [Documento de contrareferencia](StructureDefinition-derivacion-documento.md) and [Plan de seguimiento para APS](StructureDefinition-derivacion-plan-seguimiento.md)
* Examples for this Profile: [Encounter/encuentro-ref-2026-0001](Encounter-encuentro-ref-2026-0001.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-encuentro.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-encuentro.csv), [Excel](StructureDefinition-derivacion-encuentro.xlsx), [Schematron](StructureDefinition-derivacion-encuentro.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-encuentro",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-encuentro",
  "version" : "0.1.0",
  "name" : "DerivacionEncuentro",
  "title" : "Encuentro de especialidad",
  "status" : "draft",
  "date" : "2026-11-20T12:49:56+00:00",
  "description" : "La visita atendida en la especialidad. Perfil propio de esta guía, sobre el recurso base Encounter de FHIR R4. La cita es la reserva; la visita es el encuentro — nunca ambas a la vez sin regla, y la regla aquí es: reserva = Appointment, visita = Encounter.",
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
  "type" : "Encounter",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/Encounter",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "Encounter",
      "path" : "Encounter"
    },
    {
      "id" : "Encounter.identifier",
      "path" : "Encounter.identifier",
      "short" : "Creado por la especialidad",
      "min" : 1
    },
    {
      "id" : "Encounter.status",
      "path" : "Encounter.status",
      "short" : "planned → in-progress → finished (R4 no tiene 'scheduled'; el valor es 'planned')"
    },
    {
      "id" : "Encounter.class",
      "path" : "Encounter.class",
      "short" : "AMB (ambulatorio): consulta de especialidad ambulatoria",
      "fixedCoding" : {
        "system" : "http://terminology.hl7.org/CodeSystem/v3-ActCode",
        "code" : "AMB"
      }
    },
    {
      "id" : "Encounter.serviceType",
      "path" : "Encounter.serviceType",
      "short" : "El servicio de especialidad (catálogo local)",
      "min" : 1,
      "binding" : {
        "strength" : "example",
        "valueSet" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/ValueSet/derivacion-especialidad"
      }
    },
    {
      "id" : "Encounter.subject",
      "path" : "Encounter.subject",
      "min" : 1,
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-paciente"]
      }]
    },
    {
      "id" : "Encounter.basedOn",
      "path" : "Encounter.basedOn",
      "short" : "La derivación a la que pertenece esta visita",
      "min" : 1,
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-solicitud"]
      }]
    },
    {
      "id" : "Encounter.participant.individual",
      "path" : "Encounter.participant.individual",
      "short" : "El especialista que atendió, en su rol",
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-rol"]
      }]
    },
    {
      "id" : "Encounter.appointment",
      "path" : "Encounter.appointment",
      "short" : "La reserva de la que nace esta visita",
      "max" : "1",
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-cita"]
      }]
    },
    {
      "id" : "Encounter.period",
      "path" : "Encounter.period",
      "short" : "Periodo real de la visita"
    }]
  }
}

```
