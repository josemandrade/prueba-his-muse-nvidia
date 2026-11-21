# School Example - Colegio Publico San Isidro - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **School Example - Colegio Publico San Isidro**

## Example Organization: School Example - Colegio Publico San Isidro

Profile: [School Vision Screening Organization](StructureDefinition-svs-organization.md)

Colegio Publico San Isidro (Educational facility) (urn:oid:1.2.3.4.5.school-id#SCH-28079-01)

-------

| | |
| :--- | :--- |
| Type: | Educational facility |
| Contact Detail | * [+34-91-555-0100](tel:+34-91-555-0100)
* Calle Principal 123 Madrid 28001 ES (work)
 |



## Resource Content

```json
{
  "resourceType" : "Organization",
  "id" : "SVSOrganizationSchoolExample",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-organization"]
  },
  "identifier" : [{
    "system" : "urn:oid:1.2.3.4.5.school-id",
    "value" : "SCH-28079-01"
  }],
  "type" : [{
    "coding" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/organization-type",
      "code" : "edu",
      "display" : "Educational facility"
    }]
  }],
  "name" : "Colegio Publico San Isidro",
  "telecom" : [{
    "system" : "phone",
    "value" : "+34-91-555-0100"
  }],
  "address" : [{
    "use" : "work",
    "line" : ["Calle Principal 123"],
    "city" : "Madrid",
    "postalCode" : "28001",
    "country" : "ES"
  }]
}

```
