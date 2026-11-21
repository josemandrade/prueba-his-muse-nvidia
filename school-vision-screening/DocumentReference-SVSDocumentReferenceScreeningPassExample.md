# DocumentReference - Screening Pass Result (IP-4) - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **DocumentReference - Screening Pass Result (IP-4)**

## Example DocumentReference: DocumentReference - Screening Pass Result (IP-4)

Profile: [Primary Care Document Reference (IP-4)](StructureDefinition-svs-document-reference-ip4.md)

**identifier**: `urn:oid:1.2.3.4.5.ip4-doc`/DOC-IP4-2026-11-15-0042-pass

**status**: Current

**type**: Visual acuity screening panel

**category**: Screening Report

**subject**: [Maria Isabel Gonzalez (official) Female, DoB: 2018-03-15 ( PIXm Cross-reference: PIXM-987654321)](Patient-SVSPatientExample.md)

**date**: 2026-11-15 10:00:00+0000

**author**: [Carmen Ruiz (official) (urn:oid:1.2.3.4.5.employee#EMP-2026-015)](Practitioner-SVSPractitionerNurseExample.md)

**custodian**: [Servicio de Salud Escolar de Madrid (Department) (urn:oid:1.2.3.4.5.health-service-id#HSE-MAD-001)](Organization-SVSOrganizationSchoolHealthServiceExample.md)

**description**: Vision screening pass result for Maria Gonzalez (6/9 both eyes)

> **content**

### Attachments

| | |
| :--- | :--- |
| - | **Url** |
| * | [https://school-health.example.org/fhir/Observation/SCR-2026-11-15-0042](https://school-health.example.org/fhir/Observation/SCR-2026-11-15-0042) |


### Contexts

| | | | |
| :--- | :--- | :--- | :--- |
| - | **Encounter** | **Period** | **Related** |
| * | [Encounter: identifier = urn:oid:1.2.3.4.5.encounter-id#ENC-2026-11-15-0042; status = finished; class = Ambulatory (ActCode#AMB); type = Vision Screening; period = 2026-11-15 09:30:00+0000 --> 2026-11-15 09:45:00+0000](Encounter-SVSEncounterScreeningExample.md) | 2026-11-15 09:35:00+0000 --> 2026-11-15 09:35:00+0000 | [Observation Visual acuity screening panel](Observation-SVSObservationScreeningPanelReferExample.md) |



## Resource Content

```json
{
  "resourceType" : "DocumentReference",
  "id" : "SVSDocumentReferenceScreeningPassExample",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-document-reference-ip4"]
  },
  "identifier" : [{
    "system" : "urn:oid:1.2.3.4.5.ip4-doc",
    "value" : "DOC-IP4-2026-11-15-0042-pass"
  }],
  "status" : "current",
  "type" : {
    "coding" : [{
      "system" : "http://loinc.org",
      "code" : "83700-8",
      "display" : "Visual acuity screening panel"
    }]
  },
  "category" : [{
    "coding" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/document-class",
      "code" : "screening-report",
      "display" : "Screening Report"
    }]
  }],
  "subject" : {
    "reference" : "Patient/SVSPatientExample"
  },
  "date" : "2026-11-15T10:00:00Z",
  "author" : [{
    "reference" : "Practitioner/SVSPractitionerNurseExample"
  }],
  "custodian" : {
    "reference" : "Organization/SVSOrganizationSchoolHealthServiceExample"
  },
  "description" : "Vision screening pass result for Maria Gonzalez (6/9 both eyes)",
  "content" : [{
    "attachment" : {
      "url" : "https://school-health.example.org/fhir/Observation/SCR-2026-11-15-0042"
    }
  }],
  "context" : {
    "encounter" : [{
      "reference" : "Encounter/SVSEncounterScreeningExample"
    }],
    "period" : {
      "start" : "2026-11-15T09:35:00Z",
      "end" : "2026-11-15T09:35:00Z"
    },
    "related" : [{
      "reference" : "Observation/SVSObservationScreeningPanelReferExample"
    }]
  }
}

```
