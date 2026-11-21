"""
Unit tests for builders.py - Resource Construction
"""

import pytest
from svs.builders import (
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


class TestPatientBuilder:
    def test_build_patient_minimal(self):
        patient = build_patient(
            id="pat-1",
            family="Gonzalez",
            given=["Maria", "Isabel"],
            birth_date="2018-03-15",
            gender="female",
            school_roll="SCL-2026-0042",
        )
        
        assert patient["resourceType"] == "Patient"
        assert patient["id"] == "pat-1"
        assert patient["meta"]["profile"] == [PROFILES["patient"]]
        assert patient["name"][0]["family"] == "Gonzalez"
        assert patient["name"][0]["given"] == ["Maria", "Isabel"]
        assert patient["birthDate"] == "2018-03-15"
        assert patient["gender"] == "female"
        assert len(patient["identifier"]) == 1
        assert patient["identifier"][0]["value"] == "SCL-2026-0042"
    
    def test_build_patient_with_optional(self):
        patient = build_patient(
            id="pat-1",
            family="Gonzalez",
            given=["Maria"],
            birth_date="2018-03-15",
            gender="female",
            school_roll="SCL-2026-0042",
            national_id="NHS-1234567890",
            pixm_id="PIXM-987654321",
            address={"use": "home", "line": ["Calle Principal 123"], "city": "Madrid", "postalCode": "28001", "country": "ES"},
            phone="+34-91-555-0123",
            managing_org="org-1",
        )
        
        assert len(patient["identifier"]) == 3
        assert patient["identifier"][1]["value"] == "NHS-1234567890"
        assert patient["identifier"][2]["value"] == "PIXM-987654321"
        assert patient["address"][0]["city"] == "Madrid"
        assert patient["telecom"][0]["value"] == "+34-91-555-0123"
        assert patient["managingOrganization"]["reference"] == "Organization/org-1"


class TestRelatedPersonBuilder:
    def test_build_related_person(self):
        rp = build_related_person(
            id="rp-1",
            patient_id="pat-1",
            family="Gonzalez",
            given=["Ana", "Maria"],
            relationship_code="MTH",
            phone="+34-91-555-0123",
        )
        
        assert rp["resourceType"] == "RelatedPerson"
        assert rp["patient"]["reference"] == "Patient/pat-1"
        assert rp["relationship"][0]["coding"][0]["code"] == "MTH"
        assert rp["name"][0]["family"] == "Gonzalez"


class TestPractitionerBuilder:
    def test_build_practitioner(self):
        prac = build_practitioner(
            id="prac-1",
            family="Ruiz",
            given=["Carmen"],
            employee_id="EMP-2026-015",
            license_number="LIC-ENF-2026-004521",
            phone="+34-91-555-0100",
        )
        
        assert prac["resourceType"] == "Practitioner"
        assert len(prac["identifier"]) == 2
        assert prac["identifier"][0]["value"] == "EMP-2026-015"
        assert prac["identifier"][1]["value"] == "LIC-ENF-2026-004521"


class TestPractitionerRoleBuilder:
    def test_build_practitioner_role(self):
        pr = build_practitioner_role(
            id="pr-1",
            practitioner_id="prac-1",
            organization_id="org-1",
            role_code="school-nurse",
        )
        
        assert pr["resourceType"] == "PractitionerRole"
        assert pr["practitioner"]["reference"] == "Practitioner/prac-1"
        assert pr["organization"]["reference"] == "Organization/org-1"
        assert pr["code"][0]["coding"][0]["code"] == "school-nurse"


class TestOrganizationBuilder:
    def test_build_school(self):
        org = build_organization(
            id="org-1",
            name="Colegio Publico San Isidro",
            org_type="school",
            identifier="SCH-28079-01",
            phone="+34-91-555-0100",
        )
        
        assert org["resourceType"] == "Organization"
        assert org["type"][0]["coding"][0]["code"] == "edu"
    
    def test_build_clinic(self):
        org = build_organization(
            id="org-2",
            name="Clinica Oftalmologica",
            org_type="clinic",
            identifier="CLI-001",
        )
        assert org["type"][0]["coding"][0]["code"] == "prov"
    
    def test_build_primary_care(self):
        org = build_organization(
            id="org-3",
            name="Centro de Salud",
            org_type="primary-care",
            identifier="CS-001",
        )
        assert org["type"][0]["coding"][0]["code"] == "prov"
    
    def test_build_health_service(self):
        org = build_organization(
            id="org-4",
            name="Servicio Salud Escolar",
            org_type="health-service",
            identifier="HSE-001",
        )
        assert org["type"][0]["coding"][0]["code"] == "dept"


class TestEncounterBuilder:
    def test_build_encounter(self):
        enc = build_encounter(
            id="enc-1",
            patient_id="pat-1",
            practitioner_id="prac-1",
            org_id="org-1",
            start="2026-11-15T09:30:00Z",
            end="2026-11-15T09:45:00Z",
        )
        
        assert enc["resourceType"] == "Encounter"
        assert enc["status"] == "finished"
        assert enc["class"]["code"] == "AMB"
        assert enc["subject"]["reference"] == "Patient/pat-1"
        assert enc["participant"][0]["individual"]["reference"] == "Practitioner/prac-1"
        assert enc["period"]["start"] == "2026-11-15T09:30:00Z"


class TestScreeningBuilders:
    def test_build_right_eye_acuity(self):
        obs = build_right_eye_acuity(
            id="obs-od",
            patient_id="pat-1",
            encounter_id="enc-1",
            practitioner_role_id="pr-1",
            snellen_num=6,
            snellen_denom=12,
            interpretation="A",
        )
        
        assert obs["resourceType"] == "Observation"
        assert obs["meta"]["profile"] == [PROFILES["right_eye_acuity"]]
        assert obs["code"]["coding"][0]["code"] == "29474-1"
        assert obs["valueRatio"]["numerator"]["value"] == 6
        assert obs["valueRatio"]["denominator"]["value"] == 12
        assert obs["bodySite"]["coding"][0]["code"] == "363654007"
        assert obs["interpretation"][0]["coding"][0]["code"] == "A"
    
    def test_build_left_eye_acuity(self):
        obs = build_left_eye_acuity(
            id="obs-os",
            patient_id="pat-1",
            encounter_id="enc-1",
            practitioner_role_id="pr-1",
            snellen_num=6,
            snellen_denom=9,
            interpretation="N",
        )
        
        assert obs["code"]["coding"][0]["code"] == "29473-3"
        assert obs["bodySite"]["coding"][0]["code"] == "363655008"
        assert obs["interpretation"][0]["coding"][0]["code"] == "N"
    
    def test_build_screening_panel(self):
        panel = build_screening_panel(
            id="panel-1",
            patient_id="pat-1",
            encounter_id="enc-1",
            practitioner_role_id="pr-1",
            right_eye_id="obs-od",
            left_eye_id="obs-os",
            outcome="refer",
            attempt=1,
        )
        
        assert panel["resourceType"] == "Observation"
        assert panel["meta"]["profile"] == [PROFILES["screening_panel"]]
        assert panel["code"]["coding"][0]["code"] == "83700-8"
        assert len(panel["hasMember"]) == 2
        assert panel["hasMember"][0]["reference"] == "Observation/obs-od"
        assert panel["hasMember"][1]["reference"] == "Observation/obs-os"
        assert "Referral indicated: True" in panel["note"][0]["text"]


class TestReferralBuilders:
    def test_build_service_request_referral(self):
        sr = build_service_request_referral(
            id="sr-1",
            patient_id="pat-1",
            encounter_id="enc-1",
            practitioner_role_id="pr-1",
            organization_id="org-2",
            reason_codes=[{"system": "http://snomed.info/sct", "code": "416070007", "display": "Decreased visual acuity"}],
            reason_reference="panel-1",
            referral_id="REF-2026-11-15-0043",
            expected_deadline="2026-12-13T09:45:00Z",
        )
        
        assert sr["resourceType"] == "ServiceRequest"
        assert sr["meta"]["profile"] == [PROFILES["service_request_referral"]]
        assert sr["status"] == "active"
        assert sr["intent"] == "order"
        assert sr["code"]["coding"][0]["code"] == "307924000"
        assert len(sr["reasonCode"]) == 1
        assert sr["reasonReference"][0]["reference"] == "Observation/panel-1"
        assert sr["extension"][0]["valueDateTime"] == "2026-12-13T09:45:00Z"
    
    def test_build_task_referral_tracking(self):
        task = build_task_referral_tracking(
            id="task-1",
            patient_id="pat-1",
            service_request_id="sr-1",
            practitioner_role_id="pr-1",
            organization_id="org-2",
            encounter_id="enc-1",
        )
        
        assert task["resourceType"] == "Task"
        assert task["meta"]["profile"] == [PROFILES["task_referral_tracking"]]
        assert task["status"] == "requested"
        assert task["focus"]["reference"] == "ServiceRequest/sr-1"
        assert task["code"]["coding"][0]["code"] == "referral"


class TestAssessmentBuilders:
    def test_build_diagnostic_report_assessment(self):
        report = build_diagnostic_report_assessment(
            id="report-1",
            patient_id="pat-1",
            encounter_id="enc-1",
            service_request_id="sr-1",
            practitioner_id="prac-1",
            result_refs=["diag-1", "refr-od-1", "refr-os-1"],
            conclusion="Mild myopia OD",
            conclusion_codes=[{"coding": [{"system": "http://snomed.info/sct", "code": "373124007", "display": "Myopia"}]}],
        )
        
        assert report["resourceType"] == "DiagnosticReport"
        assert report["meta"]["profile"] == [PROFILES["diagnostic_report_assessment"]]
        assert report["category"][0]["coding"][0]["code"] == "OP"
        assert report["code"]["coding"][0]["code"] == "28626-8"
        assert len(report["result"]) == 3
    
    def test_build_observation_diagnosis(self):
        diag = build_observation_diagnosis(
            id="diag-1",
            patient_id="pat-1",
            snomed_code="373124007",
            snomed_display="Myopia",
            body_site_code="363654007",
        )
        
        assert diag["resourceType"] == "Observation"
        assert diag["meta"]["profile"] == [PROFILES["observation_diagnosis"]]
        assert diag["category"][0]["coding"][0]["code"] == "diagnosis"
        assert diag["code"]["coding"][0]["code"] == "373124007"
        assert diag["valueCodeableConcept"]["coding"][0]["code"] == "373124007"
    
    def test_build_observation_refraction(self):
        refr = build_observation_refraction(
            id="refr-od-1",
            patient_id="pat-1",
            eye="OD",
            sphere=-1.00,
            cylinder=-0.50,
            axis=90,
        )
        
        assert refr["resourceType"] == "Observation"
        assert refr["meta"]["profile"] == [PROFILES["observation_refraction_od"]]
        assert refr["valueQuantity"]["value"] == -1.00
        assert len(refr["component"]) == 2
    
    def test_build_care_plan_followup(self):
        cp = build_care_plan_followup(
            id="cp-1",
            patient_id="pat-1",
            encounter_id="enc-1",
            period_start="2026-11-22T10:30:00Z",
            period_end="2027-11-22T10:30:00Z",
            followup_code="373124007",
            followup_display="Myopia follow-up",
            description="Follow-up in 12 months",
        )
        
        assert cp["resourceType"] == "CarePlan"
        assert cp["meta"]["profile"] == [PROFILES["care_plan_followup"]]
        assert cp["intent"] == "plan"
        assert len(cp["activity"]) == 1


class TestAccommodationBuilder:
    def test_build_communication_accommodation(self):
        comm = build_communication_accommodation(
            id="comm-1",
            patient_id="pat-1",
            sender_id="pr-1",
            recipient_ids=["pr-teacher-1"],
            content="Student needs glasses and front seat",
            replaces_id=None,
        )
        
        assert comm["resourceType"] == "Communication"
        assert comm["meta"]["profile"] == [PROFILES["communication_accommodation"]]
        assert comm["status"] == "sent"
        assert comm["payload"][0]["contentString"] == "Student needs glasses and front seat"
    
    def test_build_with_supersession(self):
        comm = build_communication_accommodation(
            id="comm-2",
            patient_id="pat-1",
            sender_id="pr-1",
            recipient_ids=["pr-teacher-1"],
            content="Updated: student needs glasses",
            replaces_id="comm-1",
        )
        
        assert "relatesTo" in comm
        assert comm["relatesTo"][0]["code"] == "replaces"
        assert comm["relatesTo"][0]["target"]["reference"] == "Communication/comm-1"


class TestConsentBuilder:
    def test_build_consent_optout(self):
        consent = build_consent_optout(
            id="consent-1",
            patient_id="pat-1",
            practitioner_role_id="pr-1",
            organization_id="org-1",
            provisions=[
                {"type": "deny", "period": {"start": "2026-09-01", "end": "2026-11-10"}},
                {"type": "permit", "period": {"start": "2026-11-10", "end": "2026-06-30"}},
            ],
        )
        
        assert consent["resourceType"] == "Consent"
        assert consent["meta"]["profile"] == [PROFILES["consent_optout"]]
        assert consent["status"] == "active"
        assert consent["scope"]["coding"][0]["code"] == "screening"
        assert len(consent["provision"]) == 2


class TestDocumentReferenceBuilder:
    def test_build_document_reference_ip4(self):
        doc = build_document_reference_ip4(
            id="doc-1",
            patient_id="pat-1",
            doc_type_code="screening-pass",
            loinc_code="83700-8",
            loinc_display="Visual acuity screening panel",
            source_url="https://example.org/fhir/Observation/panel-1",
            author_id="pr-1",
            custodian_id="org-1",
            description="Screening pass result",
        )
        
        assert doc["resourceType"] == "DocumentReference"
        assert doc["meta"]["profile"] == [PROFILES["document_reference_ip4"]]
        assert doc["status"] == "current"
        assert doc["type"]["coding"][0]["code"] == "83700-8"
        assert doc["content"][0]["attachment"]["contentType"] == "application/fhir+json"
        assert doc["content"][0]["attachment"]["url"] == "https://example.org/fhir/Observation/panel-1"


class TestListBuilder:
    def test_build_list_primary_care(self):
        lst = build_list_primary_care(
            id="list-1",
            patient_id="pat-1",
            document_refs=["doc-1", "doc-2"],
        )
        
        assert lst["resourceType"] == "List"
        assert lst["meta"]["profile"] == [PROFILES["list_primary_care"]]
        assert lst["status"] == "current"
        assert lst["mode"] == "working"
        assert len(lst["entry"]) == 2


class TestSubscriptionBuilder:
    def test_build_subscription(self):
        sub = build_subscription(
            id="sub-1",
            patient_id="pat-1",
            endpoint="https://school.example.org/fhir",
        )
        
        assert sub["resourceType"] == "Subscription"
        assert sub["status"] == "requested"
        assert sub["channel"]["type"] == "rest-hook"
        assert sub["channel"]["endpoint"] == "https://school.example.org/fhir"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])