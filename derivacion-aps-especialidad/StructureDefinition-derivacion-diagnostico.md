# Diagnóstico de la contrareferencia - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Diagnóstico de la contrareferencia**

## Resource Profile: Diagnóstico de la contrareferencia 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-diagnostico | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionDiagnostico |

 
El diagnóstico que el especialista devuelve a APS. Perfil propio de esta guía, sobre el recurso base Condition de FHIR R4. 

**Usages:**

* Refer to this Profile: [Contrareferencia](StructureDefinition-derivacion-contrareferencia.md) and [Plan de seguimiento para APS](StructureDefinition-derivacion-plan-seguimiento.md)
* Examples for this Profile: [Condition/diagnostico-ref-2026-0001](Condition-diagnostico-ref-2026-0001.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-diagnostico.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-diagnostico.csv), [Excel](StructureDefinition-derivacion-diagnostico.xlsx), [Schematron](StructureDefinition-derivacion-diagnostico.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-diagnostico",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-diagnostico",
  "version" : "0.1.0",
  "name" : "DerivacionDiagnostico",
  "title" : "Diagnóstico de la contrareferencia",
  "status" : "draft",
  "date" : "2026-11-20T12:46:55+00:00",
  "description" : "El diagnóstico que el especialista devuelve a APS. Perfil propio de esta guía, sobre el recurso base Condition de FHIR R4.",
  "fhirVersion" : "4.0.1",
  "mapping" : [{
    "identity" : "workflow",
    "uri" : "http://hl7.org/fhir/workflow",
    "name" : "Workflow Pattern"
  },
  {
    "identity" : "sct-concept",
    "uri" : "http://snomed.info/conceptdomain",
    "name" : "SNOMED CT Concept Domain Binding"
  },
  {
    "identity" : "v2",
    "uri" : "http://hl7.org/v2",
    "name" : "HL7 v2 Mapping"
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
    "identity" : "sct-attr",
    "uri" : "http://snomed.org/attributebinding",
    "name" : "SNOMED CT Attribute Binding"
  }],
  "kind" : "resource",
  "abstract" : false,
  "type" : "Condition",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/Condition",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "Condition",
      "path" : "Condition"
    },
    {
      "id" : "Condition.clinicalStatus",
      "path" : "Condition.clinicalStatus",
      "min" : 1,
      "fixedCodeableConcept" : {
        "coding" : [{
          "system" : "http://terminology.hl7.org/CodeSystem/condition-clinical",
          "code" : "active"
        }]
      }
    },
    {
      "id" : "Condition.verificationStatus",
      "path" : "Condition.verificationStatus",
      "min" : 1,
      "fixedCodeableConcept" : {
        "coding" : [{
          "system" : "http://terminology.hl7.org/CodeSystem/condition-ver-status",
          "code" : "confirmed"
        }]
      }
    },
    {
      "id" : "Condition.code",
      "path" : "Condition.code",
      "short" : "ICD-10-CM (primario) + SNOMED CT (segunda codificación). Ejemplo trabajado: I50.22 insuficiencia cardiaca sistólica crónica + 417996009.",
      "min" : 1
    },
    {
      "id" : "Condition.code.coding",
      "path" : "Condition.code.coding",
      "slicing" : {
        "discriminator" : [{
          "type" : "value",
          "path" : "system"
        }],
        "rules" : "open"
      },
      "min" : 2
    },
    {
      "id" : "Condition.code.coding:icd10cm",
      "path" : "Condition.code.coding",
      "sliceName" : "icd10cm",
      "min" : 1,
      "max" : "1"
    },
    {
      "id" : "Condition.code.coding:icd10cm.system",
      "path" : "Condition.code.coding.system",
      "min" : 1,
      "patternUri" : "http://hl7.org/fhir/sid/icd-10-cm"
    },
    {
      "id" : "Condition.code.coding:snomed",
      "path" : "Condition.code.coding",
      "sliceName" : "snomed",
      "min" : 1,
      "max" : "1"
    },
    {
      "id" : "Condition.code.coding:snomed.system",
      "path" : "Condition.code.coding.system",
      "min" : 1,
      "patternUri" : "http://snomed.info/sct"
    },
    {
      "id" : "Condition.subject",
      "path" : "Condition.subject",
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-paciente"]
      }]
    },
    {
      "id" : "Condition.encounter",
      "path" : "Condition.encounter",
      "min" : 1,
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-encuentro"]
      }]
    }]
  }
}

```
