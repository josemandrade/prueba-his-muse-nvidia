# Primary Care Vision Screening Document Log - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Primary Care Vision Screening Document Log**

## Resource Profile: Primary Care Vision Screening Document Log 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-list-primary-care-documents | *Version*:0.1.0 |
| Active as of 2026-11-21 | *Computable Name*:SVSListPrimaryCareDocuments |

 
List of all vision screening related documents received by Primary Care for a child 

**Usages:**

* Examples for this Profile: [List/SVSListPrimaryCareDocumentsExample](List-SVSListPrimaryCareDocumentsExample.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/school-vision-screening|current/StructureDefinition/StructureDefinition-svs-list-primary-care-documents.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-svs-list-primary-care-documents.csv), [Excel](StructureDefinition-svs-list-primary-care-documents.xlsx), [Schematron](StructureDefinition-svs-list-primary-care-documents.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "svs-list-primary-care-documents",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-list-primary-care-documents",
  "version" : "0.1.0",
  "name" : "SVSListPrimaryCareDocuments",
  "title" : "Primary Care Vision Screening Document Log",
  "status" : "active",
  "experimental" : false,
  "date" : "2026-11-21T14:59:50+00:00",
  "description" : "List of all vision screening related documents received by Primary Care for a child",
  "fhirVersion" : "4.0.1",
  "mapping" : [{
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
  "type" : "List",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/List",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "List",
      "path" : "List"
    },
    {
      "id" : "List.title",
      "path" : "List.title",
      "min" : 1
    },
    {
      "id" : "List.subject",
      "path" : "List.subject",
      "min" : 1
    }]
  }
}

```
