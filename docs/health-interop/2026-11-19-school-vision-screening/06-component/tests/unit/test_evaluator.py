"""
Unit tests for evaluator.py - Rule Evaluation
"""

import pytest
from svs.evaluator import (
    evaluate_visual_acuity_referral,
    evaluate_screening_outcome,
    evaluate_screening_attempt,
    evaluate_referral_timeout,
    evaluate_consent_provisions,
    evaluate_document_reference_type,
    evaluate_accommodation_supersession,
    evaluate_all_rules,
    DetectedIssue,
    EvaluationResult,
)


class TestVisualAcuityReferral:
    """Tests for visual acuity threshold evaluation"""
    
    def test_both_eyes_pass_6_9(self):
        issues = evaluate_visual_acuity_referral("6/9", "6/9")
        assert len(issues) == 0
    
    def test_right_eye_refer_6_12(self):
        issues = evaluate_visual_acuity_referral("6/12", "6/9")
        assert len(issues) == 1
        assert issues[0].code == "acuity-low-od"
        assert issues[0].severity == "high"
    
    def test_left_eye_refer_6_12(self):
        issues = evaluate_visual_acuity_referral("6/9", "6/12")
        assert len(issues) == 1
        assert issues[0].code == "acuity-low-os"
    
    def test_both_eyes_refer(self):
        issues = evaluate_visual_acuity_referral("6/18", "6/18")
        assert len(issues) == 2
        codes = {i.code for i in issues}
        assert "acuity-low-od" in codes
        assert "acuity-low-os" in codes
    
    def test_two_line_difference(self):
        # 6/6 vs 6/12 = 2 line difference, and 6/12 triggers acuity-low-os
        issues = evaluate_visual_acuity_referral("6/6", "6/12")
        assert len(issues) == 2
        codes = {i.code for i in issues}
        assert "acuity-low-os" in codes
        assert "acuity-difference" in codes
    
    def test_invalid_snellen_format(self):
        issues = evaluate_visual_acuity_referral("invalid", "6/9")
        assert len(issues) == 1
        assert issues[0].code == "invalid-acuity"


class TestScreeningOutcome:
    """Tests for screening outcome determination"""
    
    def test_pass_outcome(self):
        outcome, issues = evaluate_screening_outcome("6/9", "6/9")
        assert outcome == "pass"
        assert len(issues) == 0
    
    def test_refer_outcome(self):
        outcome, issues = evaluate_screening_outcome("6/12", "6/9")
        assert outcome == "refer"
        assert len(issues) == 1


class TestScreeningAttempt:
    """Tests for screening attempt rules"""
    
    def test_first_attempt_no_previous(self):
        issues = evaluate_screening_attempt(1, None, "pass")
        assert len(issues) == 0
    
    def test_second_absent_after_absent_missed(self):
        issues = evaluate_screening_attempt(2, "absent", "absent")
        assert len(issues) == 1
        assert issues[0].code == "screening-missed"
    
    def test_second_incomplete_then_pass(self):
        issues = evaluate_screening_attempt(2, "incomplete", "pass")
        assert len(issues) == 0
    
    def test_second_incomplete_then_incomplete_refers(self):
        issues = evaluate_screening_attempt(2, "incomplete", "incomplete")
        assert len(issues) == 1
        assert issues[0].code == "incomplete-referral"
    
    def test_max_attempts_exceeded(self):
        issues = evaluate_screening_attempt(3, "absent", "absent")
        assert len(issues) == 1
        assert issues[0].code == "max-attempts-exceeded"


class TestReferralTimeout:
    """Tests for referral timeout evaluation"""
    
    def test_timeout_triggered(self):
        from datetime import datetime, timedelta, timezone
        authored = datetime(2026, 11, 1, tzinfo=timezone.utc).isoformat()
        now = datetime(2026, 12, 1, tzinfo=timezone.utc).isoformat()
        
        issues = evaluate_referral_timeout(authored, now, "requested")
        assert len(issues) == 1
        assert issues[0].code == "referral-timeout"
    
    def test_not_timed_out(self):
        from datetime import datetime, timedelta, timezone
        authored = datetime(2026, 11, 15, tzinfo=timezone.utc).isoformat()
        now = datetime(2026, 11, 20, tzinfo=timezone.utc).isoformat()
        
        issues = evaluate_referral_timeout(authored, now, "requested")
        assert len(issues) == 0
    
    def test_terminal_status_no_timeout(self):
        from datetime import datetime, timezone
        authored = datetime(2026, 11, 1, tzinfo=timezone.utc).isoformat()
        now = datetime(2026, 12, 1, tzinfo=timezone.utc).isoformat()
        
        issues = evaluate_referral_timeout(authored, now, "completed")
        assert len(issues) == 0


class TestConsentProvisions:
    """Tests for consent provision evaluation"""
    
    def test_valid_non_overlapping(self):
        provisions = [
            {"type": "deny", "period": {"start": "2026-09-01", "end": "2026-11-10"}},
            {"type": "permit", "period": {"start": "2026-11-10", "end": "2026-06-30"}},
        ]
        issues = evaluate_consent_provisions(provisions)
        assert len(issues) == 0
    
    def test_overlapping_provisions(self):
        provisions = [
            {"type": "deny", "period": {"start": "2026-09-01", "end": "2026-11-15"}},
            {"type": "permit", "period": {"start": "2026-11-10", "end": "2026-06-30"}},
        ]
        issues = evaluate_consent_provisions(provisions)
        assert len(issues) == 1
        assert issues[0].code == "overlapping-provisions"
    
    def test_gap_in_provisions(self):
        provisions = [
            {"type": "deny", "period": {"start": "2026-09-01", "end": "2026-11-01"}},
            {"type": "permit", "period": {"start": "2026-11-10", "end": "2026-06-30"}},
        ]
        issues = evaluate_consent_provisions(provisions)
        # Gap produces moderate issue
        gap_issues = [i for i in issues if i.code == "gap-in-provisions"]
        assert len(gap_issues) == 1
        assert gap_issues[0].severity == "moderate"


class TestDocumentReferenceType:
    """Tests for IP-4 document type validation"""
    
    def test_school_types_valid(self):
        for doc_type in ["screening-pass", "screening-decline", "screening-missed"]:
            issues = evaluate_document_reference_type(doc_type, "school")
            assert len(issues) == 0
    
    def test_ophthalmology_type_valid(self):
        issues = evaluate_document_reference_type("assessment-full", "ophthalmology")
        assert len(issues) == 0
    
    def test_source_mismatch(self):
        issues = evaluate_document_reference_type("assessment-full", "school")
        assert len(issues) == 1
        assert issues[0].code == "document-source-mismatch"
    
    def test_invalid_type(self):
        issues = evaluate_document_reference_type("invalid", "school")
        assert len(issues) == 1
        assert issues[0].code == "invalid-document-type"


class TestAccommodationSupersession:
    """Tests for accommodation supersession evaluation"""
    
    def test_valid_supersession(self):
        new_notice = {
            "id": "comm-2",
            "relatesTo": [{"code": "replaces", "target": {"reference": "Communication/comm-1"}}],
        }
        existing = [{"id": "comm-1", "status": "sent"}]
        issues = evaluate_accommodation_supersession(new_notice, existing)
        assert len(issues) == 0
    
    def test_replaces_missing_target(self):
        new_notice = {
            "id": "comm-2",
            "relatesTo": [{"code": "replaces", "target": {"reference": "Communication/missing"}}],
        }
        existing = [{"id": "comm-1", "status": "sent"}]
        issues = evaluate_accommodation_supersession(new_notice, existing)
        assert len(issues) == 1
        assert issues[0].code == "replaces-missing-target"
    
    def test_first_notice_no_replaces(self):
        new_notice = {"id": "comm-1", "relatesTo": []}
        issues = evaluate_accommodation_supersession(new_notice, [])
        assert len(issues) == 0


class TestEvaluateAllRules:
    """Tests for main evaluator entry point"""
    
    def test_service_request_referral_timeout(self):
        resource = {
            "resourceType": "ServiceRequest",
            "code": {"coding": [{"code": "307924000"}]},
            "authoredOn": "2026-11-01T00:00:00Z",
        }
        context = {"now": "2026-12-01T00:00:00Z", "task_status": "requested"}
        issues = evaluate_all_rules("ServiceRequest", resource, context)
        assert any(i.code == "referral-timeout" for i in issues)
    
    def test_consent_provisions(self):
        resource = {
            "resourceType": "Consent",
            "provision": [
                {"type": "deny", "period": {"start": "2026-09-01", "end": "2026-11-15"}},
                {"type": "permit", "period": {"start": "2026-11-10", "end": "2026-06-30"}},
            ],
        }
        issues = evaluate_all_rules("Consent", resource, {})
        assert any(i.code == "overlapping-provisions" for i in issues)
    
    def test_document_reference_type(self):
        resource = {
            "resourceType": "DocumentReference",
            "type": {"coding": [{"code": "assessment-full"}]},
            "author": [{"reference": "Organization/ophthalmology"}],
        }
        issues = evaluate_all_rules("DocumentReference", resource, {})
        assert len(issues) == 0
    
    def test_document_reference_wrong_source(self):
        resource = {
            "resourceType": "DocumentReference",
            "type": {"coding": [{"code": "assessment-full"}]},
            "author": [{"reference": "Organization/school"}],
        }
        issues = evaluate_all_rules("DocumentReference", resource, {})
        assert any(i.code == "document-source-mismatch" for i in issues)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])