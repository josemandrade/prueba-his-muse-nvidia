# Referral to Ophthalmology - Maria Gonzalez - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Referral to Ophthalmology - Maria Gonzalez**

## Example ServiceRequest: Referral to Ophthalmology - Maria Gonzalez

Profile: [School Vision Screening Referral](StructureDefinition-svs-service-request-referral.md)

**identifier**: `urn:oid:1.2.3.4.5.referral`/REF-2026-11-15-0043, `urn:ihe:pcc:360x:referral-id`/360X-REF-2026-11-15-0043

**status**: Active

**intent**: Order

**category**: Referral

**priority**: Routine

**code**: Vision screening referral: acuity OD 6/12, OS 6/9

**subject**: [Maria Isabel Gonzalez (official) Female, DoB: 2018-03-15 ( PIXm Cross-reference: PIXM-987654321)](Patient-SVSPatientExample.md)

**encounter**: [Encounter: identifier = urn:oid:1.2.3.4.5.encounter-id#ENC-2026-11-15-0042; status = finished; class = Ambulatory (ActCode#AMB); type = Vision Screening; period = 2026-11-15 09:30:00+0000 --> 2026-11-15 09:45:00+0000](Encounter-SVSEncounterScreeningExample.md)

**occurrence**: 2026-11-15 09:45:00+0000

**authoredOn**: 2026-11-15 09:45:00+0000

**requester**: [Carmen Ruiz (official) (urn:oid:1.2.3.4.5.employee#EMP-2026-015)](Practitioner-SVSPractitionerNurseExample.md)

**performer**: [Clinica Oftalmologica Central (Healthcare Provider) (urn:oid:1.2.3.4.5.clinic-id#CLI-OPT-2026-001)](Organization-SVSOrganizationClinicExample.md)

**reasonCode**: Decreased visual acuity

**reasonReference**: [Observation Visual acuity screening panel](Observation-SVSObservationScreeningPanelReferExample.md)



## Resource Content

```json
{
  "resourceType" : "ServiceRequest",
  "id" : "SVSServiceRequestReferralExample",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-service-request-referral"]
  },
  "identifier" : [{
    "system" : "urn:oid:1.2.3.4.5.referral",
    "value" : "REF-2026-11-15-0043"
  },
  {
    "system" : "urn:ihe:pcc:360x:referral-id",
    "value" : "360X-REF-2026-11-15-0043"
  }],
  "status" : "active",
  "intent" : "order",
  "category" : [{
    "coding" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/service-request-category",
      "code" : "referral",
      "display" : "Referral"
    }]
  }],
  "priority" : "routine",
  "code" : {
    "coding" : [{
      "system" : "http://snomed.info/sct",
      "code" : "307924000",
      "display" : "Referral to ophthalmologist"
    }],
    "text" : "Vision screening referral: acuity OD 6/12, OS 6/9"
  },
  "subject" : {
    "reference" : "Patient/SVSPatientExample"
  },
  "encounter" : {
    "reference" : "Encounter/SVSEncounterScreeningExample"
  },
  "occurrenceDateTime" : "2026-11-15T09:45:00Z",
  "authoredOn" : "2026-11-15T09:45:00Z",
  "requester" : {
    "reference" : "Practitioner/SVSPractitionerNurseExample"
  },
  "performer" : [{
    "reference" : "Organization/SVSOrganizationClinicExample"
  }],
  "reasonCode" : [{
    "coding" : [{
      "system" : "http://snomed.info/sct",
      "code" : "416070007",
      "display" : "Decreased visual acuity"
    }]
  }],
  "reasonReference" : [{
    "reference" : "Observation/SVSObservationScreeningPanelReferExample"
  }]
}

```
