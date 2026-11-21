# Primary Care Example - Centro de Salud Las Rosas - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Primary Care Example - Centro de Salud Las Rosas**

## Example Organization: Primary Care Example - Centro de Salud Las Rosas

Profile: [School Vision Screening Organization](StructureDefinition-svs-organization.md)

Centro de Salud Las Rosas (Healthcare Provider) (urn:oid:1.2.3.4.5.primary-care-id#CS-28079-05)

-------

| | |
| :--- | :--- |
| Type: | Healthcare Provider |
| Contact Detail | * [+34-91-555-0300](tel:+34-91-555-0300)
* Calle de las Rosas 10 Madrid 28003 ES (work)
 |



## Resource Content

```json
{
  "resourceType" : "Organization",
  "id" : "SVSOrganizationPrimaryCareExample",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-organization"]
  },
  "identifier" : [{
    "system" : "urn:oid:1.2.3.4.5.primary-care-id",
    "value" : "CS-28079-05"
  }],
  "type" : [{
    "coding" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/organization-type",
      "code" : "prov",
      "display" : "Healthcare Provider"
    }]
  }],
  "name" : "Centro de Salud Las Rosas",
  "telecom" : [{
    "system" : "phone",
    "value" : "+34-91-555-0300"
  }],
  "address" : [{
    "use" : "work",
    "line" : ["Calle de las Rosas 10"],
    "city" : "Madrid",
    "postalCode" : "28003",
    "country" : "ES"
  }]
}

```
