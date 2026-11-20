# Consulta de cardiología - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Consulta de cardiología**

## Example Location: Consulta de cardiología

Consulta de Cardiología

-------

| | |
| :--- | :--- |
| Address: | Hospital de la Red, piso 3, consulta 12 |
| Managed By: | [Servicio de Cardiología (http://especialidad.example.org/organization#CARDIOLOGIA)](Organization-org-cardiologia.md) |



## Resource Content

```json
{
  "resourceType" : "Location",
  "id" : "location-cardiologia",
  "name" : "Consulta de Cardiología",
  "address" : {
    "text" : "Hospital de la Red, piso 3, consulta 12"
  },
  "managingOrganization" : {
    "reference" : "Organization/org-cardiologia"
  }
}

```
