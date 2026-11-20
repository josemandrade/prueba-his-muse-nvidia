# Base del cruce de identidad - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Base del cruce de identidad**

## CodeSystem: Base del cruce de identidad 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-base-cruce | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionBaseCruceCS |

 
Cómo se estableció el cruce de identidad en el MPI (lista local). 

 This Code system is referenced in the content logical definition of the following value sets: 

* [Base del cruce de identidad](ValueSet-derivacion-base-cruce.md)



## Resource Content

```json
{
  "resourceType" : "CodeSystem",
  "id" : "derivacion-base-cruce",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-base-cruce",
  "version" : "0.1.0",
  "name" : "DerivacionBaseCruceCS",
  "title" : "Base del cruce de identidad",
  "status" : "draft",
  "date" : "2026-11-20T12:33:32+00:00",
  "description" : "Cómo se estableció el cruce de identidad en el MPI (lista local).",
  "content" : "complete",
  "count" : 2,
  "concept" : [{
    "code" : "identifier",
    "display" : "Identifier",
    "definition" : "El cruce se estableció por un identificador compartido."
  },
  {
    "code" : "demographics",
    "display" : "Demographics",
    "definition" : "El cruce se estableció por datos demográficos."
  }]
}

```
