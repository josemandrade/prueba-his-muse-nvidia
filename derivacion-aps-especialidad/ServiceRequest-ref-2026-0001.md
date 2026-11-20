# Solicitud de derivación REF-2026-0001 - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Solicitud de derivación REF-2026-0001**

## Example ServiceRequest: Solicitud de derivación REF-2026-0001

Profile: [Solicitud de derivación](StructureDefinition-derivacion-solicitud.md)

**identifier**: `http://aps.losaromos.example.org/referral`/REF-2026-0001

**status**: Active

**intent**: Order

**priority**: Routine

**code**: Cardiology

**subject**: [María González (official) Female, DoB: 1968-04-15 ( http://www.registrocivil.cl/run#11111111-1)](Patient-maria-gonzalez.md)

**encounter**: [Encounter: status = finished; class = Ambulatory (ActCode#AMB); period = 2026-11-19 09:00:00-0300 --> 2026-11-19 09:30:00-0300](Encounter-aps-encounter-2026-11-19.md)

**authoredOn**: 2026-11-19 09:30:00-0300

**requester**: [Ana Pérez (official) (http://www.registrocivil.cl/run#22222222-2): APS doctor at CESFAM Los Aromos (http://aps.losaromos.example.org/organization#CESFAM-LOS-AROMOS)](PractitionerRole-rol-medico-aps.md)

**performerType**: Cardiology

**performer**: [Cardiology (Cardiology) by Servicio de Cardiología (http://especialidad.example.org/organization#CARDIOLOGIA) (http://especialidad.example.org/service#cardiologia)](HealthcareService-servicio-cardiologia.md)

**reasonCode**: Suspected heart failure: exertional dyspnoea, ankle oedema

**supportingInfo**: 

* [Observation EKG study](Observation-ecg-2026-11-19.md)
* [Observation Natriuretic peptide.B prohormone N-Terminal [Mass/volume] in Serum or Plasma](Observation-ntprobnp-2026-11-19.md)

**note**: 

> 

Disnea de esfuerzo y edema de tobillos de dos semanas de evolución.




## Resource Content

```json
{
  "resourceType" : "ServiceRequest",
  "id" : "ref-2026-0001",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-solicitud"]
  },
  "identifier" : [{
    "system" : "http://aps.losaromos.example.org/referral",
    "value" : "REF-2026-0001"
  }],
  "status" : "active",
  "intent" : "order",
  "priority" : "routine",
  "code" : {
    "coding" : [{
      "system" : "https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-especialidad",
      "code" : "cardiologia",
      "display" : "Cardiology"
    }]
  },
  "subject" : {
    "reference" : "Patient/maria-gonzalez"
  },
  "encounter" : {
    "reference" : "Encounter/aps-encounter-2026-11-19"
  },
  "authoredOn" : "2026-11-19T09:30:00-03:00",
  "requester" : {
    "reference" : "PractitionerRole/rol-medico-aps"
  },
  "performerType" : {
    "coding" : [{
      "system" : "https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-especialidad",
      "code" : "cardiologia",
      "display" : "Cardiology"
    }]
  },
  "performer" : [{
    "reference" : "HealthcareService/servicio-cardiologia"
  }],
  "reasonCode" : [{
    "coding" : [{
      "system" : "http://snomed.info/sct",
      "code" : "84114007",
      "display" : "Heart failure (disorder)"
    }],
    "text" : "Suspected heart failure: exertional dyspnoea, ankle oedema"
  }],
  "supportingInfo" : [{
    "reference" : "Observation/ecg-2026-11-19"
  },
  {
    "reference" : "Observation/ntprobnp-2026-11-19"
  }],
  "note" : [{
    "text" : "Disnea de esfuerzo y edema de tobillos de dos semanas de evolución."
  }]
}

```
