# Resultado de la entrega de una notificación - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Resultado de la entrega de una notificación**

## CodeSystem: Resultado de la entrega de una notificación 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/CodeSystem/derivacion-resultado-entrega | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionResultadoEntregaCS |

 
Resultados posibles de la entrega de una notificación (lista local). 

 This Code system is referenced in the content logical definition of the following value sets: 

* [Resultado de la entrega de una notificación](ValueSet-derivacion-resultado-entrega.md)



## Resource Content

```json
{
  "resourceType" : "CodeSystem",
  "id" : "derivacion-resultado-entrega",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/CodeSystem/derivacion-resultado-entrega",
  "version" : "0.1.0",
  "name" : "DerivacionResultadoEntregaCS",
  "title" : "Resultado de la entrega de una notificación",
  "status" : "draft",
  "date" : "2026-11-20T12:46:55+00:00",
  "description" : "Resultados posibles de la entrega de una notificación (lista local).",
  "content" : "complete",
  "count" : 2,
  "concept" : [{
    "code" : "delivered",
    "display" : "Delivered",
    "definition" : "La notificación llegó al destinatario."
  },
  {
    "code" : "failed",
    "display" : "Failed",
    "definition" : "La entrega falló; el remitente reintenta (el fallo nunca cambia el estado de la derivación)."
  }]
}

```
