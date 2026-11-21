# Primary Care Document Reference (IP-4) - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Primary Care Document Reference (IP-4)**

## Resource Profile: Primary Care Document Reference (IP-4) 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-document-reference-ip4 | *Version*:0.1.0 |
| Active as of 2026-11-21 | *Computable Name*:SVSDocumentReferenceIP4 |

 
DocumentReference for each of the 6 IP-4 document types received by Primary Care 

**Usages:**

* Examples for this Profile: [DocumentReference/SVSDocumentReferenceScreeningPassExample](DocumentReference-SVSDocumentReferenceScreeningPassExample.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/school-vision-screening|current/StructureDefinition/StructureDefinition-svs-document-reference-ip4.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-svs-document-reference-ip4.csv), [Excel](StructureDefinition-svs-document-reference-ip4.xlsx), [Schematron](StructureDefinition-svs-document-reference-ip4.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "svs-document-reference-ip4",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-document-reference-ip4",
  "version" : "0.1.0",
  "name" : "SVSDocumentReferenceIP4",
  "title" : "Primary Care Document Reference (IP-4)",
  "status" : "active",
  "experimental" : false,
  "date" : "2026-11-21T14:59:50+00:00",
  "description" : "DocumentReference for each of the 6 IP-4 document types received by Primary Care",
  "fhirVersion" : "4.0.1",
  "mapping" : [{
    "identity" : "workflow",
    "uri" : "http://hl7.org/fhir/workflow",
    "name" : "Workflow Pattern"
  },
  {
    "identity" : "fhircomposition",
    "uri" : "http://hl7.org/fhir/composition",
    "name" : "FHIR Composition"
  },
  {
    "identity" : "rim",
    "uri" : "http://hl7.org/v3",
    "name" : "RIM Mapping"
  },
  {
    "identity" : "cda",
    "uri" : "http://hl7.org/v3/cda",
    "name" : "CDA (R2)"
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
  },
  {
    "identity" : "xds",
    "uri" : "http://ihe.net/xds",
    "name" : "XDS metadata equivalent"
  }],
  "kind" : "resource",
  "abstract" : false,
  "type" : "DocumentReference",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/DocumentReference",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "DocumentReference",
      "path" : "DocumentReference"
    },
    {
      "id" : "DocumentReference.type",
      "path" : "DocumentReference.type",
      "min" : 1
    },
    {
      "id" : "DocumentReference.category",
      "path" : "DocumentReference.category",
      "min" : 1,
      "max" : "1"
    },
    {
      "id" : "DocumentReference.subject",
      "path" : "DocumentReference.subject",
      "min" : 1
    },
    {
      "id" : "DocumentReference.date",
      "path" : "DocumentReference.date",
      "min" : 1
    },
    {
      "id" : "DocumentReference.author",
      "path" : "DocumentReference.author",
      "min" : 1
    },
    {
      "id" : "DocumentReference.custodian",
      "path" : "DocumentReference.custodian",
      "min" : 1
    },
    {
      "id" : "DocumentReference.description",
      "path" : "DocumentReference.description",
      "min" : 1
    },
    {
      "id" : "DocumentReference.content",
      "path" : "DocumentReference.content",
      "max" : "1"
    },
    {
      "id" : "DocumentReference.content.attachment.url",
      "path" : "DocumentReference.content.attachment.url",
      "min" : 1
    }]
  }
}

```
