# Base del cruce de identidad - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Base del cruce de identidad**

## Extension: Base del cruce de identidad 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-match-basis | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionMatchBasis |

| | |
| :--- | :--- |
| Cómo se estableció el cruce de identidad en el MPI: identifier | demographics. |

**Context of Use**

**Usage info**

**Usages:**

* This Extension is not used by any profiles in this Specification

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-match-basis.json)

### Formal Views of Extension Content

 [Description of Profiles, Differentials, Snapshots, and how the XML and JSON presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-match-basis.csv), [Excel](StructureDefinition-derivacion-match-basis.xlsx), [Schematron](StructureDefinition-derivacion-match-basis.sch) 

#### Terminology Bindings

#### Constraints



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-match-basis",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-match-basis",
  "version" : "0.1.0",
  "name" : "DerivacionMatchBasis",
  "title" : "Base del cruce de identidad",
  "status" : "draft",
  "date" : "2026-11-20T12:39:48+00:00",
  "description" : "Cómo se estableció el cruce de identidad en el MPI: identifier | demographics.",
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
      "short" : "Base del cruce de identidad",
      "definition" : "Cómo se estableció el cruce de identidad en el MPI: identifier | demographics."
    },
    {
      "id" : "Extension.extension",
      "path" : "Extension.extension",
      "max" : "0"
    },
    {
      "id" : "Extension.url",
      "path" : "Extension.url",
      "fixedUri" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-match-basis"
    },
    {
      "id" : "Extension.value[x]",
      "path" : "Extension.value[x]",
      "min" : 1,
      "type" : [{
        "code" : "code"
      }],
      "binding" : {
        "strength" : "required",
        "valueSet" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/ValueSet/derivacion-base-cruce"
      }
    }]
  }
}

```
