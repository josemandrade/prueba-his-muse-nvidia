# Endpoint del servicio de cardiología - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Endpoint del servicio de cardiología**

## Example Endpoint: Endpoint del servicio de cardiología

Cardiology FHIR endpoint (HL7 FHIR (Endpoint Connection Type#hl7-fhir-rest)): https://especialidad.example.org/fhir

-------

| | |
| :--- | :--- |
| Status: | Active |
| Address: | [https://especialidad.example.org/fhir](https://especialidad.example.org/fhir) |
| Connection Type: | [Endpoint Connection Type: hl7-fhir-rest](http://terminology.hl7.org/7.5.0/CodeSystem-endpoint-connection-type.html#endpoint-connection-type-hl7-fhir-rest)(HL7 FHIR) |
| Payload Type: | Any |
| Managed By: | [Servicio de Cardiología (http://especialidad.example.org/organization#CARDIOLOGIA)](Organization-org-cardiologia.md) |



## Resource Content

```json
{
  "resourceType" : "Endpoint",
  "id" : "endpoint-cardiologia",
  "status" : "active",
  "connectionType" : {
    "system" : "http://terminology.hl7.org/CodeSystem/endpoint-connection-type",
    "code" : "hl7-fhir-rest",
    "display" : "HL7 FHIR"
  },
  "name" : "Cardiology FHIR endpoint",
  "managingOrganization" : {
    "reference" : "Organization/org-cardiologia"
  },
  "payloadType" : [{
    "coding" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/endpoint-payload-type",
      "code" : "any",
      "display" : "Any"
    }]
  }],
  "address" : "https://especialidad.example.org/fhir"
}

```
