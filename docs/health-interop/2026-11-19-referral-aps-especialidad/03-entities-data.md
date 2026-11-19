# Entities and Data: Derivación APS → especialidad con contrareferencia

Use case: `01-use-case-spec.md` (validated 2026-11-19). BPMN:
`02-bpmn-model.md` + three parts (validated 2026-11-19). Pack
health-interop-superpowers v0.39.0.

Step 3 — Entities and data. Before any FHIR resource is chosen, this
file names the things the use case is about and the data each one
carries, in the same names as the spec and the BPMN. A name that
changes between files is a bug. Nothing here decides a FHIR resource
— that is step 4 (`04-fhir-proposal.md`).

## Entity index

| # | Entity | Definition (one line) | Owning system |
|---|--------|-----------------------|---------------|
| 1 | Patient | The person referred, identified through the MPI | APS EHR (record of care); MPI holds the cross-reference |
| 2 | Referral request | The APS request for specialty assessment, with its minimum data set | APS EHR (created); hub (routed copy, transit only) |
| 3 | Workflow state record | The referral's state, SLA clocks and loop counts, held by the hub | Referral hub |
| 4 | Triage decision | Accept (naming service/practitioner) or reject (with reason) | Specialty EHR |
| 5 | Appointment (+ Slot) | The offered/booked specialty appointment and its slot | Specialty EHR (scheduler) |
| 6 | Specialty encounter | The attended specialty visit | Specialty EHR |
| 7 | Counter-referral | Diagnosis, plan, follow-up indications + follow-up plan for APS | Specialty EHR (created); APS EHR (received copy) |
| 8 | Practitioner | APS doctor, APS admin, triage clinician, specialty scheduler, specialist, hub operator | Each practitioner's own organisation |
| 9 | Organisation / care service | APS (CESFAM), specialty service, referral hub | Directory (mCSD candidate); each organisation |
| 10 | MPI identity record | The cross-reference of the patient's identifiers across organisations | MPI |
| 11 | Notification | A named-sender notice to the patient, APS, or the specialty at a state change | The sender's system (APS EHR, hub, specialty EHR) |
| 12 | Declined-referral record | The APS record of a patient declining the referral at creation (no referral is created) | APS EHR |
| 13 | Cancellation record | A cancellation request + its reason, at any point before completion | Hub (recorded in the workflow state record); each party keeps its copy |

Names settled here: "referral request" is the request (one per
referral); "workflow state record" is the state holder (one per
referral, held by the hub); the two are kept consistent but are
different entities (spec §8 design note). "Re-triage" is a decision
on the workflow state record, not a new entity — a re-referral after
it is a NEW referral request. "Offer" is an appointment in state
`offered`, not a separate entity. "Escalation" is an event on the
workflow state record, not an entity. "Status query" (PI-4) is a read
of the workflow state record, not an entity.

## 1. Patient

- Definition: the person the APS doctor refers to the specialty. The
  worked example is María González, 58, RUN 11.111.111-1 (synthetic),
  APS CESFAM Los Aromos.
- Owning system: APS EHR holds the patient record; the MPI holds the
  identity cross-reference (§10). No local identifier travels without
  the MPI key (spec §5).
- Identifiers: MPI key (primary for cross-organisation travel);
  local APS patient identifier (APS-internal); national identifier
  (RUN, synthetic in examples). Dedup key: MPI key + patient.
- Lifecycle states: none in this use case — the patient is not
  created, changed, or closed by the referral flow. The patient record
  itself lives outside this case.
- Late / out-of-order: identity is resolved through the MPI
  before the referral is created (BPMN Part A), so a referral
  never arrives with an identifier the MPI cannot resolve — there
  is no "identity pending" hold. An identity merge after creation
  is covered by §10.
- Correction: identity corrections happen in the MPI (merge /
  link — see §10), never by editing a referral's patient field in
  flight; a corrected identity re-issues the MPI key to the hub, which
  updates the workflow state record.

| Field | Required / optional / derived | Source | Form |
|-------|-------------------------------|--------|------|
| MPI key | Required | MPI (§10) | Identifier (coded) |
| Full name | Required | APS EHR | Structured text |
| Date of birth / age | Required (age in the worked example: 58) | APS EHR | Structured (date) |
| National identifier (RUN) | Required in the worked example; synthetic only | APS EHR | Identifier |
| Contact data (phone, address, preferred channel) | Required (C12 — part of the PI-0 minimum data set) | APS EHR (patient-supplied) | Structured |
| Sex / gender as recorded | Optional | APS EHR | Coded |

Missing contact data blocks the referral: the scheduler cannot offer
or chase without it, so APS must complete it before creation (the
creation task fails validation, it does not create a referral with a
blank contact). Out-of-date contact data is corrected in the APS EHR;
the correction is pushed to the hub as a workflow-record update, and
the hub forwards it to the specialty if the referral is already
routed.

## 2. Referral request

- Definition: the APS request for specialty assessment, created once
  in the APS encounter and pushed through the hub to the requested
  specialty service. Carries the PI-0 minimum data set (spec §3.7);
  nothing outside it travels at creation.
- Owning system: APS EHR creates and owns it; the hub holds a routed
  copy in transit only (it does not retain the clinical detail —
  C10); the specialty EHR holds its received copy.
- Identifiers: referral identifier (created by APS at creation,
  persistent until the loop closes — the same identifier the 360X
  pattern keeps for the closed loop); patient MPI key (§1). Dedup
  key: referral identifier + patient MPI key. A second referral for
  the same patient and specialty is a NEW referral identifier, never
  a reuse.
- Lifecycle states (the request's own states — the workflow state
  record in §3 is the authority for where the referral stands; the
  two are kept consistent, spec §8):

| State | Who may change it | Meaning |
|-------|-------------------|---------|
| `draft` | APS doctor | Being written in the APS encounter; not yet sent |
| `requested` | APS doctor (create) | Sent to the hub (PI-0); the acceptance clock starts |
| `received` | Hub (route) / specialty (receipt) | At the requested specialty service |
| `accepted` | Triage clinician (via §4) | The specialty takes it; scheduling may start |
| `rejected` | Triage clinician (via §4) / Hub operator (scheduling-failure return) | The specialty declines it with a reason, or scheduling failed and the referral returned; APS re-triages |
| `scheduled` | Specialty scheduler (via §5) | Appointment booked |
| `completed` | Specialist (encounter done, §6) | Specialty visit attended |
| `counter-referred` | Specialist (via §7) | Terminal — counter-referral returned |
| `no-show` | Specialist (second no-show, §5) | Terminal — APS informed |
| `cancelled` | APS / patient / specialty (§13) | Terminal — any point before completion |

- Late / out-of-order: a referral arriving at the specialty after
  the hub already recorded a cancellation is rejected by the
  specialty's receipt check against the workflow state record — the
  hub's record is the authority, and a cancelled referral cannot
  advance (BPMN modeling note). A duplicate push of the same referral
  identifier is ignored by the hub (dedup on the referral
  identifier).
- Correction: a referral's clinical content is corrected by a new
  version from APS (same referral identifier, version number +1,
  superseding the previous version); the hub forwards the new version
  to the specialty and the workflow state record notes the
  supersession. A referral is never edited in place by the specialty
  or the hub. A re-referral after rejection is a NEW referral
  identifier, not a correction.

| Field | Required / optional / derived | Source | Form |
|-------|-------------------------------|--------|------|
| Referral identifier | Required | APS EHR (created) | Identifier |
| Patient (MPI key + contact data) | Required | APS EHR / MPI (§1) | Identifier + structured |
| Reason for referral | Required | APS doctor, in the APS encounter | Coded (SNOMED CT) + free-text note |
| Clinical summary | Required | APS EHR (APS doctor) | Free text (structured sections) |
| Relevant exams / results | Required if they exist (e.g. ECG, labs in the worked example) | APS EHR / laboratory | Coded (LOINC) + values; attachments by reference |
| Requesting practitioner | Required | APS EHR (APS doctor) | Reference (§8) |
| Requested specialty / service | Required | APS doctor, from the local specialty/service catalogue | Coded (local catalogue) |
| Priority | Required — `routine` / `urgent`, assigned by the APS doctor at creation (C6/Q6) | APS doctor | Coded; drives the acceptance SLA (2 vs 5 working days) |
| Creation date/time | Required (derived — stamped at creation) | APS EHR | Structured (date/time) |

Missing reason, specialty, or priority blocks creation (the APS
creation task fails validation). Missing exams are allowed only when
none exist — the field is "relevant exams", not "all exams"; an empty
list means none were relevant, and the specialty may reject for a
missing exam (the worked rejection scenario: missing
echocardiogram). The specific LOINC codes for the exams in the worked
example are pinned in step 4, not here.

## 3. Workflow state record

- Definition: the referral's state, SLA clocks, and loop counts, held
  by the hub. One referral = one request (§2) + one workflow state
  record; the state lives here, not in the request status (spec §8).
  This is the entity PI-4 reads and every later step reads first.
- Owning system: referral hub. The hub holds state and routing data
  for tracking and status queries, not the full clinical detail
  (C10 — transit, not storage).
- Identifiers: referral identifier (§2, the join key); workflow
  record identifier (hub-internal). Dedup key: referral identifier.
- Lifecycle states (the two-path state machine, spec §3.1, BPMN
  § State machine):

| State | Who may change it | Meaning |
|-------|-------------------|---------|
| `requested` | APS (creation, PI-0) | Created, pushed to the hub |
| `received` | Hub (routing, PI-0 second leg) | At the requested specialty service |
| `accepted` | Triage clinician (PI-1) | Specialty takes it |
| `rejected` | Triage clinician (PI-1) / Hub operator (scheduling-failure return) | Specialty declines, or scheduling failed and the referral returned; APS re-triage pending |
| `scheduled` | Specialty scheduler (PI-2) | Appointment booked |
| `completed` | Specialist (encounter, §6) | Specialty visit attended |
| `counter-referred` | Specialist (PI-3) | Terminal — successful completion |
| `no-show` | Specialist (second no-show) | Terminal — APS informed |
| `cancelled` | APS / patient / specialty (§13) | Terminal — any point before completion |

  Re-triage is not a state: it is the APS decision that follows
  `rejected` (or a scheduling-failure return). The first referral
  closes as `rejected` only once APS has decided the re-triage
  outcome (N1); until then it stays `rejected` with the re-triage
  clock running. That holds for a scheduling-failure return too:
  when the referral returns for re-triage after a scheduling
  failure, its state moves to `rejected` at the return (the
  scheduling path failed; APS re-triages into the shared re-triage
  entry — BPMN Part B returns land on the Part A re-triage entry),
  and the re-triage deadline runs 5 working days from the return.
- Late / out-of-order: a state change arriving for a referral
  already in a terminal state is rejected by the hub (the record is
  the authority — a cancelled referral cannot advance). A state
  change arriving out of order (e.g. `scheduled` before `accepted`)
  is rejected; the sender is told the current state. Duplicate
  deliveries of the same state change (same referral identifier +
  same transition) are ignored.
- Correction: states are never edited in place. A wrong state change
  is corrected by a compensating transition recorded as a new entry
  in the state history (who, when, from, to, reason); the history is
  append-only. The `cancelled` state has one correction path only:
  a cancellation recorded in error is undone by re-opening the
  referral to its pre-cancellation state with an explicit
  re-open entry — the hub operator performs it, APS and the specialty
  are notified.

| Field | Required / optional / derived | Source | Form |
|-------|-------------------------------|--------|------|
| Referral identifier | Required | APS (§2) | Identifier (join key) |
| Current state | Required | Hub (transitions above) | Coded (the state list) |
| State history (state, timestamp, actor, reason) | Required (derived — append-only) | Hub | Structured |
| Last state change (timestamp) | Required (derived) | Hub | Structured (date/time) |
| Next expected step | Required (derived from current state) | Hub | Coded text (e.g. "acceptance decision", "appointment offer", "counter-referral") |
| Acceptance deadline | Required (derived — 5 working days from creation, 2 if urgent) | Hub (from §2 priority + creation time) | Structured (date/time) |
| Offer deadline | Required (derived — 10 working days from acceptance) | Hub | Structured (date/time) |
| Counter-referral deadline | Required (derived — 5 working days from the encounter) | Hub | Structured (date/time) |
| Re-triage deadline | Required when re-triaging (derived — 5 working days from the re-triage trigger: the rejection, or the scheduling-failure return) | Hub | Structured (date/time) |
| Confirmation deadline | Required when an offer is open (derived — 3 working days from the offer) | Specialty scheduler, via the hub | Structured (date/time) |
| Decline count (this offer) | Required (derived — 0, 1, 2; resets per offer) | Specialty scheduler, via the hub | Integer |
| Chase count (this offer) | Required (derived — 0, 1, 2; resets per offer) | Specialty scheduler, via the hub | Integer |
| Re-scheduling count | Required (derived — 0 or 1) | Specialty scheduler, via the hub | Integer |
| Escalation history (SLA breached, escalated to, timestamp) | Required when a breach occurs | Hub | Structured |
| Accepting service / practitioner | Required once accepted | Triage clinician (§4) | Reference (§8/§9) |
| Rejection reason | Required when `rejected` | Triage clinician (§4) | Coded + free text |
| Cancellation reason | Required when `cancelled` | Requester (§13) | Coded + free text ("patient deceased" included) |
| Routing (requested specialty service + endpoint) | Required | Hub (directory, §9) | Reference |

The decline / chase counts reset per offer (N5 — each offer has its
own confirm/chase budget); the re-scheduling count does not reset
(one re-scheduling per referral). A missing deadline is a hub defect,
not a data gap: every deadline is derived from a recorded timestamp
plus a fixed SLA, so a missing deadline means the timestamp is
missing, and the hub must repair the timestamp from the state
history.

## 4. Triage decision

- Definition: the specialty's accept/reject decision on a referral
  (PI-1). Accept names the service/practitioner who takes it; reject
  carries a reason.
- Owning system: specialty EHR (triage clinician). The hub forwards
  the decision to APS; APS does not decide it.
- Identifiers: referral identifier (§2, the join key); decision
  identifier (specialty-internal). Dedup key: referral identifier —
  one triage decision per referral (a re-triage after rejection
  belongs to a NEW referral, not to this one).
- Lifecycle states: `pending` → `accepted` | `rejected`. Only the
  triage clinician may change it (C1 — the scheduler never triages).
  A decision, once recorded, is final for that referral: there is no
  "un-accept". If the accepting service cannot take the patient after
  all, the referral is cancelled (§13) and APS re-refers.
- Late / out-of-order: a decision arriving after the acceptance
  deadline has already triggered an escalation is still accepted —
  the escalation is a chase, not a closure. A decision arriving for
  a referral already `cancelled` is rejected by the hub.
- Correction: a wrong decision is corrected by recording a new
  decision entry that supersedes it (same referral identifier,
  supersedes +1) with the reason for the change; the workflow state
  record notes the supersession. The superseding decision must come
  from the triage clinician. Supersession corrects recorded data
  (e.g. the accepting practitioner); a reversal of the decision
  itself (un-accepting an accepted referral) goes through
  cancellation (§13), not supersession.

| Field | Required / optional / derived | Source | Form |
|-------|-------------------------------|--------|------|
| Referral identifier | Required | §2 | Identifier |
| Decision | Required — `accept` / `reject` | Triage clinician | Coded |
| Accepting service | Required when `accept` | Triage clinician, from the local service catalogue | Coded (local catalogue) |
| Accepting practitioner | Required when `accept` | Triage clinician | Reference (§8) |
| Rejection reason | Required when `reject` | Triage clinician | Coded (local rejection-reason list) + free text |
| Decision date/time | Required (derived — stamped at decision) | Specialty EHR | Structured (date/time) |
| Triage notes | Optional | Triage clinician | Free text |

The rejection-reason list is a local catalogue (e.g. "missing exam",
"wrong specialty", "capacity") — the worked rejection scenario uses
"missing echocardiogram". The list itself is maintained by the
specialty service; step 4 does not invent its codes.

## 5. Appointment (+ Slot)

- Definition: the specialty appointment offered to the patient and
  then booked (PI-2), with its slot. The offer is an appointment in
  state `offered`; booking confirms it into a slot.
- Owning system: specialty EHR (specialty scheduler books,
  re-schedules, offers, chases — C1). The hub forwards the offer to
  the patient and notifies the APS admin; the hub does not own the
  slot.
- Identifiers: appointment identifier (specialty-created); slot
  identifier (specialty schedule); referral identifier (§2, the join
  key). Dedup key: appointment identifier + patient MPI key.
- Lifecycle states:

| State | Who may change it | Meaning |
|-------|-------------------|---------|
| `offered` | Specialty scheduler | Offered to the patient; confirmation clock (3 working days) running |
| `confirmed` | Patient (via scheduler) | Patient confirmed attendance |
| `booked` | Specialty scheduler | Slot held; Appointment + Slot exist |
| `re-scheduled` | Specialty scheduler / patient (conflict) | New date/time after a conflict or a no-show (once) |
| `attended` | Specialist (§6) | Patient attended; encounter starts |
| `no-show` | Specialist | Patient did not attend |
| `cancelled` | Specialty scheduler (on patient decline) / APS / patient / specialty (§13) | Offer or booked appointment cancelled; all parties notified |

A re-offer is a NEW appointment, not a state of the old one: when
the patient declines an offer, that offer's appointment goes to
`cancelled` and the re-offer is created with a new appointment
identifier (same referral identifier). There is no `re-offered`
state. "Offer number" (below) is a per-referral counter (1st offer,
re-offer), so it still counts offers across appointment identifiers.

- Late / out-of-order: a confirmation arriving after the
  confirmation deadline but before the scheduler has chased is still
  accepted (the deadline triggers a chase, not a closure). A
  confirmation arriving after the referral has already returned to
  APS re-triage is rejected — the offer is dead. A booking for a slot
  already taken is rejected by the specialty schedule (slot conflict
  is detected by the scheduler, spec §3.4).
- Correction: a wrong date/time on a booked appointment is corrected
  by re-scheduling (new slot, same appointment identifier, version
  +1), not by editing the booked slot in place; the patient and APS
  are notified of the change. A cancelled appointment is never
  re-used — a new offer is a new appointment identifier.

| Field | Required / optional / derived | Source | Form |
|-------|-------------------------------|--------|------|
| Appointment identifier | Required | Specialty EHR | Identifier |
| Slot identifier | Required once booked | Specialty schedule | Identifier |
| Referral identifier | Required | §2 | Identifier |
| Date / time | Required | Specialty scheduler (from availability) | Structured (date/time) |
| Place (service, room) | Required | Specialty EHR | Coded (local location list) + text |
| Preparation instructions | Required (may be "none") | Specialty scheduler / specialist | Free text |
| Offer date/time | Required (derived — stamped at offer) | Specialty scheduler | Structured (date/time) |
| Confirmation status | Required (derived — `unconfirmed` / `confirmed` / `declined`) | Patient, via scheduler | Coded |
| Confirmation deadline | Required when `offered` (derived — 3 working days from offer) | §3 workflow state record | Structured (date/time) |
| Offer number (this referral) | Required (derived — 1st offer, re-offer) | Specialty scheduler | Integer |

A capacity conflict is detected by the specialty scheduler; a
conflict with the patient's own availability is detected by the
patient (spec §3.4) — both lead to re-scheduling, not to a new
referral.

## 6. Specialty encounter

- Definition: the attended specialty visit — the patient seen by the
  specialist at the booked appointment. The referral spans several
  encounters (APS visit, specialty visit), all linked to the
  referral (spec §8).
- Owning system: specialty EHR.
- Identifiers: encounter identifier (specialty-created); appointment
  identifier (§5); referral identifier (§2, the join key). Dedup
  key: encounter identifier + patient MPI key.
- Lifecycle states (branches, not a linear chain — the BPMN
  creates no encounter when the patient does not attend):

| State | Who may change it | Meaning |
|-------|-------------------|---------|
| `scheduled` (appointment booked) | Specialty scheduler (§5) | Appointment booked; waiting for the appointment date/time |
| `in-progress` (patient attended) | Specialist | Patient attended; visit under way |
| `finished` (visit done, counter-referral due) | Specialist | Visit done; the counter-referral clock runs |

  No-show branch: when the patient does not attend, NO encounter is
  created — the no-show lives on the Appointment only (§5,
  `no-show`; the referral's no-show terminal state follows the
  second no-show). There is no `cancelled` encounter state and no
  encounter-level attendance field: attendance is recorded once, on
  the Appointment (§5 `attended` / `no-show`). Only the specialist
  (or the specialty record) changes the encounter states above.
- Late / out-of-order: an encounter recorded after the
  counter-referral deadline has already triggered an escalation is
  still accepted — the escalation is a chase. An encounter for a
  referral already `cancelled` is rejected by the hub's record
  check.
- Correction: an encounter recorded in error is corrected by voiding
  it (status `entered-in-error` + a replacement encounter, never an
  overwrite); the workflow state record is notified so the
  counter-referral clock follows the replacement.

| Field | Required / optional / derived | Source | Form |
|-------|-------------------------------|--------|------|
| Encounter identifier | Required | Specialty EHR | Identifier |
| Appointment identifier | Required | §5 | Identifier |
| Referral identifier | Required | §2 | Identifier |
| Date / time (actual) | Required | Specialty EHR | Structured (date/time) |
| Attending specialist | Required | Specialty EHR | Reference (§8) |
| Encounter notes | Optional | Specialist | Free text |

The APS encounter that created the referral is the referral's other
encounter: it exists in the APS EHR, is linked to the referral by
the referral identifier, and is not re-modeled here — its data is
the referral's clinical summary and exams (§2).

## 7. Counter-referral

- Definition: the specialist's return to APS after the specialty
  encounter (PI-3): diagnosis, plan, follow-up indications, plus a
  follow-up plan for APS. Pushed to APS; APS acknowledges receipt;
  the referral reaches `counter-referred`.
- Owning system: specialty EHR creates it; APS EHR holds its received
  copy. The hub routes it through (transit) but does not retain the
  clinical detail (C10).
- Identifiers: counter-referral identifier (specialty-created);
  referral identifier (§2, the join key); specialty encounter
  identifier (§6). Dedup key: counter-referral identifier +
  referral identifier.
- Lifecycle states: `draft` (specialist writing) → `sent` (pushed
  via hub) → `received` (APS acknowledges receipt — the final
  state; the referral is `counter-referred`). Only the specialist creates it;
  only APS acknowledges receipt. A counter-referral is sent once per
  referral — a second one is a correction, not a second return.
- Late / out-of-order: a counter-referral arriving after its deadline
  (5 working days from the encounter) is still accepted — the
  deadline triggers escalation, not rejection. A counter-referral
  for a referral already `cancelled` is rejected by the hub.
- Correction: a wrong counter-referral is corrected by a new version
  (same counter-referral identifier, version +1, superseding the
  previous version) pushed to APS; APS is notified of the
  supersession. Never overwrite.

| Field | Required / optional / derived | Source | Form |
|-------|-------------------------------|--------|------|
| Counter-referral identifier | Required | Specialty EHR | Identifier |
| Referral identifier | Required | §2 | Identifier |
| Specialty encounter identifier | Required | §6 | Identifier |
| Diagnosis | Required | Specialist | Coded (ICD-10) + free-text note |
| Plan | Required | Specialist | Free text (structured sections) |
| Follow-up indications | Required | Specialist | Free text |
| Follow-up plan for APS | Required | Specialist | Free text — controls, exams, or a new referral if another specialty is needed |
| Issue date/time | Required (derived — stamped at sending) | Specialty EHR | Structured (date/time) |
| Receipt acknowledgement (APS) | Required (derived — APS acknowledges receipt) | APS EHR | Structured (date/time + acknowledger) |

The follow-up plan is the part APS acts on: it tells APS what to do
next. If it calls for another specialty, that is a NEW referral
(§2), not a continuation of this one.

## 8. Practitioner

- Definition: a person acting in the referral flow, in one of six
  roles: APS doctor, APS admin, triage clinician, specialty
  scheduler, specialist, hub operator. One person may hold more than one role
  across referrals, but within one referral each role is one person
  (the triage clinician is not the scheduler — C1). The hub operator
  is the person who performs the hub's transitions (routing,
  escalation, cancellation recording, status-query answering), so
  the §3 state-history "actor" field has a defined value for hub
  transitions.
- Owning system: each practitioner's own organisation (APS EHR for
  APS roles, specialty EHR for specialty roles, referral hub for the
  hub operator). No central
  practitioner registry is assumed.
- Identifiers: practitioner identifier (organisation-local);
  role (per referral). Dedup key: practitioner identifier +
  organisation.
- Lifecycle states: none in this use case — practitioners are not
  created or closed by the referral flow.
- Late / out-of-order: not applicable — a practitioner reference
  that cannot be resolved in the owning organisation blocks the
  step that names it (e.g. an acceptance naming an unknown
  practitioner is rejected by the hub's validation).
- Correction: practitioner details are corrected in the owning
  organisation's directory; a referral naming a practitioner who
  has left is corrected by the owning organisation re-assigning
  the step (triage, scheduling, encounter) to another practitioner
  of the same role, recorded in the workflow state record history.

| Field | Required / optional / derived | Source | Form |
|-------|-------------------------------|--------|------|
| Practitioner identifier | Required | Owning organisation | Identifier |
| Name | Required | Owning organisation | Structured text |
| Role in this referral | Required — one of the six roles | The step that names them | Coded |
| Organisation | Required | Owning organisation | Reference (§9) |
| Contact (for the role's notifications) | Optional | Owning organisation | Structured |

## 9. Organisation / care service

- Definition: the organisations and services in the flow — APS
  (CESFAM Los Aromos in the worked example), the specialty service
  (cardiology in the worked example), and the referral hub. The
  "requested specialty/service" in the referral is a care service,
  not an organisation.
- Owning system: the care-services directory (mCSD candidate — the
  hub finds the requested specialty service and its endpoint in the
  directory, scan § mCSD); each organisation owns its own record.
- Identifiers: organisation identifier; care-service identifier
  (from the local specialty/service catalogue). Dedup key:
  care-service identifier + organisation.
- Lifecycle states: none in this use case — organisations and
  services are not created or closed by the referral flow. A service
  that stops accepting referrals is a directory change, handled by
  the hub's routing (the hub routes only to services the directory
  lists as accepting).
- Late / out-of-order: the requested service comes from the local
  specialty/service catalogue at creation (§2), so the hub never
  receives a referral naming an unlisted service — there is no
  "routing pending" hold. A service missing from the catalogue is
  a creation-time validation failure in APS, not a hub hold.
- Correction: service details (name, endpoint, accepting status)
  are corrected in the directory; the hub re-reads the directory on
  each routing decision, so a correction applies to the next routing,
  not retroactively to referrals already routed.

| Field | Required / optional / derived | Source | Form |
|-------|-------------------------------|--------|------|
| Organisation identifier | Required | Directory / organisation | Identifier |
| Organisation name | Required | Directory | Structured text |
| Care-service identifier | Required for the requested/accepting service | Local specialty/service catalogue | Coded (local catalogue) |
| Care-service name | Required | Local catalogue | Structured text |
| Endpoint (where the hub sends the referral) | Required for routing | Directory | Structured (address) |
| Accepting referrals? | Required (derived from the directory) | Directory | Coded (yes/no) |

The specialty/service catalogue is local: the spec names "local
specialty/service catalogs" as the terminology for the requested and
accepting service. Its owner is the network (hub operator together
with the services); step 4 records the catalogue's codes as a local
code system, it does not invent a standard one.

## 10. MPI identity record

- Definition: the cross-reference of a patient's identifiers across
  organisations — the MPI key and the local identifiers it maps to.
  The MPI resolves identity; it makes no clinical decisions (spec
  §2).
- Owning system: MPI (Master Patient Index).
- Identifiers: MPI key (the cross-organisation key); each
  organisation's local patient identifier. Dedup key: MPI key.
- Lifecycle states: `active` → `merged` (two records found to be
  one person — the surviving MPI key keeps both local identifiers)
  or `retired` (an identifier retired when a duplicate is found).
  Only the MPI may change these.
- Late / out-of-order: an identity feed arriving after the referral
  was created is applied to the workflow state record (the MPI key
  is updated); the referral itself is not re-created.
- Correction: identity merges and splits are MPI operations with an
  audit trail (who merged, when, which keys). A merge never deletes
  a local identifier — it links it to the surviving MPI key, so a
  referral that travelled with the old key still resolves.

| Field | Required / optional / derived | Source | Form |
|-------|-------------------------------|--------|------|
| MPI key | Required | MPI | Identifier |
| Local identifiers (one per organisation) | Required (at least the APS one) | Each organisation's EHR | Identifier |
| Match basis (identifier / demographics) | Required | MPI | Coded |
| Match confidence | Optional | MPI | Coded/decimal |
| Merge history | Required when merged (derived) | MPI | Structured |

## 11. Notification

- Definition: a notice to the patient, APS, or the specialty at a
  referral state change, from a named sender (C5/Q3). The patient is
  informed at each step that concerns them; APS is informed at every
  change; the specialty is notified on SLA escalations.
- Owning system: the sender's system — APS EHR (APS admin), hub
  (forwarding), specialty EHR (scheduler). A notification is a
  record of a send, not the message content itself.
- Identifiers: notification identifier (sender-created); referral
  identifier (§2, the join key). Dedup key: notification identifier.
- Lifecycle states: `sent` → `delivered` | `failed` (delivery
  outcome, from the channel). The sender owns the send; the channel
  owns the delivery outcome. A failed delivery is re-tried by the
  sender — a failed notification never changes the referral state.
- Late / out-of-order: a notification arriving after the referral
  has moved on (e.g. the acceptance notice arriving after a
  cancellation) is still delivered with its original timestamp — the
  recipient sees when the event happened, not when the notice
  arrived. The hub never suppresses a notification because the state
  moved on.
- Correction: a notification sent in error is corrected by a new
  notification stating the correction ("the previous notice was
  wrong; the state is X") — never by deleting the sent record.

| Field | Required / optional / derived | Source | Form |
|-------|-------------------------------|--------|------|
| Notification identifier | Required | Sender's system | Identifier |
| Referral identifier | Required | §2 | Identifier |
| Sender (named) | Required — APS admin / specialty scheduler (via hub) / specialist / hub | The step (C5) | Coded (role) |
| Recipient | Required — patient / APS admin / APS doctor / specialty | The step (C5) | Coded (role) |
| Triggering state change | Required | §3 workflow state record | Coded (state transition) |
| Channel | Required — as recorded (phone, in person, system message) | Sender | Coded (local channel list) |
| Sent date/time | Required (derived — stamped at send) | Sender's system | Structured (date/time) |
| Delivery outcome | Optional (derived) | Channel | Coded (`delivered` / `failed`) |

Named senders (C5): referral creation → APS admin informs the
patient; acceptance/rejection → APS admin informs the patient;
appointment offer → specialty scheduler sends it via the hub, APS
admin is notified of the offer; counter-referral outcome → APS admin
informs the patient. Escalations are also notifications (hub →
specialty + APS on SLA breach; hub → APS on re-triage timeout).

## 12. Declined-referral record

- Definition: the APS record of a patient declining the referral
  itself at creation (C8). NO referral is created in this case —
  there is no referral identifier, no workflow state record, and
  nothing travels to the hub or the specialty.
- Owning system: APS EHR (APS record only).
- Identifiers: APS record identifier; patient MPI key (§1). Dedup
  key: APS record identifier. There is deliberately no referral
  identifier — a declined referral must never be mistaken for a
  created one.
- Lifecycle states: `recorded` (terminal). Only the APS doctor
  records it, at creation time.
- Late / out-of-order: not applicable — nothing travels.
- Correction: a wrongly recorded decline is corrected by a new APS
  record entry superseding it (the patient later accepts and a
  referral is created — that is a new referral, not an un-decline).

| Field | Required / optional / derived | Source | Form |
|-------|-------------------------------|--------|------|
| APS record identifier | Required | APS EHR | Identifier |
| Patient (MPI key) | Required | §1 | Identifier |
| Decision | Required — `declined` | Patient, recorded by APS doctor | Coded |
| Reason | Required | Patient (as recorded by APS) | Free text |
| Recorded date/time | Required (derived) | APS EHR | Structured (date/time) |

## 13. Cancellation record

- Definition: a cancellation request and its reason, at any point
  before completion, by APS, the patient, or the specialty (C3) —
  including patient death (reason "patient deceased", C11). An
  already-booked appointment is cancelled and all parties are
  notified.
- Owning system: hub (recorded in the workflow state record, §3);
  each party keeps its own copy of the request.
- Identifiers: referral identifier (§2, the join key); cancellation
  identifier (hub-created). Dedup key: referral identifier +
  cancellation identifier — the key covers duplicate deliveries of
  the same cancellation request (same cancellation identifier
  delivered twice is one cancellation). A cancellation after a
  re-open (§3) is a NEW cancellation entry with a new cancellation
  identifier, not a reuse of the undone one.
- Lifecycle states: `requested` → `recorded` (terminal — the
  referral is `cancelled`). The requester may be APS, the patient,
  or the specialty; the hub records it. A cancellation, once
  recorded, is final except for the one correction path in §3
  (cancellation recorded in error → re-open with an explicit entry).
- Late / out-of-order: a cancellation arriving after the referral
  reached a terminal state is rejected (nothing left to cancel). A
  cancellation arriving while the appointment is being booked is
  accepted — the booking is voided, not completed.
- Correction: as §3 — re-open only, with an explicit entry and
  notification to APS and the specialty.

| Field | Required / optional / derived | Source | Form |
|-------|-------------------------------|--------|------|
| Cancellation identifier | Required | Hub | Identifier |
| Referral identifier | Required | §2 | Identifier |
| Requester | Required — APS / patient / specialty | The requesting party | Coded (role) |
| Reason | Required — free text, or "patient deceased" | Requester | Coded + free text |
| Request date/time | Required | Requester | Structured (date/time) |
| Appointment cancelled? | Required when an appointment was booked (derived) | §5 | Coded (yes/no) |
| Parties notified | Required (derived — APS, patient, specialty) | Hub (§11) | Structured |

## Data flow per interoperability point

| PI | What travels | From → to | Entities read / written |
|----|--------------|-----------|-------------------------|
| PI-0 | Referral minimum data set (§2) + MPI key (§1) | APS → hub → specialty | Read: Patient (§1), MPI identity record (§10), Practitioner (§8), Organisation/care service (§9). Written: Referral request (§2, `requested`), Workflow state record (§3, `requested` → `received`). |
| PI-1 | Triage decision: accept (+ service/practitioner) or reject (+ reason) | Specialty → hub → APS (+ patient, via APS admin) | Read: Referral request (§2), Workflow state record (§3). Written: Triage decision (§4), Workflow state record (§3, `accepted` / `rejected`), Notification (§11). |
| PI-2 | Appointment offer / confirmation / decline / booking; re-offer; re-scheduling; no-show | Specialty ↔ patient, via hub; hub → APS admin (offer notification) | Read: Workflow state record (§3), Referral request (§2). Written: Appointment (§5), Workflow state record (§3, `scheduled`; decline/chase/re-scheduling counts; `no-show` on second no-show), Notification (§11). |
| PI-3 | Counter-referral (§7) + APS receipt acknowledgement | Specialty → hub → APS | Read: Specialty encounter (§6), Workflow state record (§3). Written: Counter-referral (§7, `sent` → `received`), Workflow state record (§3, `counter-referred`), Notification (§11). |
| PI-4 | Status query → current state, last state change, next expected step | APS → hub → APS | Read only: Workflow state record (§3). Nothing written; the query never changes state. |

## Terminologies

| Data | Terminology | Owner / maintainer | Notes |
|------|-------------|--------------------|-------|
| Reason for referral | SNOMED CT (primary) | SNOMED International / national release centre | Coded + free-text note (§2). Specific concept pinned in step 4. |
| Diagnosis (counter-referral) | ICD-10 | WHO / national adaptation | Coded + free-text note (§7). The worked example (heart failure with reduced ejection fraction) gets its ICD-10 code in step 4. |
| Exams / results | LOINC | Regenstrief / LOINC | Coded + values (§2). The worked example's ECG and lab codes are pinned in step 4, not here. |
| Requested / accepting specialty / service | Local specialty/service catalogue | Network (hub operator + services) | Local code system (§9). Step 4 records its codes; no standard catalogue is invented. |
| Priority | Local value set: `routine` / `urgent` | This use case (C6) | Drives the acceptance SLA (§3). |
| Rejection reason | Local rejection-reason list | Specialty service | e.g. "missing exam" (§4). |
| Referral state | Local value set (the §3 state list) | This use case (spec §3.1) | The state machine is the case's own vocabulary, not a standard. |
| Notification channel | Local channel list | Each sender's organisation | Phone, in person, system message (§11). |

No new identifier is created where one already works: the referral
identifier is created by APS because no network-wide referral
identifier exists; the MPI key is re-used, not re-invented; the
appointment and encounter identifiers are the specialty's own.

## Data quality and ownership — summary

- Who owns each entity is in its section above. The hub owns state
  and routing only; it never owns clinical detail. APS owns the
  referral and the patient record; the specialty owns the triage
  decision, the appointment, the encounter, and the counter-referral.
- Missing data: a missing required field blocks the step that needs
  it (creation, acceptance, offer) — the step fails validation, it
  does not proceed with a blank. The one exception is the
  confirmation deadline, which triggers a chase rather than a block.
- Duplicated data: dedup keys are listed per entity; duplicates are
  ignored (same identifier) or corrected by supersession (new
  version, same identifier), never by overwriting in place.
- Out-of-date data: corrections travel as new versions or
  compensating entries, with the workflow state record history as
  the audit trail. The hub's record is the authority for state;
  every later step reads it first.
- Retention: each organisation retains its copy under its own
  records policy (spec §5). The hub retains the workflow state
  record for tracking and status queries; it does not retain the
  clinical detail it routes in transit.

## Open questions (for the parent)

1. **LOINC codes for the worked example's exams** (ECG, labs in the
   cardiology scenario): pinned in step 4, not here — the entities
   file records the terminology (LOINC) and the slot, not the codes.
   No parent decision needed now.
2. **The local specialty/service catalogue and rejection-reason
   list**: step 4 records them as local code systems with the
   worked-example values (cardiology; "missing echocardiogram").
   No parent decision needed now.
3. **Notification channel list**: the channels (phone, in person,
   system message) are recorded as a local list; the case does not
   pick a single channel per notification. If the parent wants one
   channel pinned per notification, that is a step 4 decision.

## Handoff to step 4 (FHIR modeling)

- Entity names are fixed here and must be kept in the BPMN model,
  in this table, and later in the FHIR mapping: Patient, Referral
  request, Workflow state record, Triage decision, Appointment (+
  Slot), Specialty encounter, Counter-referral, Practitioner,
  Organisation / care service, MPI identity record, Notification,
  Declined-referral record, Cancellation record.
- Step 4 decisions waiting on this file: one referral = one request
  + one workflow state record (spec §8); the state lives in the
  workflow record, not in the request status; the hub holds state,
  not clinical detail; the decline / chase / re-scheduling counts
  live in the workflow record and must be exposed by the operations
  (step 2 decision); the MPI key travels with the referral; no
  Consent resource for the referral itself (Q7).
- Note for step 4 (reviewer verified live): R4 `Encounter.status`
  has no `scheduled` (the value is `planned`), and
  `Appointment.status` has no `offered` / `confirmed` /
  `re-offered` / `attended` — the `offered`, `confirmed`, `booked`,
  `re-scheduled`, `attended`, `no-show` states in §5 and the
  `scheduled` state in §6 are case language to map in step 4, not
  FHIR value-set values.
- Done-when check (entities-data skill): every entity has a name, a
  definition, and its owning system; every entity's fields and
  sources are listed; name clashes are settled above; the list is
  presented as tables with the same names as the BPMN model.
