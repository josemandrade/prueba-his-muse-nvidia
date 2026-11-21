# School Nurse Example - Carmen Ruiz - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **School Nurse Example - Carmen Ruiz**

## Example Practitioner: School Nurse Example - Carmen Ruiz

Profile: [School Vision Screening Practitioner](StructureDefinition-svs-practitioner.md)

Carmen Ruiz (official) (urn:oid:1.2.3.4.5.employee#EMP-2026-015)

-------

| | |
| :--- | :--- |
| Other Id: | Provider number/LIC-ENF-2026-004521 |
| Contact Detail | [+34-91-555-0100](tel:+34-91-555-0100) |



## Resource Content

```json
{
  "resourceType" : "Practitioner",
  "id" : "SVSPractitionerNurseExample",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-practitioner"]
  },
  "identifier" : [{
    "system" : "urn:oid:1.2.3.4.5.employee",
    "value" : "EMP-2026-015"
  },
  {
    "type" : {
      "coding" : [{
        "system" : "http://terminology.hl7.org/CodeSystem/v2-0203",
        "code" : "PRN",
        "display" : "Provider number"
      }]
    },
    "system" : "urn:oid:1.2.3.4.5.license",
    "value" : "LIC-ENF-2026-004521"
  }],
  "name" : [{
    "use" : "official",
    "family" : "Ruiz",
    "given" : ["Carmen"]
  }],
  "telecom" : [{
    "system" : "phone",
    "value" : "+34-91-555-0100",
    "use" : "work"
  }]
}

```
