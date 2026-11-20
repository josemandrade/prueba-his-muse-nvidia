// Contrareferencia (el documento de vuelta).
// Perfil propio de esta guía, sobre el recurso base Composition de
// FHIR R4. La contrareferencia viaja como documento FHIR (la
// Composition es la primera entrada de un Bundle de tipo document),
// para que MHD pueda llevarla y APS pueda acusar recibo del documento.

Profile: DerivacionContrareferencia
Parent: Composition
Id: derivacion-contrareferencia
Title: "Contrareferencia"
Description: "El documento clínico de vuelta del especialista a APS: diagnóstico, plan, indicaciones de seguimiento y plan de seguimiento para APS. Perfil propio de esta guía, sobre el recurso base Composition de FHIR R4."
* identifier 0..1
* identifier ^short = "Identificador de la contrareferencia, creado por la especialidad"
* status 1..1
* status = #final (exactly)
* status ^short = "final: el perfil es el documento enviado; un borrador es una Composition sin este perfil"
* type 1..1
* type = http://loinc.org#11488-4 "Consult note"
* type ^short = "LOINC 11488-4 'Consult note' (variante de cardiología: 34099-2 en el ejemplo trabajado)"
* subject 1..1
* subject only Reference(DerivacionPaciente)
* encounter 0..1
* encounter only Reference(DerivacionEncuentro)
* date 1..1
* date ^short = "Fecha de envío"
* author 1..1
* author only Reference(DerivacionRol)
* author ^short = "El especialista, en su rol"
* title 1..1
* title = "Counter-referral"
* section 1..*
* section ^slicing.discriminator.type = #value
* section ^slicing.discriminator.path = "title"
* section ^slicing.rules = #open
* section contains diagnosis 1..1 and plan 1..1 and followUpIndications 1..1 and followUpPlan 1..1
* section[diagnosis].title = "Diagnosis"
* section[diagnosis].code 1..1
* section[diagnosis].entry 0..*
* section[diagnosis].entry only Reference(DerivacionDiagnostico)
* section[plan].title = "Plan"
* section[plan].code 1..1
* section[plan].entry 0..*
* section[plan].entry only Reference(DerivacionPlanSeguimiento)
* section[followUpIndications].title = "Follow-up indications"
* section[followUpIndications].code 1..1
* section[followUpPlan].title = "Follow-up plan for APS"
* section[followUpPlan].code 1..1
* section[followUpPlan].entry 0..*
* section[followUpPlan].entry only Reference(DerivacionPlanSeguimiento)
* extension contains DerivacionReferralIdentifier named referralIdentifier 0..1
* extension[referralIdentifier] ^short = "El identificador de la derivación (el mismo de ServiceRequest.identifier)"
