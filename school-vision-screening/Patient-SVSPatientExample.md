# Child Example - Maria Gonzalez - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Child Example - Maria Gonzalez**

## Example Patient: Child Example - Maria Gonzalez

Profile: [School Vision Screening Patient (Child)](StructureDefinition-svs-patient.md)

Maria Isabel Gonzalez (official) Female, DoB: 2018-03-15 ( PIXm Cross-reference: PIXM-987654321)

-------

| | |
| :--- | :--- |
| Other Ids: | * `urn:oid:1.2.3.4.5.school-roll`/SCL-2026-0042
* National unique individual identifier/NHS-1234567890 (use: official)
 |
| Contact Detail | * [+34-91-555-0123](tel:+34-91-555-0123)
* Calle Principal 123 Madrid 28001 ES (home)
 |
| Links: | * Managing Organization: [Colegio Publico San Isidro (Educational facility) (urn:oid:1.2.3.4.5.school-id#SCH-28079-01)](Organization-SVSOrganizationSchoolExample.md)
 |



## Resource Content

```json
{
  "resourceType" : "Patient",
  "id" : "SVSPatientExample",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-patient"]
  },
  "identifier" : [{
    "system" : "urn:oid:1.2.3.4.5.school-roll",
    "value" : "SCL-2026-0042"
  },
  {
    "use" : "official",
    "type" : {
      "coding" : [{
        "system" : "http://terminology.hl7.org/CodeSystem/v2-0203",
        "code" : "NI",
        "display" : "National unique individual identifier"
      }]
    },
    "system" : "http://terminology.hl7.org/CodeSystem/v2-0203",
    "value" : "NHS-1234567890"
  },
  {
    "type" : {
      "coding" : [{
        "system" : "http://terminology.hl7.org/CodeSystem/v2-0203",
        "code" : "PIXM",
        "display" : "PIXm Cross-reference"
      }]
    },
    "system" : "urn:ihe:pixm:cross-ref",
    "value" : "PIXM-987654321"
  }],
  "name" : [{
    "use" : "official",
    "family" : "Gonzalez",
    "given" : ["Maria", "Isabel"]
  }],
  "telecom" : [{
    "system" : "phone",
    "value" : "+34-91-555-0123",
    "use" : "home"
  }],
  "gender" : "female",
  "birthDate" : "2018-03-15",
  "address" : [{
    "use" : "home",
    "line" : ["Calle Principal 123"],
    "city" : "Madrid",
    "postalCode" : "28001",
    "country" : "ES"
  }],
  "managingOrganization" : {
    "reference" : "Organization/SVSOrganizationSchoolExample"
  }
}

```
