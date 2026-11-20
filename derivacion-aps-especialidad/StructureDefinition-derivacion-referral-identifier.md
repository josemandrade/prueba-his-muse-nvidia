# Identificador de la derivación - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Identificador de la derivación**

## Extension: Identificador de la derivación 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-referral-identifier | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionReferralIdentifier |

El identificador de la derivación (el mismo de ServiceRequest.identifier) en la Composition de la contrareferencia. Ningún campo base de Composition lleva el id de la derivación; el enlace también viaja en DocumentReference.context.related.

**Context of Use**

**Usage info**

**Usages:**

* Use this Extension: [Contrareferencia](StructureDefinition-derivacion-contrareferencia.md)
* Examples for this Extension: [Bundle/bundle-pi3-ref-2026-0001](Bundle-bundle-pi3-ref-2026-0001.md) and [Composition/contrareferencia-ref-2026-0001](Composition-contrareferencia-ref-2026-0001.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-referral-identifier.json)

### Formal Views of Extension Content

 [Description of Profiles, Differentials, Snapshots, and how the XML and JSON presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-referral-identifier.csv), [Excel](StructureDefinition-derivacion-referral-identifier.xlsx), [Schematron](StructureDefinition-derivacion-referral-identifier.sch) 

#### Constraints



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-referral-identifier",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-referral-identifier",
  "version" : "0.1.0",
  "name" : "DerivacionReferralIdentifier",
  "title" : "Identificador de la derivación",
  "status" : "draft",
  "date" : "2026-11-20T12:46:55+00:00",
  "description" : "El identificador de la derivación (el mismo de ServiceRequest.identifier) en la Composition de la contrareferencia. Ningún campo base de Composition lleva el id de la derivación; el enlace también viaja en DocumentReference.context.related.",
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
    "expression" : "Composition"
  }],
  "type" : "Extension",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/Extension",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "Extension",
      "path" : "Extension",
      "short" : "Identificador de la derivación",
      "definition" : "El identificador de la derivación (el mismo de ServiceRequest.identifier) en la Composition de la contrareferencia. Ningún campo base de Composition lleva el id de la derivación; el enlace también viaja en DocumentReference.context.related."
    },
    {
      "id" : "Extension.extension",
      "path" : "Extension.extension",
      "max" : "0"
    },
    {
      "id" : "Extension.url",
      "path" : "Extension.url",
      "fixedUri" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-referral-identifier"
    },
    {
      "id" : "Extension.value[x]",
      "path" : "Extension.value[x]",
      "min" : 1,
      "type" : [{
        "code" : "Identifier"
      }]
    }]
  }
}

```
