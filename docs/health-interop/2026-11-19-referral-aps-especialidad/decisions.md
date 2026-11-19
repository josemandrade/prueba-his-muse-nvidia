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
