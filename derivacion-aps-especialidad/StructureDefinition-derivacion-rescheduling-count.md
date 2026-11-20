# Conteo de re-agendamientos - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Conteo de re-agendamientos**

## Extension: Conteo de re-agendamientos 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-rescheduling-count | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionReschedulingCount |

Número de re-agendamientos de esta derivación (0–1). No se reinicia: un solo re-agendamiento por derivación.

**Context of Use**

**Usage info**

**Usages:**

* Use this Extension: [Tarea de derivación (registro de estado)](StructureDefinition-derivacion-tarea.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-rescheduling-count.json)

### Formal Views of Extension Content

 [Description of Profiles, Differentials, Snapshots, and how the XML and JSON presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-rescheduling-count.csv), [Excel](StructureDefinition-derivacion-rescheduling-count.xlsx), [Schematron](StructureDefinition-derivacion-rescheduling-count.sch) 

#### Constraints



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-rescheduling-count",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-rescheduling-count",
  "version" : "0.1.0",
  "name" : "DerivacionReschedulingCount",
  "title" : "Conteo de re-agendamientos",
  "status" : "draft",
  "date" : "2026-11-20T12:49:56+00:00",
  "description" : "Número de re-agendamientos de esta derivación (0–1). No se reinicia: un solo re-agendamiento por derivación.",
  "fhirVersion" : "4.0.1",
  "mapping" : [{
    "identity" : "rim",
    "uri" : "http://hl7.org/v3",
    "name" : "RIM Mapping"
  }],
  "kind" : "complex-type",
  "abstract" : false,
  "context" : [{
    "type" : "element",
    "expression" : "Task"
  }],
  "type" : "Extension",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/Extension",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "Extension",
      "path" : "Extension",
      "short" : "Conteo de re-agendamientos",
      "definition" : "Número de re-agendamientos de esta derivación (0–1). No se reinicia: un solo re-agendamiento por derivación."
    },
    {
      "id" : "Extension.extension",
      "path" : "Extension.extension",
      "max" : "0"
    },
    {
      "id" : "Extension.url",
      "path" : "Extension.url",
      "fixedUri" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-rescheduling-count"
    },
    {
      "id" : "Extension.value[x]",
      "path" : "Extension.value[x]",
      "min" : 1,
      "type" : [{
        "code" : "integer"
      }],
      "constraint" : [{
        "key" : "derivacion-rescheduling-count-range",
        "severity" : "error",
        "human" : "El conteo de re-agendamientos está entre 0 y 1: un solo re-agendamiento por derivación.",
        "expression" : "$this >= 0 and $this <= 1",
        "source" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-rescheduling-count"
      }]
    }]
  }
}

```
