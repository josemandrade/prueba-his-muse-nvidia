# School Vision Screening Panel - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **School Vision Screening Panel**

## Resource Profile: School Vision Screening Panel 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-screening-panel | *Version*:0.1.0 |
| Active as of 2026-11-21 | *Computable Name*:SVSObservationScreeningPanel |

 
Panel observation containing right and left eye visual acuity measurements 

**Usages:**

* Examples for this Profile: [Observation/SVSObservationScreeningPanelReferExample](Observation-SVSObservationScreeningPanelReferExample.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/school-vision-screening|current/StructureDefinition/StructureDefinition-svs-observation-screening-panel.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-svs-observation-screening-panel.csv), [Excel](StructureDefinition-svs-observation-screening-panel.xlsx), [Schematron](StructureDefinition-svs-observation-screening-panel.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "svs-observation-screening-panel",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-observation-screening-panel",
  "version" : "0.1.0",
  "name" : "SVSObservationScreeningPanel",
  "title" : "School Vision Screening Panel",
  "status" : "active",
  "experimental" : false,
  "date" : "2026-11-21T14:59:50+00:00",
  "description" : "Panel observation containing right and left eye visual acuity measurements",
  "fhirVersion" : "4.0.1",
  "mapping" : [{
    "identity" : "workflow",
    "uri" : "http://hl7.org/fhir/workflow",
    "name" : "Workflow Pattern"
  },
  {
    "identity" : "sct-concept",
    "uri" : "http://snomed.info/conceptdomain",
    "name" : "SNOMED CT Concept Domain Binding"
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
    "identity" : "sct-attr",
    "uri" : "http://snomed.org/attributebinding",
    "name" : "SNOMED CT Attribute Binding"
  }],
  "kind" : "resource",
  "abstract" : false,
  "type" : "Observation",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/Observation",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "Observation",
      "path" : "Observation"
    },
    {
      "id" : "Observation.category",
      "path" : "Observation.category",
      "min" : 1
    },
    {
      "id" : "Observation.subject",
      "path" : "Observation.subject",
      "min" : 1
    },
    {
      "id" : "Observation.performer",
      "path" : "Observation.performer",
      "min" : 1
    },
    {
      "id" : "Observation.hasMember",
      "path" : "Observation.hasMember",
      "min" : 2,
      "max" : "2"
    }]
  }
}

```
