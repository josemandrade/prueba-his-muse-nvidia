"""
Resource Builders for School Vision Screening

Constructs FHIR resources matching the IG profiles exactly.
All data is synthetic - no real patient data.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid
import json


CANONICAL_BASE = "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening"


# =============================================================================
# PROFILE URLs
# =============================================================================

PROFILES = {
    "patient": f"{CANONICAL_BASE}/StructureDefinition/svs-patient",
    "related_person": f"{CANONICAL_BASE}/StructureDefinition/svs-related-person",
    "practitioner": f"{CANONICAL_BASE}/StructureDefinition/svs-practitioner",
    "practitioner_role": f"{CANONICAL_BASE}/StructureDefinition/svs-practitioner-role",
    "organization": f"{CANONICAL_BASE}/StructureDefinition/svs-organization",
    "encounter": f"{CANONICAL_BASE}/StructureDefinition/svs-encounter-screening",
    "screening_panel": f"{CANONICAL_BASE}/StructureDefinition/svs-observation-screening-panel",
    "right_eye_acuity": f"{CANONICAL_BASE}/StructureDefinition/svs-observation-right-eye-acuity",
    "left_eye_acuity": f"{CANONICAL_BASE}/StructureDefinition/svs-observation-left-eye-acuity",
    "service_request_referral": f"{CANONICAL_BASE}/StructureDefinition/svs-service-request-referral",
    "task_referral_tracking": f"{CANONICAL_BASE}/StructureDefinition/svs-task-referral-tracking",
    "diagnostic_report_assessment": f"{CANONICAL_BASE}/StructureDefinition/svs-diagnostic-report-assessment",
    "observation_diagnosis": f"{CANONICAL_BASE}/StructureDefinition/svs-observation-diagnosis",
    "observation_refraction_od": f"{CANONICAL_BASE}/StructureDefinition/svs-observation-refraction-od",
    "observation_refraction_os": f"{CANONICAL_BASE}/StructureDefinition/svs-observation-refraction-os",
    "care_plan_followup": f"{CANONICAL_BASE}/StructureDefinition/svs-care-plan-follow-up",
    "communication_accommodation": f"{CANONICAL_BASE}/StructureDefinition/svs-communication-accommodation",
    "consent_optout": f"{CANONICAL_BASE}/StructureDefinition/svs-consent-opt-out",
    "document_reference_ip4": f"{CANONICAL_BASE}/StructureDefinition/svs-document-reference-ip4",
    "list_primary_care": f"{CANONICAL_BASE}/StructureDefinition/svs-list-primary-care-documents",
    "questionnaire_response": f"{CANONICAL_BASE}/StructureDefinition/svs-questionnaire-response-screening",
}


# =============================================================================
# CODESYSTEM VALUES
# =============================================================================

SVS_CODESYSTEMS = {
    "screening_test_method": f"{CANONICAL_BASE}/CodeSystem/svs-screening-test-method",
    "screening_outcome": f"{CANONICAL_BASE}/CodeSystem/svs-screening-outcome",
    "referral_reason": f"{CANONICAL_BASE}/CodeSystem/svs-referral-reason",
    "accommodation_type": f"{CANONICAL_BASE}/CodeSystem/svs-accommodation-type",
    "practitioner_role": f"{CANONICAL_BASE}/CodeSystem/svs-practitioner-role",
    "document_type": f"{CANONICAL_BASE}/CodeSystem/svs-document-type",
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _meta(profile: str) -> dict:
    return {"profile": [profile]}


def _id() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _coding(system: str, code: str, display: Optional[str] = None) -> dict:
    c = {"system": system, "code": code}
    if display:
        c["display"] = display
    return c


def _reference(resource_type: str, id: str) -> dict:
    return {"reference": f"{resource_type}/{id}"}


def _period(start: str, end: Optional[str] = None) -> dict:
    p = {"start": start}
    if end:
        p["end"] = end
    return p


def _ratio(numerator: float, denominator: float, unit: str = "m") -> dict:
    return {
        "numerator": {"value": numerator, "unit": unit, "system": "http://unitsofmeasure.org", "code": unit},
        "denominator": {"value": denominator, "unit": unit, "system": "http://unitsofmeasure.org", "code": unit},
    }


# =============================================================================
# PATIENT / RELATEDPERSON
# =============================================================================

def build_patient(
    id: str,
    family: str,
    given: List[str],
    birth_date: str,
    gender: str,
    school_roll: str,
    national_id: Optional[str] = None,
    pixm_id: Optional[str] = None,
    address: Optional[dict] = None,
    phone: Optional[str] = None,
    managing_org: Optional[str] = None,
) -> dict:
    """Build SVSPatient"""
    identifiers = [
        {
            "system": "urn:oid:1.2.3.4.5.school-roll",
            "value": school_roll,
            "type": {"coding": [_coding("http://terminology.hl7.org/CodeSystem/v2-0203", "SB", "School Board")]},
        }
    ]
    if national_id:
        identifiers.append({
            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
            "value": national_id,
            "type": {"coding": [_coding("http://terminology.hl7.org/CodeSystem/v2-0203", "NI", "National unique individual identifier")]},
            "use": "official",
        })
    if pixm_id:
        identifiers.append({
            "system": "urn:ihe:pixm:cross-ref",
            "value": pixm_id,
            "type": {"coding": [_coding("http://terminology.hl7.org/CodeSystem/v2-0203", "PIXM", "PIXm Cross-reference")]},
        })
    
    name = [{"use": "official", "family": family, "given": given}]
    
    pat = {
        "resourceType": "Patient",
        "id": id,
        "meta": _meta(PROFILES["patient"]),
        "identifier": identifiers,
        "name": name,
        "birthDate": birth_date,
        "gender": gender,
    }
    
    if address:
        pat["address"] = [address]
    if phone:
        pat["telecom"] = [{"system": "phone", "value": phone, "use": "home"}]
    if managing_org:
        pat["managingOrganization"] = _reference("Organization", managing_org)
    
    return pat


def build_related_person(
    id: str,
    patient_id: str,
    family: str,
    given: List[str],
    relationship_code: str = "MTH",
    relationship_display: str = "Mother",
    phone: Optional[str] = None,
) -> dict:
    """Build SVSRelatedPerson"""
    return {
        "resourceType": "RelatedPerson",
        "id": id,
        "meta": _meta(PROFILES["related_person"]),
        "patient": _reference("Patient", patient_id),
        "relationship": [{"coding": [_coding("http://terminology.hl7.org/CodeSystem/v2-0131", relationship_code, relationship_display)]}],
        "name": [{"use": "official", "family": family, "given": given}],
        "telecom": [{"system": "phone", "value": phone, "use": "home"}] if phone else [],
    }


# =============================================================================
# PRACTITIONER / PRACTITIONERROLE
# =============================================================================

def build_practitioner(
    id: str,
    family: str,
    given: List[str],
    employee_id: str,
    license_number: Optional[str] = None,
    phone: Optional[str] = None,
) -> dict:
    """Build SVSPractitioner"""
    identifiers = [{"system": "urn:oid:1.2.3.4.5.employee", "value": employee_id}]
    if license_number:
        identifiers.append({
            "system": "urn:oid:1.2.3.4.5.license",
            "value": license_number,
            "type": {"coding": [_coding("http://terminology.hl7.org/CodeSystem/v2-0203", "PRN", "Provider number")]},
        })
    
    return {
        "resourceType": "Practitioner",
        "id": id,
        "meta": _meta(PROFILES["practitioner"]),
        "identifier": identifiers,
        "name": [{"use": "official", "family": family, "given": given}],
        "telecom": [{"system": "phone", "value": phone, "use": "work"}] if phone else [],
    }


def build_practitioner_role(
    id: str,
    practitioner_id: str,
    organization_id: str,
    role_code: str = "school-nurse",
    role_display: str = "School Nurse",
) -> dict:
    """Build SVSPractitionerRole"""
    return {
        "resourceType": "PractitionerRole",
        "id": id,
        "meta": _meta(PROFILES["practitioner_role"]),
        "practitioner": _reference("Practitioner", practitioner_id),
        "organization": _reference("Organization", organization_id),
        "code": [{"coding": [_coding(SVS_CODESYSTEMS["practitioner_role"], role_code, role_display)]}],
    }


# =============================================================================
# ORGANIZATION
# =============================================================================

def build_organization(
    id: str,
    name: str,
    org_type: str,  # "school", "clinic", "primary-care", "health-service"
    identifier: str,
    phone: Optional[str] = None,
    address: Optional[dict] = None,
) -> dict:
    """Build SVSOrganization"""
    type_map = {
        "school": {"coding": [_coding("http://terminology.hl7.org/CodeSystem/organization-type", "edu", "Educational facility")]},
        "clinic": {"coding": [_coding("http://terminology.hl7.org/CodeSystem/organization-type", "prov", "Healthcare Provider")]},
        "primary-care": {"coding": [_coding("http://terminology.hl7.org/CodeSystem/organization-type", "prov", "Healthcare Provider")]},
        "health-service": {"coding": [_coding("http://terminology.hl7.org/CodeSystem/organization-type", "dept", "Department")]},
    }
    
    return {
        "resourceType": "Organization",
        "id": id,
        "meta": _meta(PROFILES["organization"]),
        "identifier": [{"system": f"urn:oid:1.2.3.4.5.{org_type}-id", "value": identifier}],
        "name": name,
        "type": [type_map.get(org_type, type_map["clinic"])],
        "telecom": [{"system": "phone", "value": phone, "use": "work"}] if phone else [],
        "address": [address] if address else [],
    }


# =============================================================================
# ENCOUNTER
# =============================================================================

def build_encounter(
    id: str,
    patient_id: str,
    practitioner_id: str,
    org_id: str,
    start: str,
    end: str,
    encounter_type_code: str = "vision-screening",
) -> dict:
    """Build screening Encounter"""
    return {
        "resourceType": "Encounter",
        "id": id,
        "status": "finished",
        "class": _coding("http://terminology.hl7.org/CodeSystem/v3-ActCode", "AMB", "Ambulatory"),
        "type": [{"coding": [_coding(f"{CANONICAL_BASE}/CodeSystem/encounter-type", encounter_type_code, "Vision Screening")]}],
        "subject": _reference("Patient", patient_id),
        "participant": [{
            "individual": _reference("Practitioner", practitioner_id),
            "type": [{"coding": [_coding("http://terminology.hl7.org/CodeSystem/v3-ParticipationType", "PPRF", "Primary performer")]}],
        }],
        "period": {"start": start, "end": end},
        "serviceProvider": _reference("Organization", org_id),
    }


# =============================================================================
# SCREENING OBSERVATIONS
# =============================================================================

def build_right_eye_acuity(
    id: str,
    patient_id: str,
    encounter_id: str,
    practitioner_role_id: str,
    snellen_num: int,
    snellen_denom: int,
    status: str = "final",
    effective: Optional[str] = None,
    interpretation: str = "N",  # N=Normal, A=Abnormal
) -> dict:
    """Build SVSObservationRightEyeAcuity"""
    return {
        "resourceType": "Observation",
        "id": id,
        "meta": _meta(PROFILES["right_eye_acuity"]),
        "status": status,
        "category": [{"coding": [_coding("http://terminology.hl7.org/CodeSystem/observation-category", "vital-signs", "Vital Signs")]}],
        "code": {"coding": [_coding("http://loinc.org", "29474-1", "Visual acuity right eye")]},
        "subject": _reference("Patient", patient_id),
        "encounter": _reference("Encounter", encounter_id),
        "effectiveDateTime": effective or _now(),
        "performer": [_reference("PractitionerRole", practitioner_role_id)],
        "valueRatio": _ratio(snellen_num, snellen_denom),
        "bodySite": {"coding": [_coding("http://snomed.info/sct", "363654007", "Right eye")]},
        "interpretation": [{"coding": [_coding("http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation", interpretation, "Normal" if interpretation == "N" else "Abnormal")]}],
    }


def build_left_eye_acuity(
    id: str,
    patient_id: str,
    encounter_id: str,
    practitioner_role_id: str,
    snellen_num: int,
    snellen_denom: int,
    status: str = "final",
    effective: Optional[str] = None,
    interpretation: str = "N",
) -> dict:
    """Build SVSObservationLeftEyeAcuity"""
    return {
        "resourceType": "Observation",
        "id": id,
        "meta": _meta(PROFILES["left_eye_acuity"]),
        "status": status,
        "category": [{"coding": [_coding("http://terminology.hl7.org/CodeSystem/observation-category", "vital-signs", "Vital Signs")]}],
        "code": {"coding": [_coding("http://loinc.org", "29473-3", "Visual acuity left eye")]},
        "subject": _reference("Patient", patient_id),
        "encounter": _reference("Encounter", encounter_id),
        "effectiveDateTime": effective or _now(),
        "performer": [_reference("PractitionerRole", practitioner_role_id)],
        "valueRatio": _ratio(snellen_num, snellen_denom),
        "bodySite": {"coding": [_coding("http://snomed.info/sct", "363655008", "Left eye")]},
        "interpretation": [{"coding": [_coding("http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation", interpretation, "Normal" if interpretation == "N" else "Abnormal")]}],
    }


def build_screening_panel(
    id: str,
    patient_id: str,
    encounter_id: str,
    practitioner_role_id: str,
    right_eye_id: str,
    left_eye_id: str,
    test_method: str = "snellen",
    outcome: str = "refer",
    attempt: int = 1,
    status: str = "final",
    effective: Optional[str] = None,
    note: Optional[str] = None,
) -> dict:
    """Build SVSObservationScreeningPanel"""
    panel = {
        "resourceType": "Observation",
        "id": id,
        "meta": _meta(PROFILES["screening_panel"]),
        "status": status,
        "category": [{"coding": [_coding("http://terminology.hl7.org/CodeSystem/observation-category", "vital-signs", "Vital Signs")]}],
        "code": {"coding": [_coding("http://loinc.org", "83700-8", "Visual acuity screening panel")]},
        "subject": _reference("Patient", patient_id),
        "encounter": _reference("Encounter", encounter_id),
        "effectiveDateTime": effective or _now(),
        "performer": [_reference("PractitionerRole", practitioner_role_id)],
        "hasMember": [
            _reference("Observation", right_eye_id),
            _reference("Observation", left_eye_id),
        ],
    }
    
    if note:
        panel["note"] = [{"text": note}]
    
    # Add SVS-specific extensions via note or custom
    panel["note"] = panel.get("note", []) + [{
        "text": f"Test used: {test_method}; Outcome: {outcome}; Attempt: {attempt}; Referral indicated: {outcome == 'refer'}"
    }]
    
    return panel


# =============================================================================
# REFERRAL (SERVICEREQUEST + TASK)
# =============================================================================

def build_service_request_referral(
    id: str,
    patient_id: str,
    encounter_id: str,
    practitioner_role_id: str,
    organization_id: str,
    reason_codes: List[dict],  # [{"system": "...", "code": "...", "display": "..."}]
    reason_reference: str,  # Observation reference
    referral_id: str,
    referral_360x_id: Optional[str] = None,
    status: str = "active",
    expected_deadline: Optional[str] = None,
) -> dict:
    """Build SVSServiceRequestReferral"""
    sr = {
        "resourceType": "ServiceRequest",
        "id": id,
        "meta": _meta(PROFILES["service_request_referral"]),
        "identifier": [
            {"system": f"{CANONICAL_BASE}/referral", "value": referral_id},
        ],
        "status": status,
        "intent": "order",
        "category": [{"coding": [_coding("http://terminology.hl7.org/CodeSystem/service-request-category", "referral", "Referral")]}],
        "priority": "routine",
        "code": {"coding": [_coding("http://snomed.info/sct", "307924000", "Referral to ophthalmologist")]},
        "subject": _reference("Patient", patient_id),
        "encounter": _reference("Encounter", encounter_id),
        "occurrenceDateTime": _now(),
        "authoredOn": _now(),
        "requester": _reference("PractitionerRole", practitioner_role_id),
        "performer": [_reference("Organization", organization_id)],
        "reasonCode": reason_codes,
        "reasonReference": [_reference("Observation", reason_reference)],
    }
    
    if referral_360x_id:
        sr["identifier"].append({"system": "urn:ihe:pcc:360x:referral-id", "value": referral_360x_id})
    
    if expected_deadline:
        sr["extension"] = [{
            "url": f"{CANONICAL_BASE}/expected-deadline",
            "valueDateTime": expected_deadline,
        }]
    
    return sr


def build_task_referral_tracking(
    id: str,
    patient_id: str,
    service_request_id: str,
    practitioner_role_id: str,
    organization_id: str,
    status: str = "requested",
    encounter_id: Optional[str] = None,
) -> dict:
    """Build SVSTaskReferralTracking"""
    task = {
        "resourceType": "Task",
        "id": id,
        "meta": _meta(PROFILES["task_referral_tracking"]),
        "status": status,
        "intent": "order",
        "code": {"coding": [_coding("http://hl7.org/fhir/CodeSystem/task-code", "referral", "Referral tracking")]},
        "for": _reference("Patient", patient_id),
        "focus": _reference("ServiceRequest", service_request_id),
        "authoredOn": _now(),
        "lastModified": _now(),
        "requester": _reference("PractitionerRole", practitioner_role_id),
        "owner": _reference("Organization", organization_id),
    }
    
    if encounter_id:
        task["encounter"] = _reference("Encounter", encounter_id)
    
    return task


# =============================================================================
# ASSESSMENT
# =============================================================================

def build_diagnostic_report_assessment(
    id: str,
    patient_id: str,
    encounter_id: str,
    service_request_id: str,
    practitioner_id: str,
    result_refs: List[str],  # Observation references
    conclusion: str,
    conclusion_codes: List[dict],
    status: str = "final",
    effective: Optional[str] = None,
    issued: Optional[str] = None,
) -> dict:
    """Build SVSDiagnosticReportAssessment"""
    return {
        "resourceType": "DiagnosticReport",
        "id": id,
        "meta": _meta(PROFILES["diagnostic_report_assessment"]),
        "status": status,
        "category": [{"coding": [_coding("http://terminology.hl7.org/CodeSystem/v2-0074", "OP", "Ophthalmology")]}],
        "code": {"coding": [_coding("http://loinc.org", "28626-8", "Ophthalmology study")]},
        "subject": _reference("Patient", patient_id),
        "encounter": _reference("Encounter", encounter_id),
        "effectiveDateTime": effective or _now(),
        "issued": issued or _now(),
        "performer": [_reference("Practitioner", practitioner_id)],
        "resultsInterpreter": [_reference("Practitioner", practitioner_id)],
        "basedOn": [_reference("ServiceRequest", service_request_id)],
        "result": [_reference("Observation", r) for r in result_refs],
        "conclusion": conclusion,
        "conclusionCode": conclusion_codes,
    }


def build_observation_diagnosis(
    id: str,
    patient_id: str,
    snomed_code: str,
    snomed_display: str,
    body_site_code: str = "363654007",
    body_site_display: str = "Right eye",
    status: str = "final",
    effective: Optional[str] = None,
) -> dict:
    """Build SVSObservationDiagnosis"""
    return {
        "resourceType": "Observation",
        "id": id,
        "meta": _meta(PROFILES["observation_diagnosis"]),
        "status": status,
        "category": [{"coding": [_coding("http://terminology.hl7.org/CodeSystem/observation-category", "diagnosis", "Diagnosis")]}],
        "code": {"coding": [_coding("http://snomed.info/sct", snomed_code, snomed_display)]},
        "subject": _reference("Patient", patient_id),
        "effectiveDateTime": effective or _now(),
        "valueCodeableConcept": {"coding": [_coding("http://snomed.info/sct", snomed_code, snomed_display)]},
        "bodySite": {"coding": [_coding("http://snomed.info/sct", body_site_code, body_site_display)]},
    }


def build_observation_refraction(
    id: str,
    patient_id: str,
    eye: str,  # "OD" or "OS"
    sphere: float,
    cylinder: float = 0.0,
    axis: int = 0,
    status: str = "final",
    effective: Optional[str] = None,
) -> dict:
    """Build SVSObservationRefractionOD or OS"""
    profile = PROFILES["observation_refraction_od"] if eye == "OD" else PROFILES["observation_refraction_os"]
    loinc_code = "29474-1" if eye == "OD" else "29473-3"
    body_site = "363654007" if eye == "OD" else "363655008"
    body_site_display = "Right eye" if eye == "OD" else "Left eye"
    
    # Build prescription string
    parts = [f"{sphere:+.2f} DS"]
    if cylinder != 0:
        parts.append(f"{cylinder:+.2f} DC x {axis}")
    prescription = " ".join(parts)
    
    return {
        "resourceType": "Observation",
        "id": id,
        "meta": _meta(profile),
        "status": status,
        "category": [{"coding": [_coding("http://terminology.hl7.org/CodeSystem/observation-category", "exam", "Exam")]}],
        "code": {"coding": [_coding("http://loinc.org", loinc_code, f"Visual acuity {eye} eye")]},
        "subject": _reference("Patient", patient_id),
        "effectiveDateTime": effective or _now(),
        "valueQuantity": {
            "value": sphere,
            "unit": "D",
            "system": "http://unitsofmeasure.org",
            "code": "D",
        },
        "component": [
            {"code": {"coding": [_coding("http://loinc.org", "29474-1" if eye == "OD" else "29473-3", "Sphere")]},
             "valueQuantity": {"value": sphere, "unit": "D", "system": "http://unitsofmeasure.org", "code": "D"}},
            {"code": {"coding": [_coding("http://loinc.org", "29474-1" if eye == "OD" else "29473-3", "Cylinder")]},
             "valueQuantity": {"value": cylinder, "unit": "D", "system": "http://unitsofmeasure.org", "code": "D"}},
        ] if cylinder != 0 else [],
        "bodySite": {"coding": [_coding("http://snomed.info/sct", body_site, body_site_display)]},
        "note": [{"text": f"Refraction: {prescription}"}],
    }


def build_care_plan_followup(
    id: str,
    patient_id: str,
    encounter_id: str,
    period_start: str,
    period_end: str,
    followup_code: str,
    followup_display: str,
    description: str,
    status: str = "active",
) -> dict:
    """Build SVSCarePlanFollowUp"""
    return {
        "resourceType": "CarePlan",
        "id": id,
        "meta": _meta(PROFILES["care_plan_followup"]),
        "status": status,
        "intent": "plan",
        "category": [{"coding": [_coding("http://terminology.hl7.org/CodeSystem/careplan-category", "assess-plan", "Assessment Plan")]}],
        "subject": _reference("Patient", patient_id),
        "encounter": _reference("Encounter", encounter_id),
        "period": {"start": period_start, "end": period_end},
        "activity": [{
            "detail": {
                "kind": "ServiceRequest",
                "code": {"coding": [_coding("http://snomed.info/sct", followup_code, followup_display)]},
                "scheduledPeriod": {"start": period_end, "end": period_end},
                "status": "not-started",
                "description": description,
            }
        }],
    }


# =============================================================================
# COMMUNICATION (ACCOMMODATION)
# =============================================================================

def build_communication_accommodation(
    id: str,
    patient_id: str,
    sender_id: str,  # PractitionerRole
    recipient_ids: List[str],  # PractitionerRole or RelatedPerson
    content: str,
    status: str = "sent",
    sent: Optional[str] = None,
    replaces_id: Optional[str] = None,
) -> dict:
    """Build SVSCommunicationAccommodation"""
    comm = {
        "resourceType": "Communication",
        "id": id,
        "meta": _meta(PROFILES["communication_accommodation"]),
        "status": status,
        "category": [{"coding": [_coding("http://terminology.hl7.org/CodeSystem/communication-category", "instruction", "Instruction")]}],
        "subject": _reference("Patient", patient_id),
        "sender": _reference("PractitionerRole", sender_id),
        "recipient": [_reference("PractitionerRole" if "PractitionerRole" in r else "RelatedPerson", r) for r in recipient_ids],
        "sent": sent or _now(),
        "payload": [{"contentString": content}],
    }
    
    if replaces_id:
        comm["relatesTo"] = [{
            "code": "replaces",
            "target": _reference("Communication", replaces_id),
        }]
    
    return comm


# =============================================================================
# CONSENT (OPTOUT)
# =============================================================================

def build_consent_optout(
    id: str,
    patient_id: str,
    practitioner_role_id: str,
    organization_id: str,
    provisions: List[dict],  # [{"type": "deny|permit", "period": {"start": "...", "end": "..."}}]
    status: str = "active",
    date_time: Optional[str] = None,
) -> dict:
    """Build SVSConsentOptOut"""
    consent = {
        "resourceType": "Consent",
        "id": id,
        "meta": _meta(PROFILES["consent_optout"]),
        "status": status,
        "scope": {"coding": [_coding("http://terminology.hl7.org/CodeSystem/consentscope", "screening", "Screening")]},
        "category": [{"coding": [_coding("http://terminology.hl7.org/CodeSystem/consentcategorycodes", "DENY", "Deny")]}],
        "patient": _reference("Patient", patient_id),
        "dateTime": date_time or _now(),
        "performer": [_reference("PractitionerRole", practitioner_role_id)],
        "organization": _reference("Organization", organization_id),
        "provision": [],
    }
    
    for prov in provisions:
        consent["provision"].append({
            "type": prov["type"],
            "period": prov["period"],
        })
    
    return consent


# =============================================================================
# DOCUMENTREFERENCE (IP-4)
# =============================================================================

def build_document_reference_ip4(
    id: str,
    patient_id: str,
    doc_type_code: str,  # e.g., "screening-pass"
    loinc_code: str,
    loinc_display: str,
    source_url: str,
    author_id: str,
    custodian_id: str,
    description: str,
    encounter_id: Optional[str] = None,
    period_start: Optional[str] = None,
    period_end: Optional[str] = None,
    status: str = "current",
    date: Optional[str] = None,
) -> dict:
    """Build SVSDocumentReferenceIP4"""
    doc = {
        "resourceType": "DocumentReference",
        "id": id,
        "meta": _meta(PROFILES["document_reference_ip4"]),
        "status": status,
        "type": {"coding": [_coding("http://loinc.org", loinc_code, loinc_display)]},
        "category": [{"coding": [_coding("http://terminology.hl7.org/CodeSystem/document-class", "screening-report", "Screening Report")]}],
        "subject": _reference("Patient", patient_id),
        "date": date or _now(),
        "author": [_reference("PractitionerRole", author_id)],
        "custodian": _reference("Organization", custodian_id),
        "description": description,
        "content": [{
            "attachment": {
                "contentType": "application/fhir+json",
                "url": source_url,
            }
        }],
    }
    
    context = {}
    if encounter_id:
        context["encounter"] = [_reference("Encounter", encounter_id)]
    if period_start:
        context["period"] = {"start": period_start}
        if period_end:
            context["period"]["end"] = period_end
    if context:
        doc["context"] = context
    
    return doc


# =============================================================================
# LIST (PRIMARY CARE DOCUMENT LOG)
# =============================================================================

def build_list_primary_care(
    id: str,
    patient_id: str,
    document_refs: List[str],
    title: str = "School Vision Screening Documents",
    status: str = "current",
    mode: str = "working",
) -> dict:
    """Build SVSListPrimaryCareDocuments"""
    return {
        "resourceType": "List",
        "id": id,
        "meta": _meta(PROFILES["list_primary_care"]),
        "status": status,
        "mode": mode,
        "title": title,
        "subject": _reference("Patient", patient_id),
        "entry": [{"item": _reference("DocumentReference", ref)} for ref in document_refs],
    }


# =============================================================================
# SUBSCRIPTION
# =============================================================================

def build_subscription(
    id: str,
    patient_id: str,
    endpoint: str,
    criteria: str = "DiagnosticReport?patient=Patient/{patient_id}&category=OP",
) -> dict:
    """Build Subscription for assessment notifications"""
    return {
        "resourceType": "Subscription",
        "id": id,
        "status": "requested",
        "criteria": criteria.format(patient_id=patient_id),
        "channel": {
            "type": "rest-hook",
            "endpoint": endpoint,
            "payload": "application/fhir+json",
        },
    }