# NT-proBNP de la derivación REF-2026-0001 - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **NT-proBNP de la derivación REF-2026-0001**

## Example Observation: NT-proBNP de la derivación REF-2026-0001

**status**: Final

**code**: Natriuretic peptide.B prohormone N-Terminal [Mass/volume] in Serum or Plasma

**subject**: [María González (official) Female, DoB: 1968-04-15 ( http://www.registrocivil.cl/run#11111111-1)](Patient-maria-gonzalez.md)

**effective**: 2026-11-18 10:00:00-0300

**value**: 850 pg/mL (Details: UCUM codepg/mL = 'pg/mL')



## Resource Content

```json
{
  "resourceType" : "Observation",
  "id" : "ntprobnp-2026-11-19",
  "status" : "final",
  "code" : {
    "coding" : [{
      "system" : "http://loinc.org",
      "code" : "33762-6",
      "display" : "Natriuretic peptide.B prohormone N-Terminal [Mass/volume] in Serum or Plasma"
    }]
  },
  "subject" : {
    "reference" : "Patient/maria-gonzalez"
  },
  "effectiveDateTime" : "2026-11-18T10:00:00-03:00",
  "valueQuantity" : {
    "value" : 850,
    "unit" : "pg/mL",
    "system" : "http://unitsofmeasure.org",
    "code" : "pg/mL"
  }
}

```
