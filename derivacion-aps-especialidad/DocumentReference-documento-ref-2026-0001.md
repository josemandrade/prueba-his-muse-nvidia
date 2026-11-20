# Documento de contrareferencia REF-2026-0001 - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Documento de contrareferencia REF-2026-0001**

## Example DocumentReference: Documento de contrareferencia REF-2026-0001

Profile: [Documento de contrareferencia](StructureDefinition-derivacion-documento.md)

**masterIdentifier**: `http://especialidad.example.org/counter-referral`/CR-2026-0001

**status**: Current

**type**: Consult note

**subject**: [María González (official) Female, DoB: 1968-04-15 ( http://www.registrocivil.cl/run#11111111-1)](Patient-maria-gonzalez.md)

**date**: 2026-12-03 10:00:00-0300

**author**: [Carlos Rojas (official) (http://www.registrocivil.cl/run#33333333-3): Specialist at Servicio de Cardiología (http://especialidad.example.org/organization#CARDIOLOGIA)](PractitionerRole-rol-especialista.md)

> **content**

### Attachments

| | | |
| :--- | :--- | :--- |
| - | **ContentType** | **Url** |
| * | application/fhir+json | [Composition Counter-referral](Composition-contrareferencia-ref-2026-0001.md) |


### Contexts

| | | | |
| :--- | :--- | :--- | :--- |
| - | **Encounter** | **Period** | **Related** |
| * | [Encounter: identifier = http://especialidad.example.org/encounter#ENC-2026-0001; status = planned; class = Ambulatory (ActCode#AMB); serviceType = Cardiology; period = 2026-12-02 10:00:00-0300 --> 2026-12-02 10:30:00-0300](Encounter-encuentro-ref-2026-0001.md) | 2026-12-02 10:00:00-0300 --> 2026-12-02 10:30:00-0300 | [ServiceRequest Cardiology](ServiceRequest-ref-2026-0001.md) |



## Resource Content

```json
{
  "resourceType" : "DocumentReference",
  "id" : "documento-ref-2026-0001",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-documento"]
  },
  "masterIdentifier" : {
    "system" : "http://especialidad.example.org/counter-referral",
    "value" : "CR-2026-0001"
  },
  "status" : "current",
  "type" : {
    "coding" : [{
      "system" : "http://loinc.org",
      "code" : "11488-4",
      "display" : "Consult note"
    }]
  },
  "subject" : {
    "reference" : "Patient/maria-gonzalez"
  },
  "date" : "2026-12-03T10:00:00-03:00",
  "author" : [{
    "reference" : "PractitionerRole/rol-especialista"
  }],
  "content" : [{
    "attachment" : {
      "contentType" : "application/fhir+json",
      "url" : "Composition/contrareferencia-ref-2026-0001"
    }
  }],
  "context" : {
    "encounter" : [{
      "reference" : "Encounter/encuentro-ref-2026-0001"
    }],
    "period" : {
      "start" : "2026-12-02T10:00:00-03:00",
      "end" : "2026-12-02T10:30:00-03:00"
    },
    "related" : [{
      "reference" : "ServiceRequest/ref-2026-0001"
    }]
  }
}

```
