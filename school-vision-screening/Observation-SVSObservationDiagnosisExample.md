# Diagnosis - Mild Myopia OD - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Diagnosis - Mild Myopia OD**

## Example Observation: Diagnosis - Mild Myopia OD

Profile: [Ophthalmology Diagnosis](StructureDefinition-svs-observation-diagnosis.md)

**identifier**: `urn:oid:1.2.3.4.5.diagnosis`/DIAG-2026-11-22-0043

**status**: Final

**category**: Diagnosis

**code**: Myopia

**subject**: [Maria Isabel Gonzalez (official) Female, DoB: 2018-03-15 ( PIXm Cross-reference: PIXM-987654321)](Patient-SVSPatientExample.md)

**effective**: 2026-11-22 10:30:00+0000

**value**: Myopia

**bodySite**: Right eye



## Resource Content

```json
{
  "resourceType" : "Observation",
  "id" : "SVSObservationDiagnosisExample",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-diagnosis"]
  },
  "identifier" : [{
    "system" : "urn:oid:1.2.3.4.5.diagnosis",
    "value" : "DIAG-2026-11-22-0043"
  }],
  "status" : "final",
  "category" : [{
    "coding" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/observation-category",
      "code" : "diagnosis",
      "display" : "Diagnosis"
    }]
  }],
  "code" : {
    "coding" : [{
      "system" : "http://snomed.info/sct",
      "code" : "373124007",
      "display" : "Myopia"
    }]
  },
  "subject" : {
    "reference" : "Patient/SVSPatientExample"
  },
  "effectiveDateTime" : "2026-11-22T10:30:00Z",
  "valueCodeableConcept" : {
    "coding" : [{
      "system" : "http://snomed.info/sct",
      "code" : "373124007",
      "display" : "Myopia"
    }]
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
