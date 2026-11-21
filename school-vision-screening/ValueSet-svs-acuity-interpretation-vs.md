# Visual Acuity Interpretation ValueSet - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Visual Acuity Interpretation ValueSet**

## ValueSet: Visual Acuity Interpretation ValueSet 

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/ValueSet/svs-acuity-interpretation-vs | *Version*:0.1.0 |
| Active as of 2026-11-21 | *Computable Name*:SVSAcuityInterpretationVS |

 
Interpretation codes for visual acuity results 

 **References** 

This value set is not used here; it may be used elsewhere (e.g. specifications and/or implementations that use this content)

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
  "id" : "svs-acuity-interpretation-vs",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/ValueSet/svs-acuity-interpretation-vs",
  "version" : "0.1.0",
  "name" : "SVSAcuityInterpretationVS",
  "title" : "Visual Acuity Interpretation ValueSet",
  "status" : "active",
  "experimental" : false,
  "date" : "2026-11-21T14:59:50+00:00",
  "description" : "Interpretation codes for visual acuity results",
  "compose" : {
    "include" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
      "concept" : [{
        "code" : "A",
        "display" : "Abnormal (≤6/12)"
      },
      {
        "code" : "N",
        "display" : "Normal (≥6/9)"
      },
      {
        "code" : "H",
        "display" : "High"
      },
      {
        "code" : "L",
        "display" : "Low"
      }]
    }]
  }
}

```
