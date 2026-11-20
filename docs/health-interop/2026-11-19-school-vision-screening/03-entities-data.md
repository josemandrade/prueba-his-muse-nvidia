# Entities and Data: School Vision Screening

**Step 3 — Entities and data: School Vision Screening**

Based on the validated use case spec (Step 1) and BPMN model (Step 2), the following entities are involved in the school vision screening process. Each entity has a single authoritative owner, defined fields with sources, identifiers, and lifecycle states.

---

## Entity Table

| Entity | Definition | Owning System | Key Fields (Source) | Identifiers | Lifecycle States | Who Changes State |
|--------|------------|---------------|---------------------|-------------|------------------|-------------------|
| **Child** | Student enrolled in school, subject of vision screening | School Information System (SIS) | • Full name (structured, SIS)<br>• Date of birth (structured, SIS)<br>• School roll number (structured, SIS)<br>• Grade and class (structured, SIS)<br>• Sex (coded, SIS)<br>• Address (structured, SIS)<br>• Parent/guardian contact (structured, SIS) | • School roll number (local)<br>• National health ID / NHS number (if available, optional)<br>• PIXm cross-reference ID (for interop) | **Active** (enrolled) → **Transferred** (left school) → **Archived** | School admin (enrollment)<br>School nurse (screening context) |
| **Parent/Guardian** | Legal guardian of child, receives notifications, consents (opt-out) | School Information System (SIS) | • Full name (structured, SIS)<br>• Relationship to child (coded, SIS)<br>• Phone (structured, SIS)<br>• Email (structured, SIS)<br>• Preferred contact method (coded, SIS)<br>• Opt-out consent status (boolean, SIS) | • SIS guardian ID<br>• National ID (if linked) | **Active** → **Inactive** (child transferred/aged out) | School admin |
| **School Nurse** | Health professional conducting screening, managing referrals | School Health Service HR / Directory | • Full name (structured, HR)<br>• Professional license number (structured, HR)<br>• Contact (phone/email) (structured, HR)<br>• Assigned schools (structured, HR)<br>• Escalation contact (reference to ServiceLead) (reference, HR) | • Employee ID<br>• Professional license number (authoritative) | **Active** → **Inactive** (left service) | HR admin |
| **ServiceLead** | School health program lead / coordinator; receives escalations from nurses | School Health Service HR / Directory | • Full name (structured, HR)<br>• Professional license number (structured, HR)<br>• Contact (phone/email) (structured, HR)<br>• Responsible region/schools (structured, HR) | • Employee ID<br>• Professional license number (authoritative) | **Active** → **Inactive** (left service) | HR admin |
| **ScreeningEvent** | Single visual acuity screening encounter for a child | School Health Service (screening app / paper record) | • Screening date/time (structured, nurse entry)<br>• School year (structured, e.g., "2026-2027") (derived from date, copied from Child at screening)<br>• Grade at screening (structured, copied from Child at screening) (structured)<br>• Test used (coded: Snellen 6m / Tumbling E / Lea symbols) (coded, nurse entry)<br>• Right eye acuity (structured, e.g., "6/12") (structured, nurse entry)<br>• Left eye acuity (structured, e.g., "6/9") (structured, nurse entry)<br>• Outcome (coded: Pass / Refer / Absent / Incomplete) (derived + nurse entry)<br>• Incomplete reason (free text, if applicable) (free text, nurse entry)<br>• Attempt number (integer: 1=initial, 2=re-screen) (derived from attempt counters) (derived)<br>• Is re-screen (boolean) (derived: attemptNumber > 1) (derived)<br>• Screener ID (reference to School Nurse) (reference, auto-filled)<br>• Child ID (reference to Child) (reference, auto-filled)<br>• Referral indicated (boolean, derived from acuity) (derived)<br>• Acuity difference ≥2 lines (boolean, derived) (derived) | • Screening event ID (local UUID)<br>• Child ID (foreign key)<br>• School roll number (for traceability) | **Draft** (in progress) → **Recorded** (complete) → **Amended** (corrected) → **Archived** (end of year) | Nurse (creates, records, amends)<br>System (derives outcome, archives, sets attemptNumber) |
| **Referral** | Request from school nurse to ophthalmology for assessment | School Health Service (referral tracking) | • Referral ID (local UUID)<br>• Child ID (reference)<br>• ScreeningEvent ID (reference)<br>• Referral date (structured, nurse entry)<br>• Reason (coded: acuity ≤6/12 / acuity diff ≥2 lines / incomplete 2nd attempt) (coded, derived + nurse entry)<br>• Acuity per eye at referral (structured, copied from ScreeningEvent) (structured)<br>• Test used (coded, copied) (coded)<br>• Screener ID (reference)<br>• Parent decision (coded: Accept / Decline) (coded, parent response)<br>• Decline reason (free text, if declined) (free text, parent)<br>• Expected turnaround deadline (date, derived: referral date + 4 weeks) (derived)<br>• Ophthalmology clinic ID (reference, if known) (reference)<br>• 360X referral ID (if electronic) (external identifier)<br>• Replaces referral ID (reference to previous Referral, optional) (reference, system-assigned on re-issue after timeout/rejection) | • Referral ID (local UUID)<br>• 360X referral ID (for interop)<br>• Child ID (foreign key) | **Draft** → **Sent** (to parent/ophthalmology) → **Accepted** (by ophthalmology) / **Rejected** (by ophthalmology) / **Cancelled** (timeout, 360X PCC-58) → **Completed** (assessment received) / **Closed-DNS** (did not attend, 2nd DNA) / **Closed-Decline** (parent declined) / **Closed-Rejected** (referral rejected) | Nurse (creates, sends, cancels, closes)<br>Parent (accepts/declines)<br>Ophthalmology (accepts/rejects)<br>System (auto-cancel on timeout, sets replacesReferralId on re-issue) |
| **OphthalmologyAssessment** | Clinical assessment by ophthalmologist resulting from referral | Ophthalmology Clinic EHR | • Assessment ID (local UUID)<br>• Referral ID (reference)<br>• Child ID (reference)<br>• Assessment date (structured, clinician entry)<br>• Diagnosis (coded: ICD-10 / SNOMED: myopia, hyperopia, astigmatism, amblyopia, other) (coded, clinician entry)<br>• Right eye diagnosis detail (structured)<br>• Left eye diagnosis detail (structured)<br>• Refractive prescription (structured: sphere, cylinder, axis per eye) (structured, clinician entry)<br>• Follow-up plan (structured: review interval, treatment e.g., patching) (structured, clinician entry)<br>• Outcome (coded: Seen / DNA) (coded, clinician entry)<br>• Ophthalmologist ID (reference) (reference, auto-filled)<br>• Clinic ID (reference) (reference) | • Assessment ID (local UUID)<br>• Referral ID (foreign key)<br>• 360X referral ID (for linkage) | **Draft** → **Finalized** (validated by clinician) → **Amended** (addendum/correction) → **Transmitted** (to school/primary care) | Ophthalmologist (creates, finalizes, amends)<br>Clinic admin (transmits) |
| **PrimaryCareRecord** | Child's health record in primary care receiving screening/assessment data | Primary Care EHR | • Record ID (local)<br>• Child ID (reference, matched via PIXm/PDQm/PMIR)<br>• Document entries (repeating):<br>  - Document type (coded: screening-pass / screening-decline / screening-missed / assessment-full / referral-dna / referral-rejected / end-of-year-missed) (coded)<br>  - Source referral ID (reference to Referral, optional) (reference)<br>  - Received date (structured, system)<br>  - Document reference (reference to ScreeningEvent / OphthalmologyAssessment / summary) (reference)<br>  - Data completeness flag (coded: complete / partial / declined / missed) (derived)<br>  - Entered by (reference to clinician/admin) (reference) | • Primary care patient ID (local)<br>• PIXm/PDQm cross-reference | **Open** (child registered) → **Updated** (new data received) → **Closed** (transferred/deceased) | Primary care clinician/admin (enters, updates) |
| **AccommodationNotice** | Notice to teacher about classroom accommodation needed | School Health Service (nurse generates) | • Notice ID (local UUID)<br>• Child ID (reference)<br>• Assessment ID (reference, source)<br>• Date issued (structured, nurse entry)<br>• Accommodation type (coded: glasses needed / front seat / both / other) (coded, derived from assessment)<br>• Accommodation detail (free text, e.g., "mild myopia OD, glasses prescribed") (free text, nurse entry)<br>• Valid until (date, derived: end of school year or next assessment) (derived)<br>• Issued by (reference to School Nurse) (reference)<br>• Supersedes notice ID (reference to previous AccommodationNotice, optional) (reference, system-assigned on supersede) | • Notice ID (local)<br>• Child ID (foreign key) | **Draft** → **Issued** (sent to teacher) → **Superseded** (new notice) → **Expired** (end of validity) | Nurse (creates, issues, supersedes)<br>System (auto-expires) |
| **OptOutConsent** | Annual opt-out consent for screening program; revocable mid-year | School Information System (SIS) | • Consent ID (local)<br>• Child ID (reference)<br>• School year (structured, e.g., "2026-2027") (structured)<br>• Status history (repeating):<br>  - Status (boolean: true = opted out) (structured, parent response)<br>  - Effective from (date/time) (structured)<br>  - Effective to (date/time, null = current) (structured)<br>• Current status (derived: latest statusHistory entry) (derived)<br>• Date recorded (structured, system)<br>• Recorded by (reference to school admin) (reference) | • Consent ID (local)<br>• Child ID + School year (composite key) | **Pending** (start of year) → **Recorded** (parent responded) → **Updated** (status changed mid-year) → **Archived** (end of year) | Parent (responds, changes mind)<br>School admin (records) |

---

## Field Sources and Types Summary

| Entity | Field | Source | Type | Required? |
|--------|-------|--------|------|-----------|
| Child | Full name | SIS | Structured | Yes |
| Child | Date of birth | SIS | Structured | Yes |
| Child | School roll number | SIS | Structured | Yes |
| Child | Grade/class | SIS | Structured | Yes |
| Child | Sex | SIS | Coded | Yes |
| Child | Address | SIS | Structured | Yes |
| Child | Parent contact | SIS | Structured | Yes |
| Parent/Guardian | Full name | SIS | Structured | Yes |
| Parent/Guardian | Relationship | SIS | Coded | Yes |
| Parent/Guardian | Phone | SIS | Structured | Yes |
| Parent/Guardian | Email | SIS | Structured | Optional |
| Parent/Guardian | Preferred contact | SIS | Coded | Yes |
| Parent/Guardian | Opt-out status | SIS | Boolean | Yes |
| School Nurse | Full name | HR | Structured | Yes |
| School Nurse | License number | HR | Structured | Yes |
| School Nurse | Contact | HR | Structured | Yes |
| School Nurse | Assigned schools | HR | Structured | Yes |
| School Nurse | Escalation contact | HR | Reference | Yes |
| ServiceLead | Full name | HR | Structured | Yes |
| ServiceLead | License number | HR | Structured | Yes |
| ServiceLead | Contact | HR | Structured | Yes |
| ServiceLead | Responsible region/schools | HR | Structured | Yes |
| ScreeningEvent | Screening date/time | Nurse entry | Structured | Yes |
| ScreeningEvent | School year | Derived from date | Structured | Yes |
| ScreeningEvent | Grade at screening | Copied from Child | Structured | Yes |
| ScreeningEvent | Test used | Nurse entry | Coded | Yes |
| ScreeningEvent | Right eye acuity | Nurse entry | Structured | Yes |
| ScreeningEvent | Left eye acuity | Nurse entry | Structured | Yes |
| ScreeningEvent | Outcome | Derived + nurse | Coded | Yes |
| ScreeningEvent | Incomplete reason | Nurse entry | Free text | If incomplete |
| ScreeningEvent | Attempt number | Derived from counters | Integer | Yes |
| ScreeningEvent | Is re-screen | Derived | Boolean | Yes |
| ScreeningEvent | Screener ID | Auto-filled | Reference | Yes |
| ScreeningEvent | Child ID | Auto-filled | Reference | Yes |
| ScreeningEvent | Referral indicated | Derived | Boolean | Yes |
| ScreeningEvent | Acuity diff ≥2 lines | Derived | Boolean | Yes |
| Referral | Referral ID | System | UUID | Yes |
| Referral | Child ID | Reference | Reference | Yes |
| Referral | ScreeningEvent ID | Reference | Reference | Yes |
| Referral | Referral date | Nurse entry | Structured | Yes |
| Referral | Reason | Derived + nurse | Coded | Yes |
| Referral | Acuity per eye | Copied from screening | Structured | Yes |
| Referral | Test used | Copied from screening | Coded | Yes |
| Referral | Screener ID | Reference | Reference | Yes |
| Referral | Parent decision | Parent response | Coded | Yes |
| Referral | Decline reason | Parent response | Free text | If declined |
| Referral | Expected deadline | Derived | Date | Yes |
| Referral | Ophthalmology clinic | Nurse entry | Reference | Optional |
| Referral | 360X referral ID | 360X transaction | External ID | If electronic |
| Referral | Replaces referral ID | System | Reference | Optional |
| OphthalmologyAssessment | Assessment ID | Clinic EHR | UUID | Yes |
| OphthalmologyAssessment | Referral ID | Reference | Reference | Yes |
| OphthalmologyAssessment | Child ID | Reference | Reference | Yes |
| OphthalmologyAssessment | Assessment date | Clinician entry | Structured | Yes |
| OphthalmologyAssessment | Diagnosis | Clinician entry | Coded (ICD-10/SNOMED) | Yes |
| OphthalmologyAssessment | Rx detail per eye | Clinician entry | Structured | If glasses |
| OphthalmologyAssessment | Follow-up plan | Clinician entry | Structured | Yes |
| OphthalmologyAssessment | Outcome | Clinician entry | Coded | Yes |
| OphthalmologyAssessment | Ophthalmologist ID | Auto-filled | Reference | Yes |
| OphthalmologyAssessment | Clinic ID | Auto-filled | Reference | Yes |
| PrimaryCareRecord | Record ID | Primary care EHR | Local ID | Yes |
| PrimaryCareRecord | Child ID | Matched via PIXm/PDQm | Reference | Yes |
| PrimaryCareRecord | Document type | System | Coded | Yes (per entry) |
| PrimaryCareRecord | Source referral ID | Reference | Reference | Optional |
| PrimaryCareRecord | Document reference | Reference | Reference | Yes (per entry) |
| PrimaryCareRecord | Receive date | System | Structured | Yes (per entry) |
| PrimaryCareRecord | Completeness flag | Derived | Coded | Yes (per entry) |
| PrimaryCareRecord | Entered by | Reference | Reference | Yes (per entry) |
| AccommodationNotice | Notice ID | System | UUID | Yes |
| AccommodationNotice | Child ID | Reference | Reference | Yes |
| AccommodationNotice | Assessment ID | Reference | Reference | Yes |
| AccommodationNotice | Date issued | Nurse entry | Structured | Yes |
| AccommodationNotice | Accommodation type | Derived from assessment | Coded | Yes |
| AccommodationNotice | Accommodation detail | Nurse entry | Free text | Yes |
| AccommodationNotice | Valid until | Derived | Date | Yes |
| AccommodationNotice | Issued by | Reference | Reference | Yes |
| AccommodationNotice | Supersedes notice ID | System | Reference | Optional |
| OptOutConsent | Consent ID | System | Local ID | Yes |
| OptOutConsent | Child ID | Reference | Reference | Yes |
| OptOutConsent | School year | System | Structured | Yes |
| OptOutConsent | Status (current) | Derived | Boolean | Yes |
| OptOutConsent | Status history entries | Parent response | Repeating group | Yes |
| OptOutConsent | Status history - status | Parent response | Boolean | Yes (per entry) |
| OptOutConsent | Status history - effectiveFrom | System | DateTime | Yes (per entry) |
| OptOutConsent | Status history - effectiveTo | System | DateTime | Optional (per entry) |
| OptOutConsent | Date recorded | System | Structured | Yes |
| OptOutConsent | Recorded by | Reference | Reference | Yes |

---

## Identifier Strategy

| Identifier | Scope | Used By | Notes |
|------------|-------|---------|-------|
| School roll number | School district | School, Nurse, SIS | Primary key for child in school context |
| National health ID / NHS number | National health system | Primary care, Ophthalmology, PIXm | **Optional** — used when available; not assumed present for school health service |
| PIXm cross-reference ID | Interop (360X, MHD) | All systems | Links local IDs across domains; **primary matching strategy is demographic (name, DOB, address)**; national ID used as supplementary identifier when available |
| Screening event UUID | School Health Service | Nurse, Referral, Primary care | Local, unique per screening encounter |
| Referral UUID | School Health Service | Nurse, Ophthalmology, 360X | Local, unique per referral |
| 360X referral ID | 360X affinity domain | Ophthalmology, Nurse, Primary care | Assigned by 360X Referral Recipient |
| Assessment UUID | Ophthalmology Clinic | Clinic, Nurse, Primary care | Local to clinic EHR |
| Primary care patient ID | Primary care practice | Primary care | Local to practice |

**Matching Strategy**: PIXm queries use demographic matching (family name, given name, date of birth, gender, address) as the primary strategy. National health ID is included as an identifier when available but is not required for matching. This ensures portability across jurisdictions where school health services may not have access to national health identifiers.

---

## Data Quality Rules

| Entity | Missing Field Handling | Duplicate Detection | Out-of-Date Handling | Correction Rule |
|--------|------------------------|---------------------|----------------------|-----------------|
| Child | Required fields missing → cannot screen; flag to school admin | School roll number unique in SIS; national ID unique in PIXm | Grade/class updated annually by SIS | SIS correction → propagates to screening record via next sync |
| Parent/Guardian | Contact missing → use alternative; flag to nurse | Guardian ID unique per child in SIS | Contact changes → parent notifies school | SIS update |
| School Nurse | License missing → cannot screen; flag to HR | Employee ID + license unique | Assignment changes → HR updates | HR update |
| ServiceLead | License missing → cannot escalate; flag to HR | Employee ID + license unique | Assignment changes → HR updates | HR update |
| ScreeningEvent | Acuity missing → incomplete outcome; reason required | Child + date + screener composite key (one screening per child per day) | N/A (point in time) | Amended status + new ScreeningEvent with correction reason; original retained |
| Referral | Parent decision missing → pending; follow up at 4 weeks | Referral UUID unique; 360X ID unique | Deadline tracked; 4-week timer | Cancel (PCC-58) + new referral if re-issued; original closed; replacesReferralId set on new |
| OphthalmologyAssessment | Diagnosis missing → incomplete; flag to clinician | Assessment UUID unique | Follow-up plan dates tracked | Amended (addendum) + re-transmit; original retained |
| PrimaryCareRecord | Screening/assessment missing → flag completeness | Patient ID unique in practice | N/A (cumulative record) | Entered-in-error + replacement; re-notify if clinical impact |
| AccommodationNotice | Accommodation type missing → cannot issue | Child + notice ID unique | Valid until date tracked; auto-expire | Supersede with new notice; old marked superseded; supersedesNoticeId set on new |
| OptOutConsent | Status missing → assume opted in (safe default) | Child + school year composite key | Status history tracks all changes | New statusHistory entry with effectiveFrom; previous entry gets effectiveTo |

---

## Lifecycle State Transitions (Detail)

### Referral States (360X-aligned)
```
Draft → Sent (PCC-55 Submit) 
  → Accepted (PCC-56 Accept) → Completed (assessment received, PCC-61 Retrieve Report)
  → Rejected (PCC-56 Reject) → Closed-Rejected (nurse closes, notifies)
  → Cancelled (PCC-58 Close, timeout) → Sent (new referral, fresh lifecycle; replacesReferralId set)
  → Completed → Closed-DNS (2nd DNA, nurse closes)
  → Closed-Decline (parent declined at outset)
```

**Closure Reason carried in Referral.state**: The Referral entity's `state` field explicitly captures why the referral ended: `Completed` (assessment received), `Closed-DNS` (2nd DNA), `Closed-Decline` (parent declined), `Closed-Rejected` (referral rejected), `Cancelled` (timeout). The `OphthalmologyAssessment` references its `Referral`; the referral's closure reason is traversable via that reference — no separate `referralClosureReason` field needed on Assessment.

### ScreeningEvent States
```
Draft (nurse entering) → Recorded (complete) 
  → Amended (correction entered) 
  → Archived (end of school year, read-only)
```

### OphthalmologyAssessment States
```
Draft (clinician entering) → Finalized (validated) 
  → Amended (addendum/correction) 
  → Transmitted (to school/primary care via 360X/MHD)
```

---

## Cross-Entity Relationships

| From Entity | To Entity | Relationship | Cardinality | Notes |
|-------------|-----------|--------------|-------------|-------|
| Child | ScreeningEvent | Has screening | 1 : 0..N (per year) | One screening per year typically; re-screens create new events |
| Child | Referral | Has referral | 1 : 0..N | Multiple referrals possible (re-referral, direct referral) |
| Child | OptOutConsent | Has consent | 1 : 1 per year | Annual opt-out with mid-year changes tracked in statusHistory |
| Child | AccommodationNotice | Has accommodation | 1 : 0..N | New notice per assessment |
| ScreeningEvent | Referral | Triggers | 1 : 0..1 | Only if outcome = Refer or Incomplete (2nd attempt) |
| Referral | OphthalmologyAssessment | Results in | 1 : 0..1 | Assessment received closes referral |
| Referral | PrimaryCareRecord | Notifies | 1 : 1..N | Each IP-4 message flow creates a document entry |
| OphthalmologyAssessment | AccommodationNotice | Generates | 1 : 1 | Nurse creates from assessment |
| OphthalmologyAssessment | PrimaryCareRecord | Updates | 1 : 1 | Full assessment sent as document entry |
| Referral | Referral (self) | Replaces | 0..1 : 0..1 | `replacesReferralId` links new referral to cancelled one |
| AccommodationNotice | AccommodationNotice (self) | Supersedes | 0..1 : 0..1 | `supersedesNoticeId` chains updates |
| School Nurse | ServiceLead | Escalates to | N : 1 | Nurse.escalationContact references ServiceLead |

---

## Entities for FHIR Mapping (Preview)

| Entity | Likely FHIR Resource(s) | Notes |
|--------|-------------------------|-------|
| Child | `Patient` | Core demographics; `identifier` for school roll number, national ID (when available), PIXm cross-ref |
| Parent/Guardian | `RelatedPerson` | Relationship to child; contact info; `patient` reference to Child |
| School Nurse | `Practitioner` + `PractitionerRole` | Role: school nurse; organization: school health service |
| ServiceLead | `Practitioner` + `PractitionerRole` | Role: service lead; organization: school health service |
| ScreeningEvent | `Observation` panel + member Observations | **Panel Observation** (code: visual acuity screening panel, e.g., LOINC 83700-8) with **two member Observations** via `hasMember`:<br>1. Right eye acuity (code: LOINC 29474-1, `valueQuantity` Snellen fraction, `bodySite` right eye SNOMED 363654007)<br>2. Left eye acuity (code: LOINC 29473-3, `valueQuantity` Snellen fraction, `bodySite` left eye SNOMED 363655008)<br>Panel also carries `derivedFrom` → ScreeningEvent metadata (date, test used, outcome, attemptNumber) |
| Referral | `ServiceRequest` (360X) + `Task` (tracking) | 360X uses ServiceRequest + Task for workflow; `ServiceRequest.replaces` = replacesReferralId |
| OphthalmologyAssessment | `DiagnosticReport` + `Observation` (diagnosis, refraction) + `CarePlan` (follow-up) | EC-Summary/GEE content mapping; `DiagnosticReport.basedOn` → ServiceRequest (referral) |
| PrimaryCareRecord | `Patient` (record holder) + `Composition` (summary) + `List` (documents) | Receives documents via MHD; each IP-4 receipt = DocumentReference entry in List |
| AccommodationNotice | `Communication` | Nurse → Teacher; category: clinical accommodation; `Communication.sent` = date issued |
| OptOutConsent | `Consent` | Scope: screening; provision: deny; `Consent.provision.period` = school year; statusHistory mapped to `Consent.provision` updates |

---

## Validation Checklist

- [x] Every entity has a name, definition, and owning system
- [x] Every entity's fields and sources listed; name clashes settled (e.g., "Child" not "Patient" in school context)
- [x] Identifiers listed with scope and ownership; matching strategy documented
- [x] Lifecycle states defined with who changes each
- [x] Data quality rules for missing/duplicate/out-of-date/correction
- [x] Cross-entity relationships mapped including self-references (replaces, supersedes)
- [x] Table uses same names as BPMN model (Child, School Nurse, ServiceLead, ScreeningEvent, Referral, OphthalmologyAssessment, Parent/Guardian, PrimaryCareRecord, AccommodationNotice, OptOutConsent)
- [x] Expert review findings C1-C10 resolved per user Q1-Q7 answers
- [x] FHIR mapping preview specifies acuity as two member Observations under a panel with hasMember, valueQuantity (Snellen), bodySite (right/left eye)