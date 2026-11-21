# School Vision Screening Practitioner - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **School Vision Screening Practitioner**

## Resource Profile: School Vision Screening Practitioner 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-practitioner | *Version*:0.1.0 |
| Active as of 2026-11-21 | *Computable Name*:SVSPractitioner |

 
Base profile for practitioners in the school vision screening program 

**Usages:**

* Examples for this Profile: [Practitioner/SVSPractitionerNurseExample](Practitioner-SVSPractitionerNurseExample.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/school-vision-screening|current/StructureDefinition/StructureDefinition-svs-practitioner.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-svs-practitioner.csv), [Excel](StructureDefinition-svs-practitioner.xlsx), [Schematron](StructureDefinition-svs-practitioner.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "svs-practitioner",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-practitioner",
  "version" : "0.1.0",
  "name" : "SVSPractitioner",
  "title" : "School Vision Screening Practitioner",
  "status" : "active",
  "experimental" : false,
  "date" : "2026-11-21T14:59:50+00:00",
  "description" : "Base profile for practitioners in the school vision screening program",
  "fhirVersion" : "4.0.1",
  "mapping" : [{
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
    "identity" : "servd",
    "uri" : "http://www.omg.org/spec/ServD/1.0/",
    "name" : "ServD"
  },
  {
    "identity" : "w5",
    "uri" : "http://hl7.org/fhir/fivews",
    "name" : "FiveWs Pattern Mapping"
  }],
  "kind" : "resource",
  "abstract" : false,
  "type" : "Practitioner",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/Practitioner",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "Practitioner",
      "path" : "Practitioner"
    }]
  }
}

```
