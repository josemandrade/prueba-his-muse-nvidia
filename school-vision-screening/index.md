# School Vision Screening IG - v0.1.0

* [**Table of Contents**](toc.md)
* **School Vision Screening IG**

## School Vision Screening IG

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/ImplementationGuide/school-vision-screening | *Version*:0.1.0 |
| Draft as of 2026-11-21 | *Computable Name*:SchoolVisionScreening |

### School Vision Screening Implementation Guide

**Version:** 0.1.0 (CI Build)
 **FHIR Version:** 4.0.1
 **Status:** Draft
 **Canonical URL:** `https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening`

-------

#### Overview

This Implementation Guide defines the FHIR R4 profiles, operations, and examples for the **School Vision Screening** interoperability workflow. It enables the exchange of vision screening results, referrals to ophthalmology, and assessment feedback between:

* **School Health Service** (school nurses conducting screening)
* **Ophthalmology Clinic / Hospital** (assessing referred children)
* **Primary Care Team** (receiving results for the child's health record)
* **Parents/Guardians** (receiving notifications, providing consent)
* **Teachers** (receiving classroom accommodation notices)

-------

#### Clinical Use Case

Vision problems in schoolchildren go undetected until they affect learning. The school nurse screens visual acuity per eye during the school year using Snellen chart (6m), Tumbling E optotypes, or Lea symbols.

**Thresholds:**

* **Pass:** ≥6/9 in each eye
* **Refer:** ≤6/12 in either eye OR ≥2 line difference between eyes

Children with abnormal results are referred to an ophthalmologist. The referral result must reach the primary care team for the health record, and parents must be notified.

-------

#### Key Interoperability Points

| | | | | |
| :--- | :--- | :--- | :--- | :--- |
| **IP-1** | Screening Result Capture | Nurse records structured screening data (acuity per eye, test used, outcome) | `Observation`panel + 2 member`Observation`s | — |
| **IP-2** | Referral Dispatch | Structured referral with 4-week deadline tracking, parent decline handling | `ServiceRequest`+`Task` | **360X**(PCC-55/56/58/61) |
| **IP-3** | Assessment Return | Ophthalmology feedback to school nurse (summary) and primary care (full) | `DiagnosticReport`+`Observation`s +`CarePlan` | **360X**(PCC-61),**MHD**(ITI-65) |
| **IP-4** | Primary Care Receive | Screening results + assessments entered in child's health record (6 document types) | `DocumentReference`+`List` | **MHD**(ITI-65) |
| **IP-5** | Teacher Accommodation | Nurse generates accommodation notice from assessment | `Communication` | — |

-------

#### Profiles Summary

| | | |
| :--- | :--- | :--- |
| `SVSPatient` | `Patient` | Child demographics with school roll number, grade at screening |
| `SVSRelatedPerson` | `RelatedPerson` | Parent/guardian with opt-out consent status |
| `SVSPractitioner`/`SVSPractitionerRole` | `Practitioner`/`PractitionerRole` | School nurse, service lead, ophthalmologist |
| `SVSObservationScreeningPanel` | `Observation` | Panel with right/left eye acuity as member`Observation`s (Ratio) |
| `SVSServiceRequestReferral` | `ServiceRequest` | 360X referral to ophthalmology |
| `SVSTaskReferralTracking` | `Task` | 360X referral workflow tracking |
| `SVSDiagnosticReportAssessment` | `DiagnosticReport` | Ophthalmology assessment report |
| `SVSObservationDiagnosis`/`RefractionOD`/`RefractionOS` | `Observation` | Diagnosis, right/left eye refraction |
| `SVSCarePlanFollowUp` | `CarePlan` | Follow-up plan (review interval, patching) |
| `SVSCommunicationAccommodation` | `Communication` | Teacher accommodation notice |
| `SVSConsentOptOut` | `Consent` | Annual opt-out consent (revocable mid-year) |
| `SVSDocumentReferenceIP4` | `DocumentReference` | Primary care document receipts (6 types) |
| `SVSListPrimaryCareDocuments` | `List` | Primary care document log |

-------

#### Operations

| | | | |
| :--- | :--- | :--- | :--- |
| OP-1 | Record Screening | `POST Observation`(panel + members) | — |
| OP-2a | Submit Referral | `POST ServiceRequest`+`POST Task` | **360X PCC-55** |
| OP-2b | Cancel Referral | `PATCH ServiceRequest`(cancelled) | **360X PCC-58** |
| OP-2c | Reject Referral | `PATCH Task`(rejected) | **360X PCC-56** |
| OP-2d | Accept Referral | `PATCH Task`(accepted) | **360X PCC-56** |
| OP-3a | Return Summary | `GET DiagnosticReport`/`POST DocumentReference` | **360X PCC-61**,**MHD ITI-65** |
| OP-3b | Return Full | `POST DocumentReference` | **MHD ITI-65** |
| OP-4a-f | Send to Primary Care | `POST DocumentReference`(6 types) | **MHD ITI-65** |
| OP-5 | Send Accommodation | `POST Communication` | — |
| OP-6 | Query Demographics | `GET Patient?identifier=...` | **PIXm ITI-83**,**PDQm ITI-78** |

-------

#### Navigation

| | |
| :--- | :--- |
| [Clinical Use Case](usecase.md) | Detailed problem statement, users, data flows, consent, success criteria |
| [Process (BPMN)](process.md) | BPMN model with swimlanes, interoperability points marked |
| [Resource Diagram](resources.md) | Resource graph centred on ServiceRequest/Task |
| [Sequence Diagrams](sequences.md) | 7 flows with operation tables |
| [Profiles](profiles.md) | All profile definitions |
| [Operations](operations.md) | Operation details with examples |
| [IHE Relationships](ihe.md) | Profile fit assessment per interoperability point |
| [Lifecycle](lifecycle.md) | State tables for workflow resources |
| [Terminology](terminology.md) | CodeSystems, ValueSets, terminology versions |
| [Public Health & Consent](public-health.md) | Opt-out consent, legal basis, data governance |
| [Examples](examples.md) | Synthetic examples for all profiles |

-------

#### Implementation Notes

* **Terminology Versions:** SNOMED CT 2026-03-15, LOINC 2.76, UCUM 2.0.1
* **Snellen Acuity:** Expressed as `Ratio` (numerator/denominator in meters), not `Quantity`
* **Consent:** Opt-out model, revocable mid-year via multiple `Consent.provision` entries
* **Referral:** Fresh lifecycle on re-issue; `ServiceRequest.replaces` links to cancelled referral
* **Document Exchange:** MHD ITI-65 with `contentType=application/fhir+json`
* **Examples:** All synthetic — no real patient data

-------

#### Dependencies

* `hl7.fhir.r4.core#4.0.1`
* Template: `fhir.base.template#1.6.0`

-------

#### License

This Implementation Guide is licensed under [CC0-1.0](https://creativecommons.org/publicdomain/zero/1.0/).



## Resource Content

```json
{
  "resourceType" : "ImplementationGuide",
  "id" : "school-vision-screening",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/ImplementationGuide/school-vision-screening",
  "version" : "0.1.0",
  "name" : "SchoolVisionScreening",
  "status" : "draft",
  "date" : "2026-11-21T14:59:50+00:00",
  "description" : "FHIR Implementation Guide for School Vision Screening interoperability. Defines profiles, operations, and examples for the exchange of vision screening results, referrals to ophthalmology, and assessment feedback between school health services, ophthalmology clinics, and primary care teams.\nThis guide implements the workflow described in the School Vision Screening use case: school nurse screens visual acuity → refers to ophthalmology if abnormal → receives assessment summary → generates teacher accommodation notice → sends results to primary care for health record.\nKey interoperability points: - IP-1: Screening result capture (Observation panel) - IP-2: Referral dispatch and tracking (360X ServiceRequest + Task) - IP-3: Assessment return (DiagnosticReport + Observations + CarePlan) - IP-4: Primary care receives screening/assessment documents (MHD) - IP-5: Teacher accommodation notice (Communication)\n",
  "packageId" : "school-vision-screening",
  "license" : "CC0-1.0",
  "fhirVersion" : ["4.0.1"],
  "dependsOn" : [{
    "id" : "hl7tx",
    "extension" : [{
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/implementationguide-dependency-comment",
      "valueMarkdown" : "Automatically added as a dependency - all IGs depend on HL7 Terminology"
    }],
    "uri" : "http://terminology.hl7.org/ImplementationGuide/hl7.terminology",
    "packageId" : "hl7.terminology.r4",
    "version" : "7.5.0"
  },
  {
    "id" : "hl7ext",
    "extension" : [{
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/implementationguide-dependency-comment",
      "valueMarkdown" : "Automatically added as a dependency - all IGs depend on the HL7 Extension Pack"
    }],
    "uri" : "http://hl7.org/fhir/extensions/ImplementationGuide/hl7.fhir.uv.extensions",
    "packageId" : "hl7.fhir.uv.extensions.r4",
    "version" : "5.4.0"
  },
  {
    "id" : "hl7_fhir_r4_core",
    "uri" : "http://hl7.org/fhir",
    "packageId" : "hl7.fhir.r4.core",
    "version" : "4.0.1"
  }],
  "definition" : {
    "extension" : [{
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-internal-dependency",
      "valueCode" : "hl7.fhir.uv.tools.r4#1.3.0"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "copyrightyear"
      },
      {
        "url" : "value",
        "valueString" : "2026"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "releaselabel"
      },
      {
        "url" : "value",
        "valueString" : "CI Build"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "apply-jurisdiction"
      },
      {
        "url" : "value",
        "valueString" : "false"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "show-inherited-invariants"
      },
      {
        "url" : "value",
        "valueString" : "false"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "autoload-resources"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "path-liquid"
      },
      {
        "url" : "value",
        "valueString" : "template/liquid"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "path-liquid"
      },
      {
        "url" : "value",
        "valueString" : "input/liquid"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "path-qa"
      },
      {
        "url" : "value",
        "valueString" : "temp/qa"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "path-temp"
      },
      {
        "url" : "value",
        "valueString" : "temp/pages"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "path-output"
      },
      {
        "url" : "value",
        "valueString" : "output"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "path-suppressed-warnings"
      },
      {
        "url" : "value",
        "valueString" : "input/ignoreWarnings.txt"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "path-history"
      },
      {
        "url" : "value",
        "valueString" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/history.html"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "template-html"
      },
      {
        "url" : "value",
        "valueString" : "template-page.html"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "template-md"
      },
      {
        "url" : "value",
        "valueString" : "template-page-md.html"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "apply-contact"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "apply-context"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "apply-copyright"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "apply-license"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "apply-publisher"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "apply-version"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "apply-wg"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "active-tables"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "fmm-definition"
      },
      {
        "url" : "value",
        "valueString" : "http://hl7.org/fhir/versions.html#maturity"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "propagate-status"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "excludelogbinaryformat"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "tabbed-snapshots"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    }],
    "resource" : [{
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Patient"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Patient-SVSPatientExample.html"
      }],
      "reference" : {
        "reference" : "Patient/SVSPatientExample"
      },
      "name" : "Child Example - Maria Gonzalez",
      "description" : "Synthetic example of an 8-year-old child",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-patient"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "CodeSystem"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "CodeSystem-svs-accommodation-type.html"
      }],
      "reference" : {
        "reference" : "CodeSystem/svs-accommodation-type"
      },
      "name" : "Classroom Accommodation Types",
      "description" : "Types of classroom accommodations for vision impairment",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "ValueSet"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "ValueSet-svs-accommodation-type-vs.html"
      }],
      "reference" : {
        "reference" : "ValueSet/svs-accommodation-type-vs"
      },
      "name" : "Classroom Accommodation Types ValueSet",
      "description" : "Types of classroom accommodations for vision impairment",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Observation"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Observation-SVSObservationDiagnosisExample.html"
      }],
      "reference" : {
        "reference" : "Observation/SVSObservationDiagnosisExample"
      },
      "name" : "Diagnosis - Mild Myopia OD",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-diagnosis"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "DocumentReference"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "DocumentReference-SVSDocumentReferenceScreeningPassExample.html"
      }],
      "reference" : {
        "reference" : "DocumentReference/SVSDocumentReferenceScreeningPassExample"
      },
      "name" : "DocumentReference - Screening Pass Result (IP-4)",
      "description" : "Primary Care receives screening pass result via MHD",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-document-reference-ip4"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "CarePlan"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "CarePlan-SVSCarePlanFollowUpExample.html"
      }],
      "reference" : {
        "reference" : "CarePlan/SVSCarePlanFollowUpExample"
      },
      "name" : "Follow-up Plan - 12 Month Review",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-care-plan-follow-up"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Observation"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Observation-SVSObservationLeftEyeAcuityReferExample.html"
      }],
      "reference" : {
        "reference" : "Observation/SVSObservationLeftEyeAcuityReferExample"
      },
      "name" : "Left Eye Acuity - Pass (6/9)",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-left-eye-acuity"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-observation-refraction-os.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-observation-refraction-os"
      },
      "name" : "Left Eye Refraction",
      "description" : "Left eye refractive prescription",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Observation"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Observation-SVSObservationRefractionOSExample.html"
      }],
      "reference" : {
        "reference" : "Observation/SVSObservationRefractionOSExample"
      },
      "name" : "Left Eye Refraction - Normal",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-refraction-os"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-observation-left-eye-acuity.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-observation-left-eye-acuity"
      },
      "name" : "Left Eye Visual Acuity",
      "description" : "Left eye visual acuity measurement as Snellen fraction using Ratio",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "DiagnosticReport"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "DiagnosticReport-SVSDiagnosticReportAssessmentExample.html"
      }],
      "reference" : {
        "reference" : "DiagnosticReport/SVSDiagnosticReportAssessmentExample"
      },
      "name" : "Ophthalmology Assessment - Maria Gonzalez",
      "description" : "Complete assessment: mild myopia OD, prescription -1.00 DS, follow-up 12 months",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-diagnostic-report-assessment"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Organization"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Organization-SVSOrganizationClinicExample.html"
      }],
      "reference" : {
        "reference" : "Organization/SVSOrganizationClinicExample"
      },
      "name" : "Ophthalmology Clinic Example",
      "description" : "Ophthalmology clinic receiving vision screening referrals",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-organization"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-observation-diagnosis.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-observation-diagnosis"
      },
      "name" : "Ophthalmology Diagnosis",
      "description" : "Diagnosis from ophthalmology assessment",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-care-plan-follow-up.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-care-plan-follow-up"
      },
      "name" : "Ophthalmology Follow-up Plan",
      "description" : "Follow-up plan from ophthalmology assessment",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-diagnostic-report-assessment.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-diagnostic-report-assessment"
      },
      "name" : "Ophthalmology Vision Assessment Report",
      "description" : "Complete ophthalmology assessment report for vision screening referral",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "RelatedPerson"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "RelatedPerson-SVSRelatedPersonExample.html"
      }],
      "reference" : {
        "reference" : "RelatedPerson/SVSRelatedPersonExample"
      },
      "name" : "Parent Example - Ana Gonzalez",
      "description" : "Mother of Maria Gonzalez",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-related-person"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "List"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "List-SVSListPrimaryCareDocumentsExample.html"
      }],
      "reference" : {
        "reference" : "List/SVSListPrimaryCareDocumentsExample"
      },
      "name" : "Primary Care Document Log - Maria Gonzalez",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-list-primary-care-documents"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-document-reference-ip4.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-document-reference-ip4"
      },
      "name" : "Primary Care Document Reference (IP-4)",
      "description" : "DocumentReference for each of the 6 IP-4 document types received by Primary Care",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Organization"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Organization-SVSOrganizationPrimaryCareExample.html"
      }],
      "reference" : {
        "reference" : "Organization/SVSOrganizationPrimaryCareExample"
      },
      "name" : "Primary Care Example - Centro de Salud Las Rosas",
      "description" : "Primary care center receiving screening results",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-organization"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-list-primary-care-documents.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-list-primary-care-documents"
      },
      "name" : "Primary Care Vision Screening Document Log",
      "description" : "List of all vision screening related documents received by Primary Care for a child",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "ServiceRequest"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "ServiceRequest-SVSServiceRequestReferralExample.html"
      }],
      "reference" : {
        "reference" : "ServiceRequest/SVSServiceRequestReferralExample"
      },
      "name" : "Referral to Ophthalmology - Maria Gonzalez",
      "description" : "Referral from school nurse to ophthalmology for right eye acuity 6/12",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-service-request-referral"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Observation"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Observation-SVSObservationRightEyeAcuityReferExample.html"
      }],
      "reference" : {
        "reference" : "Observation/SVSObservationRightEyeAcuityReferExample"
      },
      "name" : "Right Eye Acuity - Refer (6/12)",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-right-eye-acuity"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-observation-refraction-od.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-observation-refraction-od"
      },
      "name" : "Right Eye Refraction",
      "description" : "Right eye refractive prescription",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Observation"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Observation-SVSObservationRefractionODExample.html"
      }],
      "reference" : {
        "reference" : "Observation/SVSObservationRefractionODExample"
      },
      "name" : "Right Eye Refraction -1.00 DS",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-refraction-od"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-observation-right-eye-acuity.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-observation-right-eye-acuity"
      },
      "name" : "Right Eye Visual Acuity",
      "description" : "Right eye visual acuity measurement as Snellen fraction using Ratio",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Organization"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Organization-SVSOrganizationSchoolExample.html"
      }],
      "reference" : {
        "reference" : "Organization/SVSOrganizationSchoolExample"
      },
      "name" : "School Example - Colegio Publico San Isidro",
      "description" : "Public school with vision screening program",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-organization"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Organization"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Organization-SVSOrganizationSchoolHealthServiceExample.html"
      }],
      "reference" : {
        "reference" : "Organization/SVSOrganizationSchoolHealthServiceExample"
      },
      "name" : "School Health Service - Servicio de Salud Escolar Madrid",
      "description" : "Regional school health service overseeing vision screening",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-organization"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "CodeSystem"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "CodeSystem-svs-practitioner-role.html"
      }],
      "reference" : {
        "reference" : "CodeSystem/svs-practitioner-role"
      },
      "name" : "School Health Service Practitioner Roles",
      "description" : "Roles within the school health service for vision screening",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "ValueSet"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "ValueSet-svs-practitioner-role-vs.html"
      }],
      "reference" : {
        "reference" : "ValueSet/svs-practitioner-role-vs"
      },
      "name" : "School Health Service Practitioner Roles ValueSet",
      "description" : "Roles within the school health service",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Practitioner"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Practitioner-SVSPractitionerNurseExample.html"
      }],
      "reference" : {
        "reference" : "Practitioner/SVSPractitionerNurseExample"
      },
      "name" : "School Nurse Example - Carmen Ruiz",
      "description" : "School nurse conducting vision screening",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-practitioner"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "CodeSystem"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "CodeSystem-svs-document-type.html"
      }],
      "reference" : {
        "reference" : "CodeSystem/svs-document-type"
      },
      "name" : "School Vision Screening Document Types",
      "description" : "Types of documents exchanged with Primary Care (IP-4)",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "ValueSet"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "ValueSet-svs-document-type-vs.html"
      }],
      "reference" : {
        "reference" : "ValueSet/svs-document-type-vs"
      },
      "name" : "School Vision Screening Document Types ValueSet",
      "description" : "Types of documents exchanged with Primary Care",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-consent-opt-out.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-consent-opt-out"
      },
      "name" : "School Vision Screening Opt-Out Consent",
      "description" : "Annual opt-out consent for vision screening program",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-organization.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-organization"
      },
      "name" : "School Vision Screening Organization",
      "description" : "Organization profile for School Health Service, Ophthalmology Clinic, or Primary Care Practice",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "CodeSystem"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "CodeSystem-svs-screening-outcome.html"
      }],
      "reference" : {
        "reference" : "CodeSystem/svs-screening-outcome"
      },
      "name" : "School Vision Screening Outcomes",
      "description" : "Possible outcomes of a vision screening encounter",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "ValueSet"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "ValueSet-svs-screening-outcome-vs.html"
      }],
      "reference" : {
        "reference" : "ValueSet/svs-screening-outcome-vs"
      },
      "name" : "School Vision Screening Outcomes ValueSet",
      "description" : "Possible outcomes of a vision screening encounter",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-observation-screening-panel.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-observation-screening-panel"
      },
      "name" : "School Vision Screening Panel",
      "description" : "Panel observation containing right and left eye visual acuity measurements",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-related-person.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-related-person"
      },
      "name" : "School Vision Screening Parent/Guardian",
      "description" : "Profile for a parent or guardian of a child in the screening program",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-patient.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-patient"
      },
      "name" : "School Vision Screening Patient (Child)",
      "description" : "Profile for a child enrolled in school vision screening program",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-practitioner.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-practitioner"
      },
      "name" : "School Vision Screening Practitioner",
      "description" : "Base profile for practitioners in the school vision screening program",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-practitioner-role.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-practitioner-role"
      },
      "name" : "School Vision Screening Practitioner Role",
      "description" : "Role profile for school nurses and service leads",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-questionnaire-response-screening.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-questionnaire-response-screening"
      },
      "name" : "School Vision Screening Questionnaire Response",
      "description" : "Screening form response captured by the nurse",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-service-request-referral.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-service-request-referral"
      },
      "name" : "School Vision Screening Referral",
      "description" : "Referral from school nurse to ophthalmology for vision assessment",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "CodeSystem"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "CodeSystem-svs-referral-reason.html"
      }],
      "reference" : {
        "reference" : "CodeSystem/svs-referral-reason"
      },
      "name" : "School Vision Screening Referral Reasons",
      "description" : "Reasons for referral to ophthalmology",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "ValueSet"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "ValueSet-svs-referral-reason-vs.html"
      }],
      "reference" : {
        "reference" : "ValueSet/svs-referral-reason-vs"
      },
      "name" : "School Vision Screening Referral Reasons ValueSet",
      "description" : "Reasons for referral to ophthalmology",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-task-referral-tracking.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-task-referral-tracking"
      },
      "name" : "School Vision Screening Referral Tracking",
      "description" : "Task for tracking referral workflow state",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "CodeSystem"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "CodeSystem-svs-screening-test-method.html"
      }],
      "reference" : {
        "reference" : "CodeSystem/svs-screening-test-method"
      },
      "name" : "School Vision Screening Test Methods",
      "description" : "Methods used for visual acuity screening in school settings",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "ValueSet"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "ValueSet-svs-screening-test-method-vs.html"
      }],
      "reference" : {
        "reference" : "ValueSet/svs-screening-test-method-vs"
      },
      "name" : "School Vision Screening Test Methods ValueSet",
      "description" : "Allowed test methods for school vision screening",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Encounter"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Encounter-SVSEncounterScreeningExample.html"
      }],
      "reference" : {
        "reference" : "Encounter/SVSEncounterScreeningExample"
      },
      "name" : "Screening Encounter - Maria Gonzalez",
      "exampleBoolean" : true
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Observation"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Observation-SVSObservationScreeningPanelReferExample.html"
      }],
      "reference" : {
        "reference" : "Observation/SVSObservationScreeningPanelReferExample"
      },
      "name" : "Screening Panel - Refer Result (Maria Gonzalez)",
      "description" : "Visual acuity screening panel showing refer result: right eye 6/12 (<=6/12)",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-screening-panel"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-svs-communication-accommodation.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/svs-communication-accommodation"
      },
      "name" : "Teacher Accommodation Notice",
      "description" : "Notice from school nurse to teacher about classroom accommodation",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "ValueSet"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "ValueSet-svs-acuity-interpretation-vs.html"
      }],
      "reference" : {
        "reference" : "ValueSet/svs-acuity-interpretation-vs"
      },
      "name" : "Visual Acuity Interpretation ValueSet",
      "description" : "Interpretation codes for visual acuity results",
      "exampleBoolean" : false
    }],
    "page" : {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
        "valueUrl" : "toc.html"
      }],
      "nameUrl" : "toc.html",
      "title" : "Table of Contents",
      "generation" : "html",
      "page" : [{
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "index.html"
        }],
        "nameUrl" : "index.html",
        "title" : "School Vision Screening IG",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "usecase.html"
        }],
        "nameUrl" : "usecase.html",
        "title" : "Clinical Use Case",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "process.html"
        }],
        "nameUrl" : "process.html",
        "title" : "Process (BPMN)",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "resources.html"
        }],
        "nameUrl" : "resources.html",
        "title" : "Resource Diagram",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "sequences.html"
        }],
        "nameUrl" : "sequences.html",
        "title" : "Sequence Diagrams",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "profiles.html"
        }],
        "nameUrl" : "profiles.html",
        "title" : "Profiles",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "operations.html"
        }],
        "nameUrl" : "operations.html",
        "title" : "Operations",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "ihe.html"
        }],
        "nameUrl" : "ihe.html",
        "title" : "IHE Profile Relationships",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "lifecycle.html"
        }],
        "nameUrl" : "lifecycle.html",
        "title" : "Lifecycle Tables",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "terminology.html"
        }],
        "nameUrl" : "terminology.html",
        "title" : "Terminology",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "public-health.html"
        }],
        "nameUrl" : "public-health.html",
        "title" : "Public Health & Consent",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "examples.html"
        }],
        "nameUrl" : "examples.html",
        "title" : "Examples",
        "generation" : "markdown"
      }]
    },
    "parameter" : [{
      "code" : "path-resource",
      "value" : "input/capabilities"
    },
    {
      "code" : "path-resource",
      "value" : "input/examples"
    },
    {
      "code" : "path-resource",
      "value" : "input/extensions"
    },
    {
      "code" : "path-resource",
      "value" : "input/models"
    },
    {
      "code" : "path-resource",
      "value" : "input/operations"
    },
    {
      "code" : "path-resource",
      "value" : "input/profiles"
    },
    {
      "code" : "path-resource",
      "value" : "input/resources"
    },
    {
      "code" : "path-resource",
      "value" : "input/vocabulary"
    },
    {
      "code" : "path-resource",
      "value" : "input/maps"
    },
    {
      "code" : "path-resource",
      "value" : "input/testing"
    },
    {
      "code" : "path-resource",
      "value" : "input/history"
    },
    {
      "code" : "path-resource",
      "value" : "fsh-generated/resources"
    },
    {
      "code" : "path-pages",
      "value" : "template/config"
    },
    {
      "code" : "path-pages",
      "value" : "input/images"
    },
    {
      "code" : "path-tx-cache",
      "value" : "input-cache/txcache"
    }]
  }
}

```
