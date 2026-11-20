// Diagnóstico de la contrareferencia.
// Perfil propio de esta guía, sobre el recurso base Condition de FHIR
// R4. El diagnóstico va en ICD-10-CM (código facturable I50.22) con
// SNOMED CT 417996009 como segunda codificación: Chile usa la CIE-10
// de la OMS, donde no existe un código específico de insuficiencia
// sistólica (I50 solo tiene I50.0 / I50.1 / I50.9).

Profile: DerivacionDiagnostico
Parent: Condition
Id: derivacion-diagnostico
Title: "Diagnóstico de la contrareferencia"
Description: "El diagnóstico que el especialista devuelve a APS. Perfil propio de esta guía, sobre el recurso base Condition de FHIR R4."
* code 1..1
* code ^short = "ICD-10-CM (primario) + SNOMED CT (segunda codificación). Ejemplo trabajado: I50.22 insuficiencia cardiaca sistólica crónica + 417996009."
* code.coding 1..*
* code.coding ^slicing.discriminator.type = #value
* code.coding ^slicing.discriminator.path = "system"
* code.coding ^slicing.rules = #open
* code.coding contains icd10cm 1..1 and snomed 1..1
* code.coding[icd10cm].system 1..1
* code.coding[icd10cm].system = "http://hl7.org/fhir/sid/icd-10-cm"
* code.coding[snomed].system 1..1
* code.coding[snomed].system = "http://snomed.info/sct"
* subject 1..1
* subject only Reference(DerivacionPaciente)
* encounter 1..1
* encounter only Reference(DerivacionEncuentro)
* clinicalStatus 1..1
* clinicalStatus = http://terminology.hl7.org/CodeSystem/condition-clinical#active (exactly)
* verificationStatus 1..1
* verificationStatus = http://terminology.hl7.org/CodeSystem/condition-ver-status#confirmed (exactly)
* note 0..*
