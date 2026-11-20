# Notificación - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Notificación**

## Resource Profile: Notificación 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-notificacion | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionNotificacion |

 
El registro de una notificación enviada en un cambio de estado de la derivación. Perfil propio de esta guía, sobre el recurso base Communication de FHIR R4. Una notificación enviada por error se corrige con una notificación nueva, nunca borrando el registro. 

**Usages:**

* Examples for this Profile: [Communication/notificacion-aceptacion-ref-2026-0001](Communication-notificacion-aceptacion-ref-2026-0001.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-notificacion.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-notificacion.csv), [Excel](StructureDefinition-derivacion-notificacion.xlsx), [Schematron](StructureDefinition-derivacion-notificacion.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-notificacion",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-notificacion",
  "version" : "0.1.0",
  "name" : "DerivacionNotificacion",
  "title" : "Notificación",
  "status" : "draft",
  "date" : "2026-11-20T12:46:55+00:00",
  "description" : "El registro de una notificación enviada en un cambio de estado de la derivación. Perfil propio de esta guía, sobre el recurso base Communication de FHIR R4. Una notificación enviada por error se corrige con una notificación nueva, nunca borrando el registro.",
  "fhirVersion" : "4.0.1",
  "mapping" : [{
    "identity" : "workflow",
    "uri" : "http://hl7.org/fhir/workflow",
    "name" : "Workflow Pattern"
  },
  {
    "identity" : "w5",
    "uri" : "http://hl7.org/fhir/fivews",
    "name" : "FiveWs Pattern Mapping"
  },
  {
    "identity" : "rim",
    "uri" : "http://hl7.org/v3",
    "name" : "RIM Mapping"
  }],
  "kind" : "resource",
  "abstract" : false,
  "type" : "Communication",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/Communication",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "Communication",
      "path" : "Communication"
    },
    {
      "id" : "Communication.extension",
      "path" : "Communication.extension",
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
      "id" : "Communication.extension:deliveryOutcome",
      "path" : "Communication.extension",
      "sliceName" : "deliveryOutcome",
      "short" : "delivered | failed. Un envío fallido se reintenta; nunca cambia el estado de la derivación.",
      "min" : 0,
      "max" : "1",
      "type" : [{
        "code" : "Extension",
        "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-delivery-outcome"]
      }]
    },
    {
      "id" : "Communication.identifier",
      "path" : "Communication.identifier",
      "short" : "Creado por el emisor",
      "min" : 1
    },
    {
      "id" : "Communication.basedOn",
      "path" : "Communication.basedOn",
      "short" : "La clave de unión: la derivación sobre la que se notifica",
      "min" : 1,
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-tarea"]
      }]
    },
    {
      "id" : "Communication.status",
      "path" : "Communication.status",
      "short" : "completed = enviada; el resultado de la entrega es la extensión delivery-outcome",
      "fixedCode" : "completed"
    },
    {
      "id" : "Communication.category",
      "path" : "Communication.category",
      "patternCodeableConcept" : {
        "coding" : [{
          "system" : "http://terminology.hl7.org/CodeSystem/communication-category",
          "code" : "notification",
          "display" : "Notification"
        }]
      }
    },
    {
      "id" : "Communication.medium",
      "path" : "Communication.medium",
      "short" : "Canal (lista local: teléfono / presencial / mensaje del sistema)",
      "min" : 1,
      "binding" : {
        "strength" : "example",
        "valueSet" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/ValueSet/derivacion-canal"
      }
    },
    {
      "id" : "Communication.subject",
      "path" : "Communication.subject",
      "min" : 1,
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-paciente"]
      }]
    },
    {
      "id" : "Communication.topic",
      "path" : "Communication.topic",
      "short" : "La transición que disparó el envío (p. ej. 'accepted', en texto codificado); el enlace al Task es basedOn, y el aviso legible es payload.contentString"
    },
    {
      "id" : "Communication.sent",
      "path" : "Communication.sent",
      "min" : 1
    },
    {
      "id" : "Communication.recipient",
      "path" : "Communication.recipient",
      "short" : "Paciente / admin APS / médico APS / especialidad",
      "min" : 1,
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-paciente",
        "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-rol"]
      }]
    },
    {
      "id" : "Communication.sender",
      "path" : "Communication.sender",
      "short" : "Emisor nombrado (C5/Q3): admin APS / agendador (vía hub) / especialista / hub",
      "min" : 1,
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-rol",
        "http://hl7.org/fhir/StructureDefinition/Organization"]
      }]
    },
    {
      "id" : "Communication.payload.content[x]",
      "path" : "Communication.payload.content[x]",
      "slicing" : {
        "discriminator" : [{
          "type" : "type",
          "path" : "$this"
        }],
        "ordered" : false,
        "rules" : "open"
      }
    },
    {
      "id" : "Communication.payload.content[x]:contentString",
      "path" : "Communication.payload.content[x]",
      "sliceName" : "contentString",
      "short" : "El aviso en texto legible (p. ej. 'state changed to accepted')",
      "min" : 0,
      "max" : "1",
      "type" : [{
        "code" : "string"
      }]
    },
    {
      "id" : "Communication.payload.content[x]:contentReference",
      "path" : "Communication.payload.content[x]",
      "sliceName" : "contentReference",
      "short" : "El documento, en el acuse de recibo de la contrareferencia",
      "min" : 0,
      "max" : "1",
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-documento"]
      }]
    }]
  }
}

```
