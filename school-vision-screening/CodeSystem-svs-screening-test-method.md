# School Vision Screening Test Methods - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **School Vision Screening Test Methods**

## CodeSystem: School Vision Screening Test Methods 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-screening-test-method | *Version*:0.1.0 |
| Active as of 2026-11-21 | *Computable Name*:SVSScreeningTestMethod |

 
Methods used for visual acuity screening in school settings 

 This Code system is referenced in the content logical definition of the following value sets: 

* [School Vision Screening Test Methods ValueSet](ValueSet-svs-screening-test-method-vs.md)



## Resource Content

```json
{
  "resourceType" : "CodeSystem",
  "id" : "svs-screening-test-method",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/svs-screening-test-method",
  "version" : "0.1.0",
  "name" : "SVSScreeningTestMethod",
  "title" : "School Vision Screening Test Methods",
  "status" : "active",
  "experimental" : false,
  "date" : "2026-11-21T14:59:50+00:00",
  "description" : "Methods used for visual acuity screening in school settings",
  "caseSensitive" : true,
  "content" : "complete",
  "count" : 4,
  "property" : [{
    "code" : "notSelectable",
    "description" : "Indicates that the code is not intended for selection",
    "type" : "boolean"
  }],
  "concept" : [{
    "code" : "snellen",
    "display" : "Snellen 6m chart",
    "definition" : "Snellen chart at 6 metres"
  },
  {
    "code" : "tumbling-e",
    "display" : "Tumbling E optotypes",
    "definition" : "Tumbling E optotypes for children who cannot read letters"
  },
  {
    "code" : "lea-symbols",
    "display" : "Lea symbols",
    "definition" : "Lea symbols for pre-readers"
  },
  {
    "code" : "other",
    "display" : "Other method",
    "definition" : "Other screening method not listed"
  }]
}

```
