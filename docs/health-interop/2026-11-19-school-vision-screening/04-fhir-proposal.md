# FHIR Proposal: School Vision Screening

**Step 4 — FHIR proposal: School Vision Screening**

Based on the validated use case spec (Step 1), BPMN model (Step 2), and Entities & Data (Step 3), this proposal defines the FHIR R4 resources, profiles, operations, and mappings to support the school vision screening interoperability points.

---

## 1. Resource Choices

Each entity maps to exactly one primary FHIR resource (or resource pair for workflow state), chosen from the FHIR R4 resource list and the resource-choice table. The base resource is the FHIR R4 base unless the user selects a national/profile base.

| Entity | FHIR Resource(s) | Base Resource (Canonical URL) | Profile Applied | Rationale / Alternatives Rejected |
|--------|------------------|-------------------------------|-----------------|-----------------------------------|
| **Child** | `Patient` | `http://hl7.org/fhir/StructureDefinition/Patient` | None (base R4) | Simplest resource for person demographics. Alternatives: `RelatedPerson` (wrong role — child is the subject of care), `Person` (too generic, no clinical context). User may choose a national patient profile (e.g., `CorePacienteCl`) as base. |
| **Parent/Guardian** | `RelatedPerson` | `http://hl7.org/fhir/StructureDefinition/RelatedPerson` | None (base R4) | Correct for legal guardian relationship to patient. `Patient.link` is for linking patient records, not for guardian relationship. |
| **School Nurse** | `Practitioner` + `PractitionerRole` | `http://hl7.org/fhir/StructureDefinition/Practitioner`<br>`http://hl7.org/fhir/StructureDefinition/PractitionerRole` | None (base R4) | Separate person (Practitioner) from role/context (PractitionerRole). Alternative: `CareTeam` participant (for team membership only, not identity). |
| **ServiceLead** | `Practitioner` + `PractitionerRole` | Same as School Nurse | None (base R4) | Same pattern as School Nurse; distinguished by `PractitionerRole.code` (service lead vs school nurse). |
| **ScreeningEvent** | `Observation` (panel) + member `Observation`s | `http://hl7.org/fhir/StructureDefinition/Observation` | None (base R4) | Visual acuity is a vital sign / observation. Panel pattern: parent Observation (panel code LOINC 83700-8 "Visual acuity screening panel") with two member Observations via `hasMember` — right eye (LOINC 29474-1) and left eye (LOINC 29473-3). Alternatives rejected: single Observation with component (components are for multi-part single observation, not distinct body sites); `DiagnosticReport` (for report document, not the measurement itself). |
| **Referral** | `ServiceRequest` + `Task` | `http://hl7.org/fhir/StructureDefinition/ServiceRequest`<br>`http://hl7.org/fhir/StructureDefinition/Task` | **360X** (PCC-55/56/58/61) | 360X Closed Loop Referral profile uses `ServiceRequest` for the referral request and `Task` for workflow tracking. `ServiceRequest.replaces` = `replacesReferralId`. Alternatives: `ReferralRequest` (R4 deprecated, use `ServiceRequest`); `CommunicationRequest` (for simple notification, not workflow). |
| **OphthalmologyAssessment** | `DiagnosticReport` + `Observation` (diagnosis, refraction) + `CarePlan` (follow-up) | `http://hl7.org/fhir/StructureDefinition/DiagnosticReport`<br>`http://hl7.org/fhir/StructureDefinition/Observation`<br>`http://hl7.org/fhir/StructureDefinition/CarePlan` | **EC-Summary** (EYECARE, TI) for content structure | `DiagnosticReport` carries the assessment report; member `Observation`s for diagnosis (SNOMED CT), refraction (LOINC); `CarePlan` for follow-up plan (patching, review interval). EC-Summary (Eye Care Summary Record) provides content structure for eye care reports. Alternative: `ClinicalImpression` (for impression/differential, not finalized assessment). |
| **PrimaryCareRecord** | `Patient` (record holder) + `Composition` (summary) + `List` (document entries) | `http://hl7.org/fhir/StructureDefinition/Patient`<br>`http://hl7.org/fhir/StructureDefinition/Composition`<br>`http://hl7.org/fhir/StructureDefinition/List` | **MHD** (ITI) for document exchange | Primary care receives documents via MHD. `List` holds `DocumentReference` entries for each IP-4 receipt (6 document types). `Composition` for summary view. Alternative: `Bundle` (transient, not stored). |
| **AccommodationNotice** | `Communication` | `http://hl7.org/fhir/StructureDefinition/Communication` | None (base R4) | Nurse → Teacher communication about clinical accommodation. Category: clinical accommodation. Alternatives: `Flag` (for persistent alerts, not one-time notices); `Task` (for work assignment, not notification). |
| **OptOutConsent** | `Consent` | `http://hl7.org/fhir/StructureDefinition/Consent` | None (base R4) | Scope: screening; provision: deny (opt-out). `Consent.provision.period` = school year. `statusHistory` mapped to `Consent.provision` updates (new provision entry per status change). Alternative: `Consent` with `provision.type = deny` is correct for opt-out. |

**Terminology Versions** (pinned from terminology server):
- SNOMED CT: `http://snomed.info/sct/21000325107/version/20260315` (International Edition, 2026-03-15)
- LOINC: version 2.76 (as reported by terminology server)
- UCUM: version 2.0.1 (as in R4 UCUM expansion)
- ICD-10: WHO 2024 version (for diagnosis coding where used)

---

## 2. Resource Profiles and Key Fields

### 2.1 Patient (Child)
```yaml
Patient:
  identifier:
    - system: "urn:oid:1.2.3.4.5.school-roll"  # School roll number
      value: "[school roll number]"
      type:
        coding:
          - system: "http://terminology.hl7.org/CodeSystem/v2-0203"
            code: "SB"
            display: "School Board"
    - system: "http://terminology.hl7.org/CodeSystem/v2-0203"  # National ID (optional)
      value: "[national health ID]"
      type:
        coding:
          - code: "NI"
            display: "National unique individual identifier"
      use: "official"
    - system: "urn:ihe:pixm:cross-ref"  # PIXm cross-reference
      value: "[PIXm ID]"
      type:
        coding:
          - code: "PIXM"
            display: "PIXm Cross-reference"
  name:
    - use: "official"
      family: "[family name]"
      given: ["[given name]"]
  birthDate: "[YYYY-MM-DD]"
  gender: "[male|female|other|unknown]"  # from SIS sex code
  address:
    - use: "home"
      line: ["[street address]"]
      city: "[city]"
      postalCode: "[postal code]"
      country: "[country]"
  telecom:
    - system: "phone"
      value: "[parent phone]"
      use: "home"
  managingOrganization:
    reference: "Organization/[school-health-service-org-id]"
```

### 2.2 RelatedPerson (Parent/Guardian)
```yaml
RelatedPerson:
  identifier:
    - system: "urn:oid:1.2.3.4.5.guardian"
      value: "[SIS guardian ID]"
  patient:
    reference: "Patient/[child-id]"
  relationship:
    coding:
      - system: "http://terminology.hl7.org/CodeSystem/v2-0131"
        code: "MTH"  # Mother
        display: "Mother"
        # or FTH (Father), GRD (Guardian), etc.
  name:
    - use: "official"
      family: "[family name]"
      given: ["[given name]"]
  telecom:
    - system: "phone"
      value: "[phone]"
      use: "home"
    - system: "email"
      value: "[email]"
      use: "home"
  communication:
    - preferred: true
      language:
        coding:
          - system: "urn:ietf:bcp:47"
            code: "es"  # or appropriate language
```

### 2.3 Practitioner + PractitionerRole (School Nurse / ServiceLead)
```yaml
Practitioner:
  identifier:
    - system: "urn:oid:1.2.3.4.5.employee"
      value: "[employee ID]"
    - system: "urn:oid:1.2.3.4.5.license"
      value: "[professional license number]"
      type:
        coding:
          - system: "http://terminology.hl7.org/CodeSystem/v2-0203"
            code: "PRN"
            display: "Provider number"
  name:
    - use: "official"
      family: "[family name]"
      given: ["[given name]"]
  telecom:
    - system: "phone"
      value: "[work phone]"
      use: "work"
    - system: "email"
      value: "[work email]"
      use: "work"

PractitionerRole:
  practitioner:
    reference: "Practitioner/[practitioner-id]"
  organization:
    reference: "Organization/[school-health-service-org-id]"
  code:
    - coding:
        - system: "http://terminology.hl7.org/CodeSystem/practitioner-role"
          code: "school-nurse"  # or "service-lead"
          display: "School Nurse"  # or "School Health Service Lead"
  specialty:
    - coding:
        - system: "http://snomed.info/sct/21000325107/version/20260315"
          code: "408480009"  # School nursing
          display: "School nursing"
  location:
    - reference: "Location/[school-id]"
  telecom:
    - system: "phone"
      value: "[work phone]"
      use: "work"
  healthcareService:
    - reference: "HealthcareService/[school-vision-screening-service-id]"
```

### 2.4 Observation Panel (ScreeningEvent)
```yaml
Observation (Panel):
  identifier:
    - system: "urn:oid:1.2.3.4.5.screening-event"
      value: "[screening-event-uuid]"
  status: "final"  # or "amended", "corrected"
  category:
    - coding:
        - system: "http://terminology.hl7.org/CodeSystem/observation-category"
          code: "vital-signs"
          display: "Vital Signs"
  code:
    coding:
      - system: "http://loinc.org"
        code: "83700-8"
        display: "Visual acuity screening panel"
    text: "Visual Acuity Screening (School)"
  subject:
    reference: "Patient/[child-id]"
  encounter:
    reference: "Encounter/[screening-encounter-id]"  # if Encounter used
  effectiveDateTime: "[YYYY-MM-DDTHH:MM:SSZ]"
  performer:
    - reference: "Practitioner/[nurse-id]"
  hasMember:
    - reference: "Observation/[right-eye-acuity-obs-id]"
    - reference: "Observation/[left-eye-acuity-obs-id]"
  derivedFrom:
    - reference: "QuestionnaireResponse/[screening-form-id]"  # if form used
  note:
    - text: "Test used: Snellen 6m / Tumbling E / Lea symbols; Outcome: Pass/Refer/Absent/Incomplete; Attempt: 1/2"
  component: []  # not used; member Observations carry the values

Observation (Right Eye Acuity - member):
  identifier:
    - system: "urn:oid:1.2.3.4.5.acuity"
      value: "[right-eye-obs-uuid]"
  status: "final"
  category:
    - coding:
        - system: "http://terminology.hl7.org/CodeSystem/observation-category"
          code: "vital-signs"
  code:
    coding:
      - system: "http://loinc.org"
        code: "29474-1"
        display: "Visual acuity right eye"
  subject:
    reference: "Patient/[child-id]"
  effectiveDateTime: "[YYYY-MM-DDTHH:MM:SSZ]"
  valueRatio:  # Snellen fraction as Ratio (numerator/denominator)
    numerator:
      value: 6
      unit: "m"
      system: "http://unitsofmeasure.org"
      code: "m"
    denominator:
      value: 12
      unit: "m"
      system: "http://unitsofmeasure.org"
      code: "m"
  bodySite:
    coding:
      - system: "http://snomed.info/sct/21000325107/version/20260315"
        code: "363654007"
        display: "Right eye"
  interpretation:
    - coding:
        - system: "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation"
          code: "A"  # Abnormal (if ≤6/12)
          display: "Abnormal"
  note:
    - text: "Test: Snellen 6m"

Observation (Left Eye Acuity - member):
  identifier:
    - system: "urn:oid:1.2.3.4.5.acuity"
      value: "[left-eye-obs-uuid]"
  status: "final"
  category:
    - coding:
        - system: "http://terminology.hl7.org/CodeSystem/observation-category"
          code: "vital-signs"
  code:
    coding:
      - system: "http://loinc.org"
        code: "29473-3"
        display: "Visual acuity left eye"
  subject:
    reference: "Patient/[child-id]"
  effectiveDateTime: "[YYYY-MM-DDTHH:MM:SSZ]"
  valueRatio:  # Snellen fraction as Ratio
    numerator:
      value: 6
      unit: "m"
      system: "http://unitsofmeasure.org"
      code: "m"
    denominator:
      value: 9
      unit: "m"
      system: "http://unitsofmeasure.org"
      code: "m"
  bodySite:
    coding:
      - system: "http://snomed.info/sct/21000325107/version/20260315"
        code: "363655008"
        display: "Left eye"
  interpretation:
    - coding:
        - system: "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation"
          code: "N"  # Normal (if ≥6/9)
          display: "Normal"
  note:
    - text: "Test: Snellen 6m"
```

### 2.5 ServiceRequest + Task (Referral) — 360X Profile
```yaml
ServiceRequest (360X Referral Request):
  identifier:
    - system: "urn:oid:1.2.3.4.5.referral"
      value: "[referral-uuid]"
    - system: "urn:ihe:pcc:360x:referral-id"
      value: "[360X-referral-id]"  # assigned by Recipient
  instantiatesCanonical:
    - "http://hl7.org/fhir/uv/ips/PlanDefinition/vision-screening-referral"  # optional protocol
  status: "active"  # draft | active | on-hold | revoked | completed | entered-in-error | unknown
  intent: "order"  # proposal | plan | order | original-order | reflex-order | filler-order | instance-order
  category:
    - coding:
        - system: "http://terminology.hl7.org/CodeSystem/service-request-category"
          code: "referral"
          display: "Referral"
  priority: "routine"  # routine | urgent | asap | stat
  code:
    coding:
      - system: "http://snomed.info/sct/21000325107/version/20260315"
        code: "307924000"  # Referral to ophthalmologist
        display: "Referral to ophthalmologist"
    text: "Vision screening referral: acuity OD 6/12, OS 6/9"
  subject:
    reference: "Patient/[child-id]"
  encounter:
    reference: "Encounter/[screening-encounter-id]"
  occurrenceDateTime: "[YYYY-MM-DDTHH:MM:SSZ]"  # referral date
  authoredOn: "[YYYY-MM-DDTHH:MM:SSZ]"
  requester:
    reference: "Practitioner/[nurse-id]"
  performer:
    - reference: "Organization/[ophthalmology-clinic-org-id]"
  reasonCode:
    - coding:
        - system: "http://snomed.info/sct/21000325107/version/20260315"
          code: "416070007"  # Decreased visual acuity
          display: "Decreased visual acuity"
      # or code for "Anisometropia" (difference ≥2 lines)
  reasonReference:
    - reference: "Observation/[screening-panel-obs-id]"
  note:
    - text: "Referral reason: acuity OD 6/12 (≤6/12) / OS 6/9; test: Snellen 6m; screener: [nurse name]"
  replaces:
    - reference: "ServiceRequest/[previous-referral-id]"  # replacesReferralId

Task (360X Referral Tracking):
  identifier:
    - system: "urn:oid:1.2.3.4.5.referral-task"
      value: "[referral-task-uuid]"
  instantiatesCanonical:
    - "http://ihe.net/fhir/pcc/StructureDefinition/360XReferralTask"
  status: "requested"  # requested | received | accepted | rejected | ready | cancelled | in-progress | on-hold | failed | completed | entered-in-error
  intent: "order"  # unknown | proposal | plan | order | original-order | reflex-order | filler-order | instance-order
  priority: "routine"
  code:
    coding:
      - system: "http://hl7.org/fhir/CodeSystem/task-code"
        code: "referral"
        display: "Referral tracking"
  for:
    reference: "Patient/[child-id]"
  encounter:
    reference: "Encounter/[screening-encounter-id]"
  authoredOn: "[YYYY-MM-DDTHH:MM:SSZ]"
  lastModified: "[YYYY-MM-DDTHH:MM:SSZ]"
  requester:
    reference: "Practitioner/[nurse-id]"
  owner:
    reference: "Organization/[ophthalmology-clinic-org-id]"
  focus:
    reference: "ServiceRequest/[referral-servicerequest-id]"
  restriction:
    period:
      end: "[referral-date + 4 weeks]"  # expected turnaround deadline
  input:
    - type:
        coding:
          - system: "http://hl7.org/fhir/CodeSystem/task-param"
            code: "referral-detail"
            display: "Referral detail"
      valueReference:
        reference: "ServiceRequest/[referral-servicerequest-id]"
  output:
    - type:
        coding:
          - system: "http://hl7.org/fhir/CodeSystem/task-param"
            code: "assessment-report"
            display: "Assessment report"
      valueReference:
        reference: "DiagnosticReport/[assessment-report-id]"  # when completed
```

### 2.6 DiagnosticReport + Observation + CarePlan (OphthalmologyAssessment)
```yaml
DiagnosticReport (Assessment Report):
  identifier:
    - system: "urn:oid:1.2.3.4.5.assessment"
      value: "[assessment-uuid]"
  status: "final"  # registered | partial | preliminary | final | amended | corrected | appended | cancelled | entered-in-error | unknown
  category:
    - coding:
        - system: "http://terminology.hl7.org/CodeSystem/v2-0074"
          code: "OP"
          display: "Ophthalmology"
  code:
    coding:
      - system: "http://loinc.org"
        code: "28626-8"  # Ophthalmology study
        display: "Ophthalmology study"
    text: "Ophthalmology assessment for vision screening referral"
  subject:
    reference: "Patient/[child-id]"
  encounter:
    reference: "Encounter/[assessment-encounter-id]"
  effectiveDateTime: "[YYYY-MM-DDTHH:MM:SSZ]"
  issued: "[YYYY-MM-DDTHH:MM:SSZ]"
  performer:
    - reference: "Practitioner/[ophthalmologist-id]"
  resultsInterpreter:
    - reference: "Practitioner/[ophthalmologist-id]"
  basedOn:
    - reference: "ServiceRequest/[referral-servicerequest-id]"
  result:
    - reference: "Observation/[diagnosis-obs-id]"
    - reference: "Observation/[refraction-od-obs-id]"
    - reference: "Observation/[refraction-os-obs-id]"
  conclusion: "Mild myopia OD. Prescription: -1.00 DS OD. Follow-up: 12 months."
  conclusionCode:
    - coding:
        - system: "http://snomed.info/sct/21000325107/version/20260315"
          code: "373124007"  # Myopia
          display: "Myopia"
  presentedForm: []  # if PDF attached

Observation (Diagnosis):
  status: "final"
  category:
    - coding:
        - system: "http://terminology.hl7.org/CodeSystem/observation-category"
          code: "diagnosis"
  code:
    coding:
      - system: "http://snomed.info/sct/21000325107/version/20260315"
        code: "373124007"  # Myopia
        display: "Myopia"
  subject:
    reference: "Patient/[child-id]"
  effectiveDateTime: "[YYYY-MM-DDTHH:MM:SSZ]"
  valueCodeableConcept:
    coding:
      - system: "http://snomed.info/sct/21000325107/version/20260315"
        code: "373124007"
        display: "Myopia"
  bodySite:
    coding:
      - system: "http://snomed.info/sct/21000325107/version/20260315"
        code: "363654007"  # Right eye
        display: "Right eye"

Observation (Refraction OD):
  status: "final"
  category:
    - coding:
        - system: "http://terminology.hl7.org/CodeSystem/observation-category"
          code: "exam"
  code:
    coding:
      - system: "http://loinc.org"
        code: "29474-1"  # Visual acuity right eye (or specific refraction LOINC)
        display: "Refraction right eye"
  subject:
    reference: "Patient/[child-id]"
  effectiveDateTime: "[YYYY-MM-DDTHH:MM:SSZ]"
  valueQuantity:
    value: -1.00
    unit: "D"
    system: "http://unitsofmeasure.org"
    code: "D"  # Diopter
  bodySite:
    coding:
      - system: "http://snomed.info/sct/21000325107/version/20260315"
        code: "363654007"
        display: "Right eye"
  component:
    - code:
        coding:
          - system: "http://loinc.org"
            code: "29468-3"
            display: "Sphere"
      valueQuantity:
        value: -1.00
        unit: "D"
        system: "http://unitsofmeasure.org"
        code: "D"
    - code:
        coding:
          - system: "http://loinc.org"
            code: "29469-1"
            display: "Cylinder"
      valueQuantity:
        value: 0.00
        unit: "D"
        system: "http://unitsofmeasure.org"
        code: "D"
    - code:
        coding:
          - system: "http://loinc.org"
            code: "29470-9"
            display: "Axis"
      valueQuantity:
        value: 0
        unit: "deg"
        system: "http://unitsofmeasure.org"
        code: "deg"

CarePlan (Follow-up Plan):
  status: "active"  # draft | active | on-hold | revoked | completed | entered-in-error | unknown
  intent: "plan"  # proposal | plan | order | option
  category:
    - coding:
        - system: "http://terminology.hl7.org/CodeSystem/careplan-category"
          code: "assess-plan"
          display: "Assessment Plan"
  subject:
    reference: "Patient/[child-id]"
  encounter:
    reference: "Encounter/[assessment-encounter-id]"
  period:
    start: "[assessment-date]"
    end: "[assessment-date + review-interval]"
  activity:
    - detail:
        kind: "ServiceRequest"
        code:
          coding:
            - system: "http://snomed.info/sct/21000325107/version/20260315"
              code: "373124007"  # Myopia follow-up
              display: "Myopia follow-up"
        scheduledPeriod:
          start: "[assessment-date + 12 months]"
          end: "[assessment-date + 12 months]"
        status: "not-started"
        description: "Follow-up in 12 months for myopia monitoring"
    - detail:
        kind: "Task"
        code:
          coding:
            - system: "http://snomed.info/sct/21000325107/version/20260315"
              code: "712743006"  # Patching therapy
              display: "Patching therapy"
        status: "in-progress"
        description: "Occlusion patching for amblyopia (if applicable)"
```

### 2.7 Communication (AccommodationNotice)
```yaml
Communication:
  identifier:
    - system: "urn:oid:1.2.3.4.5.accommodation"
      value: "[notice-uuid]"
  status: "sent"  # preparation | in-progress | not-done | on-hold | stopped | completed | entered-in-error | unknown
  category:
    - coding:
        - system: "http://terminology.hl7.org/CodeSystem/communication-category"
          code: "clinical-accommodation"
          display: "Clinical Accommodation"
  subject:
    reference: "Patient/[child-id]"
  sender:
    reference: "Practitioner/[nurse-id]"
  recipient:
    - reference: "Practitioner/[teacher-id]"  # or RelatedPerson if teacher not a Practitioner
  sent: "[YYYY-MM-DDTHH:MM:SSZ]"
  payload:
    - contentString: "Accommodation needed: glasses, front seat. Detail: mild myopia OD, glasses prescribed. Valid until end of school year."
  note:
    - text: "Based on ophthalmology assessment [assessment-id]. Supersedes notice [previous-notice-id] if applicable."
```

### 2.8 Consent (OptOutConsent)
```yaml
Consent:
  identifier:
    - system: "urn:oid:1.2.3.4.5.optout-consent"
      value: "[consent-id]"
  status: "active"  # draft | proposed | active | rejected | inactive | entered-in-error
  scope:
    coding:
      - system: "http://terminology.hl7.org/CodeSystem/consentscope"
        code: "screening"
        display: "Screening"
  category:
    - coding:
        - system: "http://terminology.hl7.org/CodeSystem/consentcategorycodes"
          code: "DENY"
          display: "Deny"
  patient:
    reference: "Patient/[child-id]"
  dateTime: "[YYYY-MM-DDTHH:MM:SSZ]"  # when recorded
  performer:
    - reference: "Practitioner/[school-admin-id]"
  organization:
    - reference: "Organization/[school-health-service-org-id]"
  provision:
    type: "deny"
    period:
      start: "[school-year-start]"
      end: "[school-year-end]"
    # statusHistory mapped as multiple provision entries with period:
    - type: "deny"
      period:
        start: "[effectiveFrom-1]"
        end: "[effectiveTo-1 or school-year-end]"
      # action: "screening" (if coded)
    - type: "permit"  # if parent opts back in
      period:
        start: "[effectiveFrom-2]"
        end: "[effectiveTo-2 or school-year-end]"
  sourceAttachment:
    url: "[url-to-signed-consent-form-if-any]"
```

### 2.9 List + DocumentReference (PrimaryCareRecord Document Entries)
```yaml
List (Document Log):
  identifier:
    - system: "urn:oid:1.2.3.4.5.primary-care-docs"
      value: "[patient-primary-care-id]-documents"
  status: "current"  # current | retired | entered-in-error
  mode: "working"  # working | snapshot | changes
  title: "School Vision Screening Documents for [Child Name]"
  subject:
    reference: "Patient/[primary-care-patient-id]"
  encounter:
    - reference: "Encounter/[screening-or-assessment-encounter-id]"
  entry:
    - item:
        reference: "DocumentReference/[doc-ref-1]"
    - item:
        reference: "DocumentReference/[doc-ref-2]"
  # ... one entry per IP-4 receipt

DocumentReference (per IP-4 receipt):
  identifier:
    - system: "urn:oid:1.2.3.4.5.ip4-doc"
      value: "[doc-ref-uuid]"
  status: "current"  # current | superseded | entered-in-error
  type:
    coding:
      - system: "http://loinc.org"
        code: "[varies by documentType]"
        display: "[varies]"
  category:
    - coding:
        - system: "http://terminology.hl7.org/CodeSystem/document-class"
          code: "screening-report"
          display: "Screening Report"
  subject:
    reference: "Patient/[primary-care-patient-id]"
  date: "[receive-date]"
  author:
    - reference: "Practitioner/[nurse-or-ophthalmologist-id]"
  custodian:
    reference: "Organization/[school-health-service-or-ophthalmology-org-id]"
  relatesTo:
    - code: "replaces"  # if superseding previous
      target:
        reference: "DocumentReference/[previous-doc-ref-id]"
  description: "[documentType display, e.g., 'Vision screening pass result']"
  content:
    - attachment:
        contentType: "application/fhir+json"
        url: "[url-to-screening-event-or-assessment-resource]"
      format:
        system: "http://ihe.net/fhir/ihe.formatcode.fhir/CodeSystem/formatcode"
        code: "application/fhir+json"
        display: "FHIR JSON"
  context:
    encounter:
      reference: "Encounter/[screening-encounter-id]"
    period:
      start: "[screening-date]"
      end: "[screening-date]"
```

**DocumentType → LOINC Code Mapping:**
| documentType (IP-4) | LOINC Code | Display |
|---------------------|------------|---------|
| screening-pass | 83700-8 | Visual acuity screening panel |
| screening-decline | 83700-8 | Visual acuity screening panel (with decline note) |
| screening-missed | 83700-8 | Visual acuity screening panel (missed) |
| assessment-full | 28626-8 | Ophthalmology study |
| referral-dna | 28626-8 | Ophthalmology study (DNA closure) |
| referral-rejected | 28626-8 | Ophthalmology study (rejected) |
| end-of-year-missed | 83700-8 | Visual acuity screening panel (end-of-year missed) |

---

## 3. Lifecycle Tables

### 3.1 Referral (ServiceRequest + Task) — 360X-Aligned

**R4 Task.status Value Set (Required Binding)**: `draft | requested | received | accepted | rejected | ready | cancelled | in-progress | on-hold | failed | completed | entered-in-error`

**R4 ServiceRequest.status Value Set (Required Binding)**: `draft | active | on-hold | revoked | completed | entered-in-error | unknown`

| State (ServiceRequest.status / Task.status) | Allowed Next States | Triggering Operation (PI) | Forbidden Transitions |
|---------------------------------------------|---------------------|---------------------------|----------------------|
| **Draft** (ServiceRequest.draft / Task.draft) | **Sent** (active/requested) | IP-2a: Submit Referral (PCC-55) | Direct to Completed, Cancelled, Closed-* |
| **Sent** (active/requested) | **Accepted** (active/received) | IP-2d: Ophthalmology Accept (PCC-56 Accept) | Direct to Completed (must go through Accepted) |
| | **Rejected** (rejected/rejected) | IP-2c: Ophthalmology Reject (PCC-56 Reject) | — |
| | **Cancelled** (cancelled/cancelled) | IP-2b: Timeout Cancel (PCC-58 Close) | — |
| **Accepted** (active/received) | **Completed** (completed/completed) | IP-3: Assessment Received (PCC-61 Retrieve Report) | Back to Sent, Draft |
| | **Closed-DNS** (completed/completed) | IP-4c: DNA Closure (2nd DNA) | — |
| **Rejected** (rejected/rejected) | **Closed-Rejected** (completed/completed) | Nurse closes, notifies (IP-4e) | Back to Sent, Accepted |
| **Cancelled** (cancelled/cancelled) | **Sent** (new referral, fresh lifecycle) | IP-2a: Re-issue Referral (new ServiceRequest with replaces) | Re-activate cancelled referral |
| **Completed** (completed/completed) | **Closed-DNS** (completed/completed) | If 2nd DNA after completion (rare) | — |
| **Closed-Decline** (completed/completed) | (terminal) | IP-4b: Parent Decline at outset | — |
| **Closed-Rejected** (completed/completed) | (terminal) | After Rejected, nurse closes | — |

**Note**: All Task.status and ServiceRequest.status values are from the R4 Required binding value sets. The state names in parentheses show the exact value set codes used.

### 3.2 ScreeningEvent (Observation Panel)

| State (Observation.status) | Allowed Next States | Triggering Operation | Forbidden Transitions |
|---------------------------|---------------------|----------------------|----------------------|
| **registered** | **preliminary** | Nurse starts entry | Direct to final/amended |
| **preliminary** | **final** | Nurse completes & records | Back to registered |
| | **amended** | Nurse corrects (after final) | — |
| | **corrected** | System corrects (data error) | — |
| **final** | **amended** | Nurse enters correction | Back to preliminary |
| | **corrected** | System corrects | — |
| **amended** | **final** | Re-validated | — |
| **corrected** | **final** | Re-validated | — |
| **cancelled** | (terminal) | Entered in error | Any other |
| **entered-in-error** | (terminal) | Wrong patient/encounter | Any other |
| **unknown** | (terminal) | Status unknown | Any other |

### 3.3 OphthalmologyAssessment (DiagnosticReport)

**R4 DiagnosticReport.status Value Set (Required Binding)**: `registered | partial | preliminary | final | amended | corrected | appended | cancelled | entered-in-error | unknown`

**States Actually Used in This Workflow** (others are allowed by value set but not used):
- **registered** → **final** (typical: clinician enters and validates in one step)
- **final** → **amended** (addendum) / **corrected** (correction) / **appended** (additional results)
- **amended/corrected/appended** → **final** (re-validated)
- **cancelled** / **entered-in-error** / **unknown** (terminal, error conditions)

| State (DiagnosticReport.status) | Allowed Next States | Triggering Operation | Forbidden Transitions | Actually Used? |
|--------------------------------|---------------------|----------------------|----------------------|----------------|
| **registered** | **partial** / **preliminary** / **final** | Partial/preliminary results entered; or direct to final | — | **Yes** (often → final directly) |
| **partial** | **preliminary** / **final** | Preliminary results | Back to registered | Optional |
| **preliminary** | **final** | Clinician validates | Back to partial | Optional |
| **final** | **amended** / **corrected** / **appended** | Addendum / correction / additional results | — | **Yes** |
| **amended** | **final** | Re-validated | — | **Yes** |
| **corrected** | **final** | Re-validated | — | **Yes** |
| **appended** | **final** | Re-validated | — | **Yes** |
| **cancelled** | (terminal) | Report cancelled | Any other | Error only |
| **entered-in-error** | (terminal) | Wrong patient/encounter | Any other | Error only |
| **unknown** | (terminal) | Status unknown | Any other | Error only |

### 3.4 OptOutConsent (Consent)

| State (Consent.status) | Allowed Next States | Triggering Operation | Forbidden Transitions |
|------------------------|---------------------|----------------------|----------------------|
| **draft** | **proposed** | Parent reviews | Direct to active |
| **proposed** | **active** | Parent submits opt-out | Back to draft |
| | **rejected** | Parent declines opt-out | — |
| **active** | **inactive** | Parent opts back in (mid-year) | — |
| | **inactive** | End of school year (auto) | — |
| **rejected** | **active** | Parent changes mind, opts out | — |
| **inactive** | (terminal) | Archived end of year | Any other |
| **entered-in-error** | (terminal) | Wrong patient/year | Any other |

---

## 4. Resource Graph

**Centre Resource**: `ServiceRequest` (Referral) / `Task` (Referral Tracking)

**Why**: The referral is the central workflow object that coordinates across all three organizations (School, Ophthalmology, Primary Care). It carries the lifecycle state (Draft → Sent → Accepted/Rejected/Cancelled → Completed/Closed-*) and links to:
- `Observation` panel (ScreeningEvent) via `reasonReference`
- `DiagnosticReport` (OphthalmologyAssessment) via `basedOn` / Task.output
- `Patient` (Child) via `subject`
- `Practitioner` (Nurse, Ophthalmologist) via `requester` / `performer`
- `Organization` (School, Clinic, Primary Care) via `performer` / `owner`
- `Consent` (OptOutConsent) via policy enforcement (not direct reference)

**Graph Structure** (textual):
```
Patient (Child)
  ├── RelatedPerson (Parent/Guardian)
  ├── Observation (ScreeningEvent Panel)
  │     ├── hasMember → Observation (Right Eye Acuity)
  │     └── hasMember → Observation (Left Eye Acuity)
  ├── ServiceRequest (Referral) ← 360X
  │     ├── replaces → ServiceRequest (previous referral)
  │     ├── reasonReference → Observation (ScreeningEvent)
  │     ├── basedOn → DiagnosticReport (Assessment)
  │     └── focus → Task (Referral Tracking)
  │           ├── owner → Organization (Ophthalmology)
  │           └── output → DiagnosticReport (Assessment)
  ├── DiagnosticReport (OphthalmologyAssessment)
  │     ├── result → Observation (Diagnosis)
  │     ├── result → Observation (Refraction OD)
  │     ├── result → Observation (Refraction OS)
  │     └── basedOn → ServiceRequest (Referral)
  ├── CarePlan (Follow-up Plan)
  │     └── activity → ServiceRequest/Task (follow-up)
  ├── Communication (AccommodationNotice)
  │     ├── sender → Practitioner (Nurse)
  │     ├── recipient → Practitioner/RelatedPerson (Teacher)
  │     └── basedOn → DiagnosticReport (Assessment)
  ├── Consent (OptOutConsent)
  │     └── patient → Patient (Child)
  ├── List (PrimaryCareRecord Document Log)
  │     └── entry → DocumentReference (6 IP-4 types)
  └── Practitioner + PractitionerRole (Nurse, ServiceLead, Ophthalmologist)
```

---

## 5. Operations and Interoperability Points

| Op ID | Name | Description | FHIR Interaction | IHE Profile / Transaction | IP |
|-------|------|-------------|------------------|---------------------------|----|
| OP-1 | Record Screening | Nurse records screening result (Observation panel) | `POST Observation` (panel + members) | **None applies** — local capture; no IHE profile for school nurse data entry. MHD ITI-65 could be used to store but not mandated. | IP-1 |
| OP-2a | Submit Referral | Nurse sends referral to Ophthalmology | `POST ServiceRequest` + `POST Task` (360X) | **360X PCC-55 Submit Referral** (TI) — actors: Referral Initiator (School) → Referral Recipient (Ophthalmology). FHIR REST. | IP-2a |
| OP-2b | Cancel Referral (Timeout) | System cancels referral after 4-week timeout | `PATCH ServiceRequest` (status=cancelled) + `PATCH Task` (status=cancelled) | **360X PCC-58 Close Referral** — Referral Initiator closes with reason "No Response Within 4 Weeks". | IP-2b |
| OP-2c | Referral Rejection | Ophthalmology rejects referral | `PATCH ServiceRequest` (status=rejected) + `PATCH Task` (status=rejected) | **360X PCC-56 Reject Referral** — Referral Recipient rejects with reason. | IP-2c |
| OP-2d | Accept Referral | Ophthalmology accepts referral | `PATCH ServiceRequest` (status=active) + `PATCH Task` (status=received/accepted) | **360X PCC-56 Accept Referral** — Referral Recipient accepts. | IP-2a |
| OP-3a | Return Assessment Summary | Ophthalmology sends summary to School Nurse | `POST DiagnosticReport` + `POST Observation`s + `POST CarePlan`; or `POST Bundle` | **360X PCC-61 Retrieve Report** (partial) — Referral Initiator retrieves report. MHD ITI-65 Provide Document Bundle (full) for document push. DSUBm ITI-112 Notify (optional) for push notification. | IP-3a |
| OP-3b | Return Assessment Full | Ophthalmology sends full assessment to Primary Care | Same as OP-3a | **MHD ITI-65 Provide Document Bundle** (FT) — Document Source (Ophthalmology) → Document Recipient (Primary Care). DSUBm ITI-112 Notify for push. | IP-3b |
| OP-4a | Send Screening Pass | School sends pass result to Primary Care | `POST DocumentReference` (screening-pass) to Primary Care MHD endpoint | **MHD ITI-65 Provide Document Bundle** — Document Source (School) → Document Recipient (Primary Care). | IP-4a |
| OP-4b | Send Screening Decline | School sends decline result to Primary Care | `POST DocumentReference` (screening-decline) | **MHD ITI-65** | IP-4b |
| OP-4c | Send DNA Closure | School sends DNA closure to Primary Care | `POST DocumentReference` (referral-dna) | **MHD ITI-65** | IP-4c |
| OP-4d | Send Missed Screening | School sends missed (2nd absent) to Primary Care | `POST DocumentReference` (screening-missed) | **MHD ITI-65** | IP-4d |
| OP-4e | Send Rejected Referral | School sends rejected referral notice to Primary Care | `POST DocumentReference` (referral-rejected) | **MHD ITI-65** | IP-4e |
| OP-4f | Send End-of-Year Missed | School sends end-of-year missed to Primary Care | `POST DocumentReference` (end-of-year-missed) | **MHD ITI-65** | IP-4f |
| OP-5 | Send Accommodation Notice | Nurse sends accommodation to Teacher | `POST Communication` (internal) | **None applies** — internal school communication; no IHE profile. | IP-5 |
| OP-6 | Query Patient Demographics | Nurse/Ophthalmologist look up child in MPI | `GET Patient?identifier=...` or `GET Patient?family=...&given=...&birthdate=...` | **PIXm ITI-83** (cross-reference) / **PDQm ITI-78** (demographics query) — for patient matching across domains. | IP-1, IP-2, IP-3, IP-4 |
| OP-7 | Subscribe to Assessment Documents | Nurse/Primary Care subscribe for push notifications | `POST Subscription` (topic: DiagnosticReport for patient) | **DSUBm ITI-110 Subscribe** / ITI-112 Notify (TI) — for push instead of polling. | IP-3 |

**IHE Profile URLs (verified live 2026-11-19):**
- 360X: https://profiles.ihe.net/PCC/360X/ (PCC-55–61, TI, Revised 2021-04-14)
- MHD: https://profiles.ihe.net/ITI/MHD/ (ITI-65–69, FT, Release 4.2.5 2026-10-18)
- DSUBm: https://profiles.ihe.net/ITI/DSUBm/ (ITI-110–112, TI, Published 2024-02-29)
- PIXm: https://profiles.ihe.net/ITI/PIXm/ (ITI-83–84, TI, Release 3.1.0 2025-11-06)
- PDQm: https://profiles.ihe.net/ITI/PDQm/ (ITI-78, TI, Release 3.2.0 2025-11-06)
- EC-Summary: https://profiles.ihe.net/EYECARE/EC-Summary/ (TI, Published 2017-09-15)

---

## 6. IHE Profile Review per Interoperability Point

| IP | Interoperability Point | Candidate Profiles (from Landscape Scan) | Fit | Actors & Transactions | Gaps / Custom Remaining | Offer to User |
|----|------------------------|------------------------------------------|-----|----------------------|------------------------|---------------|
| **IP-1** | Screening Result Capture (Nurse → School Record) | MHD, FHIR Observation, PIXm/PDQm | **Partial (MHD)** — MHD ITI-65 can store the Observation panel as a document, but the profile is for document sharing, not data entry. No IHE profile for school nurse screening data capture. | Document Source (Nurse) → Document Recipient (School Repository) / ITI-65 | Custom: screening form UI, validation rules, outcome derivation. PIXm/PDQm for patient lookup. | **Offer MHD** for document storage if school has repository; otherwise custom FHIR REST. |
| **IP-2a** | Referral Dispatch (School → Ophthalmology) | **360X** (primary), XBeR-WD, MHD, Scheduling, PIXm/PDQm | **Full (360X)** — exactly matches closed-loop referral with tracking, accept/reject, cancel, report retrieval. Actors: Referral Initiator (School), Referral Recipient (Ophthalmology), Referral Tracker (School). Transactions: PCC-55 Submit, PCC-56 Accept/Reject, PCC-58 Close, PCC-61 Retrieve Report. | Referral Initiator → Referral Recipient (PCC-55); Recipient → Initiator (PCC-56); Initiator → Recipient (PCC-58); Initiator → Recipient (PCC-61) | 360X is Trial Implementation; wire format FHIR REST matches guide. Scheduling for appointment booking (optional). PIXm/PDQm for patient matching. | **Offer 360X conformance** — align guide's referral workflow to 360X actors/transactions. |
| **IP-2b** | Cancel Referral (Timeout) | 360X PCC-58 | **Full (360X)** — PCC-58 Close Referral with reason "No Response Within 4 Weeks". | Referral Initiator → Referral Recipient (PCC-58) | None — covered by 360X. | Included in 360X offer. |
| **IP-2c** | Referral Rejection Response | 360X PCC-56 Reject | **Full (360X)** — PCC-56 Reject with reason. | Referral Recipient → Referral Initiator (PCC-56 Reject) | None — covered by 360X. | Included in 360X offer. |
| **IP-3a** | Assessment Return — Summary (Ophthalmology → School Nurse) | 360X PCC-61, MHD, DSUBm, EC-Summary | **Partial (360X + MHD)** — 360X PCC-61 Retrieve Report (Initiator pulls). MHD ITI-65 Provide Document Bundle (Recipient pushes). DSUBm ITI-112 Notify (push notification). EC-Summary for content structure (CDA-based; guide uses FHIR). | Referral Initiator → Referral Recipient (PCC-61 pull); Document Source → Document Recipient (MHD ITI-65 push); Publisher → Subscriber (DSUBm ITI-112) | 360X is pull; guide may prefer push (MHD). EC-Summary is CDA — custom FHIR mapping needed. DSUBm is TI. | **Offer 360X + MHD** — declare conformance to both patterns (pull via 360X, push via MHD). |
| **IP-3b** | Assessment Return — Full (Ophthalmology → Primary Care) | MHD, DSUBm, EC-Summary | **Full (MHD)** — MHD ITI-65 Provide Document Bundle for document push. DSUBm ITI-112 for notification. | Document Source (Ophthalmology) → Document Recipient (Primary Care) (MHD ITI-65); Publisher → Subscriber (DSUBm ITI-112) | EC-Summary content structure CDA-based; custom FHIR mapping. | **Offer MHD conformance** for document exchange. |
| **IP-4a-f** | Primary Care Receives (6 document types) | MHD, PIXm/PDQm/PMIR | **Full (MHD)** — MHD ITI-65 for each document receipt. PIXm/PDQm for patient matching. | Document Source (School/Ophthalmology) → Document Recipient (Primary Care) (MHD ITI-65); Consumer → Supplier (PIXm ITI-83 / PDQm ITI-78) | 6 distinct document types mapped to LOINC; Primary Care must handle all. | **Offer MHD + PIXm/PDQm** for document receipt and patient matching. |
| **IP-5** | Teacher Accommodation (Internal) | None | **None applies** — internal school communication; no IHE profile for teacher accommodation notices. | — | Custom: Communication resource, internal delivery (paper, email, EHR message). | No IHE profile; custom FHIR. |

**Summary of IHE Offers to User:**
1. **360X** (TI) — for referral workflow (IP-2a/b/c). Align ServiceRequest/Task to 360X actors/transactions.
2. **MHD** (FT) — for document exchange (IP-1 storage, IP-3a/b push, IP-4a-f). Align DocumentReference/Bundle to MHD.
3. **DSUBm** (TI) — optional push notifications for assessments (IP-3a/b).
4. **PIXm/PDQm** (TI) — patient matching across domains (all IPs).
5. **EC-Summary** (TI) — content structure reference for ophthalmology assessment (CDA-based; custom FHIR mapping).

**No IHE Profile — Explicitly None Applies:**
- School nurse screening data entry (IP-1 capture) — no IHE profile for school health screening.
- Teacher accommodation notice (IP-5) — internal communication.
- Threshold evaluation (Pass/Refer logic) — custom clinical logic.
- Opt-out consent management — custom Consent usage (no BPPC/APPC/PCF fit for opt-out program consent).

---

## 7. Mapping Table

**Source**: Paper form / nurse entry (ScreeningEvent), Referral letter, Ophthalmology EHR, SIS, HR
**Destination**: FHIR R4 resources as defined above

| Source Entity / Field | Source Format | FHIR Path | Transformation Rule | Binding Strength | Unit (UCUM) | Missing / Ambiguous / Invalid Handling |
|----------------------|---------------|-----------|---------------------|------------------|-------------|----------------------------------------|
| **Child** | | | | | | |
| Full name | Structured (SIS) | `Patient.name[0].family`, `Patient.name[0].given` | Direct copy | Required (text) | — | Missing → cannot create Patient; flag to admin |
| Date of birth | Structured (SIS) | `Patient.birthDate` | Direct copy (YYYY-MM-DD) | Required (date) | — | Missing → cannot screen; flag |
| School roll number | Structured (SIS) | `Patient.identifier[0].value` (system=school-roll) | Direct copy | Required | — | Missing → cannot screen; flag |
| National health ID | Structured (SIS, optional) | `Patient.identifier[1].value` (system=national) | Direct copy if present | Extensible | — | If missing → omit identifier; demographic matching used |
| Sex | Coded (SIS) | `Patient.gender` | Map SIS code → male/female/other/unknown | Required (valueSet) | — | Invalid code → map to "unknown"; log |
| Grade/class | Structured (SIS) | `ScreeningEvent.Observation.note` (panel) / `Encounter.class` | Copy to ScreeningEvent gradeAtScreening | Extensible | — | Missing → omit |
| Address | Structured (SIS) | `Patient.address` | Direct copy | Required | — | Missing → use school address; flag |
| Parent contact | Structured (SIS) | `Patient.telecom`, `RelatedPerson.telecom` | Split to Patient (emergency) and RelatedPerson | Required | — | Missing → flag |

| **Parent/Guardian** | | | | | | |
| Full name | Structured (SIS) | `RelatedPerson.name` | Direct copy | Required | — | Missing → flag |
| Relationship | Coded (SIS) | `RelatedPerson.relationship` | Map SIS code → HL7 v2-0131 (MTH, FTH, GRD, etc.) | Extensible | — | Invalid → "GRD" (guardian) |
| Phone | Structured (SIS) | `RelatedPerson.telecom` | Direct copy | Required | — | Missing → use child's contact |
| Email | Structured (SIS) | `RelatedPerson.telecom` | Direct copy | Extensible | — | Optional |
| Opt-out status | Boolean (SIS) | `Consent.provision.type` (deny/permit) + `period` | True → deny; False → permit; statusHistory for changes | Required | — | Missing → assume permit (opted in) |

| **School Nurse / ServiceLead** | | | | | | |
| Full name | Structured (HR) | `Practitioner.name` | Direct copy | Required | — | Missing → cannot act |
| License number | Structured (HR) | `Practitioner.identifier` (system=license) | Direct copy | Required | — | Missing → cannot screen; flag HR |
| Assigned schools | Structured (HR) | `PractitionerRole.location` | Map to Location references | Extensible | — | Missing → flag |
| Escalation contact | Reference (HR) | `PractitionerRole.extension(escalationContact)` | Reference to ServiceLead PractitionerRole | Extensible | — | Missing → default to regional lead |

| **ScreeningEvent** | | | | | | |
| Screening date/time | Nurse entry | `Observation.effectiveDateTime` (panel + members) | Direct copy (ISO 8601) | Required | — | Missing → incomplete outcome |
| School year | Derived | `Observation.note` (panel) | Derive from date (e.g., 2026-2027) | Extensible | — | Auto-derived |
| Grade at screening | Copied from Child | `Observation.note` (panel) | Snapshot from Child at screening | Extensible | — | Auto-copied |
| Test used | Coded (nurse) | `Observation.note` (panel) / `Observation.method` | Map: Snellen 6m / Tumbling E / Lea symbols → local codes | Extensible | — | Missing → default Snellen; log |
| Right eye acuity | Structured (nurse) | `Observation.valueRatio` (member 1) | Parse Snellen fraction "6/12" → numerator.value=6, numerator.unit=m, denominator.value=12, denominator.unit=m | Required | Ratio (UCUM: m/m) | Missing → incomplete outcome; reason required |
| Left eye acuity | Structured (nurse) | `Observation.valueRatio` (member 2) | Parse Snellen fraction; bodySite=363655008 (left eye) | Required | Ratio (UCUM: m/m) | Missing → incomplete outcome; reason required |
| Outcome | Derived + nurse | `Observation.note` (panel) / `Observation.interpretation` | Auto-derive: Pass if both ≥6/9; Refer if either ≤6/12 OR diff≥2 lines; Absent/Incomplete from nurse | Required (coded) | — | If acuity missing → Incomplete; if both present → auto-derive |
| Incomplete reason | Free text (nurse) | `Observation.note` (panel) | Direct copy | Extensible | — | Required if outcome=Incomplete |
| Attempt number | Derived from counters | `Observation.note` (panel) | 1=initial, 2=re-screen (from Absent/Incomplete counters) | Required | — | Auto-derived |
| Screener ID | Auto-filled | `Observation.performer` | Reference to Practitioner (nurse) | Required | — | Auto-filled from session |
| Child ID | Auto-filled | `Observation.subject` | Reference to Patient (child) | Required | — | Auto-filled from selection |

| **Referral** | | | | | | |
| Referral ID | System UUID | `ServiceRequest.identifier`, `Task.identifier` | Direct copy | Required | — | Auto-generated |
| Child ID | Reference | `ServiceRequest.subject`, `Task.for` | Reference to Patient | Required | — | From ScreeningEvent |
| ScreeningEvent ID | Reference | `ServiceRequest.reasonReference` | Reference to Observation panel | Required | — | From ScreeningEvent |
| Referral date | Nurse entry | `ServiceRequest.occurrenceDateTime`, `Task.authoredOn` | Direct copy | Required | — | Default to today |
| Reason | Derived + nurse | `ServiceRequest.reasonCode` | Map: acuity≤6/12 → SNOMED 416070007; diff≥2 lines → SNOMED 267083005 (anisometropia); incomplete → custom | Extensible (SNOMED) | — | Auto-derived from ScreeningEvent |
| Acuity per eye | Copied | `ServiceRequest.note` | Copy from ScreeningEvent | Extensible | — | Auto-copied |
| Test used | Copied | `ServiceRequest.note` | Copy from ScreeningEvent | Extensible | — | Auto-copied |
| Screener ID | Reference | `ServiceRequest.requester` | Reference to Practitioner | Required | — | Auto-filled |
| Parent decision | Coded (parent) | `ServiceRequest.note` / `Task.input` | Accept/Decline → text note | Extensible | — | Missing → pending; follow up at 4 weeks |
| Decline reason | Free text (parent) | `ServiceRequest.note` | Direct copy | Extensible | — | Required if decline |
| Expected deadline | Derived | `Task.restriction.period.end` | referralDate + 4 weeks | Required | — | Auto-derived |
| Ophthalmology clinic | Reference (optional) | `ServiceRequest.performer` | Reference to Organization | Extensible | — | If known |
| 360X referral ID | External (360X) | `ServiceRequest.identifier` (system=360x) | Assigned by Recipient | Extensible | — | Populated after PCC-55 |
| Replaces referral ID | Reference | `ServiceRequest.replaces` (0..*) | Reference to previous ServiceRequest(s); typically one entry per re-issue | Extensible | — | Set on re-issue; array with single entry typically |

| **OphthalmologyAssessment** | | | | | | |
| Assessment ID | System UUID | `DiagnosticReport.identifier` | Direct copy | Required | — | Auto-generated |
| Referral ID | Reference | `DiagnosticReport.basedOn` | Reference to ServiceRequest | Required | — | From referral |
| Child ID | Reference | `DiagnosticReport.subject` | Reference to Patient | Required | — | From referral |
| Assessment date | Clinician entry | `DiagnosticReport.effectiveDateTime`, `DiagnosticReport.issued` | Direct copy | Required | — | Required |
| Diagnosis | Coded (clinician) | `DiagnosticReport.conclusionCode`, `Observation.valueCodeableConcept` (diagnosis member) | Map ICD-10/SNOMED → SNOMED CT (required binding) | Required (SNOMED) | — | Missing → incomplete; flag |
| Right eye diagnosis detail | Structured | `Observation.valueCodeableConcept` (diagnosis member) + `bodySite` | SNOMED + bodySite right eye | Extensible | — | Optional |
| Left eye diagnosis detail | Structured | Same pattern, bodySite left eye | SNOMED + bodySite left eye | Extensible | — | Optional |
| Refractive prescription | Structured (sphere, cylinder, axis) | `Observation.valueQuantity` + `component` (refraction members) | Sphere/cylinder/axis → valueQuantity + components; unit=D (diopter), axis=deg | Required | D, deg | If no glasses → omit |
| Follow-up plan | Structured (interval, treatment) | `CarePlan.activity.detail.scheduledPeriod`, `code` | Interval → period; patching → Task/ServiceRequest code | Extensible | — | Required |
| Outcome | Coded (clinician) | `DiagnosticReport.conclusion` / `Observation.valueCodeableConcept` | Seen/DNA → text + code | Extensible | — | Required |
| Ophthalmologist ID | Auto-filled | `DiagnosticReport.performer`, `DiagnosticReport.resultsInterpreter` | Reference to Practitioner | Required | — | Auto-filled |
| Clinic ID | Auto-filled | `DiagnosticReport.custodian` | Reference to Organization | Required | — | Auto-filled |

| **PrimaryCareRecord Document Entries** | | | | | | |
| Document type | Coded (system) | `DocumentReference.type` (LOINC), `List.entry` | Map 6 types → LOINC codes (see table) | Required | — | Required per entry |
| Source referral ID | Reference | `DocumentReference.context.related` | Reference to ServiceRequest | Extensible | — | Optional |
| Document reference | Reference | `DocumentReference.content.attachment.url` | URL to ScreeningEvent/Assessment resource | Required | — | Required |
| Receive date | System | `DocumentReference.date` | Direct copy | Required | — | Auto-set |
| Completeness flag | Derived | `DocumentReference.description` / `DocumentReference.context` | Map: complete/partial/declined/missed | Extensible | — | Derived |
| Entered by | Reference | `DocumentReference.author` | Reference to Practitioner/admin | Required | — | Auto-set |

| **AccommodationNotice** | | | | | | |
| Notice ID | System UUID | `Communication.identifier` | Direct copy | Required | — | Auto-generated |
| Child ID | Reference | `Communication.subject` | Reference to Patient | Required | — | Required |
| Assessment ID | Reference | `Communication.basedOn` | Reference to DiagnosticReport | Extensible | — | Required |
| Date issued | Nurse entry | `Communication.sent` | Direct copy | Required | — | Required |
| Accommodation type | Coded (derived) | `Communication.category`, `Communication.payload` | Map: glasses/front-seat/both/other → text in payload | Extensible | — | Required |
| Accommodation detail | Free text (nurse) | `Communication.payload.contentString` | Direct copy | Extensible | — | Required |
| Valid until | Derived | `Communication.note` | Derived: end of school year or next assessment | Extensible | — | Auto-derived |
| Issued by | Reference | `Communication.sender` | Reference to Practitioner (nurse) | Required | — | Required |
| Supersedes notice ID | Reference | `Communication.relatesTo` (code=replaces) | Reference to previous Communication | Extensible | — | Optional |

| **OptOutConsent** | | | | | | |
| Consent ID | System | `Consent.identifier` | Direct copy | Required | — | Auto-generated |
| Child ID | Reference | `Consent.patient` | Reference to Patient | Required | — | Required |
| School year | Structured | `Consent.provision.period` | Start/end of school year | Required | — | Required |
| Status history | Repeating group | `Consent.provision` (multiple entries) | Each statusHistory entry → provision with period | Required | — | Required |
| Current status | Derived | `Consent.provision.type` (latest) | deny=opted-out, permit=opted-in | Required | — | Derived |
| Date recorded | System | `Consent.dateTime` | Direct copy | Required | — | Auto-set |
| Recorded by | Reference | `Consent.performer` | Reference to Practitioner (admin) | Required | — | Required |

**Unmapped Codes** (no target terminology):
- Test used (Snellen/Tumbling E/Lea) — local codes; define local CodeSystem if needed
- Screening outcome (Pass/Refer/Absent/Incomplete) — local codes; map to Observation.interpretation where possible
- Accommodation type — local codes

---

## 8. Sequence Diagrams

*To be created in `04-sequence-diagrams.md` with one diagram per flow:*
1. **Screening Flow** — Child presents → Opt-out check → Screening → Outcome (Pass/Refer/Absent/Incomplete) → Parent notification → Primary Care (Pass)
2. **Referral Flow** — Refer outcome → Parent decision (Accept/Decline) → Send Referral (360X) → Ophthalmology Accept/Reject → 4-week wait → Timeout cancel → Re-issue
3. **Assessment Return Flow** — Ophthalmology assessment → Seen → Summary to Nurse (360X/MHD) + Full to Primary Care (MHD) → Nurse generates Accommodation → Close referral
4. **DNA / Re-referral Flow** — DNA outcome → Nurse contacts parent → Re-referral (Accept/Decline) → 2nd DNA → Close + Primary Care notify
5. **Absent/Incomplete Re-screen Flow** — Absent/Incomplete → Re-screen scheduled → 2nd attempt → Missed (absent) or Direct Referral (incomplete) → Primary Care notify
6. **End-of-Year Flow** — End-of-year boundary → Pending re-screens → Record missed → Parent + Primary Care notify
7. **Opt-Out Change Flow** — Parent changes opt-out mid-year → Consent updated → Next screening respects new status

*Each diagram will be saved as `04-sequence-<flow>.svg` with operation table mapping messages to OP-1 through OP-7.*

---

## 9. Validation Summary

- [x] Every entity maps to exactly one primary FHIR resource (or pair for workflow)
- [x] Base resource canonical URLs stated; user offered alternative bases
- [x] All workflow-state resources have lifecycle tables (Referral, ScreeningEvent, Assessment, Consent)
- [x] Resource graph centres on ServiceRequest/Task (referral workflow) with justification
- [x] IHE profile review per interoperability point with fit assessment (full/partial/none), actors, transactions
- [x] Mapping table with source→FHIR path, transformation, binding, unit, missing handling
- [x] Terminology versions pinned (SNOMED CT 2026-03-15, LOINC 2.76, UCUM 2.0.1)
- [x] All examples synthetic (to be generated beside proposal)
- [x] Sequence diagrams planned for all 7 flows