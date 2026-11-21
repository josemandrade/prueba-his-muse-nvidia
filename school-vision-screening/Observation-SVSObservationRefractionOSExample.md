# Left Eye Refraction - Normal - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Left Eye Refraction - Normal**

## Example Observation: Left Eye Refraction - Normal

Profile: [Left Eye Refraction](StructureDefinition-svs-observation-refraction-os.md)

**identifier**: `urn:oid:1.2.3.4.5.refraction`/REFR-OS-2026-11-22-0043

**status**: Final

**category**: Exam

**code**: Visual acuity left eye

**subject**: [Maria Isabel Gonzalez (official) Female, DoB: 2018-03-15 ( PIXm Cross-reference: PIXM-987654321)](Patient-SVSPatientExample.md)

**effective**: 2026-11-22 10:30:00+0000

**value**: 0 D (Details: UCUM codeD = 'D')

**bodySite**: Left eye



## Resource Content

```json
{
  "resourceType" : "Observation",
  "id" : "SVSObservationRefractionOSExample",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-refraction-os"]
  },
  "identifier" : [{
    "system" : "urn:oid:1.2.3.4.5.refraction",
    "value" : "REFR-OS-2026-11-22-0043"
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
      "code" : "29473-3",
      "display" : "Visual acuity left eye"
    }]
  },
  "subject" : {
    "reference" : "Patient/SVSPatientExample"
  },
  "effectiveDateTime" : "2026-11-22T10:30:00Z",
  "valueQuantity" : {
    "value" : 0,
    "unit" : "D",
    "system" : "http://unitsofmeasure.org",
    "code" : "D"
  },
  "bodySite" : {
    "coding" : [{
      "system" : "http://snomed.info/sct",
      "code" : "363655008",
      "display" : "Left eye"
    }]
  }
}

```
