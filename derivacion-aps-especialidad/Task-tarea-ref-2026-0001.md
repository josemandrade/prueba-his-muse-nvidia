# Tarea de derivación REF-2026-0001 (requested) - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Tarea de derivación REF-2026-0001 (requested)**

## Example Task: Tarea de derivación REF-2026-0001 (requested)

Profile: [Tarea de derivación (registro de estado)](StructureDefinition-derivacion-tarea.md)

**Plazo de aceptación**: 2026-11-26 17:00:00-0300

**identifier**: `http://aps.losaromos.example.org/referral`/REF-2026-0001

**status**: Requested

**businessStatus**: Requested

**intent**: order

**code**: Referral workflow

**description**: acceptance decision

**focus**: [ServiceRequest Cardiology](ServiceRequest-ref-2026-0001.md)

**for**: [María González (official) Female, DoB: 1968-04-15 ( http://www.registrocivil.cl/run#11111111-1)](Patient-maria-gonzalez.md)

**authoredOn**: 2026-11-19 09:30:00-0300

**lastModified**: 2026-11-19 09:30:00-0300

**requester**: [Ana Pérez (official) (http://www.registrocivil.cl/run#22222222-2): APS doctor at CESFAM Los Aromos (http://aps.losaromos.example.org/organization#CESFAM-LOS-AROMOS)](PractitionerRole-rol-medico-aps.md)



## Resource Content

```json
{
  "resourceType" : "Task",
  "id" : "tarea-ref-2026-0001",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-tarea"]
  },
  "extension" : [{
    "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-sla-acceptance-deadline",
    "valueDateTime" : "2026-11-26T17:00:00-03:00"
  }],
  "identifier" : [{
    "system" : "http://aps.losaromos.example.org/referral",
    "value" : "REF-2026-0001"
  }],
  "status" : "requested",
  "businessStatus" : {
    "coding" : [{
      "system" : "https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-estado-referencia",
      "code" : "requested",
      "display" : "Requested"
    }]
  },
  "intent" : "order",
  "code" : {
    "coding" : [{
      "system" : "https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-task-code",
      "code" : "referral-workflow",
      "display" : "Referral workflow"
    }]
  },
  "description" : "acceptance decision",
  "focus" : {
    "reference" : "ServiceRequest/ref-2026-0001"
  },
  "for" : {
    "reference" : "Patient/maria-gonzalez"
  },
  "authoredOn" : "2026-11-19T09:30:00-03:00",
  "lastModified" : "2026-11-19T09:30:00-03:00",
  "requester" : {
    "reference" : "PractitionerRole/rol-medico-aps"
  }
}

```
