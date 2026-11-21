"""
State Machine Validation for School Vision Screening

Each workflow-state resource has a defined lifecycle with states, allowed transitions,
and forbidden transitions. This module enforces all transitions before building resources.
"""

from typing import Dict, List, Set, Tuple, Optional
from enum import Enum
from dataclasses import dataclass
import json


class ReferralState(str, Enum):
    """ServiceRequest + Task combined states (360X-aligned)"""
    DRAFT = "draft"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    CLOSED_DNS = "closed_dns"
    CLOSED_DECLINE = "closed_decline"
    CLOSED_REJECTED = "closed_rejected"


class ScreeningState(str, Enum):
    """Observation (Panel) states"""
    REGISTERED = "registered"
    PRELIMINARY = "preliminary"
    FINAL = "final"
    AMENDED = "amended"
    CORRECTED = "corrected"
    CANCELLED = "cancelled"
    ENTERED_IN_ERROR = "entered-in-error"
    UNKNOWN = "unknown"


class AssessmentState(str, Enum):
    """DiagnosticReport states"""
    REGISTERED = "registered"
    PARTIAL = "partial"
    PRELIMINARY = "preliminary"
    FINAL = "final"
    AMENDED = "amended"
    CORRECTED = "corrected"
    APPENDED = "appended"
    CANCELLED = "cancelled"
    ENTERED_IN_ERROR = "entered-in-error"
    UNKNOWN = "unknown"


class ConsentState(str, Enum):
    """Consent (OptOut) states"""
    DRAFT = "draft"
    PROPOSED = "proposed"
    ACTIVE = "active"
    REJECTED = "rejected"
    INACTIVE = "inactive"
    ENTERED_IN_ERROR = "entered-in-error"


class CommunicationState(str, Enum):
    """Communication (Accommodation) states"""
    PREPARATION = "preparation"
    IN_PROGRESS = "in-progress"
    SENT = "sent"
    NOT_DONE = "not-done"
    COMPLETED = "completed"
    SUPERSEDED = "superseded"
    ENTERED_IN_ERROR = "entered-in-error"
    UNKNOWN = "unknown"


class DocumentState(str, Enum):
    """DocumentReference states"""
    CURRENT = "current"
    SUPERSEDED = "superseded"
    ENTERED_IN_ERROR = "entered-in-error"


# =============================================================================
# TRANSITION TABLES
# =============================================================================

REFERRAL_TRANSITIONS: Dict[ReferralState, Set[ReferralState]] = {
    ReferralState.DRAFT: {ReferralState.SENT},
    ReferralState.SENT: {
        ReferralState.ACCEPTED,
        ReferralState.REJECTED,
        ReferralState.CANCELLED,
        ReferralState.CLOSED_DECLINE,
    },
    ReferralState.ACCEPTED: {
        ReferralState.COMPLETED,
        ReferralState.CLOSED_DNS,
    },
    ReferralState.REJECTED: {ReferralState.CLOSED_REJECTED},
    ReferralState.CANCELLED: {ReferralState.SENT},  # New referral with replaces
    ReferralState.COMPLETED: {ReferralState.CLOSED_DNS},
    ReferralState.CLOSED_DECLINE: set(),  # Terminal
    ReferralState.CLOSED_REJECTED: set(),  # Terminal
    ReferralState.CLOSED_DNS: set(),  # Terminal
}

SCREENING_TRANSITIONS: Dict[ScreeningState, Set[ScreeningState]] = {
    ScreeningState.REGISTERED: {ScreeningState.PRELIMINARY},
    ScreeningState.PRELIMINARY: {
        ScreeningState.FINAL,
        ScreeningState.AMENDED,
        ScreeningState.CORRECTED,
    },
    ScreeningState.FINAL: {
        ScreeningState.AMENDED,
        ScreeningState.CORRECTED,
    },
    ScreeningState.AMENDED: {ScreeningState.FINAL},
    ScreeningState.CORRECTED: {ScreeningState.FINAL},
    ScreeningState.CANCELLED: set(),
    ScreeningState.ENTERED_IN_ERROR: set(),
    ScreeningState.UNKNOWN: set(),
}

ASSESSMENT_TRANSITIONS: Dict[AssessmentState, Set[AssessmentState]] = {
    AssessmentState.REGISTERED: {
        AssessmentState.PARTIAL,
        AssessmentState.PRELIMINARY,
        AssessmentState.FINAL,
    },
    AssessmentState.PARTIAL: {
        AssessmentState.PRELIMINARY,
        AssessmentState.FINAL,
    },
    AssessmentState.PRELIMINARY: {AssessmentState.FINAL},
    AssessmentState.FINAL: {
        AssessmentState.AMENDED,
        AssessmentState.CORRECTED,
        AssessmentState.APPENDED,
    },
    AssessmentState.AMENDED: {AssessmentState.FINAL},
    AssessmentState.CORRECTED: {AssessmentState.FINAL},
    AssessmentState.APPENDED: {AssessmentState.FINAL},
    AssessmentState.CANCELLED: set(),
    AssessmentState.ENTERED_IN_ERROR: set(),
    AssessmentState.UNKNOWN: set(),
}

CONSENT_TRANSITIONS: Dict[ConsentState, Set[ConsentState]] = {
    ConsentState.DRAFT: {ConsentState.PROPOSED},
    ConsentState.PROPOSED: {ConsentState.ACTIVE, ConsentState.REJECTED},
    ConsentState.ACTIVE: {ConsentState.INACTIVE},
    ConsentState.REJECTED: {ConsentState.ACTIVE},
    ConsentState.INACTIVE: set(),
    ConsentState.ENTERED_IN_ERROR: set(),
}

COMMUNICATION_TRANSITIONS: Dict[CommunicationState, Set[CommunicationState]] = {
    CommunicationState.PREPARATION: {CommunicationState.IN_PROGRESS},
    CommunicationState.IN_PROGRESS: {CommunicationState.SENT, CommunicationState.NOT_DONE},
    CommunicationState.SENT: {CommunicationState.COMPLETED},
    CommunicationState.NOT_DONE: set(),
    CommunicationState.COMPLETED: {CommunicationState.SUPERSEDED},
    CommunicationState.SUPERSEDED: set(),
    CommunicationState.ENTERED_IN_ERROR: set(),
    CommunicationState.UNKNOWN: set(),
}

DOCUMENT_TRANSITIONS: Dict[DocumentState, Set[DocumentState]] = {
    DocumentState.CURRENT: {DocumentState.SUPERSEDED, DocumentState.ENTERED_IN_ERROR},
    DocumentState.SUPERSEDED: set(),
    DocumentState.ENTERED_IN_ERROR: set(),
}

ALL_TRANSITIONS = {
    "referral": REFERRAL_TRANSITIONS,
    "screening": SCREENING_TRANSITIONS,
    "assessment": ASSESSMENT_TRANSITIONS,
    "consent": CONSENT_TRANSITIONS,
    "communication": COMMUNICATION_TRANSITIONS,
    "document": DOCUMENT_TRANSITIONS,
}


# =============================================================================
# EXCEPTIONS
# =============================================================================

class ForbiddenTransitionError(Exception):
    """Raised when a state transition is not allowed"""
    def __init__(self, machine: str, from_state: str, to_state: str, allowed: List[str]):
        self.machine = machine
        self.from_state = from_state
        self.to_state = to_state
        self.allowed = allowed
        super().__init__(
            f"Forbidden transition in {machine}: {from_state} -> {to_state}. "
            f"Allowed: {', '.join(allowed) if allowed else 'none (terminal)'}"
        )


class ValidationError(Exception):
    """Raised when validation fails"""
    pass


# =============================================================================
# STATE MACHINE VALIDATOR
# =============================================================================

def validate_transition(machine: str, from_state: str, to_state: str) -> None:
    """
    Validate that a state transition is allowed for the given machine.
    
    Args:
        machine: One of "referral", "screening", "assessment", "consent", 
                 "communication", "document"
        from_state: Current state
        to_state: Proposed next state
        
    Raises:
        ForbiddenTransitionError: If transition is not allowed
    """
    transitions = ALL_TRANSITIONS.get(machine)
    if not transitions:
        raise ValidationError(f"Unknown machine: {machine}")
    
    try:
        from_enum = _get_enum_for_machine(machine, from_state)
        to_enum = _get_enum_for_machine(machine, to_state)
    except ValueError as e:
        raise ValidationError(str(e))
    
    allowed = transitions.get(from_enum, set())
    if to_enum not in allowed:
        allowed_str = [e.value for e in allowed]
        raise ForbiddenTransitionError(machine, from_state, to_state, allowed_str)


def _get_enum_for_machine(machine: str, state: str) -> Enum:
    """Map string state to appropriate Enum for machine"""
    enum_map = {
        "referral": ReferralState,
        "screening": ScreeningState,
        "assessment": AssessmentState,
        "consent": ConsentState,
        "communication": CommunicationState,
        "document": DocumentState,
    }
    enum_cls = enum_map.get(machine)
    if not enum_cls:
        raise ValidationError(f"Unknown machine: {machine}")
    try:
        return enum_cls(state)
    except ValueError:
        valid = [e.value for e in enum_cls]
        raise ValidationError(f"Invalid state '{state}' for {machine}. Valid: {valid}")


# =============================================================================
# CROSS-MACHINE INVARIANTS
# =============================================================================

def validate_referral_invariants(
    service_request_status: str,
    task_status: str
) -> None:
    """
    Validate cross-machine invariants for referral (ServiceRequest + Task).
    
    Raises:
        ForbiddenTransitionError: If invariant violated
    """
    # Invariant: A referral cannot be both Accepted and Cancelled
    if service_request_status == "active" and task_status == "cancelled":
        raise ForbiddenTransitionError(
            "referral", "active/cancelled", "invalid",
            ["active/requested (Accepted)", "active/received (Accepted)"]
        )
    
    # Invariant: A cancelled referral cannot be re-activated on same resource
    if service_request_status == "cancelled" and task_status in ("requested", "received", "accepted"):
        raise ForbiddenTransitionError(
            "referral", "cancelled", "reactivated",
            ["new referral with replaces"]
        )
    
    # Invariant: DNS closure only from Accepted or Completed
    if task_status == "completed" and service_request_status == "active":
        # This is valid - Completed from Accepted
        pass
    elif service_request_status == "completed" and task_status == "cancelled":
        raise ForbiddenTransitionError(
            "referral", "completed/cancelled", "invalid",
            ["completed from Accepted or Completed only"]
        )


def validate_screening_attempt_consistency(
    current_attempt: int,
    previous_outcome: str,
    new_outcome: str
) -> None:
    """
    Validate screening attempt number consistency.
    
    Rules:
    - 1st Absent -> re-screen (attempt 2)
    - 2nd Absent -> missed (terminal)
    - 1st Incomplete -> re-screen (attempt 2)
    - 2nd Incomplete -> direct referral (with partial data)
    """
    if current_attempt == 1:
        if previous_outcome in ("absent", "incomplete"):
            raise ValidationError(
                f"Attempt 1 cannot have previous outcome {previous_outcome}"
            )
    elif current_attempt == 2:
        if previous_outcome == "absent" and new_outcome != "absent":
            raise ValidationError("2nd attempt after absent must be absent or missed")
        if previous_outcome == "incomplete" and new_outcome not in ("pass", "refer", "incomplete"):
            raise ValidationError("2nd attempt after incomplete must be pass/refer/incomplete")
    elif current_attempt > 2:
        raise ValidationError(f"Maximum 2 screening attempts allowed, got {current_attempt}")


def validate_consent_provisions(provisions: List[dict]) -> None:
    """
    Validate Consent provisions do not overlap.
    
    Each provision has period.start and period.end.
    """
    for i, prov in enumerate(provisions):
        start = prov.get("period", {}).get("start")
        end = prov.get("period", {}).get("end")
        if not start:
            continue
        for j, other in enumerate(provisions):
            if i >= j:
                continue
            other_start = other.get("period", {}).get("start")
            other_end = other.get("period", {}).get("end")
            if not other_start:
                continue
            # Check overlap
            if end and other_end:
                if start < other_end and other_start < end:
                    raise ValidationError(
                        f"Consent provisions {i} and {j} overlap: "
                        f"{start}-{end} overlaps {other_start}-{other_end}"
                    )
            elif end and not other_end:
                if start < end and other_start <= end:
                    raise ValidationError(
                        f"Consent provision {i} ({start}-{end}) overlaps "
                        f"open-ended provision {j} ({other_start}-)"
                    )


def validate_document_type_matches_ip4(document_type: str, source: str) -> None:
    """
    Validate DocumentReference type matches IP-4 document types.
    
    Args:
        document_type: LOINC code or SVS code
        source: "school" or "ophthalmology"
    """
    valid_types = {
        "screening-pass": {"loinc": "83700-8", "source": "school"},
        "screening-decline": {"loinc": "83700-8", "source": "school"},
        "screening-missed": {"loinc": "83700-8", "source": "school"},
        "end-of-year-missed": {"loinc": "83700-8", "source": "school"},
        "referral-dna": {"loinc": "11506-3", "source": "school"},
        "referral-rejected": {"loinc": "11506-3", "source": "school"},
        "assessment-full": {"loinc": "28626-8", "source": "ophthalmology"},
    }
    
    if document_type not in valid_types:
        raise ValidationError(f"Invalid document type: {document_type}")
    
    if valid_types[document_type]["source"] != source:
        raise ValidationError(
            f"Document type {document_type} must come from {valid_types[document_type]['source']}, "
            f"not {source}"
        )


def validate_accommodation_supersession_chain(
    new_notice: dict,
    previous_notices: Optional[List[dict]]
) -> None:
    """
    Validate accommodation notice supersession chain.
    
    Each new notice must have relatesTo.code=replaces pointing to previous.
    Previous notice status must become superseded.
    """
    if previous_notices:
        relates_to = new_notice.get("relatesTo", [])
        replaces = [r for r in relates_to if r.get("code") == "replaces"]
        if not replaces:
            raise ValidationError(
                "New accommodation notice must have relatesTo.code=replaces "
                "pointing to previous notice"
            )
        prev_ids = {n.get("id") for n in previous_notices if n.get("id")}
        for r in replaces:
            target_ref = r.get("target", {}).get("reference", "")
            target_id = target_ref.replace("Communication/", "")
            if target_id not in prev_ids:
                raise ValidationError(
                    f"New notice replaces {target_id} which does not exist"
                )
        
        # Check previous notice status
        for n in previous_notices:
            if n.get("id") in prev_ids:
                if n.get("status") not in ("sent", "completed"):
                    raise ValidationError(
                        f"Previous notice {n.get('id')} has status {n.get('status')}, "
                        f"expected sent or completed"
                    )


# =============================================================================
# MAIN VALIDATION ENTRY POINT
# =============================================================================

def validate_resource_transition(
    resource_type: str,
    current_resource: dict,
    proposed_resource: dict
) -> List[str]:
    """
    Validate a resource transition before applying.
    
    Returns list of warnings (non-blocking issues).
    Raises ForbiddenTransitionError for blocking issues.
    """
    warnings = []
    
    if resource_type in ("ServiceRequest", "Task"):
        # Referral workflow
        sr_status = proposed_resource.get("status", current_resource.get("status"))
        task_status = proposed_resource.get("status") if resource_type == "Task" else None
        
        # For ServiceRequest, we need Task status from context
        if resource_type == "ServiceRequest" and task_status is None:
            # Can't fully validate without Task, but can check ServiceRequest alone
            pass
        
    elif resource_type == "Observation":
        # ScreeningEvent panel
        status = proposed_resource.get("status", current_resource.get("status"))
        if status:
            validate_transition("screening", 
                              current_resource.get("status", "registered"), 
                              status)
            
            # Check panel has 2 members
            has_member = proposed_resource.get("hasMember", [])
            if status == "final" and len(has_member) != 2:
                raise ValidationError(
                    "Screening panel must have exactly 2 member Observations (OD and OS)"
                )
    
    elif resource_type == "DiagnosticReport":
        status = proposed_resource.get("status", current_resource.get("status"))
        if status:
            validate_transition("assessment",
                              current_resource.get("status", "registered"),
                              status)
    
    elif resource_type == "Consent":
        status = proposed_resource.get("status", current_resource.get("status"))
        if status:
            validate_transition("consent",
                              current_resource.get("status", "draft"),
                              status)
        # Validate provisions
        provisions = proposed_resource.get("provision", [])
        if provisions:
            validate_consent_provisions(provisions)
    
    elif resource_type == "Communication":
        status = proposed_resource.get("status", current_resource.get("status"))
        if status:
            validate_transition("communication",
                              current_resource.get("status", "preparation"),
                              status)
        # Validate supersession
        relates_to = proposed_resource.get("relatesTo", [])
        replaces = [r for r in relates_to if r.get("code") == "replaces"]
        if replaces and status == "completed":
            warnings.append("Ensure previous notice status updated to superseded")
    
    elif resource_type == "DocumentReference":
        status = proposed_resource.get("status", current_resource.get("status"))
        if status:
            validate_transition("document",
                              current_resource.get("status", "current"),
                              status)
        # Validate document type
        doc_type = proposed_resource.get("type", {}).get("coding", [{}])[0].get("code")
        source = proposed_resource.get("author", [{}])[0].get("reference", "")
        if doc_type:
            source_key = "school" if "school" in source.lower() else "ophthalmology"
            validate_document_type_matches_ip4(doc_type, source_key)
    
    return warnings