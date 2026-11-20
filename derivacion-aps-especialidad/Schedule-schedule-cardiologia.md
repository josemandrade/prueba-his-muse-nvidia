# Agenda de cardiología - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Agenda de cardiología**

## Example Schedule: Agenda de cardiología

**actor**: [Cardiology (Cardiology) by Servicio de Cardiología (http://especialidad.example.org/organization#CARDIOLOGIA) (http://especialidad.example.org/service#cardiologia)](HealthcareService-servicio-cardiologia.md)

**planningHorizon**: 2026-12-01 08:00:00-0300 --> 2026-12-31 17:00:00-0300

**comment**: Agenda de la consulta de cardiología.



## Resource Content

```json
{
  "resourceType" : "Schedule",
  "id" : "schedule-cardiologia",
  "actor" : [{
    "reference" : "HealthcareService/servicio-cardiologia"
  }],
  "planningHorizon" : {
    "start" : "2026-12-01T08:00:00-03:00",
    "end" : "2026-12-31T17:00:00-03:00"
  },
  "comment" : "Agenda de la consulta de cardiología."
}

```
