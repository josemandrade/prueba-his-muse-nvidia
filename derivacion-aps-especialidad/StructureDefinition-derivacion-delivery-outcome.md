# Resultado de la entrega - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Resultado de la entrega**

## Extension: Resultado de la entrega 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-delivery-outcome | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionDeliveryOutcome |

| | |
| :--- | :--- |
| Resultado de la entrega de una notificación: delivered | failed. Communication.status = completed significa enviada; el resultado de la entrega es esta extensión. |

**Context of Use**

**Usage info**

**Usages:**

* Use this Extension: [Notificación](StructureDefinition-derivacion-notificacion.md)
* Examples for this Extension: [Communication/notificacion-aceptacion-ref-2026-0001](Communication-notificacion-aceptacion-ref-2026-0001.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-delivery-outcome.json)

### Formal Views of Extension Content

 [Description of Profiles, Differentials, Snapshots, and how the XML and JSON presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-delivery-outcome.csv), [Excel](StructureDefinition-derivacion-delivery-outcome.xlsx), [Schematron](StructureDefinition-derivacion-delivery-outcome.sch) 

#### Terminology Bindings

#### Constraints



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-delivery-outcome",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-delivery-outcome",
  "version" : "0.1.0",
  "name" : "DerivacionDeliveryOutcome",
  "title" : "Resultado de la entrega",
  "status" : "draft",
  "date" : "2026-11-20T12:49:56+00:00",
  "description" : "Resultado de la entrega de una notificación: delivered | failed. Communication.status = completed significa enviada; el resultado de la entrega es esta extensión.",
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
    "expression" : "Communication"
  }],
  "type" : "Extension",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/Extension",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "Extension",
      "path" : "Extension",
      "short" : "Resultado de la entrega",
      "definition" : "Resultado de la entrega de una notificación: delivered | failed. Communication.status = completed significa enviada; el resultado de la entrega es esta extensión."
    },
    {
      "id" : "Extension.extension",
      "path" : "Extension.extension",
      "max" : "0"
    },
    {
      "id" : "Extension.url",
      "path" : "Extension.url",
      "fixedUri" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-delivery-outcome"
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
        "valueSet" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/ValueSet/derivacion-resultado-entrega"
      }
    }]
  }
}

```
