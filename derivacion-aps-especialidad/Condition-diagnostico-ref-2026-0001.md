# Diagnóstico: insuficiencia cardiaca sistólica crónica - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Diagnóstico: insuficiencia cardiaca sistólica crónica**

## Example Condition: Diagnóstico: insuficiencia cardiaca sistólica crónica

Profile: [Diagnóstico de la contrareferencia](StructureDefinition-derivacion-diagnostico.md)

**clinicalStatus**: Active

**verificationStatus**: Confirmed

**code**: Insuficiencia cardiaca sistólica crónica (FEVI 35%)

**subject**: [María González (official) Female, DoB: 1968-04-15 ( http://www.registrocivil.cl/run#11111111-1)](Patient-maria-gonzalez.md)

**encounter**: [Encounter: identifier = http://especialidad.example.org/encounter#ENC-2026-0001; status = planned; class = Ambulatory (ActCode#AMB); serviceType = Cardiology; period = 2026-12-02 10:00:00-0300 --> 2026-12-02 10:30:00-0300](Encounter-encuentro-ref-2026-0001.md)

**note**: 

> 

FEVI 35% por ecocardiograma. Sin isquemia aguda en el ECG.




## Resource Content

```json
{
  "resourceType" : "Condition",
  "id" : "diagnostico-ref-2026-0001",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-diagnostico"]
  },
  "clinicalStatus" : {
    "coding" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/condition-clinical",
      "code" : "active",
      "display" : "Active"
    }]
  },
  "verificationStatus" : {
    "coding" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/condition-ver-status",
      "code" : "confirmed",
      "display" : "Confirmed"
    }]
  },
  "code" : {
    "coding" : [{
      "system" : "http://hl7.org/fhir/sid/icd-10-cm",
      "code" : "I50.22",
      "display" : "Chronic systolic (congestive) heart failure"
    },
    {
      "system" : "http://snomed.info/sct",
      "code" : "417996009",
      "display" : "Systolic heart failure"
    }],
    "text" : "Insuficiencia cardiaca sistólica crónica (FEVI 35%)"
  },
  "subject" : {
    "reference" : "Patient/maria-gonzalez"
  },
  "encounter" : {
    "reference" : "Encounter/encuentro-ref-2026-0001"
  },
  "note" : [{
    "text" : "FEVI 35% por ecocardiograma. Sin isquemia aguda en el ECG."
  }]
}

```
