# Motivo de rechazo - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Motivo de rechazo**

## CodeSystem: Motivo de rechazo 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/CodeSystem/derivacion-motivo-rechazo | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionMotivoRechazoCS |

 
Motivos de rechazo de la derivación (lista local de la especialidad; el texto libre acompaña al código). 

 This Code system is referenced in the content logical definition of the following value sets: 

* [Motivo de rechazo](ValueSet-derivacion-motivo-rechazo.md)



## Resource Content

```json
{
  "resourceType" : "CodeSystem",
  "id" : "derivacion-motivo-rechazo",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/CodeSystem/derivacion-motivo-rechazo",
  "version" : "0.1.0",
  "name" : "DerivacionMotivoRechazoCS",
  "title" : "Motivo de rechazo",
  "status" : "draft",
  "date" : "2026-11-20T12:46:55+00:00",
  "description" : "Motivos de rechazo de la derivación (lista local de la especialidad; el texto libre acompaña al código).",
  "content" : "complete",
  "count" : 3,
  "concept" : [{
    "code" : "missing-exam",
    "display" : "Missing exam",
    "definition" : "Falta un examen necesario para el triaje (ejemplo trabajado: falta el ecocardiograma)."
  },
  {
    "code" : "wrong-specialty",
    "display" : "Wrong specialty",
    "definition" : "La derivación no corresponde a esta especialidad."
  },
  {
    "code" : "capacity",
    "display" : "Capacity",
    "definition" : "La especialidad no tiene capacidad para atender la derivación en plazo."
  }]
}

```
