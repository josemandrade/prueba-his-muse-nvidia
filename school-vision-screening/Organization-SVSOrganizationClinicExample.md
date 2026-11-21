# Ophthalmology Clinic Example - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Ophthalmology Clinic Example**

## Example Organization: Ophthalmology Clinic Example

Profile: [School Vision Screening Organization](StructureDefinition-svs-organization.md)

Clinica Oftalmologica Central (Healthcare Provider) (urn:oid:1.2.3.4.5.clinic-id#CLI-OPT-2026-001)

-------

| | |
| :--- | :--- |
| Type: | Healthcare Provider |
| Contact Detail | * [+34-91-444-0200](tel:+34-91-444-0200)
* Avenida de la Salud 45 Madrid 28002 ES (work)
 |



## Resource Content

```json
{
  "resourceType" : "Organization",
  "id" : "SVSOrganizationClinicExample",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-organization"]
  },
  "identifier" : [{
    "system" : "urn:oid:1.2.3.4.5.clinic-id",
    "value" : "CLI-OPT-2026-001"
  }],
  "type" : [{
    "coding" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/organization-type",
      "code" : "prov",
      "display" : "Healthcare Provider"
    }]
  }],
  "name" : "Clinica Oftalmologica Central",
  "telecom" : [{
    "system" : "phone",
    "value" : "+34-91-444-0200"
  }],
  "address" : [{
    "use" : "work",
    "line" : ["Avenida de la Salud 45"],
    "city" : "Madrid",
    "postalCode" : "28002",
    "country" : "ES"
  }]
}

```
