# School Vision Screening Organization - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **School Vision Screening Organization**

## Resource Profile: School Vision Screening Organization 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-organization | *Version*:0.1.0 |
| Active as of 2026-11-21 | *Computable Name*:SVSOrganization |

 
Organization profile for School Health Service, Ophthalmology Clinic, or Primary Care Practice 

**Usages:**

* Examples for this Profile: [Clinica Oftalmologica Central](Organization-SVSOrganizationClinicExample.md), [Centro de Salud Las Rosas](Organization-SVSOrganizationPrimaryCareExample.md), [Colegio Publico San Isidro](Organization-SVSOrganizationSchoolExample.md) and [Servicio de Salud Escolar de Madrid](Organization-SVSOrganizationSchoolHealthServiceExample.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/school-vision-screening|current/StructureDefinition/StructureDefinition-svs-organization.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-svs-organization.csv), [Excel](StructureDefinition-svs-organization.xlsx), [Schematron](StructureDefinition-svs-organization.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "svs-organization",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-organization",
  "version" : "0.1.0",
  "name" : "SVSOrganization",
  "title" : "School Vision Screening Organization",
  "status" : "active",
  "experimental" : false,
  "date" : "2026-11-21T14:59:50+00:00",
  "description" : "Organization profile for School Health Service, Ophthalmology Clinic, or Primary Care Practice",
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
  "type" : "Organization",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/Organization",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "Organization",
      "path" : "Organization"
    },
    {
      "id" : "Organization.identifier",
      "path" : "Organization.identifier",
      "min" : 1
    },
    {
      "id" : "Organization.type",
      "path" : "Organization.type",
      "max" : "1"
    },
    {
      "id" : "Organization.name",
      "path" : "Organization.name",
      "min" : 1
    }]
  }
}

```
