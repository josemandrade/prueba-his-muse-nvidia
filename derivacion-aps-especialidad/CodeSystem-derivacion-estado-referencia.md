# Estado de la derivación - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Estado de la derivación**

## CodeSystem: Estado de la derivación 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-estado-referencia | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionEstadoReferenciaCS |

 
Los nueve estados del caso de la derivación APS → especialidad (spec §3.1). El estado vive en Task.businessStatus, nunca como valor inventado de Task.status. 

 This Code system is referenced in the content logical definition of the following value sets: 

* [Estado de la derivación](ValueSet-derivacion-estado-referencia.md)



## Resource Content

```json
{
  "resourceType" : "CodeSystem",
  "id" : "derivacion-estado-referencia",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-estado-referencia",
  "version" : "0.1.0",
  "name" : "DerivacionEstadoReferenciaCS",
  "title" : "Estado de la derivación",
  "status" : "draft",
  "date" : "2026-11-20T12:33:32+00:00",
  "description" : "Los nueve estados del caso de la derivación APS → especialidad (spec §3.1). El estado vive en Task.businessStatus, nunca como valor inventado de Task.status.",
  "content" : "complete",
  "count" : 9,
  "concept" : [{
    "code" : "requested",
    "display" : "Requested",
    "definition" : "Derivación creada por APS, aún no recibida por el hub."
  },
  {
    "code" : "received",
    "display" : "Received",
    "definition" : "Derivación recibida por el hub y enrutada a la especialidad."
  },
  {
    "code" : "accepted",
    "display" : "Accepted",
    "definition" : "La especialidad aceptó la derivación (nombrando servicio y profesional)."
  },
  {
    "code" : "rejected",
    "display" : "Rejected",
    "definition" : "La especialidad rechazó la derivación (con motivo); APS re-triajea."
  },
  {
    "code" : "scheduled",
    "display" : "Scheduled",
    "definition" : "Cita reservada; la visita aún no ha empezado."
  },
  {
    "code" : "completed",
    "display" : "Completed",
    "definition" : "Visita atendida; la contrareferencia está pendiente."
  },
  {
    "code" : "counter-referred",
    "display" : "Counter-referred",
    "definition" : "Contrareferencia enviada y recibida por APS; el ciclo está cerrado."
  },
  {
    "code" : "no-show",
    "display" : "No-show",
    "definition" : "El paciente no asistió dos veces; la derivación se cerró sin completar."
  },
  {
    "code" : "cancelled",
    "display" : "Cancelled",
    "definition" : "Derivación cancelada antes de completarse (por APS, el paciente o la especialidad; también por fallecimiento del paciente)."
  }]
}

```
