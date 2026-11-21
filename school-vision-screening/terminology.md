# Terminology - v0.1.0

* [**Table of Contents**](toc.md)
* **Terminology**

## Terminology

### Terminology

-------

#### Terminology Versions

All terminology versions are pinned from the terminology server (`https://tx.hl7chile.cl/r4` or equivalent) at the time of IG build.

| | | |
| :--- | :--- | :--- |
| **SNOMED CT** | `http://snomed.info/sct/21000325107/version/20260315` | International Edition, 2026-03-15 |
| **LOINC** | 2.76 | Terminology server |
| **UCUM** | 2.0.1 | R4 UCUM expansion |
| **ICD-10** | WHO 2024 | WHO |
| **HL7 v2-0131**(Relationship) | R4 | HL7 |
| **HL7 v2-0203**(Identifier Type) | R4 | HL7 |
| **HL7 v2-0074**(Diagnostic Service) | R4 | HL7 |

-------

#### Standard Code Systems Used

| | | |
| :--- | :--- | :--- |
| SNOMED CT | `http://snomed.info/sct` | Diagnoses (myopia, hyperopia, etc.), body sites, procedures |
| LOINC | `http://loinc.org` | Observation codes (acuity, refraction), document types, panels |
| UCUM | `http://unitsofmeasure.org` | Units for refraction (diopters), Ratios for Snellen acuity |
| HL7 v2-0131 | `http://terminology.hl7.org/CodeSystem/v2-0131` | Relationship codes (MTH, FTH, GRD) |
| HL7 v2-0203 | `http://terminology.hl7.org/CodeSystem/v2-0203` | Identifier types (SB, NI, PRN, PIXM) |
| HL7 v2-0074 | `http://terminology.hl7.org/CodeSystem/v2-0074` | Diagnostic service category (OP) |
| ObsInterp | `http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation` | A (Abnormal), N (Normal) |
| ConsentScope | `http://terminology.hl7.org/CodeSystem/consentscope` | screening |
| ConsentCategory | `http://terminology.hl7.org/CodeSystem/consentcategorycodes` | DENY |
| DocClass | `http://terminology.hl7.org/CodeSystem/document-class` | screening-report |
| FormatCode | `http://ihe.net/fhir/ihe.formatcode.fhir/CodeSystem/formatcode` | application/fhir+json |
| TaskCode | `http://hl7.org/fhir/CodeSystem/task-code` | referral, referral-detail, assessment-report |
| ServiceRequestCategory | `http://terminology.hl7.org/CodeSystem/service-request-category` | referral |
| ObsCategory | `http://terminology.hl7.org/CodeSystem/observation-category` | vital-signs, diagnosis, exam |
| CommCategory | `http://terminology.hl7.org/CodeSystem/communication-category` | instruction |
| CarePlanCategory | `http://terminology.hl7.org/CodeSystem/careplan-category` | assess-plan |
| PractitionerRoleCode | `http://terminology.hl7.org/CodeSystem/practitioner-role` | (standard roles) |

-------

#### Local CodeSystems (Defined in This IG)

##### SVSScreeningTestMethod

**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-screening-test-method`

| | | |
| :--- | :--- | :--- |
| `snellen` | Snellen 6m chart | Snellen chart at 6 metres |
| `tumbling-e` | Tumbling E optotypes | Tumbling E optotypes for children who cannot read letters |
| `lea-symbols` | Lea symbols | Lea symbols for pre-readers |
| `other` | Other method | Other screening method not listed |

**ValueSet:** `SVSScreeningTestMethodVS` (`https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/ValueSet/svs-screening-test-method-vs`)

-------

##### SVSScreeningOutcome

**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-screening-outcome`

| | | |
| :--- | :--- | :--- |
| `pass` | Pass | Visual acuity ≥6/9 in both eyes |
| `refer` | Refer | Visual acuity ≤6/12 in either eye OR ≥2 line difference between eyes |
| `absent` | Absent | Child was absent on screening day |
| `incomplete` | Incomplete | Screening could not be completed (uncooperative, one eye only) |

**ValueSet:** `SVSScreeningOutcomeVS` (`https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/ValueSet/svs-screening-outcome-vs`)

-------

##### SVSReferralReason

**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-referral-reason`

| | | |
| :--- | :--- | :--- |
| `acuity-low` | Acuity ≤6/12 | Visual acuity 6/12 or worse in either eye |
| `acuity-diff` | Acuity difference ≥2 lines | Difference of two or more lines between eyes |
| `incomplete-2nd` | Incomplete after 2 attempts | Screening incomplete after two attempts with partial data |

**ValueSet:** `SVSReferralReasonVS` (`https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/ValueSet/svs-referral-reason-vs`)

-------

##### SVSAccommodationType

**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-accommodation-type`

| | | |
| :--- | :--- | :--- |
| `glasses` | Glasses needed | Child requires prescription glasses |
| `front-seat` | Front seat | Child needs front row seating |
| `both` | Glasses and front seat | Child needs both glasses and front seat |
| `other` | Other accommodation | Other classroom accommodation |

**ValueSet:** `SVSAccommodationTypeVS` (`https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/ValueSet/svs-accommodation-type-vs`)

-------

##### SVSPractitionerRole

**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-practitioner-role`

| | | |
| :--- | :--- | :--- |
| `school-nurse` | School Nurse | Registered nurse conducting vision screening |
| `service-lead` | Service Lead | School health program lead / coordinator |

**ValueSet:** `SVSPractitionerRoleVS` (`https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/ValueSet/svs-practitioner-role-vs`)

-------

##### SVSDocumentType

**Canonical:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-document-type`

| | | | |
| :--- | :--- | :--- | :--- |
| `screening-pass` | Screening Pass | Vision screening result: pass (≥6/9 both eyes) | 83700-8 |
| `screening-decline` | Screening Decline | Vision screening result: parent declined referral | 83700-8 |
| `screening-missed` | Screening Missed | Vision screening not completed (2nd absent) | 83700-8 |
| `assessment-full` | Full Assessment | Complete ophthalmology assessment report | 28626-8 |
| `referral-dna` | Referral DNA | Referral closed: did not attend (2nd DNA) | 11506-3 |
| `referral-rejected` | Referral Rejected | Referral rejected by ophthalmology | 11506-3 |
| `end-of-year-missed` | End-of-Year Missed | Screening missed at end of school year (pending re-screen) | 83700-8 |

**ValueSet:** `SVSDocumentTypeVS` (`https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/ValueSet/svs-document-type-vs`)

-------

#### Key SNOMED CT Codes (Verified 2026-03-15 Edition)

| | | | |
| :--- | :--- | :--- | :--- |
| Myopia | 373124007 | Myopia | Diagnosis |
| Hyperopia | 13962005 | Hyperopia | Diagnosis |
| Astigmatism | 45337004 | Astigmatism | Diagnosis |
| Amblyopia | 26920007 | Amblyopia | Diagnosis |
| Decreased visual acuity | 416070007 | Decreased visual acuity | Referral reasonCode |
| Anisometropia | 267083005 | Anisometropia | Referral reasonCode (acuity diff) |
| Referral to ophthalmologist | 307924000 | Referral to ophthalmologist | ServiceRequest.code |
| Right eye | 363654007 | Right eye | Observation.bodySite |
| Left eye | 363655008 | Left eye | Observation.bodySite |
| School nursing | 408480009 | School nursing | PractitionerRole.specialty |
| Ophthalmology | 309474003 | Ophthalmology | PractitionerRole.specialty |
| Patching therapy | 712743006 | Patching therapy | CarePlan.activity.code |
| Myopia follow-up | 373124007 | Myopia follow-up | CarePlan.activity.code |

-------

#### Key LOINC Codes

| | | | |
| :--- | :--- | :--- | :--- |
| Visual acuity screening panel | 83700-8 | Visual acuity screening panel | Observation.code (panel), DocumentReference.type |
| Visual acuity right eye | 29474-1 | Visual acuity right eye | Observation.code (member) |
| Visual acuity left eye | 29473-3 | Visual acuity left eye | Observation.code (member) |
| Sphere | 29468-3 | Sphere | Observation.component.code |
| Cylinder | 29469-1 | Cylinder | Observation.component.code |
| Axis | 29470-9 | Axis | Observation.component.code |
| Ophthalmology study | 28626-8 | Ophthalmology study | DiagnosticReport.code, DocumentReference.type |
| Referral note | 11506-3 | Referral note | DocumentReference.type (DNA, rejected) |

-------

#### UCUM Units

| | | | |
| :--- | :--- | :--- | :--- |
| Meter | m | meter | Ratio numerator/denominator for Snellen |
| Diopter | D | diopter | Refraction sphere/cylinder |
| Degree | deg | degree | Refraction axis |

-------

#### Binding Strengths

| | | |
| :--- | :--- | :--- |
| `Observation.code`(panel) | Required | LOINC 83700-8 |
| `Observation.code`(right eye) | Required | LOINC 29474-1 |
| `Observation.code`(left eye) | Required | LOINC 29473-3 |
| `Observation.code`(diagnosis) | Required | SNOMED CT (Diagnosis hierarchy) |
| `Observation.code`(refraction) | Required | LOINC 29474-1 / 29473-3 |
| `Observation.component.code` | Required | LOINC 29468-3, 29469-1, 29470-9 |
| `Observation.valueRatio` | Required | Ratio (numerator/denominator in meters) |
| `Observation.valueQuantity`(refraction) | Required | UCUM (D, deg) |
| `Observation.bodySite` | Required | SNOMED CT (363654007, 363655008) |
| `Observation.interpretation` | Required | `SVSAcuityInterpretationVS`(A, N) |
| `ServiceRequest.reasonCode` | Extensible | `SVSReferralReasonVS`+ SNOMED |
| `ServiceRequest.category` | Required | `referral` |
| `Task.code` | Extensible | `referral` |
| `DiagnosticReport.category` | Extensible | HL7 v2-0074 OP |
| `DiagnosticReport.code` | Required | LOINC 28626-8 |
| `Observation.code`(refraction components) | Required | LOINC 29468-3, 29469-1, 29470-9 |
| `Communication.category` | Preferred | `instruction` |
| `Consent.scope` | Required | `screening` |
| `Consent.category` | Required | `DENY` |
| `DocumentReference.type` | Required | LOINC (per documentType table) |
| `DocumentReference.format` | Required | `application/fhir+json` |

-------

#### Unmapped Codes

| | | |
| :--- | :--- | :--- |
| Test used (snellen/tumbling-e/lea) | No standard LOINC/SNOMED | `SVSScreeningTestMethod` |
| Screening outcome (pass/refer/absent/incomplete) | No standard ValueSet | `SVSScreeningOutcome` |
| Accommodation type | No standard ValueSet | `SVSAccommodationType` |
| Referral reason (incomplete-2nd) | Partially mapped | `SVSReferralReason`(custom) |
| Parent decision (accept/decline) | No standard ValueSet | Local extension |

-------

#### Terminology Server

**Primary:** `https://tx.hl7chile.cl/r4` (or equivalent national terminology server)

**Expansion/Validation:** All ValueSets expandable and validatable against the terminology server at build time.

**SNOMED CT Edition:** International Edition, `http://snomed.info/sct/21000325107/version/20260315`

**LOINC Version:** 2.76 (as reported by terminology server)

**UCUM Version:** 2.0.1 (as in R4 UCUM expansion)

