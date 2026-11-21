# Operations - v0.1.0

* [**Table of Contents**](toc.md)
* **Operations**

## Operations

### Operations

-------

#### Operation Definitions

This page defines all operations (named interactions) for the School Vision Screening interoperability points. Each operation includes its FHIR interaction, IHE profile support, inputs, outputs, and worked examples.

-------

#### OP-1: Record Screening

**Description:** Nurse records screening result (Observation panel with two member Observations for right/left eye acuity)

**Interoperability Point:** IP-1

**FHIR Interaction:**

```
POST [base]/Observation

```

**Request Body:** `SVSObservationScreeningPanel` with `hasMember` → 2 member Observations (`SVSObservationRightEyeAcuity`, `SVSObservationLeftEyeAcuity`)

**Response:** `201 Created` with Location header pointing to the created panel Observation

**IHE Profile:** None applies (local capture)

**Example Request:**

```
{
  "resourceType": "Observation",
  "meta": {
    "profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-screening-panel"]
  },
  "status": "final",
  "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "vital-signs"}]}],
  "code": {"coding": [{"system": "http://loinc.org", "code": "83700-8", "display": "Visual acuity screening panel"}]},
  "subject": {"reference": "Patient/SCL-2026-0042"},
  "effectiveDateTime": "2026-11-15T09:35:00Z",
  "performer": [{"reference": "PractitionerRole/SVSPractitionerRoleNurseExample"}],
  "hasMember": [
    {"reference": "Observation/ACU-OD-2026-11-15-0043"},
    {"reference": "Observation/ACU-OS-2026-11-15-0043"}
  ],
  "note": [
    {"text": "Test used: Snellen 6m; Outcome: Refer; Attempt: 1; Referral indicated: true"}
  ]
}

```

**Error Handling:**

* `400 Bad Request` — Missing required fields (subject, code, hasMember)
* `422 Unprocessable Entity` — Invalid Ratio format, missing bodySite on members

-------

#### OP-2a: Submit Referral

**Description:** Nurse sends referral to Ophthalmology via 360X

**Interoperability Point:** IP-2a

**FHIR Interactions:**

```
POST [base]/ServiceRequest
POST [base]/Task

```

(Submitted as a Bundle or sequentially with Task.focus referencing ServiceRequest)

**Request Body:** `SVSServiceRequestReferral` + `SVSTaskReferralTracking`

**Response:** `201 Created` for both resources; ServiceRequest gets 360X Referral ID assigned by Recipient

**IHE Profile:** **360X PCC-55** Submit Referral

**Actors:** Referral Initiator (School) → Referral Recipient (Ophthalmology)

**Example ServiceRequest:**

```
{
  "resourceType": "ServiceRequest",
  "meta": {"profile": ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-service-request-referral"]},
  "identifier": [
    {"system": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/referral", "value": "REF-2026-11-15-0043"},
    {"system": "urn:ihe:pcc:360x:referral-id", "value": "360X-REF-2026-11-15-0043"}
  ],
  "status": "active",
  "intent": "order",
  "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/service-request-category", "code": "referral"}]}],
  "priority": "routine",
  "code": {"coding": [{"system": "http://snomed.info/sct", "code": "307924000", "display": "Referral to ophthalmologist"}]},
  "subject": {"reference": "Patient/SCL-2026-0042"},
  "occurrenceDateTime": "2026-11-15T09:45:00Z",
  "authoredOn": "2026-11-15T09:45:00Z",
  "requester": {"reference": "PractitionerRole/SVSPractitionerRoleNurseExample"},
  "performer": [{"reference": "Organization/SVSOrganizationClinicExample"}],
  "reasonCode": [{"coding": [{"system": "http://snomed.info/sct", "code": "416070007", "display": "Decreased visual acuity"}]}],
  "reasonReference": [{"reference": "Observation/SCR-2026-11-15-0043"}],
  "extension": [
    {"url": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/expected-deadline", "valueDateTime": "2026-12-13T09:45:00Z"}
  ]
}

```

**Error Handling:**

* `409 Conflict` — Duplicate referral for same screening event
* `422 Unprocessable Entity` — Missing required fields (subject, reasonCode, reasonReference)

-------

#### OP-2b: Cancel Referral (Timeout)

**Description:** System cancels referral after 4-week timeout (no response from Ophthalmology)

**Interoperability Point:** IP-2b

**FHIR Interactions:**

```
PATCH [base]/ServiceRequest/[id]
PATCH [base]/Task/[id]

```

**Request Body:**

```
[
  {"op": "replace", "path": "/status", "value": "cancelled"},
  {"op": "add", "path": "/extension", "value": {"url": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/cancel-reason", "valueString": "No Response Within 4 Weeks"}}
]

```

**Response:** `200 OK` for both resources

**IHE Profile:** **360X PCC-58** Close Referral

**Actors:** Referral Initiator (School) → Referral Recipient (Ophthalmology)

**Trigger:** Boundary timer event at 4 weeks (P4W) on "Wait for Assessment" task

-------

#### OP-2c: Reject Referral

**Description:** Ophthalmology rejects referral (wrong patient, not their specialty, duplicate)

**Interoperability Point:** IP-2c

**FHIR Interactions:**

```
PATCH [base]/ServiceRequest/[id]
PATCH [base]/Task/[id]

```

**Request Body:**

```
[
  {"op": "replace", "path": "/status", "value": "rejected"},
  {"op": "add", "path": "/statusReason", "value": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/task-status-reason", "code": "duplicate", "display": "Duplicate referral"}]}}
]

```

**Response:** `200 OK`

**IHE Profile:** **360X PCC-56** Reject Referral

**Actors:** Referral Recipient (Ophthalmology) → Referral Initiator (School)

-------

#### OP-2d: Accept Referral

**Description:** Ophthalmology accepts referral

**Interoperability Point:** IP-2a

**FHIR Interactions:**

```
PATCH [base]/ServiceRequest/[id]
PATCH [base]/Task/[id]

```

**Request Body:**

```
[
  {"op": "replace", "path": "/status", "value": "active"},
  {"op": "replace", "path": "/Task/status", "value": "received"}
]

```

**Response:** `200 OK`

**IHE Profile:** **360X PCC-56** Accept Referral

-------

#### OP-3a: Return Assessment Summary

**Description:** Ophthalmology sends assessment summary to School Nurse

**Interoperability Point:** IP-3a

**FHIR Interactions (Pull):**

```
GET [base]/DiagnosticReport/[id]?_include=DiagnosticReport:result

```

OR (Push):

```
POST [base]/DocumentReference

```

**Response:** `200 OK` DiagnosticReport + included Observations (pull) OR `201 Created` DocumentReference (push)

**IHE Profile:** **360X PCC-61** Retrieve Report (pull) **or** **MHD ITI-65** Provide Document Bundle (push)

**Actors:** Referral Recipient (Ophthalmology) → Referral Initiator (School)

-------

#### OP-3b: Return Assessment Full

**Description:** Ophthalmology sends full assessment to Primary Care

**Interoperability Point:** IP-3b

**FHIR Interaction:**

```
POST [base]/DocumentReference

```

**Request Body:** `SVSDocumentReferenceIP4` with `type` = LOINC 28626-8, `content.attachment.contentType` = application/fhir+json, `url` pointing to DiagnosticReport

**Response:** `201 Created` DocumentReference in Primary Care List

**IHE Profile:** **MHD ITI-65** Provide Document Bundle

**Actors:** Document Source (Ophthalmology) → Document Recipient (Primary Care)

-------

#### OP-4a-f: Send to Primary Care (6 Document Types)

**Description:** School/Ophthalmology sends screening/assessment documents to Primary Care via MHD

**Interoperability Point:** IP-4

**FHIR Interaction:**

```
POST [base]/DocumentReference

```

**Document Types & LOINC Codes:**

| | | | |
| :--- | :--- | :--- | :--- |
| OP-4a | screening-pass | 83700-8 | School |
| OP-4b | screening-decline | 83700-8 | School |
| OP-4c | referral-dna | 11506-3 | School |
| OP-4d | screening-missed | 83700-8 | School |
| OP-4e | referral-rejected | 11506-3 | School |
| OP-4f | end-of-year-missed | 83700-8 | School |
| OP-3b | assessment-full | 28626-8 | Ophthalmology |

**Request Body:** `SVSDocumentReferenceIP4` with appropriate `type`, `content.attachment.contentType=application/fhir+json`, `url` to source resource

**Response:** `201 Created` DocumentReference; Primary Care adds to `SVSListPrimaryCareDocuments`

**IHE Profile:** **MHD ITI-65** Provide Document Bundle

**Actors:** Document Source (School/Ophthalmology) → Document Recipient (Primary Care)

-------

#### OP-5: Send Accommodation Notice

**Description:** Nurse sends accommodation notice to Teacher

**Interoperability Point:** IP-5

**FHIR Interaction:**

```
POST [base]/Communication

```

**Request Body:** `SVSCommunicationAccommodation`

**Response:** `201 Created` Communication

**IHE Profile:** None applies (internal)

**Delivery:** Non-FHIR (paper, email, EHR message) — Communication records the event

-------

#### OP-6: Query Patient Demographics

**Description:** Nurse/Ophthalmologist look up child in MPI for patient matching

**Interoperability Points:** All IPs

**FHIR Interactions:**

```
GET [base]/Patient?identifier=[system]|[value]
GET [base]/Patient?family=[family]&given=[given]&birthdate=[YYYY-MM-DD]

```

**Response:** `200 OK` Bundle of Patient resources

**IHE Profiles:** **PIXm ITI-83** (cross-reference) / **PDQm ITI-78** (demographics query)

**Matching Strategy:** Demographic matching (name, DOB, address) primary; national ID supplementary when available

-------

#### OP-7: Subscribe to Assessment Documents

**Description:** Nurse/Primary Care subscribe for push notifications when assessments are available

**Interoperability Point:** IP-3

**FHIR Interaction:**

```
POST [base]/Subscription

```

**Request Body:**

```
{
  "resourceType": "Subscription",
  "status": "requested",
  "criteria": "DiagnosticReport?patient=Patient/123&category=OP",
  "channel": {
    "type": "rest-hook",
    "endpoint": "https://school-health.example.org/fhir",
    "payload": "application/fhir+json"
  }
}

```

**IHE Profile:** **DSUBm ITI-110** Subscribe / ITI-112 Notify (TI)

**Actors:** Document Subscriber (School/Primary Care) → Document Publisher (Ophthalmology)

-------

#### Operation Summary Table

| | | | | |
| :--- | :--- | :--- | :--- | :--- |
| OP-1 | Record Screening | `POST Observation` | None | IP-1 |
| OP-2a | Submit Referral | `POST ServiceRequest`+`POST Task` | **360X PCC-55** | IP-2a |
| OP-2b | Cancel Referral | `PATCH ServiceRequest`+`PATCH Task` | **360X PCC-58** | IP-2b |
| OP-2c | Reject Referral | `PATCH ServiceRequest`+`PATCH Task` | **360X PCC-56** | IP-2c |
| OP-2d | Accept Referral | `PATCH ServiceRequest`+`PATCH Task` | **360X PCC-56** | IP-2a |
| OP-3a | Return Summary | `GET DiagnosticReport`/`POST DocumentReference` | **360X PCC-61**/**MHD ITI-65** | IP-3a |
| OP-3b | Return Full | `POST DocumentReference` | **MHD ITI-65** | IP-3b |
| OP-4a-f | Send to Primary Care | `POST DocumentReference` | **MHD ITI-65** | IP-4 |
| OP-5 | Send Accommodation | `POST Communication` | None | IP-5 |
| OP-6 | Query Demographics | `GET Patient` | **PIXm ITI-83**/**PDQm ITI-78** | All |
| OP-7 | Subscribe | `POST Subscription` | **DSUBm ITI-110/112** | IP-3 |

-------

#### Error Handling Patterns

| | | |
| :--- | :--- | :--- |
| `200 OK` | Success (read/update) | Continue |
| `201 Created` | Resource created | Use Location header |
| `400 Bad Request` | Invalid request syntax | Fix request syntax |
| `401 Unauthorized` | Authentication required | Authenticate |
| `403 Forbidden` | Insufficient permissions | Check consent/role |
| `404 Not Found` | Resource not found | Verify identifier |
| `409 Conflict` | Duplicate/conflict | Use conditional create or check existing |
| `412 Precondition Failed` | Version mismatch | Re-read and retry |
| `422 Unprocessable Entity` | Semantic validation failed | Fix clinical data |
| `500 Internal Server Error` | Server error | Retry with exponential backoff |

-------

#### Conditional Create Pattern (for idempotency)

For operations that must be idempotent (e.g., Submit Referral):

```
POST [base]/ServiceRequest?identifier=REF-2026-11-15-0043
If-None-Exist: identifier=REF-2026-11-15-0043

```

* If resource with that identifier exists → `409 Conflict` with existing resource
* If not → `201 Created` with new resource

