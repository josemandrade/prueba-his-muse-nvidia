# Screening Encounter - Maria Gonzalez - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Screening Encounter - Maria Gonzalez**

## Example Encounter: Screening Encounter - Maria Gonzalez

**identifier**: `urn:oid:1.2.3.4.5.encounter-id`/ENC-2026-11-15-0042

**status**: Finished

**class**: [ActCode: AMB](http://terminology.hl7.org/7.5.0/CodeSystem-v3-ActCode.html#v3-ActCode-AMB) (Ambulatory)

**type**: Vision Screening

**subject**: [Maria Isabel Gonzalez (official) Female, DoB: 2018-03-15 ( PIXm Cross-reference: PIXM-987654321)](Patient-SVSPatientExample.md)

### Participants

| | | |
| :--- | :--- | :--- |
| - | **Type** | **Individual** |
| * | Primary performer | [Carmen Ruiz (official) (urn:oid:1.2.3.4.5.employee#EMP-2026-015)](Practitioner-SVSPractitionerNurseExample.md) |

**period**: 2026-11-15 09:30:00+0000 --> 2026-11-15 09:45:00+0000

**serviceProvider**: [Servicio de Salud Escolar de Madrid (Department) (urn:oid:1.2.3.4.5.health-service-id#HSE-MAD-001)](Organization-SVSOrganizationSchoolHealthServiceExample.md)



## Resource Content

```json
{
  "resourceType" : "Encounter",
  "id" : "SVSEncounterScreeningExample",
  "identifier" : [{
    "system" : "urn:oid:1.2.3.4.5.encounter-id",
    "value" : "ENC-2026-11-15-0042"
  }],
  "status" : "finished",
  "class" : {
    "system" : "http://terminology.hl7.org/CodeSystem/v3-ActCode",
    "code" : "AMB",
    "display" : "Ambulatory"
  },
  "type" : [{
    "coding" : [{
      "system" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/encounter-type",
      "code" : "vision-screening",
      "display" : "Vision Screening"
    }]
  }],
  "subject" : {
    "reference" : "Patient/SVSPatientExample"
  },
  "participant" : [{
    "type" : [{
      "coding" : [{
        "system" : "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
        "code" : "PPRF",
        "display" : "Primary performer"
      }]
    }],
    "individual" : {
      "reference" : "Practitioner/SVSPractitionerNurseExample"
    }
  }],
  "period" : {
    "start" : "2026-11-15T09:30:00Z",
    "end" : "2026-11-15T09:45:00Z"
  },
  "serviceProvider" : {
    "reference" : "Organization/SVSOrganizationSchoolHealthServiceExample"
  }
}

```
