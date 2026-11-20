# Plan de seguimiento para APS - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Plan de seguimiento para APS**

## Resource Profile: Plan de seguimiento para APS 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-plan-seguimiento | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionPlanSeguimiento |

 
El plan de seguimiento que el especialista deja a APS. Perfil propio de esta guía, sobre el recurso base CarePlan de FHIR R4. Una actualización del plan es una versión nueva, nunca una sobrescritura silenciosa. 

**Usages:**

* Refer to this Profile: [Contrareferencia](StructureDefinition-derivacion-contrareferencia.md)
* Examples for this Profile: [CarePlan/plan-ref-2026-0001](CarePlan-plan-ref-2026-0001.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-plan-seguimiento.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-plan-seguimiento.csv), [Excel](StructureDefinition-derivacion-plan-seguimiento.xlsx), [Schematron](StructureDefinition-derivacion-plan-seguimiento.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-plan-seguimiento",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-plan-seguimiento",
  "version" : "0.1.0",
  "name" : "DerivacionPlanSeguimiento",
  "title" : "Plan de seguimiento para APS",
  "status" : "draft",
  "date" : "2026-11-20T12:33:32+00:00",
  "description" : "El plan de seguimiento que el especialista deja a APS. Perfil propio de esta guía, sobre el recurso base CarePlan de FHIR R4. Una actualización del plan es una versión nueva, nunca una sobrescritura silenciosa.",
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
  "type" : "CarePlan",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/CarePlan",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "CarePlan",
      "path" : "CarePlan"
    },
    {
      "id" : "CarePlan.replaces",
      "path" : "CarePlan.replaces",
      "short" : "La versión anterior de este plan, en una actualización"
    },
    {
      "id" : "CarePlan.status",
      "path" : "CarePlan.status",
      "fixedCode" : "active"
    },
    {
      "id" : "CarePlan.intent",
      "path" : "CarePlan.intent",
      "fixedCode" : "plan"
    },
    {
      "id" : "CarePlan.subject",
      "path" : "CarePlan.subject",
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-paciente"]
      }]
    },
    {
      "id" : "CarePlan.encounter",
      "path" : "CarePlan.encounter",
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-encuentro"]
      }]
    },
    {
      "id" : "CarePlan.author",
      "path" : "CarePlan.author",
      "short" : "El especialista, en su rol",
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-rol"]
      }]
    },
    {
      "id" : "CarePlan.addresses",
      "path" : "CarePlan.addresses",
      "short" : "El diagnóstico al que responde este plan",
      "min" : 1,
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-diagnostico"]
      }]
    },
    {
      "id" : "CarePlan.activity.reference",
      "path" : "CarePlan.activity.reference",
      "short" : "La solicitud de seguimiento / la cita de control / la tarea (reference O detail, nunca ambos)",
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["http://hl7.org/fhir/StructureDefinition/ServiceRequest",
        "http://hl7.org/fhir/StructureDefinition/Appointment",
        "http://hl7.org/fhir/StructureDefinition/Task"]
      }]
    }]
  }
}

```
