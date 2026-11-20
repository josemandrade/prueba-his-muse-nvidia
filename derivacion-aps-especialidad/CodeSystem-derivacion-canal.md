# Canal de notificación - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Canal de notificación**

## CodeSystem: Canal de notificación 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/CodeSystem/derivacion-canal | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionCanalCS |

 
Canales por los que se envía una notificación (lista local; el caso no fija un canal por notificación). 

 This Code system is referenced in the content logical definition of the following value sets: 

* [Canal de notificación](ValueSet-derivacion-canal.md)



## Resource Content

```json
{
  "resourceType" : "CodeSystem",
  "id" : "derivacion-canal",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/CodeSystem/derivacion-canal",
  "version" : "0.1.0",
  "name" : "DerivacionCanalCS",
  "title" : "Canal de notificación",
  "status" : "draft",
  "date" : "2026-11-20T12:46:55+00:00",
  "description" : "Canales por los que se envía una notificación (lista local; el caso no fija un canal por notificación).",
  "content" : "complete",
  "count" : 3,
  "concept" : [{
    "code" : "phone",
    "display" : "Phone",
    "definition" : "Llamada telefónica."
  },
  {
    "code" : "in-person",
    "display" : "In person",
    "definition" : "Aviso presencial."
  },
  {
    "code" : "system-message",
    "display" : "System message",
    "definition" : "Mensaje del sistema (portal o mensajería del EHR)."
  }]
}

```
