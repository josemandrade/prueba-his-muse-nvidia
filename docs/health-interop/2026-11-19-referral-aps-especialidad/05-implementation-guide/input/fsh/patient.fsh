// Paciente de la derivación.
// Perfil propio de esta guía. Diseñado a partir de la especificación del
// caso de uso (entidades y datos de los pasos 1–3) sobre el recurso base
// Patient de FHIR R4.

Profile: DerivacionPaciente
Parent: Patient
Id: derivacion-paciente
Title: "Paciente de la derivación"
Description: "Persona derivada desde APS a una especialidad. Perfil propio de esta guía, sobre el recurso base Patient de FHIR R4. La clave MPI y el RUN son los identificadores que viajan; los datos de contacto son obligatorios (C12) — sin ellos la creación se bloquea."
* identifier 1..*
* identifier ^slicing.discriminator.type = #value
* identifier ^slicing.discriminator.path = "system"
* identifier ^slicing.rules = #open
* identifier contains mpiKey 0..1 and run 1..1
* identifier[mpiKey].system = "http://mpi.red.example.org"
* identifier[mpiKey].value 1..1
* identifier[mpiKey] ^short = "Clave MPI: la clave entre organizaciones"
* identifier[run].system = "http://www.registrocivil.cl/run"
* identifier[run].value 1..1
* identifier[run] ^short = "RUN (sintético en los ejemplos: 11.111.111-1)"
* name 1..1
* name ^short = "Nombre y apellidos (use = official)"
* birthDate 1..1
* telecom 1..*
* telecom ^short = "Datos de contacto (teléfono, correo). Obligatorios (C12)."
* address 0..*
* gender 0..1
* extension contains DerivacionPreferredContactChannel named preferredContactChannel 0..1
* extension[preferredContactChannel] ^short = "Canal preferido del paciente para las notificaciones"
