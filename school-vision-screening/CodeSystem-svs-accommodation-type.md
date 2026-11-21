# Classroom Accommodation Types - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Classroom Accommodation Types**

## CodeSystem: Classroom Accommodation Types 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-accommodation-type | *Version*:0.1.0 |
| Active as of 2026-11-21 | *Computable Name*:SVSAccommodationType |

 
Types of classroom accommodations for vision impairment 

 This Code system is referenced in the content logical definition of the following value sets: 

* [Classroom Accommodation Types ValueSet](ValueSet-svs-accommodation-type-vs.md)



## Resource Content

```json
{
  "resourceType" : "CodeSystem",
  "id" : "svs-accommodation-type",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-accommodation-type",
  "version" : "0.1.0",
  "name" : "SVSAccommodationType",
  "title" : "Classroom Accommodation Types",
  "status" : "active",
  "experimental" : false,
  "date" : "2026-11-21T14:59:50+00:00",
  "description" : "Types of classroom accommodations for vision impairment",
  "caseSensitive" : true,
  "content" : "complete",
  "count" : 4,
  "concept" : [{
    "code" : "glasses",
    "display" : "Glasses needed",
    "definition" : "Child requires prescription glasses"
  },
  {
    "code" : "front-seat",
    "display" : "Front seat",
    "definition" : "Child needs front row seating"
  },
  {
    "code" : "both",
    "display" : "Glasses and front seat",
    "definition" : "Child needs both glasses and front seat"
  },
  {
    "code" : "other",
    "display" : "Other accommodation",
    "definition" : "Other classroom accommodation"
  }]
}

```
