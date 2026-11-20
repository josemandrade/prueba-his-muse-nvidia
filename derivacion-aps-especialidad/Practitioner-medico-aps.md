# Médico APS (sintético) - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Médico APS (sintético)**

## Example Practitioner: Médico APS (sintético)

Ana Pérez (official) (http://www.registrocivil.cl/run#22222222-2)

-------

| | |
| :--- | :--- |
| Gender: | Female |



## Resource Content

```json
{
  "resourceType" : "Practitioner",
  "id" : "medico-aps",
  "identifier" : [{
    "system" : "http://www.registrocivil.cl/run",
    "value" : "22222222-2"
  }],
  "name" : [{
    "use" : "official",
    "family" : "Pérez",
    "given" : ["Ana"]
  }],
  "gender" : "female"
}

```
