# School Health Service - Servicio de Salud Escolar Madrid - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **School Health Service - Servicio de Salud Escolar Madrid**

## Example Organization: School Health Service - Servicio de Salud Escolar Madrid

Profile: [School Vision Screening Organization](StructureDefinition-svs-organization.md)

Servicio de Salud Escolar de Madrid (Department) (urn:oid:1.2.3.4.5.health-service-id#HSE-MAD-001)

-------

| | |
| :--- | :--- |
| Type: | Department |
| Contact Detail | * [+34-91-555-0101](tel:+34-91-555-0101)
* Calle Salud Publica 5 Madrid 28004 ES (work)
 |



## Resource Content

```json
{
  "resourceType" : "Organization",
  "id" : "SVSOrganizationSchoolHealthServiceExample",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-organization"]
  },
  "identifier" : [{
    "system" : "urn:oid:1.2.3.4.5.health-service-id",
    "value" : "HSE-MAD-001"
  }],
  "type" : [{
    "coding" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/organization-type",
      "code" : "dept",
      "display" : "Department"
    }]
  }],
  "name" : "Servicio de Salud Escolar de Madrid",
  "telecom" : [{
    "system" : "phone",
    "value" : "+34-91-555-0101"
  }],
  "address" : [{
    "use" : "work",
    "line" : ["Calle Salud Publica 5"],
    "city" : "Madrid",
    "postalCode" : "28004",
    "country" : "ES"
  }]
}

```
