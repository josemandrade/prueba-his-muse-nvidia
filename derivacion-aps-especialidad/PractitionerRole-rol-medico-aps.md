# Médico APS en la derivación REF-2026-0001 - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Médico APS en la derivación REF-2026-0001**

## Example PractitionerRole: Médico APS en la derivación REF-2026-0001

Profile: [Rol en la derivación](StructureDefinition-derivacion-rol.md)

Ana Pérez (official) (http://www.registrocivil.cl/run#22222222-2): APS doctor at CESFAM Los Aromos (http://aps.losaromos.example.org/organization#CESFAM-LOS-AROMOS)

-------

| | |
| :--- | :--- |
| Active: | true |
| Practitioner: | [Ana Pérez (official) (http://www.registrocivil.cl/run#22222222-2)](Practitioner-medico-aps.md) |
| Organization: | [CESFAM Los Aromos (http://aps.losaromos.example.org/organization#CESFAM-LOS-AROMOS)](Organization-org-cesfam-los-aromos.md) |
| Role: | APS doctor |



## Resource Content

```json
{
  "resourceType" : "PractitionerRole",
  "id" : "rol-medico-aps",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-rol"]
  },
  "active" : true,
  "practitioner" : {
    "reference" : "Practitioner/medico-aps"
  },
  "organization" : {
    "reference" : "Organization/org-cesfam-los-aromos"
  },
  "code" : [{
    "coding" : [{
      "system" : "https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-rol",
      "code" : "aps-doctor",
      "display" : "APS doctor"
    }]
  }]
}

```
