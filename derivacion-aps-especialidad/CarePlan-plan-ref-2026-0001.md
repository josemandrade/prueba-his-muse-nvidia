# Plan de seguimiento para APS - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Plan de seguimiento para APS**

## Example CarePlan: Plan de seguimiento para APS

Profile: [Plan de seguimiento para APS](StructureDefinition-derivacion-plan-seguimiento.md)

**status**: Active

**intent**: Plan

**subject**: [María González (official) Female, DoB: 1968-04-15 ( http://www.registrocivil.cl/run#11111111-1)](Patient-maria-gonzalez.md)

**encounter**: [Encounter: identifier = http://especialidad.example.org/encounter#ENC-2026-0001; status = planned; class = Ambulatory (ActCode#AMB); serviceType = Cardiology; period = 2026-12-02 10:00:00-0300 --> 2026-12-02 10:30:00-0300](Encounter-encuentro-ref-2026-0001.md)

**author**: [Carlos Rojas (official) (http://www.registrocivil.cl/run#33333333-3): Specialist at Servicio de Cardiología (http://especialidad.example.org/organization#CARDIOLOGIA)](PractitionerRole-rol-especialista.md)

**addresses**: [Condition Insuficiencia cardiaca sistólica crónica (FEVI 35%)](Condition-diagnostico-ref-2026-0001.md)

> **activity**

### Details

| | | |
| :--- | :--- | :--- |
| - | **Status** | **Description** |
| * | active | Control en APS en 2 semanas: presión arterial, peso, síntomas. |


> **activity**

### Details

| | | |
| :--- | :--- | :--- |
| - | **Status** | **Description** |
| * | active | NT-proBNP de control en 3 meses. |


> **activity****reference**: [ServiceRequest Cardiology](ServiceRequest-ref-2026-0001.md)



## Resource Content

```json
{
  "resourceType" : "CarePlan",
  "id" : "plan-ref-2026-0001",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-plan-seguimiento"]
  },
  "status" : "active",
  "intent" : "plan",
  "subject" : {
    "reference" : "Patient/maria-gonzalez"
  },
  "encounter" : {
    "reference" : "Encounter/encuentro-ref-2026-0001"
  },
  "author" : {
    "reference" : "PractitionerRole/rol-especialista"
  },
  "addresses" : [{
    "reference" : "Condition/diagnostico-ref-2026-0001"
  }],
  "activity" : [{
    "detail" : {
      "status" : "active",
      "description" : "Control en APS en 2 semanas: presión arterial, peso, síntomas."
    }
  },
  {
    "detail" : {
      "status" : "active",
      "description" : "NT-proBNP de control en 3 meses."
    }
  },
  {
    "reference" : {
      "reference" : "ServiceRequest/ref-2026-0001"
    }
  }]
}

```
