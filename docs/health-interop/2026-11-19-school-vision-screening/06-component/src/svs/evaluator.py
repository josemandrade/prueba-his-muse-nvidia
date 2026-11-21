"""
Rule Evaluation for School Vision Screening

This module evaluates clinical rules over patient data to produce DetectedIssues
or block operations. Separated from transitions.py (which holds states).
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json


class EvaluationResult(str, Enum):
    """Result of a rule evaluation"""
    TRIGGERED = "triggered"
    NOT_TRIGGERED = "not_triggered"
    ERROR = "error"


@dataclass
class DetectedIssue:
    """FHIR DetectedIssue resource representation"""
    code: str
    severity: str  # high, moderate, low
    detail: str
    reference: str  # Reference to the resource that triggered the issue
    mitigation: Optional[str] = None


# =============================================================================
# VISUAL ACUITY THRESHOLD RULES (Point Rules)
# =============================================================================

# Snellen acuity thresholds (6m equivalent)
# Referral criteria: <= 6/12 in either eye OR >= 2 line difference
SNELLEN_THRESHOLDS = {
    "6/3": -0.30,
    "6/4": -0.20,
    "6/5": -0.10,
    "6/6": 0.0,
    "6/7.5": 0.10,
    "6/9": 0.20,
    "6/12": 0.30,
    "6/18": 0.50,
    "6/24": 0.60,
    "6/36": 0.80,
    "6/60": 1.00,
}

# 2-line difference in logMAR = 0.20
LINE_DIFF_THRESHOLD = 0.20


def snellen_to_logmar(snellen: str) -> float:
    """Convert Snellen fraction (e.g., '6/12') to logMAR value"""
    if "/" not in snellen:
        raise ValueError(f"Invalid Snellen format: {snellen}")
    num, denom = snellen.split("/")
    try:
        return SNELLEN_THRESHOLDS.get(snellen, float(num) / float(denom) * 0.3)  # Approximate
    except ValueError:
        return 0.0


def evaluate_visual_acuity_referral(
    right_eye_snellen: str,
    left_eye_snellen: str
) -> List[DetectedIssue]:
    """
    Evaluate visual acuity against referral criteria.
    
    Criteria (from use case):
    - Visual acuity <= 6/12 in either eye -> Refer
    - >= 2 line difference between eyes -> Refer
    
    Returns:
        List of DetectedIssues (empty if no referral needed)
    """
    issues = []
    
    try:
        od_logmar = snellen_to_logmar(right_eye_snellen)
        os_logmar = snellen_to_logmar(left_eye_snellen)
    except ValueError as e:
        return [DetectedIssue(
            code="invalid-acuity",
            severity="high",
            detail=f"Invalid acuity format: {e}",
            reference="Observation/visual-acuity"
        )]
    
    # Check <= 6/12 (logMAR >= 0.30)
    if od_logmar >= 0.30:
        issues.append(DetectedIssue(
            code="acuity-low-od",
            severity="high",
            detail=f"Right eye visual acuity {right_eye_snellen} <= 6/12 (logMAR {od_logmar:.2f})",
            reference="Observation/right-eye-acuity",
            mitigation="Refer to ophthalmology"
        ))
    
    if os_logmar >= 0.30:
        issues.append(DetectedIssue(
            code="acuity-low-os",
            severity="high",
            detail=f"Left eye visual acuity {left_eye_snellen} <= 6/12 (logMAR {os_logmar:.2f})",
            reference="Observation/left-eye-acuity",
            mitigation="Refer to ophthalmology"
        ))
    
    # Check >= 2 line difference
    diff = abs(od_logmar - os_logmar)
    if diff >= LINE_DIFF_THRESHOLD:
        issues.append(DetectedIssue(
            code="acuity-difference",
            severity="high",
            detail=f"Inter-eye acuity difference {diff:.2f} logMAR >= 2 lines",
            reference="Observation/screening-panel",
            mitigation="Refer to ophthalmology"
        ))
    
    return issues


def evaluate_screening_outcome(
    right_eye_snellen: str,
    left_eye_snellen: str
) -> Tuple[str, List[DetectedIssue]]:
    """
    Determine screening outcome based on acuity.
    
    Returns: (outcome_code, issues)
    outcome_code: "pass", "refer", "absent", "incomplete"
    """
    issues = evaluate_visual_acuity_referral(right_eye_snellen, left_eye_snellen)
    
    if issues:
        return "refer", issues
    return "pass", []


# =============================================================================
# SCREENING ATTEMPT RULES
# =============================================================================

def evaluate_screening_attempt(
    attempt_number: int,
    previous_outcome: Optional[str],
    current_outcome: str,
    has_partial_data: bool = False
) -> List[DetectedIssue]:
    """
    Evaluate screening attempt rules.
    
    Rules from lifecycle:
    - 1st Absent -> re-screen (attempt 2)
    - 2nd Absent -> missed (terminal, notify)
    - 1st Incomplete -> re-screen (attempt 2)
    - 2nd Incomplete -> direct referral with partial data
    """
    issues = []
    
    if attempt_number == 1:
        if previous_outcome:
            issues.append(DetectedIssue(
                code="invalid-attempt-sequence",
                severity="high",
                detail=f"Attempt 1 cannot have previous outcome: {previous_outcome}",
                reference="Observation/screening-panel"
            ))
    
    elif attempt_number == 2:
        if previous_outcome == "absent" and current_outcome == "absent":
            issues.append(DetectedIssue(
                code="screening-missed",
                severity="high",
                detail="Second absence - screening missed, notify parent and primary care",
                reference="Observation/screening-panel",
                mitigation="Trigger OP-4d: screening-missed to Primary Care"
            ))
        elif previous_outcome == "incomplete":
            if current_outcome in ("pass", "refer"):
                # Valid - use result
                pass
            elif current_outcome == "incomplete":
                issues.append(DetectedIssue(
                    code="incomplete-referral",
                    severity="high",
                    detail="Second incomplete - direct referral with partial data",
                    reference="Observation/screening-panel",
                    mitigation="Trigger OP-2a: Submit Referral with partial data"
                ))
    
    elif attempt_number > 2:
        issues.append(DetectedIssue(
            code="max-attempts-exceeded",
            severity="high",
            detail=f"Attempt {attempt_number} exceeds maximum of 2",
            reference="Observation/screening-panel"
        ))
    
    return issues


# =============================================================================
# REFERRAL TIMEOUT RULE
# =============================================================================

def evaluate_referral_timeout(
    referral_authored: str,  # ISO datetime
    now: str,
    task_status: str
) -> List[DetectedIssue]:
    """
    Evaluate if referral has timed out (4 weeks / P4W).
    
    Trigger OP-2b: Cancel Referral after 4 weeks with no response.
    """
    from datetime import datetime, timedelta
    issues = []
    
    if task_status in ("completed", "cancelled", "rejected", "failed"):
        return issues  # Already terminal
    
    try:
        authored = datetime.fromisoformat(referral_authored.replace("Z", "+00:00"))
        current = datetime.fromisoformat(now.replace("Z", "+00:00"))
    except ValueError:
        return [DetectedIssue(
            code="invalid-datetime",
            severity="moderate",
            detail="Could not parse referral authored or current time",
            reference="ServiceRequest/referral"
        )]
    
    if current - authored >= timedelta(weeks=4):
        issues.append(DetectedIssue(
            code="referral-timeout",
            severity="high",
            detail=f"Referral timeout after 4 weeks (authored {referral_authored})",
            reference="ServiceRequest/referral",
            mitigation="Trigger OP-2b: Cancel Referral (PCC-58)"
        ))
    
    return issues


# =============================================================================
# CONSENT OVERLAP RULE
# =============================================================================

def evaluate_consent_provisions(provisions: List[dict]) -> List[DetectedIssue]:
    """
    Evaluate consent provisions for overlaps and gaps.
    """
    from datetime import datetime
    issues = []
    
    if not provisions:
        return issues
    
    sorted_provisions = sorted(
        provisions,
        key=lambda p: p.get("period", {}).get("start", "")
    )
    
    for i, prov in enumerate(sorted_provisions):
        start = prov.get("period", {}).get("start")
        end = prov.get("period", {}).get("end")
        
        if not start:
            issues.append(DetectedIssue(
                code="missing-period-start",
                severity="moderate",
                detail=f"Provision {i} missing period.start",
                reference="Consent/optout"
            ))
            continue
        
        try:
            start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
            end_dt = datetime.fromisoformat(end.replace("Z", "+00:00")) if end else None
        except ValueError:
            issues.append(DetectedIssue(
                code="invalid-period-format",
                severity="moderate",
                detail=f"Provision {i} has invalid period format",
                reference="Consent/optout"
            ))
            continue
        
        # Check overlap with next
        if i + 1 < len(sorted_provisions):
            next_prov = sorted_provisions[i + 1]
            next_start = next_prov.get("period", {}).get("start")
            if next_start:
                try:
                    next_start_dt = datetime.fromisoformat(next_start.replace("Z", "+00:00"))
                    if end_dt and start_dt < next_start_dt < end_dt:
                        issues.append(DetectedIssue(
                            code="overlapping-provisions",
                            severity="high",
                            detail=f"Provision {i} overlaps {i+1}",
                            reference="Consent/optout"
                        ))
                    # Check gap
                    elif end_dt and end_dt < next_start_dt:
                        gap_days = (next_start_dt - end_dt).days
                        if gap_days > 1:
                            issues.append(DetectedIssue(
                                code="gap-in-provisions",
                                severity="moderate",
                                detail=f"Gap of {gap_days} days between provision {i} and {i+1}",
                                reference="Consent/optout"
                            ))
                except ValueError:
                    pass
    
    return issues


# =============================================================================
# DOCUMENT REFERENCE TYPE VALIDATION
# =============================================================================

# Mapping from LOINC codes to local keys
LOINC_TO_DOC_TYPE = {
    "83700-8": "screening-pass",  # also used for screening-decline, screening-missed, end-of-year-missed
    "11506-3": "referral-dna",    # also used for referral-rejected
    "28626-8": "assessment-full",
}

# Valid types with their allowed sources
VALID_DOC_TYPES = {
    "screening-pass": {"loinc": "83700-8", "source": "school"},
    "screening-decline": {"loinc": "83700-8", "source": "school"},
    "screening-missed": {"loinc": "83700-8", "source": "school"},
    "end-of-year-missed": {"loinc": "83700-8", "source": "school"},
    "referral-dna": {"loinc": "11506-3", "source": "school"},
    "referral-rejected": {"loinc": "11506-3", "source": "school"},
    "assessment-full": {"loinc": "28626-8", "source": "ophthalmology"},
}

def evaluate_document_reference_type(
    doc_type_code: str,
    source_org_type: str  # "school" or "ophthalmology"
) -> List[DetectedIssue]:
    """
    Validate DocumentReference type matches IP-4 allowed types.
    
    Accepts either local key (e.g., "screening-pass") or LOINC code (e.g., "83700-8").
    """
    issues = []
    
    # Resolve LOINC code to local key if needed
    local_key = LOINC_TO_DOC_TYPE.get(doc_type_code, doc_type_code)
    
    if local_key not in VALID_DOC_TYPES:
        issues.append(DetectedIssue(
            code="invalid-document-type",
            severity="high",
            detail=f"Document type {doc_type_code} not in IP-4 allowed types",
            reference="DocumentReference/ip4"
        ))
        return issues
    
    if VALID_DOC_TYPES[local_key]["source"] != source_org_type:
        issues.append(DetectedIssue(
            code="document-source-mismatch",
            severity="high",
            detail=f"Document type {local_key} must come from {VALID_DOC_TYPES[local_key]['source']}, "
                   f"not {source_org_type}",
            reference="DocumentReference/ip4"
        ))
    
    return issues


# =============================================================================
# ACCOMMODATION NOTICE SUPERSESSION RULE
# =============================================================================

def evaluate_accommodation_supersession(
    new_notice: dict,
    existing_notices: List[dict]
) -> List[DetectedIssue]:
    """
    Validate accommodation notice supersession chain.
    """
    issues = []
    
    relates_to = new_notice.get("relatesTo", [])
    replaces = [r for r in relates_to if r.get("code") == "replaces"]
    
    if replaces:
        # Must reference an existing notice
        for r in replaces:
            target_ref = r.get("target", {}).get("reference", "")
            target_id = target_ref.replace("Communication/", "")
            
            found = any(n.get("id") == target_id for n in existing_notices)
            if not found:
                issues.append(DetectedIssue(
                    code="replaces-missing-target",
                    severity="high",
                    detail=f"New notice replaces {target_id} which does not exist",
                    reference="Communication/accommodation"
                ))
        
        # Check previous notice status
        for n in existing_notices:
            if n.get("id") in [r.get("target", {}).get("reference", "").replace("Communication/", "") 
                               for r in replaces]:
                if n.get("status") not in ("sent", "completed"):
                    issues.append(DetectedIssue(
                        code="invalid-previous-status",
                        severity="moderate",
                        detail=f"Previous notice {n.get('id')} has status {n.get('status')}, "
                               f"expected sent or completed",
                        reference="Communication/accommodation"
                    ))
    
    return issues


# =============================================================================
# MAIN EVALUATOR ENTRY POINT
# =============================================================================

def evaluate_all_rules(
    resource_type: str,
    resource: dict,
    context: dict
) -> List[DetectedIssue]:
    """
    Evaluate all applicable rules for a resource.
    
    Args:
        resource_type: FHIR resource type
        resource: The resource to evaluate
        context: Additional context (patient, other resources, etc.)
        
    Returns:
        List of DetectedIssues
    """
    all_issues = []
    
    if resource_type == "Observation":
        # Screening panel evaluation
        if resource.get("code", {}).get("coding", [{}])[0].get("code") == "83700-8":
            # This is a screening panel - evaluate members
            has_member = resource.get("hasMember", [])
            if len(has_member) == 2:
                # In real impl, would fetch member resources
                # For now, check if acuity values present
                pass
    
    elif resource_type == "ServiceRequest":
        # Referral timeout check
        if resource.get("code", {}).get("coding", [{}])[0].get("code") == "307924000":
            authored = resource.get("authoredOn")
            if authored:
                issues = evaluate_referral_timeout(
                    authored,
                    context.get("now", ""),
                    context.get("task_status", "requested")
                )
                all_issues.extend(issues)
    
    elif resource_type == "Consent":
        provisions = resource.get("provision", [])
        if provisions:
            all_issues.extend(evaluate_consent_provisions(provisions))
    
    elif resource_type == "DocumentReference":
        doc_type = resource.get("type", {}).get("coding", [{}])[0].get("code")
        source = resource.get("author", [{}])[0].get("reference", "")
        source_type = "school" if "school" in source.lower() else "ophthalmology"
        if doc_type:
            all_issues.extend(evaluate_document_reference_type(doc_type, source_type))
    
    elif resource_type == "Communication":
        existing = context.get("existing_notices", [])
        all_issues.extend(evaluate_accommodation_supersession(resource, existing))
    
    return all_issues