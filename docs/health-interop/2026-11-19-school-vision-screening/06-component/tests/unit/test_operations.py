"""
Integration tests for OP-1 through OP-7 operations
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

from svs.client import FHIRClient, FHIRConfig
from svs.builders import (
    build_patient,
    build_practitioner,
    build_practitioner_role,
    build_organization,
    build_encounter,
)
from svs.transitions import ForbiddenTransitionError, ValidationError
from svs.evaluator import evaluate_all_rules


class MockResponse:
    """Mock httpx.Response for testing"""
    def __init__(self, status_code: int, json_data: dict = None, text: str = ""):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.text = text
    
    def json(self):
        return self._json_data
    
    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(f"{self.status_code}", request=None, response=self)


@pytest.fixture
def fhir_config():
    return FHIRConfig(base_url="https://fhir.example.org")


@pytest.fixture
def mock_client(fhir_config):
    """Create a client with mocked HTTP"""
    # Create client without initializing real httpx client
    client = object.__new__(FHIRClient)
    client.config = fhir_config
    client.client = AsyncMock(spec=httpx.AsyncClient)
    return client


class TestOP1RecordScreening:
    """OP-1: Record Screening"""
    
    @pytest.mark.asyncio
    async def test_record_screening_success(self, mock_client):
        """Test successful screening panel creation with 2 members"""
        # Setup mock responses for member observations and panel
        mock_client.client.post.side_effect = [
            AsyncMock(status_code=201, json=lambda: {"resourceType": "Observation", "id": "obs-od"}),
            AsyncMock(status_code=201, json=lambda: {"resourceType": "Observation", "id": "obs-os"}),
            AsyncMock(status_code=201, json=lambda: {"resourceType": "Observation", "id": "panel-1"}),
        ]
        
        result = await mock_client.op1_record_screening(
            patient_id="pat-1",
            encounter_id="enc-1",
            practitioner_role_id="pr-1",
            right_eye_snellen=(6, 12),
            left_eye_snellen=(6, 9),
            test_method="snellen",
            outcome="refer",
        )
        
        assert result["id"] == "panel-1"
        assert mock_client.client.post.call_count == 3
    
    @pytest.mark.asyncio
    async def test_record_screening_members_created_first(self, mock_client):
        """Verify members are created before panel"""
        mock_client.client.post.side_effect = [
            AsyncMock(status_code=201, json=lambda: {"resourceType": "Observation", "id": "obs-od"}),
            AsyncMock(status_code=201, json=lambda: {"resourceType": "Observation", "id": "obs-os"}),
            AsyncMock(status_code=201, json=lambda: {"resourceType": "Observation", "id": "panel-1"}),
        ]
        
        await mock_client.op1_record_screening(
            patient_id="pat-1",
            encounter_id="enc-1",
            practitioner_role_id="pr-1",
            right_eye_snellen=(6, 12),
            left_eye_snellen=(6, 9),
        )
        
        # First two calls should be for right and left eye
        calls = mock_client.client.post.call_args_list
        assert "right-eye-acuity" in str(calls[0]) or "29474-1" in str(calls[0])
        assert "left-eye-acuity" in str(calls[1]) or "29473-3" in str(calls[1])


class TestOP2Referral:
    """OP-2a through OP-2d: Referral workflow"""
    
    @pytest.mark.asyncio
    async def test_submit_referral(self, mock_client):
        """OP-2a: Submit Referral"""
        mock_client.client.post.side_effect = [
            AsyncMock(status_code=201, json=lambda: {"resourceType": "ServiceRequest", "id": "sr-1"}),
            AsyncMock(status_code=201, json=lambda: {"resourceType": "Task", "id": "task-1"}),
        ]
        
        sr, task = await mock_client.op2a_submit_referral(
            patient_id="pat-1",
            encounter_id="enc-1",
            practitioner_role_id="pr-1",
            organization_id="org-2",
            screening_panel_id="panel-1",
            reason_codes=[{"system": "http://snomed.info/sct", "code": "416070007", "display": "Decreased visual acuity"}],
            referral_id="REF-2026-11-15-0043",
        )
        
        assert sr["id"] == "sr-1"
        assert task["id"] == "task-1"
        assert mock_client.client.post.call_count == 2
    
    @pytest.mark.asyncio
    async def test_cancel_referral_timeout(self, mock_client):
        """OP-2b: Cancel Referral Timeout"""
        # Mock read to return current state (called twice per patch: once for SR, once for Task)
        mock_client.client.get.side_effect = [
            MockResponse(200, {"resourceType": "ServiceRequest", "id": "sr-1", "status": "active"}),
            MockResponse(200, {"resourceType": "Task", "id": "task-1", "status": "requested"}),
            MockResponse(200, {"resourceType": "ServiceRequest", "id": "sr-1", "status": "active"}),
            MockResponse(200, {"resourceType": "Task", "id": "task-1", "status": "requested"}),
        ]
        # Mock patch to return updated state
        mock_client.client.patch.side_effect = [
            MockResponse(200, {"resourceType": "ServiceRequest", "id": "sr-1", "status": "cancelled"}),
            MockResponse(200, {"resourceType": "Task", "id": "task-1", "status": "cancelled"}),
        ]
        
        sr, task = await mock_client.op2b_cancel_referral_timeout(
            service_request_id="sr-1",
            task_id="task-1",
        )
        
        assert sr["status"] == "cancelled"
        assert task["status"] == "cancelled"
    
    @pytest.mark.asyncio
    async def test_reject_referral(self, mock_client):
        """OP-2c: Reject Referral"""
        # Mock read to return current state (called twice per patch: once for SR, once for Task)
        mock_client.client.get.side_effect = [
            MockResponse(200, {"resourceType": "ServiceRequest", "id": "sr-1", "status": "active"}),
            MockResponse(200, {"resourceType": "Task", "id": "task-1", "status": "requested"}),
            MockResponse(200, {"resourceType": "ServiceRequest", "id": "sr-1", "status": "active"}),
            MockResponse(200, {"resourceType": "Task", "id": "task-1", "status": "requested"}),
        ]
        # Mock patch to return updated state
        mock_client.client.patch.side_effect = [
            MockResponse(200, {"resourceType": "ServiceRequest", "id": "sr-1", "status": "rejected"}),
            MockResponse(200, {"resourceType": "Task", "id": "task-1", "status": "rejected"}),
        ]
        
        sr, task = await mock_client.op2c_reject_referral(
            service_request_id="sr-1",
            task_id="task-1",
            reason="duplicate",
        )
        
        assert sr["status"] == "rejected"
        assert task["status"] == "rejected"
    
    @pytest.mark.asyncio
    async def test_accept_referral(self, mock_client):
        """OP-2d: Accept Referral"""
        # Mock read to return current state (called twice per patch: once for SR, once for Task)
        mock_client.client.get.side_effect = [
            MockResponse(200, {"resourceType": "ServiceRequest", "id": "sr-1", "status": "active"}),
            MockResponse(200, {"resourceType": "Task", "id": "task-1", "status": "requested"}),
            MockResponse(200, {"resourceType": "ServiceRequest", "id": "sr-1", "status": "active"}),
            MockResponse(200, {"resourceType": "Task", "id": "task-1", "status": "requested"}),
        ]
        # Mock patch to return updated state
        mock_client.client.patch.side_effect = [
            MockResponse(200, {"resourceType": "ServiceRequest", "id": "sr-1", "status": "active"}),
            MockResponse(200, {"resourceType": "Task", "id": "task-1", "status": "received"}),
        ]
        
        sr, task = await mock_client.op2d_accept_referral(
            service_request_id="sr-1",
            task_id="task-1",
        )
        
        assert sr["status"] == "active"
        assert task["status"] == "received"


class TestOP3Assessment:
    """OP-3a and OP-3b: Assessment return"""
    
    @pytest.mark.asyncio
    async def test_return_assessment_summary(self, mock_client):
        """OP-3a: Return Assessment Summary"""
        mock_client.client.post.side_effect = [
            AsyncMock(status_code=201, json=lambda: {"resourceType": "Observation", "id": "diag-1"}),
            AsyncMock(status_code=201, json=lambda: {"resourceType": "Observation", "id": "refr-od-1"}),
            AsyncMock(status_code=201, json=lambda: {"resourceType": "Observation", "id": "refr-os-1"}),
            AsyncMock(status_code=201, json=lambda: {"resourceType": "DiagnosticReport", "id": "report-1"}),
        ]
        
        report = await mock_client.op3a_return_assessment(
            patient_id="pat-1",
            encounter_id="enc-1",
            service_request_id="sr-1",
            practitioner_id="prac-1",
            diagnosis_code="373124007",
            diagnosis_display="Myopia",
            refraction_od=(-1.00, -0.50, 90),
            refraction_os=(0.00, 0.00, 0),
            conclusion="Mild myopia OD",
            conclusion_code="373124007",
            conclusion_display="Myopia",
        )
        
        assert report["id"] == "report-1"
        assert mock_client.client.post.call_count == 4
    
    @pytest.mark.asyncio
    async def test_return_assessment_full(self, mock_client):
        """OP-3b: Return Assessment Full (DocumentReference)"""
        mock_client.client.post.return_value = MockResponse(
            201, {"resourceType": "DocumentReference", "id": "doc-1"}
        )
        
        doc = await mock_client.op3b_return_assessment_full(
            patient_id="pat-1",
            assessment_report_id="report-1",
            doc_type="assessment-full",
            loinc_code="28626-8",
            loinc_display="Ophthalmology study",
            source_url="https://example.org/fhir/DiagnosticReport/report-1",
            author_id="pr-ophthalmologist",
            custodian_id="org-2",
            description="Full assessment",
        )
        
        assert doc["id"] == "doc-1"


class TestOP4PrimaryCare:
    """OP-4a-f: Send to Primary Care"""
    
    @pytest.mark.asyncio
    async def test_send_screening_pass(self, mock_client):
        """OP-4a: Screening Pass"""
        mock_client.client.post.return_value = MockResponse(
            201, {"resourceType": "DocumentReference", "id": "doc-1"}
        )
        
        doc = await mock_client.op4_send_to_primary_care(
            patient_id="pat-1",
            doc_type="screening-pass",
            loinc_code="83700-8",
            loinc_display="Visual acuity screening panel",
            source_url="https://example.org/fhir/Observation/panel-1",
            author_id="pr-school-1",
            custodian_id="org-1",
            description="Screening pass",
        )
        
        assert doc["id"] == "doc-1"
    
    @pytest.mark.asyncio
    async def test_send_assessment_full(self, mock_client):
        """OP-3b/OP-4: Assessment Full from Ophthalmology"""
        mock_client.client.post.return_value = AsyncMock(
            status_code=201,
            json=lambda: {"resourceType": "DocumentReference", "id": "doc-2"}
        )
        
        doc = await mock_client.op4_send_to_primary_care(
            patient_id="pat-1",
            doc_type="assessment-full",
            loinc_code="28626-8",
            loinc_display="Ophthalmology study",
            source_url="https://example.org/fhir/DiagnosticReport/report-1",
            author_id="pr-ophthalmologist",
            custodian_id="org-2",
            description="Full assessment",
        )
        
        assert doc["id"] == "doc-2"


class TestOP5Accommodation:
    """OP-5: Send Accommodation Notice"""
    
    @pytest.mark.asyncio
    async def test_send_accommodation(self, mock_client):
        mock_client.client.post.return_value = AsyncMock(
            status_code=201,
            json=lambda: {"resourceType": "Communication", "id": "comm-1"}
        )
        
        comm = await mock_client.op5_send_accommodation(
            patient_id="pat-1",
            sender_id="pr-1",
            recipient_ids=["pr-teacher-1"],
            content="Student needs glasses and front seat",
        )
        
        assert comm["id"] == "comm-1"
    
    @pytest.mark.asyncio
    async def test_send_accommodation_with_supersession(self, mock_client):
        # Mock _validate_create to provide context with existing notice
        original_validate = mock_client._validate_create
        
        async def mock_validate(resource):
            if resource.get("resourceType") == "Communication" and resource.get("relatesTo"):
                # Provide context with existing notice
                eval_issues = evaluate_all_rules(
                    "Communication", 
                    resource, 
                    {"existing_notices": [{"id": "comm-1", "status": "sent"}]}
                )
                blocking = [i for i in eval_issues if i.severity == "high"]
                if blocking:
                    raise ValidationError(f"Validation failed: {[i.detail for i in blocking]}")
            else:
                return await original_validate(resource)
        
        mock_client._validate_create = mock_validate
        
        mock_client.client.post.return_value = AsyncMock(
            status_code=201,
            json=lambda: {"resourceType": "Communication", "id": "comm-2", "relatesTo": [{"code": "replaces", "target": {"reference": "Communication/comm-1"}}]}
        )
        
        comm = await mock_client.op5_send_accommodation(
            patient_id="pat-1",
            sender_id="pr-1",
            recipient_ids=["pr-teacher-1"],
            content="Updated notice",
            replaces_id="comm-1",
        )
        
        assert comm["id"] == "comm-2"
        mock_client._validate_create = original_validate


class TestOP6Demographics:
    """OP-6: Query Patient Demographics"""
    
    @pytest.mark.asyncio
    async def test_query_by_identifier(self, mock_client):
        mock_client.client.get.return_value = MagicMock(
            status_code=200,
            json=lambda: {"resourceType": "Bundle", "entry": [{"resource": {"resourceType": "Patient", "id": "pat-1"}}]}
        )
        
        bundle = await mock_client.op6_query_patient(
            identifier_system="urn:oid:1.2.3.4.5.school-roll",
            identifier_value="SCL-2026-0042",
        )
        
        assert bundle["resourceType"] == "Bundle"
        mock_client.client.get.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_query_by_demographics(self, mock_client):
        mock_client.client.get.return_value = MagicMock(
            status_code=200,
            json=lambda: {"resourceType": "Bundle", "entry": []}
        )
        
        bundle = await mock_client.op6_query_patient(
            family="Gonzalez",
            given="Maria",
            birthdate="2018-03-15",
        )
        
        assert bundle["resourceType"] == "Bundle"


class TestOP7Subscription:
    """OP-7: Subscribe to Assessment Documents"""
    
    @pytest.mark.asyncio
    async def test_subscribe(self, mock_client):
        mock_client.client.post.return_value = AsyncMock(
            status_code=201,
            json=lambda: {
                "resourceType": "Subscription", 
                "id": "sub-1",
                "channel": {
                    "type": "rest-hook",
                    "endpoint": "https://school.example.org/fhir",
                    "payload": "application/fhir+json"
                }
            }
        )
        
        sub = await mock_client.op7_subscribe(
            patient_id="pat-1",
            endpoint="https://school.example.org/fhir",
        )
        
        assert sub["id"] == "sub-1"
        assert sub["channel"]["endpoint"] == "https://school.example.org/fhir"


class TestValidationErrors:
    """Tests that validation errors are properly raised"""
    
    @pytest.mark.asyncio
    async def test_duplicate_referral_409(self, mock_client):
        """OP-2a should raise on 409 Conflict"""
        mock_client.client.post.return_value = AsyncMock(
            status_code=409,
            text="Duplicate referral"
        )
        
        with pytest.raises(ValidationError) as exc:
            await mock_client.op2a_submit_referral(
                patient_id="pat-1",
                encounter_id="enc-1",
                practitioner_role_id="pr-1",
                organization_id="org-2",
                screening_panel_id="panel-1",
                reason_codes=[{"code": "416070007"}],
                referral_id="REF-2026-11-15-0043",
            )
        assert "Conflict" in str(exc.value)
    
    @pytest.mark.asyncio
    async def test_invalid_transition_422(self, mock_client):
        """PATCH should raise on 422 for invalid transition"""
        # Create proper mock response objects
        class MockResponse:
            def __init__(self, status_code, json_data, text=""):
                self.status_code = status_code
                self._json_data = json_data
                self.text = text
            
            def json(self):
                return self._json_data
            
            def raise_for_status(self):
                if self.status_code >= 400:
                    raise httpx.HTTPStatusError(f"{self.status_code}", request=None, response=self)
        
        # Mock get to return cancelled ServiceRequest
        mock_client.client.get.return_value = MockResponse(
            200, 
            {"resourceType": "ServiceRequest", "id": "sr-1", "status": "cancelled"}
        )
        # Mock patch to return 422
        mock_client.client.patch.return_value = MockResponse(
            422, 
            {}, 
            "Cannot reactivate cancelled referral"
        )
        
        with pytest.raises(ValidationError) as exc:
            await mock_client.op2d_accept_referral(
                service_request_id="sr-1",
                task_id="task-1",
            )
        assert "reactivate" in str(exc.value).lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])