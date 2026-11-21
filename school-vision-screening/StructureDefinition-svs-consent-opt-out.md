# School Vision Screening Opt-Out Consent - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **School Vision Screening Opt-Out Consent**

## Resource Profile: School Vision Screening Opt-Out Consent 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-consent-opt-out | *Version*:0.1.0 |
| Active as of 2026-11-21 | *Computable Name*:SVSConsentOptOut |

 
Annual opt-out consent for vision screening program 

**Usages:**

* This Profile is not used by any profiles in this Specification

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/school-vision-screening|current/StructureDefinition/StructureDefinition-svs-consent-opt-out.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-svs-consent-opt-out.csv), [Excel](StructureDefinition-svs-consent-opt-out.xlsx), [Schematron](StructureDefinition-svs-consent-opt-out.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "svs-consent-opt-out",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-consent-opt-out",
  "version" : "0.1.0",
  "name" : "SVSConsentOptOut",
  "title" : "School Vision Screening Opt-Out Consent",
  "status" : "active",
  "experimental" : false,
  "date" : "2026-11-21T14:59:50+00:00",
  "description" : "Annual opt-out consent for vision screening program",
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
  }],
  "kind" : "resource",
  "abstract" : false,
  "type" : "Consent",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/Consent",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "Consent",
      "path" : "Consent"
    },
    {
      "id" : "Consent.category",
      "path" : "Consent.category",
      "max" : "1"
    },
    {
      "id" : "Consent.patient",
      "path" : "Consent.patient",
      "min" : 1
    },
    {
      "id" : "Consent.dateTime",
      "path" : "Consent.dateTime",
      "min" : 1
    },
    {
      "id" : "Consent.performer",
      "path" : "Consent.performer",
      "min" : 1,
      "max" : "1"
    },
    {
      "id" : "Consent.organization",
      "path" : "Consent.organization",
      "min" : 1,
      "max" : "1"
    }]
  }
}

```
