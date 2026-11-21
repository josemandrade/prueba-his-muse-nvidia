# School Vision Screening Referral - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **School Vision Screening Referral**

## Resource Profile: School Vision Screening Referral 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-service-request-referral | *Version*:0.1.0 |
| Active as of 2026-11-21 | *Computable Name*:SVSServiceRequestReferral |

 
Referral from school nurse to ophthalmology for vision assessment 

**Usages:**

* Examples for this Profile: [ServiceRequest/SVSServiceRequestReferralExample](ServiceRequest-SVSServiceRequestReferralExample.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/school-vision-screening|current/StructureDefinition/StructureDefinition-svs-service-request-referral.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-svs-service-request-referral.csv), [Excel](StructureDefinition-svs-service-request-referral.xlsx), [Schematron](StructureDefinition-svs-service-request-referral.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "svs-service-request-referral",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-service-request-referral",
  "version" : "0.1.0",
  "name" : "SVSServiceRequestReferral",
  "title" : "School Vision Screening Referral",
  "status" : "active",
  "experimental" : false,
  "date" : "2026-11-21T14:59:50+00:00",
  "description" : "Referral from school nurse to ophthalmology for vision assessment",
  "fhirVersion" : "4.0.1",
  "mapping" : [{
    "identity" : "workflow",
    "uri" : "http://hl7.org/fhir/workflow",
    "name" : "Workflow Pattern"
  },
  {
    "identity" : "v2",
    "uri" : "http://hl7.org/v2",
    "name" : "HL7 v2 Mapping"
  },
  {
    "identity" : "rim",
    "uri" : "http://hl7.org/v3",
    "name" : "RIM Mapping"
  },
  {
    "identity" : "w5",
    "uri" : "http://hl7.org/fhir/fivews",
    "name" : "FiveWs Pattern Mapping"
  },
  {
    "identity" : "quick",
    "uri" : "http://siframework.org/cqf",
    "name" : "Quality Improvement and Clinical Knowledge (QUICK)"
  }],
  "kind" : "resource",
  "abstract" : false,
  "type" : "ServiceRequest",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/ServiceRequest",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "ServiceRequest",
      "path" : "ServiceRequest"
    },
    {
      "id" : "ServiceRequest.intent",
      "path" : "ServiceRequest.intent",
      "patternCode" : "order"
    },
    {
      "id" : "ServiceRequest.category",
      "path" : "ServiceRequest.category",
      "min" : 1,
      "max" : "1"
    },
    {
      "id" : "ServiceRequest.priority",
      "path" : "ServiceRequest.priority",
      "min" : 1,
      "patternCode" : "routine"
    },
    {
      "id" : "ServiceRequest.code",
      "path" : "ServiceRequest.code",
      "min" : 1
    },
    {
      "id" : "ServiceRequest.occurrence[x]",
      "path" : "ServiceRequest.occurrence[x]",
      "slicing" : {
        "discriminator" : [{
          "type" : "type",
          "path" : "$this"
        }],
        "ordered" : false,
        "rules" : "open"
      },
      "min" : 1
    },
    {
      "id" : "ServiceRequest.occurrence[x]:occurrenceDateTime",
      "path" : "ServiceRequest.occurrence[x]",
      "sliceName" : "occurrenceDateTime",
      "min" : 1,
      "max" : "1",
      "type" : [{
        "code" : "dateTime"
      }]
    },
    {
      "id" : "ServiceRequest.authoredOn",
      "path" : "ServiceRequest.authoredOn",
      "min" : 1
    },
    {
      "id" : "ServiceRequest.requester",
      "path" : "ServiceRequest.requester",
      "min" : 1
    },
    {
      "id" : "ServiceRequest.performer",
      "path" : "ServiceRequest.performer",
      "min" : 1,
      "max" : "1"
    },
    {
      "id" : "ServiceRequest.reasonCode",
      "path" : "ServiceRequest.reasonCode",
      "min" : 1
    }]
  }
}

```
