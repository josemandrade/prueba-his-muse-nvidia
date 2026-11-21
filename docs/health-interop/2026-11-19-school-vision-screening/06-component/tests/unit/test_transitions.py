"""
Unit tests for transitions.py - State Machine Validation
"""

import pytest
from svs.transitions import (
    validate_transition,
    validate_referral_invariants,
    validate_screening_attempt_consistency,
    validate_consent_provisions,
    validate_document_type_matches_ip4,
    validate_accommodation_supersession_chain,
    ForbiddenTransitionError,
    ValidationError,
    ReferralState,
    ScreeningState,
    AssessmentState,
    ConsentState,
    CommunicationState,
    DocumentState,
)


class TestReferralTransitions:
    """Tests for 360X-aligned referral state machine"""
    
    def test_draft_to_sent_allowed(self):
        assert validate_transition("referral", "draft", "sent") is None
    
    def test_sent_to_accepted_allowed(self):
        assert validate_transition("referral", "sent", "accepted") is None
    
    def test_sent_to_rejected_allowed(self):
        assert validate_transition("referral", "sent", "rejected") is None
    
    def test_sent_to_cancelled_allowed(self):
        assert validate_transition("referral", "sent", "cancelled") is None
    
    def test_sent_to_closed_decline_allowed(self):
        assert validate_transition("referral", "sent", "closed_decline") is None
    
    def test_accepted_to_completed_allowed(self):
        assert validate_transition("referral", "accepted", "completed") is None
    
    def test_accepted_to_closed_dns_allowed(self):
        assert validate_transition("referral", "accepted", "closed_dns") is None
    
    def test_rejected_to_closed_rejected_allowed(self):
        assert validate_transition("referral", "rejected", "closed_rejected") is None
    
    def test_cancelled_to_sent_allowed_new_referral(self):
        assert validate_transition("referral", "cancelled", "sent") is None
    
    def test_completed_to_closed_dns_allowed(self):
        assert validate_transition("referral", "completed", "closed_dns") is None
    
    # Forbidden transitions
    def test_sent_to_completed_forbidden(self):
        with pytest.raises(ForbiddenTransitionError) as exc:
            validate_transition("referral", "sent", "completed")
        assert "completed" in str(exc.value)
    
    def test_cancelled_to_reactivated_forbidden(self):
        with pytest.raises(ForbiddenTransitionError) as exc:
            validate_transition("referral", "cancelled", "accepted")
        assert "cancelled" in str(exc.value).lower()
    
    def test_accepted_to_sent_forbidden(self):
        with pytest.raises(ForbiddenTransitionError) as exc:
            validate_transition("referral", "accepted", "sent")
    
    def test_rejected_to_accepted_forbidden(self):
        with pytest.raises(ForbiddenTransitionError) as exc:
            validate_transition("referral", "rejected", "accepted")
    
    def test_terminal_states_no_transitions(self):
        for state in ["closed_decline", "closed_rejected", "closed_dns"]:
            with pytest.raises(ForbiddenTransitionError):
                validate_transition("referral", state, "sent")


class TestScreeningTransitions:
    """Tests for ScreeningEvent (Observation panel) state machine"""
    
    def test_registered_to_preliminary_allowed(self):
        assert validate_transition("screening", "registered", "preliminary") is None
    
    def test_preliminary_to_final_allowed(self):
        assert validate_transition("screening", "preliminary", "final") is None
    
    def test_preliminary_to_amended_allowed(self):
        assert validate_transition("screening", "preliminary", "amended") is None
    
    def test_final_to_amended_allowed(self):
        assert validate_transition("screening", "final", "amended") is None
    
    def test_final_to_corrected_allowed(self):
        assert validate_transition("screening", "final", "corrected") is None
    
    def test_amended_to_final_allowed(self):
        assert validate_transition("screening", "amended", "final") is None
    
    def test_corrected_to_final_allowed(self):
        assert validate_transition("screening", "corrected", "final") is None
    
    # Forbidden
    def test_preliminary_to_registered_forbidden(self):
        with pytest.raises(ForbiddenTransitionError):
            validate_transition("screening", "preliminary", "registered")
    
    def test_preliminary_to_amended_allowed(self):
        # Per lifecycle table, preliminary -> amended IS allowed (nurse corrects after final)
        validate_transition("screening", "preliminary", "amended")
    
    def test_registered_to_amended_forbidden(self):
        with pytest.raises(ForbiddenTransitionError):
            validate_transition("screening", "registered", "amended")
    
    def test_registered_to_final_forbidden(self):
        with pytest.raises(ForbiddenTransitionError):
            validate_transition("screening", "registered", "final")
    
    def test_terminal_states_no_transitions(self):
        for state in ["cancelled", "entered-in-error", "unknown"]:
            with pytest.raises(ForbiddenTransitionError):
                validate_transition("screening", state, "final")


class TestAssessmentTransitions:
    """Tests for OphthalmologyAssessment (DiagnosticReport) state machine"""
    
    def test_registered_to_final_allowed(self):
        assert validate_transition("assessment", "registered", "final") is None
    
    def test_final_to_amended_allowed(self):
        assert validate_transition("assessment", "final", "amended") is None
    
    def test_final_to_appended_allowed(self):
        assert validate_transition("assessment", "final", "appended") is None
    
    def test_amended_to_final_allowed(self):
        assert validate_transition("assessment", "amended", "final") is None


class TestConsentTransitions:
    """Tests for OptOutConsent state machine"""
    
    def test_draft_to_proposed_allowed(self):
        assert validate_transition("consent", "draft", "proposed") is None
    
    def test_proposed_to_active_allowed(self):
        assert validate_transition("consent", "proposed", "active") is None
    
    def test_proposed_to_rejected_allowed(self):
        assert validate_transition("consent", "proposed", "rejected") is None
    
    def test_active_to_inactive_allowed(self):
        assert validate_transition("consent", "active", "inactive") is None
    
    def test_rejected_to_active_allowed(self):
        assert validate_transition("consent", "rejected", "active") is None
    
    def test_active_to_proposed_forbidden(self):
        with pytest.raises(ForbiddenTransitionError):
            validate_transition("consent", "active", "proposed")


class TestCommunicationTransitions:
    """Tests for AccommodationNotice state machine"""
    
    def test_preparation_to_in_progress_allowed(self):
        assert validate_transition("communication", "preparation", "in-progress") is None
    
    def test_in_progress_to_sent_allowed(self):
        assert validate_transition("communication", "in-progress", "sent") is None
    
    def test_in_progress_to_not_done_allowed(self):
        assert validate_transition("communication", "in-progress", "not-done") is None
    
    def test_sent_to_completed_allowed(self):
        assert validate_transition("communication", "sent", "completed") is None
    
    def test_completed_to_superseded_allowed(self):
        assert validate_transition("communication", "completed", "superseded") is None
    
    def test_preparation_to_completed_forbidden(self):
        with pytest.raises(ForbiddenTransitionError):
            validate_transition("communication", "preparation", "completed")


class TestDocumentTransitions:
    """Tests for DocumentReference state machine"""
    
    def test_current_to_superseded_allowed(self):
        assert validate_transition("document", "current", "superseded") is None
    
    def test_current_to_entered_in_error_allowed(self):
        assert validate_transition("document", "current", "entered-in-error") is None
    
    def test_superseded_terminal(self):
        with pytest.raises(ForbiddenTransitionError):
            validate_transition("document", "superseded", "current")


class TestReferralInvariants:
    """Tests for cross-machine referral invariants"""
    
    def test_accepted_and_cancelled_forbidden(self):
        with pytest.raises(ForbiddenTransitionError):
            validate_referral_invariants("active", "cancelled")
    
    def test_cancelled_reactivate_forbidden(self):
        with pytest.raises(ForbiddenTransitionError):
            validate_referral_invariants("cancelled", "requested")
    
    def test_valid_accepted_received(self):
        # Should not raise
        validate_referral_invariants("active", "received")
    
    def test_valid_completed_from_accepted(self):
        # Should not raise
        validate_referral_invariants("completed", "completed")


class TestScreeningAttemptConsistency:
    """Tests for screening attempt number rules"""
    
    def test_first_attempt_no_previous(self):
        validate_screening_attempt_consistency(1, None, "pass")
    
    def test_second_after_absent_missed(self):
        validate_screening_attempt_consistency(2, "absent", "absent")
    
    def test_second_after_incomplete_referral(self):
        validate_screening_attempt_consistency(2, "incomplete", "refer")
    
    def test_max_two_attempts(self):
        with pytest.raises(ValidationError):
            validate_screening_attempt_consistency(3, "absent", "absent")


class TestConsentProvisions:
    """Tests for consent provision overlap validation"""
    
    def test_non_overlapping_provisions_valid(self):
        provisions = [
            {"type": "deny", "period": {"start": "2026-09-01", "end": "2026-11-10"}},
            {"type": "permit", "period": {"start": "2026-11-10", "end": "2026-06-30"}},
        ]
        validate_consent_provisions(provisions)
    
    def test_overlapping_provisions_invalid(self):
        provisions = [
            {"type": "deny", "period": {"start": "2026-09-01", "end": "2026-11-15"}},
            {"type": "permit", "period": {"start": "2026-11-10", "end": "2027-06-30"}},
        ]
        with pytest.raises(ValidationError) as exc:
            validate_consent_provisions(provisions)
        assert "overlap" in str(exc.value)
    
    def test_gap_in_provisions_warning(self):
        # Gap is allowed but warned - no exception
        provisions = [
            {"type": "deny", "period": {"start": "2026-09-01", "end": "2026-11-01"}},
            {"type": "permit", "period": {"start": "2026-11-10", "end": "2026-06-30"}},
        ]
        validate_consent_provisions(provisions)  # Should not raise


class TestDocumentTypeValidation:
    """Tests for IP-4 document type validation"""
    
    def test_school_document_types_valid(self):
        for doc_type in ["screening-pass", "screening-decline", "screening-missed", 
                         "end-of-year-missed", "referral-dna", "referral-rejected"]:
            validate_document_type_matches_ip4(doc_type, "school")
    
    def test_ophthalmology_document_type_valid(self):
        validate_document_type_matches_ip4("assessment-full", "ophthalmology")
    
    def test_school_type_from_ophthalmology_invalid(self):
        with pytest.raises(ValidationError):
            validate_document_type_matches_ip4("assessment-full", "school")
    
    def test_ophthalmology_type_from_school_invalid(self):
        with pytest.raises(ValidationError):
            validate_document_type_matches_ip4("screening-pass", "ophthalmology")
    
    def test_invalid_document_type(self):
        with pytest.raises(ValidationError):
            validate_document_type_matches_ip4("invalid-type", "school")


class TestAccommodationSupersession:
    """Tests for accommodation notice supersession chain"""
    
    def test_valid_supersession(self):
        new_notice = {
            "id": "comm-2",
            "relatesTo": [{"code": "replaces", "target": {"reference": "Communication/comm-1"}}],
        }
        existing = [{"id": "comm-1", "status": "sent"}]
        validate_accommodation_supersession_chain(new_notice, existing)
    
    def test_replaces_missing_target_invalid(self):
        new_notice = {
            "id": "comm-2",
            "relatesTo": [{"code": "replaces", "target": {"reference": "Communication/missing"}}],
        }
        existing = [{"id": "comm-1", "status": "sent"}]
        with pytest.raises(ValidationError) as exc:
            validate_accommodation_supersession_chain(new_notice, existing)
        assert "does not exist" in str(exc.value)
    
    def test_no_replaces_allowed(self):
        # First notice has no replaces
        new_notice = {"id": "comm-1", "relatesTo": []}
        validate_accommodation_supersession_chain(new_notice, [])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])