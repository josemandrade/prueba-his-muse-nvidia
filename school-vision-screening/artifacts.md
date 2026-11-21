# Artifacts Summary - v0.1.0

* [**Table of Contents**](toc.md)
* **Artifacts Summary**

## Artifacts Summary

This page provides a list of the FHIR artifacts defined as part of this implementation guide.

### Structures: Resource Profiles 

These define constraints on FHIR resources for systems conforming to this implementation guide.

| | |
| :--- | :--- |
| [Left Eye Refraction](StructureDefinition-svs-observation-refraction-os.md) | Left eye refractive prescription |
| [Left Eye Visual Acuity](StructureDefinition-svs-observation-left-eye-acuity.md) | Left eye visual acuity measurement as Snellen fraction using Ratio |
| [Ophthalmology Diagnosis](StructureDefinition-svs-observation-diagnosis.md) | Diagnosis from ophthalmology assessment |
| [Ophthalmology Follow-up Plan](StructureDefinition-svs-care-plan-follow-up.md) | Follow-up plan from ophthalmology assessment |
| [Ophthalmology Vision Assessment Report](StructureDefinition-svs-diagnostic-report-assessment.md) | Complete ophthalmology assessment report for vision screening referral |
| [Primary Care Document Reference (IP-4)](StructureDefinition-svs-document-reference-ip4.md) | DocumentReference for each of the 6 IP-4 document types received by Primary Care |
| [Primary Care Vision Screening Document Log](StructureDefinition-svs-list-primary-care-documents.md) | List of all vision screening related documents received by Primary Care for a child |
| [Right Eye Refraction](StructureDefinition-svs-observation-refraction-od.md) | Right eye refractive prescription |
| [Right Eye Visual Acuity](StructureDefinition-svs-observation-right-eye-acuity.md) | Right eye visual acuity measurement as Snellen fraction using Ratio |
| [School Vision Screening Opt-Out Consent](StructureDefinition-svs-consent-opt-out.md) | Annual opt-out consent for vision screening program |
| [School Vision Screening Organization](StructureDefinition-svs-organization.md) | Organization profile for School Health Service, Ophthalmology Clinic, or Primary Care Practice |
| [School Vision Screening Panel](StructureDefinition-svs-observation-screening-panel.md) | Panel observation containing right and left eye visual acuity measurements |
| [School Vision Screening Parent/Guardian](StructureDefinition-svs-related-person.md) | Profile for a parent or guardian of a child in the screening program |
| [School Vision Screening Patient (Child)](StructureDefinition-svs-patient.md) | Profile for a child enrolled in school vision screening program |
| [School Vision Screening Practitioner](StructureDefinition-svs-practitioner.md) | Base profile for practitioners in the school vision screening program |
| [School Vision Screening Practitioner Role](StructureDefinition-svs-practitioner-role.md) | Role profile for school nurses and service leads |
| [School Vision Screening Questionnaire Response](StructureDefinition-svs-questionnaire-response-screening.md) | Screening form response captured by the nurse |
| [School Vision Screening Referral](StructureDefinition-svs-service-request-referral.md) | Referral from school nurse to ophthalmology for vision assessment |
| [School Vision Screening Referral Tracking](StructureDefinition-svs-task-referral-tracking.md) | Task for tracking referral workflow state |
| [Teacher Accommodation Notice](StructureDefinition-svs-communication-accommodation.md) | Notice from school nurse to teacher about classroom accommodation |

### Terminology: Value Sets 

These define sets of codes used by systems conforming to this implementation guide.

| | |
| :--- | :--- |
| [Classroom Accommodation Types ValueSet](ValueSet-svs-accommodation-type-vs.md) | Types of classroom accommodations for vision impairment |
| [School Health Service Practitioner Roles ValueSet](ValueSet-svs-practitioner-role-vs.md) | Roles within the school health service |
| [School Vision Screening Document Types ValueSet](ValueSet-svs-document-type-vs.md) | Types of documents exchanged with Primary Care |
| [School Vision Screening Outcomes ValueSet](ValueSet-svs-screening-outcome-vs.md) | Possible outcomes of a vision screening encounter |
| [School Vision Screening Referral Reasons ValueSet](ValueSet-svs-referral-reason-vs.md) | Reasons for referral to ophthalmology |
| [School Vision Screening Test Methods ValueSet](ValueSet-svs-screening-test-method-vs.md) | Allowed test methods for school vision screening |
| [Visual Acuity Interpretation ValueSet](ValueSet-svs-acuity-interpretation-vs.md) | Interpretation codes for visual acuity results |

### Terminology: Code Systems 

These define new code systems used by systems conforming to this implementation guide.

| | |
| :--- | :--- |
| [Classroom Accommodation Types](CodeSystem-svs-accommodation-type.md) | Types of classroom accommodations for vision impairment |
| [School Health Service Practitioner Roles](CodeSystem-svs-practitioner-role.md) | Roles within the school health service for vision screening |
| [School Vision Screening Document Types](CodeSystem-svs-document-type.md) | Types of documents exchanged with Primary Care (IP-4) |
| [School Vision Screening Outcomes](CodeSystem-svs-screening-outcome.md) | Possible outcomes of a vision screening encounter |
| [School Vision Screening Referral Reasons](CodeSystem-svs-referral-reason.md) | Reasons for referral to ophthalmology |
| [School Vision Screening Test Methods](CodeSystem-svs-screening-test-method.md) | Methods used for visual acuity screening in school settings |

### Example: Example Instances 

These are example instances that show what data produced and consumed by systems conforming with this implementation guide might look like.

| | |
| :--- | :--- |
| [Child Example - Maria Gonzalez](Patient-SVSPatientExample.md) | Synthetic example of an 8-year-old child |
| [Diagnosis - Mild Myopia OD](Observation-SVSObservationDiagnosisExample.md) |  |
| [DocumentReference - Screening Pass Result (IP-4)](DocumentReference-SVSDocumentReferenceScreeningPassExample.md) | Primary Care receives screening pass result via MHD |
| [Follow-up Plan - 12 Month Review](CarePlan-SVSCarePlanFollowUpExample.md) |  |
| [Left Eye Acuity - Pass (6/9)](Observation-SVSObservationLeftEyeAcuityReferExample.md) |  |
| [Left Eye Refraction - Normal](Observation-SVSObservationRefractionOSExample.md) |  |
| [Ophthalmology Assessment - Maria Gonzalez](DiagnosticReport-SVSDiagnosticReportAssessmentExample.md) | Complete assessment: mild myopia OD, prescription -1.00 DS, follow-up 12 months |
| [Ophthalmology Clinic Example](Organization-SVSOrganizationClinicExample.md) | Ophthalmology clinic receiving vision screening referrals |
| [Parent Example - Ana Gonzalez](RelatedPerson-SVSRelatedPersonExample.md) | Mother of Maria Gonzalez |
| [Primary Care Document Log - Maria Gonzalez](List-SVSListPrimaryCareDocumentsExample.md) |  |
| [Primary Care Example - Centro de Salud Las Rosas](Organization-SVSOrganizationPrimaryCareExample.md) | Primary care center receiving screening results |
| [Referral to Ophthalmology - Maria Gonzalez](ServiceRequest-SVSServiceRequestReferralExample.md) | Referral from school nurse to ophthalmology for right eye acuity 6/12 |
| [Right Eye Acuity - Refer (6/12)](Observation-SVSObservationRightEyeAcuityReferExample.md) |  |
| [Right Eye Refraction -1.00 DS](Observation-SVSObservationRefractionODExample.md) |  |
| [School Example - Colegio Publico San Isidro](Organization-SVSOrganizationSchoolExample.md) | Public school with vision screening program |
| [School Health Service - Servicio de Salud Escolar Madrid](Organization-SVSOrganizationSchoolHealthServiceExample.md) | Regional school health service overseeing vision screening |
| [School Nurse Example - Carmen Ruiz](Practitioner-SVSPractitionerNurseExample.md) | School nurse conducting vision screening |
| [Screening Encounter - Maria Gonzalez](Encounter-SVSEncounterScreeningExample.md) |  |
| [Screening Panel - Refer Result (Maria Gonzalez)](Observation-SVSObservationScreeningPanelReferExample.md) | Visual acuity screening panel showing refer result: right eye 6/12 (<=6/12) |

