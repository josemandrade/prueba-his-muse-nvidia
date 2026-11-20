# María González (paciente sintética) - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **María González (paciente sintética)**

## Example Patient: María González (paciente sintética)

Profile: [Paciente de la derivación](StructureDefinition-derivacion-paciente.md)

María González (official) Female, DoB: 1968-04-15 ( http://www.registrocivil.cl/run#11111111-1)

-------

| | |
| :--- | :--- |
| Other Id: | `http://mpi.red.example.org`/MPI-2026-0042 |
| Contact Detail | * [+56 9 1111 1111](tel:+56911111111)
* Calle Ejemplo 123, Los Aromos(home)
 |
| [Canal de contacto preferido](StructureDefinition-derivacion-preferred-contact-channel.md) | phone |



## Resource Content

```json
{
  "resourceType" : "Patient",
  "id" : "maria-gonzalez",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-paciente"]
  },
  "extension" : [{
    "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-preferred-contact-channel",
    "valueCode" : "phone"
  }],
  "identifier" : [{
    "system" : "http://www.registrocivil.cl/run",
    "value" : "11111111-1"
  },
  {
    "system" : "http://mpi.red.example.org",
    "value" : "MPI-2026-0042"
  }],
  "name" : [{
    "use" : "official",
    "family" : "González",
    "given" : ["María"]
  }],
  "telecom" : [{
    "system" : "phone",
    "value" : "+56 9 1111 1111",
    "use" : "mobile"
  }],
  "gender" : "female",
  "birthDate" : "1968-04-15",
  "address" : [{
    "use" : "home",
    "text" : "Calle Ejemplo 123, Los Aromos"
  }]
}

```
