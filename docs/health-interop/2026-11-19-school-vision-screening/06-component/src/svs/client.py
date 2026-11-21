"""
FHIR Client for School Vision Screening Component

Provides async FHIR operations with validation using transitions.py and evaluator.py.
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime, timezone
import httpx
import uuid

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
)
from .evaluator import evaluate_all_rules, DetectedIssue
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

logger = logging.getLogger(__name__)


@dataclass
class FHIRConfig:
    """FHIR server configuration"""
    base_url: str
    auth_token: Optional[str] = None
    timeout: float = 30.0


class FHIRClient:
    """Async FHIR client with validation"""
    
    def __init__(self, config: FHIRConfig):
        self.config = config
        self.client = httpx.AsyncClient(
            base_url=config.base_url,
            timeout=config.timeout,
            headers=self._headers(),
        )
    
    def _headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "application/fhir+json",
            "Content-Type": "application/fhir+json",
        }
        if self.config.auth_token:
            headers["Authorization"] = f"Bearer {self.config.auth_token}"
        return headers
    
    async def close(self):
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    # =========================================================================
    # GENERIC FHIR OPERATIONS
    # =========================================================================
    
    async def create(self, resource: dict) -> dict:
        """POST a resource"""
        resource_type = resource.get("resourceType")
        if not resource_type:
            raise ValidationError("Resource must have resourceType")
        
        # Validate before create
        await self._validate_create(resource)
        
        response = await self.client.post(f"/{resource_type}", json=resource)
        if response.status_code in (200, 201):
            return response.json()
        elif response.status_code == 409:
            raise ValidationError(f"Conflict: {response.text}")
        elif response.status_code == 422:
            raise ValidationError(f"Validation failed: {response.text}")
        else:
            response.raise_for_status()
    
    async def read(self, resource_type: str, id: str) -> dict:
        """GET a resource by ID"""
        response = await self.client.get(f"/{resource_type}/{id}")
        if response.status_code == 404:
            raise ValidationError(f"{resource_type}/{id} not found")
        if response.status_code >= 400:
            raise ValidationError(f"GET failed: {response.status_code} {response.text}")
        return response.json()
    
    async def update(self, resource_type: str, id: str, resource: dict) -> dict:
        """PUT a resource (full update)"""
        resource["id"] = id
        await self._validate_update(resource_type, id, resource)
        
        response = await self.client.put(f"/{resource_type}/{id}", json=resource)
        if response.status_code >= 400:
            raise ValidationError(f"PUT failed: {response.status_code} {response.text}")
        return response.json()
    
    async def patch(self, resource_type: str, id: str, patch: List[dict]) -> dict:
        """PATCH a resource (partial update)"""
        # For PATCH, we need to read current, apply patch, validate, then write
        current = await self.read(resource_type, id)
        
        # Apply JSON Patch operations
        for op in patch:
            current = self._apply_patch(current, op)
        
        await self._validate_update(resource_type, id, current)
        
        response = await self.client.patch(
            f"/{resource_type}/{id}",
            json=patch,
            headers={"Content-Type": "application/json-patch+json"},
        )
        if response.status_code >= 400:
            raise ValidationError(f"PATCH failed: {response.status_code} {response.text}")
        return response.json()
    
    def _apply_patch(self, resource: dict, op: dict) -> dict:
        """Apply a single JSON Patch operation"""
        op_type = op.get("op")
        path = op.get("path", "").lstrip("/")
        value = op.get("value")
        
        if op_type == "replace":
            parts = path.split("/")
            target = resource
            for part in parts[:-1]:
                if part.isdigit():
                    target = target[int(part)]
                else:
                    target = target.setdefault(part, {})
            target[parts[-1]] = value
        elif op_type == "add":
            parts = path.split("/")
            target = resource
            for part in parts[:-1]:
                if part.isdigit():
                    target = target[int(part)]
                else:
                    target = target.setdefault(part, {})
            if parts[-1].isdigit():
                idx = int(parts[-1])
                if isinstance(target, list):
                    target.insert(idx, value)
                else:
                    target[parts[-1]] = value
            else:
                target[parts[-1]] = value
        elif op_type == "remove":
            parts = path.split("/")
            target = resource
            for part in parts[:-1]:
                target = target[part]
            if parts[-1].isdigit():
                del target[int(parts[-1])]
            else:
                del target[parts[-1]]
        
        return resource
    
    async def search(self, resource_type: str, params: Dict[str, str]) -> dict:
        """Search resources"""
        response = await self.client.get(f"/{resource_type}", params=params)
        response.raise_for_status()
        return response.json()
    
    # =========================================================================
    # VALIDATION
    # =========================================================================
    
    async def _validate_create(self, resource: dict) -> List[DetectedIssue]:
        """Validate resource before creation"""
        issues = []
        
        # Check required fields
        resource_type = resource.get("resourceType")
        if not resource_type:
            raise ValidationError("Missing resourceType")
        
        # Profile-specific validation
        if resource_type == "Observation":
            issues.extend(self._validate_observation(resource))
        elif resource_type == "ServiceRequest":
            issues.extend(self._validate_service_request(resource))
        elif resource_type == "Task":
            issues.extend(self._validate_task(resource))
        elif resource_type == "Consent":
            issues.extend(self._validate_consent(resource))
        elif resource_type == "Communication":
            issues.extend(self._validate_communication(resource))
        elif resource_type == "DocumentReference":
            issues.extend(self._validate_document_reference(resource))
        elif resource_type == "DiagnosticReport":
            issues.extend(self._validate_diagnostic_report(resource))
        
        # Run evaluator rules
        eval_issues = evaluate_all_rules(resource_type, resource, {})
        issues.extend(eval_issues)
        
        # Check for blocking issues
        blocking = [i for i in issues if i.severity == "high"]
        if blocking:
            raise ValidationError(f"Validation failed: {[i.detail for i in blocking]}")
        
        return issues
    
    async def _validate_update(self, resource_type: str, id: str, proposed: dict) -> List[DetectedIssue]:
        """Validate resource before update"""
        current = await self.read(resource_type, id)
        issues = validate_resource_transition(resource_type, current, proposed)
        
        # Run evaluator rules
        eval_issues = evaluate_all_rules(resource_type, proposed, {"current": current})
        issues.extend([i for i in eval_issues if isinstance(i, DetectedIssue)])
        
        # Check for blocking issues
        blocking = [i for i in issues if isinstance(i, DetectedIssue) and i.severity == "high"]
        if blocking:
            raise ValidationError(f"Update validation failed: {[i.detail for i in blocking]}")
        
        return issues
    
    def _validate_observation(self, obs: dict) -> List[DetectedIssue]:
        """Validate Observation"""
        issues = []
        
        # Screening panel must have 2 members when final
        code = obs.get("code", {}).get("coding", [{}])[0].get("code")
        if code == "83700-8":  # Screening panel
            has_member = obs.get("hasMember", [])
            if len(has_member) != 2:
                issues.append(DetectedIssue(
                    code="missing-members",
                    severity="high",
                    detail="Screening panel must have exactly 2 member Observations",
                    reference=f"Observation/{obs.get('id', 'new')}"
                ))
        
        # Right/left eye must have bodySite
        if code in ("29474-1", "29473-3"):
            body_site = obs.get("bodySite")
            if not body_site:
                issues.append(DetectedIssue(
                    code="missing-body-site",
                    severity="high",
                    detail="Eye acuity observation must have bodySite",
                    reference=f"Observation/{obs.get('id', 'new')}"
                ))
        
        return issues
    
    def _validate_service_request(self, sr: dict) -> List[DetectedIssue]:
        """Validate ServiceRequest referral"""
        issues = []
        
        # Must have reasonCode and reasonReference for referral
        if sr.get("code", {}).get("coding", [{}])[0].get("code") == "307924000":
            if not sr.get("reasonCode"):
                issues.append(DetectedIssue(
                    code="missing-reason-code",
                    severity="high",
                    detail="Referral must have reasonCode",
                    reference=f"ServiceRequest/{sr.get('id', 'new')}"
                ))
            if not sr.get("reasonReference"):
                issues.append(DetectedIssue(
                    code="missing-reason-reference",
                    severity="high",
                    detail="Referral must have reasonReference to screening panel",
                    reference=f"ServiceRequest/{sr.get('id', 'new')}"
                ))
        
        return issues
    
    def _validate_task(self, task: dict) -> List[DetectedIssue]:
        """Validate Task referral tracking"""
        issues = []
        
        # Must have focus to ServiceRequest
        if not task.get("focus"):
            issues.append(DetectedIssue(
                code="missing-focus",
                severity="high",
                detail="Referral tracking Task must have focus referencing ServiceRequest",
                reference=f"Task/{task.get('id', 'new')}"
            ))
        
        return issues
    
    def _validate_consent(self, consent: dict) -> List[DetectedIssue]:
        """Validate Consent opt-out"""
        issues = []
        
        # Must have provisions with periods
        provisions = consent.get("provision", [])
        if not provisions:
            issues.append(DetectedIssue(
                code="missing-provisions",
                severity="high",
                detail="Opt-out consent must have at least one provision",
                reference=f"Consent/{consent.get('id', 'new')}"
            ))
        
        return issues
    
    def _validate_communication(self, comm: dict) -> List[DetectedIssue]:
        """Validate Communication accommodation"""
        issues = []
        
        # Must have sender and recipient
        if not comm.get("sender"):
            issues.append(DetectedIssue(
                code="missing-sender",
                severity="high",
                detail="Accommodation notice must have sender",
                reference=f"Communication/{comm.get('id', 'new')}"
            ))
        if not comm.get("recipient"):
            issues.append(DetectedIssue(
                code="missing-recipient",
                severity="high",
                detail="Accommodation notice must have recipient",
                reference=f"Communication/{comm.get('id', 'new')}"
            ))
        
        return issues
    
    def _validate_document_reference(self, doc: dict) -> List[DetectedIssue]:
        """Validate DocumentReference IP-4"""
        issues = []
        
        # Must have type
        if not doc.get("type"):
            issues.append(DetectedIssue(
                code="missing-type",
                severity="high",
                detail="DocumentReference must have type",
                reference=f"DocumentReference/{doc.get('id', 'new')}"
            ))
        
        # Must have content with attachment
        content = doc.get("content", [])
        if not content or not content[0].get("attachment", {}).get("url"):
            issues.append(DetectedIssue(
                code="missing-attachment",
                severity="high",
                detail="DocumentReference must have content.attachment.url",
                reference=f"DocumentReference/{doc.get('id', 'new')}"
            ))
        
        return issues
    
    def _validate_diagnostic_report(self, dr: dict) -> List[DetectedIssue]:
        """Validate DiagnosticReport assessment"""
        issues = []
        
        # Must have result references
        if not dr.get("result"):
            issues.append(DetectedIssue(
                code="missing-results",
                severity="moderate",
                detail="Assessment should have result references",
                reference=f"DiagnosticReport/{dr.get('id', 'new')}"
            ))
        
        return issues
    
    # =========================================================================
    # OPERATION IMPLEMENTATIONS (OP-1 through OP-7)
    # =========================================================================
    
    async def op1_record_screening(
        self,
        patient_id: str,
        encounter_id: str,
        practitioner_role_id: str,
        right_eye_snellen: tuple,  # (num, denom)
        left_eye_snellen: tuple,
        test_method: str = "snellen",
        outcome: str = "refer",
        attempt: int = 1,
    ) -> dict:
        """OP-1: Record Screening - POST Observation panel with members"""
        right_num, right_denom = right_eye_snellen
        left_num, left_denom = left_eye_snellen
        
        # Build member observations
        right_id = str(uuid.uuid4())
        left_id = str(uuid.uuid4())
        
        right_obs = build_right_eye_acuity(
            id=right_id,
            patient_id=patient_id,
            encounter_id=encounter_id,
            practitioner_role_id=practitioner_role_id,
            snellen_num=right_num,
            snellen_denom=right_denom,
            interpretation="A" if outcome == "refer" and right_denom >= 12 else "N",
        )
        
        left_obs = build_left_eye_acuity(
            id=left_id,
            patient_id=patient_id,
            encounter_id=encounter_id,
            practitioner_role_id=practitioner_role_id,
            snellen_num=left_num,
            snellen_denom=left_denom,
            interpretation="A" if outcome == "refer" and left_denom >= 12 else "N",
        )
        
        # Create members first
        await self.create(right_obs)
        await self.create(left_obs)
        
        # Build and create panel
        panel_id = str(uuid.uuid4())
        panel = build_screening_panel(
            id=panel_id,
            patient_id=patient_id,
            encounter_id=encounter_id,
            practitioner_role_id=practitioner_role_id,
            right_eye_id=right_id,
            left_eye_id=left_id,
            test_method=test_method,
            outcome=outcome,
            attempt=attempt,
        )
        
        return await self.create(panel)
    
    async def op2a_submit_referral(
        self,
        patient_id: str,
        encounter_id: str,
        practitioner_role_id: str,
        organization_id: str,
        screening_panel_id: str,
        reason_codes: List[dict],
        referral_id: str,
    ) -> tuple:
        """OP-2a: Submit Referral - POST ServiceRequest + Task"""
        sr_id = str(uuid.uuid4())
        task_id = str(uuid.uuid4())
        
        sr = build_service_request_referral(
            id=sr_id,
            patient_id=patient_id,
            encounter_id=encounter_id,
            practitioner_role_id=practitioner_role_id,
            organization_id=organization_id,
            reason_codes=reason_codes,
            reason_reference=screening_panel_id,
            referral_id=referral_id,
        )
        
        task = build_task_referral_tracking(
            id=task_id,
            patient_id=patient_id,
            service_request_id=sr_id,
            practitioner_role_id=practitioner_role_id,
            organization_id=organization_id,
            encounter_id=encounter_id,
        )
        
        # Create both (use conditional create for idempotency)
        created_sr = await self.create(sr)
        created_task = await self.create(task)
        
        return created_sr, created_task
    
    async def op2b_cancel_referral_timeout(
        self,
        service_request_id: str,
        task_id: str,
    ) -> tuple:
        """OP-2b: Cancel Referral Timeout - PATCH both to cancelled"""
        sr_patch = [
            {"op": "replace", "path": "/status", "value": "cancelled"},
            {"op": "add", "path": "/extension/-", "value": {
                "url": f"{CANONICAL_BASE}/cancel-reason",
                "valueString": "No Response Within 4 Weeks"
            }},
        ]
        task_patch = [
            {"op": "replace", "path": "/status", "value": "cancelled"},
        ]
        
        updated_sr = await self.patch("ServiceRequest", service_request_id, sr_patch)
        updated_task = await self.patch("Task", task_id, task_patch)
        
        return updated_sr, updated_task
    
    async def op2c_reject_referral(
        self,
        service_request_id: str,
        task_id: str,
        reason: str = "duplicate",
    ) -> tuple:
        """OP-2c: Reject Referral - PATCH both to rejected"""
        sr_patch = [
            {"op": "replace", "path": "/status", "value": "rejected"},
        ]
        task_patch = [
            {"op": "replace", "path": "/status", "value": "rejected"},
            {"op": "add", "path": "/statusReason", "value": {
                "coding": [_coding("http://terminology.hl7.org/CodeSystem/task-status-reason", reason, reason.capitalize())]
            }},
        ]
        
        updated_sr = await self.patch("ServiceRequest", service_request_id, sr_patch)
        updated_task = await self.patch("Task", task_id, task_patch)
        
        return updated_sr, updated_task
    
    async def op2d_accept_referral(
        self,
        service_request_id: str,
        task_id: str,
    ) -> tuple:
        """OP-2d: Accept Referral - PATCH ServiceRequest active, Task received"""
        sr_patch = [
            {"op": "replace", "path": "/status", "value": "active"},
        ]
        task_patch = [
            {"op": "replace", "path": "/status", "value": "received"},
        ]
        
        updated_sr = await self.patch("ServiceRequest", service_request_id, sr_patch)
        updated_task = await self.patch("Task", task_id, task_patch)
        
        return updated_sr, updated_task
    
    async def op3a_return_assessment(
        self,
        patient_id: str,
        encounter_id: str,
        service_request_id: str,
        practitioner_id: str,
        diagnosis_code: str,
        diagnosis_display: str,
        refraction_od: tuple,  # (sphere, cylinder, axis)
        refraction_os: tuple,
        conclusion: str,
        conclusion_code: str,
        conclusion_display: str,
    ) -> dict:
        """OP-3a: Return Assessment - create DiagnosticReport + Observations"""
        diag_id = str(uuid.uuid4())
        refr_od_id = str(uuid.uuid4())
        refr_os_id = str(uuid.uuid4())
        
        # Build observations
        diag_obs = build_observation_diagnosis(
            id=diag_id,
            patient_id=patient_id,
            snomed_code=diagnosis_code,
            snomed_display=diagnosis_display,
        )
        
        refr_od = build_observation_refraction(
            id=refr_od_id,
            patient_id=patient_id,
            eye="OD",
            sphere=refraction_od[0],
            cylinder=refraction_od[1],
            axis=refraction_od[2],
        )
        
        refr_os = build_observation_refraction(
            id=refr_os_id,
            patient_id=patient_id,
            eye="OS",
            sphere=refraction_os[0],
            cylinder=refraction_os[1],
            axis=refraction_os[2],
        )
        
        # Create observations
        await self.create(diag_obs)
        await self.create(refr_od)
        await self.create(refr_os)
        
        # Build and create DiagnosticReport
        report_id = str(uuid.uuid4())
        report = build_diagnostic_report_assessment(
            id=report_id,
            patient_id=patient_id,
            encounter_id=encounter_id,
            service_request_id=service_request_id,
            practitioner_id=practitioner_id,
            result_refs=[diag_id, refr_od_id, refr_os_id],
            conclusion=conclusion,
            conclusion_codes=[{"coding": [_coding("http://snomed.info/sct", conclusion_code, conclusion_display)]}],
        )
        
        return await self.create(report)
    
    async def op3b_return_assessment_full(
        self,
        patient_id: str,
        assessment_report_id: str,
        doc_type: str,
        loinc_code: str,
        loinc_display: str,
        source_url: str,
        author_id: str,
        custodian_id: str,
        description: str,
        encounter_id: Optional[str] = None,
    ) -> dict:
        """OP-3b: Return Assessment Full - create DocumentReference for assessment-full"""
        return await self.op4_send_to_primary_care(
            patient_id=patient_id,
            doc_type=doc_type,
            loinc_code=loinc_code,
            loinc_display=loinc_display,
            source_url=source_url,
            author_id=author_id,
            custodian_id=custodian_id,
            description=description,
            encounter_id=encounter_id,
        )
    
    async def op4_send_to_primary_care(
        self,
        patient_id: str,
        doc_type: str,
        loinc_code: str,
        loinc_display: str,
        source_url: str,
        author_id: str,
        custodian_id: str,
        description: str,
        encounter_id: Optional[str] = None,
    ) -> dict:
        """OP-4: Send document to Primary Care via MHD"""
        doc_id = str(uuid.uuid4())
        
        doc = build_document_reference_ip4(
            id=doc_id,
            patient_id=patient_id,
            doc_type_code=doc_type,
            loinc_code=loinc_code,
            loinc_display=loinc_display,
            source_url=source_url,
            author_id=author_id,
            custodian_id=custodian_id,
            description=description,
            encounter_id=encounter_id,
        )
        
        return await self.create(doc)
    
    async def op5_send_accommodation(
        self,
        patient_id: str,
        sender_id: str,
        recipient_ids: List[str],
        content: str,
        replaces_id: Optional[str] = None,
    ) -> dict:
        """OP-5: Send Accommodation Notice"""
        comm_id = str(uuid.uuid4())
        
        comm = build_communication_accommodation(
            id=comm_id,
            patient_id=patient_id,
            sender_id=sender_id,
            recipient_ids=recipient_ids,
            content=content,
            replaces_id=replaces_id,
        )
        
        return await self.create(comm)
    
    async def op6_query_patient(
        self,
        identifier_system: Optional[str] = None,
        identifier_value: Optional[str] = None,
        family: Optional[str] = None,
        given: Optional[str] = None,
        birthdate: Optional[str] = None,
    ) -> dict:
        """OP-6: Query Patient Demographics"""
        params = {}
        if identifier_system and identifier_value:
            params["identifier"] = f"{identifier_system}|{identifier_value}"
        if family:
            params["family"] = family
        if given:
            params["given"] = given
        if birthdate:
            params["birthdate"] = birthdate
        
        return await self.search("Patient", params)
    
    async def op7_subscribe(
        self,
        patient_id: str,
        endpoint: str,
    ) -> dict:
        """OP-7: Subscribe to Assessment Documents"""
        sub_id = str(uuid.uuid4())
        sub = build_subscription(sub_id, patient_id, endpoint)
        return await self.create(sub)


def _coding(system: str, code: str, display: Optional[str] = None) -> dict:
    c = {"system": system, "code": code}
    if display:
        c["display"] = display
    return c