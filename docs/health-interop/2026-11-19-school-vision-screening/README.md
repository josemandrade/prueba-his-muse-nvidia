# School Vision Screening - Health Interoperability Use Case

## Published guide
https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/

## Status

| Step | Description | Status |
|------|-------------|--------|
| 1 | Clinical use case specification | **Validated** ✓ |
| 2 | BPMN modeling | **Validated** ✓ |
| 3 | Entities and data | **Validated** ✓ |
| 4 | FHIR proposal | **Validated** ✓ |
| 5 | Implementation Guide (SUSHI) | **Validated** ✓ |
| 6 | Component build | **Validated** ✓ |

## Current Step
Complete: all 6 steps validated

## Blockers
None

## Work Folder
`docs/health-interop/2026-11-19-school-vision-screening/`

## Artefacts
- `01-use-case-spec.md` - Clinical use case specification (validated)
- `02-bpmn-model.bpmn` - BPMN process model (validated)
- `02-bpmn-model.md` - BPMN description, IHE landscape scan, interoperability points (validated)
- `03-entities-data.md` - Entities and Data (validated)
- `04-fhir-proposal.md` - FHIR Proposal with resource choices, profiles, lifecycle tables, resource graph, operations, IHE profile review (validated)
- `04-mapping-table.md` - Mapping table with all source→FHIR transformations (validated)
- `04-sequence-diagrams.md` - 7 sequence diagrams with operation tables (validated)
- `05-implementation-guide/` - Implementation Guide built with SUSHI (0 errors / 0 warnings; 20 profiles, 6 CodeSystems, 7 ValueSets, 19 examples; canonical on the school subpath) (validated)
- `06-component/` - Component implementing the guide: 11 operations, 6 state machines, rule evaluator, 20 profile builders, FHIR client; 136 unit tests pass, 0 warnings (validated)
- `state.md` - Checkpoint for resumption
- `decisions.md` - Recorded decisions including Q1-Q5 answers (Step 1) and Q1-Q7 answers (Step 3) and Q1-Q7 answers (Step 4)
- `validation.md` - Process expert reviews with findings, resolutions, and user validations