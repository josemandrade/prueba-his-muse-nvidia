# Ophthalmology Follow-up Plan - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Ophthalmology Follow-up Plan**

## Resource Profile: Ophthalmology Follow-up Plan 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-care-plan-follow-up | *Version*:0.1.0 |
| Active as of 2026-11-21 | *Computable Name*:SVSCarePlanFollowUp |

 
Follow-up plan from ophthalmology assessment 

**Usages:**

* Examples for this Profile: [CarePlan/SVSCarePlanFollowUpExample](CarePlan-SVSCarePlanFollowUpExample.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/school-vision-screening|current/StructureDefinition/StructureDefinition-svs-care-plan-follow-up.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-svs-care-plan-follow-up.csv), [Excel](StructureDefinition-svs-care-plan-follow-up.xlsx), [Schematron](StructureDefinition-svs-care-plan-follow-up.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "svs-care-plan-follow-up",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-care-plan-follow-up",
  "version" : "0.1.0",
  "name" : "SVSCarePlanFollowUp",
  "title" : "Ophthalmology Follow-up Plan",
  "status" : "active",
  "experimental" : false,
  "date" : "2026-11-21T14:59:50+00:00",
  "description" : "Follow-up plan from ophthalmology assessment",
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
  "type" : "CarePlan",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/CarePlan",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "CarePlan",
      "path" : "CarePlan"
    },
    {
      "id" : "CarePlan.intent",
      "path" : "CarePlan.intent",
      "patternCode" : "plan"
    },
    {
      "id" : "CarePlan.category",
      "path" : "CarePlan.category",
      "min" : 1,
      "max" : "1"
    },
    {
      "id" : "CarePlan.activity",
      "path" : "CarePlan.activity",
      "min" : 1
    }]
  }
}

```
