# Servicio de especialidad - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Servicio de especialidad**

## Resource Profile: Servicio de especialidad 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-servicio | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionServicio |

 
El servicio de especialidad al que se deriva (p. ej. cardiología), con su endpoint de enrutado. Perfil propio de esta guía, sobre el recurso base HealthcareService de FHIR R4. 

**Usages:**

* Refer to this Profile: [Solicitud de derivación](StructureDefinition-derivacion-solicitud.md) and [Tarea de derivación (registro de estado)](StructureDefinition-derivacion-tarea.md)
* Examples for this Profile: [Cardiology](HealthcareService-servicio-cardiologia.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-servicio.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-servicio.csv), [Excel](StructureDefinition-derivacion-servicio.xlsx), [Schematron](StructureDefinition-derivacion-servicio.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-servicio",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-servicio",
  "version" : "0.1.0",
  "name" : "DerivacionServicio",
  "title" : "Servicio de especialidad",
  "status" : "draft",
  "date" : "2026-11-20T12:39:48+00:00",
  "description" : "El servicio de especialidad al que se deriva (p. ej. cardiología), con su endpoint de enrutado. Perfil propio de esta guía, sobre el recurso base HealthcareService de FHIR R4.",
  "fhirVersion" : "4.0.1",
  "mapping" : [{
    "identity" : "rim",
    "uri" : "http://hl7.org/v3",
    "name" : "RIM Mapping"
  },
  {
    "identity" : "w5",
    "uri" : "http://hl7.org/fhir/fivews",
    "name" : "FiveWs Pattern Mapping"
  }],
  "kind" : "resource",
  "abstract" : false,
  "type" : "HealthcareService",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/HealthcareService",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "HealthcareService",
      "path" : "HealthcareService"
    },
    {
      "id" : "HealthcareService.identifier",
      "path" : "HealthcareService.identifier",
      "short" : "Identificador del servicio (catálogo local)",
      "min" : 1
    },
    {
      "id" : "HealthcareService.active",
      "path" : "HealthcareService.active",
      "short" : "El hub solo enruta a servicios que el directorio lista como aceptantes",
      "min" : 1
    },
    {
      "id" : "HealthcareService.providedBy",
      "path" : "HealthcareService.providedBy",
      "min" : 1
    },
    {
      "id" : "HealthcareService.type",
      "path" : "HealthcareService.type",
      "short" : "La especialidad (catálogo local)",
      "min" : 1,
      "max" : "1",
      "binding" : {
        "strength" : "example",
        "valueSet" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/ValueSet/derivacion-especialidad"
      }
    },
    {
      "id" : "HealthcareService.name",
      "path" : "HealthcareService.name",
      "short" : "p. ej. 'Cardiology'"
    },
    {
      "id" : "HealthcareService.endpoint",
      "path" : "HealthcareService.endpoint",
      "short" : "Dónde envía el hub la derivación (connectionType = hl7-fhir-rest)"
    }]
  }
}

```
