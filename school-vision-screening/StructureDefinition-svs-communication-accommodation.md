# Teacher Accommodation Notice - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Teacher Accommodation Notice**

## Resource Profile: Teacher Accommodation Notice 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-communication-accommodation | *Version*:0.1.0 |
| Active as of 2026-11-21 | *Computable Name*:SVSCommunicationAccommodation |

 
Notice from school nurse to teacher about classroom accommodation 

**Usages:**

* This Profile is not used by any profiles in this Specification

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/school-vision-screening|current/StructureDefinition/StructureDefinition-svs-communication-accommodation.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-svs-communication-accommodation.csv), [Excel](StructureDefinition-svs-communication-accommodation.xlsx), [Schematron](StructureDefinition-svs-communication-accommodation.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "svs-communication-accommodation",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-communication-accommodation",
  "version" : "0.1.0",
  "name" : "SVSCommunicationAccommodation",
  "title" : "Teacher Accommodation Notice",
  "status" : "active",
  "experimental" : false,
  "date" : "2026-11-21T14:59:50+00:00",
  "description" : "Notice from school nurse to teacher about classroom accommodation",
  "fhirVersion" : "4.0.1",
  "mapping" : [{
    "identity" : "workflow",
    "uri" : "http://hl7.org/fhir/workflow",
    "name" : "Workflow Pattern"
  },
  {
    "identity" : "w5",
    "uri" : "http://hl7.org/fhir/fivews",
    "name" : "FiveWs Pattern Mapping"
  },
  {
    "identity" : "rim",
    "uri" : "http://hl7.org/v3",
    "name" : "RIM Mapping"
  }],
  "kind" : "resource",
  "abstract" : false,
  "type" : "Communication",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/Communication",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "Communication",
      "path" : "Communication"
    },
    {
      "id" : "Communication.category",
      "path" : "Communication.category",
      "min" : 1,
      "max" : "1"
    },
    {
      "id" : "Communication.subject",
      "path" : "Communication.subject",
      "min" : 1
    },
    {
      "id" : "Communication.sent",
      "path" : "Communication.sent",
      "min" : 1
    },
    {
      "id" : "Communication.sender",
      "path" : "Communication.sender",
      "min" : 1
    },
    {
      "id" : "Communication.payload",
      "path" : "Communication.payload",
      "min" : 1,
      "max" : "1"
    },
    {
      "id" : "Communication.payload.content[x]",
      "path" : "Communication.payload.content[x]",
      "slicing" : {
        "discriminator" : [{
          "type" : "type",
          "path" : "$this"
        }],
        "ordered" : false,
        "rules" : "open"
      }
    },
    {
      "id" : "Communication.payload.content[x]:contentString",
      "path" : "Communication.payload.content[x]",
      "sliceName" : "contentString",
      "min" : 1,
      "max" : "1",
      "type" : [{
        "code" : "string"
      }]
    }]
  }
}

```
