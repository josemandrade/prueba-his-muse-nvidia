// Documento de la contrareferencia (la entrada de índice).
// Perfil propio de esta guía, sobre el recurso base DocumentReference
// de FHIR R4. La Composition es el documento; el DocumentReference es
// su entrada de índice, por la que MHD lo encuentra y APS lo recupera.

Profile: DerivacionDocumento
Parent: DocumentReference
Id: derivacion-documento
Title: "Documento de contrareferencia"
Description: "La entrada de índice de la contrareferencia. Perfil propio de esta guía, sobre el recurso base DocumentReference de FHIR R4."
* masterIdentifier 0..1
* masterIdentifier ^short = "El mismo valor que Composition.identifier"
* status 1..1
* status = #current (exactly)
* status ^short = "current al enviar (superseded en una corrección, nunca sobrescrito)"
* type 1..1
* type = http://loinc.org#11488-4 "Consult note"
* type ^short = "LOINC 11488-4 'Consult note'"
* subject 1..1
* subject only Reference(DerivacionPaciente)
* author 0..*
* author only Reference(DerivacionRol)
* date 0..1
* date ^short = "Fecha de envío"
* content 1..*
* content.attachment.url 1..1
* content.attachment.url ^short = "La Composition: [base]/Composition/{id}"
* content.attachment.contentType 1..1
* content.attachment.contentType = #application/fhir+json (exactly)
* context 0..1
* context.encounter 0..*
* context.encounter only Reference(DerivacionEncuentro)
* context.related 0..*
* context.related only Reference(DerivacionSolicitud)
* context.related ^short = "El enlace del documento a la derivación"
* context.period 0..1
* relatesTo 0..*
* relatesTo ^short = "Una corrección enlaza (code = replaces) al DocumentReference anterior"
