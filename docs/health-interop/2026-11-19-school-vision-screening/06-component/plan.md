# Component Build Plan: School Vision Screening

**Guide Canonical:** https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening
**Operations:** 11 operations (OP-1 through OP-7 + OP-4a-f variants, 16 named variants)
**State Machines:** 6 (Referral, ScreeningEvent, Assessment, OptOutConsent, AccommodationNotice, DocumentReference)

---

## Plan Tasks (one operation/subscription per task)

| Task | Operation | Description | Module | Profile(s) | Goldens |
|------|-----------|-------------|--------|------------|---------|
| 1 | OP-1 | Record Screening (POST Observation panel) | `src/svs/screening.py` | SVSObservationScreeningPanel, SVSObservationRightEyeAcuity, SVSObservationLeftEyeAcuity | given, invalid-ratio, missing-member |
| 2 | OP-2a | Submit Referral (POST ServiceRequest + Task) | `src/svs/referral.py` | SVSServiceRequestReferral, SVSTaskReferralTracking | given, duplicate-referral, missing-fields |
| 3 | OP-2b | Cancel Referral Timeout (PATCH) | `src/svs/referral.py` | SVSServiceRequestReferral, SVSTaskReferralTracking | timeout-cancel |
| 4 | OP-2c | Reject Referral (PATCH) | `src/svs/referral.py` | SVSServiceRequestReferral, SVSTaskReferralTracking | rejected-duplicate |
| 5 | OP-2d | Accept Referral (PATCH) | `src/svs/referral.py` | SVSServiceRequestReferral, SVSTaskReferralTracking | accepted |
| 6 | OP-3a | Return Assessment Summary (GET DiagnosticReport / POST DocumentReference) | `src/svs/assessment.py` | SVSDiagnosticReportAssessment, SVSObservationDiagnosis, SVSObservationRefractionOD, SVSObservationRefractionOS, SVSCarePlanFollowUp | given-pull, given-push |
| 7 | OP-3b | Return Assessment Full (POST DocumentReference) | `src/svs/assessment.py` | SVSDocumentReferenceIP4 (assessment-full) | given |
| 8 | OP-4a-f | Send to Primary Care (6 document types) (POST DocumentReference) | `src/svs/primary_care.py` | SVSDocumentReferenceIP4, SVSListPrimaryCareDocuments | screening-pass, screening-decline, referral-dna, screening-missed, referral-rejected, end-of-year-missed |
| 9 | OP-5 | Send Accommodation Notice (POST Communication) | `src/svs/accommodation.py` | SVSCommunicationAccommodation | given |
| 10 | OP-6 | Query Patient Demographics (GET Patient) | `src/svs/demographics.py` | SVSPatient, SVSRelatedPerson | by-id, by-demographics |
| 11 | OP-7 | Subscribe to Assessment Documents (POST Subscription) | `src/svs/subscription.py` | Subscription | given |
| 12 | Core | State machines (transitions.py) | `src/svs/transitions.py` | All lifecycle resources | All forbidden-transition tests |
| 13 | Core | Rule evaluator (evaluator.py) | `src/svs/evaluator.py` | — | Threshold rules |
| 14 | Core | Resource builders (builders.py) | `src/svs/builders.py` | All profiles | All synthetic examples |
| 15 | Core | FHIR client/server (client.py) | `src/svs/client.py` | — | — |
| 16 | Test | Run all goldens | `tests/` | — | — |
| 17 | Doc | README with run instructions | `README.md` | — | — |

---

## Traceability Table (from guide to code)

| Operation | Module | Function | Forbidden Transition Test |
|-----------|--------|----------|---------------------------|
| OP-1 | screening.py | create_screening_panel | test_screening_amended_before_final_fails |
| OP-2a | referral.py | submit_referral | test_duplicate_referral_fails |
| OP-2b | referral.py | cancel_referral | test_cancelled_cannot_reactivate |
| OP-2c | referral.py | reject_referral | test_rejected_cannot_accept |
| OP-2d | referral.py | accept_referral | test_sent_cannot_complete_directly |
| OP-3a | assessment.py | return_assessment | test_assessment_references_referral |
| OP-3b | assessment.py | return_assessment_full | test_documentreference_created |
| OP-4* | primary_care.py | send_to_primary_care | test_document_types_valid |
| OP-5 | accommodation.py | send_accommodation | test_supersession_chain |
| OP-6 | demographics.py | query_patient | test_matching_strategy |
| OP-7 | subscription.py | subscribe | test_notification_delivered |

---

## Guards Table

| Guard | Module | Function | Failing Golden |
|-------|--------|----------|----------------|
| Screening must have 2 members (OD/OS) | transitions.py | validate_screening | missing-member |
| Screening cannot be amended before final | transitions.py | validate_transition | amended-before-final |
| Referral cannot skip Accepted → Completed | transitions.py | validate_transition | sent-to-completed-direct |
| Cancelled referral cannot reactivate | transitions.py | validate_transition | cancelled-reactivate |
| Consent provisions must not overlap | transitions.py | validate_consent | overlapping-provisions |
| DocumentReference type must match IP-4 | transitions.py | validate_document | invalid-document-type |
| Accommodation supersession chain | transitions.py | validate_supersession | broken-chain |

---

## Goldens Directory Structure

```
tests/goldens/
├── screening/
│   ├── given_valid_panel.json
│   ├── given_invalid_ratio.json
│   └── given_missing_member.json
├── referral/
│   ├── given_submit_valid.json
│   ├── given_duplicate_referral.json
│   ├── given_missing_fields.json
│   ├── given_timeout_cancel.json
│   ├── given_reject_duplicate.json
│   └── given_accept_valid.json
├── assessment/
│   ├── given_return_summary_pull.json
│   ├── given_return_summary_push.json
│   └── given_return_full.json
├── primary_care/
│   ├── given_screening_pass.json
│   ├── given_screening_decline.json
│   ├── given_referral_dna.json
│   ├── given_screening_missed.json
│   ├── given_referral_rejected.json
│   └── given_end_of_year_missed.json
├── accommodation/
│   └── given_valid.json
├── demographics/
│   ├── given_by_id.json
│   └── given_by_demographics.json
├── subscription/
│   └── given_valid.json
└── transitions/
    ├── given_cancelled_reactivate.json (must fail)
    ├── given_sent_to_completed.json (must fail)
    ├── given_amended_before_final.json (must fail)
    ├── given_overlapping_provisions.json (must fail)
    └── given_invalid_document_type.json (must fail)
```

---

## Task Order (RED-GREEN)

Each task follows: write failing test → implement code → test passes → record completion.

1. Task 12: transitions.py (state machines first - blocks other tasks)
2. Task 13: evaluator.py (rule evaluation)
3. Task 14: builders.py (resource construction)
4. Task 15: client.py (FHIR operations)
5. Task 1: OP-1 screening
6. Task 2-5: OP-2a-d referral
7. Task 6-7: OP-3a-b assessment
8. Task 8: OP-4a-f primary care
9. Task 9: OP-5 accommodation
10. Task 10: OP-6 demographics
11. Task 11: OP-7 subscription
12. Task 16: tests pass
13. Task 17: README