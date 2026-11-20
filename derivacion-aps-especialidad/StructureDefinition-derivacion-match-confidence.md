# Confianza del cruce de identidad - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Confianza del cruce de identidad**

## Extension: Confianza del cruce de identidad 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-match-confidence | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionMatchConfidence |

Confianza del cruce de identidad del MPI, de 0 a 1. Opcional.

**Context of Use**

**Usage info**

**Usages:**

* This Extension is not used by any profiles in this Specification

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-match-confidence.json)

### Formal Views of Extension Content

 [Description of Profiles, Differentials, Snapshots, and how the XML and JSON presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-match-confidence.csv), [Excel](StructureDefinition-derivacion-match-confidence.xlsx), [Schematron](StructureDefinition-derivacion-match-confidence.sch) 

#### Constraints



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-match-confidence",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-match-confidence",
  "version" : "0.1.0",
  "name" : "DerivacionMatchConfidence",
  "title" : "Confianza del cruce de identidad",
  "status" : "draft",
  "date" : "2026-11-20T12:39:48+00:00",
  "description" : "Confianza del cruce de identidad del MPI, de 0 a 1. Opcional.",
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
    "expression" : "Patient"
  }],
  "type" : "Extension",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/Extension",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "Extension",
      "path" : "Extension",
      "short" : "Confianza del cruce de identidad",
      "definition" : "Confianza del cruce de identidad del MPI, de 0 a 1. Opcional."
    },
    {
      "id" : "Extension.extension",
      "path" : "Extension.extension",
      "max" : "0"
    },
    {
      "id" : "Extension.url",
      "path" : "Extension.url",
      "fixedUri" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-match-confidence"
    },
    {
      "id" : "Extension.value[x]",
      "path" : "Extension.value[x]",
      "min" : 1,
      "type" : [{
        "code" : "decimal"
      }],
      "constraint" : [{
        "key" : "derivacion-match-confidence-range",
        "severity" : "error",
        "human" : "La confianza del cruce de identidad está entre 0 y 1.",
        "expression" : "$this >= 0 and $this <= 1",
        "source" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-match-confidence"
      }]
    }]
  }
}

```
