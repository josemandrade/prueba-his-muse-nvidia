# State — referral-aps-especialidad

- Last updated: 2026-11-19 14:00 America/Santiago
- Current step: step 2 BPMN DRAFT complete — three parts built, mechanical
  check 0/0 on all three, PNGs rendered at 2× and inspected; STOPPED for
  parent expert review + step 2 validation (do NOT commit until validated)
- Current task: STOPPED — report the step 2 draft to the parent
- Last completed: step 2 BPMN draft — Part A referral-triage (52 shapes,
  42 flows), Part B scheduling-counterreferral (64 shapes, 57 flows),
  Part C status-query (16 shapes, 11 flows); `02-bpmn-model.md` holds the
  scan, PI register, state machine, SLAs and part descriptions; builder
  `build_bpmn.py` + `parts_data.py` in the case folder; two clone-root tool
  fixes (checker: flow-node shapes only; renderer: vector envelope marker).
  A modeling gap found while writing the PI register (Part A had no
  message flow delivering the referral to the specialty) was fixed with
  m11 (hub → specialty, PI-0 second leg), re-checked 0/0.
- Recovery note (2026-11-19 10:36): the previous coordinator errored out
  mid-task (output token cap) after claiming Plan task 5 (IHE landscape
  scan, "12 profiles verified live") COMPLETE and "written into
  02-bpmn-model.md". That is NOT TRUE ON DISK: no 02-bpmn-model.md exists
  anywhere for this case (verified by the parent with a filesystem
  search). The scan results survive ONLY as the summary below. Plan task 5
  is reset to REDO. The renderer and checker it created DO exist and are
  reusable: render_bpmn.py and check_bpmn.py in the clone root (created
  10:28). No .bpmn files exist yet for this case. Also reconciling: the
  summary says "12 profiles" but lists 14 names (mCSD, Scheduling, MHD,
  360X, XBeR-WD, XDW, PIXm, PDQm, QEDm, DSUBm, ATNA, CT, XDS.b, BPPC) —
  recount during the redo; the list is a CHECKLIST to re-verify live, not
  established fact.
- Next action: parent runs independent expert review on the step 2 draft
  and validates step 2 (parent acts as validating user). Then step 3
  (entities). Do NOT commit step 2 until validated. Do NOT attempt the
  Step 1 push in this run.
- Open questions: none
- Blockers: STEP 1 PUSH BLOCKED — GitHub App cannot initialize the empty repo
  (403 Resource not accessible by integration on PUT contents/README.md,
  twice, second time with a root README.md in the manifest — hypothesis
  REFUTED); approval was granted both times, so this is not an approval
  problem. Diagnosis: the repo is most likely not in the GitHub App
  installation with write access (the earlier "coverage verified" check only
  proved read visibility via the 409). The user is being asked in parallel to
  add prueba-his-muse-nvidia to the App installation
  (https://github.com/apps/meta-muse-ai/installations/new). The push retry
  happens after that fix — DO NOT attempt another push in this run. Local
  work (scan + step 2) continues meanwhile; the Step 1 push is independent
  of it. Step 1 remains committed locally (6831859); repo verified still
  empty (409); no sync record written.
- Resume by / next review date: none
- Waiting for: parent expert review + step 2 validation
- Files changed in this task: 01-use-case-spec.md, README.md, decisions.md,
  validation.md, state.md, 02-bpmn-model.md,
  02-bpmn-model-referral-triage.bpmn/.svg/.png,
  02-bpmn-model-scheduling-counterreferral.bpmn/.svg/.png,
  02-bpmn-model-status-query.bpmn/.svg/.png, build_bpmn.py, parts_data.py;
  clone-root tools fixed: check_bpmn.py, render_bpmn.py
- Do not redo: step 1 spec draft; review fixes C1–C12; Q1–Q7 decisions; re-check
  fixes N1–N5; step 1 validation; local commit 6831859; scan redo (14
  profiles); step 2 BPMN draft (three parts, CHECK OK, PNGs inspected)

Tasks:
- Plan task 1: complete (step 1 spec drafted)
- Plan task 2: complete (review fixes C1–C12 applied to the spec text; Q1–Q7 recorded)
- Plan task 3: complete (re-check fixes N1–N5 applied to the spec text; decisions and validation recorded)
- Plan task 4: complete (step 1 committed 6831859; push BLOCKED at repo initialization 403 — App installation fix pending with the user; push retry after the fix, not in this run)
- Plan task 5: complete (REDO — scan re-verified live, 14 profiles,
  written into 02-bpmn-model.md; recount reconciled: 14, not 12)
- Plan task 6: complete (draft) — step 2 BPMN three-part split model built
  (Part A 52 shapes / 42 flows, Part B 64 / 57, Part C 16 / 11),
  mechanical check 0/0 on all three parts, PNGs rendered at 2× and
  inspected; STOPPED for parent expert review + step 2 validation; do NOT
  commit until validated
