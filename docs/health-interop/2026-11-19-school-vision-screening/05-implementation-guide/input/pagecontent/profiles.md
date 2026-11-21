# Profiles

---

## Profile Definitions

This page lists all profiles defined in this Implementation Guide. Each profile is derived from a FHIR R4 base resource and includes constraints, bindings, and extensions specific to the School Vision Screening workflow.

---

### Patient Profile: SVSPatient

**Base:** `Patient`  
**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-patient`

**Constraints:**
- `identifier` 1..* (school roll number required, national ID optional, PIXm cross-ref)
- `name` 1..* (official name required)
- `birthDate` 1..1
- `gender` 1..1
- `managingOrganization` 0..1 Reference(`SVSOrganization`)
- **Extensions:**
  - `gradeAtScreening` (string) — snapshot of grade at time of screening
  - `schoolYear` (string) — e.g., "2026-2027"

**Key Identifiers:**
| System | Type | Description |
|--------|------|-------------|
| `urn:oid:1.2.3.4.5.school-roll` | SB | School roll number (required) |
| `http://terminology.hl7.org/CodeSystem/v2-0203#NI` | NI | National health ID (optional) |
| `urn:ihe:pixm:cross-ref` | PIXM | PIXm cross-reference ID |

---

### RelatedPerson Profile: SVSRelatedPerson

**Base:** `RelatedPerson`  
**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-related-person`

**Constraints:**
- `patient` 1..1 Reference(`SVSPatient`)
- `relationship` 1..1 CodeableConcept from HL7 v2-0131 (required)
- `name` 1..*
- `telecom` 1..*
- **Extensions:**
  - `optOutStatus` (boolean) — current opt-out status
  - `optOutEffectiveFrom` (dateTime)
  - `optOutEffectiveTo` (dateTime)

---

### Practitioner / PractitionerRole Profiles

#### SVSPractitioner
**Base:** `Practitioner`  
**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-practitioner`

**Constraints:**
- `identifier` 1..* (employee ID, license number required)
- `name` 1..*
- `telecom` 0..*

#### SVSPractitionerRole
**Base:** `PractitionerRole`  
**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-practitioner-role`

**Constraints:**
- `practitioner` 1..1 Reference(`SVSPractitioner`)
- `organization` 1..1 Reference(`SVSOrganization`)
- `code` 1..1 from `SVSPractitionerRole` ValueSet (school-nurse, service-lead)
- `specialty` 0..* SNOMED 408480009 "School nursing"
- **Extension:** `escalationContact` 0..1 Reference(`SVSPractitionerRole`) — for ServiceLead escalation

---

### Observation Profiles (ScreeningEvent)

#### SVSObservationScreeningPanel
**Base:** `Observation`  
**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-screening-panel`

**Constraints:**
- `status` = final | amended | corrected
- `category` = vital-signs
- `code` = LOINC 83700-8 "Visual acuity screening panel"
- `subject` 1..1 Reference(`SVSPatient`)
- `performer` 1..* Reference(`SVSPractitionerRole`)
- `hasMember` 2..2 Reference(`SVSObservationRightEyeAcuity` | `SVSObservationLeftEyeAcuity`)
- **Notes (metadata):**
  - `test-used` (string)
  - `outcome` (CodeableConcept from `SVSScreeningOutcome`)
  - `attempt-number` (integer)
  - `is-re-screen` (boolean)
  - `referral-indicated` (boolean)
  - `acuity-diff-two-lines` (boolean)

#### SVSObservationRightEyeAcuity / SVSObservationLeftEyeAcuity
**Base:** `Observation`  
**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-right-eye-acuity` / `svs-observation-left-eye-acuity`

**Key Constraint:** `value[x]` = **Ratio** (not Quantity)
- `valueRatio.numerator` Quantity (value in meters, UCUM "m")
- `valueRatio.denominator` Quantity (value in meters, UCUM "m")
- `bodySite` = SNOMED 363654007 (Right eye) / 363655008 (Left eye)
- `interpretation` from `SVSAcuityInterpretation` (A=Abnormal ≤6/12, N=Normal ≥6/9)

---

### Referral Profiles (360X Aligned)

#### SVSServiceRequestReferral
**Base:** `ServiceRequest`  
**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-service-request-referral`

**Constraints:**
- `status` = draft | active | on-hold | revoked | completed | entered-in-error | unknown
- `intent` = order
- `category` = referral
- `priority` = routine
- `code` = SNOMED 307924000 "Referral to ophthalmologist"
- `reasonCode` from `SVSReferralReason`
- `reasonReference` 1..1 Reference(`SVSObservationScreeningPanel`)
- **Extensions:**
  - `expectedDeadline` (dateTime) — referral date + 4 weeks
  - `parentDecision` (CodeableConcept: accept/decline)
  - `declineReason` (string)
- `replaces` 0..* Reference(`SVSServiceRequestReferral`) — for re-issued referrals

#### SVSTaskReferralTracking
**Base:** `Task`  
**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-task-referral-tracking`

**Constraints:**
- `status` = draft | requested | received | accepted | rejected | ready | cancelled | in-progress | on-hold | failed | completed | entered-in-error
- `code` = referral
- `focus` 1..1 Reference(`SVSServiceRequestReferral`)
- `restriction.period.end` 0..1 dateTime — 4-week deadline
- `input` referral-detail → Reference(`SVSServiceRequestReferral`)
- `output` assessment-report → Reference(`SVSDiagnosticReportAssessment`)

---

### Assessment Profiles

#### SVSDiagnosticReportAssessment
**Base:** `DiagnosticReport`  
**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-diagnostic-report-assessment`

**Constraints:**
- `status` = registered | partial | preliminary | final | amended | corrected | appended | cancelled | entered-in-error | unknown
- `category` = OP (Ophthalmology)
- `code` = LOINC 28626-8 "Ophthalmology study"
- `basedOn` 1..1 Reference(`SVSServiceRequestReferral`)
- `result` 1..* Reference(`SVSObservationDiagnosis` | `SVSObservationRefractionOD` | `SVSObservationRefractionOS`)

#### SVSObservationDiagnosis
**Base:** `Observation`  
**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-diagnosis`

**Constraints:**
- `category` = diagnosis
- `code` from SNOMED (required binding)
- `value[x]` = CodeableConcept from SNOMED (required)
- `bodySite` 0..1 SNOMED (363654007 Right eye / 363655008 Left eye)

#### SVSObservationRefractionOD / SVSObservationRefractionOS
**Base:** `Observation`  
**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-refraction-od` / `svs-observation-refraction-os`

**Constraints:**
- `category` = exam
- `valueQuantity` = Quantity (diopters, UCUM "D")
- `bodySite` = Right eye (363654007) / Left eye (363655008)
- `component` 3..3:
  - Sphere (LOINC 29468-3) — Quantity (D)
  - Cylinder (LOINC 29469-1) — Quantity (D)
  - Axis (LOINC 29470-9) — Quantity (deg)

#### SVSCarePlanFollowUp
**Base:** `CarePlan`  
**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-care-plan-follow-up`

**Constraints:**
- `intent` = plan
- `category` = assess-plan
- `activity` 1..* with `detail.kind` = ServiceRequest | Task
- `detail.scheduledPeriod` for review interval

---

### Communication Profile: SVSCommunicationAccommodation

**Base:** `Communication`  
**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-communication-accommodation`

**Constraints:**
- `category` = instruction
- `sender` 1..1 Reference(`SVSPractitionerRole`) — School Nurse
- `recipient` 1..* Reference(`PractitionerRole` | `RelatedPerson`) — Teacher
- `payload.contentString` 1..1 string
- **Extensions:**
  - `accommodationType` from `SVSAccommodationType`
  - `validUntil` (date)
  - `assessmentReference` Reference(`SVSDiagnosticReportAssessment`)
- `relatesTo` code=replaces → previous Communication

---

### Consent Profile: SVSConsentOptOut

**Base:** `Consent`  
**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-consent-opt-out`

**Constraints:**
- `scope` = screening
- `category` = DENY
- `provision` 1..* (multiple for statusHistory)
  - `type` = deny | permit
  - `period` with start/end
  - `action` = vision-screening
- Multiple `provision` entries model mid-year status changes (opt-out → opt-in → opt-out)

---

### DocumentReference Profile: SVSDocumentReferenceIP4

**Base:** `DocumentReference`  
**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-document-reference-ip4`

**Constraints:**
- `type` from LOINC per documentType:
  - screening-pass/decline/missed/end-of-year → LOINC 83700-8
  - assessment-full → LOINC 28626-8
  - referral-dna/rejected → LOINC 11506-3 "Referral note"
- `content.attachment.contentType` = application/fhir+json
- `content.attachment.url` → URL to FHIR resource
- `context.related` 0..1 Reference(`SVSServiceRequestReferral`) — sourceReferralId

---

### List Profile: SVSListPrimaryCareDocuments

**Base:** `List`  
**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-list-primary-care-documents`

**Constraints:**
- `mode` = working
- `entry` 0..* Reference(`SVSDocumentReferenceIP4`)

---

### Organization Profile: SVSOrganization

**Base:** `Organization`  
**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-organization`

**Constraints:**
- `identifier` 1..*
- `name` 1..1
- `type` 0..1 CodeableConcept
- `telecom` 0..*
- `address` 0..*

---

## Profile Inheritance Summary

```
SVSPatient → Patient
SVSRelatedPerson → RelatedPerson
SVSPractitioner → Practitioner
SVSPractitionerRole → PractitionerRole
SVSObservationScreeningPanel → Observation
  SVSObservationRightEyeAcuity → Observation
  SVSObservationLeftEyeAcuity → Observation
SVSServiceRequestReferral → ServiceRequest
SVSTaskReferralTracking → Task
SVSDiagnosticReportAssessment → DiagnosticReport
  SVSObservationDiagnosis → Observation
  SVSObservationRefractionOD → Observation
  SVSObservationRefractionOS → Observation
SVSCarePlanFollowUp → CarePlan
SVSCommunicationAccommodation → Communication
SVSConsentOptOut → Consent
SVSDocumentReferenceIP4 → DocumentReference
SVSListPrimaryCareDocuments → List
SVSOrganization → Organization
SVSPractitioner → Practitioner
SVSPractitionerRole → PractitionerRole
```

---

## Validation

All profiles validate against FHIR R4 base resources with:
- Required bindings respected (SNOMED CT, LOINC, UCUM)
- Extensions only where no base field carries the meaning
- Cardinalities constrained per workflow requirements
- Examples provided for each profile (see [Examples](examples.html))