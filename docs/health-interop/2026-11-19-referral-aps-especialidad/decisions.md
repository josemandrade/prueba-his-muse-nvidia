# Decisions — referral-aps-especialidad

## 2026-11-19 — Plan tasks named "Plan task N" (FHIR Task in use)

- Context: this case uses the FHIR `Task` resource for the referral state, so the
  pack's "Task N" plan naming would collide with the resource name (audit 1, L1).
- Decision: plan items are written "Plan task N" in `plan.md` and `state.md`.
- Alternatives considered: keeping "Task N" — rejected, ambiguous next to a
  `Task` resource.
- Consequences: step 5 and step 6 plans use "Plan task N" throughout.

## 2026-11-19 — Consent covered by the care relationship (decided 2026-11-19)

- Context: the referral shares clinical data with the requested specialty; the
  case file does not state a consent model.
- Decision (decided 2026-11-19 by the parent, acting as validating user — Q7):
  sharing the referral data with the requested specialty is covered by the care
  relationship; no separate consent is requested for the referral itself.
- Alternatives considered: a separate signed consent per referral — rejected, it
  would block a routine care-coordination flow.
- Consequences: the design note records consent in the care relationship; step 4
  does not model a Consent resource for the referral itself.

## 2026-11-19 — SLAs (decided 2026-11-19)

- Context: the case file says waits last days but gives no numbers; the BPMN needs
  timer events and the hub needs an escalation rule.
- Decision (decided 2026-11-19 by the parent, acting as validating user — Q1):
  acceptance 5 working days from referral creation (2 for urgent); appointment
  offered 10 working days from acceptance; counter-referral 5 working days from
  the specialty encounter; on timeout the hub escalates to the specialty and
  notifies APS.
- Alternatives considered: no numbers in the spec, leaving SLAs to step 2 —
  rejected, the lifecycle questions belong in step 1.
- Consequences: the BPMN models the timeouts as timer events; step 4 records the
  escalation as a hub responsibility.

## 2026-11-19 — Hub as routing and state-tracking intermediary (decided 2026-11-19)

- Context: the case file lists a "hub de derivación" as an actor without pinning
  its responsibilities.
- Decision (decided 2026-11-19 by the parent, acting as validating user — Q2):
  the hub receives the referral, routes it to the requested specialty service,
  holds the referral state, answers status queries, and escalates on timeout. It
  does not hold the full clinical detail.
- Alternatives considered: direct APS → specialty messaging with no hub — rejected,
  the case file names the hub as an actor and PI-4 needs a state holder.
- Consequences: the BPMN has a hub pool; step 4 models the hub as the state
  holder for PI-4.

## 2026-11-19 — Worked example specialty: cardiology

- Context: the case file names cardiology as the example specialty.
- Decision: the success example and the synthetic scenarios use cardiology
  (suspected heart failure).
- Alternatives considered: another specialty — no reason to change the case
  file's example.
- Consequences: step 4–6 examples use the cardiology scenario.

## 2026-11-19 — Case source and pack version

- Context: the user asked to build the audit 1 referral case with the current
  pack.
- Decision: build the audit 1 vehicle (`pack-audit-2026-11-12-referral-case.md`)
  with pack v0.39.0; do not re-litigate audit 1 (57 findings, fully implemented
  as v0.19.0 — the pack already carries the referral vocabulary).
- Alternatives considered: re-auditing the case against v0.39.0 — rejected, the
  task is to build the case, not to audit the pack again.
- Consequences: step 4 uses the current skills' referral vocabulary
  (ServiceRequest/Task/Appointment, state machine, Scheduling, XDW).

## 2026-11-19 — Synthetic data only; test repo

- Context: all work is synthetic by default; the user authorised pushes to the
  public test repo `prueba-his-muse-nvidia` only.
- Decision: synthetic data only in every example and test; work in
  `docs/health-interop/2026-11-19-referral-aps-especialidad/` inside the clone;
  do not touch the school-vision-screening folder or the pack.
- Alternatives considered: none.
- Consequences: no real patient data anywhere in the case folder.

## 2026-11-19 — Expert review fix C1: triage owner is the triage clinician

- Context: the review found the spec named the scheduler as the triage owner.
- Decision (review fix, parent accepted): clinical triage is performed by the
  triage clinician (accept/reject with reason, naming the accepting
  service/practitioner); the specialty scheduler books, re-schedules, offers the
  appointment and chases unconfirmed offers only.
- Consequences: new "Triage clinician" row in the §2 role table; §3.3 names the
  triage clinician; the scheduler row no longer claims accept/reject.

## 2026-11-19 — Expert review fix C2: two-path state chain

- Context: the review found the single linear chain hid the rejection path.
- Decision (review fix, parent accepted): the lifecycle is two paths — accepted
  (`requested → received → accepted → scheduled → completed → counter-referred`)
  and rejected (`requested → received → rejected → APS re-triage → [new referral
  | different specialty | resolve in APS] → closed as rejected`). A re-referral
  after a rejection is a NEW referral; the first closes as `rejected` only once
  APS has decided the re-triage outcome.
- Consequences: §3.1 rewritten as two paths; §3.3 and the §6 rejection scenario
  state the new-referral rule.

## 2026-11-19 — Expert review fix C3: cancellation at any point before completion

- Context: the review found cancellation was limited to before acceptance.
- Decision (review fix, parent accepted): cancellation is possible at any point
  before completion and can be requested by APS, by the patient, or by the
  specialty; an already-booked appointment is cancelled and all parties are
  notified.
- Consequences: §3.1 terminal states rewritten; the BPMN must allow a cancel
  path out of every pre-completion state.

## 2026-11-19 — Expert review fix C4: offer-confirm loop

- Context: the review found no offer-decline → re-offer loop.
- Decision (review fix, parent accepted): the patient has 3 working days to
  confirm an offered appointment; the specialty scheduler chases on expiry; on
  a decline the scheduler offers another slot (one re-offer); after a second
  decline, or an offer still unconfirmed after the second chase, the referral
  returns to APS for re-triage. A capacity conflict is detected by the specialty
  scheduler; a conflict with the patient's own availability is detected by the
  patient.
- Consequences: §3.4 rewritten; §3.8 gains the 3-working-day confirmation SLA.

## 2026-11-19 — Expert review fix C5: notification senders pinned

- Context: the review found §3.1 and §4 disagreed on who informs the patient.
- Decision (review fix, parent accepted): referral creation → APS admin informs
  the patient; acceptance/rejection → APS admin informs the patient; appointment
  offer → specialty scheduler sends it via the hub, APS admin is notified of the
  offer; counter-referral outcome → APS admin informs the patient.
- Consequences: §2 APS admin row, §3.1, §4 and the §6 example all name the
  sender; referral creation added to the §3.1 patient notification list.

## 2026-11-19 — Expert review fix C6: priority values routine / urgent

- Context: the review found the priority values undefined.
- Decision (review fix, parent accepted): priority is `routine` / `urgent`,
  assigned by the APS doctor at referral creation; urgent halves the acceptance
  SLA (2 working days vs 5).
- Consequences: §3.2 input, §3.7 PI-0 data set and §3.8 state the values and the
  assigner.

## 2026-11-19 — Expert review fix C7: re-triage decision SLA

- Context: the review found no SLA for the APS re-triage decision after a
  rejection.
- Decision (review fix, parent accepted): the APS doctor re-triages within
  5 working days of the rejection; on expiry the hub escalates to APS (notifies
  the APS admin and the APS doctor).
- Consequences: §3.3 and §3.8 state the SLA and the escalation.

## 2026-11-19 — Expert review fix C8: patient declines the referral at creation

- Context: the review found no branch for the patient declining the referral
  itself.
- Decision (review fix, parent accepted): if the patient declines the referral
  itself at creation, NO referral is created; APS records the decision and the
  reason in the APS record.
- Consequences: §3.2 gains the branch; the §2 patient row gains "whether to
  accept the referral itself at creation".

## 2026-11-19 — Expert review fix C10: hub transit, not storage

- Context: the review found it unclear whether the hub retains the
  counter-referral.
- Decision (review fix, parent accepted): the hub routes referrals and
  counter-referrals through (transit) but does not retain the clinical detail.
- Consequences: §3.5, §5 and the §8 design note state transit vs storage.

## 2026-11-19 — Expert review fix C11: death while the referral is open

- Context: the review asked for the rule when the patient dies with an open
  referral.
- Decision (review fix, parent accepted): the referral closes as `cancelled`
  (reason "patient deceased") and APS and the specialty are notified.
- Consequences: §3.1 terminal states state the rule; step 4 must model the
  transition and step 6 must test it.

## 2026-11-19 — Expert review fix C12: patient contact data in the PI-0 data set

- Context: the review found patient contact data missing from the PI-0 minimum
  data set.
- Decision (review fix, parent accepted): patient contact data is part of the
  PI-0 minimum data set.
- Consequences: §3.2 input and §3.7 PI-0 list include patient contact data.

## 2026-11-19 — Expert review re-check fix N1: scheduling-failure re-triage closure rule

- Context: the re-check found the return to APS after a scheduling failure had
  no closure rule.
- Decision (re-check fix, parent ruled): the APS re-triage after a scheduling
  failure follows the same outcome options as the re-triage after a rejection
  ([new referral | different specialty | resolve in APS]), and the first
  referral closes as `rejected` once APS has decided.
- Consequences: §3.1 state machine and §3.4 state the rule; the BPMN models
  the scheduling-failure return into the same re-triage branch as a rejection.

## 2026-11-19 — Expert review re-check fix N2: scoped timeout escalation

- Context: the re-check found the generic §3.8 timeout bullet covered all
  timeouts, contradicting the re-triage escalation to APS and the confirmation
  chase by the scheduler.
- Decision (re-check fix, parent ruled): the bullet reads "On timeout of the
  acceptance, appointment-offer, or counter-referral SLAs: the hub escalates to
  the specialty service and notifies APS." The re-triage timeout escalates to
  APS; the confirmation timeout is the scheduler's chase.
- Consequences: §3.8 bullet scoped; no other timeout rule changes.

## 2026-11-19 — Expert review re-check fix N3: second chase pinned

- Context: the re-check found §3.4 named a "second chase" without pinning when
  it happens.
- Decision (re-check fix, parent ruled): the scheduler chases once on expiry of
  the 3-working-day confirmation window; if the offer is still unconfirmed
  after a further 3 working days, the scheduler chases once more (second
  chase); if the offer is still unconfirmed after that second chase, the
  referral returns to APS for re-triage.
- Consequences: §3.4 confirm loop states the timing; the BPMN models two
  chases before the return to APS.

## 2026-11-19 — Expert review re-check fix N4: counter-referred as terminal state

- Context: the re-check found the §3.1 terminal-states list omitted the
  successful completion state.
- Decision (re-check fix, parent ruled): `counter-referred` is a terminal state
  (successful completion).
- Consequences: §3.1 terminal-states list includes it.

## 2026-11-19 — Expert review re-check fix N5: post-no-show offer follows the confirm loop

- Context: the re-check found §3.4 did not say which confirm/chase rules apply
  to the re-scheduled offer after a no-show.
- Decision (re-check fix, parent ruled): the re-scheduled offer follows the
  same confirm/chase rules as the first offer (3 working days to confirm, the
  scheduler chases on expiry — once, then once more after a further 3 working
  days — one re-offer on decline); a second decline, or an offer still
  unconfirmed after the second chase, sends the referral back to APS for
  re-triage, as in the confirm loop.
- Consequences: §3.4 no-show bullet states the rules; the BPMN models the
  re-scheduled offer with the same loop.

## 2026-11-19 — Step 2 model split in three parts

- Context: the referral lifecycle (creation → triage → scheduling →
  encounter → counter-referral, plus status query) is too long for one
  readable diagram.
- Decision: split in three parts — A referral-triage, B
  scheduling-counterreferral, C status-query. PI ids are global across
  the three diagrams; the single PI register lives in
  `02-bpmn-model.md`. Part A ends at acceptance; Part B starts there.
  Part C can be invoked at any point.
- Alternatives considered: one diagram — rejected, unreadable at display
  size.
- Consequences: the linking message carries its PI id in both diagrams;
  step 4 maps operations per PI across the parts.

## 2026-11-19 — Step 2 event-based gateways drawn as exclusive

- Context: the acceptance and confirmation waits are event-based
  (message vs timer), but the renderer draws only exclusive / parallel
  gateways.
- Decision: draw them as exclusive gateways named `Decision received?`
  and record in `02-bpmn-model.md` that they are event-based.
- Alternatives considered: a custom gateway glyph — rejected, out of
  scope for the case tools.
- Consequences: the model description, not the glyph, carries the
  event-based semantics; step 4 maps them to the wait/subscription
  mechanism.

## 2026-11-19 — Step 2 count-based decisions are data-based gateways

- Context: "one re-offer", "chase at most twice", "one re-scheduling"
  are counts; BPMN has no counter.
- Decision: model them as data-based gateways (`First decline?`,
  `Chased twice?`, `Re-scheduling succeeds?`) that read the workflow
  record held by the hub. After a second decline, or an offer still
  unconfirmed after the second chase, the referral returns to APS
  re-triage; after a second no-show it closes as `no-show` (Q5).
- Alternatives considered: a loop counter in the diagram — rejected, no
  honest BPMN shape for it.
- Consequences: the hub must expose the decline / chase / re-scheduling
  counts in the workflow record (step 3 entities, step 4 operations).

## 2026-11-19 — Step 2 cancellation as a message-start row

- Context: cancellation is possible at any point before completion, by
  APS, the patient, or the specialty (C3); a boundary event on every
  task would clutter all three parts.
- Decision: one message start event per part (`Cancellation requested`
  → `Record cancellation; notify all parties` → `Cancelled
  (terminal)`), in the hub loop row of Parts A and B. The start event
  has no incoming message flow in the diagram — the requester (APS,
  patient, or specialty) is outside the modeled scope; the description
  states any party may request it. Part C has no cancellation row
  (a query cannot be cancelled).
- Alternatives considered: a boundary event on every task — rejected,
  unreadable.
- Consequences: step 4 models one cancel operation; step 6 tests it
  from each pre-completion state.

## 2026-11-19 — Step 2 Part C single shared APS lane

- Context: PI-4 is a read-only lookup any APS staff member can make;
  splitting it into doctor/admin lanes would duplicate the query.
- Decision: Part C has one APS lane ("APS doctor / admin").
- Alternatives considered: two lanes with duplicated tasks — rejected,
  noise.
- Consequences: the lane represents the APS as requester, not a single
  role; step 3 notes the requester is any APS staff member.

## 2026-11-19 — Step 2 builder + two clone-root tool fixes

- Context: hand-writing three `.bpmn` files with explicit orthogonal
  waypoints is error-prone; the checker flagged every flow as crossing
  its pool/lane containers, and the message-event glyph (✉) rendered
  as a tofu box in the PNG font.
- Decision: generate the `.bpmn` files from data tables
  (`build_bpmn.py` + `parts_data.py`, kept in the case folder — the
  geometry is the model). Fix the clone-root tools (not the pack):
  `check_bpmn.py` tests only flow-node shapes (participants/lanes are
  containers, as its docstring already said); `render_bpmn.py` draws
  the message envelope as vector lines instead of the ✉ glyph.
- Alternatives considered: hand-editing the XML — rejected, the
  waypoint tables are auditable and regenerable.
- Consequences: any geometry change goes through `parts_data.py` +
  rebuild + check + render + look.

## 2026-11-19 — Step 2 modeling gap found by the PI register (m11)

- Context: while writing the single PI register, Part A had no message
  flow delivering the referral to the specialty — the hub routed it
  (sequence) but the specialty's triage task had no incoming message.
- Decision: add m11 (PI-0 second leg, hub → specialty), re-check 0/0.
- Alternatives considered: leaving the triage task message-triggered by
  nothing — rejected, a task with no trigger is a modeling gap.
- Consequences: PI-0 has two legs (m3 APS → hub, m11 hub → specialty);
  the register lists both.

## 2026-11-19 — Step 2 SLA label shorthand on the diagram

- Context: "10 working days" / "5 working days" labels collide with
  neighbouring flow labels in the dense scheduler area.
- Decision: the diagram shortens them to "10 days" / "5 days"; the full
  "working days" wording lives in `02-bpmn-model.md` (§ SLAs) and in
  the spec (§3.8).
- Alternatives considered: full wording on the diagram — rejected, the
  labels overlapped and hid each other.
- Consequences: the reader must not quote the diagram label as the SLA;
  the spec is authoritative.

## 2026-11-19 — Step 2 expert-review fixes C1–C14 (review NOT APPROVED)

- Context: the independent expert review of the step 2 draft returned
  NOT APPROVED — 6 medium (C1–C6) + 8 low (C7–C14). All fixes follow
  the already-validated spec; no new user decisions.
- Decisions:
  - C1: add m12 (rejection notice to the patient, APS admin →
    patient) and name the doctor notification on the acceptance path
    ("Receive acceptance; inform patient and APS doctor").
  - C2: escalation tasks rename to name the APS notification; h19/h20
    carry the delay escalation to a new APS admin task ("Receive delay
    escalation; notify APS doctor").
  - C3: the re-scheduled offer routes back to `Offer appointment`, so
    it goes through the same confirm/chase loop (counts reset per
    offer); the patient's agreement to the new date IS the confirmation
    of the re-scheduled offer in that loop.
  - C4: scheduling-failure returns land on the Part A re-triage entry
    (end events renamed "— Part A outcomes apply"); same three
    outcomes and the same rejected closure once APS decides.
  - C5: patient death is a cancellation cause handled by the generic
    cancellation row (reason "patient deceased", hub notifies APS +
    specialty) — recorded in the model doc.
  - C6: duration labels on the timeout branches ("5 working days (2 if
    urgent)", "3 working days"); one acceptance wait covers both
    durations because the timer is data-driven on the referral
    priority, which travels in the minimum data set.
  - C7: "Re-scheduling succeeds?" renamed "First re-scheduling?" (the
    second no-show → `no-show` terminal is now visible).
  - C8: h6/h7 landing on the decision gateways is a RECORDED deviation
    (the gateway's decision is the message receipt; a catch event per
    decision would duplicate the gateway).
  - C9: cancellation start events name the requester (APS / patient /
    specialty); the non-termination caveat is recorded in the model
    doc (the hub's record is the authority).
  - C10: SUPERSEDES the "SLA label shorthand" decision above — full
    "working days" wording everywhere on the diagrams (the shorthand
    was needed only before the renderer fixes; labels no longer
    overlap).
  - C11: Part C return aligned to spec §3.7 (current state, last state
    change, next expected step) in task, message and return-task
    labels.
  - C12: end event renamed "New referral to different specialty; first
    closed as rejected".
  - C13: renderer fixes (opaque label backing, own-shape nudge guard,
    extended nudges, canvas expansion) + geometry nudges (g14 loop
    rerouted to y=860, g21 label shortened to one line); all three
    PNGs re-rendered and re-looked.
  - C14: ITI-118 is "Search Patient Appointments"; MHD gains ITI-106
    Generate Metadata; 360X "Rev. 1.2" confirmed from the supplement
    PDF itself (2021-04-14).
- Consequences: Part A 52 shapes / 43 flows, Part B 65 / 59, Part C
  16 / 11; mechanical check 0/0 on all three parts after the fixes;
  awaiting the parent's focused re-check and step 2 validation.

## 2026-11-19 — Step 3 file name is 03-entities-data.md

- Context: the step 3 brief named the artefact `03-entities.md`,
  but `references/work-structure.md` and the `entities-data` skill
  both fix the name as `03-entities-data.md`, and the case README
  status table already listed `03-entities-data.md` as the pending
  step 3 artefact.
- Decision: write the step 3 artefact as `03-entities-data.md` (the
  canonical name); no file named `03-entities.md` exists in the case
  folder.
- Alternatives considered: following the brief's name literally —
  rejected, it would contradict the pack's fixed layout and the
  case's own README.
- Consequences: step 4 references `03-entities-data.md`.

## 2026-11-19 — Step 3 expert-review fixes C1–C10 (review NOT APPROVED)

- Context: the independent expert review of the step 3 draft returned
  NOT APPROVED — 5 medium (C1–C5) + 5 low (C6–C10). All fixes follow
  the already-validated spec and BPMN; no new user decisions.
- Decisions:
  - C1: add the hub operator as a sixth Practitioner role
    (organisation: referral hub). Hub transitions (routing,
    escalation, cancellation recording, status-query answering) are
    recorded in the §3 state history with actor "hub operator" —
    hub actions are human-operated, not system-automated.
  - C2: each offer is a NEW Appointment. The `re-offered` state is
    dropped from the §5 lifecycle; a declined offer's appointment
    goes to `cancelled` and the re-offer carries a new appointment
    identifier. "Offer number" stays a per-referral counter.
  - C3: no Encounter is created when the patient does not attend —
    the no-show lives on the Appointment only (§5). The §6
    lifecycle is rewritten as branches (`scheduled` →
    `in-progress` → `finished`); the Attendance field is dropped
    (attendance is recorded once, on the Appointment).
  - C4: the re-triage deadline derives from the re-triage trigger
    (rejection, or the scheduling-failure return). During a
    scheduling-failure re-triage the referral is in state
    `rejected` (moved there at the return, into the shared
    re-triage entry); the deadline runs 5 working days from the
    return.
  - C5: widen the §11 notification definition to "the patient, APS,
    or the specialty"; add specialist to senders and specialty to
    recipients (escalations h19/h20 target the specialty; the
    specialist originates "Notify APS of no-show").
  - C6: supersession corrects recorded data (e.g. the accepting
    practitioner); a reversal of the decision itself goes through
    cancellation (§13).
  - C7: drop the "identity pending" and "routing pending" hold
    rules. Identity is resolved via the MPI before creation (BPMN
    Part A), so no referral arrives unresolvable; the MPI-merge
    case is already covered by §10. The requested service comes
    from the local catalogue at creation, so an unlisted service
    is a creation-time validation failure, not a hub hold.
  - C8: drop the "Requested date (if any)" field from §2 — it is
    outside the PI-0 minimum data set (spec §3.7); no spec change
    recorded.
  - C9: the §13 dedup key (referral identifier + cancellation
    identifier) covers duplicate deliveries of the same
    cancellation request; a post-re-open cancellation is a new
    entry with a new cancellation identifier.
  - C10: the §7 lifecycle ends in the named state `received` (APS
    acknowledged receipt); "terminal" is no longer used as a state
    name there.
- Consequences: §8 has six roles; §5 has no `re-offered` state; §6
  has no encounter on a no-show and no Attendance field; §3 derives
  the re-triage deadline from the trigger; §11 covers the specialty
  as sender and recipient; §2 has no requested-date field; §13
  dedup is per cancellation identifier; §7 ends in `received`. The
  step 4 handoff notes the reviewer-verified R4 status-value facts
  (`Encounter.status` has no `scheduled`; `Appointment.status` has
  no `offered` / `confirmed` / `re-offered` / `attended`).

## Noted spec widening (not applied — spec is validated)

- N3 (2026-11-19, from the step 3 re-check): spec §3.8 names only
  the rejection trigger ("Re-triage decision after a rejection:
  5 working days from the rejection") while `03-entities-data.md`
  §3 derives the second trigger (scheduling-failure return) from
  the validated BPMN. The spec is NOT edited here (validated).
  Proposed wording for the next spec touch: "Re-triage decision
  after a rejection or a scheduling-failure return: **5 working
  days** from the rejection or the return;".

## Step 4 design decisions (2026-11-19, draft — not validated)

- **Centre resource is `Task` (`DerivacionTarea`)**, not the
  ServiceRequest: the case's question at every step is "where does
  the referral stand?", and the answer lives in the workflow
  record (state, SLA clocks, loop counts). The ServiceRequest is
  the request the work is about (`Task.focus`).
- **Referral travels as resources, counter-referral as a document.**
  The referral is a workflow exchange (`ServiceRequest` + `Task` in
  a transaction Bundle); the counter-referral is a clinical
  document (`Composition` first entry of a document Bundle,
  indexed by a `DocumentReference`) that APS acknowledges receipt
  of, so MHD can carry it.
- **No `Consent` resource** (Q7 — care relationship covers
  sharing); BPPC/PCF set aside. No consent artifact travels.
- **Counts are state on the Task** (decline/chase/re-scheduling
  counts as extensions), exposed by the status operation (OP-7)
  and the offer operations (OP-3/OP-4).
- **Own profiles `Derivacion*`** on the FHIR R4 base resources
  (canonical URLs in the proposal table); the user may choose a
  different base per profile (e.g. `CorePacienteCl` for Patient —
  offered as an association, not assumed).
- **Local extension namespace is `http://derivacion.example.org/fhir/StructureDefinition/`**
  in the step 4 draft; it is a placeholder to be fixed to the real
  guide canonical in step 5 (the proposal says so).
- **Graph geometry**: 12 nodes, 4 cols × 3 rows, Task centre;
  verified mechanically — 0 edges through a node interior,
  exactly 2 right-angle crossings ((1090,495) and (1090,520)).
  The first draft had 2 routing defects found by the mechanical
  check (the `for` edge through HealthcareService, the
  Composition→Encounter edge through Condition) — both fixed by
  re-routing, not by hand-waving. The proposal text was corrected
  to the real crossing count (2, not the 3 first written).
- **IHE fit summary**: full 3 (PIXm ITI-83, PDQm ITI-78, mCSD
  ITI-90 — each for a sub-step, if implemented exactly); partial 8
  (360X PCC-55/56/57/58/60/61 as pattern, XBeR-WD/XDW as pattern,
  Scheduling ITI-115/116/117/118 for the booking half, MHD ITI-65
  for the PI-3 document leg, DSUBm ITI-110 for document
  availability); none 1 (PI-4 status query — explicit "none
  applies"). No point is carried end-to-end by an IHE profile.
- **Sequence diagrams belong to step 5, not step 4** (parent brief
  overrides the fhir-modeling skill default here). Step 4 proposes
  the 12 operations (OP-1…OP-12) so step 5 can build them.
- **360X supplement read live** (Rev. 1.2 TI 2021-04-14):
  PCC-55 Referral Request, PCC-56 Referral Decline, PCC-57
  Referral Outcome, PCC-58 Referral Cancellation, PCC-59 Interim
  Consultation Note, PCC-60 Appointment Notification, PCC-61
  No-show Notification; scope test passes (patient returns to the
  referring provider for continued care, §X.4.1). 360X is
  document-based (CDA over XDM/XDR/MHD) and Trial Implementation —
  pattern only, never the mechanism.

## 2026-11-19 — Step 5 decisions (guide canonical + R4 corrections found by SUSHI)

- **Guide canonical (closes the step 4 open item):** the guide canonical
  is `https://josemandrade.github.io/prueba-his-muse-nvidia/` (the test
  repo's GitHub Pages root, where the CI workflow deploys the guide —
  same pattern as the DAU case). It replaces the step 4 placeholder
  `http://derivacion.example.org/fhir/` everywhere in the guide. Caveat
  recorded in `05-implementation-guide/plan.md`: the test repo holds a
  second case (school vision screening); if that case publishes its own
  guide, it will need its own deployment path decision — this canonical
  is the site root, which today this guide occupies. The `example.org`
  domains that remain are identifier systems in synthetic examples
  (MPI, RUN, APS referral id), not the guide canonical.
- **No `controlled-medications.md` page:** the case has no medications,
  so the controlled-substances page does not apply (recorded in plan.md,
  Plan task 10.22).
- **R4 correction 1 — `Communication.topic`:** the mapping table §11
  maps the triggering state change to `Communication.topic` → Task.
  In R4 `Communication.topic` is a CodeableConcept 0..1, not a
  reference (SUSHI error, fixed 2026-11-19). The guide keeps `topic`
  as the coded transition name (e.g. "accepted"); the Task link is
  `basedOn` (already the join key) and the human-readable notice is
  `payload.contentString`. The mapping table §11 is wrong on this row
  and should be corrected at the next touch of the mapping table.
- **R4 correction 2 — `Task.owner`:** the mapping table §3/§4 maps
  both the accepting service and the accepting practitioner to
  `Task.owner` (0..*). In R4 `Task.owner` is 0..1 (SUSHI error, fixed
  2026-11-19). The guide sets `owner` 0..1 → the accepting service
  (`DerivacionServicio`, the party responsible for the work); the
  accepting practitioner is recorded as the Provenance agent of the
  accept transition in the §3 history (which already requires who/when/
  from/to/reason per transition). The mapping table §3/§4 is wrong on
  this cardinality and should be corrected at the next touch.
- **ValueSet rename:** the ValueSet `DerivacionRol` collided by name
  with the profile `DerivacionRol` (SUSHI duplicate-name warning).
  Renamed to `DerivacionRolVS` (id `derivacion-rol` unchanged); the
  profile keeps the proposal's name `DerivacionRol`.
- **R4 correction 3 — `CarePlan.activity.detail`:** SUSHI error in
  the counter-referral example (Plan task 10.16): in R4
  `CarePlan.activity.detail` is a BackboneElement and its narrative
  text is `detail.description`, not `detail.text` (with
  `detail.status` 1..1 when detail exists). Fixed in examples.fsh.
- **Sequence diagrams live in the guide, not in a `04-sequence-diagrams.md`:**
  unlike the DAU case, this case has no `04-sequence-diagrams.md` file —
  the per-diagram message → operation → IHE → expected-result tables
  live in the guide page `05-implementation-guide/input/pagecontent/
  sequences.md`. The SVG sources live in the case folder
  (`04-sequence-<flow>.svg`); copies go to `input/images/` for the
  published guide (same as the BPMN SVGs and the resource-graph SVG).
- **Sequence renderer tab fix (2026-11-19):** the cancellation `opt`
  tab ("opt [si hay cita reservada]") was half-covered by the hub
  activation bar — tabs were drawn before activation bars. Fixed in
  `render_sequence.py`: fragment tabs are drawn AFTER the activation
  bars; lesson recorded in the generator docstring. Also shortened
  the result-return label `POST /Bundle (document: Composition +
  DocumentReference + Condition + CarePlan)` to `POST /Bundle
  (document)` (too wide, crossed two columns); the detail lives in
  the `sequences.md` operation table.
- **Image widths in the guide:** sequence diagrams display at SVG-native
  width (the PNG is 2×, stays crisp); BPMN parts and the resource graph
  display at PNG-native width; all inside a horizontal-scroll container.
- **CI workflow test caveat:** `.github/workflows/ig-build.yml` is
  written but untested — its test steps (a green push, a broken-FSH
  push that must fail without deploying) require a push and are for
  the parent. Java is not available in this environment, so the IG
  Publisher / FHIR validator do not run locally; full validation runs
  in CI.
- **Transient SUSHI warning (not meaning-changing):** "Failed to load
  automatically-provided hl7.terminology.r4#latest" appeared once in
  the Plan task 10.16 run (network/cache, varies run to run) and did
  not appear in the final run. Recorded in the validation report.

## 2026-11-19 — Step 5 expert-review fixes C1–C9 (review NOT APPROVED)

- **C1 — Composition section slicing:** discriminator changed from
  `code` to `title` — the slices are distinguished by title (each
  section's title is fixed: "Diagnosis", "Plan", "Follow-up
  indications", "Follow-up plan for APS") and the example sets each
  title, so a validator slicing on `title` can assign every section.
  Pinning a code per section was not chosen: the sections carry
  `code.text` only, no coding.
- **C2 — Task.owner on acceptance:** `owner` is the accepting
  service only (`DerivacionServicio`); the accepting practitioner
  goes as the Provenance agent of the accept transition. Fixed in
  `operations.md` (OP-2) and `sequences.md` (diagram 2, row 1).
- **C3 — ValueSet name:** `DerivacionRol` → `DerivacionRolVS` in
  `profiles.md` (the rename itself was a SUSHI duplicate-name fix;
  id `derivacion-rol` unchanged).
- **C4 — Decline-at-creation reference:** C8, not Q7 (Q7 is the
  consent decision).
- **C5 — SUSHI result honesty:** the final run is recorded as it
  ran (0 errors / 0 warnings this run); the transient package-load
  warning varies run to run (reviewer's re-run: 0/1) — 0 errors
  always. The `example.org` sweep now also names the synthetic
  Endpoint address `https://especialidad.example.org/fhir`.
- **C6 — Extension value constraints:** two new local ValueSets
  (`DerivacionResultadoEntrega`: delivered | failed;
  `DerivacionBaseCruce`: identifier | demographics) bound required
  to the two code extensions; range invariants on the integer /
  decimal extensions (decline/chase 0–2, re-scheduling 0–1,
  match confidence 0–1). Guide now has 8 ValueSets / 8 CodeSystems.
- **C7 — Contrareferencia status short:** the profile is the sent
  document; a draft is a Composition without this profile.
- **C8 — Sequence separator pill:** the `alt` guard pill is now
  inset 16 from the fragment border (was ~7, sat on the border);
  the centre is computed with the same width the pill is drawn
  with (size 12.5). Lesson in the `render_sequence.py` comment.
- **C9 — G6 mitigation:** the FHIR validator runs in CI
  (`ig-build.yml`) — not yet executed; no local validator run
  exists (no Java here).

## Step 6 — component (2026-11-19, draft complete, Plan tasks 11.1–11.13)

Rulings del componente (detalle en `06-component/../state.md` y
`06-component/README.md`):

- **Retorno por fallo de agendamiento** (`accepted → rejected`):
  lo exige el paso 3 validado (C4) aunque la tabla del paso 4 no lo
  liste. Transición guardada, solo por OP-4 (segundo rechazo) o R3
  (sin confirmar tras la segunda persecución).
- **Conteo de decline por ciclo de oferta**, no por Appointment: no
  se reinicia en la re-oferta tras un rechazo (si no, el gateway
  "First decline?" nunca vería el segundo rechazo); se reinicia solo
  en un ciclo nuevo tras un no-show (N5). El de chase se reinicia en
  cada oferta; el de re-agendamiento (0–1) nunca.
- **Triggers `booked` y `chase`** añadidos a la tabla de emisores
  nombrados: los diagramas de secuencia registran Communication en
  la reserva (diagrama 3, fila 10) y en cada persecución (fila 5).
  El reenvío del rechazo al agendador NO es Communication (la
  AppointmentResponse es la señal).
- **R3 no se marca como disparada tras una persecución**: se sigue
  por el conteo de chase; si no, la segunda persecución y el retorno
  nunca se evaluarían. Las escalaciones R1/R2/R4/R5 disparan una
  sola vez por plazo.
- **Encounter `planned` de una cita perdida** queda como está y se
  conserva en la historia: la guía no define un `cancelled` de
  encuentro para el no-show (mapeo §6); I4 lo admite. En el
  re-agendamiento la reserva crea un Encounter NUEVO.
- **El conteo de re-agendamiento mide re-agendamientos (0–1)**, no
  no-shows: el primer no-show deja el Task en `scheduled`; el
  re-agendamiento lo lleva a 1; el segundo no-show cierra el Task.
- **La contrareferencia cierra el ciclo con el acuse de recibo**,
  no con el envío (diagrama 5, fila 4; OP-6). El envío desarma R4 y
  bloquea la cancelación. Acuse con trigger nuevo
  `counter-referral-receipt` (aps-admin → hub).
- **Re-apertura no restaura la cita cancelada**: el agendador debe
  re-ofertar. La guía no dice qué pasa con la cita al re-abrir.
- **Conteos en cero no viajan** como extensiones del Task (el
  ejemplo de la guía no los lleva); el Slot pasa a `busy` en la
  reserva, no en la oferta (OP-3).
- El validador FHIR / IG Publisher NO corrió sobre los ejemplos del
  componente (no hay Java aquí; corre en CI).

## 2026-11-19 — Step 6 expert-review fixes C1–C6 (review NOT APPROVED)

- **C1**: R5 no se evaluaba tras el retorno por fallo de
  agendamiento; `retriage_return_at` ahora viaja por
  `_evaluator_state` y `evaluate_escalations` (3 tests nuevos).
- **C2**: la afirmación «31/31 goldens» era falsa: 20/31 instancias
  comparadas por valor en 23 aserciones; las 11 no comparadas se
  listan con su motivo en `validation-report.md` (externos de APS,
  directorio referenciado por id, divergencia documentada del Slot).
- **C3 — destinatarios de notificación**: `DerivacionNotificacion`
  solo admite Patient y DerivacionRol como `recipient`; la
  «especialidad» como Organization ya no es destinataria. Cada
  escalada va al responsable de la acción pendiente (R1 → clínico
  de triaje, R2 → agendador, R4 → especialista, cancelación →
  agendador; rules.md: «el responsable de cada servicio responde a
  las escaladas de su servicio»). El operador del hub es ahora un
  PractitionerRole (`rol-operador-hub`, código `hub-operator` del
  DerivacionRolCS — la guía define el código, pero sus ejemplos no
  materializan el rol): el componente lo siembra en el registro
  (Practitioner `operador-hub`, RUN sintético 44444444-4) y lo usa
  como emisor del hub, destinatario del acuse de recibo y agente de
  la re-apertura. `build_communication` rechaza Organization como
  destinatario; `test_validation.py` verifica los targetProfile del
  perfil generado por SUSHI. **Decisión para el próximo toque del
  paso 5 (no aplicada — la guía está validada)**: añadir el
  PractitionerRole `rol-operador-hub` (y su Practitioner) a los
  ejemplos de la guía, para que el rol exista también en SUSHI y no
  solo en el componente.
- **C4**: la suscripción exportada llevaba claves internas
  (`_active`, `notifications`); `all_resources` vuelca una copia
  sin ellas (la contabilidad en memoria sigue igual).
- **C5**: `decide_retriage` no dejaba Provenance; la decisión de
  APS queda auditada (actor `aps-doctor`, `rol-medico-aps`).
- **C6**: README decía «156 tests»; corregido a 168, con los
  conteos por archivo de la tabla de trazabilidad actualizados.
- **Canonical a subruta (2026-11-20, re-toque del paso 5)**: la guía
  pasa de la raíz del sitio a la subruta
  `derivacion-aps-especialidad` (decisión del usuario: un archivo por
  guía con subrutas). `sushi-config.yaml` canonical =
  `https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad`;
  SUSHI reconstruido 0/0 (74 recursos); las 61 generadas y los 4
  archivos a mano (index.md, terminology.md, plan.md,
  validation-report.md) llevan la nueva URL; la línea `Published
  guide` del README también. El workflow es ahora
  `ig-build-referral.yml` (rama gh-pages, `destination_dir`
  `derivacion-aps-especialidad`).
- **Canonical del componente a subruta (2026-11-20, re-toque del
  paso 6, H1 del revisor)**: el componente estampaba la canonical
  raíz y los goldens también (copias de la guía anterior), así que
  los 168 tests pasaban aunque la guía ya estaba en la subruta.
  `constants.py` CANONICAL pasa a la URL de subruta; goldens
  re-copiados desde fsh-generated/ reconstruido; ejemplos
  regenerados con el CLI; nuevo test que compara la canonical del
  componente con la de `sushi-config.yaml` en cada corrida.
