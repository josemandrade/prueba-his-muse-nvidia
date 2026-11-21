# School Vision Screening Questionnaire Response - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **School Vision Screening Questionnaire Response**

## Resource Profile: School Vision Screening Questionnaire Response 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-questionnaire-response-screening | *Version*:0.1.0 |
| Active as of 2026-11-21 | *Computable Name*:SVSQuestionnaireResponseScreening |

 
Screening form response captured by the nurse 

**Usages:**

* This Profile is not used by any profiles in this Specification

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/school-vision-screening|current/StructureDefinition/StructureDefinition-svs-questionnaire-response-screening.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-svs-questionnaire-response-screening.csv), [Excel](StructureDefinition-svs-questionnaire-response-screening.xlsx), [Schematron](StructureDefinition-svs-questionnaire-response-screening.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "svs-questionnaire-response-screening",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-questionnaire-response-screening",
  "version" : "0.1.0",
  "name" : "SVSQuestionnaireResponseScreening",
  "title" : "School Vision Screening Questionnaire Response",
  "status" : "active",
  "experimental" : false,
  "date" : "2026-11-21T14:59:50+00:00",
  "description" : "Screening form response captured by the nurse",
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
  }],
  "kind" : "resource",
  "abstract" : false,
  "type" : "QuestionnaireResponse",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/QuestionnaireResponse",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "QuestionnaireResponse",
      "path" : "QuestionnaireResponse"
    },
    {
      "id" : "QuestionnaireResponse.subject",
      "path" : "QuestionnaireResponse.subject",
      "min" : 1
    },
    {
      "id" : "QuestionnaireResponse.authored",
      "path" : "QuestionnaireResponse.authored",
      "min" : 1
    },
    {
      "id" : "QuestionnaireResponse.author",
      "path" : "QuestionnaireResponse.author",
      "min" : 1
    },
    {
      "id" : "QuestionnaireResponse.item",
      "path" : "QuestionnaireResponse.item",
      "min" : 1
    }]
  }
}

```
