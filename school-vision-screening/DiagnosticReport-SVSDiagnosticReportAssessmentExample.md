# Ophthalmology Assessment - Maria Gonzalez - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Ophthalmology Assessment - Maria Gonzalez**

## Example DiagnosticReport: Ophthalmology Assessment - Maria Gonzalez

Profile: [Ophthalmology Vision Assessment Report](StructureDefinition-svs-diagnostic-report-assessment.md)

### Ophthalmology study (Ophthalmology) 

| | |
| :--- | :--- |
| Subject | Maria Isabel Gonzalez (official) Female, DoB: 2018-03-15 ( PIXm Cross-reference: PIXM-987654321) |
| Relevant Time | 2026-11-22 10:30:00+0000 |
| Reported | 2026-11-22 11:00:00+0000 |
| Performer | [Carmen Ruiz (official) (urn:oid:1.2.3.4.5.employee#EMP-2026-015)](Practitioner-SVSPractitionerNurseExample.md) |
| Identifier | `urn:oid:1.2.3.4.5.assessment`/ASM-2026-11-22-0043 |

**Report Details**

* **Code**: [Myopia](Observation-SVSObservationDiagnosisExample.md)(Right eye)
  * **Value**: Myopia
  * **Flags**: Final
* **Code**: [Visual acuity right eye](Observation-SVSObservationRefractionODExample.md)(Right eye)
  * **Value**: -1 D (Details: UCUM codeD = 'D')
  * **Flags**: Final
* **Code**: [Visual acuity left eye](Observation-SVSObservationRefractionOSExample.md)(Left eye)
  * **Value**: 0 D (Details: UCUM codeD = 'D')
  * **Flags**: Final

Mild myopia OD. Prescription: -1.00 DS OD. Follow-up: 12 months.

**Coded Conclusions:**

* Myopia



## Resource Content

```json
{
  "resourceType" : "DiagnosticReport",
  "id" : "SVSDiagnosticReportAssessmentExample",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-diagnostic-report-assessment"]
  },
  "identifier" : [{
    "system" : "urn:oid:1.2.3.4.5.assessment",
    "value" : "ASM-2026-11-22-0043"
  }],
  "basedOn" : [{
    "reference" : "ServiceRequest/SVSServiceRequestReferralExample"
  }],
  "status" : "final",
  "category" : [{
    "coding" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/v2-0074",
      "code" : "OP",
      "display" : "Ophthalmology"
    }]
  }],
  "code" : {
    "coding" : [{
      "system" : "http://loinc.org",
      "code" : "28626-8",
      "display" : "Ophthalmology study"
    }]
  },
  "subject" : {
    "reference" : "Patient/SVSPatientExample"
  },
  "effectiveDateTime" : "2026-11-22T10:30:00Z",
  "issued" : "2026-11-22T11:00:00Z",
  "performer" : [{
    "reference" : "Practitioner/SVSPractitionerNurseExample"
  }],
  "resultsInterpreter" : [{
    "reference" : "Practitioner/SVSPractitionerNurseExample"
  }],
  "result" : [{
    "reference" : "Observation/SVSObservationDiagnosisExample"
  },
  {
    "reference" : "Observation/SVSObservationRefractionODExample"
  },
  {
    "reference" : "Observation/SVSObservationRefractionOSExample"
  }],
  "conclusion" : "Mild myopia OD. Prescription: -1.00 DS OD. Follow-up: 12 months.",
  "conclusionCode" : [{
    "coding" : [{
      "system" : "http://snomed.info/sct",
      "code" : "373124007",
      "display" : "Myopia"
    }]
  }]
}

```
