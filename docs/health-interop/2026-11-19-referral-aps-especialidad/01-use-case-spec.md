# Use Case Specification: Derivación APS → especialidad con contrareferencia

## 1. Clinical Problem

A primary-care (APS) doctor identifies a health problem that exceeds APS resolutive
capacity and must be assessed by a specialist. Today the referral travels by paper,
form, phone, or disconnected systems, with no reliable feedback loop: APS does not
know whether the specialty accepted the referral, when the appointment is, whether
the patient attended, or what the specialist decided. Referrals get lost, patients
wait without information, and the counter-referral — the diagnosis, plan and
follow-up indications the specialist owes back to APS — often never arrives, breaking
continuity of care.

This use case builds the closed loop: APS creates the referral, the specialty accepts
or rejects it, schedules and attends, and returns a counter-referral; APS tracks the
referral state at any time and retrieves the result. The flow is longitudinal (days
to weeks between steps) and multi-encounter (an APS visit and a specialty visit),
with an explicit state machine. It is a request/workflow case, not an
episode-notification case: the state of the referral is itself the data APS needs
most of the time.

## 2. Users, Roles, and Departments

| Role | Department / Organisation | What they do | What they see | What they decide |
|------|---------------------------|--------------|---------------|------------------|
| APS doctor | APS (CESFAM) | Identifies the need for specialty assessment, creates the referral, receives the counter-referral, continues follow-up in APS | Patient identity and clinical summary, referral state, counter-referral (diagnosis, plan, follow-up) | Whether to refer; which specialty/service; priority; follow-up in APS after the counter-referral |
| APS admin | APS (CESFAM) | Registers and tracks the referral, informs the patient of the referral creation, of acceptance/rejection, and of the counter-referral outcome; is notified of the appointment offer, retrieves the counter-referral | Referral state, appointment date, patient contact data | When to chase a missing status change; when to escalate to the APS doctor |
| Referral hub operator | Referral hub | Receives the referral, routes it to the requested specialty service, holds the referral state, answers status queries, escalates on timeout | Referral state and routing data — not the full clinical detail | Routing to the specialty service; escalation on timeout |
| Specialty scheduler | Specialty service (e.g. cardiology) | Books and re-schedules the appointment, offers the appointment to the patient, chases an unconfirmed offer | Referral content, service capacity, appointment availability | Appointment slot; re-scheduling; chasing an unconfirmed offer |
| Triage clinician | Specialty service | Clinically triages the referral: accepts it (naming the service/practitioner who takes it) or rejects it with a reason | Referral content, service capacity | Accept or reject; accepting service/practitioner |
| Specialist | Specialty service | Attends the patient, records diagnosis and plan, issues the counter-referral | Referral content, patient identity, prior results | Diagnosis, plan, follow-up indications, follow-up plan |
| Patient | — | Receives notifications, attends the appointment | Own referral state, appointment date, outcome | Whether to accept the referral itself at creation; whether to attend; whether to accept a re-scheduled appointment |
| MPI | Master Patient Index (system) | Resolves patient identity across organisations | Identity cross-references | Identity matches (no clinical decisions) |

## 3. Data Flow Summary

### 3.1 The referral lifecycle (state machine)

One referral moves through these states, in one of two paths:

- Accepted path: `requested → received → accepted → scheduled → completed → counter-referred`
- Rejected path: `requested → received → rejected → APS re-triage → [new referral | different specialty | resolve in APS] → closed as rejected`

A re-referral after a rejection is a NEW referral; the first referral closes as
`rejected` only once APS has decided the re-triage outcome. A referral that
returns to APS for re-triage after a scheduling failure (§3.4) follows the same
re-triage outcomes ([new referral | different specialty | resolve in APS]) and
closes as `rejected` once APS has decided.

Terminal states: `counter-referred` (successful completion), `rejected` (once
APS has decided the re-triage outcome), `no-show` (after a failed re-scheduling,
see §3.4), `cancelled`. Cancellation is
possible at any point before completion and can be requested by APS, by the
patient, or by the specialty: an already-booked appointment is cancelled and all
parties are notified. A referral also closes as `cancelled` (reason "patient
deceased") if the patient dies while the referral is open; APS and the specialty
are notified.

- **Who tracks the status:** the APS doctor and APS admin own the referral; the hub
  holds the referral state and answers status queries.
- **Who is informed at each state change:** APS (doctor and admin) at every change.
  The patient is informed at each step by a named sender: at referral creation by
  the APS admin; at acceptance/rejection by the APS admin; at the appointment offer
  by the specialty scheduler, sent via the hub, with the APS admin notified of the
  offer; at the counter-referral outcome by the APS admin.

### 3.2 PI-0 Creation and push of the referral (APS → hub → specialty)

- Input: patient identity, patient contact data, reason for referral, clinical
  summary, relevant exams and results, requesting practitioner, requested
  specialty/service, priority (routine / urgent, assigned by the APS doctor at
  referral creation; urgent halves the acceptance SLA, see §3.8).
- The referral is created once, in the APS encounter, and pushed to the hub, which
  routes it to the requested specialty service.
- If the patient declines the referral itself at creation, NO referral is created;
  APS records the decision and the reason in the APS record.
- The referral carries a minimum data set (see §3.7); nothing outside it travels
  at this point.

### 3.3 PI-1 Acceptance / rejection (specialty → hub → APS)

- The triage clinician triages the referral and either **accepts** it (naming
  the service/practitioner who takes it) or **rejects** it with a reason.
- A rejection loops back to APS: the APS doctor re-triages within **5 working
  days** of the rejection — re-refer with more information (a NEW referral),
  refer to a different specialty, or resolve the problem in APS. On expiry of
  the 5 working days the hub escalates to APS (notifies the APS admin and the
  APS doctor). The referral is closed as `rejected` only once APS has decided
  the re-triage outcome.
- The acceptance/rejection decision is the state change APS waits for first (see
  §3.8 for the wait).

### 3.4 PI-2 Scheduling (specialty ↔ patient, via hub)

- Once accepted, the specialty scheduler offers an appointment; the patient has
  **3 working days** to confirm it. On expiry the scheduler chases the patient
  once; if the offer is still unconfirmed after a further 3 working days, the
  scheduler chases once more (second chase); if the offer is still unconfirmed
  after that second chase, the referral returns to APS for re-triage. If the
  patient declines the offered appointment, the scheduler offers another slot
  (one re-offer). After a second decline, the referral returns to APS for
  re-triage. The APS re-triage after a scheduling failure follows the same
  outcome options as the re-triage after a rejection ([new referral |
  different specialty | resolve in APS]), and the first referral closes as
  `rejected` once APS has decided.
- On conflict the appointment is re-scheduled; re-scheduling is a loop, not a new
  referral. A capacity conflict is detected by the specialty scheduler; a
  conflict with the patient's own availability is detected by the patient.
- **No-show:** if the patient does not attend, one re-scheduling is offered.
  The re-scheduled offer follows the same confirm/chase rules as the first
  offer: 3 working days to confirm, the scheduler chases on expiry (once, then
  once more after a further 3 working days), one re-offer on decline; a second
  decline, or an offer still unconfirmed after the second chase, sends the
  referral back to APS for re-triage, as in the confirm loop. If the patient
  does not attend the second appointment either, the referral closes as
  `no-show` and APS is informed.

### 3.5 PI-3 Counter-referral return (specialty → hub → APS)

- After the specialty encounter, the specialist returns the counter-referral:
  diagnosis, plan, and follow-up indications, plus a follow-up plan for APS.
- APS retrieves the counter-referral (it is pushed to APS and APS acknowledges
  receipt); the referral reaches its final state, `counter-referred`. The hub
  routes the counter-referral through (transit) but does not retain the clinical
  detail.
- The follow-up plan tells APS what to do next: controls, exams, or a new referral
  if the problem needs another specialty.

### 3.6 PI-4 Status query (APS → hub)

- At any time, APS queries the current state of the referral; the hub answers from
  the referral state it holds.
- The query never changes the state; it only reads it.

### 3.7 Minimum data set

- **PI-0 (referral):** patient identity, patient contact data, reason for
  referral, clinical summary, relevant exams/results, requesting practitioner,
  requested specialty/service, priority (routine / urgent, assigned by the APS
  doctor at referral creation).
- **PI-1 (accept/reject):** decision, accepting service/practitioner, or rejection
  reason.
- **PI-2 (scheduling):** appointment date/time, place, preparation instructions.
- **PI-3 (counter-referral):** diagnosis, plan, follow-up indications, follow-up
  plan for APS.
- **PI-4 (status query):** current state, last state change, next expected step.

### 3.8 Waits and timeouts (SLAs)

- Acceptance decision (PI-1): **5 working days** from referral creation
  (**2 working days** for urgent referrals).
- Appointment offered (PI-2): **10 working days** from acceptance.
- Appointment confirmation: **3 working days** from the offer; the scheduler
  chases on expiry (see §3.4).
- Counter-referral (PI-3): **5 working days** from the specialty encounter.
- Re-triage decision after a rejection: **5 working days** from the rejection;
  on expiry the hub escalates to APS (notifies the APS admin and the APS
  doctor).
- On timeout of the acceptance, appointment-offer, or counter-referral SLAs:
  the hub escalates to the specialty service and notifies APS.

## 4. Consent and Legal Basis

- The referral is part of the care relationship: sharing the referral data with the
  requested specialty is covered by that relationship; no separate consent is
  requested for the referral itself.
- No legal mandate for reporting: this is care coordination, not a mandated report.
- The patient is informed of the referral and of each state change that concerns
  them, by a named sender: referral creation by the APS admin; acceptance/rejection
  by the APS admin; appointment offer by the specialty scheduler via the hub (APS
  admin notified of the offer); counter-referral outcome by the APS admin.

## 5. Data Governance

- The referral record and the counter-referral are part of the patient's clinical
  record; each organisation retains its copy under its own records policy.
- The hub holds the referral state and routing data for tracking and status
  queries, not the full clinical detail. It routes referrals and
  counter-referrals through (transit) but does not retain the clinical detail.
- Patient identity is resolved through the MPI; no local identifier travels without
  the MPI key.
- No real patient data in this design — synthetic data only for examples and tests.

## 6. Success Criteria (Concrete Example)

**Scenario (cardiology):** María González, 58 years old, RUN 11.111.111-1
(synthetic), APS CESFAM Los Aromos. Her APS doctor refers her to cardiology for
suspected heart failure (exertional dyspnoea, ankle oedema; ECG and labs attached).

- Referred 2026-11-19 → accepted by cardiology 2026-11-24 → appointment
  2026-12-02 → attended; diagnosis heart failure with reduced ejection fraction,
  plan and follow-up indications recorded → counter-referral returned 2026-12-04
  → APS retrieves it the same day and continues follow-up in APS.
- Every step traceable; APS knows the state at any time; the patient is informed
  at creation, of the acceptance, of the appointment, and of the outcome.

**Rejection scenario:** cardiology rejects the referral — reason: missing
echocardiogram. APS re-triages: orders the echocardiogram and creates a NEW
referral with the result attached. The first referral closes as `rejected` only
after the APS re-triage decision.

**No-show scenario:** patient misses the 2026-12-02 appointment → one
re-scheduling offered for 2026-12-09 → patient attends.

**Timeout scenario:** no acceptance decision by 2026-11-26 (5 working days) → the
hub escalates to cardiology and notifies APS.

## 7. Out of Scope

- Real patient data, production EHR access, clinical decision support.
- Direct integration with a specific EHR vendor system (design for
  interoperability, not a specific product).
- Billing, insurance, or financial workflows.
- Emergency care pathways (emergency department, SAMU) — the referral covers
  elective and urgent specialty care, not emergencies.
- Referrals outside the network.

## 8. Design Note

This use case has five interoperability points:

1. **PI-0 referral creation and push** — APS creates the referral with its minimum
   data set and pushes it through the hub to the specialty.
2. **PI-1 accept / reject** — the specialty triages and decides; a rejection loops
   back to APS for re-triage.
3. **PI-2 scheduling** — the specialty offers the appointment; re-scheduling is a
   loop; a no-show closes the referral after one failed re-scheduling.
4. **PI-3 counter-referral return** — the specialty returns diagnosis, plan,
   follow-up indications, and a follow-up plan for APS.
5. **PI-4 status query** — APS reads the current referral state from the hub at
   any time; the query never changes the state.

Cross-resource decisions (to be modelled in step 4, not decided here): one
referral is one request plus one workflow state record; the state lives in the
workflow record, not in the request status, and the two are kept consistent; the
referral spans several encounters (APS visit, specialty visit), all linked to the
referral; the hub routes the referral and holds its state but not the full clinical
detail (transit, not storage). Consent, purpose, and retention are recorded in §4–§5.

Next step: IHE landscape scan, then BPMN modeling of this process with the
interoperability points marked.
