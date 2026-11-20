# Especialidad / servicio (catálogo local) - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Especialidad / servicio (catálogo local)**

## CodeSystem: Especialidad / servicio (catálogo local) 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/CodeSystem/derivacion-especialidad | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionEspecialidadCS |

 
Catálogo local de especialidades y servicios, versionado por la red (hub + servicios). El ejemplo trabajado es cardiología; la red amplía el catálogo sin tocar esta guía. 

 This Code system is referenced in the content logical definition of the following value sets: 

* [Especialidad / servicio (catálogo local)](ValueSet-derivacion-especialidad.md)



## Resource Content

```json
{
  "resourceType" : "CodeSystem",
  "id" : "derivacion-especialidad",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/CodeSystem/derivacion-especialidad",
  "version" : "0.1.0",
  "name" : "DerivacionEspecialidadCS",
  "title" : "Especialidad / servicio (catálogo local)",
  "status" : "draft",
  "date" : "2026-11-20T12:49:56+00:00",
  "description" : "Catálogo local de especialidades y servicios, versionado por la red (hub + servicios). El ejemplo trabajado es cardiología; la red amplía el catálogo sin tocar esta guía.",
  "content" : "complete",
  "count" : 1,
  "concept" : [{
    "code" : "cardiologia",
    "display" : "Cardiology",
    "definition" : "Servicio de cardiología (ejemplo trabajado)."
  }]
}

```
