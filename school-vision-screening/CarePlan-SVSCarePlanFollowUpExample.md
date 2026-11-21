# Follow-up Plan - 12 Month Review - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Follow-up Plan - 12 Month Review**

## Example CarePlan: Follow-up Plan - 12 Month Review

Profile: [Ophthalmology Follow-up Plan](StructureDefinition-svs-care-plan-follow-up.md)

**identifier**: `urn:oid:1.2.3.4.5.care-plan`/CP-2026-11-22-0043

**status**: Active

**intent**: Plan

**category**: Assessment Plan

**subject**: [Maria Isabel Gonzalez (official) Female, DoB: 2018-03-15 ( PIXm Cross-reference: PIXM-987654321)](Patient-SVSPatientExample.md)

**encounter**: [Encounter: identifier = urn:oid:1.2.3.4.5.encounter-id#ENC-2026-11-15-0042; status = finished; class = Ambulatory (ActCode#AMB); type = Vision Screening; period = 2026-11-15 09:30:00+0000 --> 2026-11-15 09:45:00+0000](Encounter-SVSEncounterScreeningExample.md)

**period**: 2026-11-22 10:30:00+0000 --> 2027-11-22 10:30:00+0000

> **activity**

### Details

| | | | | | |
| :--- | :--- | :--- | :--- | :--- | :--- |
| - | **Kind** | **Code** | **Status** | **Scheduled[x]** | **Description** |
| * | ServiceRequest | Myopia follow-up | Not Started | 2027-11-22 10:30:00+0000 --> 2027-11-22 10:30:00+0000 | Follow-up in 12 months for myopia monitoring |




## Resource Content

```json
{
  "resourceType" : "CarePlan",
  "id" : "SVSCarePlanFollowUpExample",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-care-plan-follow-up"]
  },
  "identifier" : [{
    "system" : "urn:oid:1.2.3.4.5.care-plan",
    "value" : "CP-2026-11-22-0043"
  }],
  "status" : "active",
  "intent" : "plan",
  "category" : [{
    "coding" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/careplan-category",
      "code" : "assess-plan",
      "display" : "Assessment Plan"
    }]
  }],
  "subject" : {
    "reference" : "Patient/SVSPatientExample"
  },
  "encounter" : {
    "reference" : "Encounter/SVSEncounterScreeningExample"
  },
  "period" : {
    "start" : "2026-11-22T10:30:00Z",
    "end" : "2027-11-22T10:30:00Z"
  },
  "activity" : [{
    "detail" : {
      "kind" : "ServiceRequest",
      "code" : {
        "coding" : [{
          "system" : "http://snomed.info/sct",
          "code" : "373124007",
          "display" : "Myopia follow-up"
        }]
      },
      "status" : "not-started",
      "scheduledPeriod" : {
        "start" : "2027-11-22T10:30:00Z",
        "end" : "2027-11-22T10:30:00Z"
      },
      "description" : "Follow-up in 12 months for myopia monitoring"
    }
  }]
}

```
