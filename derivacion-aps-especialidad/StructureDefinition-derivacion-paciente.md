# Paciente de la derivación - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Paciente de la derivación**

## Resource Profile: Paciente de la derivación 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-paciente | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionPaciente |

 
Persona derivada desde APS a una especialidad. Perfil propio de esta guía, sobre el recurso base Patient de FHIR R4. La clave MPI y el RUN son los identificadores que viajan; los datos de contacto son obligatorios (C12) — sin ellos la creación se bloquea. 

**Usages:**

* Refer to this Profile: [Contrareferencia](StructureDefinition-derivacion-contrareferencia.md), [Diagnóstico de la contrareferencia](StructureDefinition-derivacion-diagnostico.md), [Documento de contrareferencia](StructureDefinition-derivacion-documento.md), [Encuentro de especialidad](StructureDefinition-derivacion-encuentro.md)... Show 4 more, [Notificación](StructureDefinition-derivacion-notificacion.md), [Plan de seguimiento para APS](StructureDefinition-derivacion-plan-seguimiento.md), [Solicitud de derivación](StructureDefinition-derivacion-solicitud.md) and [Tarea de derivación (registro de estado)](StructureDefinition-derivacion-tarea.md)
* Examples for this Profile: [Patient/maria-gonzalez](Patient-maria-gonzalez.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-paciente.json)

### Formal Views of Profile Content

 [Description of Profiles, Differentials, Snapshots and how the different presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-paciente.csv), [Excel](StructureDefinition-derivacion-paciente.xlsx), [Schematron](StructureDefinition-derivacion-paciente.sch) 



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-paciente",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-paciente",
  "version" : "0.1.0",
  "name" : "DerivacionPaciente",
  "title" : "Paciente de la derivación",
  "status" : "draft",
  "date" : "2026-11-20T12:33:32+00:00",
  "description" : "Persona derivada desde APS a una especialidad. Perfil propio de esta guía, sobre el recurso base Patient de FHIR R4. La clave MPI y el RUN son los identificadores que viajan; los datos de contacto son obligatorios (C12) — sin ellos la creación se bloquea.",
  "fhirVersion" : "4.0.1",
  "mapping" : [{
    "identity" : "rim",
    "uri" : "http://hl7.org/v3",
    "name" : "RIM Mapping"
  },
  {
    "identity" : "cda",
    "uri" : "http://hl7.org/v3/cda",
    "name" : "CDA (R2)"
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
  },
  {
    "identity" : "loinc",
    "uri" : "http://loinc.org",
    "name" : "LOINC code for the element"
  }],
  "kind" : "resource",
  "abstract" : false,
  "type" : "Patient",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/Patient",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "Patient",
      "path" : "Patient"
    },
    {
      "id" : "Patient.extension",
      "path" : "Patient.extension",
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
      "id" : "Patient.extension:preferredContactChannel",
      "path" : "Patient.extension",
      "sliceName" : "preferredContactChannel",
      "short" : "Canal preferido del paciente para las notificaciones",
      "min" : 0,
      "max" : "1",
      "type" : [{
        "code" : "Extension",
        "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-preferred-contact-channel"]
      }]
    },
    {
      "id" : "Patient.identifier",
      "path" : "Patient.identifier",
      "slicing" : {
        "discriminator" : [{
          "type" : "value",
          "path" : "system"
        }],
        "rules" : "open"
      },
      "min" : 1
    },
    {
      "id" : "Patient.identifier:mpiKey",
      "path" : "Patient.identifier",
      "sliceName" : "mpiKey",
      "short" : "Clave MPI: la clave entre organizaciones",
      "min" : 0,
      "max" : "1"
    },
    {
      "id" : "Patient.identifier:mpiKey.system",
      "path" : "Patient.identifier.system",
      "min" : 1,
      "patternUri" : "http://mpi.red.example.org"
    },
    {
      "id" : "Patient.identifier:mpiKey.value",
      "path" : "Patient.identifier.value",
      "min" : 1
    },
    {
      "id" : "Patient.identifier:run",
      "path" : "Patient.identifier",
      "sliceName" : "run",
      "short" : "RUN (sintético en los ejemplos: 11.111.111-1)",
      "min" : 1,
      "max" : "1"
    },
    {
      "id" : "Patient.identifier:run.system",
      "path" : "Patient.identifier.system",
      "min" : 1,
      "patternUri" : "http://www.registrocivil.cl/run"
    },
    {
      "id" : "Patient.identifier:run.value",
      "path" : "Patient.identifier.value",
      "min" : 1
    },
    {
      "id" : "Patient.name",
      "path" : "Patient.name",
      "short" : "Nombre y apellidos (use = official)",
      "min" : 1,
      "max" : "1"
    },
    {
      "id" : "Patient.telecom",
      "path" : "Patient.telecom",
      "short" : "Datos de contacto (teléfono, correo). Obligatorios (C12).",
      "min" : 1
    },
    {
      "id" : "Patient.birthDate",
      "path" : "Patient.birthDate",
      "min" : 1
    }]
  }
}

```
