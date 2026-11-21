# Lifecycle Tables - v0.1.0

* [**Table of Contents**](toc.md)
* **Lifecycle Tables**

## Lifecycle Tables

### Lifecycle Tables

-------

#### Overview

Each workflow-state resource in this Implementation Guide has a defined lifecycle with states, allowed transitions, triggering operations (with PI), and forbidden transitions. These tables are derived from the validated FHIR proposal and BPMN model.

-------

#### 1. Referral (ServiceRequest + Task) — 360X-Aligned

##### R4 Value Sets

* **ServiceRequest.status** (Required): `draft | active | on-hold | revoked | completed | entered-in-error | unknown`
* **Task.status** (Required): `draft | requested | received | accepted | rejected | ready | cancelled | in-progress | on-hold | failed | completed | entered-in-error`

##### Lifecycle Table

| | | | |
| :--- | :--- | :--- | :--- |
| **Draft**(draft / draft) | **Sent**(active / requested) | OP-2a: Submit Referral (PCC-55) | Direct to Completed, Cancelled, Closed-* |
| **Sent**(active / requested) | **Accepted**(active / received) | OP-2d: Accept Referral (PCC-56) | Direct to Completed (must go through Accepted) |
|   | **Rejected**(rejected / rejected) | OP-2c: Reject Referral (PCC-56) | — |
|   | **Cancelled**(cancelled / cancelled) | OP-2b: Timeout Cancel (PCC-58) | — |
| **Accepted**(active / received) | **Completed**(completed / completed) | OP-3: Assessment Received (PCC-61) | Back to Sent, Draft |
|   | **Closed-DNS**(completed / completed) | OP-4c: DNA Closure (2nd DNA) | — |
| **Rejected**(rejected / rejected) | **Closed-Rejected**(completed / completed) | Nurse closes, notifies (OP-4e) | Back to Sent, Accepted |
| **Cancelled**(cancelled / cancelled) | **Sent**(new referral, fresh lifecycle) | OP-2a: Re-issue Referral (new ServiceRequest with`replaces`) | Re-activate cancelled referral |
| **Completed**(completed / completed) | **Closed-DNS**(completed / completed) | If 2nd DNA after completion (rare) | — |
| **Closed-Decline**(completed / completed) | (terminal) | OP-4b: Parent Decline at outset | — |
| **Closed-Rejected**(completed / completed) | (terminal) | After Rejected, nurse closes | — |

##### Cross-Machine Invariants

| | |
| :--- | :--- |
| A referral cannot be both Accepted and Cancelled | If ServiceRequest.status = active, Task.status cannot be cancelled without going through Cancelled state first |
| A cancelled referral cannot be re-activated | No transition from Cancelled → Active on same ServiceRequest; new referral must be created with`replaces` |
| DNA closure only from Accepted or Completed | Closed-DNS only reachable from Accepted or Completed states |
| Parent Decline closes without sending referral | Closed-Decline reachable directly from Sent (parent decision = decline) |

-------

#### 2. ScreeningEvent (Observation Panel)

##### R4 Value Set

* **Observation.status** (Required): `registered | preliminary | final | amended | corrected | cancelled | entered-in-error | unknown`

##### Lifecycle Table

| | | | |
| :--- | :--- | :--- | :--- |
| **registered** | **preliminary** | Nurse starts entry | Direct to final/amended |
| **preliminary** | **final** | Nurse completes & records | Back to registered |
|   | **amended** | Nurse corrects (after final) | — |
|   | **corrected** | System corrects (data error) | — |
| **final** | **amended** | Nurse enters correction | Back to preliminary |
|   | **corrected** | System corrects | — |
| **amended** | **final** | Re-validated | — |
| **corrected** | **final** | Re-validated | — |
| **cancelled** | (terminal) | Entered in error | Any other |
| **entered-in-error** | (terminal) | Wrong patient/encounter | Any other |
| **unknown** | (terminal) | Status unknown | Any other |

##### Notes

* Typical path: `registered → preliminary → final` (nurse enters, completes, records)
* `amended`/`corrected` only after `final`
* Each re-screen creates a **new** Observation panel (attemptNumber increments), not a state change on the same panel

-------

#### 3. OphthalmologyAssessment (DiagnosticReport)

##### R4 Value Set

* **DiagnosticReport.status** (Required): `registered | partial | preliminary | final | amended | corrected | appended | cancelled | entered-in-error | unknown`

##### States Actually Used in This Workflow

| | | | | |
| :--- | :--- | :--- | :--- | :--- |
| **registered** | **partial**/**preliminary**/**final** | Partial/preliminary results entered; or direct to final | — | **Yes**(often → final directly) |
| **partial** | **preliminary**/**final** | Preliminary results | Back to registered | Optional |
| **preliminary** | **final** | Clinician validates | Back to partial | Optional |
| **final** | **amended**/**corrected**/**appended** | Addendum / correction / additional results | — | **Yes** |
| **amended** | **final** | Re-validated | — | **Yes** |
| **corrected** | **final** | Re-validated | — | **Yes** |
| **appended** | **final** | Re-validated | — | **Yes** |
| **cancelled** | (terminal) | Report cancelled | Any other | Error only |
| **entered-in-error** | (terminal) | Wrong patient/encounter | Any other | Error only |
| **unknown** | (terminal) | Status unknown | Any other | Error only |

##### Typical Path

`registered → final` (clinician enters and validates in one step) → `amended`/`corrected`/`appended` as needed

-------

#### 4. OptOutConsent (Consent)

##### R4 Value Set

* **Consent.status** (Required): `draft | proposed | active | rejected | inactive | entered-in-error`

##### Lifecycle Table

| | | | |
| :--- | :--- | :--- | :--- |
| **draft** | **proposed** | Parent reviews | Direct to active |
| **proposed** | **active** | Parent submits opt-out | Back to draft |
|   | **rejected** | Parent declines opt-out | — |
| **active** | **inactive** | Parent opts back in (mid-year) | — |
|   | **inactive** | End of school year (auto) | — |
| **rejected** | **active** | Parent changes mind, opts out | — |
| **inactive** | (terminal) | Archived end of year | Any other |
| **entered-in-error** | (terminal) | Wrong patient/year | Any other |

##### StatusHistory Mechanism

Multiple `Consent.provision` entries model status changes:

* Each provision has `type` (deny/permit) and `period` (start/end)
* Current status = latest provision by period.start
* Example: deny [Sep 1 – Nov 10] → permit [Nov 10 – Jun 30]

-------

#### 5. ScreeningEvent Attempt Lifecycle (Cross-Resource)

##### Absent Path

| Attempt | ScreeningEvent State | Next Action | |———|———————|————-| | 1st Absent | `final` (outcome=Absent) | Schedule re-screen → new ScreeningEvent (attemptNumber=2) | | 2nd Absent | `final` (outcome=Absent) | Record as Missed → Notify Parent + Primary Care (OP-4d) |

##### Incomplete Path

| Attempt | ScreeningEvent State | Next Action | |———|———————|————-| | 1st Incomplete | `final` (outcome=Incomplete) | Schedule re-screen → new ScreeningEvent (attemptNumber=2) | | 2nd Incomplete | `final` (outcome=Incomplete) | Direct Referral (OP-2a) with partial data |

-------

#### 6. AccommodationNotice (Communication)

##### R4 Value Set

* **Communication.status** (Required): `preparation | in-progress | not-done | on-hold | stopped | completed | entered-in-error | unknown`

##### Lifecycle Table

| | | | |
| :--- | :--- | :--- | :--- |
| **preparation** | **in-progress** | Nurse drafting | Direct to completed |
| **in-progress** | **sent**/**not-done** | Nurse sends / aborts | Back to preparation |
| **sent** | **completed** | Teacher acknowledges | — |
| **not-done** | (terminal) | Aborted | — |
| **completed** | **superseded** | New notice issued | Back to sent |
| **superseded** | (terminal) | Replaced | — |
| **entered-in-error** | (terminal) | Wrong child/data | Any other |

##### Supersession Chain

Each new notice has `relatesTo.code=replaces` → previous notice. Previous notice status becomes `superseded`.

-------

#### 6. PrimaryCareRecord Document Entries (DocumentReference)

##### R4 Value Set

* **DocumentReference.status** (Required): `current | superseded | entered-in-error`

##### Lifecycle Table

| | | | |
| :--- | :--- | :--- | :--- |
| **current** | **superseded** | New document received for same type/referral | Back to current |
|   | **entered-in-error** | Wrong document | — |
| **superseded** | (terminal) | Replaced | — |
| **entered-in-error** | (terminal) | Error | — |

##### Document Types & Replacement Rules

| | |
| :--- | :--- |
| screening-pass | New screening result for same child |
| screening-decline | N/A (terminal) |
| screening-missed | N/A (terminal) |
| assessment-full | New assessment for same referral |
| referral-dna | N/A (terminal) |
| referral-rejected | N/A (terminal) |
| end-of-year-missed | N/A (terminal) |

-------

#### Cross-Machine Invariants (Global)

| | | |
| :--- | :--- | :--- |
| Every referral has exactly one ServiceRequest | ServiceRequest | Count(ServiceRequest where focus=Task) = 1 per Task |
| Every Task tracks exactly one ServiceRequest | Task, ServiceRequest | Task.focus references valid ServiceRequest |
| Referral closure reason traversable | ServiceRequest, DiagnosticReport | Assessment.reference → ServiceRequest → ServiceRequest.state gives closure reason |
| ScreeningEvent attemptNumber consistent | Observation (Panel) | attemptNumber increments by 1 per re-screen; max 2 |
| Consent statusHistory continuous | Consent | No gaps in provision.period; each new provision starts when previous ends |
| PrimaryCareRecord documents match IP-4 count | List, DocumentReference | 6 document types max per child per year |

-------

#### Forbidden Transition Tests (For Implementation)

```
# Referral cannot be re-activated after cancellation
Scenario: Cancelled referral cannot go back to Sent
  Given a ServiceRequest with status "cancelled"
  When attempting to set status to "active"
  Then the operation SHALL fail with 409 Conflict

# Referral must go through Accepted before Completed
Scenario: Sent referral cannot go directly to Completed
  Given a ServiceRequest with status "active" and Task with status "requested"
  When attempting to set ServiceRequest to "completed"
  Then the operation SHALL fail with 422 Unprocessable Entity

# ScreeningEvent cannot be amended before final
Scenario: Preliminary screening cannot be amended
  Given an Observation with status "preliminary"
  When attempting to set status to "amended"
  Then the operation SHALL fail with 422 Unprocessable Entity

# Consent cannot have overlapping provisions
Scenario: Consent provisions must not overlap
  Given a Consent with two provisions
  When period.end of first > period.start of second
  Then validation SHALL fail with 422 Unprocessable Entity

```

-------

#### Summary of Lifecycle Resources

| | | | |
| :--- | :--- | :--- | :--- |
| ServiceRequest | `SVSServiceRequestReferral` | 360X referral workflow | Completed, Closed-Decline, Closed-Rejected, Closed-DNS, Cancelled |
| Task | `SVSTaskReferralTracking` | 360X task tracking | Completed, Cancelled, Failed |
| Observation (Panel) | `SVSObservationScreeningPanel` | Screening capture | Final, Amended, Corrected, Cancelled, Entered-in-error |
| DiagnosticReport | `SVSDiagnosticReportAssessment` | Assessment report | Final, Amended, Corrected, Appended, Cancelled, Entered-in-error |
| Consent | `SVSConsentOptOut` | Opt-out consent | Inactive, Entered-in-error |
| Communication | `SVSCommunicationAccommodation` | Accommodation notice | Completed, Superseded, Entered-in-error |
| DocumentReference | `SVSDocumentReferenceIP4` | Primary care documents | Superseded, Entered-in-error |

