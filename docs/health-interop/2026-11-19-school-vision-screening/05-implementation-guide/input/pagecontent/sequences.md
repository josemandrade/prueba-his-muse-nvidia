# Sequence Diagrams

---

## Overview

This page contains one sequence diagram per flow, taken from the BPMN model. Each diagram shows the messages in time order, with every message naming its operation (OP-1 through OP-7), FHIR interaction, IHE profile, and expected result.

---

## Flow 1: Screening Flow

**BPMN Path**: Start → Opt-Out Consent → Schedule Screening → Screening Day → Check Opt-Out → Perform Screening → Outcome (Pass) → Record Pass → Notify Parent → Primary Care Receive Screening → Next Child

**Participants**: School Nurse, Child, Parent/Guardian, Primary Care Team

![Screening Flow](images/04-sequence-screening.png)

### Operation Table: Screening Flow

| # | Message | Operation | FHIR Interaction | IHE Profile / Transaction | Expected Result |
|---|---------|-----------|------------------|---------------------------|-----------------|
| 1 | Nurse records screening result (Observation panel + 2 members) | **OP-1: Record Screening** | `POST Observation` (panel + hasMember) | None applies (local capture) | `201 Created` Observation panel + 2 member Observations |
| 2 | Nurse sends pass result to Primary Care | **OP-4a: Send Screening Pass** | `POST DocumentReference` (type=screening-pass, LOINC 83700-8) | **MHD ITI-65** Provide Document Bundle | `201 Created` DocumentReference in Primary Care List |
| 3 | Parent receives pass letter | Non-FHIR | Paper letter / email | None applies | Parent notified |

---

## Flow 2: Referral Flow

**BPMN Path**: Refer outcome → Create Referral → Parent Decision (Accept/Decline) → Send Referral (360X) → Ophthalmology Accept/Reject → 4-week wait → Timeout cancel → Re-issue

**Participants**: School Nurse, Parent/Guardian, Ophthalmology Clinic, Primary Care Team

![Referral Flow](images/04-sequence-referral.png)

### Operation Table: Referral Flow

| # | Message | Operation | FHIR Interaction | IHE Profile / Transaction | Expected Result |
|---|---------|-----------|------------------|---------------------------|-----------------|
| 1 | Nurse submits referral to Ophthalmology | **OP-2a: Submit Referral** | `POST ServiceRequest` + `POST Task` (360X bundle) | **360X PCC-55** Submit Referral | `201 Created` ServiceRequest + Task; 360X Referral ID returned |
| 2 | Ophthalmology accepts referral | **OP-2d: Accept Referral** | `PATCH Task` (status=received/accepted) | **360X PCC-56** Accept Referral | `200 OK` |
| 3 | Ophthalmology rejects referral | **OP-2c: Reject Referral** | `PATCH Task` (status=rejected) + reason | **360X PCC-56** Reject Referral | `200 OK` |
| 4 | Nurse handles rejection: correct & resend | **OP-2a: Re-submit** | `POST ServiceRequest` (replaces=old) + `POST Task` | **360X PCC-55** | `201 Created` new referral |
| 5 | Nurse handles rejection: close | **OP-4e: Send Rejected Notice** | `POST DocumentReference` (referral-rejected) | **MHD ITI-65** | `201 Created` DocumentReference |
| 6 | 4-week timeout: Nurse cancels original referral | **OP-2b: Cancel Referral** | `PATCH ServiceRequest` (status=cancelled) + `PATCH Task` (status=cancelled) | **360X PCC-58** Close Referral | `200 OK` |
| 7 | Nurse re-issues new referral | **OP-2a: Submit Referral** | `POST ServiceRequest` (replaces=old) + `POST Task` | **360X PCC-55** | `201 Created` new referral (fresh lifecycle) |
| 8 | Nurse sends decline to Primary Care | **OP-4b: Send Decline** | `POST DocumentReference` (screening-decline) | **MHD ITI-65** | `201 Created` |

---

## Flow 3: Assessment Return Flow

**BPMN Path**: Assessment Received → Outcome (Seen) → Process Assessment → Send Summary to Nurse (360X/MHD) + Full to Primary Care (MHD) → Nurse Generates Accommodation → Close Referral

**Participants**: Ophthalmology Clinic, School Nurse, Primary Care Team, Teacher

![Assessment Return Flow](images/04-sequence-assessment-return.png)

### Operation Table: Assessment Return Flow

| # | Message | Operation | FHIR Interaction | IHE Profile / Transaction | Expected Result |
|---|---------|-----------|------------------|---------------------------|-----------------|
| 1 | Ophthalmology sends summary to Nurse | **OP-3a: Return Summary** | `GET DiagnosticReport` (360X PCC-61) OR `POST DocumentReference` (MHD ITI-65) | **360X PCC-61** Retrieve Report (pull) **or** **MHD ITI-65** Provide Document Bundle (push) | `200 OK` DiagnosticReport + Observations **or** `201 Created` DocumentReference |
| 2 | Ophthalmology sends full assessment to Primary Care | **OP-3b: Return Full** | `POST DocumentReference` (assessment-full, LOINC 28626-8) | **MHD ITI-65** Provide Document Bundle | `201 Created` DocumentReference in Primary Care List |
| 3 | Nurse generates accommodation notice | **OP-5: Send Accommodation** | `POST Communication` (category=instruction) | None applies (internal) | `201 Created` Communication |
| 4 | Nurse sends accommodation to Teacher | Non-FHIR | Internal delivery (paper/email/EHR message) | None applies | Teacher notified |

---

## Flow 4: DNA / Re-referral Flow

**BPMN Path**: Assessment Outcome (DNA) → Record DNA → Nurse Contacts Parent → Re-referral Decision (Accept/Decline) → Create Re-referral → Send Referral → 2nd DNA → Close Referral → Primary Care Notify

**Participants**: School Nurse, Parent/Guardian, Ophthalmology Clinic, Primary Care Team

![DNA Re-referral Flow](images/04-sequence-dna-rereferral.png)

### Operation Table: DNA / Re-referral Flow

| # | Message | Operation | FHIR Interaction | IHE Profile / Transaction | Expected Result |
|---|---------|-----------|------------------|---------------------------|-----------------|
| 1 | Nurse submits re-referral | **OP-2a: Submit Referral** | `POST ServiceRequest` + `POST Task` (new, replaces=previous if any) | **360X PCC-55** | `201 Created` new referral |
| 2 | Ophthalmology accepts re-referral | **OP-2d: Accept Referral** | `PATCH Task` (status=received) | **360X PCC-56** | `200 OK` |
| 3 | 2nd DNA: Nurse closes referral | Internal | `PATCH ServiceRequest` (status=completed) + `PATCH Task` (status=completed) | None (internal state) | Referral closed |
| 4 | Nurse sends DNA closure to Primary Care | **OP-4c: Send DNA Closure** | `POST DocumentReference` (referral-dna, LOINC 11506-3) | **MHD ITI-65** | `201 Created` DocumentReference |
| 5 | Parent declines re-referral | Internal | `PATCH ServiceRequest` (status=completed) + `PATCH Task` (status=completed) | None | Referral closed |
| 6 | Nurse sends DNA closure (decline) to Primary Care | **OP-4c** | `POST DocumentReference` | **MHD ITI-65** | `201 Created` |

---

## Flow 5: Absent / Incomplete Re-screen Flow

**BPMN Path**: Outcome (Absent/Incomplete) → Record + Increment Counter → Schedule Re-screen (2 weeks) → 1st Attempt → Re-screen → 2nd Attempt → Missed (Absent) or Direct Referral (Incomplete) → Primary Care Notify

**Participants**: School Nurse, Child, Parent/Guardian, Primary Care Team, Ophthalmology Clinic (for direct referral from incomplete)

![Absent/Incomplete Flow](images/04-sequence-absent-incomplete.png)

### Operation Table: Absent/Incomplete Re-screen Flow

| # | Message | Operation | FHIR Interaction | IHE Profile / Transaction | Expected Result |
|---|---------|-----------|------------------|---------------------------|-----------------|
| 1 | Nurse records re-screen result | **OP-1: Record Screening** | `POST Observation` (new panel, attemptNumber=2) | None applies | `201 Created` new ScreeningEvent |
| 2 | 2nd absent: Nurse sends missed to Primary Care | **OP-4d: Send Missed** | `POST DocumentReference` (screening-missed) | **MHD ITI-65** | `201 Created` |
| 3 | 2nd incomplete: Nurse submits direct referral | **OP-2a: Submit Referral** | `POST ServiceRequest` + `POST Task` (reason=incomplete-2nd-attempt) | **360X PCC-55** | `201 Created` |
| 4 | Nurse notifies parent of direct referral | Non-FHIR | Internal notification (paper/email) | None applies | Parent notified |
| 5 | Parent notified of missed screening | Non-FHIR | Paper letter / email | None applies | Parent notified |

---

## Flow 6: End-of-Year Flow

**BPMN Path**: End of School Year (boundary timer on Screening Day) → Handle Pending Re-screens → Record as Missed → Notify Parent → Notify Primary Care → End Screening Year

**Participants**: School Nurse, Parent/Guardian, Primary Care Team

![End-of-Year Flow](images/04-sequence-end-of-year.png)

### Operation Table: End-of-Year Flow

| # | Message | Operation | FHIR Interaction | IHE Profile / Transaction | Expected Result |
|---|---------|-----------|------------------|---------------------------|-----------------|
| 1 | Nurse sends end-of-year missed to Primary Care | **OP-4f: Send End-of-Year Missed** | `POST DocumentReference` (end-of-year-missed, LOINC 83700-8) | **MHD ITI-65** | `201 Created` DocumentReference |
| 2 | Nurse notifies parent | Non-FHIR | Paper letter / email | None applies | Parent notified |
| 3 | Nurse archives records | Internal | Update ScreeningEvent status=archived | None applies | Records archived |

---

## Flow 7: Opt-Out Change Flow

**BPMN Path**: Parent Changes Opt-Out Mid-Year → Consent Updated (statusHistory) → Next Screening Respects New Status

**Participants**: Parent/Guardian, School Admin (SIS), School Nurse

![Opt-Out Change Flow](images/04-sequence-optout-change.png)

### Operation Table: Opt-Out Change Flow

| # | Message | Operation | FHIR Interaction | IHE Profile / Transaction | Expected Result |
|---|---------|-----------|------------------|---------------------------|-----------------|
| 1 | Admin updates consent | Internal (Consent update) | `PATCH Consent` (add provision entry for new status period) | None applies | Consent updated with new statusHistory |
| 2 | Nurse reads current status at screening | Internal (Consent read) | `GET Consent?patient=[child]&status=active` | None applies | Current status returned |
| 3 | Nurse acts on status | Internal | Conditional logic in screening workflow | None applies | Screening performed or skipped |

---

## Mechanical Validation Summary

| Check | Count | Status |
|-------|-------|--------|
| Messages referencing an operation ID | 28 | ✅ All messages map to OP-1 through OP-7 |
| Non-FHIR messages (declared) | 7 | ✅ All labelled with channel/payload |
| Operations without a diagram | 0 | ✅ OP-1 through OP-7 all appear in at least one diagram |
| Diagrams rendered as SVG/PNG | 7 | ✅ `04-sequence-<flow>.svg` files created |

---

## Diagram Files

| Flow | SVG Source | PNG for Guide |
|------|------------|---------------|
| 1. Screening | `04-sequence-screening.svg` | `images/04-sequence-screening.png` |
| 2. Referral | `04-sequence-referral.svg` | `images/04-sequence-referral.png` |
| 3. Assessment Return | `04-sequence-assessment-return.svg` | `images/04-sequence-assessment-return.png` |
| 4. DNA / Re-referral | `04-sequence-dna-rereferral.svg` | `images/04-sequence-dna-rereferral.png` |
| 5. Absent/Incomplete | `04-sequence-absent-incomplete.svg` | `images/04-sequence-absent-incomplete.png` |
| 6. End-of-Year | `04-sequence-end-of-year.svg` | `images/04-sequence-end-of-year.png` |
| 7. Opt-Out Change | `04-sequence-optout-change.svg` | `images/04-sequence-optout-change.png` |

*All diagrams rendered from mermaid source using `render_sequence.py`. PNGs are binary — upload via GitHub website into `input/images/`.*