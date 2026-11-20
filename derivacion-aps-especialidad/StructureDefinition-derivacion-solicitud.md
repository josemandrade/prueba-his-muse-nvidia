# Solicitud de derivación - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Solicitud de derivación**

## Resource Profile: Solicitud de derivación 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-solicitud | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionSolicitud |

 
La derivación que APS crea y el hub enruta: una solicitud de un servicio de especialidad. Perfil propio de esta guía, sobre el recurso base ServiceRequest de FHIR R4. El estado de la derivación NO vive aquí (vive en DerivacionTarea); ServiceRequest.status es solo un espejo grueso. 

**Usages:**

* Refer to this Profile: [Cita de la derivación](StructureDefinition-derivacion-cita.md), [Documento de contrareferencia](StructureDefinition-derivacion-documento.md), [Encuentro de especialidad](StructureDefinition-derivacion-encuentro.md) and [Tarea de derivación (registro de estado)](StructureDefinition-derivacion-tarea.md)
* Examples for this Profile: [ServiceRequest/ref-2026-0001](ServiceRequest-ref-2026-0001.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-solicitud.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-solicitud.csv), [Excel](StructureDefinition-derivacion-solicitud.xlsx), [Schematron](StructureDefinition-derivacion-solicitud.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-solicitud",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-solicitud",
  "version" : "0.1.0",
  "name" : "DerivacionSolicitud",
  "title" : "Solicitud de derivación",
  "status" : "draft",
  "date" : "2026-11-20T12:49:56+00:00",
  "description" : "La derivación que APS crea y el hub enruta: una solicitud de un servicio de especialidad. Perfil propio de esta guía, sobre el recurso base ServiceRequest de FHIR R4. El estado de la derivación NO vive aquí (vive en DerivacionTarea); ServiceRequest.status es solo un espejo grueso.",
  "fhirVersion" : "4.0.1",
  "mapping" : [{
    "identity" : "workflow",
    "uri" : "http://hl7.org/fhir/workflow",
    "name" : "Workflow Pattern"
  },
  {
    "identity" : "v2",
    "uri" : "http://hl7.org/v2",
    "name" : "HL7 v2 Mapping"
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
    "identity" : "quick",
    "uri" : "http://siframework.org/cqf",
    "name" : "Quality Improvement and Clinical Knowledge (QUICK)"
  }],
  "kind" : "resource",
  "abstract" : false,
  "type" : "ServiceRequest",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/ServiceRequest",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "ServiceRequest",
      "path" : "ServiceRequest"
    },
    {
      "id" : "ServiceRequest.identifier",
      "path" : "ServiceRequest.identifier",
      "short" : "Identificador de la derivación, creado por APS; persistente hasta que se cierra el ciclo (el identificador persistente de 360X)",
      "min" : 1
    },
    {
      "id" : "ServiceRequest.intent",
      "path" : "ServiceRequest.intent",
      "fixedCode" : "order"
    },
    {
      "id" : "ServiceRequest.priority",
      "path" : "ServiceRequest.priority",
      "short" : "routine | urgent (C6/Q6); urgent reduce a la mitad el plazo de aceptación",
      "min" : 1
    },
    {
      "id" : "ServiceRequest.code",
      "path" : "ServiceRequest.code",
      "short" : "El servicio solicitado (catálogo local de especialidades)",
      "min" : 1,
      "binding" : {
        "strength" : "example",
        "valueSet" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/ValueSet/derivacion-especialidad"
      }
    },
    {
      "id" : "ServiceRequest.subject",
      "path" : "ServiceRequest.subject",
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-paciente"]
      }]
    },
    {
      "id" : "ServiceRequest.encounter",
      "path" : "ServiceRequest.encounter",
      "short" : "El encuentro de APS que creó la derivación (existe en el EHR de APS)"
    },
    {
      "id" : "ServiceRequest.authoredOn",
      "path" : "ServiceRequest.authoredOn",
      "min" : 1
    },
    {
      "id" : "ServiceRequest.requester",
      "path" : "ServiceRequest.requester",
      "short" : "El médico de APS, en su rol",
      "min" : 1,
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-rol"]
      }]
    },
    {
      "id" : "ServiceRequest.performerType",
      "path" : "ServiceRequest.performerType",
      "short" : "La especialidad solicitada (catálogo local)",
      "binding" : {
        "strength" : "example",
        "valueSet" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/ValueSet/derivacion-especialidad"
      }
    },
    {
      "id" : "ServiceRequest.performer",
      "path" : "ServiceRequest.performer",
      "short" : "El servicio, una vez enrutado",
      "type" : [{
        "code" : "Reference",
        "targetProfile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-servicio"]
      }]
    },
    {
      "id" : "ServiceRequest.reasonCode",
      "path" : "ServiceRequest.reasonCode",
      "short" : "Motivo de la derivación: SNOMED CT (p. ej. 84114007 insuficiencia cardiaca) + nota en texto libre",
      "min" : 1
    },
    {
      "id" : "ServiceRequest.supportingInfo",
      "path" : "ServiceRequest.supportingInfo",
      "short" : "Resumen clínico de APS y exámenes relevantes (Observation con LOINC, DocumentReference)"
    }]
  }
}

```
