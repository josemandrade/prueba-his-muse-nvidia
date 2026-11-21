# School Vision Screening Implementation Guide

**Version:** 0.1.0 (CI Build)  
**FHIR Version:** 4.0.1  
**Status:** Draft  
**Canonical URL:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening`

---

## Overview

This Implementation Guide defines the FHIR R4 profiles, operations, and examples for the **School Vision Screening** interoperability workflow. It enables the exchange of vision screening results, referrals to ophthalmology, and assessment feedback between:

- **School Health Service** (school nurses conducting screening)
- **Ophthalmology Clinic / Hospital** (assessing referred children)
- **Primary Care Team** (receiving results for the child's health record)
- **Parents/Guardians** (receiving notifications, providing consent)
- **Teachers** (receiving classroom accommodation notices)

---

## Clinical Use Case

Vision problems in schoolchildren go undetected until they affect learning. The school nurse screens visual acuity per eye during the school year using Snellen chart (6m), Tumbling E optotypes, or Lea symbols.

**Thresholds:**
- **Pass:** ≥6/9 in each eye
- **Refer:** ≤6/12 in either eye OR ≥2 line difference between eyes

Children with abnormal results are referred to an ophthalmologist. The referral result must reach the primary care team for the health record, and parents must be notified.

---

## Key Interoperability Points

| IP | Name | Description | FHIR Resources | IHE Profile |
|----|------|-------------|----------------|-------------|
| **IP-1** | Screening Result Capture | Nurse records structured screening data (acuity per eye, test used, outcome) | `Observation` panel + 2 member `Observation`s | — |
| **IP-2** | Referral Dispatch | Structured referral with 4-week deadline tracking, parent decline handling | `ServiceRequest` + `Task` | **360X** (PCC-55/56/58/61) |
| **IP-3** | Assessment Return | Ophthalmology feedback to school nurse (summary) and primary care (full) | `DiagnosticReport` + `Observation`s + `CarePlan` | **360X** (PCC-61), **MHD** (ITI-65) |
| **IP-4** | Primary Care Receive | Screening results + assessments entered in child's health record (6 document types) | `DocumentReference` + `List` | **MHD** (ITI-65) |
| **IP-5** | Teacher Accommodation | Nurse generates accommodation notice from assessment | `Communication` | — |

---

## Profiles Summary

| Profile | Base Resource | Purpose |
|---------|---------------|---------|
| `SVSPatient` | `Patient` | Child demographics with school roll number, grade at screening |
| `SVSRelatedPerson` | `RelatedPerson` | Parent/guardian with opt-out consent status |
| `SVSPractitioner` / `SVSPractitionerRole` | `Practitioner` / `PractitionerRole` | School nurse, service lead, ophthalmologist |
| `SVSObservationScreeningPanel` | `Observation` | Panel with right/left eye acuity as member `Observation`s (Ratio) |
| `SVSServiceRequestReferral` | `ServiceRequest` | 360X referral to ophthalmology |
| `SVSTaskReferralTracking` | `Task` | 360X referral workflow tracking |
| `SVSDiagnosticReportAssessment` | `DiagnosticReport` | Ophthalmology assessment report |
| `SVSObservationDiagnosis` / `RefractionOD` / `RefractionOS` | `Observation` | Diagnosis, right/left eye refraction |
| `SVSCarePlanFollowUp` | `CarePlan` | Follow-up plan (review interval, patching) |
| `SVSCommunicationAccommodation` | `Communication` | Teacher accommodation notice |
| `SVSConsentOptOut` | `Consent` | Annual opt-out consent (revocable mid-year) |
| `SVSDocumentReferenceIP4` | `DocumentReference` | Primary care document receipts (6 types) |
| `SVSListPrimaryCareDocuments` | `List` | Primary care document log |

---

## Operations

| Op ID | Name | Interaction | IHE Profile |
|-------|------|-------------|-------------|
| OP-1 | Record Screening | `POST Observation` (panel + members) | — |
| OP-2a | Submit Referral | `POST ServiceRequest` + `POST Task` | **360X PCC-55** |
| OP-2b | Cancel Referral | `PATCH ServiceRequest` (cancelled) | **360X PCC-58** |
| OP-2c | Reject Referral | `PATCH Task` (rejected) | **360X PCC-56** |
| OP-2d | Accept Referral | `PATCH Task` (accepted) | **360X PCC-56** |
| OP-3a | Return Summary | `GET DiagnosticReport` / `POST DocumentReference` | **360X PCC-61**, **MHD ITI-65** |
| OP-3b | Return Full | `POST DocumentReference` | **MHD ITI-65** |
| OP-4a-f | Send to Primary Care | `POST DocumentReference` (6 types) | **MHD ITI-65** |
| OP-5 | Send Accommodation | `POST Communication` | — |
| OP-6 | Query Demographics | `GET Patient?identifier=...` | **PIXm ITI-83**, **PDQm ITI-78** |

---

## Navigation

| Page | Description |
|------|-------------|
| [Clinical Use Case](usecase.html) | Detailed problem statement, users, data flows, consent, success criteria |
| [Process (BPMN)](process.html) | BPMN model with swimlanes, interoperability points marked |
| [Resource Diagram](resources.html) | Resource graph centred on ServiceRequest/Task |
| [Sequence Diagrams](sequences.html) | 7 flows with operation tables |
| [Profiles](profiles.html) | All profile definitions |
| [Operations](operations.html) | Operation details with examples |
| [IHE Relationships](ihe.html) | Profile fit assessment per interoperability point |
| [Lifecycle](lifecycle.html) | State tables for workflow resources |
| [Terminology](terminology.html) | CodeSystems, ValueSets, terminology versions |
| [Public Health & Consent](public-health.html) | Opt-out consent, legal basis, data governance |
| [Examples](examples.html) | Synthetic examples for all profiles |

---

## Implementation Notes

- **Terminology Versions:** SNOMED CT 2026-03-15, LOINC 2.76, UCUM 2.0.1
- **Snellen Acuity:** Expressed as `Ratio` (numerator/denominator in meters), not `Quantity`
- **Consent:** Opt-out model, revocable mid-year via multiple `Consent.provision` entries
- **Referral:** Fresh lifecycle on re-issue; `ServiceRequest.replaces` links to cancelled referral
- **Document Exchange:** MHD ITI-65 with `contentType=application/fhir+json`
- **Examples:** All synthetic — no real patient data

---

## Dependencies

- `hl7.fhir.r4.core#4.0.1`
- Template: `fhir.base.template#1.6.0`

---

## License

This Implementation Guide is licensed under [CC0-1.0](https://creativecommons.org/publicdomain/zero/1.0/).