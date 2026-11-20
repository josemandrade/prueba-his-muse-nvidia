# BPMN Model: School Vision Screening

## IHE Landscape Scan

**Date checked**: 2026-11-19  
**Source**: https://profiles.ihe.net/ (PCC, ITI, EYECARE, QRPH domains checked live)

| Profile | Domain | Version / Status | Actors / Transactions | Relevance to This Use Case |
|---------|--------|------------------|----------------------|----------------------------|
| **360X** (Closed Loop Referral) | PCC | Suppl. Revised 2021-04-14 (TI) | Referral Initiator, Referral Recipient, Referral Tracker / PCC-55 Submit Referral, PCC-56 Accept/Reject, PCC-57 Update Status, PCC-58 Close, PCC-59 Query Status, PCC-60 Retrieve Referral, PCC-61 Retrieve Report | **Primary candidate** — exactly matches the referral from school nurse to ophthalmologist with tracking, acceptance, status updates, and closure. Covers the 4-week deadline and DNA/re-referral paths. |
| **XBeR-WD** (Basic eReferral Workflow Definition) | PCC | Suppl. Revised 2013-10-04 (TI) | Workflow definition for eReferral (XDW-based) | Complements 360X — provides executable workflow definition for the referral process. Could model the absent/incomplete/decline/DNA branches. |
| **MHD** (Mobile Access to Health Documents) | ITI | Release 4.2.5 (FHIR R4), Revised 2026-10-18 (FT) | Document Source, Recipient, Consumer, Registry, Repository / ITI-65 Provide Document Bundle, ITI-66 Find Document Lists, ITI-67 Retrieve Document, ITI-68 Search, ITI-69 Retrieve | **Strong candidate** — FHIR REST document exchange for screening results, referral letters, ophthalmology assessments between school, eye clinic, primary care. Normative, widely implemented. |
| **MHDS** (Mobile Health Document Sharing) | ITI | Release 2.3.1, Revised 2023-08-04 (TI) | Similar to MHD but for health document sharing | Alternative to MHD if XDS.b affinity domain model preferred; less common for new FHIR implementations. |
| **DSUBm** (Document Subscription for Mobile) | ITI | Release 1.0.0, Published 2024-02-29 (TI) | Document Subscriber, Document Publisher / ITI-110 Subscribe, ITI-111 Unsubscribe, ITI-112 Notify | **Candidate** — nurse/primary care subscribe to ophthalmology assessment documents; notify when available (replaces polling). |
| **PIXm** (Patient Identifier Cross-reference for Mobile) | ITI | Release 3.1.0, Revised 2025-11-06 (TI) | Patient Identifier Cross-reference Consumer, Manager / ITI-83 PIXm Query, ITI-84 PIXm Feed | **Candidate** — link child's school record, ophthalmology record, primary care record across domains. |
| **PDQm** (Patient Demographics Query for Mobile) | ITI | Release 3.2.0, Revised 2025-11-06 (TI) | Patient Demographics Consumer, Supplier / ITI-78 PDQm Query | **Candidate** — nurse/ophthalmologist look up child demographics in primary care or MPI before screening/assessment. |
| **PMIR** (Patient Master Identity Registry) | ITI | Release 1.6.0, Revised 2025-11-06 (TI) | Patient Identity Registry, Consumer / ITI-93 Register, ITI-94 Revise | **Candidate** — if a national/regional MPI exists, use for golden record; otherwise PIXm/PDQm suffice. |
| **Scheduling** | ITI | Release 1.0.0, Published 2024-12-12 (TI) | Scheduling Client, Server / ITI-115–118 (Slot, Appointment, Schedule CRUD) | **Candidate** — parent books ophthalmology appointment; nurse tracks appointment status. |
| **EC-Summary** (Eye Care Summary Record) | EYECARE | Published 2017-09-15 (TI) | Content profile for eye care summary document | **Candidate** — standardizes the ophthalmology assessment content (diagnosis, prescription, follow-up). CDA-based; FHIR equivalent would be custom. |
| **GEE** (General Eye Evaluation) | EYECARE | Revised 2016-12-29 (TI) | C-CDA based general eye evaluation content | Alternative to EC-Summary; CDA-based. |
| **DCP** (Dynamic Care Planning) | PCC | Suppl. Revised 2019-09-27 (TI) | Care Plan Contributor, Manager / PCC-37–41 | **Candidate** — if the follow-up plan (patching, review interval) is managed as a shared care plan across nurse, ophthalmologist, primary care. |
| **DCTM** (Dynamic Care Team Management) | PCC | Published 2017-09-08 (TI), v2.0 PC 2019-12-31 | Care Team Manager, Member / PCC-42–46 | **Candidate** — if the child's care team (nurse, ophthalmologist, primary care, parent) is explicitly managed. |
| **IPS / FIPS / sIPS** (International Patient Summary) | PCC / ITI | IPS Revised 2023-10-09 (TI); FIPS PC 2026-03; sIPS Published 2023-11-17 | IPS content + MHD/sIPS sharing | **Set aside** — this use case is not a patient summary exchange (not cross-border, not portable record). The screening result and ophthalmology assessment are encounter-specific documents, not a summary. |
| **ATNA** (Audit Trail and Node Authentication) | ITI | Normative (FT) | Secure Node, Audit Record Repository / ITI-19, ITI-20 | **Infrastructure** — required for all production exchanges; not an interoperability point per se. |
| **CT** (Consistent Time) | ITI | Normative (FT) | Time Client, Time Server | **Infrastructure** — timestamp consistency across systems. |
| **BPPC / APPC / PCF** (Consent) | ITI | BPPC FT; APPC Revised 2021-07-02 (TI); PCF Release 1.1.0 Revised 2024-02-23 (TI) | Consent Manager, Consumer, Enforcement Point | **Set aside** — consent model is opt-out at school year start, not per-encounter treatment consent. No legal mandate. Privacy consent not the primary interoperability point. |
| **mADX** (Mobile Aggregate Data Exchange) | QRPH | Revised 2025-09-19 (TI) | Aggregate Report Sender, Receiver / QRPH-58, QRPH-59 | **Set aside** — no aggregate/public health reporting mandate for this screening program. |
| **EHDI / EHDI-WD** (Early Hearing Detection) | QRPH | Revised 2016-08-10 / 2019-08-30 (TI) | Workflow for newborn hearing screening | **Set aside** — different domain (hearing vs vision), different population (newborn vs school-age). No vision-screening equivalent in QRPH. |
| **SDC** (Structured Data Capture) | QRPH | Revised 2021-05-14 (TI) | Form Manager, Form Filler, Form Receiver | **Set aside** — the screening form is simple structured data, not a complex dynamic form. FHIR Questionnaire/Observation suffices. |

### Interoperability Points from Use Case Spec (Section 8)

| # | Interoperability Point | Description | Candidate Profiles from Scan |
|---|------------------------|-------------|------------------------------|
| IP-1 | **Screening result capture** | Nurse records structured screening data (acuity per eye, test used, outcome: pass/refer/absent/incomplete) | MHD (document), FHIR Observation/QuestionnaireResponse (custom), PIXm/PDQm (patient lookup) |
| IP-2 | **Referral dispatch** | Structured referral from nurse to ophthalmology with 4-week deadline tracking, parent decline handling, rejection handling | **360X** (primary: PCC-55, PCC-56, PCC-58), XBeR-WD (workflow), MHD (document transport), Scheduling (appointment), PIXm/PDQm (patient match) |
| IP-3 | **Assessment return** | Structured feedback from ophthalmology to school nurse (summary) and primary care (full) with DNA/re-referral handling | **360X** (PCC-61, status/closure), MHD (document), DSUBm (notification), EC-Summary/GEE (content), PIXm/PDQm (patient match) |
| IP-4 | **Primary care receive** | Screening result + ophthalmology assessment entered in child's health record (pass, decline, missed, DNA, rejected, end-of-year missed) | MHD, PIXm/PDQm/PMIR |
| IP-5 | **Teacher accommodation** | Nurse generates accommodation notice from ophthalmology feedback (glasses, front seat) | Internal only — no IHE profile; FHIR Communication or custom |

---

## BPMN Model Description

### Pools (Organizations)
1. **School Health Service** — owns the screening process (main process)
2. **Ophthalmology Clinic / Hospital** — receives referral, returns assessment
3. **Primary Care Team** — receives screening results and assessments for health record

### Lanes (Roles within School Health Service)
- **School Nurse** — performs screening, manages referrals, follows up, generates accommodations
- **Child** — participates in screening
- **Parent / Guardian** — receives notifications, consents, takes child to appointments
- **Teacher** — receives accommodation notices only

### Data Objects (Process Variables)
| Data Object | Purpose |
|-------------|---------|
| `Opt-Out List` | Children opted out at school year start; read at "Check Opt-Out" |
| `Absent Attempt Count` | Tracks re-screen attempts for absent children (max 2) |
| `Incomplete Attempt Count` | Tracks re-screen attempts for incomplete screening (max 2) |
| `Active Referral ID` | Current referral identifier for 360X tracking |
| `Referral Status` | Current referral state (sent, accepted, rejected, closed, DNA) |

### Process Flow Summary

**Main Flow (left to right):**
1. **School Year Starts** → Opt-Out Consent distributed to parents
2. **Schedule Screening Sessions** for the year
3. **For each child (loop):**
   - Child presents for screening
   - **Check Opt-Out** (reads `Opt-Out List`) → if yes: record opt-out, next child
   - Perform visual acuity screening (Snellen/E/Lea)
   - **Screening Outcome Gateway** (4 branches):
     - **Pass** (≥6/9 both eyes): Record pass, notify parent (pass letter), send to Primary Care (IP-4) → Next Child
     - **Refer** (≤6/12 either eye OR ≥2 line diff): Create referral → **Parent Decision**
       - **Parent Declines**: Record decline + reason, send screening result to Primary Care (IP-4, no referral sent) → Next Child
       - **Parent Accepts**: Send referral to Ophthalmology (via parent), store Referral ID, start **4-week timer** (IP-2, 360X PCC-55)
     - **Absent**: Record absent, increment `Absent Attempt Count`, schedule re-screen within 2 weeks
       - **1st Absent**: Re-screen scheduled → loop back to Screening Day
       - **2nd Absent**: Record as Missed, notify parent, send "Screening Not Completed" to Primary Care (IP-4) → Next Child
     - **Incomplete** (uncooperative/one eye): Record incomplete + reason, increment `Incomplete Attempt Count`, schedule re-screen within 2 weeks
       - **1st Incomplete**: Re-screen scheduled → loop back to Screening Day
       - **2nd Incomplete**: **Direct Referral** to Ophthalmology with partial result noted (clinical decision, covered by opt-out consent) → Notify Parent → Send Referral (IP-2)

**Referral Waiting (with 4-week boundary timer):**
- Wait for assessment
- **Referral Rejection** (360X PCC-56 Reject): Ophthalmology rejects → Nurse handles: Correct & Resend (back to Send Referral) OR Close Rejected Referral (notify Parent & Primary Care, IP-4)
- **4-Week Timer fires** → **Cancel Original Referral** at Ophthalmology (360X PCC-58 Close: No Response Within 4 Weeks) → Nurse contacts parent, checks appointment, re-issues **new referral** (fresh lifecycle, new Referral ID) → back to Send Referral

**Assessment Received:**
- **Assessment Outcome Gateway:**
  - **Seen**: Process assessment → send summary to Nurse (IP-3, 360X PCC-61), full report to Primary Care (IP-3)
    - Nurse generates Teacher Accommodation (IP-5) → sends to Teacher
    - Close referral, archive
  - **DNA (Did Not Attend)**: Nurse contacts parent, offers **one re-referral**
    - **Parent Accepts Re-Referral**: Create new referral with new appointment → back to Send Referral
    - **Parent Declines OR 2nd DNA**: Close referral as DNA, notify Primary Care (IP-4)

**End-of-Year Handling:**
- **End of School Year** boundary event on Screening Day loop (timer cycle R/P1Y)
- Children with pending re-screen (absent/incomplete) → Record as Missed, notify parent, notify Primary Care (IP-4)

**Loop continues** until all children screened → **Screening Year Complete**, archive records.

### Interoperability Points (Marked in BPMN with Message Flows)

| PI ID | Name | Source Task | Target | Data Payload | Candidate Profiles |
|-------|------|-------------|--------|--------------|-------------------|
| **IP-1** | Screening Result Capture | `Task_PerformScreening` → `Task_RecordPass/Refer/Absent/Incomplete` | School Health Record (internal) | Child ID, screening date, test used, right/left acuity, outcome, screener | MHD, FHIR Observation, PIXm/PDQm |
| **IP-2a** | Referral Dispatch | `Task_SendReferral` | Ophthalmology Clinic | Referral letter: child ID, DOB, school/grade, screening date, acuity per eye, test used, reason, screener contact | **360X PCC-55**, MHD, Scheduling, PIXm/PDQm |
| **IP-2b** | Cancel Referral (Timeout) | `Task_CancelReferral` | Ophthalmology Clinic | 360X PCC-58 Close: reason "No Response Within 4 Weeks" | **360X PCC-58** |
| **IP-2c** | Referral Rejection Response | Ophthalmology Clinic | `Task_WaitAssessment` (boundary) | 360X PCC-56 Reject with reason | **360X PCC-56** |
| **IP-3a** | Assessment Return — Summary | Ophthalmology Clinic | `Task_NurseReceiveSummary` | Diagnosis, prescription summary, follow-up plan | **360X PCC-61**, MHD, DSUBm, EC-Summary |
| **IP-3b** | Assessment Return — Full | Ophthalmology Clinic | `Task_PrimaryCareReceiveAssessment` | Full assessment: diagnosis, prescription, follow-up plan, outcome | **360X**, MHD, DSUBm, EC-Summary |
| **IP-4a** | Primary Care Receives Screening (Pass) | `Task_RecordPass` | Primary Care Team | Screening result: pass, acuity values | MHD, PIXm/PDQm/PMIR |
| **IP-4b** | Primary Care Receives Screening (Decline) | `Task_RecordDecline` | Primary Care Team | Screening result + decline reason | MHD, PIXm/PDQm/PMIR |
| **IP-4c** | Primary Care Receives DNA Closure | `Task_CloseAfterDNA` | Primary Care Team | DNA closure notification | MHD, PIXm/PDQm/PMIR |
| **IP-4d** | Primary Care Receives Missed Screening | `Task_RecordMissed` | Primary Care Team | Screening not completed (2nd absent) | MHD, PIXm/PDQm/PMIR |
| **IP-4e** | Primary Care Receives Rejected Referral | `Task_CloseRejectedReferral` | Primary Care Team | Referral rejected & closed | MHD, PIXm/PDQm/PMIR |
| **IP-4f** | Primary Care Receives End-of-Year Missed | `Task_HandleEndOfYearPending` | Primary Care Team | End-of-year missed screening (pending re-screen) | MHD, PIXm/PDQm/PMIR |
| **IP-5** | Teacher Accommodation | `Task_SendAccommodation` | Teacher (internal) | Accommodation needed: glasses, front seat | Internal (FHIR Communication) |

### Key BPMN Patterns Used

1. **Boundary Timer Event** on `Task_WaitAssessment` (4-week deadline) — models the nurse's escalation when ophthalmology doesn't return assessment; cancels activity, triggers cancellation of original referral
2. **Boundary Timer Event** on `Task_ScreeningDay` (End of School Year, cycle R/P1Y) — handles pending re-screens at year end
3. **Exclusive Gateways** for all decision points (opt-out, screening outcome, parent decision, referral rejection, assessment outcome, re-referral decision, absent count, incomplete count, more children, end-of-year)
4. **Loop Back** for re-screening (absent/incomplete) and re-referral (DNA)
5. **Data Objects** for attempt counters and opt-out list — gateway conditions evaluate process variables
6. **Message Flows** between pools for each interoperability point (IP-2a/b/c, IP-3a/b, IP-4a–f, IP-5)
7. **360X Transaction Mapping**: PCC-55 (Submit), PCC-56 (Reject), PCC-58 (Close), PCC-61 (Retrieve Report)

### Validation Notes

- All sequence flows are orthogonal (horizontal/vertical only) — renderer will enforce
- No diagonal message flows — they connect pool boundaries vertically/horizontally
- Each interoperability point has a unique PI id and labeled message flow
- Boundary event labels are single-line, placed outside the task shape
- Pool/lane structure: 3 pools, 4 lanes in School pool
- Data objects provide gateway condition evaluation context
- Model validates structurally (XML well-formed, all refs resolve)
- Task count: 33, Gateways: 10, Events: 4, Sequence Flows: 54, Message Flows: 12

### Expert Review Findings Resolution

| ID | Finding | Resolution Applied |
|----|---------|-------------------|
| C1 | Original referral not cancelled on timeout | Added `Task_CancelReferral` (360X PCC-58 Close) before re-issuing; new referral = fresh lifecycle |
| C2 | Absent path loops indefinitely | Added `Absent Attempt Count` data object; 2nd attempt → `Task_RecordMissed` → notify parent + IP-4 to Primary Care |
| C3 | Incomplete path missing attempt counter | Added `Incomplete Attempt Count` data object; gateway evaluates count |
| C4 | No referral rejection path | Added PCC-56 Reject branch from `Task_WaitAssessment` → `Task_HandleReject` → Correct & Resend OR Close |
| C5 | Direct referral had duplicate Parent Decision | Replaced with `Task_NotifyParentDirectReferral` (inform only, covered by opt-out consent) |
| C6 | Pass path implicit parallel split | Restructured: Pass → `Task_RecordPass` → `Task_PrimaryCareReceiveScreening` → Next Child (sequential) |
| C7 | Teacher Accommodation not a message flow | Added `Task_SendAccommodation` with message flow IP-5 to School pool (Teacher lane) |
| C8 | Opt-Out check missing data source | Added `Opt-Out List` data object; read at `Gateway_CheckOptOut` |
| C9 | No end-of-year handling for pending re-screens | Added boundary timer event (R/P1Y) on `Task_ScreeningDay` → `Task_HandleEndOfYearPending` → IP-4 to Primary Care |

---

## Next Step

Proceed to **Step 3: Entities and Data** — list main entities and their data fields.