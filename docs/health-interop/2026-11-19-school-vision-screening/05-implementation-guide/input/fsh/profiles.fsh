/*
 * Profiles for School Vision Screening - Minimal for Build
 */

// ============================================================
// Patient (Child) Profile
// ============================================================
Profile: SVSPatient
Parent: Patient
Id: svs-patient
Title: "School Vision Screening Patient (Child)"
Description: "Profile for a child enrolled in school vision screening program"
* ^status = #active
* ^experimental = false

// ============================================================
// RelatedPerson (Parent/Guardian) Profile
// ============================================================
Profile: SVSRelatedPerson
Parent: RelatedPerson
Id: svs-related-person
Title: "School Vision Screening Parent/Guardian"
Description: "Profile for a parent or guardian of a child in the screening program"
* ^status = #active
* ^experimental = false
* patient 1..1

// ============================================================
// Practitioner + PractitionerRole Profiles
// ============================================================
Profile: SVSPractitioner
Parent: Practitioner
Id: svs-practitioner
Title: "School Vision Screening Practitioner"
Description: "Base profile for practitioners in the school vision screening program"
* ^status = #active
* ^experimental = false

Profile: SVSPractitionerRole
Parent: PractitionerRole
Id: svs-practitioner-role
Title: "School Vision Screening Practitioner Role"
Description: "Role profile for school nurses and service leads"
* ^status = #active
* ^experimental = false
* practitioner 1..1
* organization 1..1

// ============================================================
// Observation Panel (ScreeningEvent) Profile
// ============================================================
Profile: SVSObservationScreeningPanel
Parent: Observation
Id: svs-observation-screening-panel
Title: "School Vision Screening Panel"
Description: "Panel observation containing right and left eye visual acuity measurements"
* ^status = #active
* ^experimental = false
* category 1..*
* code 1..1
* subject 1..1
* performer 1..*
* hasMember 2..2

Profile: SVSObservationRightEyeAcuity
Parent: Observation
Id: svs-observation-right-eye-acuity
Title: "Right Eye Visual Acuity"
Description: "Right eye visual acuity measurement as Snellen fraction using Ratio"
* ^status = #active
* ^experimental = false
* category 1..*
* code 1..1
* subject 1..1
* effectiveDateTime 1..1
* valueRatio 1..1
* bodySite 1..1

Profile: SVSObservationLeftEyeAcuity
Parent: Observation
Id: svs-observation-left-eye-acuity
Title: "Left Eye Visual Acuity"
Description: "Left eye visual acuity measurement as Snellen fraction using Ratio"
* ^status = #active
* ^experimental = false
* category 1..*
* code 1..1
* subject 1..1
* effectiveDateTime 1..1
* valueRatio 1..1
* bodySite 1..1

// ============================================================
// ServiceRequest + Task (Referral) Profiles - 360X Aligned
// ============================================================
Profile: SVSServiceRequestReferral
Parent: ServiceRequest
Id: svs-service-request-referral
Title: "School Vision Screening Referral"
Description: "Referral from school nurse to ophthalmology for vision assessment"
* ^status = #active
* ^experimental = false
* intent 1..1
* intent = #order
* category 1..1
* priority 1..1
* priority = #routine
* code 1..1
* subject 1..1
* encounter 0..1
* occurrenceDateTime 1..1
* authoredOn 1..1
* requester 1..1
* performer 1..1
* reasonCode 1..*

Profile: SVSTaskReferralTracking
Parent: Task
Id: svs-task-referral-tracking
Title: "School Vision Screening Referral Tracking"
Description: "Task for tracking referral workflow state"
* ^status = #active
* ^experimental = false
* intent 1..1
* intent = #order
* code 1..1
* for 1..1
* encounter 0..1
* authoredOn 1..1
* lastModified 1..1
* requester 1..1
* owner 1..1
* focus 1..1

// ============================================================
// Assessment Profiles
// ============================================================
Profile: SVSDiagnosticReportAssessment
Parent: DiagnosticReport
Id: svs-diagnostic-report-assessment
Title: "Ophthalmology Vision Assessment Report"
Description: "Complete ophthalmology assessment report for vision screening referral"
* ^status = #active
* ^experimental = false
* category 1..1
* code 1..1
* subject 1..1
* encounter 0..1
* effectiveDateTime 1..1
* issued 1..1
* performer 1..1
* resultsInterpreter 1..1
* basedOn 1..1
* result 1..*

Profile: SVSObservationDiagnosis
Parent: Observation
Id: svs-observation-diagnosis
Title: "Ophthalmology Diagnosis"
Description: "Diagnosis from ophthalmology assessment"
* ^status = #active
* ^experimental = false
* category 1..1
* code 1..1
* subject 1..1
* effectiveDateTime 1..1
* valueCodeableConcept 1..1

Profile: SVSObservationRefractionOD
Parent: Observation
Id: svs-observation-refraction-od
Title: "Right Eye Refraction"
Description: "Right eye refractive prescription"
* ^status = #active
* ^experimental = false
* category 1..1
* code 1..1
* subject 1..1
* effectiveDateTime 1..1
* valueQuantity 1..1
* bodySite 1..1

Profile: SVSObservationRefractionOS
Parent: Observation
Id: svs-observation-refraction-os
Title: "Left Eye Refraction"
Description: "Left eye refractive prescription"
* ^status = #active
* ^experimental = false
* category 1..1
* code 1..1
* subject 1..1
* effectiveDateTime 1..1
* valueQuantity 1..1
* bodySite 1..1

Profile: SVSCarePlanFollowUp
Parent: CarePlan
Id: svs-care-plan-follow-up
Title: "Ophthalmology Follow-up Plan"
Description: "Follow-up plan from ophthalmology assessment"
* ^status = #active
* ^experimental = false
* intent 1..1
* intent = #plan
* category 1..1
* subject 1..1
* encounter 0..1
* period 0..1
* activity 1..*

// ============================================================
// Communication (Accommodation Notice) Profile
// ============================================================
Profile: SVSCommunicationAccommodation
Parent: Communication
Id: svs-communication-accommodation
Title: "Teacher Accommodation Notice"
Description: "Notice from school nurse to teacher about classroom accommodation"
* ^status = #active
* ^experimental = false
* category 1..1
* subject 1..1
* sender 1..1
* recipient 0..*
* sent 1..1
* payload 1..1
  * contentString 1..1

// ============================================================
// Consent (Opt-Out) Profile
// ============================================================
Profile: SVSConsentOptOut
Parent: Consent
Id: svs-consent-opt-out
Title: "School Vision Screening Opt-Out Consent"
Description: "Annual opt-out consent for vision screening program"
* ^status = #active
* ^experimental = false
* scope 1..1
* category 1..1
* patient 1..1
* dateTime 1..1
* performer 1..1
* organization 1..1

// ============================================================
// DocumentReference (Primary Care Receipt) Profile
// ============================================================
Profile: SVSDocumentReferenceIP4
Parent: DocumentReference
Id: svs-document-reference-ip4
Title: "Primary Care Document Reference (IP-4)"
Description: "DocumentReference for each of the 6 IP-4 document types received by Primary Care"
* ^status = #active
* ^experimental = false
* type 1..1
* category 1..1
* subject 1..1
* date 1..1
* author 1..*
* custodian 1..1
* description 1..1
* content 1..1
  * attachment 1..1
    * contentType 0..1
    * url 1..1
* context 0..1
  * encounter 0..*
  * period 0..1

// ============================================================
// List (Primary Care Document Log) Profile
// ============================================================
Profile: SVSListPrimaryCareDocuments
Parent: List
Id: svs-list-primary-care-documents
Title: "Primary Care Vision Screening Document Log"
Description: "List of all vision screening related documents received by Primary Care for a child"
* ^status = #active
* ^experimental = false
* status 1..1
* mode 1..1
* title 1..1
* subject 1..1
* entry 0..*

// ============================================================
// Organization Profile
// ============================================================
Profile: SVSOrganization
Parent: Organization
Id: svs-organization
Title: "School Vision Screening Organization"
Description: "Organization profile for School Health Service, Ophthalmology Clinic, or Primary Care Practice"
* ^status = #active
* ^experimental = false
* identifier 1..*
* name 1..1
* type 0..1
* telecom 0..*
* address 0..*

// ============================================================
// QuestionnaireResponse Profile
// ============================================================
Profile: SVSQuestionnaireResponseScreening
Parent: QuestionnaireResponse
Id: svs-questionnaire-response-screening
Title: "School Vision Screening Questionnaire Response"
Description: "Screening form response captured by the nurse"
* ^status = #active
* ^experimental = false
* status 1..1
* subject 1..1
* encounter 0..1
* authored 1..1
* author 1..1
* item 1..*