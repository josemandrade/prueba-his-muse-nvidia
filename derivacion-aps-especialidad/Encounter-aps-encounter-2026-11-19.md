# Encuentro APS que creó la derivación - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Encuentro APS que creó la derivación**

## Example Encounter: Encuentro APS que creó la derivación

**status**: Finished

**class**: [ActCode: AMB](http://terminology.hl7.org/7.5.0/CodeSystem-v3-ActCode.html#v3-ActCode-AMB) (Ambulatory)

**subject**: [María González (official) Female, DoB: 1968-04-15 ( http://www.registrocivil.cl/run#11111111-1)](Patient-maria-gonzalez.md)

**period**: 2026-11-19 09:00:00-0300 --> 2026-11-19 09:30:00-0300



## Resource Content

```json
{
  "resourceType" : "Encounter",
  "id" : "aps-encounter-2026-11-19",
  "status" : "finished",
  "class" : {
    "system" : "http://terminology.hl7.org/CodeSystem/v3-ActCode",
    "code" : "AMB",
    "display" : "Ambulatory"
  },
  "subject" : {
    "reference" : "Patient/maria-gonzalez"
  },
  "period" : {
    "start" : "2026-11-19T09:00:00-03:00",
    "end" : "2026-11-19T09:30:00-03:00"
  }
}

```
