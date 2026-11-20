# Clínico de triaje en la derivación REF-2026-0001 - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Clínico de triaje en la derivación REF-2026-0001**

## Example PractitionerRole: Clínico de triaje en la derivación REF-2026-0001

Profile: [Rol en la derivación](StructureDefinition-derivacion-rol.md)

Carlos Rojas (official) (http://www.registrocivil.cl/run#33333333-3): Triage clinician at Servicio de Cardiología (http://especialidad.example.org/organization#CARDIOLOGIA)

-------

| | |
| :--- | :--- |
| Active: | true |
| Practitioner: | [Carlos Rojas (official) (http://www.registrocivil.cl/run#33333333-3)](Practitioner-especialista-cardiologia.md) |
| Organization: | [Servicio de Cardiología (http://especialidad.example.org/organization#CARDIOLOGIA)](Organization-org-cardiologia.md) |
| Role: | Triage clinician |



## Resource Content

```json
{
  "resourceType" : "PractitionerRole",
  "id" : "rol-triaje",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-rol"]
  },
  "active" : true,
  "practitioner" : {
    "reference" : "Practitioner/especialista-cardiologia"
  },
  "organization" : {
    "reference" : "Organization/org-cardiologia"
  },
  "code" : [{
    "coding" : [{
      "system" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/CodeSystem/derivacion-rol",
      "code" : "triage-clinician",
      "display" : "Triage clinician"
    }]
  }]
}

```
