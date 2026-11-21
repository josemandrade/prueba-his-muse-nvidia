# Right Eye Refraction -1.00 DS - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Right Eye Refraction -1.00 DS**

## Example Observation: Right Eye Refraction -1.00 DS

Profile: [Right Eye Refraction](StructureDefinition-svs-observation-refraction-od.md)

**identifier**: `urn:oid:1.2.3.4.5.refraction`/REFR-OD-2026-11-22-0043

**status**: Final

**category**: Exam

**code**: Visual acuity right eye

**subject**: [Maria Isabel Gonzalez (official) Female, DoB: 2018-03-15 ( PIXm Cross-reference: PIXM-987654321)](Patient-SVSPatientExample.md)

**effective**: 2026-11-22 10:30:00+0000

**value**: -1 D (Details: UCUM codeD = 'D')

**bodySite**: Right eye



## Resource Content

```json
{
  "resourceType" : "Observation",
  "id" : "SVSObservationRefractionODExample",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-refraction-od"]
  },
  "identifier" : [{
    "system" : "urn:oid:1.2.3.4.5.refraction",
    "value" : "REFR-OD-2026-11-22-0043"
  }],
  "status" : "final",
  "category" : [{
    "coding" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/observation-category",
      "code" : "exam",
      "display" : "Exam"
    }]
  }],
  "code" : {
    "coding" : [{
      "system" : "http://loinc.org",
      "code" : "29474-1",
      "display" : "Visual acuity right eye"
    }]
  },
  "subject" : {
    "reference" : "Patient/SVSPatientExample"
  },
  "effectiveDateTime" : "2026-11-22T10:30:00Z",
  "valueQuantity" : {
    "value" : -1,
    "unit" : "D",
    "system" : "http://unitsofmeasure.org",
    "code" : "D"
  },
  "bodySite" : {
    "coding" : [{
      "system" : "http://snomed.info/sct",
      "code" : "363654007",
      "display" : "Right eye"
    }]
  }
}

```
