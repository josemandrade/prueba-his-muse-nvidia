# Rol en la derivación - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Rol en la derivación**

## CodeSystem: Rol en la derivación 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/CodeSystem/derivacion-rol | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionRolCS |

 
Los seis roles del caso de uso (spec §2). Dentro de una derivación, cada rol es una persona (el clínico de triaje no es el agendador — C1). 

 This Code system is referenced in the content logical definition of the following value sets: 

* [Rol en la derivación](ValueSet-derivacion-rol.md)



## Resource Content

```json
{
  "resourceType" : "CodeSystem",
  "id" : "derivacion-rol",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/CodeSystem/derivacion-rol",
  "version" : "0.1.0",
  "name" : "DerivacionRolCS",
  "title" : "Rol en la derivación",
  "status" : "draft",
  "date" : "2026-11-20T12:39:48+00:00",
  "description" : "Los seis roles del caso de uso (spec §2). Dentro de una derivación, cada rol es una persona (el clínico de triaje no es el agendador — C1).",
  "content" : "complete",
  "count" : 6,
  "concept" : [{
    "code" : "aps-doctor",
    "display" : "APS doctor",
    "definition" : "Médico de APS que crea la derivación."
  },
  {
    "code" : "aps-admin",
    "display" : "APS admin",
    "definition" : "Administrativo de APS que registra y sigue la derivación e informa al paciente."
  },
  {
    "code" : "triage-clinician",
    "display" : "Triage clinician",
    "definition" : "Clínico de la especialidad que acepta o rechaza la derivación."
  },
  {
    "code" : "specialty-scheduler",
    "display" : "Specialty scheduler",
    "definition" : "Agendador de la especialidad que reserva y re-agenda la cita."
  },
  {
    "code" : "specialist",
    "display" : "Specialist",
    "definition" : "Especialista que atiende y emite la contrareferencia."
  },
  {
    "code" : "hub-operator",
    "display" : "Hub operator",
    "definition" : "Operador del hub de derivación (enruta, escala, registra cancelaciones, responde consultas de estado)."
  }]
}

```
