// Rol de un profesional en la derivación.
// Perfil propio de esta guía, sobre el recurso base PractitionerRole
// de FHIR R4. La persona es un Practitioner; el rol que tiene en esta
// derivación es este perfil (seis roles, C1).

Profile: DerivacionRol
Parent: PractitionerRole
Id: derivacion-rol
Title: "Rol en la derivación"
Description: "El rol que un profesional tiene en una derivación. Perfil propio de esta guía, sobre el recurso base PractitionerRole de FHIR R4. Una persona puede tener más de un rol en distintas derivaciones, pero dentro de una derivación cada rol es una persona."
* practitioner 1..1
* practitioner only Reference(Practitioner)
* organization 1..1
* organization only Reference(Organization)
* organization ^short = "La organización propia del profesional (APS, especialidad, hub)"
* code 1..*
* code from DerivacionRolVS (required)
* code ^short = "Uno de los seis roles del caso"
* active 0..1
* active ^short = "true mientras la persona tiene el rol"
* telecom 0..*
