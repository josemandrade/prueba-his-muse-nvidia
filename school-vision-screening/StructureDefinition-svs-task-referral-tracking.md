# School Vision Screening Referral Tracking - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **School Vision Screening Referral Tracking**

## Resource Profile: School Vision Screening Referral Tracking 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-task-referral-tracking | *Version*:0.1.0 |
| Active as of 2026-11-21 | *Computable Name*:SVSTaskReferralTracking |

 
Task for tracking referral workflow state 

**Usages:**

* This Profile is not used by any profiles in this Specification

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/school-vision-screening|current/StructureDefinition/StructureDefinition-svs-task-referral-tracking.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-svs-task-referral-tracking.csv), [Excel](StructureDefinition-svs-task-referral-tracking.xlsx), [Schematron](StructureDefinition-svs-task-referral-tracking.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "svs-task-referral-tracking",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-task-referral-tracking",
  "version" : "0.1.0",
  "name" : "SVSTaskReferralTracking",
  "title" : "School Vision Screening Referral Tracking",
  "status" : "active",
  "experimental" : false,
  "date" : "2026-11-21T14:59:50+00:00",
  "description" : "Task for tracking referral workflow state",
  "fhirVersion" : "4.0.1",
  "mapping" : [{
    "identity" : "workflow",
    "uri" : "http://hl7.org/fhir/workflow",
    "name" : "Workflow Pattern"
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
    "identity" : "v2",
    "uri" : "http://hl7.org/v2",
    "name" : "HL7 v2 Mapping"
  }],
  "kind" : "resource",
  "abstract" : false,
  "type" : "Task",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/Task",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "Task",
      "path" : "Task"
    },
    {
      "id" : "Task.intent",
      "path" : "Task.intent",
      "patternCode" : "order"
    },
    {
      "id" : "Task.code",
      "path" : "Task.code",
      "min" : 1
    },
    {
      "id" : "Task.focus",
      "path" : "Task.focus",
      "min" : 1
    },
    {
      "id" : "Task.for",
      "path" : "Task.for",
      "min" : 1
    },
    {
      "id" : "Task.authoredOn",
      "path" : "Task.authoredOn",
      "min" : 1
    },
    {
      "id" : "Task.lastModified",
      "path" : "Task.lastModified",
      "min" : 1
    },
    {
      "id" : "Task.requester",
      "path" : "Task.requester",
      "min" : 1
    },
    {
      "id" : "Task.owner",
      "path" : "Task.owner",
      "min" : 1
    }]
  }
}

```
