# Canal de notificación - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Canal de notificación**

## ValueSet: Canal de notificación 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/ValueSet/derivacion-canal | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionCanal |

 
Canales de notificación de la derivación. 

 **References** 

* [Notificación](StructureDefinition-derivacion-notificacion.md)
* [Canal de contacto preferido](StructureDefinition-derivacion-preferred-contact-channel.md)

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
  "id" : "derivacion-canal",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/ValueSet/derivacion-canal",
  "version" : "0.1.0",
  "name" : "DerivacionCanal",
  "title" : "Canal de notificación",
  "status" : "draft",
  "date" : "2026-11-20T12:46:55+00:00",
  "description" : "Canales de notificación de la derivación.",
  "compose" : {
    "include" : [{
      "system" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/CodeSystem/derivacion-canal"
    }]
  }
}

```
