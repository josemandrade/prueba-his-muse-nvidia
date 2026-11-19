# Derivación APS → especialidad con contrareferencia — Health Interoperability Use Case

Built with health-interop-superpowers v0.39.0. Source case: audit 1 vehicle
(`pack-audit-2026-11-12-referral-case.md`, 2026-11-12; audit 1 implemented as
v0.19.0 — not re-litigated here).

## Status

| Step | Artefact | Status | Validated by | Date |
|------|----------|--------|--------------|------|
| 1 | `01-use-case-spec.md` | validated | parent (validating user) | 2026-11-19 |
| 1–2 (scan) | `02-bpmn-model.md` (§ scan) | drafted | — | 2026-11-19 |
| 2 | `02-bpmn-model.md` (+ 3 `.bpmn` / `.svg` / `.png`) | draft — awaiting parent expert review + validation | — | 2026-11-19 |
| 3 | `03-entities-data.md` | pending | — | — |
| 4 | `04-fhir-proposal.md` | pending | — | — |
| 4 | `04-sequence-diagrams.md` (+ `04-sequence-<flow>.svg`) | pending | — | — |
| 5 | `05-implementation-guide/` | pending | — | — |
| 6 | `06-component/` | pending | — | — |

## Next step

Step 2 BPMN DRAFT complete (three parts, mechanical check 0/0, PNGs
inspected) — STOPPED for parent expert review and step 2 validation.
Do NOT commit step 2 until validated. Push still BLOCKED (see Blockers)
— the user is fixing the GitHub App installation in parallel; do NOT
attempt any push in this run.

## Blockers

- Push blocked 2026-11-19: snapshot push failed at repo initialization —
  `failed to initialize repository: failed to create initial file: PUT
  .../contents/README.md: 403 Resource not accessible by integration`. The
  approval was granted; the GitHub App could not create the initial file in
  the empty repo. Repo verified still empty (409) after the failure; no sync
  record written. The parent acts as validating user; the user is notified
  only when all six steps are finished.

## Work Folder

`docs/health-interop/2026-11-19-referral-aps-especialidad/`

## Artefacts

- `01-use-case-spec.md` — Clinical use case specification (validated 2026-11-19)
- `02-bpmn-model.md` — BPMN model index: IHE landscape scan (14 profiles),
  PI register, state machine, SLAs, part descriptions (draft 2026-11-19,
  awaiting validation)
- `02-bpmn-model-referral-triage.bpmn` / `.svg` / `.png` — Part A
  (52 shapes, 42 flows, CHECK OK)
- `02-bpmn-model-scheduling-counterreferral.bpmn` / `.svg` / `.png` — Part B
  (64 shapes, 57 flows, CHECK OK)
- `02-bpmn-model-status-query.bpmn` / `.svg` / `.png` — Part C
  (16 shapes, 11 flows, CHECK OK)
- `build_bpmn.py`, `parts_data.py` — BPMN builder + geometry tables
- `state.md` — Checkpoint for resumption
- `decisions.md` — Recorded decisions
- `validation.md` — Validation log (step 1 validated)
