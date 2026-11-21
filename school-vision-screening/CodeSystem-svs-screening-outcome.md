# School Vision Screening Outcomes - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **School Vision Screening Outcomes**

## CodeSystem: School Vision Screening Outcomes 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-screening-outcome | *Version*:0.1.0 |
| Active as of 2026-11-21 | *Computable Name*:SVSScreeningOutcome |

 
Possible outcomes of a vision screening encounter 

 This Code system is referenced in the content logical definition of the following value sets: 

* [School Vision Screening Outcomes ValueSet](ValueSet-svs-screening-outcome-vs.md)



## Resource Content

```json
{
  "resourceType" : "CodeSystem",
  "id" : "svs-screening-outcome",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-screening-outcome",
  "version" : "0.1.0",
  "name" : "SVSScreeningOutcome",
  "title" : "School Vision Screening Outcomes",
  "status" : "active",
  "experimental" : false,
  "date" : "2026-11-21T14:59:50+00:00",
  "description" : "Possible outcomes of a vision screening encounter",
  "caseSensitive" : true,
  "content" : "complete",
  "count" : 4,
  "concept" : [{
    "code" : "pass",
    "display" : "Pass",
    "definition" : "Visual acuity ≥6/9 in both eyes"
  },
  {
    "code" : "refer",
    "display" : "Refer",
    "definition" : "Visual acuity ≤6/12 in either eye OR ≥2 line difference between eyes"
  },
  {
    "code" : "absent",
    "display" : "Absent",
    "definition" : "Child was absent on screening day"
  },
  {
    "code" : "incomplete",
    "display" : "Incomplete",
    "definition" : "Screening could not be completed (uncooperative, one eye only)"
  }]
}

```
