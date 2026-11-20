# Derivación APS → especialidad con contrareferencia — Health Interoperability Use Case

Built with health-interop-superpowers v0.39.0. Source case: audit 1 vehicle
(`pack-audit-2026-11-12-referral-case.md`, 2026-11-12; audit 1 implemented as
v0.19.0 — not re-litigated here).

## Status

| Step | Artefact | Status | Validated by | Date |
|------|----------|--------|--------------|------|
| 1 | `01-use-case-spec.md` | validated | parent (validating user) | 2026-11-19 |
| 1–2 (scan) | `02-bpmn-model.md` (§ scan) | validated | parent (validating user) | 2026-11-19 |
| 2 | `02-bpmn-model.md` (+ 3 `.bpmn` / `.svg` / `.png`) | validated | parent (validating user) | 2026-11-19 |
| 3 | `03-entities-data.md` | validated | parent (validating user) | 2026-11-19 |
| 4 | `04-fhir-proposal.md` + `04-mapping-table.md` + `04-fhir-proposal-graph.svg` | validated | parent (validating user) | 2026-11-19 |
| 5 | `04-sequence-<flow>.svg` (7) + `05-implementation-guide/input/pagecontent/sequences.md` | validated | parent (validating user) | 2026-11-19 |
| 5 | `05-implementation-guide/` (SUSHI 0/0, 74 recursos, 12 páginas, workflow CI, informe de validación) | validated | parent (validating user) | 2026-11-19 |
| 6 | `06-component/` | validated | parent (validating user) | 2026-11-19 |

## Next step

All 6 steps VALIDATED 2026-11-19 (`06-component/`, Python 3.12
solo stdlib, 168 tests en verde, 3 escenarios end-to-end con
63 ejemplos JSON, README con trazabilidad, informe de validación).
Expert review NOT APPROVED first (0 critical/high, 3 medium + 3 low
C1–C6); fixes C1–C6 applied; focused re-check APPROVED
(0 critical/high/medium, 0 new findings). Next: local commit of
step 6, then notify the user that all 6 steps are finished.
Pushes of steps 2–6 remain pending — the step 2 retry card expired;
the user re-approves when ready.

## Blockers

- None. The step 1 push SUCCEEDED 2026-11-19 11:01 (commit 155ffa02)
  after the user added the repo to the GitHub App installation; the
  earlier 403 block is resolved. The parent acts as validating user;
  the user is notified only when all six steps are finished.

## Work Folder

`docs/health-interop/2026-11-19-referral-aps-especialidad/`

## Artefacts

- `01-use-case-spec.md` — Clinical use case specification (validated 2026-11-19)
- `02-bpmn-model.md` — BPMN model index: IHE landscape scan (14 profiles),
  PI register, state machine, SLAs, part descriptions (validated 2026-11-19)
- `02-bpmn-model-referral-triage.bpmn` / `.svg` / `.png` — Part A
  (52 shapes, 43 flows, CHECK OK)
- `02-bpmn-model-scheduling-counterreferral.bpmn` / `.svg` / `.png` — Part B
  (65 shapes, 59 flows, CHECK OK)
- `02-bpmn-model-status-query.bpmn` / `.svg` / `.png` — Part C
  (16 shapes, 11 flows, CHECK OK)
- `03-entities-data.md` — Step 3 entities and data (validated 2026-11-19):
  13 entities, PI data-flow summary, terminologies
- `04-fhir-proposal.md` — Step 4 FHIR proposal (validated 2026-11-19): resource choices + rejected
  alternatives, 12 own profiles (`Derivacion*`), lifecycle tables,
  terminology, 12 proposed operations, IHE review per PI, gaps/risks,
  associations offered, 2 short JSON examples
- `04-mapping-table.md` — Step 4 field-by-field mapping (validated
  2026-11-19): all 13 entities + fields → FHIR resource/element,
  incl. the honest "no FHIR equivalent" for the declined-referral
  record (§12) and the Task-transition entities (§4, §13)
- `04-fhir-proposal-graph.svg` — Resource graph (draft 2026-11-19):
  12 nodes, Task centre, Bundle frame; geometry verified
  mechanically (0 edges through a node, 2 right-angle crossings)
- `render_fhir_graph.py` — Graph renderer (adapted from the DAU
  precedent `~/workspace/health-interop-test-run/render_fhir_graph.py`)
- `build_bpmn.py`, `parts_data.py` — BPMN builder + geometry tables
- `05-implementation-guide/` — Step 5 Implementation Guide (validated
  2026-11-19, SUSHI 0/0, 74 recursos): `sushi-config.yaml`
  (canonical https://josemandrade.github.io/prueba-his-muse-nvidia/),
  `input/fsh/` (12 perfiles, 14 extensiones, 8 CodeSystems +
  8 ValueSets, 31 ejemplos), `input/pagecontent/` (12 páginas),
  `input/images/` (BPMN + grafo + secuencia PNG/SVG),
  `validation-report.md`
- `04-sequence-<flow>.svg` — 7 diagramas de secuencia (request,
  triage, schedule, attend, result-return, status-query,
  cancellation; check 0/0, PNGs inspeccionados)
- `render_sequence.py` — Generador de diagramas de secuencia
  (adaptado del DAU `~/workspace/health-interop-test-run/render_sequence.py`)
- `.github/workflows/ig-build.yml` — Workflow CI (SUSHI + IG Publisher
  + Pages; en la raíz del repo)
- `06-component/` — Step 6 component (validated 2026-11-19):
  Python 3.12 solo stdlib (`src/derivacion/`), 168 tests en verde,
  3 escenarios end-to-end (`examples/`, 63 JSON), CLI
  (`python3 -m derivacion.cli <accepted|rejected|no-show>`), README
  con trazabilidad, `validation-report.md`
- `state.md` — Checkpoint for resumption
- `decisions.md` — Recorded decisions
- `validation.md` — Validation log (steps 1–6 validated)
