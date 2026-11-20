# Tarea de derivación (registro de estado) - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Tarea de derivación (registro de estado)**

## Resource Profile: Tarea de derivación (registro de estado) 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-tarea | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionTarea |

 
El registro de estado del flujo de trabajo de una derivación: lleva el estado del caso, los relojes SLA y los conteos de los ciclos. Es el centro del grafo de recursos y lo primero que lee cada paso posterior. Perfil propio de esta guía, sobre el recurso base Task de FHIR R4. 

**Usages:**

* Refer to this Profile: [Notificación](StructureDefinition-derivacion-notificacion.md)
* Examples for this Profile: [Task/tarea-ref-2026-0001](Task-tarea-ref-2026-0001.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-tarea.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-tarea.csv), [Excel](StructureDefinition-derivacion-tarea.xlsx), [Schematron](StructureDefinition-derivacion-tarea.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-tarea",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-tarea",
  "version" : "0.1.0",
  "name" : "DerivacionTarea",
  "title" : "Tarea de derivación (registro de estado)",
  "status" : "draft",
  "date" : "2026-11-20T12:49:56+00:00",
  "description" : "El registro de estado del flujo de trabajo de una derivación: lleva el estado del caso, los relojes SLA y los conteos de los ciclos. Es el centro del grafo de recursos y lo primero que lee cada paso posterior. Perfil propio de esta guía, sobre el recurso base Task de FHIR R4.",
  "fhirVersion" : "4.0.1",
  "mapping" : [{
    "identity" : "workflow",
    "uri" : "http://hl7.org/fhir/workflow",
    "name" : "Workflow Pattern"
  },
  {
    "identity" : "rim",
    "uri" : "http://hl7.org/v3",
    "name" : "RIM Mapping"
  },
  {
    "identity" : "w5",
    "uri" : "http://hl7.org/fhir/fivews",
    "name" : "FiveWs Pattern Mapping"
  },
  {
    "identity" : "v2",
    "uri" : "http://hl7.org/v2",
    "name" : "HL7 v2 Mapping"
  }],
  "kind" : "resource",
  "abstract" : false,
  "type" : "Task",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/Task",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "Task",
      "path" : "Task"
    },
    {
      "id" : "Task.extension",
      "path" : "Task.extension",
      "slicing" : {
        "discriminator" : [{
          "type" : "value",
          "path" : "url"
        }],
        "ordered" : false,
        "rules" : "open"
      }
    },
    {
      "id" : "Task.extension:slaAcceptanceDeadline",
      "path" : "Task.extension",
      "sliceName" : "slaAcceptanceDeadline",
      "min" : 0,
      "max" : "1",
      "type" : [{
        "code" : "Extension",
        "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-sla-acceptance-deadline"]
      }]
    },
    {
      "id" : "Task.extension:slaOfferDeadline",
      "path" : "Task.extension",
      "sliceName" : "slaOfferDeadline",
      "min" : 0,
      "max" : "1",
      "type" : [{
        "code" : "Extension",
        "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-sla-offer-deadline"]
      }]
    },
    {
      "id" : "Task.extension:slaCounterreferralDeadline",
      "path" : "Task.extension",
      "sliceName" : "slaCounterreferralDeadline",
      "min" : 0,
      "max" : "1",
      "type" : [{
        "code" : "Extension",
        "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-sla-counterreferral-deadline"]
      }]
    },
    {
      "id" : "Task.extension:slaRetriageDeadline",
      "path" : "Task.extension",
      "sliceName" : "slaRetriageDeadline",
      "min" : 0,
      "max" : "1",
      "type" : [{
        "code" : "Extension",
        "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-sla-retriage-deadline"]
      }]
    },
    {
      "id" : "Task.extension:slaConfirmationDeadline",
      "path" : "Task.extension",
      "sliceName" : "slaConfirmationDeadline",
      "min" : 0,
      "max" : "1",
      "type" : [{
        "code" : "Extension",
        "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-sla-confirmation-deadline"]
      }]
    },
    {
      "id" : "Task.extension:offerDeclineCount",
      "path" : "Task.extension",
      "sliceName" : "offerDeclineCount",
      "min" : 0,
      "max" : "1",
      "type" : [{
        "code" : "Extension",
        "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-offer-decline-count"]
      }]
    },
    {
      "id" : "Task.extension:offerChaseCount",
      "path" : "Task.extension",
      "sliceName" : "offerChaseCount",
      "min" : 0,
      "max" : "1",
      "type" : [{
        "code" : "Extension",
        "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-offer-chase-count"]
      }]
    },
    {
      "id" : "Task.extension:reschedulingCount",
      "path" : "Task.extension",
      "sliceName" : "reschedulingCount",
      "min" : 0,
      "max" : "1",
      "type" : [{
        "code" : "Extension",
        "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-rescheduling-count"]
      }]
    },
    {
      "id" : "Task.identifier",
      "path" : "Task.identifier",
      "short" : "El mismo valor que ServiceRequest.identifier: la clave de unión entre solicitud y registro",
      "min" : 1
    },
    {
      "id" : "Task.status",
      "path" : "Task.status",
      "short" : "El valor grueso de R4; el estado del caso vive en businessStatus"
    },
    {
      "id" : "Task.statusReason",
      "path" : "Task.statusReason",
      "short" : "Motivo de rechazo o de cancelación (incl. 'patient deceased')",
      "binding" : {
        "strength" : "example",
        "valueSet" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/ValueSet/derivacion-motivo-rechazo"
      }
    },
    {
      "id" : "Task.businessStatus",
      "path" : "Task.businessStatus",
      "short" : "El estado del caso, textual (los nueve estados de DerivacionEstadoReferencia)",
      "min" : 1,
      "binding" : {
        "strength" : "example",
        "valueSet" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/ValueSet/derivacion-estado-referencia"
      }
    },
    {
      "id" : "Task.intent",
      "path" : "Task.intent",
      "fixedCode" : "order"
    },
    {
      "id" : "Task.code",
      "path" : "Task.code",
      "short" : "referral-workflow: este Task es siempre un registro de flujo de trabajo de derivación",
      "binding" : {
        "strength" : "example",
        "valueSet" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/ValueSet/derivacion-task-code"
      }
    },
    {
      "id" : "Task.description",
      "path" : "Task.description",
      "short" : "El próximo paso esperado (p. ej. 'acceptance decision', 'appointment offer')"
    },
    {
      "id" : "Task.focus",
      "path" : "Task.focus",
      "short" : "La solicitud sobre la que trabaja este Task",
      "min" : 1,
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-solicitud"]
      }]
    },
    {
      "id" : "Task.for",
      "path" : "Task.for",
      "min" : 1,
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-paciente"]
      }]
    },
    {
      "id" : "Task.requester",
      "path" : "Task.requester",
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-rol"]
      }]
    },
    {
      "id" : "Task.owner",
      "path" : "Task.owner",
      "short" : "El servicio que acepta (es el responsable del trabajo); el profesional que acepta se registra como agente de Provenance en la entrada de aceptación del historial",
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-servicio"]
      }]
    },
    {
      "id" : "Task.relevantHistory",
      "path" : "Task.relevantHistory",
      "short" : "Historial de estados (solo añadir; nunca se edita un estado)"
    }]
  }
}

```
