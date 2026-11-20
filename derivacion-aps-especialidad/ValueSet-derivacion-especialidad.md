# Especialidad / servicio (catálogo local) - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Especialidad / servicio (catálogo local)**

## ValueSet: Especialidad / servicio (catálogo local) 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/ValueSet/derivacion-especialidad | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionEspecialidad |

 
Especialidades y servicios a los que se puede derivar. 

 **References** 

* [Cita de la derivación](StructureDefinition-derivacion-cita.md)
* [Encuentro de especialidad](StructureDefinition-derivacion-encuentro.md)
* [Servicio de especialidad](StructureDefinition-derivacion-servicio.md)
* [Solicitud de derivación](StructureDefinition-derivacion-solicitud.md)

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
  "id" : "derivacion-especialidad",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/ValueSet/derivacion-especialidad",
  "version" : "0.1.0",
  "name" : "DerivacionEspecialidad",
  "title" : "Especialidad / servicio (catálogo local)",
  "status" : "draft",
  "date" : "2026-11-20T12:49:56+00:00",
  "description" : "Especialidades y servicios a los que se puede derivar.",
  "compose" : {
    "include" : [{
      "system" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/CodeSystem/derivacion-especialidad"
    }]
  }
}

```
