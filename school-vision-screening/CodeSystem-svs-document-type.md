# School Vision Screening Document Types - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **School Vision Screening Document Types**

## CodeSystem: School Vision Screening Document Types 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-document-type | *Version*:0.1.0 |
| Active as of 2026-11-21 | *Computable Name*:SVSDocumentType |

 
Types of documents exchanged with Primary Care (IP-4) 

 This Code system is referenced in the content logical definition of the following value sets: 

* [School Vision Screening Document Types ValueSet](ValueSet-svs-document-type-vs.md)



## Resource Content

```json
{
  "resourceType" : "CodeSystem",
  "id" : "svs-document-type",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-document-type",
  "version" : "0.1.0",
  "name" : "SVSDocumentType",
  "title" : "School Vision Screening Document Types",
  "status" : "active",
  "experimental" : false,
  "date" : "2026-11-21T14:59:50+00:00",
  "description" : "Types of documents exchanged with Primary Care (IP-4)",
  "caseSensitive" : true,
  "content" : "complete",
  "count" : 7,
  "concept" : [{
    "code" : "screening-pass",
    "display" : "Screening Pass",
    "definition" : "Vision screening result: pass (≥6/9 both eyes)"
  },
  {
    "code" : "screening-decline",
    "display" : "Screening Decline",
    "definition" : "Vision screening result: parent declined referral"
  },
  {
    "code" : "screening-missed",
    "display" : "Screening Missed",
    "definition" : "Vision screening not completed (2nd absent)"
  },
  {
    "code" : "assessment-full",
    "display" : "Full Assessment",
    "definition" : "Complete ophthalmology assessment report"
  },
  {
    "code" : "referral-dna",
    "display" : "Referral DNA",
    "definition" : "Referral closed: did not attend (2nd DNA)"
  },
  {
    "code" : "referral-rejected",
    "display" : "Referral Rejected",
    "definition" : "Referral rejected by ophthalmology"
  },
  {
    "code" : "end-of-year-missed",
    "display" : "End-of-Year Missed",
    "definition" : "Screening missed at end of school year (pending re-screen)"
  }]
}

```
