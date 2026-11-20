# Canal de contacto preferido - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Canal de contacto preferido**

## Extension: Canal de contacto preferido 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-preferred-contact-channel | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionPreferredContactChannel |

| | | |
| :--- | :--- | :--- |
| Canal preferido del paciente para las notificaciones: phone | in-person | system-message (ValueSet DerivacionCanal). |

**Context of Use**

**Usage info**

**Usages:**

* Use this Extension: [Paciente de la derivación](StructureDefinition-derivacion-paciente.md)
* Examples for this Extension: [Patient/maria-gonzalez](Patient-maria-gonzalez.md)

You can also check for [usages in the FHIR IG Statistics](https://packages2.fhir.org/xig/resource/hl7.fhir.uv.test.derivacion-aps-especialidad|current/StructureDefinition/StructureDefinition-derivacion-preferred-contact-channel.json)

### Formal Views of Extension Content

 [Description of Profiles, Differentials, Snapshots, and how the XML and JSON presentations work](http://build.fhir.org/ig/FHIR/ig-guidance/readingIgs.html#structure-definitions). 

 

Other representations of profile: [CSV](StructureDefinition-derivacion-preferred-contact-channel.csv), [Excel](StructureDefinition-derivacion-preferred-contact-channel.xlsx), [Schematron](StructureDefinition-derivacion-preferred-contact-channel.sch) 

#### Terminology Bindings

#### Constraints



## Resource Content

```json
{
  "resourceType" : "StructureDefinition",
  "id" : "derivacion-preferred-contact-channel",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-preferred-contact-channel",
  "version" : "0.1.0",
  "name" : "DerivacionPreferredContactChannel",
  "title" : "Canal de contacto preferido",
  "status" : "draft",
  "date" : "2026-11-20T12:46:55+00:00",
  "description" : "Canal preferido del paciente para las notificaciones: phone | in-person | system-message (ValueSet DerivacionCanal).",
  "fhirVersion" : "4.0.1",
  "mapping" : [{
    "identity" : "rim",
    "uri" : "http://hl7.org/v3",
    "name" : "RIM Mapping"
  }],
  "kind" : "complex-type",
  "abstract" : false,
  "context" : [{
    "type" : "element",
    "expression" : "Patient"
  }],
  "type" : "Extension",
  "baseDefinition" : "http://hl7.org/fhir/StructureDefinition/Extension",
  "derivation" : "constraint",
  "differential" : {
    "element" : [{
      "id" : "Extension",
      "path" : "Extension",
      "short" : "Canal de contacto preferido",
      "definition" : "Canal preferido del paciente para las notificaciones: phone | in-person | system-message (ValueSet DerivacionCanal)."
    },
    {
      "id" : "Extension.extension",
      "path" : "Extension.extension",
      "max" : "0"
    },
    {
      "id" : "Extension.url",
      "path" : "Extension.url",
      "fixedUri" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-preferred-contact-channel"
    },
    {
      "id" : "Extension.value[x]",
      "path" : "Extension.value[x]",
      "min" : 1,
      "type" : [{
        "code" : "code"
      }],
      "binding" : {
        "strength" : "required",
        "valueSet" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/ValueSet/derivacion-canal"
      }
    }]
  }
}

```
