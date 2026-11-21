"""
School Vision Screening Component

A FHIR-based implementation of the School Vision Screening interoperability guide.
"""

from .transitions import (
    validate_transition,
    validate_resource_transition,
    ForbiddenTransitionError,
    ValidationError,
    ReferralState,
    ScreeningState,
    AssessmentState,
    ConsentState,
    CommunicationState,
    DocumentState,
    validate_referral_invariants,
    validate_screening_attempt_consistency,
    validate_consent_provisions,
    validate_document_type_matches_ip4,
    validate_accommodation_supersession_chain,
)

from .evaluator import (
    evaluate_all_rules,
    evaluate_visual_acuity_referral,
    evaluate_screening_outcome,
    evaluate_screening_attempt,
    evaluate_referral_timeout,
    evaluate_consent_provisions,
    evaluate_document_reference_type,
    evaluate_accommodation_supersession,
    DetectedIssue,
    EvaluationResult,
)

from .builders import (
    build_patient,
    build_related_person,
    build_practitioner,
    build_practitioner_role,
    build_organization,
    build_encounter,
    build_right_eye_acuity,
    build_left_eye_acuity,
    build_screening_panel,
    build_service_request_referral,
    build_task_referral_tracking,
    build_diagnostic_report_assessment,
    build_observation_diagnosis,
    build_observation_refraction,
    build_care_plan_followup,
    build_communication_accommodation,
    build_consent_optout,
    build_document_reference_ip4,
    build_list_primary_care,
    build_subscription,
    CANONICAL_BASE,
    PROFILES,
)

from .client import FHIRClient, FHIRConfig

__version__ = "0.1.0"
__all__ = [
    # Transitions
    "validate_transition",
    "validate_resource_transition",
    "ForbiddenTransitionError",
    "ValidationError",
    "ReferralState",
    "ScreeningState",
    "AssessmentState",
    "ConsentState",
    "CommunicationState",
    "DocumentState",
    "validate_referral_invariants",
    "validate_screening_attempt_consistency",
    "validate_consent_provisions",
    "validate_document_type_matches_ip4",
    "validate_accommodation_supersession_chain",
    # Evaluator
    "evaluate_all_rules",
    "evaluate_visual_acuity_referral",
    "evaluate_screening_outcome",
    "evaluate_screening_attempt",
    "evaluate_referral_timeout",
    "evaluate_consent_provisions",
    "evaluate_document_reference_type",
    "evaluate_accommodation_supersession",
    "DetectedIssue",
    "EvaluationResult",
    # Builders
    "build_patient",
    "build_related_person",
    "build_practitioner",
    "build_practitioner_role",
    "build_organization",
    "build_encounter",
    "build_right_eye_acuity",
    "build_left_eye_acuity",
    "build_screening_panel",
    "build_service_request_referral",
    "build_task_referral_tracking",
    "build_diagnostic_report_assessment",
    "build_observation_diagnosis",
    "build_observation_refraction",
    "build_care_plan_followup",
    "build_communication_accommodation",
    "build_consent_optout",
    "build_document_reference_ip4",
    "build_list_primary_care",
    "build_subscription",
    "CANONICAL_BASE",
    "PROFILES",
    # Client
    "FHIRClient",
    "FHIRConfig",
]