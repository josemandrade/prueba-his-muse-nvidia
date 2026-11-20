# Estado de la derivación - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Estado de la derivación**

## ValueSet: Estado de la derivación 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/ValueSet/derivacion-estado-referencia | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionEstadoReferencia |

 
Estados posibles de una derivación APS → especialidad. 

 **References** 

* [Tarea de derivación (registro de estado)](StructureDefinition-derivacion-tarea.md)

### Logical Definition (CLD)

 

### Expansion

-------

 Explanation of the columns that may appear on this page: 

| | |
| :--- | :--- |
| Level | A few code lists that FHIR defines are hierarchical - each code is assigned a level. In this scheme, some codes are under other codes, and imply that the code they are under also applies |
| System | The source of the definition of the code (when the value set draws in codes defined elsewhere) |
| Code | The code (used as the code in the resource instance) |
| Display | The display (used in the*display*element of a[Coding](http://hl7.org/fhir/R4/datatypes.html#Coding)). If there is no display, implementers should not simply display the code, but map the concept into their application |
| Definition | An explanation of the meaning of the concept |
| Comments | Additional notes about how to use the code |



## Resource Content

```json
{
  "resourceType" : "ValueSet",
  "id" : "derivacion-estado-referencia",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/ValueSet/derivacion-estado-referencia",
  "version" : "0.1.0",
  "name" : "DerivacionEstadoReferencia",
  "title" : "Estado de la derivación",
  "status" : "draft",
  "date" : "2026-11-20T12:33:32+00:00",
  "description" : "Estados posibles de una derivación APS → especialidad.",
  "compose" : {
    "include" : [{
      "system" : "https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-estado-referencia"
    }]
  }
}

```
