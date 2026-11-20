# Conteo de rechazos de esta oferta - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Conteo de rechazos de esta oferta**

## Extension: Conteo de rechazos de esta oferta 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-offer-decline-count | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionOfferDeclineCount |

Número de veces que el paciente ha rechazado esta oferta (0–2). Se reinicia por oferta (N5).

**Context of Use**

**Usage info**

**Usages:**

* Use this Extension: [Tarea de derivación (registro de estado)](StructureDefinition-derivacion-tarea.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-offer-decline-count.json)

### Formal Views of Extension Content

 [Description of Profiles, Differentials, Snapshots, and how the XML and JSON presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-offer-decline-count.csv), [Excel](StructureDefinition-derivacion-offer-decline-count.xlsx), [Schematron](StructureDefinition-derivacion-offer-decline-count.sch) 

#### Constraints



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-offer-decline-count",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-offer-decline-count",
  "version" : "0.1.0",
  "name" : "DerivacionOfferDeclineCount",
  "title" : "Conteo de rechazos de esta oferta",
  "status" : "draft",
  "date" : "2026-11-20T12:33:32+00:00",
  "description" : "Número de veces que el paciente ha rechazado esta oferta (0–2). Se reinicia por oferta (N5).",
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
      "short" : "Conteo de rechazos de esta oferta",
      "definition" : "Número de veces que el paciente ha rechazado esta oferta (0–2). Se reinicia por oferta (N5)."
    },
    {
      "id" : "Extension.extension",
      "path" : "Extension.extension",
      "max" : "0"
    },
    {
      "id" : "Extension.url",
      "path" : "Extension.url",
      "fixedUri" : "https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-offer-decline-count"
    },
    {
      "id" : "Extension.value[x]",
      "path" : "Extension.value[x]",
      "min" : 1,
      "type" : [{
        "code" : "integer"
      }],
      "constraint" : [{
        "key" : "derivacion-decline-count-range",
        "severity" : "error",
        "human" : "El conteo de rechazos de esta oferta está entre 0 y 2.",
        "expression" : "$this >= 0 and $this <= 2",
        "source" : "https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-offer-decline-count"
      }]
    }]
  }
}

```
