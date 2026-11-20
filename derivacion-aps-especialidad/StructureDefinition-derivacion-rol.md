# Rol en la derivación - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Rol en la derivación**

## Resource Profile: Rol en la derivación 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-rol | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionRol |

 
El rol que un profesional tiene en una derivación. Perfil propio de esta guía, sobre el recurso base PractitionerRole de FHIR R4. Una persona puede tener más de un rol en distintas derivaciones, pero dentro de una derivación cada rol es una persona. 

**Usages:**

* Refer to this Profile: [Contrareferencia](StructureDefinition-derivacion-contrareferencia.md), [Documento de contrareferencia](StructureDefinition-derivacion-documento.md), [Encuentro de especialidad](StructureDefinition-derivacion-encuentro.md), [Notificación](StructureDefinition-derivacion-notificacion.md)... Show 3 more, [Plan de seguimiento para APS](StructureDefinition-derivacion-plan-seguimiento.md), [Solicitud de derivación](StructureDefinition-derivacion-solicitud.md) and [Tarea de derivación (registro de estado)](StructureDefinition-derivacion-tarea.md)
* Examples for this Profile: [PractitionerRole/rol-admin-aps](PractitionerRole-rol-admin-aps.md), [PractitionerRole/rol-agendador](PractitionerRole-rol-agendador.md), [PractitionerRole/rol-especialista](PractitionerRole-rol-especialista.md), [PractitionerRole/rol-medico-aps](PractitionerRole-rol-medico-aps.md) and [PractitionerRole/rol-triaje](PractitionerRole-rol-triaje.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-rol.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-rol.csv), [Excel](StructureDefinition-derivacion-rol.xlsx), [Schematron](StructureDefinition-derivacion-rol.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-rol",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-rol",
  "version" : "0.1.0",
  "name" : "DerivacionRol",
  "title" : "Rol en la derivación",
  "status" : "draft",
  "date" : "2026-11-20T12:49:56+00:00",
  "description" : "El rol que un profesional tiene en una derivación. Perfil propio de esta guía, sobre el recurso base PractitionerRole de FHIR R4. Una persona puede tener más de un rol en distintas derivaciones, pero dentro de una derivación cada rol es una persona.",
  "fhirVersion" : "4.0.1",
  "mapping" : [{
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
    "identity" : "servd",
    "uri" : "http://www.omg.org/spec/ServD/1.0/",
    "name" : "ServD"
  },
  {
    "identity" : "w5",
    "uri" : "http://hl7.org/fhir/fivews",
    "name" : "FiveWs Pattern Mapping"
  }],
  "kind" : "resource",
  "abstract" : false,
  "type" : "PractitionerRole",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/PractitionerRole",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "PractitionerRole",
      "path" : "PractitionerRole"
    },
    {
      "id" : "PractitionerRole.active",
      "path" : "PractitionerRole.active",
      "short" : "true mientras la persona tiene el rol"
    },
    {
      "id" : "PractitionerRole.practitioner",
      "path" : "PractitionerRole.practitioner",
      "min" : 1
    },
    {
      "id" : "PractitionerRole.organization",
      "path" : "PractitionerRole.organization",
      "short" : "La organización propia del profesional (APS, especialidad, hub)",
      "min" : 1
    },
    {
      "id" : "PractitionerRole.code",
      "path" : "PractitionerRole.code",
      "short" : "Uno de los seis roles del caso",
      "min" : 1,
      "binding" : {
        "strength" : "required",
        "valueSet" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/ValueSet/derivacion-rol"
      }
    }]
  }
}

```
