# Plazo de confirmación - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Plazo de confirmación**

## Extension: Plazo de confirmación 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-sla-confirmation-deadline | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionSlaConfirmationDeadline |

Fecha límite para confirmar una oferta: oferta + 3 días hábiles. Presente solo mientras una oferta está abierta.

**Context of Use**

**Usage info**

**Usages:**

* Use this Extension: [Tarea de derivación (registro de estado)](StructureDefinition-derivacion-tarea.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-sla-confirmation-deadline.json)

### Formal Views of Extension Content

 [Description of Profiles, Differentials, Snapshots, and how the XML and JSON presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-sla-confirmation-deadline.csv), [Excel](StructureDefinition-derivacion-sla-confirmation-deadline.xlsx), [Schematron](StructureDefinition-derivacion-sla-confirmation-deadline.sch) 

#### Constraints



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-sla-confirmation-deadline",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-sla-confirmation-deadline",
  "version" : "0.1.0",
  "name" : "DerivacionSlaConfirmationDeadline",
  "title" : "Plazo de confirmación",
  "status" : "draft",
  "date" : "2026-11-20T12:33:32+00:00",
  "description" : "Fecha límite para confirmar una oferta: oferta + 3 días hábiles. Presente solo mientras una oferta está abierta.",
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
      "short" : "Plazo de confirmación",
      "definition" : "Fecha límite para confirmar una oferta: oferta + 3 días hábiles. Presente solo mientras una oferta está abierta."
    },
    {
      "id" : "Extension.extension",
      "path" : "Extension.extension",
      "max" : "0"
    },
    {
      "id" : "Extension.url",
      "path" : "Extension.url",
      "fixedUri" : "https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-sla-confirmation-deadline"
    },
    {
      "id" : "Extension.value[x]",
      "path" : "Extension.value[x]",
      "min" : 1,
      "type" : [{
        "code" : "dateTime"
      }]
    }]
  }
}

```
