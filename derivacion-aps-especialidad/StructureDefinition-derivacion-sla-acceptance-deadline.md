# Plazo de aceptación - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Plazo de aceptación**

## Extension: Plazo de aceptación 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-sla-acceptance-deadline | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionSlaAcceptanceDeadline |

Fecha límite para la decisión de aceptación/rechazo: creación + 5 días hábiles (2 si es urgente).

**Context of Use**

**Usage info**

**Usages:**

* Use this Extension: [Tarea de derivación (registro de estado)](StructureDefinition-derivacion-tarea.md)
* Examples for this Extension: [Bundle/bundle-pi0-ref-2026-0001](Bundle-bundle-pi0-ref-2026-0001.md) and [Task/tarea-ref-2026-0001](Task-tarea-ref-2026-0001.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-sla-acceptance-deadline.json)

### Formal Views of Extension Content

 [Description of Profiles, Differentials, Snapshots, and how the XML and JSON presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-sla-acceptance-deadline.csv), [Excel](StructureDefinition-derivacion-sla-acceptance-deadline.xlsx), [Schematron](StructureDefinition-derivacion-sla-acceptance-deadline.sch) 

#### Constraints



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-sla-acceptance-deadline",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-sla-acceptance-deadline",
  "version" : "0.1.0",
  "name" : "DerivacionSlaAcceptanceDeadline",
  "title" : "Plazo de aceptación",
  "status" : "draft",
  "date" : "2026-11-20T12:46:55+00:00",
  "description" : "Fecha límite para la decisión de aceptación/rechazo: creación + 5 días hábiles (2 si es urgente).",
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
      "short" : "Plazo de aceptación",
      "definition" : "Fecha límite para la decisión de aceptación/rechazo: creación + 5 días hábiles (2 si es urgente)."
    },
    {
      "id" : "Extension.extension",
      "path" : "Extension.extension",
      "max" : "0"
    },
    {
      "id" : "Extension.url",
      "path" : "Extension.url",
      "fixedUri" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-sla-acceptance-deadline"
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
