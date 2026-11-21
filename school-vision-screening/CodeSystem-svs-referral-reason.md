# School Vision Screening Referral Reasons - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **School Vision Screening Referral Reasons**

## CodeSystem: School Vision Screening Referral Reasons 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-referral-reason | *Version*:0.1.0 |
| Active as of 2026-11-21 | *Computable Name*:SVSReferralReason |

 
Reasons for referral to ophthalmology 

 This Code system is referenced in the content logical definition of the following value sets: 

* [School Vision Screening Referral Reasons ValueSet](ValueSet-svs-referral-reason-vs.md)



## Resource Content

```json
{
  "resourceType" : "CodeSystem",
  "id" : "svs-referral-reason",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-referral-reason",
  "version" : "0.1.0",
  "name" : "SVSReferralReason",
  "title" : "School Vision Screening Referral Reasons",
  "status" : "active",
  "experimental" : false,
  "date" : "2026-11-21T14:59:50+00:00",
  "description" : "Reasons for referral to ophthalmology",
  "caseSensitive" : true,
  "content" : "complete",
  "count" : 3,
  "concept" : [{
    "code" : "acuity-low",
    "display" : "Acuity ≤6/12",
    "definition" : "Visual acuity 6/12 or worse in either eye"
  },
  {
    "code" : "acuity-diff",
    "display" : "Acuity difference ≥2 lines",
    "definition" : "Difference of two or more lines between eyes"
  },
  {
    "code" : "incomplete-2nd",
    "display" : "Incomplete after 2 attempts",
    "definition" : "Screening incomplete after two attempts with partial data"
  }]
}

```
