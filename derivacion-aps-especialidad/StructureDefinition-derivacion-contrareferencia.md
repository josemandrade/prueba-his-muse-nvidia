# Contrareferencia - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Contrareferencia**

## Resource Profile: Contrareferencia 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-contrareferencia | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionContrareferencia |

 
El documento clínico de vuelta del especialista a APS: diagnóstico, plan, indicaciones de seguimiento y plan de seguimiento para APS. Perfil propio de esta guía, sobre el recurso base Composition de FHIR R4. 

**Usages:**

* Examples for this Profile: [Composition/contrareferencia-ref-2026-0001](Composition-contrareferencia-ref-2026-0001.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-contrareferencia.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-contrareferencia.csv), [Excel](StructureDefinition-derivacion-contrareferencia.xlsx), [Schematron](StructureDefinition-derivacion-contrareferencia.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-contrareferencia",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-contrareferencia",
  "version" : "0.1.0",
  "name" : "DerivacionContrareferencia",
  "title" : "Contrareferencia",
  "status" : "draft",
  "date" : "2026-11-20T12:49:56+00:00",
  "description" : "El documento clínico de vuelta del especialista a APS: diagnóstico, plan, indicaciones de seguimiento y plan de seguimiento para APS. Perfil propio de esta guía, sobre el recurso base Composition de FHIR R4.",
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
    "identity" : "cda",
    "uri" : "http://hl7.org/v3/cda",
    "name" : "CDA (R2)"
  },
  {
    "identity" : "fhirdocumentreference",
    "uri" : "http://hl7.org/fhir/documentreference",
    "name" : "FHIR DocumentReference"
  },
  {
    "identity" : "w5",
    "uri" : "http://hl7.org/fhir/fivews",
    "name" : "FiveWs Pattern Mapping"
  }],
  "kind" : "resource",
  "abstract" : false,
  "type" : "Composition",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/Composition",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "Composition",
      "path" : "Composition"
    },
    {
      "id" : "Composition.extension",
      "path" : "Composition.extension",
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
      "id" : "Composition.extension:referralIdentifier",
      "path" : "Composition.extension",
      "sliceName" : "referralIdentifier",
      "short" : "El identificador de la derivación (el mismo de ServiceRequest.identifier)",
      "min" : 0,
      "max" : "1",
      "type" : [{
        "code" : "Extension",
        "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-referral-identifier"]
      }]
    },
    {
      "id" : "Composition.identifier",
      "path" : "Composition.identifier",
      "short" : "Identificador de la contrareferencia, creado por la especialidad"
    },
    {
      "id" : "Composition.status",
      "path" : "Composition.status",
      "short" : "final: el perfil es el documento enviado; un borrador es una Composition sin este perfil",
      "fixedCode" : "final"
    },
    {
      "id" : "Composition.type",
      "path" : "Composition.type",
      "short" : "LOINC 11488-4 'Consult note' (variante de cardiología: 34099-2 en el ejemplo trabajado)",
      "patternCodeableConcept" : {
        "coding" : [{
          "system" : "http://loinc.org",
          "code" : "11488-4",
          "display" : "Consult note"
        }]
      }
    },
    {
      "id" : "Composition.subject",
      "path" : "Composition.subject",
      "min" : 1,
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-paciente"]
      }]
    },
    {
      "id" : "Composition.encounter",
      "path" : "Composition.encounter",
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-encuentro"]
      }]
    },
    {
      "id" : "Composition.date",
      "path" : "Composition.date",
      "short" : "Fecha de envío"
    },
    {
      "id" : "Composition.author",
      "path" : "Composition.author",
      "short" : "El especialista, en su rol",
      "max" : "1",
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-rol"]
      }]
    },
    {
      "id" : "Composition.title",
      "path" : "Composition.title",
      "patternString" : "Counter-referral"
    },
    {
      "id" : "Composition.section",
      "path" : "Composition.section",
      "slicing" : {
        "discriminator" : [{
          "type" : "value",
          "path" : "title"
        }],
        "rules" : "open"
      },
      "min" : 4
    },
    {
      "id" : "Composition.section:diagnosis",
      "path" : "Composition.section",
      "sliceName" : "diagnosis",
      "min" : 1,
      "max" : "1"
    },
    {
      "id" : "Composition.section:diagnosis.title",
      "path" : "Composition.section.title",
      "min" : 1,
      "patternString" : "Diagnosis"
    },
    {
      "id" : "Composition.section:diagnosis.code",
      "path" : "Composition.section.code",
      "min" : 1
    },
    {
      "id" : "Composition.section:diagnosis.entry",
      "path" : "Composition.section.entry",
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-diagnostico"]
      }]
    },
    {
      "id" : "Composition.section:plan",
      "path" : "Composition.section",
      "sliceName" : "plan",
      "min" : 1,
      "max" : "1"
    },
    {
      "id" : "Composition.section:plan.title",
      "path" : "Composition.section.title",
      "min" : 1,
      "patternString" : "Plan"
    },
    {
      "id" : "Composition.section:plan.code",
      "path" : "Composition.section.code",
      "min" : 1
    },
    {
      "id" : "Composition.section:plan.entry",
      "path" : "Composition.section.entry",
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-plan-seguimiento"]
      }]
    },
    {
      "id" : "Composition.section:followUpIndications",
      "path" : "Composition.section",
      "sliceName" : "followUpIndications",
      "min" : 1,
      "max" : "1"
    },
    {
      "id" : "Composition.section:followUpIndications.title",
      "path" : "Composition.section.title",
      "min" : 1,
      "patternString" : "Follow-up indications"
    },
    {
      "id" : "Composition.section:followUpIndications.code",
      "path" : "Composition.section.code",
      "min" : 1
    },
    {
      "id" : "Composition.section:followUpPlan",
      "path" : "Composition.section",
      "sliceName" : "followUpPlan",
      "min" : 1,
      "max" : "1"
    },
    {
      "id" : "Composition.section:followUpPlan.title",
      "path" : "Composition.section.title",
      "min" : 1,
      "patternString" : "Follow-up plan for APS"
    },
    {
      "id" : "Composition.section:followUpPlan.code",
      "path" : "Composition.section.code",
      "min" : 1
    },
    {
      "id" : "Composition.section:followUpPlan.entry",
      "path" : "Composition.section.entry",
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-plan-seguimiento"]
      }]
    }]
  }
}

```
