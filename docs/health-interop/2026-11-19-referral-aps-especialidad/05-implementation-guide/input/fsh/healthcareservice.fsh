// Servicio de especialidad (directorio).
// Perfil propio de esta guía, sobre el recurso base HealthcareService
// de FHIR R4. Son exactamente los recursos del directorio mCSD: el hub
// encuentra el servicio solicitado y su endpoint con ITI-90.

Profile: DerivacionServicio
Parent: HealthcareService
Id: derivacion-servicio
Title: "Servicio de especialidad"
Description: "El servicio de especialidad al que se deriva (p. ej. cardiología), con su endpoint de enrutado. Perfil propio de esta guía, sobre el recurso base HealthcareService de FHIR R4."
* identifier 1..*
* identifier ^short = "Identificador del servicio (catálogo local)"
* providedBy 1..1
* providedBy only Reference(Organization)
* type 1..1
* type from DerivacionEspecialidad (example)
* type ^short = "La especialidad (catálogo local)"
* name 0..1
* name ^short = "p. ej. 'Cardiology'"
* active 1..1
* active ^short = "El hub solo enruta a servicios que el directorio lista como aceptantes"
* location 0..*
* location only Reference(Location)
* endpoint 0..*
* endpoint only Reference(Endpoint)
* endpoint ^short = "Dónde envía el hub la derivación (connectionType = hl7-fhir-rest)"
