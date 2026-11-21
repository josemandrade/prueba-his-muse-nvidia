# Examples - v0.1.0

* [**Table of Contents**](toc.md)
* **Examples**

## Examples

### Examples

-------

#### Overview

This page provides synthetic examples for all profiles defined in this Implementation Guide. All examples use **synthetic data only** — no real patient data, identifiers, or clinical text.

Examples are available as JSON files in the `examples/` directory of the IG build output, and can be downloaded individually below.

-------

#### Patient (Child) Examples

##### SVSPatientExample (Maria Gonzalez)

**Profile:** `SVSPatient`
 **Scenario:** 8-year-old child in Grade 3, screened 2026-11-15

```
{
  "resourceType": "Patient",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-patient"]},
  "identifier": [
    {"system": "urn:oid:1.2.3.4.5.school-roll", "value": "SCL-2026-0042", "type": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v2-0203", "code": "SB"}]}},
    {"system": "http://terminology.hl7.org/CodeSystem/v2-0203", "value": "NHS-1234567890", "type": {"coding": [{"code": "NI"}]}, "use": "official"},
    {"system": "urn:ihe:pixm:cross-ref", "value": "PIXM-987654321", "type": {"coding": [{"code": "PIXM"}]}}
  ],
  "name": [{"use": "official", "family": "Gonzalez", "given": ["Maria", "Isabel"]}],
  "birthDate": "2018-03-15",
  "gender": "female",
  "address": [{"use": "home", "line": ["Calle Principal 123"], "city": "Madrid", "postalCode": "28001", "country": "ES"}],
  "telecom": [{"system": "phone", "value": "+34-91-555-0123", "use": "home"}],
  "managingOrganization": {"reference": "Organization/SVSOrganizationSchoolExample"},
  "extension": [
    {"url": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/grade-at-screening", "valueString": "Grade 3"},
    {"url": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/school-year", "valueString": "2026-2027"}
  ]
}

```

-------

#### RelatedPerson (Parent) Example

##### SVSRelatedPersonExample (Ana Gonzalez)

**Profile:** `SVSRelatedPerson`
 **Scenario:** Mother of Maria Gonzalez, opted in

```
{
  "resourceType": "RelatedPerson",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-related-person"]},
  "identifier": [{"system": "urn:oid:1.2.3.4.5.guardian", "value": "GRD-2026-0042"}],
  "patient": {"reference": "Patient/SCL-2026-0042"},
  "relationship": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v2-0131", "code": "MTH", "display": "Mother"}]}],
  "name": [{"use": "official", "family": "Gonzalez", "given": ["Ana", "Maria"]}],
  "telecom": [
    {"system": "phone", "value": "+34-91-555-0123", "use": "home"},
    {"system": "email", "value": "ana.gonzalez@email.es", "use": "home"}
  ],
  "communication": [{"preferred": true, "language": {"coding": [{"system": "urn:ietf:bcp:47", "code": "es"}]}}],
  "extension": [
    {"url": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/opt-out-status", "valueBoolean": false},
    {"url": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/opt-out-effective-from", "valueDateTime": "2026-09-01T00:00:00Z"}
  ]
}

```

-------

#### Practitioner / PractitionerRole Examples

##### School Nurse (Carmen Ruiz)

```
{
  "resourceType": "Practitioner",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-practitioner"]},
  "identifier": [
    {"system": "urn:oid:1.2.3.4.5.employee", "value": "EMP-2026-015"},
    {"system": "urn:oid:1.2.3.4.5.license", "value": "LIC-ENF-2026-004521", "type": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v2-0203", "code": "PRN"}]}}
  ],
  "name": [{"use": "official", "family": "Ruiz", "given": ["Carmen"]}],
  "telecom": [
    {"system": "phone", "value": "+34-91-555-0100", "use": "work"},
    {"system": "email", "value": "carmen.ruiz@salud-escolar.es", "use": "work"}
  ]
}

```

##### School Nurse Role

```
{
  "resourceType": "PractitionerRole",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-practitioner-role"]},
  "practitioner": {"reference": "Practitioner/SVSPractitionerNurseExample"},
  "organization": {"reference": "Organization/SVSOrganizationSchoolExample"},
  "code": [{"coding": [{"system": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-practitioner-role", "code": "school-nurse", "display": "School Nurse"}]}],
  "specialty": [{"coding": [{"system": "http://snomed.info/sct", "code": "408480009", "display": "School nursing"}]}],
  "location": [{"reference": "Location/SVSLocationSchoolExample"}],
  "telecom": [{"system": "phone", "value": "+34-91-555-0100", "use": "work"}],
  "extension": [{"url": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/escalation-contact", "valueReference": {"reference": "PractitionerRole/SVSPractitionerRoleServiceLeadExample"}}]
}

```

##### Ophthalmologist (Dr. Javier Morales)

```
{
  "resourceType": "Practitioner",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-practitioner"]},
  "identifier": [
    {"system": "urn:oid:1.2.3.4.5.employee", "value": "EMP-OPT-2026-008"},
    {"system": "urn:oid:1.2.3.4.5.license", "value": "LIC-MED-2026-001234", "type": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v2-0203", "code": "PRN"}]}}
  ],
  "name": [{"use": "official", "family": "Morales", "given": ["Javier"], "prefix": ["Dr."]}],
  "telecom": [
    {"system": "phone", "value": "+34-91-444-0200", "use": "work"},
    {"system": "email", "value": "j.morales@clinica-oftalmologica.es", "use": "work"}
  ]
}

```

-------

#### ScreeningEvent Examples

##### Pass Result (Maria Gonzalez)

```
{
  "resourceType": "Observation",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-screening-panel"]},
  "identifier": [{"system": "urn:oid:1.2.3.4.5.screening-event", "value": "SCR-2026-11-15-0042"}],
  "status": "final",
  "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "vital-signs"}]}],
  "code": {"coding": [{"system": "http://loinc.org", "code": "83700-8", "display": "Visual acuity screening panel"}]},
  "subject": {"reference": "Patient/SCL-2026-0042"},
  "encounter": {"reference": "Encounter/SVSEncounterScreeningExample"},
  "effectiveDateTime": "2026-11-15T09:35:00Z",
  "performer": [{"reference": "PractitionerRole/SVSPractitionerRoleNurseExample"}],
  "hasMember": [
    {"reference": "Observation/ACU-OD-2026-11-15-0042"},
    {"reference": "Observation/ACU-OS-2026-11-15-0042"}
  ],
  "note": [{"text": "Test used: Snellen 6m; Outcome: Pass; Attempt: 1; Referral indicated: false; Acuity diff ≥2 lines: false"}]
}

```

##### Right Eye Acuity (Pass: 6/9)

```
{
  "resourceType": "Observation",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-right-eye-acuity"]},
  "identifier": [{"system": "urn:oid:1.2.3.4.5.acuity", "value": "ACU-OD-2026-11-15-0042"}],
  "status": "final",
  "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "vital-signs"}]}],
  "code": {"coding": [{"system": "http://loinc.org", "code": "29474-1", "display": "Visual acuity right eye"}]},
  "subject": {"reference": "Patient/SCL-2026-0042"},
  "effectiveDateTime": "2026-11-15T09:35:00Z",
  "valueRatio": {
    "numerator": {"value": 6, "unit": "m", "system": "http://unitsofmeasure.org", "code": "m"},
    "denominator": {"value": 9, "unit": "m", "system": "http://unitsofmeasure.org", "code": "m"}
  },
  "bodySite": {"coding": [{"system": "http://snomed.info/sct", "code": "363654007", "display": "Right eye"}]},
  "interpretation": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation", "code": "N", "display": "Normal"}]}],
  "note": [{"text": "Test: Snellen 6m"}]
}

```

##### Refer Result (Right eye 6/12, Left eye 6/9)

```
{
  "resourceType": "Observation",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-screening-panel"]},
  "identifier": [{"system": "urn:oid:1.2.3.4.5.screening-event", "value": "SCR-2026-11-15-0043"}],
  "status": "final",
  "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "vital-signs"}]}],
  "code": {"coding": [{"system": "http://loinc.org", "code": "83700-8", "display": "Visual acuity screening panel"}]},
  "subject": {"reference": "Patient/SCL-2026-0042"},
  "encounter": {"reference": "Encounter/SVSEncounterScreeningExample"},
  "effectiveDateTime": "2026-11-15T09:35:00Z",
  "performer": [{"reference": "PractitionerRole/SVSPractitionerRoleNurseExample"}],
  "hasMember": [
    {"reference": "Observation/ACU-OD-2026-11-15-0043"},
    {"reference": "Observation/ACU-OS-2026-11-15-0043"}
  ],
  "note": [{"text": "Test used: Snellen 6m; Outcome: Refer; Attempt: 1; Referral indicated: true; Acuity diff ≥2 lines: false"}]
}

```

##### Right Eye Acuity (Refer: 6/12)

```
{
  "resourceType": "Observation",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-right-eye-acuity"]},
  "identifier": [{"system": "urn:oid:1.2.3.4.5.acuity", "value": "ACU-OD-2026-11-15-0043"}],
  "status": "final",
  "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "vital-signs"}]}],
  "code": {"coding": [{"system": "http://loinc.org", "code": "29474-1", "display": "Visual acuity right eye"}]},
  "subject": {"reference": "Patient/SCL-2026-0042"},
  "effectiveDateTime": "2026-11-15T09:35:00Z",
  "valueRatio": {
    "numerator": {"value": 6, "unit": "m", "system": "http://unitsofmeasure.org", "code": "m"},
    "denominator": {"value": 12, "unit": "m", "system": "http://unitsofmeasure.org", "code": "m"}
  },
  "bodySite": {"coding": [{"system": "http://snomed.info/sct", "code": "363654007", "display": "Right eye"}]},
  "interpretation": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation", "code": "A", "display": "Abnormal"}]}],
  "note": [{"text": "Test: Snellen 6m; Referral threshold: ≤6/12"}]
}

```

-------

#### Referral Examples

##### ServiceRequest Referral

```
{
  "resourceType": "ServiceRequest",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-service-request-referral"]},
  "identifier": [
    {"system": "urn:oid:1.2.3.4.5.referral", "value": "REF-2026-11-15-0043"},
    {"system": "urn:ihe:pcc:360x:referral-id", "value": "360X-REF-2026-11-15-0043"}
  ],
  "status": "active",
  "intent": "order",
  "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/service-request-category", "code": "referral"}]}],
  "priority": "routine",
  "code": {"coding": [{"system": "http://snomed.info/sct", "code": "307924000", "display": "Referral to ophthalmologist"}]},
  "subject": {"reference": "Patient/SCL-2026-0042"},
  "encounter": {"reference": "Encounter/SVSEncounterScreeningExample"},
  "occurrenceDateTime": "2026-11-15T09:45:00Z",
  "authoredOn": "2026-11-15T09:45:00Z",
  "requester": {"reference": "PractitionerRole/SVSPractitionerRoleNurseExample"},
  "performer": [{"reference": "Organization/SVSOrganizationClinicExample"}],
  "reasonCode": [{"coding": [{"system": "http://snomed.info/sct", "code": "416070007", "display": "Decreased visual acuity"}]}],
  "reasonReference": [{"reference": "Observation/SCR-2026-11-15-0043"}],
  "note": [{"text": "Referral reason: acuity OD 6/12 (≤6/12) / OS 6/9; test: Snellen 6m; screener: Carmen Ruiz"}],
  "extension": [
    {"url": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/expected-deadline", "valueDateTime": "2026-12-13T09:45:00Z"},
    {"url": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/parent-decision", "valueCodeableConcept": {"coding": [{"system": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/parent-decision", "code": "accept", "display": "Accept"}]}}
  ]
}

```

##### Task Referral Tracking

```
{
  "resourceType": "Task",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-task-referral-tracking"]},
  "identifier": [{"system": "urn:oid:1.2.3.4.5.referral-task", "value": "TASK-REF-2026-11-15-0043"}],
  "status": "requested",
  "intent": "order",
  "code": {"coding": [{"system": "http://hl7.org/fhir/CodeSystem/task-code", "code": "referral", "display": "Referral tracking"}]},
  "for": {"reference": "Patient/SCL-2026-0042"},
  "encounter": {"reference": "Encounter/SVSEncounterScreeningExample"},
  "authoredOn": "2026-11-15T09:45:00Z",
  "lastModified": "2026-11-15T09:45:00Z",
  "requester": {"reference": "PractitionerRole/SVSPractitionerRoleNurseExample"},
  "owner": {"reference": "Organization/SVSOrganizationClinicExample"},
  "focus": {"reference": "ServiceRequest/REF-2026-11-15-0043"},
  "restriction": {"period": {"end": "2026-12-13T09:45:00Z"}},
  "input": [{"type": {"coding": [{"system": "http://hl7.org/fhir/CodeSystem/task-code", "code": "referral-detail"}]}, "valueReference": {"reference": "ServiceRequest/REF-2026-11-15-0043"}}]
}

```

-------

#### Assessment Examples

##### DiagnosticReport (Assessment)

```
{
  "resourceType": "DiagnosticReport",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-diagnostic-report-assessment"]},
  "identifier": [{"system": "urn:oid:1.2.3.4.5.assessment", "value": "ASM-2026-11-22-0043"}],
  "status": "final",
  "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v2-0074", "code": "OP", "display": "Ophthalmology"}]}],
  "code": {"coding": [{"system": "http://loinc.org", "code": "28626-8", "display": "Ophthalmology study"}]},
  "subject": {"reference": "Patient/SCL-2026-0042"},
  "encounter": {"reference": "Encounter/SVSEncounterAssessmentExample"},
  "effectiveDateTime": "2026-11-22T10:30:00Z",
  "issued": "2026-11-22T11:00:00Z",
  "performer": [{"reference": "Practitioner/SVSPractitionerOphthalmologistExample"}],
  "resultsInterpreter": [{"reference": "Practitioner/SVSPractitionerOphthalmologistExample"}],
  "basedOn": [{"reference": "ServiceRequest/REF-2026-11-15-0043"}],
  "result": [
    {"reference": "Observation/DIAG-2026-11-22-0043"},
    {"reference": "Observation/REFR-OD-2026-11-22-0043"},
    {"reference": "Observation/REFR-OS-2026-11-22-0043"}
  ],
  "conclusion": "Mild myopia OD. Prescription: -1.00 DS OD. Follow-up: 12 months.",
  "conclusionCode": [{"coding": [{"system": "http://snomed.info/sct", "code": "373124007", "display": "Myopia"}]}]
}

```

##### Diagnosis Observation (Myopia OD)

```
{
  "resourceType": "Observation",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-diagnosis"]},
  "identifier": [{"system": "urn:oid:1.2.3.4.5.diagnosis", "value": "DIAG-2026-11-22-0043"}],
  "status": "final",
  "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "diagnosis"}]}],
  "code": {"coding": [{"system": "http://snomed.info/sct", "code": "373124007", "display": "Myopia"}]},
  "subject": {"reference": "Patient/SCL-2026-0042"},
  "effectiveDateTime": "2026-11-22T10:30:00Z",
  "valueCodeableConcept": {"coding": [{"system": "http://snomed.info/sct", "code": "373124007", "display": "Myopia"}]},
  "bodySite": {"coding": [{"system": "http://snomed.info/sct", "code": "363654007", "display": "Right eye"}]}
}

```

##### Refraction OD (-1.00 DS)

```
{
  "resourceType": "Observation",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-refraction-od"]},
  "identifier": [{"system": "urn:oid:1.2.3.4.5.refraction", "value": "REFR-OD-2026-11-22-0043"}],
  "status": "final",
  "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "exam"}]}],
  "code": {"coding": [{"system": "http://loinc.org", "code": "29474-1", "display": "Visual acuity right eye"}]},
  "subject": {"reference": "Patient/SCL-2026-0042"},
  "effectiveDateTime": "2026-11-22T10:30:00Z",
  "valueQuantity": {"value": -1.00, "unit": "D", "system": "http://unitsofmeasure.org", "code": "D"},
  "bodySite": {"coding": [{"system": "http://snomed.info/sct", "code": "363654007", "display": "Right eye"}]},
  "component": [
    {"code": {"coding": [{"system": "http://loinc.org", "code": "29468-3", "display": "Sphere"}]}, "valueQuantity": {"value": -1.00, "unit": "D", "system": "http://unitsofmeasure.org", "code": "D"}},
    {"code": {"coding": [{"system": "http://loinc.org", "code": "29469-1", "display": "Cylinder"}]}, "valueQuantity": {"value": 0.00, "unit": "D", "system": "http://unitsofmeasure.org", "code": "D"}},
    {"code": {"coding": [{"system": "http://loinc.org", "code": "29470-9", "display": "Axis"}]}, "valueQuantity": {"value": 0, "unit": "deg", "system": "http://unitsofmeasure.org", "code": "deg"}}
  ]
}

```

##### CarePlan (Follow-up)

```
{
  "resourceType": "CarePlan",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-care-plan-follow-up"]},
  "identifier": [{"system": "urn:oid:1.2.3.4.5.care-plan", "value": "CP-2026-11-22-0043"}],
  "status": "active",
  "intent": "plan",
  "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/careplan-category", "code": "assess-plan"}]}],
  "subject": {"reference": "Patient/SCL-2026-0042"},
  "encounter": {"reference": "Encounter/SVSEncounterAssessmentExample"},
  "period": {"start": "2026-11-22T10:30:00Z", "end": "2027-11-22T10:30:00Z"},
  "activity": [
    {
      "detail": {
        "kind": "ServiceRequest",
        "code": {"coding": [{"system": "http://snomed.info/sct", "code": "373124007", "display": "Myopia follow-up"}]},
        "scheduledPeriod": {"start": "2027-11-22T10:30:00Z", "end": "2027-11-22T10:30:00Z"},
        "status": "not-started",
        "description": "Follow-up in 12 months for myopia monitoring"
      }
    }
  ]
}

```

-------

#### Accommodation Notice Example

```
{
  "resourceType": "Communication",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-communication-accommodation"]},
  "identifier": [{"system": "urn:oid:1.2.3.4.5.accommodation", "value": "ACC-2026-11-22-0043"}],
  "status": "sent",
  "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/communication-category", "code": "instruction"}]}],
  "subject": {"reference": "Patient/SCL-2026-0042"},
  "sender": {"reference": "PractitionerRole/SVSPractitionerRoleNurseExample"},
  "recipient": [{"reference": "PractitionerRole/SVSPractitionerRoleTeacherExample"}],
  "sent": "2026-11-22T14:00:00Z",
  "payload": [{"contentString": "Accommodation needed: glasses, front seat. Detail: mild myopia OD, glasses prescribed. Valid until end of school year."}],
  "note": [{"text": "Based on ophthalmology assessment ASM-2026-11-22-0043. Supersedes notice ACC-2026-11-22-0042 if applicable."}],
  "extension": [
    {"url": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/accommodation-type", "valueCodeableConcept": {"coding": [{"system": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-accommodation-type", "code": "both", "display": "Glasses and front seat"}]}},
    {"url": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/valid-until", "valueDate": "2027-06-30"},
    {"url": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/assessment-reference", "valueReference": {"reference": "DiagnosticReport/ASM-2026-11-22-0043"}}
  ]
}

```

-------

#### Opt-Out Consent Examples

##### Opted In (Permit)

```
{
  "resourceType": "Consent",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-consent-opt-out"]},
  "identifier": [{"system": "urn:oid:1.2.3.4.5.optout-consent", "value": "OPT-2026-0042"}],
  "status": "active",
  "scope": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/consentscope", "code": "screening"}]},
  "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/consentcategorycodes", "code": "DENY"}]}],
  "patient": {"reference": "Patient/SCL-2026-0042"},
  "dateTime": "2026-09-01T00:00:00Z",
  "performer": [{"reference": "PractitionerRole/SVSPractitionerRoleAdminExample"}],
  "organization": [{"reference": "Organization/SVSOrganizationSchoolHealthServiceExample"}],
  "provision": [
    {"type": "permit", "period": {"start": "2026-09-01T00:00:00Z", "end": "2027-06-30T23:59:59Z"}, "action": [{"coding": [{"system": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/consent-action", "code": "vision-screening"}]}]}
  ]
}

```

##### Opted Out Then Opted Back In (StatusHistory)

```
{
  "resourceType": "Consent",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-consent-opt-out"]},
  "identifier": [{"system": "urn:oid:1.2.3.4.5.optout-consent", "value": "OPT-2026-0043"}],
  "status": "active",
  "scope": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/consentscope", "code": "screening"}]},
  "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/consentcategorycodes", "code": "DENY"}]}],
  "patient": {"reference": "Patient/SCL-2026-0043"},
  "dateTime": "2026-09-01T00:00:00Z",
  "performer": [{"reference": "PractitionerRole/SVSPractitionerRoleAdminExample"}],
  "organization": [{"reference": "Organization/SVSOrganizationSchoolHealthServiceExample"}],
  "provision": [
    {"type": "deny", "period": {"start": "2026-09-01T00:00:00Z", "end": "2026-11-10T23:59:59Z"}, "action": [{"coding": [{"system": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/consent-action", "code": "vision-screening"}]}]},
    {"type": "permit", "period": {"start": "2026-11-10T10:00:00Z", "end": "2027-06-30T23:59:59Z"}, "action": [{"coding": [{"system": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/consent-action", "code": "vision-screening"}]}]}
  ]
}

```

-------

#### DocumentReference (IP-4) Examples

##### Screening Pass

```
{
  "resourceType": "DocumentReference",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-document-reference-ip4"]},
  "identifier": [{"system": "urn:oid:1.2.3.4.5.ip4-doc", "value": "DOC-IP4-2026-11-15-0042-pass"}],
  "status": "current",
  "type": {"coding": [{"system": "http://loinc.org", "code": "83700-8", "display": "Visual acuity screening panel"}]},
  "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/document-class", "code": "screening-report"}]}],
  "subject": {"reference": "Patient/PC-2026-001234"},
  "date": "2026-11-15T10:00:00Z",
  "author": [{"reference": "PractitionerRole/SVSPractitionerRoleNurseExample"}],
  "custodian": {"reference": "Organization/SVSOrganizationSchoolHealthServiceExample"},
  "description": "Vision screening pass result for Maria Gonzalez (6/9 both eyes)",
  "content": [{"attachment": {"contentType": "application/fhir+json", "url": "https://school-health.example.org/fhir/Observation/SCR-2026-11-15-0042"}, "format": {"system": "http://ihe.net/fhir/ihe.formatcode.fhir/CodeSystem/formatcode", "code": "application/fhir+json"}}],
  "context": {"encounter": [{"reference": "Encounter/SVSEncounterScreeningExample"}], "period": {"start": "2026-11-15T09:35:00Z", "end": "2026-11-15T09:35:00Z"}, "related": [{"reference": "Observation/SCR-2026-11-15-0042"}]}
}

```

##### Full Assessment

```
{
  "resourceType": "DocumentReference",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-document-reference-ip4"]},
  "identifier": [{"system": "urn:oid:1.2.3.4.5.ip4-doc", "value": "DOC-IP4-2026-11-22-0043-assessment"}],
  "status": "current",
  "type": {"coding": [{"system": "http://loinc.org", "code": "28626-8", "display": "Ophthalmology study"}]},
  "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/document-class", "code": "screening-report"}]}],
  "subject": {"reference": "Patient/PC-2026-001234"},
  "date": "2026-11-22T11:30:00Z",
  "author": [{"reference": "PractitionerRole/SVSPractitionerRoleOphthalmologistExample"}],
  "custodian": {"reference": "Organization/SVSOrganizationClinicExample"},
  "description": "Full ophthalmology assessment for Maria Gonzalez: mild myopia OD, -1.00 DS",
  "content": [{"attachment": {"contentType": "application/fhir+json", "url": "https://clinica-oftalmologica.example.org/fhir/DiagnosticReport/ASM-2026-11-22-0043"}, "format": {"system": "http://ihe.net/fhir/ihe.formatcode.fhir/CodeSystem/formatcode", "code": "application/fhir+json"}}],
  "context": {"encounter": [{"reference": "Encounter/SVSEncounterAssessmentExample"}], "period": {"start": "2026-11-22T10:00:00Z", "end": "2026-11-22T11:00:00Z"}, "related": [{"reference": "DiagnosticReport/ASM-2026-11-22-0043"}]}
}

```

##### DNA Closure (LOINC 11506-3)

```
{
  "resourceType": "DocumentReference",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-document-reference-ip4"]},
  "identifier": [{"system": "urn:oid:1.2.3.4.5.ip4-doc", "value": "DOC-IP4-2027-01-10-0043-dna"}],
  "status": "current",
  "type": {"coding": [{"system": "http://loinc.org", "code": "11506-3", "display": "Referral note"}]},
  "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/document-class", "code": "screening-report"}]}],
  "subject": {"reference": "Patient/PC-2026-001234"},
  "date": "2027-01-10T10:00:00Z",
  "author": [{"reference": "PractitionerRole/SVSPractitionerRoleNurseExample"}],
  "custodian": {"reference": "Organization/SVSOrganizationSchoolHealthServiceExample"},
  "description": "Referral closed: 2nd DNA for Maria Gonzalez (referral REF-2026-11-15-0043)",
  "content": [{"attachment": {"contentType": "application/fhir+json", "url": "https://school-health.example.org/fhir/Communication/ACC-2027-01-10-0043-dna"}, "format": {"system": "http://ihe.net/fhir/ihe.formatcode.fhir/CodeSystem/formatcode", "code": "application/fhir+json"}}],
  "context": {"related": [{"reference": "ServiceRequest/REF-2026-11-15-0043"}]}
}

```

-------

#### List (Primary Care Document Log)

```
{
  "resourceType": "List",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-list-primary-care-documents"]},
  "identifier": [{"system": "urn:oid:1.2.3.4.5.primary-care-docs", "value": "PC-2026-001234-documents"}],
  "status": "current",
  "mode": "working",
  "title": "School Vision Screening Documents for Maria Gonzalez",
  "subject": {"reference": "Patient/PC-2026-001234"},
  "entry": [
    {"item": {"reference": "DocumentReference/DOC-IP4-2026-11-15-0042-pass"}},
    {"item": {"reference": "DocumentReference/DOC-IP4-2026-11-22-0043-assessment"}}
  ]
}

```

-------

#### QuestionnaireResponse (Screening Form)

```
{
  "resourceType": "QuestionnaireResponse",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-questionnaire-response-screening"]},
  "identifier": [{"system": "urn:oid:1.2.3.4.5.screening-form", "value": "FORM-2026-11-15-0042"}],
  "status": "completed",
  "subject": {"reference": "Patient/SCL-2026-0042"},
  "encounter": {"reference": "Encounter/SVSEncounterScreeningExample"},
  "authored": "2026-11-15T09:35:00Z",
  "author": {"reference": "PractitionerRole/SVSPractitionerRoleNurseExample"},
  "item": [
    {"linkId": "test-used", "answer": [{"valueCoding": {"system": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-screening-test-method", "code": "snellen", "display": "Snellen 6m chart"}}]},
    {"linkId": "right-eye-acuity", "answer": [{"valueString": "6/12"}]},
    {"linkId": "left-eye-acuity", "answer": [{"valueString": "6/9"}]},
    {"linkId": "outcome", "answer": [{"valueCoding": {"system": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-screening-outcome", "code": "refer", "display": "Refer"}}]}
  ]
}

```

-------

#### Download All Examples

All examples are available as individual JSON files in the IG build output:

* `examples/` directory in the published IG
* Each example validates against its profile
* Bundle of all examples: `examples-bundle.json`

-------

#### Validation

All examples have been validated against their respective profiles using the FHIR Validator. Run validation locally:

```
sushi build
# Examples are validated during build

```

