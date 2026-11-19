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
