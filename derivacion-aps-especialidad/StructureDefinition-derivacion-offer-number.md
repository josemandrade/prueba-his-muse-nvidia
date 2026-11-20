# Número de oferta (de esta derivación) - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Número de oferta (de esta derivación)**

## Extension: Número de oferta (de esta derivación) 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-offer-number | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionOfferNumber |

Contador por derivación: 1ª oferta, re-oferta (2ª), etc. Cada oferta es un Appointment nuevo.

**Context of Use**

**Usage info**

**Usages:**

* Use this Extension: [Cita de la derivación](StructureDefinition-derivacion-cita.md)
* Examples for this Extension: [Appointment/cita-ref-2026-0001](Appointment-cita-ref-2026-0001.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-offer-number.json)

### Formal Views of Extension Content

 [Description of Profiles, Differentials, Snapshots, and how the XML and JSON presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-offer-number.csv), [Excel](StructureDefinition-derivacion-offer-number.xlsx), [Schematron](StructureDefinition-derivacion-offer-number.sch) 

#### Constraints



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-offer-number",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-offer-number",
  "version" : "0.1.0",
  "name" : "DerivacionOfferNumber",
  "title" : "Número de oferta (de esta derivación)",
  "status" : "draft",
  "date" : "2026-11-20T12:33:32+00:00",
  "description" : "Contador por derivación: 1ª oferta, re-oferta (2ª), etc. Cada oferta es un Appointment nuevo.",
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
    "expression" : "Appointment"
  }],
  "type" : "Extension",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/Extension",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "Extension",
      "path" : "Extension",
      "short" : "Número de oferta (de esta derivación)",
      "definition" : "Contador por derivación: 1ª oferta, re-oferta (2ª), etc. Cada oferta es un Appointment nuevo."
    },
    {
      "id" : "Extension.extension",
      "path" : "Extension.extension",
      "max" : "0"
    },
    {
      "id" : "Extension.url",
      "path" : "Extension.url",
      "fixedUri" : "https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-offer-number"
    },
    {
      "id" : "Extension.value[x]",
      "path" : "Extension.value[x]",
      "min" : 1,
      "type" : [{
        "code" : "integer"
      }]
    }]
  }
}

```
