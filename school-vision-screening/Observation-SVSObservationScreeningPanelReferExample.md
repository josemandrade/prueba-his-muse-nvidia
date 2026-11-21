# Screening Panel - Refer Result (Maria Gonzalez) - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Screening Panel - Refer Result (Maria Gonzalez)**

## Example Observation: Screening Panel - Refer Result (Maria Gonzalez)

Profile: [School Vision Screening Panel](StructureDefinition-svs-observation-screening-panel.md)

**identifier**: `urn:oid:1.2.3.4.5.screening-event`/SCR-2026-11-15-0043

**status**: Final

**category**: Vital Signs

**code**: Visual acuity screening panel

**subject**: [Maria Isabel Gonzalez (official) Female, DoB: 2018-03-15 ( PIXm Cross-reference: PIXM-987654321)](Patient-SVSPatientExample.md)

**encounter**: [Encounter: identifier = urn:oid:1.2.3.4.5.encounter-id#ENC-2026-11-15-0042; status = finished; class = Ambulatory (ActCode#AMB); type = Vision Screening; period = 2026-11-15 09:30:00+0000 --> 2026-11-15 09:45:00+0000](Encounter-SVSEncounterScreeningExample.md)

**effective**: 2026-11-15 09:35:00+0000

**performer**: [Carmen Ruiz (official) (urn:oid:1.2.3.4.5.employee#EMP-2026-015)](Practitioner-SVSPractitionerNurseExample.md)

**note**: 

> 

Test used: Snellen 6m; Outcome: Refer; Attempt: 1; Referral indicated: true


**hasMember**: 

* [Observation Visual acuity right eye](Observation-SVSObservationRightEyeAcuityReferExample.md)
* [Observation Visual acuity left eye](Observation-SVSObservationLeftEyeAcuityReferExample.md)



## Resource Content

```json
{
  "resourceType" : "Observation",
  "id" : "SVSObservationScreeningPanelReferExample",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-screening-panel"]
  },
  "identifier" : [{
    "system" : "urn:oid:1.2.3.4.5.screening-event",
    "value" : "SCR-2026-11-15-0043"
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
      "code" : "83700-8",
      "display" : "Visual acuity screening panel"
    }]
  },
  "subject" : {
    "reference" : "Patient/SVSPatientExample"
  },
  "encounter" : {
    "reference" : "Encounter/SVSEncounterScreeningExample"
  },
  "effectiveDateTime" : "2026-11-15T09:35:00Z",
  "performer" : [{
    "reference" : "Practitioner/SVSPractitionerNurseExample"
  }],
  "note" : [{
    "text" : "Test used: Snellen 6m; Outcome: Refer; Attempt: 1; Referral indicated: true"
  }],
  "hasMember" : [{
    "reference" : "Observation/SVSObservationRightEyeAcuityReferExample"
  },
  {
    "reference" : "Observation/SVSObservationLeftEyeAcuityReferExample"
  }]
}

```
