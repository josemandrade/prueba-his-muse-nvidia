# Public Health & Consent - v0.1.0

* [**Table of Contents**](toc.md)
* **Public Health & Consent**

## Public Health & Consent

### Public Health, Consent & Data Governance

-------

#### Consent Model

##### Opt-Out Consent (Annual, Revocable)

The school vision screening program operates under an **opt-out consent model**:

* **At start of school year:** Parents/guardians are informed about the screening program and can decline participation for their child
* **Default:** Opted in (screening proceeds unless parent explicitly declines)
* **Revocable mid-year:** Parents can change their decision at any time during the school year
* **No signed consent per child:** Consent is recorded in the School Information System (SIS)
* **No legal mandate:** The program runs under the school health program; no statutory reporting requirement

##### Consent Representation (FHIR Consent)

The `SVSConsentOptOut` profile models consent using multiple `provision` entries to capture status history:

```
{
  "resourceType": "Consent",
  "status": "active",
  "scope": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/consentscope", "code": "screening"}]},
  "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/consentcategorycodes", "code": "DENY"}]}],
  "patient": {"reference": "Patient/SCL-2026-0042"},
  "provision": [
    {
      "type": "deny",
      "period": {"start": "2026-09-01T00:00:00Z", "end": "2026-11-10T23:59:59Z"},
      "action": [{"coding": [{"system": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/consent-action", "code": "vision-screening"}]}]
    },
    {
      "type": "permit",
      "period": {"start": "2026-11-10T10:00:00Z", "end": "2027-06-30T23:59:59Z"},
      "action": [{"coding": [{"system": "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/consent-action", "code": "vision-screening"}]}]
    }
  ]
}

```

##### Consent Check at Screening

At each screening encounter, the nurse checks the current consent status:

1. `GET Consent?patient=[child]&status=active`
1. Current status = latest`provision`by`period.start`
1. If`type=deny`→ record opt-out, no screening performed
1. If`type=permit`→ proceed with screening

-------

#### Data Governance

##### Data Ownership

| | | |
| :--- | :--- | :--- |
| Child demographics | School Information System (SIS) | School admin |
| Screening results | School Health Service | School nurse |
| Referral letters | School Health Service | School nurse |
| Ophthalmology assessments | Ophthalmology Clinic EHR | Ophthalmologist |
| Primary care records | Primary Care EHR | Primary care clinician |
| Opt-out consent | School Information System (SIS) | School admin |
| Accommodation notices | School Health Service | School nurse |

##### Data Retention

| | | |
| :--- | :--- | :--- |
| ScreeningEvent | School year + archive | Archived (read-only) |
| Referral | School year + archive | Archived with screening record |
| OphthalmologyAssessment | Per clinic policy (typically 10+ years) | Archived |
| PrimaryCareRecord | Per primary care policy (typically lifelong) | Retained in health record |
| OptOutConsent | School year + archive | Archived |
| AccommodationNotice | School year (valid until) | Expired → superseded/archived |
| Teacher notifications | School year | Discarded after school year |

**Single Retention Rule:** All school-held records (screening, referral, consent, accommodation) are retained for the school year, then archived together under school records policy. Clinic and primary care records follow their own institutional policies.

##### Data Access Controls

| | | | |
| :--- | :--- | :--- | :--- |
| School Nurse | ScreeningEvent, Referral, Consent, Communication | ScreeningEvent, Referral, Communication | No |
| School Admin | All school-held data | Consent, Demographics | No |
| Ophthalmologist | Referral, ScreeningEvent (read), Assessment | Assessment | No |
| Primary Care Clinician | All received documents | PrimaryCareRecord | No |
| Parent/Guardian | Own child's data (via portal/paper) | Consent (opt-out change) | No |
| Teacher | AccommodationNotice only | No | No |

##### Data Minimisation

* **Teachers** receive only `Communication` with accommodation type (glasses/front seat) — **never** acuity values, diagnosis, or screening details
* **Parents** receive screening outcome letter (pass/refer) or referral letter — no raw data
* **Primary Care** receives structured documents via MHD — only data relevant to health record
* **Ophthalmology** receives referral with screening data — minimum necessary for assessment

-------

#### Privacy & Security

##### Audit Trail (ATNA)

All FHIR interactions SHOULD be audited per **ATNA** (Audit Trail and Node Authentication):

* `POST`/`PATCH`/`DELETE` on any resource → audit event
* `GET` on sensitive resources (Consent, Patient) → audit event
* Audit events sent to central audit repository

##### Consistent Time (CT)

All systems SHOULD synchronize time via **CT** (Consistent Time) profile for accurate timestamps across organisations.

##### Encryption

* **In transit:** TLS 1.2+ for all FHIR REST interactions
* **At rest:** Encryption per organisational policy

##### De-identification

* **Synthetic data only** in examples, tests, and documentation
* **No real patient data** in this IG or its examples
* Production implementations MUST apply appropriate de-identification for analytics/research

-------

#### Legal Basis

| | | |
| :--- | :--- | :--- |
| General (no mandate) | School health program policy | Opt-out consent is the legal basis |
| GDPR (EU) | Art. 6(1)(e) public task / Art. 9(2)(h) healthcare | Opt-out = valid consent mechanism |
| HIPAA (US) | Treatment, Payment, Operations | School health = treatment |
| Other | Local education/health law | Verify locally |

##### Cross-Border Considerations

* This IG is **jurisdiction-agnostic** — demographic matching (name, DOB, address) is primary PIXm strategy
* National health ID is **optional** supplementary identifier
* No assumption of specific legal framework; implementers must map to local law

-------

#### Aggregate Reporting (Not in Scope)

This IG does **not** define aggregate/public health reporting (no mADX, no notifiable disease reporting). If needed in future:

* Would use **mADX** (QRPH-58/59) for aggregate reporting
* Small cell suppression required (threshold per jurisdiction)
* Jurisdiction rules for reporting destination

-------

#### Safety & Risk Mitigation

| | | | |
| :--- | :--- | :--- | :--- |
| Parent opts out but child needs screening | Low | Medium | Annual notification; teacher awareness; primary care follow-up |
| Referral lost (paper) | Medium | High | 360X electronic tracking; 4-week timeout; re-issue |
| Ophthalmology rejects referral | Low | Medium | 360X PCC-56 Reject; nurse corrects & resends or closes |
| Child DNA twice | Low | High | One re-referral offered; then close + primary care notify |
| Consent status stale | Low | Medium | Real-time Consent read at screening; statusHistory tracked |
| Teacher sees acuity values | Very Low | High | Communication payload only contains accommodation type; no clinical data |
| National ID unavailable | Medium | Low | Demographic matching primary; national ID optional supplement |

-------

#### Incident Response

| | |
| :--- | :--- |
| Data breach | Notify DPA within 72h (GDPR); follow organisational policy |
| Wrong patient in referral | Cancel referral (OP-2b); notify all parties; audit |
| Incorrect screening result | Amend Observation (status=amended); re-send to primary care |
| System downtime | Paper fallback; queue FHIR transactions for replay |

-------

#### Compliance Checklist

* Opt-out consent model documented
* Consent revocable mid-year
* Data retention periods defined
* Data ownership clear
* Access controls per role
* Data minimisation (teacher sees only accommodation)
* Audit trail (ATNA) referenced
* Encryption in transit/at rest
* No legal mandate assumed
* Jurisdiction-agnostic design
* Synthetic data only in examples
* No real patient data in IG

