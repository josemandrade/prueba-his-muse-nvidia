# Left Eye Acuity - Pass (6/9) - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Left Eye Acuity - Pass (6/9)**

## Example Observation: Left Eye Acuity - Pass (6/9)

Profile: [Left Eye Visual Acuity](StructureDefinition-svs-observation-left-eye-acuity.md)

**identifier**: `urn:oid:1.2.3.4.5.acuity`/ACU-OS-2026-11-15-0043

**status**: Final

**category**: Vital Signs

**code**: Visual acuity left eye

**subject**: [Maria Isabel Gonzalez (official) Female, DoB: 2018-03-15 ( PIXm Cross-reference: PIXM-987654321)](Patient-SVSPatientExample.md)

**effective**: 2026-11-15 09:35:00+0000

**value**: 6 m (Details: UCUM codem = 'm')/9 m (Details: UCUM codem = 'm')

**interpretation**: Normal

**bodySite**: Left eye



## Resource Content

```json
{
  "resourceType" : "Observation",
  "id" : "SVSObservationLeftEyeAcuityReferExample",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-left-eye-acuity"]
  },
  "identifier" : [{
    "system" : "urn:oid:1.2.3.4.5.acuity",
    "value" : "ACU-OS-2026-11-15-0043"
  }],
  "status" : "final",
  "category" : [{
    "coding" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/observation-category",
      "code" : "vital-signs",
      "display" : "Vital Signs"
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
  "effectiveDateTime" : "2026-11-15T09:35:00Z",
  "valueRatio" : {
    "numerator" : {
      "value" : 6,
      "unit" : "m",
      "system" : "http://unitsofmeasure.org",
      "code" : "m"
    },
    "denominator" : {
      "value" : 9,
      "unit" : "m",
      "system" : "http://unitsofmeasure.org",
      "code" : "m"
    }
  },
  "interpretation" : [{
    "coding" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
      "code" : "N",
      "display" : "Normal"
    }]
  }],
  "bodySite" : {
    "coding" : [{
      "system" : "http://snomed.info/sct",
      "code" : "363655008",
      "display" : "Left eye"
    }]
  }
}

```
