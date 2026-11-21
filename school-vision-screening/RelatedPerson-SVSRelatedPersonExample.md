# Parent Example - Ana Gonzalez - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Parent Example - Ana Gonzalez**

## Example RelatedPerson: Parent Example - Ana Gonzalez

Profile: [School Vision Screening Parent/Guardian](StructureDefinition-svs-related-person.md)

Ana Maria Gonzalez (official) - Mother (urn:oid:1.2.3.4.5.guardian#GRD-2026-0042)

-------

| | |
| :--- | :--- |
| Patient: | [Maria Isabel Gonzalez (official) Female, DoB: 2018-03-15 ( PIXm Cross-reference: PIXM-987654321)](Patient-SVSPatientExample.md) |
| Relationship: | Mother |
| Contact Detail | [+34-91-555-0123](tel:+34-91-555-0123) |



## Resource Content

```json
{
  "resourceType" : "RelatedPerson",
  "id" : "SVSRelatedPersonExample",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-related-person"]
  },
  "identifier" : [{
    "system" : "urn:oid:1.2.3.4.5.guardian",
    "value" : "GRD-2026-0042"
  }],
  "patient" : {
    "reference" : "Patient/SVSPatientExample"
  },
  "relationship" : [{
    "coding" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/v2-0131",
      "code" : "MTH",
      "display" : "Mother"
    }]
  }],
  "name" : [{
    "use" : "official",
    "family" : "Gonzalez",
    "given" : ["Ana", "Maria"]
  }],
  "telecom" : [{
    "system" : "phone",
    "value" : "+34-91-555-0123",
    "use" : "home"
  }]
}

```
