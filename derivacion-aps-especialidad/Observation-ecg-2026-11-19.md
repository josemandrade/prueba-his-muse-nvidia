# ECG de la derivación REF-2026-0001 - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **ECG de la derivación REF-2026-0001**

## Example Observation: ECG de la derivación REF-2026-0001

**status**: Final

**code**: EKG study

**subject**: [María González (official) Female, DoB: 1968-04-15 ( http://www.registrocivil.cl/run#11111111-1)](Patient-maria-gonzalez.md)

**effective**: 2026-11-18 10:00:00-0300

**value**: Ritmo sinusal, 72 lpm, sin isquemia aguda.



## Resource Content

```json
{
  "resourceType" : "Observation",
  "id" : "ecg-2026-11-19",
  "status" : "final",
  "code" : {
    "coding" : [{
      "system" : "http://loinc.org",
      "code" : "11524-6",
      "display" : "EKG study"
    }]
  },
  "subject" : {
    "reference" : "Patient/maria-gonzalez"
  },
  "effectiveDateTime" : "2026-11-18T10:00:00-03:00",
  "valueString" : "Ritmo sinusal, 72 lpm, sin isquemia aguda."
}

```
