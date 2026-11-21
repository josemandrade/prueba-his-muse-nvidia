# IHE Profile Relationships

---

## Overview

This page documents the relationship between each interoperability point (IP) in this Implementation Guide and the relevant IHE profiles. For each IP, we assess whether an IHE profile applies (full, partial, or none), the actors and transactions involved, and any gaps or custom work required.

**Principle:** We offer IHE profile associations to the user; an unchosen association is documented as a relationship, not claimed as conformance.

---

## IHE Profile Assessment per Interoperability Point

### IP-1: Screening Result Capture (Nurse → School Record)

| Aspect | Assessment |
|--------|------------|
| **Candidate Profiles** | MHD, FHIR Observation, PIXm/PDQm |
| **Fit** | **Partial (MHD)** — MHD ITI-65 can store the Observation panel as a document, but MHD is for document sharing, not data entry. No IHE profile for school nurse screening data capture. |
| **Actors / Transactions** | Document Source (Nurse) → Document Recipient (School Repository) / ITI-65 |
| **Gaps / Custom Remaining** | Custom: screening form UI, validation rules, outcome derivation (Pass/Refer/Absent/Incomplete). PIXm/PDQm for patient lookup. |
| **Offer to User** | **Offer MHD** for document storage if school has repository; otherwise custom FHIR REST. |

---

### IP-2a: Referral Dispatch (School → Ophthalmology)

| Aspect | Assessment |
|--------|------------|
| **Candidate Profiles** | **360X** (primary), XBeR-WD, MHD, Scheduling, PIXm/PDQm |
| **Fit** | **Full (360X)** — Exactly matches closed-loop referral with tracking, accept/reject, cancel, report retrieval. |
| **Actors / Transactions** | Referral Initiator (School) → Referral Recipient (Ophthalmology) / PCC-55 Submit Referral |
| **Gaps / Custom Remaining** | 360X is Trial Implementation; wire format FHIR REST matches guide. Scheduling for appointment booking (optional). PIXm/PDQm for patient matching. |
| **Offer to User** | **Offer 360X conformance** — align guide's referral workflow to 360X actors/transactions. |

---

### IP-2b: Cancel Referral (Timeout)

| Aspect | Assessment |
|--------|------------|
| **Candidate Profiles** | 360X PCC-58 |
| **Fit** | **Full (360X)** — PCC-58 Close Referral with reason "No Response Within 4 Weeks". |
| **Actors / Transactions** | Referral Initiator (School) → Referral Recipient (Ophthalmology) / PCC-58 |
| **Gaps / Custom Remaining** | None — covered by 360X. |
| **Offer to User** | Included in 360X offer. |

---

### IP-2c: Referral Rejection Response

| Aspect | Assessment |
|--------|------------|
| **Candidate Profiles** | 360X PCC-56 Reject |
| **Fit** | **Full (360X)** — PCC-56 Reject with reason. |
| **Actors / Transactions** | Referral Recipient (Ophthalmology) → Referral Initiator (School) / PCC-56 Reject |
| **Gaps / Custom Remaining** | None — covered by 360X. |
| **Offer to User** | Included in 360X offer. |

---

### IP-3a: Assessment Return — Summary (Ophthalmology → School Nurse)

| Aspect | Assessment |
|--------|------------|
| **Candidate Profiles** | 360X PCC-61, MHD, DSUBm, EC-Summary |
| **Fit** | **Partial (360X + MHD)** — 360X PCC-61 Retrieve Report (Initiator pulls). MHD ITI-65 Provide Document Bundle (Recipient pushes). DSUBm ITI-112 Notify (push notification). EC-Summary for content structure (CDA-based; guide uses FHIR). |
| **Actors / Transactions** | Referral Initiator → Referral Recipient (PCC-61 pull); Document Source → Document Recipient (MHD ITI-65 push); Publisher → Subscriber (DSUBm ITI-112) |
| **Gaps / Custom Remaining** | 360X is pull; guide may prefer push (MHD). EC-Summary is CDA — custom FHIR mapping needed. DSUBm is TI. |
| **Offer to User** | **Offer 360X + MHD** — declare conformance to both patterns (pull via 360X, push via MHD). |

---

### IP-3b: Assessment Return — Full (Ophthalmology → Primary Care)

| Aspect | Assessment |
|--------|------------|
| **Candidate Profiles** | MHD, DSUBm, EC-Summary |
| **Fit** | **Full (MHD)** — MHD ITI-65 Provide Document Bundle for document push. DSUBm ITI-112 for notification. |
| **Actors / Transactions** | Document Source (Ophthalmology) → Document Recipient (Primary Care) (MHD ITI-65); Publisher → Subscriber (DSUBm ITI-112) |
| **Gaps / Custom Remaining** | EC-Summary content structure CDA-based; custom FHIR mapping. |
| **Offer to User** | **Offer MHD conformance** for document exchange. |

---

### IP-4a-f: Primary Care Receives (6 Document Types)

| Aspect | Assessment |
|--------|------------|
| **Candidate Profiles** | MHD, PIXm/PDQm/PMIR |
| **Fit** | **Full (MHD)** — MHD ITI-65 for each document receipt. PIXm/PDQm for patient matching. |
| **Actors / Transactions** | Document Source (School/Ophthalmology) → Document Recipient (Primary Care) (MHD ITI-65); Consumer → Supplier (PIXm ITI-83 / PDQm ITI-78) |
| **Gaps / Custom Remaining** | 6 distinct document types mapped to LOINC; Primary Care must handle all. |
| **Offer to User** | **Offer MHD + PIXm/PDQm** for document receipt and patient matching. |

---

### IP-5: Teacher Accommodation (Internal)

| Aspect | Assessment |
|--------|------------|
| **Candidate Profiles** | None |
| **Fit** | **None applies** — Internal school communication; no IHE profile for teacher accommodation notices. |
| **Gaps / Custom Remaining** | Custom: Communication resource, internal delivery (paper, email, EHR message). |
| **Offer to User** | No IHE profile; custom FHIR. |

---

## Summary of IHE Offers to User

| # | Profile | Status | Interoperability Points | Conformance Offered |
|---|---------|--------|------------------------|---------------------|
| 1 | **360X** | TI (Revised 2021-04-14) | IP-2a, IP-2b, IP-2c, IP-3a | **Yes** — align referral workflow |
| 2 | **MHD** | FT (Release 4.2.5, 2026-10-18) | IP-1 (storage), IP-3a (push), IP-3b, IP-4a-f | **Yes** — align document exchange |
| 3 | **DSUBm** | TI (Published 2024-02-29) | IP-3a, IP-3b | **Optional** — push notifications |
| 4 | **PIXm** | TI (Release 3.1.0, 2025-11-06) | All IPs (patient matching) | **Yes** — patient identity |
| 5 | **PDQm** | TI (Release 3.2.0, 2025-11-06) | All IPs (patient lookup) | **Yes** — patient demographics |
| 6 | **EC-Summary** | TI (Published 2017-09-15) | IP-3a, IP-3b (content reference) | **Reference only** — CDA-based, custom FHIR mapping |
| 7 | **XBeR-WD** | TI (Revised 2013-10-04) | IP-2a (workflow definition) | **Optional** — executable workflow |

---

## No IHE Profile — Explicitly None Applies

| Interoperability Point | Reason |
|------------------------|--------|
| **IP-1: Screening Result Capture** | No IHE profile for school health screening data entry |
| **IP-5: Teacher Accommodation** | Internal school communication; no IHE profile |
| **Threshold Evaluation** | Custom clinical logic (Pass/Refer logic) |
| **Opt-out Consent Management** | Custom Consent usage (no BPPC/APPC/PCF fit for opt-out program consent) |

---

## IHE Profile Version Verification

All IHE profile versions and statuses verified live at https://profiles.ihe.net/ on **2026-11-19**:

| Profile | Version | Status | URL |
|---------|---------|--------|-----|
| 360X | Revised 2021-04-14 | Trial Implementation | https://profiles.ihe.net/PCC/360X/ |
| MHD | Release 4.2.5 | Final Text | https://profiles.ihe.net/ITI/MHD/ |
| DSUBm | Release 1.0.0 | Trial Implementation | https://profiles.ihe.net/ITI/DSUBm/ |
| PIXm | Release 3.1.0 | Trial Implementation | https://profiles.ihe.net/ITI/PIXm/ |
| PDQm | Release 3.2.0 | Trial Implementation | https://profiles.ihe.net/ITI/PDQm/ |
| EC-Summary | Published 2017-09-15 | Trial Implementation | https://profiles.ihe.net/EYECARE/EC-Summary/ |
| XBeR-WD | Revised 2013-10-04 | Trial Implementation | https://profiles.ihe.net/PCC/XBeR-WD/ |

---

## Fit Assessment Criteria

| Fit Level | Definition |
|-----------|------------|
| **Full** | Same actors, same transaction number, same message semantics and options as the profile. Wire format (FHIR REST) matches. |
| **Partial** | Pattern coincides but mechanism is the guide's own (e.g., plain FHIR search where profile defines a transaction; push vs pull). Different wire format = max partial. |
| **None** | Profile's actors/transactions do not cover the point; no applicable profile exists. |

---

## Gap and Risk Analysis

| Gap / Risk | Severity | Affected IPs | Mitigation |
|------------|----------|--------------|------------|
| 360X is Trial Implementation | Medium | IP-2, IP-3a | Document as TI; monitor for FT; fallback to custom FHIR if needed |
| MHD document format for screening results | Low | IP-1, IP-4 | Document FHIR-native MHD usage (`application/fhir+json`); validate with MHD test tools |
| EC-Summary CDA-based | Medium | IP-3 | Provide explicit EC-Summary → FHIR mapping table (see [Profiles](profiles.html)) |
| DSUBm is TI | Low | IP-3 | Optional; document as enhancement; not required for core workflow |
| No IHE profile for school screening capture | Medium | IP-1 | Accept custom FHIR; design for future IHE profile adoption |
| Demographic matching without national ID | Medium | All IPs | Document as primary strategy; national ID supplementary when available |

---

## Conformance Declaration

If the user accepts the offers above, the guide would declare conformance to:

```
Conformance:
  - 360X (TI): Referral workflow (IP-2a/b/c, IP-3a pull)
  - MHD (FT): Document exchange (IP-1 storage, IP-3 push, IP-4)
  - PIXm/PDQm (TI): Patient matching (all IPs)
  - DSUBm (TI): Optional push notifications (IP-3)
```

Unchosen associations (e.g., EC-Summary, XBeR-WD) are documented as relationships in this IG, not claimed as conformance.