# Validation — referral-aps-especialidad

## 2026-11-19 — Step 1 draft written, awaiting review

- Artefact: `01-use-case-spec.md` (draft)
- Tool / profile: —
- Result: pending — awaiting process-expert-review (run by the parent) and parent
  validation (the parent acts as validating user)
- Failures: —
- Evidence: —

## 2026-11-19 — Step 1 expert review: NOT APPROVED, fixes applied, re-check pending

- Artefact: `01-use-case-spec.md` (revised after review)
- Tool / profile: process-expert-review (run by the parent)
- Result: NOT APPROVED — 8 medium (C1–C8, blocking) + 4 low (C9–C12). All 12
  fixes applied to the spec text; re-check pending with the parent.
- Failures: C1 triage owner unnamed (scheduler named as triage owner); C2
  single-path state chain hid the rejection path; C3 cancellation limited to
  before acceptance; C4 no offer-decline → re-offer loop; C5 notification
  senders unpinned and §3.1/§4 inconsistent; C6 priority values undefined;
  C7 no re-triage decision SLA; C8 no patient-declines-the-referral branch;
  C9 Q1–Q7 recorded nowhere in the folder; C10 hub transit vs storage unclear;
  C11 no rule for the patient dying with an open referral; C12 no patient
  contact data in the PI-0 minimum data set.
- Evidence: fixes in `01-use-case-spec.md` (§2 role table, §3.1–§3.8, §4, §5,
  §6, §8); decisions recorded in `decisions.md` (review fixes C1–C12); Q1–Q7
  recorded below.

## 2026-11-19 — Step 1 expert re-check: APPROVED, conditional on N1–N5 fixes

- Artefact: `01-use-case-spec.md` (revised after re-check)
- Tool / profile: process-expert-review re-check (run by the parent)
- Result: APPROVED — all 12 prior findings C1–C12 are fixed in the spec text.
  Step 1 approved CONDITIONAL on fixing 5 new issues before BPMN modeling:
  N1 (medium) no closure rule for the scheduling-failure return to APS
  re-triage; N2 (low) generic timeout bullet unscoped; N3 (low) second chase
  unpinned; N4 (low) `counter-referred` missing from the terminal-states list;
  N5 (low) post-no-show re-scheduling offer rules unstated. All 5 fixes
  applied to the spec text per the parent's rulings; step 1 pending the
  parent's final validation check.
- Failures: —
- Evidence: fixes in `01-use-case-spec.md` (§3.1 state machine and terminal
  states, §3.4 confirm loop and no-show, §3.8 timeout bullet); decisions
  recorded in `decisions.md` (re-check fixes N1–N5).

## 2026-11-19 — Step 1 final validation: VALIDATED

- Artefact: `01-use-case-spec.md` (validated)
- Tool / profile: parent final validation (parent acts as validating user),
  after process-expert-review re-check APPROVED
- Result: VALIDATED — expert re-check APPROVED C1–C12 and verified N1–N5 in
  the spec text. Step 1 closed; proceed to commit + push, IHE landscape scan,
  and step 2 BPMN.
- Failures: —
- Evidence: fixes in `01-use-case-spec.md` (§3.1 state machine and terminal
  states, §3.4 confirm loop and no-show, §3.8 timeout bullet); decisions
  recorded in `decisions.md` (re-check fixes N1–N5).

## Resolved questions Q1–Q7 (decided 2026-11-19 by the parent, acting as validating user)

- **Q1 — SLAs:** What are the SLAs for each wait (acceptance, appointment offer,
  counter-referral, timeout escalation)? Proposal: acceptance 5 working days
  from referral creation (2 for urgent); appointment offered 10 working days
  from acceptance; counter-referral 5 working days from the specialty encounter;
  on timeout the hub escalates to the specialty and notifies APS. Decision:
  accepted as proposed. Recorded in §3.8 and `decisions.md` (SLAs).
- **Q2 — Hub role:** What is the hub's role? Proposal: routing + state-tracking
  intermediary + escalation owner; holds the referral state, not the full
  clinical detail. Decision: accepted as proposed. Recorded in §2, §5 and
  `decisions.md` (hub as intermediary).
- **Q3 — Patient notification:** Who informs the patient at each step? Proposal:
  the patient is informed at acceptance/rejection, at the appointment offer, and
  at the counter-referral outcome. Decision: accepted as proposed EXCEPT the
  counter-referral outcome notification moves to APS — APS admin informs the
  patient of acceptance/rejection and of the counter-referral outcome; the
  specialty scheduler sends the appointment offer (via the hub, APS admin
  notified of the offer); APS admin also informs the patient at referral
  creation. Recorded in §2, §3.1, §4 and `decisions.md` (review fix C5).
- **Q4 — Rejection loop:** What happens on rejection — who re-triages and when
  does the referral close? Proposal: APS re-triages; the referral closes as
  rejected only after the APS re-triage decision. Decision: accepted as proposed.
  Recorded in §3.1, §3.3 and `decisions.md` (review fix C2).
- **Q5 — No-show:** What happens when the patient does not attend? Proposal: one
  re-scheduling is offered; after a second no-show the referral closes as
  no-show and APS is informed. Decision: accepted as proposed. Recorded in
  §3.4.
- **Q6 — Priority:** What are the priority values and who assigns them? Proposal:
  routine / urgent; urgent halves the acceptance SLA; assigned by the APS doctor
  at referral creation. Decision: accepted as proposed. Recorded in §3.2, §3.7,
  §3.8 and `decisions.md` (review fix C6).
- **Q7 — Consent:** Is a separate consent needed for the referral? Proposal: the
  care relationship covers referral data sharing; no separate consent for the
  referral itself. Decision: accepted as proposed. Recorded in §4 and
  `decisions.md` (consent).

## 2026-11-19 — Step 2 draft built, awaiting review

- Artefact: `02-bpmn-model.md` + `02-bpmn-model-referral-triage.bpmn`
  (52 shapes, 42 flows) + `02-bpmn-model-scheduling-counterreferral.bpmn`
  (64 shapes, 57 flows) + `02-bpmn-model-status-query.bpmn` (16 shapes,
  11 flows), each with `.svg` and `.png` (2×); builder `build_bpmn.py` +
  `parts_data.py`
- Tool / profile: `check_bpmn.py --check` (clone root), `render_bpmn.py`
  + cairosvg PNG at 2×, visual inspection of all three PNGs
- Result: draft — mechanical check **CHECK OK on all three parts: 0
  diagonal segments, 0 shape crossings, 0 DI elements missing id, 0
  collapsed sub-processes without isExpanded=false**. PNGs inspected:
  labels legible at display size; two tool defects found and fixed in
  the clone root (checker counted pool/lane containers as crossed
  shapes; message-event ✉ glyph rendered as tofu — now a vector
  envelope). One modeling gap found while writing the PI register
  (Part A had no message delivering the referral to the specialty)
  and fixed with m11 (PI-0 second leg), re-checked 0/0. Awaiting
  process-expert-review (run by the parent) and parent validation
  (the parent acts as validating user). Do NOT commit until validated.
- Failures: —
- Evidence: `.bpmn` / `.svg` / `.png` files in the case folder;
  `02-bpmn-model.md` (§§ Model split, PI register, State machine,
  SLAs, Part A/B/C, Modeling notes, Files, Mechanical check);
  decisions recorded in `decisions.md` (step 2 split, event-based
  gateways, count-based gateways, cancellation row, Part C lane,
  builder + tool fixes, m11 gap, SLA shorthand).

## 2026-11-19 — Step 2 expert-review fixes C1–C14 applied (awaiting focused re-check)

- Artefact: `02-bpmn-model.md` + `02-bpmn-model-referral-triage.bpmn`
  (52 shapes, 43 flows) + `02-bpmn-model-scheduling-counterreferral.bpmn`
  (65 shapes, 59 flows) + `02-bpmn-model-status-query.bpmn` (16 shapes,
  11 flows), each with `.svg` and `.png` (2×); builder `build_bpmn.py` +
  `parts_data.py`; renderer `render_bpmn.py` (clone root)
- Tool / profile: `check_bpmn.py --check` (clone root), `render_bpmn.py`
  + cairosvg PNG at 2×, visual inspection of all three PNGs; 360X PDF
  read live (IHE_PCC_Suppl_360X.pdf)
- Result: all 14 review findings fixed — C1 patient rejection notice
  (m12) + doctor notification named; C2 APS notification on both SLA
  escalations (h19/h20 + new admin task); C3 re-scheduled offer
  through the same confirm/chase loop; C4 scheduling-failure return
  linked to the Part A re-triage outcomes + rejected closure; C5
  patient-death cancellation recorded; C6 duration labels + urgency
  note; C7 count-based gateway rename; C8 h6/h7 deviation recorded;
  C9 requester named + non-termination caveat recorded; C10 full
  working-days wording (supersedes the shorthand decision); C11 Part C
  wording aligned to spec §3.7; C12 end-event rename; C13 renderer
  fixes + all three PNGs re-rendered and re-looked, no label clipped
  or struck through; C14 scan wording (ITI-118, ITI-106, 360X Rev.
  1.2 confirmed from the PDF). Mechanical check **CHECK OK on all
  three parts: 0 diagonal segments, 0 shape crossings, 0 DI elements
  missing id, 0 collapsed sub-processes without isExpanded=false**.
  Awaiting the parent's focused re-check and step 2 validation (the
  parent acts as validating user). Do NOT commit until validated.
- Failures: two intermediate CHECK FAILED runs while fixing (m12 first
  route crossed t_accept; h19/h20 first routes crossed the tasks
  above the escalation tasks; g14 first reroute crossed
  t_counterref) — each rerouted and re-checked 0/0.
- Evidence: `.bpmn` / `.svg` / `.png` files in the case folder;
  `02-bpmn-model.md` (§§ scan, PI register, State machine, SLAs,
  Part A/B/C, Modeling notes, Files, Mechanical check); fix decisions
  in `decisions.md` (2026-11-19 — Step 2 expert-review fixes C1–C14).

## 2026-11-19 — Step 2 re-check polish N1/N2 applied (awaiting step 2 validation)

- N1 (LOW): cancellation task in Parts A and B relabelled "Record
  cancellation (incl. patient death); notify all parties" (`t_cancel_a`,
  `t_cancel_b` in `parts_data.py`); the death cause and reason are also
  noted in the modeling notes of `02-bpmn-model.md`. Verified: grep
  finds "patient death" 1× in each of the two `.bpmn` files.
- N2 (LOW, observation): receipt-branch convention recorded in the
  modeling notes — `t_pat_create`, `t_pat_notice2` (Part A, Patient
  pool) and `t_admin_notify_offer`, `t_admin_esc` (Part B, APS admin
  lane) have no outgoing sequence flow and no end event by convention;
  no end events added.
- Rebuilt, mechanical check CHECK OK on all three parts (0 diagonal
  segments, 0 shape crossings, 0 DI elements missing id, 0 collapsed
  sub-processes without isExpanded=false); PNGs re-rendered at 2× and
  re-looked — the lengthened cancellation label is legible in both
  parts, no clipping or overlap. Awaiting the parent's step 2
  validation (the parent acts as validating user). Do NOT commit until
  validated.

## 2026-11-19 — Step 2 final validation: VALIDATED

- Artefact: `02-bpmn-model.md` + three-part BPMN (Part A referral-triage 52
  shapes / 43 flows, Part B scheduling-counterreferral 65 / 59, Part C
  status-query 16 / 11), each with `.bpmn` / `.svg` / `.png` (PNG at 2×);
  builder `build_bpmn.py` + `parts_data.py`.
- Tool / profile: process-expert-review (run by the parent, independent
  reviewer) + focused re-check (run by the parent, independent reviewer).
- Result: VALIDATED 2026-11-19 by the parent, acting as validating user
  (per the user's delegation 2026-11-19: "valida todo tú, avisame cuando
  termines todos los pasos"). First review NOT APPROVED (6 medium C1–C6 +
  8 low C7–C14); all 14 fixes applied and verified in the XML by the
  focused re-check: APPROVED, 0 critical/high/medium, 1 low residual (N1)
  + 1 low observation (N2). N1 (name the patient-death reason on the
  cancellation row) and N2 (record the receipt-branch convention) applied
  as polish before this validation.
- Failures fixed: C1 rejection notice to patient (m12) + doctor named on
  both decision paths; C2 APS notification on both Part B SLA escalations
  (h19/h20 → `t_admin_esc`); C3 re-scheduled offer through the same
  confirm/chase loop; C4 scheduling-failure return linked to Part A
  re-triage outcomes + rejected closure; C5 patient-death closure
  (doc-recorded, then annotated on the cancellation row — "patient death"
  1× in each of Parts A and B); C6 duration labels on all timeout
  branches ("5 working days (2 if urgent)", "10 working days",
  "5 working days", "3 working days") with the urgent variant justified
  as one data-driven wait; C7 "First re-scheduling?"; C8 h6/h7 deviation
  recorded; C9 cancellation requester named + non-termination caveat;
  C10 full "working days" wording; C11 Part C return per spec §3.7;
  C12 end-event rename; C13 label legibility (renderer fixes + nudges,
  canvas expansion); C14 ITI-118 "Search Patient Appointments", MHD
  ITI-106 Generate Metadata, 360X Rev. 1.2 confirmed from the PDF.
- Evidence: mechanical check CHECK OK on all three parts (0 diagonal
  segments, 0 shape crossings, 0 DI elements missing id — re-run by the
  parent); IHE scan claims spot-checked live by the parent (Scheduling
  v1.0.0, MHD v4.2.5 + ITI-106) and by both reviewers (10 of 14 + C14
  trio, incl. the XDS.b orders quote verbatim and the 360X PDF title
  page); PNGs looked at by the parent and both reviewers.
- Recorded deviations (in `02-bpmn-model.md` modeling notes): event-based
  gateways drawn as exclusive (renderer limitation); message flows h6/h7
  land on gateways (recorded deviation); cancellation row does not
  terminate the in-flight main flow (hub record is the authority);
  notification-receipt tasks end their branch without an end event
  (standing convention).

## 2026-11-19 — Step 3 draft written, awaiting review

- Artefact: `03-entities-data.md` (693 lines, 6,744 words) — 13 entities
  (Patient, Referral request, Workflow state record, Triage decision,
  Appointment + Slot, Specialty encounter, Counter-referral,
  Practitioner, Organisation / care service, MPI identity record,
  Notification, Declined-referral record, Cancellation record), each
  with name, definition, owning system, fields (required / optional /
  derived, source, form), identifiers, lifecycle states + who may
  change each, dedup key, late / out-of-order rule, correction rule;
  plus a data-flow summary per PI (PI-0…PI-4), a terminologies table
  (SNOMED CT reason, ICD-10 diagnosis, LOINC exams, local
  specialty/service catalogue, local priority / rejection-reason /
  state / channel lists), a data-quality and ownership summary, 3 open
  questions deferred to step 4, and a handoff to step 4.
- Tool / profile: entities-data skill (pack v0.39.0); grounded in the
  validated spec (`01-use-case-spec.md`) and BPMN (`02-bpmn-model.md` +
  three parts, PI register, state machine, SLAs, Q1–Q7, C1–C12, N1–N5).
- Result: draft — awaiting process-expert-review (run by the parent)
  and parent validation (the parent acts as validating user). Do NOT
  commit until validated. File name note: the brief named
  `03-entities.md`, but the canonical name per `work-structure.md`
  and the skill is `03-entities-data.md` (already the README's listed
  artefact); recorded in `decisions.md`.
- Failures: —
- Evidence: `03-entities-data.md` in the case folder; README status
  table updated (step 3 draft, step 4 next); Plan task 8 in
  `state.md`.

## 2026-11-19 — Step 3 expert review: NOT APPROVED, fixes C1–C10 applied, re-check pending

- Artefact: `03-entities-data.md` (revised after review)
- Tool / profile: process-expert-review (run by the parent)
- Result: NOT APPROVED — 5 medium (C1–C5) + 5 low (C6–C10). All 10
  fixes applied to the entities text; re-check pending with the
  parent. The parent spot-checked all five mediums in the text and
  they hold.
- Failures: C1 hub operator role missing from §8 (spec §2 names it,
  BPMN hub lane is "Hub operator"); C2 `re-offered` as a state vs
  "a new offer is a new appointment identifier"; C3 encounter
  lifecycle mis-modeled the no-show (linear chain ending in
  `cancelled`, double-recorded via the Attendance field); C4
  re-triage deadline undefined for the scheduling-failure return
  and the state during that re-triage unstated; C5 notification
  definition and enums excluded the specialty (sender: specialist;
  recipient: specialty, target of escalations h19/h20); C6 "final,
  no un-accept" vs supersession; C7 "identity pending" / "routing
  pending" sub-states undefined in §3 and the identity hold
  contradicting the BPMN; C8 "Requested date (if any)" outside the
  PI-0 minimum data set; C9 dedup key vs the re-open path; C10
  lifecycle ending in an unnamed "terminal".
- Evidence: fixes in `03-entities-data.md` (§1 identity hold
  dropped, §2 requested-date field dropped, §3 re-triage deadline
  + scheduling-failure state, §4 supersession sentence, §5
  re-offer rule, §6 encounter branches, §7 `received` final state,
  §8 six roles, §9 routing hold dropped, §11 widened definition +
  enums, §13 dedup key, handoff step-4 note); choices recorded in
  `decisions.md` (Step 3 expert-review fixes C1–C10).
- Re-check polish (2026-11-19, 2 low findings, applied after the
  focused re-check APPROVED step 3): N1 §5 `cancelled` row now
  names the specialty scheduler (on patient decline) and covers
  "Offer or booked appointment cancelled"; N2 §3 `rejected` row
  names the hub operator as recorder of the scheduling-failure
  return, mirrored in the §2 `rejected` row. N3 recorded in
  `decisions.md` as a noted spec widening for the next spec touch
  (spec §3.8 second trigger); `01-use-case-spec.md` NOT edited.

## 2026-11-19 — Step 3 final validation: VALIDATED

- Artefact: `03-entities-data.md` (736 lines; 13 entities, data flow per
  PI, terminologies, data-quality summary, handoff to step 4).
- Tool / profile: process-expert-review (run by the parent, independent
  reviewer) + focused re-check (run by the parent, independent reviewer).
- Result: VALIDATED 2026-11-19 by the parent, acting as validating user
  (per the user's delegation 2026-11-19: "valida todo tú, avisame cuando
  termines todos los pasos"). First review NOT APPROVED (5 medium C1–C5 +
  5 low C6–C10); all 10 fixes applied and verified in the text by the
  focused re-check: APPROVED, 0 critical/high/medium, 3 new low findings
  (N1–N3). N1 (decline path in the §5 `cancelled` row) and N2 (hub
  operator as recorder of the return-driven `rejected` transition, mirrored
  in §2) applied as polish before this validation. N3 (spec §3.8 names
  only the rejection trigger) recorded in decisions.md as a one-line spec
  widening for the next spec touch; the validated spec was NOT edited.
- Failures fixed: C1 hub operator as sixth Practitioner role; C2 each
  offer is a new Appointment (`re-offered` dropped, declined offer's
  appointment → `cancelled`); C3 no Encounter on a no-show (lives on the
  Appointment only), §6 lifecycle as branches, Attendance field dropped;
  C4 re-triage deadline derives from the trigger (rejection or
  scheduling-failure return), referral in state `rejected` during a
  scheduling-failure re-triage; C5 notifications widened to the specialty
  (specialist sender, specialty recipient); C6 supersession vs
  cancellation; C7 pending-hold rules dropped; C8 requested-date field
  dropped; C9 dedup key covers duplicate deliveries, post-re-open
  cancellation is new; C10 §7 ends in named state `received`.
- Evidence: focused re-check verified each fix in the text against the
  validated spec and BPMN; the first reviewer verified live that R4
  `Encounter.status` includes `entered-in-error` (and has no `scheduled`
  — value is `planned`), `Appointment.status` includes `noshow` and
  `cancelled` (and has no `offered`/`confirmed`/`re-offered`/`attended`),
  `RequestStatus` includes `draft`, and the 360X persistent referral
  identifier (§X.1.3.1 of the Rev. 1.2 supplement). The R4 status
  mappings are recorded in the step 4 handoff of `03-entities-data.md`.
- File-name decision: the brief said `03-entities.md`, but
  `work-structure.md`, the `entities-data` skill, and the case README fix
  the name as `03-entities-data.md`; the canonical name was used
  (recorded in decisions.md).

## Step 4 — FHIR proposal (DRAFT, not validated)

- Draft: `04-fhir-proposal.md` + `04-mapping-table.md` +
  `04-fhir-proposal-graph.svg` + `render_fhir_graph.py`, written
  2026-11-19. STOPPED for the parent's expert review and step 4
  validation. Do NOT commit until validated. Do NOT push in this run.
- Coverage: all 13 entities mapped (mapping table §§1–13 +
  supporting resources); 12 own profiles with base canonical URLs
  and the alternative-base note; lifecycle tables for Task,
  ServiceRequest, Appointment, Encounter, CarePlan; terminology
  table (LOINC 11524-6 / 33762-6 / 57133-1 / 11488-4 / 34099-2,
  SNOMED CT 84114007 / 417996009, ICD-10 I50.2, all verified live
  2026-11-19); 12 proposed operations OP-1…OP-12; IHE review per
  PI-0…PI-4 (full 3 / partial 8 / none 1, PI-4 explicit none);
  gaps G1–G7; associations offered; 2 short synthetic JSON
  examples (ServiceRequest + Task).
- Evidence: live verifications done 2026-11-19 (360X supplement
  PDF Rev. 1.2 TI 2021-04-14; XBeR-WD wiki; R4 value sets
  AppointmentStatus 10 / TaskStatus 12 / EncounterStatus 9 /
  RequestStatus 7; LOINC via loinc.org; SNOMED CT 84114007 via
  tx.hl7chile.cl + EVS). Graph geometry verified mechanically
  (0 node-interior hits, 2 crossings) and visually inspected via
  PNG render at 1.5× (labels legible, no clipping after the
  `content` label fix and the `→` → `->` font fix).
- Open: expert review findings (if any) and the parent's step 4
  validation. Sequence diagrams + full operation definitions
  belong to step 5.

## 2026-11-19 — Step 4 expert-review fixes C1–C10 applied (re-check pending)

- Tool / profile: process-expert-review (run by the parent, independent
  reviewer). Verdict on the draft: NOT APPROVED — 0 critical, 0 high,
  4 medium + 6 low. All 10 fixes applied 2026-11-19 12:35 by the fix
  coordinator; focused re-check + step 4 validation by the parent
  still pending.
- C1 (medium): diagnosis code relabelled ICD-10-CM and re-pinned to
  the billable I50.22 "Chronic systolic (congestive) heart failure"
  (proposal terminology table + § Terminology version note +
  mapping-table §7 + graph Condition node); note added that Chile
  uses WHO ICD-10, where no systolic-specific code exists, so the
  SNOMED CT second coding 417996009 carries the precise meaning.
- C2 (medium): OP-3 now creates the Encounter (`status = planned`,
  `appointment` → the Appointment) at booking; OP-5 PATCHes it
  (`planned` → `in-progress` → `finished`); the Encounter lifecycle
  table's `planned` row names OP-3 as the creator. No "POST
  Encounter" wording remains.
- C3 (medium): ServiceRequest `active` → `revoked` added for the
  rejected-closure (APS re-triage decision, PI-1; hub updates it in
  the same transaction as the Task's terminal `rejected`); the
  mapping-table §2 row split into `rejected` (re-triage pending) →
  `active` and `rejected` (closed) → `revoked`.
- C4 (medium): graph `appointment` edge reversed in
  `render_fhir_graph.py` (now Encounter top → Appointment bottom,
  arrowhead at Appointment, matching `Encounter.appointment`); SVG
  re-rendered and visually re-checked via PNG at 1.5× (edge direction
  correct, Condition node reads ICD-10-CM I50.22, labels legible).
- C5 (low): QEDm option renamed "Diagnostic Reports" in both
  occurrences (PI-4 row, set-aside row); 0 "Diagnostic Results"
  remain in either file.
- C6 (low): fit summary reconciled — "partial 13" (13 rows, 6
  distinct partially-fitting profiles: 360X, XBeR-WD, XDW,
  Scheduling, MHD, DSUBm), matching the table after the C7 row.
- C7 (low): PCC-58 row added to the review table (Any PI —
  cancellation; partial pattern) with the direction cap (Initiator
  → Recipient only; specialty/patient-initiated legs are the guide's
  own Communication fan-out).
- C8 (low): `businessStatus` aligned to 1..1 in both files.
- C9 (low): Task `scheduled` → `completed` pinned to the Encounter
  reaching `finished` (not the Appointment reaching `arrived`).
- C10 (low): one line added in the Examples section — the
  example.org canonical is the placeholder replaced in step 5.
- Deliberately NOT changed: the Appointment status chain
  (offered → `proposed`, confirmed → `pending`, booked → `booked`)
  — the reviewer verified live it is correct R4 and the expected
  change to `booked` would be wrong.

## 2026-11-19 — Step 4 final validation: VALIDATED

- Artefacts: `04-fhir-proposal.md` (440 lines; 12 own `Derivacion*`
  profiles on FHIR R4 base resources with canonical URLs +
  alternative-base note, e.g. `CorePacienteCl`; lifecycle tables for
  Task, ServiceRequest, Appointment, Encounter, CarePlan;
  terminology; 12 proposed operations OP-1…OP-12; IHE review per PI;
  gaps G1–G7; associations offered; 2 short synthetic JSON examples),
  `04-mapping-table.md` (550 lines; all 13 entities + fields mapped),
  `04-fhir-proposal-graph.svg` + `render_fhir_graph.py` (12 nodes,
  Task centre, Bundle frame).
- Tool / profile: process-expert-review (run by the parent,
  independent reviewer) + focused re-check (run by the parent,
  independent reviewer).
- Result: VALIDATED 2026-11-19 by the parent, acting as validating
  user (per the user's delegation 2026-11-19: "valida todo tú,
  avisame cuando termines todos los pasos"). First review NOT
  APPROVED (4 medium C1–C4 + 6 low C5–C10); all 10 fixes applied
  and verified in the text by the focused re-check: APPROVED, 0
  critical/high/medium, 1 new low finding (N1, cosmetic stray
  "— +" punctuation in the mapping-table Diagnosis row) — applied
  by the parent before this validation.
- Failures fixed: C1 diagnosis relabelled ICD-10-CM, re-pinned to
  billable I50.22, WHO ICD-10 note added (no systolic code there;
  SNOMED CT 417996009 carries the precise meaning); C2 OP-3 creates
  the Encounter (`planned`) at booking, OP-5 PATCHes it; C3
  ServiceRequest `revoked` on rejected-closure (same transaction as
  the Task's terminal `rejected`); C4 graph `appointment` edge
  reversed (Encounter → Appointment); C5 QEDm option "Diagnostic
  Reports"; C6 fit summary reconciled (partial 13, 13 rows, 6
  profiles); C7 PCC-58 row added with the Initiator → Recipient
  direction cap; C8 `businessStatus` 1..1 in both files; C9 Task
  `completed` pinned to the Encounter reaching `finished`; C10
  example.org placeholder note added in the Examples section.
- Evidence: first reviewer verified live that WHO ICD-10 I50 has
  only I50.0/I50.1/I50.9 and I50.2 is ICD-10-CM non-billable
  (parent re-verified: I50.22 billable, chronic systolic); LOINC
  11524-6 / 33762-6 / 57133-1 / 11488-4 / 34099-2, SNOMED CT
  84114007 / 417996009; 360X Rev. 1.2 TI 2021-04-14, PCC-55–61
  directions; Scheduling ITI-115/116/117/118; MHD ITI-65/66/67/68/
  105/106; DSUBm ITI-110–114; QEDm PCC-44 (10 options, 0 mentions
  of Task/Appointment status); PIXm ITI-83/104, PDQm ITI-78/119,
  mCSD ITI-90/91/130. IHE fit: full 3 (PIXm ITI-83, PDQm ITI-78,
  mCSD ITI-90 — sub-steps only, if implemented exactly), partial 13
  rows across 6 profiles, none 1 (PI-4 status query, explicit
  "none applies"). No point is carried end-to-end by an IHE profile.
  The Appointment status chain (offered → `proposed`, confirmed →
  `pending`, booked → `booked`) was confirmed CORRECT by both
  reviewers against R4 §12.10.2.1 — left unchanged.
- Open item recorded for step 5: the local extension namespace
  `http://derivacion.example.org/fhir/StructureDefinition/` is a
  placeholder to be fixed to the real guide canonical in step 5.

## 2026-11-19 — Step 5 draft complete (DRAFT, not validated)

- Guide built per `05-implementation-guide/plan.md` (Plan tasks
  10.1–10.33 all complete). Canonical
  `https://josemandrade.github.io/prueba-his-muse-nvidia/` — closes
  the step 4 open item (the `example.org` extension namespace
  placeholder); no `example.org` in any generated canonical URL.
- SUSHI v3.21.1 final: **0 errores / 0 advertencias**, exit 0.
  12 perfiles, 14 extensiones, 6 ValueSets, 6 CodeSystems, 31
  instancias, 70 recursos generados. 12 páginas de guía; sin página
  de medicamentos controlados (el caso no tiene medicamentos).
- Sequence diagrams: 7 (request, triage, schedule, attend,
  result-return, status-query, cancellation), `render_sequence.py
  --check` **0/0** (39 mensajes, 0 sin operación, 0 operaciones sin
  diagrama); PNGs a 2× mirados — legibles; 2 defectos de render
  corregidos (pestañas tras las barras de activación; etiqueta OP-6
  acortada).
- BPMN re-verificado: `check_bpmn.py` CHECK OK 0/0 en las tres
  partes; PNGs mirados a 2×. Grafo re-renderizado a 2× e
  inspeccionado (arista `appointment` con la dirección correcta).
- Enlaces internos: 0 problemas (12 páginas, 70 recursos generados,
  22 imágenes).
- R4 corrections found by SUSHI and recorded in decisions.md:
  `Communication.topic` (CodeableConcept, no referencia),
  `Task.owner` (0..1, no 0..*), `CarePlan.activity.detail`
  (`detail.description`); ValueSet `DerivacionRol` → `DerivacionRolVS`.
  Las filas correspondientes de la tabla de mapeo del paso 4 quedan
  pendientes de corrección en su próximo toque.
- CI workflow `.github/workflows/ig-build.yml` written, untested
  (its push tests are for the parent). IG Publisher / FHIR validator
  do not run locally (no Java here); full validation runs in CI.
- Full report: `05-implementation-guide/validation-report.md`.
- Next: independent expert review (parent spawns it), then parent
  validation as validating user. Do NOT commit until validated.
  Do NOT push in this run (step 2 push pending).

## 2026-11-19 — Step 5 expert-review fixes C1–C9 (DRAFT, not validated)

- Review verdict: NOT APPROVED (2 medium C1–C2 + 7 low C3–C9).
  All 9 fixes applied 2026-11-19; SUSHI re-run: **0 errores / 0
  advertencias** (esta corrida; la advertencia transitoria de carga
  de paquetes varía entre corridas — el re-chequeo del revisor dio
  0 errores / 1 advertencia — 0 errores siempre).
  12 perfiles, 14 extensiones, 8 ValueSets, 8 CodeSystems, 31
  instancias, 74 recursos generados.
- C1: discriminador de slicing de `Composition.section` cambiado de
  `code` a `title` (las secciones se distinguen por título; el
  ejemplo fija cada título) — verificado en el JSON generado
  (discriminator path `title`, pattern `Diagnosis`).
- C2: OP-2 en `operations.md` y la fila 1 del diagrama 2 en
  `sequences.md` ahora dicen `owner` = el servicio que acepta; el
  profesional va como agente de Provenance en la entrada de
  aceptación.
- C3: `profiles.md` cita `DerivacionRolVS` (no `DerivacionRol`).
- C4: `public-health.md` atribuye la rama de rechazo en la creación
  a C8 (no Q7).
- C5: `validation-report.md` registra el resultado real de SUSHI
  (0/0 en la corrida final; 0–1 advertencias transitorias según la
  corrida) y el barrido `example.org` menciona la dirección
  sintética del Endpoint `https://especialidad.example.org/fhir`.
- C6: dos ValueSets nuevos (`DerivacionResultadoEntrega`,
  `DerivacionBaseCruce`, con sus CodeSystems) ligados a las
  extensiones de código; invariantes de rango en las extensiones
  de conteo (0–2 rechazos/persecuciones, 0–1 re-agendamientos) y
  confianza (0–1) — verificados en el JSON generado (binding
  required; constraints de error). `terminology.md` lista los 8
  ValueSets locales.
- C7: texto corto de `DerivacionContrareferencia.status` corregido
  (el perfil es el documento enviado; un borrador es una
  Composition sin este perfil).
- C8: píldora `[la paciente rechaza]` del separador `alt` del
  diagrama de agendamiento movida a inset 16 del borde del
  fragmento (antes a 7) — verificado en el recorte del PNG.
- C9: la mitigación G6 en `ihe.md` dice ahora que el validador FHIR
  corre en CI (`ig-build.yml`) — aún no ejecutado.
- Ruling del revisor sobre el ítem 7 (errores R4 de la tabla de
  mapeo del paso 4): NO bloquea — la guía es correcta en R4 donde
  la tabla estaba mal; los archivos validados del paso 4 no se
  tocaron.
- Sequence mechanical check re-run: **CHECK OK** (7 diagramas, 39
  mensajes, 0 sin operación, 0 operaciones sin diagrama).
- Next: focused re-check (parent spawns it), then parent validation
  as validating user. Do NOT commit until validated.
  Do NOT push in this run (step 2 push pending).

## 2026-11-19 — Step 5 final validation: VALIDATED

- Artefacts: `05-implementation-guide/` (sushi-config.yaml,
  canonical `https://josemandrade.github.io/prueba-his-muse-nvidia/`,
  IG id `hl7.fhir.uv.test.derivacion-aps-especialidad`, v0.1.0,
  draft, only dependency `hl7.fhir.r4.core`; 15 FSH files; 12 pages;
  `plan.md` tasks 10.1–10.33; `validation-report.md`), 7 sequence
  diagrams (`04-sequence-*.svg` + PNG/SVG in `input/images/`,
  `render_sequence.py`, `sequences.md` with message → operation →
  IHE profile → expected result tables), CI workflow
  `.github/workflows/ig-build.yml` (SUSHI → IG Publisher → Pages,
  referral paths only, untested).
- Tool / profile: process-expert-review (run by the parent,
  independent reviewer) + focused re-check (run by the parent,
  independent reviewer).
- Result: VALIDATED 2026-11-19 by the parent, acting as validating
  user (per the user's delegation 2026-11-19: "valida todo tú,
  avisame cuando termines todos los pasos"). First review NOT
  APPROVED (2 medium C1–C2 + 7 low C3–C9); all 9 fixes applied
  and verified in the text and generated JSON by the focused
  re-check: APPROVED, 0 critical/high/medium, 0 new findings.
- Failures fixed: C1 Composition section slicing discriminator
  `code` → `title` (four slices carry title patterns; the example
  sets exactly those four titles); C2 OP-2 `owner` = the accepting
  service, the accepting professional as Provenance agent (both
  prose spots); C3 `DerivacionRolVS`; C4 decline-at-creation is C8
  (not Q7); C5 validation-report records the real SUSHI result
  (0/0 final run; 0–1 transient package-load warnings across runs)
  and names the synthetic Endpoint address in the example.org sweep;
  C6 two new ValueSets with required bindings + range invariants
  (decline/chase 0–2, re-scheduling 0–1, confidence 0–1); C7
  Composition status short fixed; C8 schedule-diagram pill moved
  inside the `alt` fragment; C9 G6 mitigation reworded (validator
  runs in CI — not yet executed).
- Evidence: SUSHI re-run independently by the re-check reviewer:
  0 errors / 0 warnings, 12 profiles, 14 extensions, 8 ValueSets,
  8 CodeSystems, 31 instances, 74 resources; sequence mechanical
  check re-run: 0 messages without an operation, 0 operations
  without a diagram (39 send messages, OP-1…OP-12 all covered);
  terminology spot-checked live (LOINC 33762-6, 11524-6); no
  generated resource `url` contains example.org; IG Publisher /
  FHIR validator NOT run locally (no Java) — full validation
  depends on the CI run. The step 4 mapping-table R4 errors
  (`Communication.topic`, `Task.owner`) were ruled NOT blocking by
  the first reviewer: the guide is R4-correct where the mapping
  table was wrong, both corrections documented in mapping.md /
  decisions.md with the exact rows to fix at the next touch; the
  validated step 4 files were left untouched.
- Open items recorded for later: the FHIR validator run (CI,
  `ig-build.yml`, not yet executed); the step 4 mapping-table rows
  §11 and §3/§4 to fix at the next touch (R4 corrections found by
  SUSHI).

- Step 6 component DRAFT COMPLETE 2026-11-19 (Plan tasks 11.1–11.13):
  Python 3.12 solo stdlib, 161 tests en verde (`sh run_tests.sh`),
  31 goldens de SUSHI coinciden (SR, Task, Bundles PI-0/PI-3,
  Appointment, Encounter, Communication, Composition,
  DocumentReference, Condition, CarePlan y resto), 41 tests de
  transiciones (cada legal pasa, cada ilegal lanza
  `ForbiddenTransition`), 25 tests SLA R1–R5, invariantes I1–I6
  limpias en los 3 escenarios, `validating-interop` corrido
  (`06-component/tests/test_validation.py`: codings con
  system/code/display, referencias resueltas, Bundle de documento
  con Composition primera, solo datos sintéticos) — informe en
  `06-component/validation-report.md`. 4 defectos encontrados y
  corregidos durante la validación (plazo de aceptación perdido en
  la creación, id del Bundle PI-0, Slots no volcados en los
  ejemplos, conteo de re-agendamiento que medía no-shows). El
  validador FHIR / IG Publisher NO corrió sobre los ejemplos del
  componente (no hay Java aquí; corre en CI). Pendiente: revisión
  experta independiente + validación del parent como usuario
  validador.

- Step 6 component FINAL VALIDATION: VALIDATED 2026-11-19 (parent
  as validating user). Expert review NOT APPROVED first — 0
  critical, 0 high, 3 medium + 3 low: C1 R5 never fired after a
  scheduling-failure return (`_evaluator_state` dropped
  `retriage_return_at`); C2 the "31/31 golden matches" claim was
  false (recount: 23 assertions, 20/31 instances compared by
  value, 11 excluded); C3 shipped Communications with Organization
  recipients stamped with `DerivacionNotificacion`, whose profile
  allows only Patient / PractitionerRole; C4 exported Subscriptions
  leaked internal keys (`_active`, `notifications`); C5
  `decide_retriage` recorded no Provenance entry; C6 README said
  "156 tests". All 6 fixed (C1: `retriage_return_at` threaded
  through, 3 new R5 tests; C2: claim corrected to 20/31 with the
  11 excluded listed and the Slot divergence named, Slot behavior
  unchanged; C3: escalations routed to the responsible role, hub
  operator materialized as PractitionerRole `rol-operador-hub`
  (code `hub-operator`, verified in the guide's generated
  CodeSystem), `build_communication` rejects Organization
  recipients, profile-target check added to `test_validation.py`
  reading the SUSHI-generated StructureDefinitions, examples
  regenerated; C4: internal keys stripped on export; C5:
  Provenance on re-triage decision, actor `aps-doctor`; C6: README
  168 tests). Focused re-check APPROVED 2026-11-19 — all 6 fixes
  verified in code/text and by driving the component (R5 fires on
  both the second-decline and R3 return paths; golden recount by
  AST: 23 assertions / 20 distinct names; 19 shipped
  Communications, none with an Organization recipient or sender;
  rejected scenario history 2 → 3 entries); 0 critical/high/
  medium, 0 new findings. Parent's own verification: `sh
  run_tests.sh` → 168 tests OK; example 11 recipient now
  PractitionerRole/rol-operador-hub; validation-report.md says
  20/31. Final state: Python 3.12 solo stdlib, OP-1…OP-12
  implemented (no stubs), 3 escenarios end-to-end con 63 ejemplos
  JSON, invariantes I1–I6 limpias, solo datos sintéticos.
- Open items recorded for later: the FHIR validator run (CI,
  `ig-build.yml`, not yet executed); the step 4 mapping-table rows
  §11 and §3/§4 to fix at the next touch (R4 corrections found by
  SUSHI); add `rol-operador-hub` to the guide's examples at the
  next step 5 touch (decisions.md — the guide's CodeSystem already
  carries the `hub-operator` code; only the examples lack the
  role).
- Canonical move (2026-11-20): guide canonical changed from the site
  root to the `derivacion-aps-especialidad` subpath (user decision:
  one workflow per guide, with subpaths); SUSHI rebuilt 0/0; pending
  expert re-review of this re-touch before pushing.
- Component follow-up of the canonical move (2026-11-20, H1 fix):
  `06-component/src/derivacion/constants.py` CANONICAL moved to the
  subpath URL; the 74 goldens re-copied from the rebuilt
  fsh-generated/ and the 63 example JSON regenerated with the CLI;
  `06-component/README.md` URL updated; new test
  `test_component_canonical_matches_guide_canonical` cross-checks the
  component's canonical against `sushi-config.yaml` on every run,
  so a future guide move cannot go unnoticed again.
