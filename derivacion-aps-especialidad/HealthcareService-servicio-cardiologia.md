# Servicio de cardiología - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Servicio de cardiología**

## Example HealthcareService: Servicio de cardiología

Profile: [Servicio de especialidad](StructureDefinition-derivacion-servicio.md)

Cardiology (Cardiology) by Servicio de Cardiología (http://especialidad.example.org/organization#CARDIOLOGIA) (http://especialidad.example.org/service#cardiologia)

-------

| | |
| :--- | :--- |
| Active: | true |
| Provided By: | [Servicio de Cardiología (http://especialidad.example.org/organization#CARDIOLOGIA)](Organization-org-cardiologia.md) |
| Type: | Cardiology |
| Endpoint: | [Cardiology FHIR endpoint (HL7 FHIR (Endpoint Connection Type#hl7-fhir-rest)): https://especialidad.example.org/fhir](Endpoint-endpoint-cardiologia.md) |



## Resource Content

```json
{
  "resourceType" : "HealthcareService",
  "id" : "servicio-cardiologia",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-servicio"]
  },
  "identifier" : [{
    "system" : "http://especialidad.example.org/service",
    "value" : "cardiologia"
  }],
  "active" : true,
  "providedBy" : {
    "reference" : "Organization/org-cardiologia"
  },
  "type" : [{
    "coding" : [{
      "system" : "https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-especialidad",
      "code" : "cardiologia",
      "display" : "Cardiology"
    }]
  }],
  "name" : "Cardiology",
  "endpoint" : [{
    "reference" : "Endpoint/endpoint-cardiologia"
  }]
}

```
