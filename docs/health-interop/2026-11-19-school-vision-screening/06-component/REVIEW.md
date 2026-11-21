# Process Expert Review: Step 6 - Component Building (School Vision Screening)

**Date:** 2026-11-21  
**Reviewer:** Process Expert (automated)  
**Artefact:** Component in `06-component/`  
**Status:** APPROVED with minor findings

---

## Summary

The component implements all 11 operations from the validated Implementation Guide with:
- 6 state machines (transitions.py) matching the IG lifecycle tables exactly
- Rule evaluator (evaluator.py) for all clinical rules from the IG
- Resource builders (builders.py) for all 20 profiles
- FHIR client with validation (client.py) implementing all 11 operations
- 136 passing unit tests covering transitions, evaluator, builders, and operations

---

## Findings

### C1 (Low): Mock warnings in demographics tests
**Location:** `tests/unit/test_operations.py::TestOP6Demographics`  
**Issue:** RuntimeWarning about coroutine 'AsyncMockMixin._execute_mock_call' never awaited. The search method uses `client.get` but the mock returns AsyncMock instead of MockResponse.  
**Proposed fix:** Update the demographics tests to use MockResponse for the get method.  
**Impact:** Low - tests pass but with warnings.

### C2 (Low): Missing aggregator.py for cohort reports
**Location:** `src/svs/`  
**Issue:** The IG mentions aggregate reporting for public health but no `aggregator.py` module exists.  
**Proposed fix:** Add `aggregator.py` for MeasureReport generation if public health reporting is in scope.  
**Impact:** Low - not in current IG operations.

### C3 (Low): Subscription evaluation could be enhanced
**Location:** `src/svs/evaluator.py`  
**Issue:** OP-7 Subscription creation doesn't validate criteria syntax or channel endpoint reachability.  
**Proposed fix:** Add `evaluate_subscription` checking criteria is valid FHIR search, endpoint is HTTPS, payload is application/fhir+json.  
**Impact:** Low - subscription is infrastructure, not clinical.

---

## Positive Findings

✅ **All 6 state machines match IG lifecycle tables exactly** - Referral (360X), Screening, Assessment, Consent, Accommodation, DocumentReference  
✅ **All 11 operations have builder functions and client methods** - OP-1 through OP-7 + OP-4a-f variants (16 named variants)  
✅ **All forbidden transitions have test coverage** - 64 transition tests pass  
✅ **All clinical rules evaluated in evaluator.py** - acuity thresholds, screening attempts, referral timeout, consent provisions, document types, accommodation supersession  
✅ **All 20 profiles have builder functions** - matching IG profiles exactly  
✅ **136 unit tests pass** - transitions (64), evaluator (30), builders (25), operations (17)  
✅ **Synthetic data only** - no real PHI in code, tests, or goldens  
✅ **Traceability maintained** - each operation maps to code module/function with forbidden transition tests  
✅ **Guards documented** - all 7 guards in traceability table with failing goldens  

---

## Validation Against IG

| IG Operation | Component Module | Validation |
|--------------|------------------|------------|
| OP-1 Record Screening | `client.op1_record_screening` + `builders.build_screening_panel` | ✅ |
| OP-2a Submit Referral | `client.op2a_submit_referral` + `builders.build_service_request_referral` + `build_task_referral_tracking` | ✅ |
| OP-2b Cancel Referral | `client.op2b_cancel_referral_timeout` + `evaluator.evaluate_referral_timeout` | ✅ |
| OP-2c Reject Referral | `client.op2c_reject_referral` | ✅ |
| OP-2d Accept Referral | `client.op2d_accept_referral` | ✅ |
| OP-3a Return Summary | `client.op3a_return_assessment` + `builders.build_diagnostic_report_assessment` | ✅ |
| OP-3b Return Full | `client.op3b_return_assessment_full` + `builders.build_document_reference_ip4` | ✅ |
| OP-4a-f Primary Care | `client.op4_send_to_primary_care` + `builders.build_document_reference_ip4` | ✅ |
| OP-5 Accommodation | `client.op5_send_accommodation` + `builders.build_communication_accommodation` | ✅ |
| OP-6 Demographics | `client.op6_query_patient` | ✅ |
| OP-7 Subscription | `client.op7_subscribe` + `builders.build_subscription` | ✅ |

---

## Approval

**APPROVED** - The component correctly implements the validated Implementation Guide. All critical and high-severity requirements are met. The minor findings (C1-C3) do not block validation and can be addressed in future iterations.

**Reviewer:** Process Expert (automated)  
**Date:** 2026-11-21