# Mapping Table: School Vision Screening

**Step 4 — Mapping table: School Vision Screening**

This table maps every source field to its FHIR destination with transformation rules, binding strength, units, and handling for missing/ambiguous/invalid data. One row per rule.

---

## Child (Patient)

| Source Field | Source Format | FHIR Path | Transformation Rule | Binding Strength | Unit (UCUM) | Missing / Ambiguous / Invalid Handling |
|--------------|---------------|-----------|---------------------|------------------|-------------|----------------------------------------|
| Full name (family) | Structured (SIS) | `Patient.name[0].family` | Direct copy | Required (text) | — | Missing → cannot create Patient; flag to admin |
| Full name (given) | Structured (SIS) | `Patient.name[0].given` | Direct copy (array) | Required (text) | — | Missing → cannot create Patient; flag to admin |
| Date of birth | Structured (SIS) | `Patient.birthDate` | Direct copy (YYYY-MM-DD) | Required (date) | — | Missing → cannot screen; flag |
| School roll number | Structured (SIS) | `Patient.identifier[0].value` (system=urn:oid:1.2.3.4.5.school-roll) | Direct copy; type.code=SB | Required | — | Missing → cannot screen; flag |
| National health ID | Structured (SIS, optional) | `Patient.identifier[1].value` (system=http://terminology.hl7.org/CodeSystem/v2-0203, code=NI) | Direct copy if present; type.code=NI | Extensible | — | If missing → omit identifier; demographic matching used |
| Sex | Coded (SIS) | `Patient.gender` | Map SIS code → male/female/other/unknown | Required (valueSet) | — | Invalid code → "unknown"; log |
| Grade/class | Structured (SIS) | `Observation.note` (panel) / `Encounter.class` | Copy to ScreeningEvent gradeAtScreening | Extensible | — | Missing → omit |
| Address (street) | Structured (SIS) | `Patient.address[0].line` | Direct copy | Required | — | Missing → use school address; flag |
| Address (city) | Structured (SIS) | `Patient.address[0].city` | Direct copy | Required | — | Missing → flag |
| Address (postalCode) | Structured (SIS) | `Patient.address[0].postalCode` | Direct copy | Required | — | Missing → flag |
| Parent phone | Structured (SIS) | `Patient.telecom[0].value` (system=phone, use=home) | Direct copy | Required | — | Missing → flag |
| PIXm cross-reference ID | System (PIXm) | `Patient.identifier[2].value` (system=urn:ihe:pixm:cross-ref) | Direct copy if available | Extensible | — | Assigned by PIXm; if not available → omit |

---

## Parent/Guardian (RelatedPerson)

| Source Field | Source Format | FHIR Path | Transformation Rule | Binding Strength | Unit (UCUM) | Missing / Ambiguous / Invalid Handling |
|--------------|---------------|-----------|---------------------|------------------|-------------|----------------------------------------|
| Full name (family) | Structured (SIS) | `RelatedPerson.name[0].family` | Direct copy | Required | — | Missing → flag |
| Full name (given) | Structured (SIS) | `RelatedPerson.name[0].given` | Direct copy (array) | Required | — | Missing → flag |
| Relationship | Coded (SIS) | `RelatedPerson.relationship[0].coding` | Map SIS code → HL7 v2-0131 (MTH/FTH/GRD/etc.) | Extensible | — | Invalid → "GRD" (guardian) |
| Phone | Structured (SIS) | `RelatedPerson.telecom[0].value` (system=phone, use=home) | Direct copy | Required | — | Missing → use child's contact |
| Email | Structured (SIS) | `RelatedPerson.telecom[1].value` (system=email, use=home) | Direct copy | Extensible | — | Optional |
| Preferred contact method | Coded (SIS) | `RelatedPerson.communication[0].preferred` + language | Map to BCP-47 language code | Extensible | — | Default "es" |
| Opt-out status | Boolean (SIS) | `Consent.provision.type` (deny/permit) + `period` | True → deny; False → permit; statusHistory for changes | Required | — | Missing → assume permit (opted in) |

---

## School Nurse / ServiceLead (Practitioner + PractitionerRole)

| Source Field | Source Format | FHIR Path | Transformation Rule | Binding Strength | Unit (UCUM) | Missing / Ambiguous / Invalid Handling |
|--------------|---------------|-----------|---------------------|------------------|-------------|----------------------------------------|
| Full name (family) | Structured (HR) | `Practitioner.name[0].family` | Direct copy | Required | — | Missing → cannot act |
| Full name (given) | Structured (HR) | `Practitioner.name[0].given` | Direct copy | Required | — | Missing → cannot act |
| License number | Structured (HR) | `Practitioner.identifier[0].value` (system=license, type.code=PRN) | Direct copy | Required | — | Missing → cannot screen; flag HR |
| Employee ID | Structured (HR) | `Practitioner.identifier[1].value` (system=employee) | Direct copy | Extensible | — | Missing → flag |
| Assigned schools | Structured (HR) | `PractitionerRole.location` (Reference to Location) | Map to Location references | Extensible | — | Missing → flag |
| Role code | Fixed | `PractitionerRole.code[0].coding` | school-nurse: code=school-nurse, display=School Nurse; service-lead: code=service-lead, display=School Health Service Lead | Extensible | — | Fixed per role |
| Specialty | Fixed | `PractitionerRole.specialty[0].coding` | SNOMED 408480009 (School nursing) | Extensible | — | Fixed |
| Escalation contact | Reference (HR) | `PractitionerRole.extension(url=...escalationContact).valueReference` | Reference to ServiceLead PractitionerRole | Extensible | — | Missing → default to regional lead |

---

## ScreeningEvent (Observation Panel + Members)

| Source Field | Source Format | FHIR Path | Transformation Rule | Binding Strength | Unit (UCUM) | Missing / Ambiguous / Invalid Handling |
|--------------|---------------|-----------|---------------------|------------------|-------------|----------------------------------------|
| Screening date/time | Nurse entry | `Observation.effectiveDateTime` (panel + members) | Direct copy (ISO 8601) | Required | — | Missing → incomplete outcome |
| School year | Derived from date | `Observation.note[0].text` (panel) | Derive: e.g., "2026-2027" | Extensible | — | Auto-derived |
| Grade at screening | Copied from Child | `Observation.note[1].text` (panel) | Snapshot from Child at screening | Extensible | — | Auto-copied |
| Test used | Coded (nurse) | `Observation.note[2].text` (panel) / `Observation.method` | Map: Snellen 6m / Tumbling E / Lea symbols → local codes | Extensible | — | Missing → default Snellen; log |
| Right eye acuity | Structured (nurse) | `Observation.valueRatio` (member 1, LOINC 29474-1) | Parse Snellen fraction "6/12" → numerator.value=6, numerator.unit=m, denominator.value=12, denominator.unit=m; bodySite=363654007 (right eye) | Required | Ratio (UCUM: m/m) | Missing → incomplete outcome; reason required |
| Left eye acuity | Structured (nurse) | `Observation.valueRatio` (member 2, LOINC 29473-3) | Parse Snellen fraction; bodySite=363655008 (left eye) | Required | Ratio (UCUM: m/m) | Missing → incomplete outcome; reason required |
| Outcome | Derived + nurse | `Observation.interpretation` (panel) / `Observation.note[3].text` | Auto-derive: Pass if both ≥6/9; Refer if either ≤6/12 OR diff≥2 lines; Absent/Incomplete from nurse | Required (coded) | — | If acuity missing → Incomplete; if both present → auto-derive |
| Incomplete reason | Free text (nurse) | `Observation.note[4].text` (panel) | Direct copy | Extensible | — | Required if outcome=Incomplete |
| Acuity difference ≥2 lines | Derived | `Observation.note[5].text` (panel) | Calculate: lines difference ≥2 | Extensible | — | Auto-derived |
| Attempt number | Derived from counters | `Observation.note[6].text` (panel) | 1=initial, 2=re-screen | Required | — | Auto-derived |
| Is re-screen | Derived | `Observation.note[7].text` (panel) | attemptNumber > 1 | Required | — | Auto-derived |
| Screener ID | Auto-filled | `Observation.performer[0].reference` | Reference to Practitioner (nurse) | Required | — | Auto-filled from session |
| Child ID | Auto-filled | `Observation.subject.reference` | Reference to Patient (child) | Required | — | Auto-filled from selection |
| Referral indicated | Derived | `Observation.note[8].text` (panel) | Boolean from outcome | Extensible | — | Auto-derived |
| Panel code | Fixed | `Observation.code` (panel) | LOINC 83700-8 "Visual acuity screening panel" | Required | — | Fixed |
| Member 1 code | Fixed | `Observation.code` (member 1) | LOINC 29474-1 "Visual acuity right eye" | Required | — | Fixed |
| Member 2 code | Fixed | `Observation.code` (member 2) | LOINC 29473-3 "Visual acuity left eye" | Required | — | Fixed |
| Member 1 bodySite | Fixed | `Observation.bodySite` (member 1) | SNOMED 363654007 "Right eye" | Required | — | Fixed |
| Member 2 bodySite | Fixed | `Observation.bodySite` (member 2) | SNOMED 363655008 "Left eye" | Required | — | Fixed |

---

## Referral (ServiceRequest + Task) — 360X

| Source Field | Source Format | FHIR Path | Transformation Rule | Binding Strength | Unit (UCUM) | Missing / Ambiguous / Invalid Handling |
|--------------|---------------|-----------|---------------------|------------------|-------------|----------------------------------------|
| Referral ID | System UUID | `ServiceRequest.identifier[0].value` (system=referral-uuid) | Direct copy | Required | — | Auto-generated |
| 360X referral ID | External (360X) | `ServiceRequest.identifier[1].value` (system=urn:ihe:pcc:360x:referral-id) | Assigned by Recipient after PCC-55 | Extensible | — | Populated after PCC-55 |
| Child ID | Reference | `ServiceRequest.subject.reference` | Reference to Patient | Required | — | From ScreeningEvent |
| ScreeningEvent ID | Reference | `ServiceRequest.reasonReference[0].reference` | Reference to Observation panel | Required | — | From ScreeningEvent |
| Referral date | Nurse entry | `ServiceRequest.occurrenceDateTime` / `Task.authoredOn` | Direct copy (ISO 8601) | Required | — | Default to today |
| Reason | Derived + nurse | `ServiceRequest.reasonCode[0].coding` | Map: acuity≤6/12 → SNOMED 416070007 (Decreased visual acuity); diff≥2 lines → SNOMED 267083005 (Anisometropia); incomplete 2nd attempt → custom code | Extensible (SNOMED) | — | Auto-derived from ScreeningEvent |
| Acuity per eye | Copied from screening | `ServiceRequest.note[0].text` | Copy from ScreeningEvent | Extensible | — | Auto-copied |
| Test used | Copied from screening | `ServiceRequest.note[1].text` | Copy from ScreeningEvent | Extensible | — | Auto-copied |
| Screener ID | Reference | `ServiceRequest.requester.reference` | Reference to Practitioner | Required | — | Auto-filled |
| Parent decision | Coded (parent) | `Task.input[0].valueCodeableConcept` | Accept/Decline → coding | Extensible | — | Missing → pending; follow up at 4 weeks |
| Decline reason | Free text (parent) | `Task.input[1].valueString` | Direct copy | Extensible | — | Required if decline |
| Expected deadline | Derived | `Task.restriction.period.end` | referralDate + 4 weeks (ISO 8601) | Required | — | Auto-derived |
| Ophthalmology clinic | Reference (optional) | `ServiceRequest.performer[0].reference` | Reference to Organization | Extensible | — | If known |
| Replaces referral ID | Reference | `ServiceRequest.replaces[0].reference` | Reference to previous ServiceRequest | Extensible | — | Set on re-issue after timeout/rejection |
| Task status (initial) | Fixed | `Task.status` | "requested" | Required | — | Fixed |
| Task code | Fixed | `Task.code.coding` | LOINC/360X task code for referral tracking | Extensible | — | Fixed |
| Task focus | Reference | `Task.focus.reference` | Reference to ServiceRequest | Required | — | Auto-linked |

---

## OphthalmologyAssessment (DiagnosticReport + Observations + CarePlan)

| Source Field | Source Format | FHIR Path | Transformation Rule | Binding Strength | Unit (UCUM) | Missing / Ambiguous / Invalid Handling |
|--------------|---------------|-----------|---------------------|------------------|-------------|----------------------------------------|
| Assessment ID | System UUID | `DiagnosticReport.identifier[0].value` | Direct copy | Required | — | Auto-generated |
| Referral ID | Reference | `DiagnosticReport.basedOn[0].reference` | Reference to ServiceRequest | Required | — | From referral |
| Child ID | Reference | `DiagnosticReport.subject.reference` | Reference to Patient | Required | — | From referral |
| Assessment date | Clinician entry | `DiagnosticReport.effectiveDateTime` / `DiagnosticReport.issued` | Direct copy (ISO 8601) | Required | — | Required |
| Diagnosis | Coded (clinician) | `DiagnosticReport.conclusionCode[0].coding` + `Observation.valueCodeableConcept` (diagnosis member) | Map ICD-10/SNOMED → SNOMED CT (required binding) | Required (SNOMED) | — | Missing → incomplete; flag |
| Right eye diagnosis detail | Structured | `Observation.valueCodeableConcept` (diagnosis member) + `bodySite` (363654007) | SNOMED + bodySite right eye | Extensible | — | Optional |
| Left eye diagnosis detail | Structured | `Observation.valueCodeableConcept` (diagnosis member) + `bodySite` (363655008) | SNOMED + bodySite left eye | Extensible | — | Optional |
| Refraction OD (sphere) | Structured | `Observation.valueQuantity` + `component[0]` (LOINC 29468-3) | value=sphere, unit=D (diopter) | Required | D | If no glasses → omit |
| Refraction OD (cylinder) | Structured | `Observation.component[1]` (LOINC 29469-1) | value=cylinder, unit=D | Extensible | D | Optional |
| Refraction OD (axis) | Structured | `Observation.component[2]` (LOINC 29470-9) | value=axis, unit=deg | Extensible | deg | Optional |
| Refraction OS | Structured | Same pattern, bodySite=363655008 | Sphere/cylinder/axis for left eye | Extensible | D, deg | Optional |
| Follow-up plan (interval) | Structured | `CarePlan.activity.detail.scheduledPeriod` | Interval → period.start/end | Extensible | — | Required |
| Follow-up plan (treatment) | Structured | `CarePlan.activity.detail.code` | Patching → SNOMED 712743006 | Extensible | — | If applicable |
| Outcome | Coded (clinician) | `DiagnosticReport.conclusion` / `Observation.valueCodeableConcept` | Seen/DNA → text + code | Extensible | — | Required |
| Ophthalmologist ID | Auto-filled | `DiagnosticReport.performer[0].reference` / `resultsInterpreter[0].reference` | Reference to Practitioner | Required | — | Auto-filled |
| Clinic ID | Auto-filled | `DiagnosticReport.custodian.reference` | Reference to Organization | Required | — | Auto-filled |
| Report category | Fixed | `DiagnosticReport.category[0].coding` | HL7 v2-0074 OP "Ophthalmology" | Extensible | — | Fixed |
| Report code | Fixed | `DiagnosticReport.code.coding` | LOINC 28626-8 "Ophthalmology study" | Required | — | Fixed |

---

## PrimaryCareRecord Document Entries (List + DocumentReference)

| Source Field | Source Format | FHIR Path | Transformation Rule | Binding Strength | Unit (UCUM) | Missing / Ambiguous / Invalid Handling |
|--------------|---------------|-----------|---------------------|------------------|-------------|----------------------------------------|
| Document type | Coded (system) | `DocumentReference.type.coding` | Map 6 types → LOINC: pass/decline/missed=83700-8; assessment/dna/rejected/end-of-year=28626-8 | Required | — | Required per entry |
| Source referral ID | Reference | `DocumentReference.context.related[0].reference` | Reference to ServiceRequest | Extensible | — | Optional |
| Document reference | Reference | `DocumentReference.content[0].attachment.url` | URL to ScreeningEvent/Assessment resource (or Binary) | Required | — | Required |
| Receive date | System | `DocumentReference.date` | Direct copy (ISO 8601) | Required | — | Auto-set |
| Completeness flag | Derived | `DocumentReference.description` / `context` | Map: complete/partial/declined/missed | Extensible | — | Derived |
| Entered by | Reference | `DocumentReference.author[0].reference` | Reference to Practitioner/admin | Required | — | Auto-set |
| List entry | Reference | `List.entry[].item.reference` | Reference to DocumentReference | Required | — | Auto-linked |

---

## AccommodationNotice (Communication)

| Source Field | Source Format | FHIR Path | Transformation Rule | Binding Strength | Unit (UCUM) | Missing / Ambiguous / Invalid Handling |
|--------------|---------------|-----------|---------------------|------------------|-------------|----------------------------------------|
| Notice ID | System UUID | `Communication.identifier[0].value` | Direct copy | Required | — | Auto-generated |
| Child ID | Reference | `Communication.subject.reference` | Reference to Patient | Required | — | Required |
| Assessment ID | Reference | `Communication.basedOn[0].reference` | Reference to DiagnosticReport | Extensible | — | Required |
| Date issued | Nurse entry | `Communication.sent` | Direct copy (ISO 8601) | Required | — | Required |
| Accommodation type | Coded (derived) | `Communication.category[0].coding` + `payload[0].contentString` | Map: glasses/front-seat/both/other → text in payload | Extensible | — | Required |
| Accommodation detail | Free text (nurse) | `Communication.payload[0].contentString` | Direct copy | Extensible | — | Required |
| Valid until | Derived | `Communication.note[0].text` | Derived: end of school year or next assessment | Extensible | — | Auto-derived |
| Issued by | Reference | `Communication.sender.reference` | Reference to Practitioner (nurse) | Required | — | Required |
| Supersedes notice ID | Reference | `Communication.relatesTo[0].target.reference` (code=replaces) | Reference to previous Communication | Extensible | — | Optional |

---

## OptOutConsent (Consent)

| Source Field | Source Format | FHIR Path | Transformation Rule | Binding Strength | Unit (UCUM) | Missing / Ambiguous / Invalid Handling |
|--------------|---------------|-----------|---------------------|------------------|-------------|----------------------------------------|
| Consent ID | System | `Consent.identifier[0].value` | Direct copy | Required | — | Auto-generated |
| Child ID | Reference | `Consent.patient.reference` | Reference to Patient | Required | — | Required |
| School year | Structured | `Consent.provision[0].period` | Start=school-year-start, End=school-year-end | Required | — | Required |
| Status history | Repeating group | `Consent.provision[]` (multiple entries) | Each statusHistory entry → provision with period (type=deny/permit) | Required | — | Required |
| Current status | Derived | `Consent.provision[-1].type` (latest) | deny=opted-out, permit=opted-in | Required | — | Derived |
| Date recorded | System | `Consent.dateTime` | Direct copy (ISO 8601) | Required | — | Auto-set |
| Recorded by | Reference | `Consent.performer[0].reference` | Reference to Practitioner (admin) | Required | — | Required |
| Consent scope | Fixed | `Consent.scope.coding` | CodeSystem=consentscope, code=screening | Required | — | Fixed |
| Consent category | Fixed | `Consent.category[0].coding` | CodeSystem=consentcategorycodes, code=DENY | Required | — | Fixed |

---

## Unmapped Codes (Local Catalogues)

| Source Code | Source System | Reason Not Mapped | Local CodeSystem (if created) |
|-------------|---------------|-------------------|-------------------------------|
| Test used: Snellen 6m / Tumbling E / Lea symbols | Local | No standard LOINC/SNOMED for test method | `CodeSystem` URL: urn:oid:1.2.3.4.5.test-method |
| Screening outcome: Pass/Refer/Absent/Incomplete | Local | No standard valueSet | `CodeSystem` URL: urn:oid:1.2.3.4.5.screening-outcome |
| Accommodation type: glasses/front-seat/both/other | Local | No standard valueSet | `CodeSystem` URL: urn:oid:1.2.3.4.5.accommodation-type |
| Referral reason: acuity≤6/12 / diff≥2 lines / incomplete-2nd | Derived + local | Partially mapped to SNOMED | SNOMED for first two; custom for third |

---

## Terminology Versions (Pinned)

| Terminology | Version | Source |
|-------------|---------|--------|
| SNOMED CT | http://snomed.info/sct/21000325107/version/20260315 | International Edition, 2026-03-15 |
| LOINC | 2.76 | Terminology server |
| UCUM | 2.0.1 | R4 UCUM expansion |
| HL7 v2-0131 (Relationship) | R4 | HL7 |
| HL7 v2-0203 (Identifier Type) | R4 | HL7 |
| HL7 v2-0074 (Diagnostic Service) | R4 | HL7 |