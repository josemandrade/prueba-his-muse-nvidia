# Process (BPMN)

---

## BPMN Model

The following BPMN model represents the school vision screening workflow with three pools (organisations) and interoperability points marked.

![BPMN Model](images/02-bpmn-model.png)

*Click to view full-size. Use scroll/zoom controls.*

---

## Model Overview

### Pools (Organisations)
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

---

## Process Flow Summary

### Main Flow (left to right):
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

### Referral Waiting (with 4-week boundary timer):
- Wait for assessment
- **Referral Rejection** (360X PCC-56 Reject): Ophthalmology rejects → Nurse handles: Correct & Resend (back to Send Referral) OR Close Rejected Referral (notify Parent & Primary Care, IP-4)
- **4-Week Timer fires** → **Cancel Original Referral** at Ophthalmology (360X PCC-58 Close: No Response Within 4 Weeks) → Nurse contacts parent, checks appointment, re-issues **new referral** (fresh lifecycle, new Referral ID) → back to Send Referral

### Assessment Received:
- **Assessment Outcome Gateway:**
  - **Seen**: Process assessment → send summary to Nurse (IP-3, 360X PCC-61), full report to Primary Care (IP-3)
    - Nurse generates Teacher Accommodation (IP-5) → sends to Teacher
    - Close referral, archive
  - **DNA (Did Not Attend)**: Nurse contacts parent, offers **one re-referral**
    - **Parent Accepts Re-Referral**: Create new referral with new appointment → back to Send Referral
    - **Parent Declines OR 2nd DNA**: Close referral as DNA, notify Primary Care (IP-4)

### End-of-Year Handling:
- **End of School Year** boundary event on Screening Day loop (timer cycle R/P1Y)
- Children with pending re-screen (absent/incomplete) → Record as Missed, notify parent, notify Primary Care (IP-4)

**Loop continues** until all children screened → **Screening Year Complete**, archive records.

---

## Interoperability Points (Marked in BPMN with Message Flows)

| PI ID | Name | Source Task | Target | Data Payload | IHE Profile |
|-------|------|-------------|--------|--------------|-------------|
| **IP-1** | Screening Result Capture | `Task_PerformScreening` → `Task_RecordPass/Refer/Absent/Incomplete` | School Health Record (internal) | Child ID, screening date, test used, right/left acuity, outcome, screener | — |
| **IP-2a** | Referral Dispatch | `Task_SendReferral` | Ophthalmology Clinic | Referral letter: child ID, DOB, school/grade, screening date, acuity per eye, test used, reason, screener contact | **360X PCC-55** |
| **IP-2b** | Cancel Referral (Timeout) | `Task_CancelReferral` | Ophthalmology Clinic | 360X PCC-58 Close: reason "No Response Within 4 Weeks" | **360X PCC-58** |
| **IP-2c** | Referral Rejection Response | Ophthalmology Clinic | `Task_WaitAssessment` (boundary) | 360X PCC-56 Reject with reason | **360X PCC-56** |
| **IP-3a** | Assessment Return — Summary | Ophthalmology Clinic | `Task_NurseReceiveSummary` | Diagnosis, prescription summary, follow-up plan | **360X PCC-61**, **MHD ITI-65** |
| **IP-3b** | Assessment Return — Full | Ophthalmology Clinic | `Task_PrimaryCareReceiveAssessment` | Full assessment: diagnosis, prescription, follow-up plan, outcome | **MHD ITI-65** |
| **IP-4a** | Primary Care Receives Screening (Pass) | `Task_RecordPass` | Primary Care Team | Screening result: pass, acuity values | **MHD ITI-65** |
| **IP-4b** | Primary Care Receives Screening (Decline) | `Task_RecordDecline` | Primary Care Team | Screening result + decline reason | **MHD ITI-65** |
| **IP-4c** | Primary Care Receives DNA Closure | `Task_CloseAfterDNA` | Primary Care Team | DNA closure notification | **MHD ITI-65** |
| **IP-4d** | Primary Care Receives Missed Screening | `Task_RecordMissed` | Primary Care Team | Screening not completed (2nd absent) | **MHD ITI-65** |
| **IP-4e** | Primary Care Receives Rejected Referral | `Task_CloseRejectedReferral` | Primary Care Team | Referral rejected & closed | **MHD ITI-65** |
| **IP-4f** | Primary Care Receives End-of-Year Missed | `Task_HandleEndOfYearPending` | Primary Care Team | End-of-year missed screening (pending re-screen) | **MHD ITI-65** |
| **IP-5** | Teacher Accommodation | `Task_SendAccommodation` | Teacher (internal) | Accommodation needed: glasses, front seat | Internal |

---

## BPMN Validation

- **Mechanical validation:** ✅ 0 diagonal edges, 0 segments crossing figure interior
- **Task count:** 33
- **Gateways:** 10
- **Events:** 4 (1 start, 1 end, 2 boundary timers)
- **Sequence flows:** 54
- **Message flows:** 12
- **Validation date:** 2026-11-19
- **BPMN version:** 2.0

---

## Key BPMN Patterns Used

1. **Boundary Timer Event** on `Task_WaitAssessment` (4-week deadline) — models nurse's escalation when ophthalmology doesn't return assessment; cancels activity, triggers cancellation of original referral
2. **Boundary Timer Event** on `Task_ScreeningDay` (End of School Year, cycle R/P1Y) — handles pending re-screens at year end
3. **Exclusive Gateways** for all decision points
4. **Loop Back** for re-screening (absent/incomplete) and re-referral (DNA)
5. **Data Objects** for attempt counters and opt-out list — gateway conditions evaluate process variables
6. **Message Flows** between pools for each interoperability point
7. **360X Transaction Mapping**: PCC-55 (Submit), PCC-56 (Accept/Reject), PCC-58 (Close), PCC-61 (Retrieve Report)