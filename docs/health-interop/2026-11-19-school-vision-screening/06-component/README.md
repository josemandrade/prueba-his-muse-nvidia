# School Vision Screening FHIR Component

Implementation of the School Vision Screening Implementation Guide (IG) as a runnable FHIR component.

**Guide Canonical:** https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening  
**IG Source:** `../05-implementation-guide/`  
**SUSHI Build:** 0 errors, 0 warnings (20 profiles, 6 CodeSystems, 7 ValueSets, 19 instances)

---

## Overview

This component implements all 11 operations defined in the IG (16 named variants with OP-4a–f expanded):

| Op ID | Name | FHIR Interaction | IHE Profile |
|-------|------|------------------|-------------|
| OP-1 | Record Screening | `POST Observation` | None |
| OP-2a | Submit Referral | `POST ServiceRequest` + `POST Task` | 360X PCC-55 |
| OP-2b | Cancel Referral | `PATCH ServiceRequest` + `PATCH Task` | 360X PCC-58 |
| OP-2c | Reject Referral | `PATCH ServiceRequest` + `PATCH Task` | 360X PCC-56 |
| OP-2d | Accept Referral | `PATCH ServiceRequest` + `PATCH Task` | 360X PCC-56 |
| OP-3a | Return Assessment | `GET DiagnosticReport` / `POST DocumentReference` | 360X PCC-61 / MHD ITI-65 |
| OP-3b | Return Full | `POST DocumentReference` | MHD ITI-65 |
| OP-4a-f | Send to Primary Care | `POST DocumentReference` (6 types) | MHD ITI-65 |
| OP-5 | Accommodation Notice | `POST Communication` | None |
| OP-6 | Query Demographics | `GET Patient` | PIXm ITI-83 / PDQm ITI-78 |
| OP-7 | Subscribe | `POST Subscription` | DSUBm ITI-110/112 |

---

## Prerequisites

- Python 3.11+
- FHIR R4 server (HAPI FHIR, Azure FHIR, Google FHIR, etc.)
- `httpx` for async HTTP

```bash
pip install -e ".[dev]"
```

---

## Quick Start

```python
import asyncio
from src.svs.client import FHIRClient, FHIRConfig

async def main():
    config = FHIRConfig(
        base_url="https://fhir.example.org",
        auth_token="your-bearer-token",
    )
    
    async with FHIRClient(config) as client:
        # OP-1: Record screening
        panel = await client.op1_record_screening(
            patient_id="pat-1",
            encounter_id="enc-1",
            practitioner_role_id="pr-1",
            right_eye_snellen=(6, 12),
            left_eye_snellen=(6, 9),
            outcome="refer",
        )
        print(f"Created screening panel: {panel['id']}")

asyncio.run(main())
```

---

## Running Tests

```bash
# All tests
pytest tests/ -v

# Unit tests only
pytest tests/unit/ -v

# With coverage
pytest tests/ --cov=src/svs --cov-report=html
```

### Test Structure

```
tests/
├── unit/
│   ├── test_transitions.py      # State machine validation
│   ├── test_evaluator.py        # Rule evaluation
│   ├── test_builders.py         # Resource construction
│   └── test_operations.py       # Operation integration
└── goldens/                     # Synthetic test fixtures
    ├── screening/
    ├── referral/
    ├── assessment/
    ├── primary_care/
    ├── accommodation/
    └── transitions/             # Forbidden transition fixtures
```

---

## Architecture

```
src/svs/
├── __init__.py           # Public API
├── transitions.py        # State machine validation (6 machines)
├── evaluator.py          # Rule evaluation (acuity, timeout, consent, etc.)
├── builders.py           # Resource construction (all 20 profiles)
├── client.py             # FHIR client with validation + operations
```

### Key Design Principles

1. **Transitions first**: All state changes validated in `transitions.py` before resource modification
2. **Evaluator separate**: Clinical rules in `evaluator.py`, never in transitions
3. **Builders are pure**: No I/O, just resource construction matching IG profiles
4. **Client validates**: Every create/update/patch runs validation + evaluator rules

---

## State Machines

Six state machines enforced:

| Machine | Resource | States | Forbidden Transitions |
|---------|----------|--------|----------------------|
| Referral | ServiceRequest + Task | Draft→Sent→Accepted/Rejected/Cancelled→Completed/Closed* | Cancelled→Active, Sent→Completed direct |
| Screening | Observation (panel) | Registered→Preliminary→Final→Amended/Corrected | Amended before Final |
| Assessment | DiagnosticReport | Registered→Final→Amended/Corrected/Appended | - |
| Consent | Consent | Draft→Proposed→Active→Inactive | Active→Proposed |
| Accommodation | Communication | Preparation→In-progress→Sent/Not-done→Completed→Superseded | Preparation→Completed |
| DocumentReference | DocumentReference | Current→Superseded/Entered-in-error | Superseded→Current |

---

## Rule Evaluation

Key rules evaluated in `evaluator.py`:

- **Visual acuity referral**: ≤6/12 either eye OR ≥2 line difference → `DetectedIssue`
- **Screening attempt**: 2nd absent → missed; 2nd incomplete → referral
- **Referral timeout**: 4 weeks (P4W) → auto-cancel
- **Consent provisions**: No overlaps, no gaps >1 day
- **Document types**: IP-4 allowed types only, source must match
- **Accommodation supersession**: New notice must replace previous

---

## Synthetic Examples

All examples are synthetic. Goldens in `tests/goldens/` are hand-written synthetic fixtures for the operations (not copies of the IG's `fsh-generated/resources/`).

Example: Running OP-1 with goldens
```python
# tests/unit/test_operations.py::TestOP1RecordScreening::test_record_screening_success
# Uses builders to create valid resources, validates against transitions
```

---

## Configuration

```python
from src.svs.client import FHIRConfig

config = FHIRConfig(
    base_url="https://fhir.example.org",      # FHIR server base
    auth_token="Bearer ...",                  # Optional auth
    timeout=30.0,                             # Request timeout
)
```

---

## Traceability

Each operation maps to code:

| Operation | Module | Function | Validation |
|-----------|--------|----------|------------|
| OP-1 | `client.py` | `op1_record_screening` | `transitions.validate_transition("screening", ...)` |
| OP-2a | `client.py` | `op2a_submit_referral` | `transitions.validate_referral_invariants` |
| OP-2b | `client.py` | `op2b_cancel_referral_timeout` | `evaluator.evaluate_referral_timeout` |
| OP-3a | `client.py` | `op3a_return_assessment` | `transitions.validate_transition("assessment", ...)` |
| OP-4 | `client.py` | `op4_send_to_primary_care` | `evaluator.evaluate_document_reference_type` |
| OP-5 | `client.py` | `op5_send_accommodation` | `evaluator.evaluate_accommodation_supersession` |
| OP-6 | `client.py` | `op6_query_patient` | - |
| OP-7 | `client.py` | `op7_subscribe` | - |

---

## Forbidden Transition Tests

Run forbidden transition tests:
```bash
pytest tests/unit/test_transitions.py -v -k "forbidden"
```

Key forbidden transitions tested:
- Cancelled referral → Active (must create new with `replaces`)
- Sent referral → Completed direct (must go through Accepted)
- Preliminary screening → Amended (only after Final)
- Consent provisions overlapping
- DocumentReference Superseded → Current

---

## License

CC0-1.0 - Synthetic data only, no real patient data.

---

## Related

- IG Source: `../05-implementation-guide/`
- Step 4 FHIR Proposal: `../04-fhir-proposal.md`
- BPMN Model: `../02-bpmn-model.md`
- Entities & Data: `../03-entities-data.md`