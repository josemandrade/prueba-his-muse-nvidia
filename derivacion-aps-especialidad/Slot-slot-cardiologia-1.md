# Slot de cardiología (reservado) - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Slot de cardiología (reservado)**

## Example Slot: Slot de cardiología (reservado)

**schedule**: [Schedule: planningHorizon = 2026-12-01 08:00:00-0300 --> 2026-12-31 17:00:00-0300; comment = Agenda de la consulta de cardiología.](Schedule-schedule-cardiologia.md)

**status**: Busy

**start**: 2026-12-02 10:00:00-0300

**end**: 2026-12-02 10:30:00-0300



## Resource Content

```json
{
  "resourceType" : "Slot",
  "id" : "slot-cardiologia-1",
  "schedule" : {
    "reference" : "Schedule/schedule-cardiologia"
  },
  "status" : "busy",
  "start" : "2026-12-02T10:00:00-03:00",
  "end" : "2026-12-02T10:30:00-03:00"
}

```
