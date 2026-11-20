// Extensiones propias de esta guía. Una extensión solo se usa donde ningún
// campo base lleva el significado (tabla de mapeo §3, §1, §5, §7, §10, §11).

Extension: DerivacionSlaAcceptanceDeadline
Id: derivacion-sla-acceptance-deadline
Title: "Plazo de aceptación"
Description: "Fecha límite para la decisión de aceptación/rechazo: creación + 5 días hábiles (2 si es urgente)."
* ^context[+].type = #element
* ^context[=].expression = "Task"
* value[x] only dateTime
* valueDateTime 1..1

Extension: DerivacionSlaOfferDeadline
Id: derivacion-sla-offer-deadline
Title: "Plazo de oferta de cita"
Description: "Fecha límite para ofrecer la cita: aceptación + 10 días hábiles."
* ^context[+].type = #element
* ^context[=].expression = "Task"
* value[x] only dateTime
* valueDateTime 1..1

Extension: DerivacionSlaCounterreferralDeadline
Id: derivacion-sla-counterreferral-deadline
Title: "Plazo de contrareferencia"
Description: "Fecha límite para enviar la contrareferencia: encuentro + 5 días hábiles."
* ^context[+].type = #element
* ^context[=].expression = "Task"
* value[x] only dateTime
* valueDateTime 1..1

Extension: DerivacionSlaRetriageDeadline
Id: derivacion-sla-retriage-deadline
Title: "Plazo de re-triaje"
Description: "Fecha límite para la decisión de re-triaje de APS: rechazo (o retorno por fallo de agendamiento) + 5 días hábiles."
* ^context[+].type = #element
* ^context[=].expression = "Task"
* value[x] only dateTime
* valueDateTime 1..1

Extension: DerivacionSlaConfirmationDeadline
Id: derivacion-sla-confirmation-deadline
Title: "Plazo de confirmación"
Description: "Fecha límite para confirmar una oferta: oferta + 3 días hábiles. Presente solo mientras una oferta está abierta."
* ^context[+].type = #element
* ^context[=].expression = "Task"
* value[x] only dateTime
* valueDateTime 1..1

Invariant: derivacion-decline-count-range
Description: "El conteo de rechazos de esta oferta está entre 0 y 2."
Expression: "$this >= 0 and $this <= 2"
Severity: #error

Extension: DerivacionOfferDeclineCount
Id: derivacion-offer-decline-count
Title: "Conteo de rechazos de esta oferta"
Description: "Número de veces que el paciente ha rechazado esta oferta (0–2). Se reinicia por oferta (N5)."
* ^context[+].type = #element
* ^context[=].expression = "Task"
* value[x] only integer
* valueInteger 1..1
* valueInteger obeys derivacion-decline-count-range

Invariant: derivacion-chase-count-range
Description: "El conteo de persecuciones de esta oferta está entre 0 y 2."
Expression: "$this >= 0 and $this <= 2"
Severity: #error

Extension: DerivacionOfferChaseCount
Id: derivacion-offer-chase-count
Title: "Conteo de persecuciones de esta oferta"
Description: "Número de veces que el agendador ha perseguido una oferta sin confirmar (0–2). Se reinicia por oferta (N5)."
* ^context[+].type = #element
* ^context[=].expression = "Task"
* value[x] only integer
* valueInteger 1..1
* valueInteger obeys derivacion-chase-count-range

Invariant: derivacion-rescheduling-count-range
Description: "El conteo de re-agendamientos está entre 0 y 1: un solo re-agendamiento por derivación."
Expression: "$this >= 0 and $this <= 1"
Severity: #error

Extension: DerivacionReschedulingCount
Id: derivacion-rescheduling-count
Title: "Conteo de re-agendamientos"
Description: "Número de re-agendamientos de esta derivación (0–1). No se reinicia: un solo re-agendamiento por derivación."
* ^context[+].type = #element
* ^context[=].expression = "Task"
* value[x] only integer
* valueInteger 1..1
* valueInteger obeys derivacion-rescheduling-count-range

Extension: DerivacionOfferNumber
Id: derivacion-offer-number
Title: "Número de oferta (de esta derivación)"
Description: "Contador por derivación: 1ª oferta, re-oferta (2ª), etc. Cada oferta es un Appointment nuevo."
* ^context[+].type = #element
* ^context[=].expression = "Appointment"
* value[x] only integer
* valueInteger 1..1

Extension: DerivacionReferralIdentifier
Id: derivacion-referral-identifier
Title: "Identificador de la derivación"
Description: "El identificador de la derivación (el mismo de ServiceRequest.identifier) en la Composition de la contrareferencia. Ningún campo base de Composition lleva el id de la derivación; el enlace también viaja en DocumentReference.context.related."
* ^context[+].type = #element
* ^context[=].expression = "Composition"
* value[x] only Identifier
* valueIdentifier 1..1

Extension: DerivacionPreferredContactChannel
Id: derivacion-preferred-contact-channel
Title: "Canal de contacto preferido"
Description: "Canal preferido del paciente para las notificaciones: phone | in-person | system-message (ValueSet DerivacionCanal)."
* ^context[+].type = #element
* ^context[=].expression = "Patient"
* value[x] only code
* valueCode 1..1
* valueCode from DerivacionCanal (required)

Extension: DerivacionDeliveryOutcome
Id: derivacion-delivery-outcome
Title: "Resultado de la entrega"
Description: "Resultado de la entrega de una notificación: delivered | failed. Communication.status = completed significa enviada; el resultado de la entrega es esta extensión."
* ^context[+].type = #element
* ^context[=].expression = "Communication"
* value[x] only code
* valueCode 1..1
* valueCode from DerivacionResultadoEntrega (required)

Extension: DerivacionMatchBasis
Id: derivacion-match-basis
Title: "Base del cruce de identidad"
Description: "Cómo se estableció el cruce de identidad en el MPI: identifier | demographics."
* ^context[+].type = #element
* ^context[=].expression = "Patient"
* value[x] only code
* valueCode 1..1
* valueCode from DerivacionBaseCruce (required)

Invariant: derivacion-match-confidence-range
Description: "La confianza del cruce de identidad está entre 0 y 1."
Expression: "$this >= 0 and $this <= 1"
Severity: #error

Extension: DerivacionMatchConfidence
Id: derivacion-match-confidence
Title: "Confianza del cruce de identidad"
Description: "Confianza del cruce de identidad del MPI, de 0 a 1. Opcional."
* ^context[+].type = #element
* ^context[=].expression = "Patient"
* value[x] only decimal
* valueDecimal 1..1
* valueDecimal obeys derivacion-match-confidence-range
