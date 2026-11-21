# Right Eye Acuity - Refer (6/12) - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Right Eye Acuity - Refer (6/12)**

## Example Observation: Right Eye Acuity - Refer (6/12)

Profile: [Right Eye Visual Acuity](StructureDefinition-svs-observation-right-eye-acuity.md)

**identifier**: `urn:oid:1.2.3.4.5.acuity`/ACU-OD-2026-11-15-0043

**status**: Final

**category**: Vital Signs

**code**: Visual acuity right eye

**subject**: [Maria Isabel Gonzalez (official) Female, DoB: 2018-03-15 ( PIXm Cross-reference: PIXM-987654321)](Patient-SVSPatientExample.md)

**effective**: 2026-11-15 09:35:00+0000

**value**: 6 m (Details: UCUM codem = 'm')/12 m (Details: UCUM codem = 'm')

**interpretation**: Abnormal

**bodySite**: Right eye



## Resource Content

```json
{
  "resourceType" : "Observation",
  "id" : "SVSObservationRightEyeAcuityReferExample",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-right-eye-acuity"]
  },
  "identifier" : [{
    "system" : "urn:oid:1.2.3.4.5.acuity",
    "value" : "ACU-OD-2026-11-15-0043"
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
      "code" : "29474-1",
      "display" : "Visual acuity right eye"
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
      "value" : 12,
      "unit" : "m",
      "system" : "http://unitsofmeasure.org",
      "code" : "m"
    }
  },
  "interpretation" : [{
    "coding" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
      "code" : "A",
      "display" : "Abnormal"
    }]
  }],
  "bodySite" : {
    "coding" : [{
      "system" : "http://snomed.info/sct",
      "code" : "363654007",
      "display" : "Right eye"
    }]
  }
}

```
