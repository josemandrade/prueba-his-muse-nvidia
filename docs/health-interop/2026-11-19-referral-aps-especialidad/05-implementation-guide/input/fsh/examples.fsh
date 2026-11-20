// Ejemplos sintéticos del caso trabajado: María González, 58 años, RUN
// 11.111.111-1, CESFAM Los Aromos → cardiología, sospecha de
// insuficiencia cardiaca. Todos los datos son sintéticos. Cada ejemplo
// valida contra su perfil (SUSHI).

Instance: maria-gonzalez
InstanceOf: DerivacionPaciente
Usage: #example
Title: "María González (paciente sintética)"
Description: "Paciente de la derivación REF-2026-0001."
* identifier[mpiKey].system = "http://mpi.red.example.org"
* identifier[mpiKey].value = "MPI-2026-0042"
* identifier[run].system = "http://www.registrocivil.cl/run"
* identifier[run].value = "11111111-1"
* name.use = #official
* name.family = "González"
* name.given = "María"
* birthDate = "1968-04-15"
* gender = #female
* telecom[0].system = #phone
* telecom[0].value = "+56 9 1111 1111"
* telecom[0].use = #mobile
* address.use = #home
* address.text = "Calle Ejemplo 123, Los Aromos"
* extension[preferredContactChannel].valueCode = #phone

Instance: medico-aps
InstanceOf: Practitioner
Usage: #example
Title: "Médico APS (sintético)"
* identifier.system = "http://www.registrocivil.cl/run"
* identifier.value = "22222222-2"
* name.use = #official
* name.family = "Pérez"
* name.given = "Ana"
* gender = #female

Instance: especialista-cardiologia
InstanceOf: Practitioner
Usage: #example
Title: "Especialista de cardiología (sintético)"
* identifier.system = "http://www.registrocivil.cl/run"
* identifier.value = "33333333-3"
* name.use = #official
* name.family = "Rojas"
* name.given = "Carlos"
* gender = #male

Instance: org-cesfam-los-aromos
InstanceOf: Organization
Usage: #example
Title: "CESFAM Los Aromos"
* identifier.system = "http://aps.losaromos.example.org/organization"
* identifier.value = "CESFAM-LOS-AROMOS"
* name = "CESFAM Los Aromos"
* active = true

Instance: org-cardiologia
InstanceOf: Organization
Usage: #example
Title: "Servicio de cardiología (organización)"
* identifier.system = "http://especialidad.example.org/organization"
* identifier.value = "CARDIOLOGIA"
* name = "Servicio de Cardiología"
* active = true

Instance: org-hub
InstanceOf: Organization
Usage: #example
Title: "Hub de derivación"
* identifier.system = "http://hub.example.org/organization"
* identifier.value = "HUB-DERIVACION"
* name = "Hub de Derivación de la Red"
* active = true

Instance: rol-medico-aps
InstanceOf: DerivacionRol
Usage: #example
Title: "Médico APS en la derivación REF-2026-0001"
* practitioner = Reference(medico-aps)
* organization = Reference(org-cesfam-los-aromos)
* code = DerivacionRolCS#aps-doctor "APS doctor"
* active = true

Instance: rol-admin-aps
InstanceOf: DerivacionRol
Usage: #example
Title: "Administrativo APS en la derivación REF-2026-0001"
* practitioner = Reference(medico-aps)
* organization = Reference(org-cesfam-los-aromos)
* code = DerivacionRolCS#aps-admin "APS admin"
* active = true

Instance: rol-especialista
InstanceOf: DerivacionRol
Usage: #example
Title: "Especialista en la derivación REF-2026-0001"
* practitioner = Reference(especialista-cardiologia)
* organization = Reference(org-cardiologia)
* code = DerivacionRolCS#specialist "Specialist"
* active = true

Instance: rol-triaje
InstanceOf: DerivacionRol
Usage: #example
Title: "Clínico de triaje en la derivación REF-2026-0001"
* practitioner = Reference(especialista-cardiologia)
* organization = Reference(org-cardiologia)
* code = DerivacionRolCS#triage-clinician "Triage clinician"
* active = true

Instance: rol-agendador
InstanceOf: DerivacionRol
Usage: #example
Title: "Agendador en la derivación REF-2026-0001"
* practitioner = Reference(especialista-cardiologia)
* organization = Reference(org-cardiologia)
* code = DerivacionRolCS#specialty-scheduler "Specialty scheduler"
* active = true

Instance: servicio-cardiologia
InstanceOf: DerivacionServicio
Usage: #example
Title: "Servicio de cardiología"
* identifier.system = "http://especialidad.example.org/service"
* identifier.value = "cardiologia"
* providedBy = Reference(org-cardiologia)
* type = DerivacionEspecialidadCS#cardiologia "Cardiology"
* name = "Cardiology"
* active = true
* endpoint = Reference(endpoint-cardiologia)

Instance: endpoint-cardiologia
InstanceOf: Endpoint
Usage: #example
Title: "Endpoint del servicio de cardiología"
* status = #active
* connectionType = http://terminology.hl7.org/CodeSystem/endpoint-connection-type#hl7-fhir-rest "HL7 FHIR"
* name = "Cardiology FHIR endpoint"
* managingOrganization = Reference(org-cardiologia)
* payloadType = http://terminology.hl7.org/CodeSystem/endpoint-payload-type#any "Any"
* address = "https://especialidad.example.org/fhir"

Instance: location-cardiologia
InstanceOf: Location
Usage: #example
Title: "Consulta de cardiología"
* name = "Consulta de Cardiología"
* address.text = "Hospital de la Red, piso 3, consulta 12"
* managingOrganization = Reference(org-cardiologia)

Instance: ref-2026-0001
InstanceOf: DerivacionSolicitud
Usage: #example
Title: "Solicitud de derivación REF-2026-0001"
Description: "Derivación de María González a cardiología por sospecha de insuficiencia cardiaca (PI-0)."
* identifier.system = "http://aps.losaromos.example.org/referral"
* identifier.value = "REF-2026-0001"
* status = #active
* intent = #order
* code = DerivacionEspecialidadCS#cardiologia "Cardiology"
* subject = Reference(maria-gonzalez)
* encounter = Reference(aps-encounter-2026-11-19)
* authoredOn = "2026-11-19T09:30:00-03:00"
* requester = Reference(rol-medico-aps)
* performerType = DerivacionEspecialidadCS#cardiologia "Cardiology"
* performer = Reference(servicio-cardiologia)
* reasonCode = http://snomed.info/sct#84114007 "Heart failure (disorder)"
* reasonCode.text = "Suspected heart failure: exertional dyspnoea, ankle oedema"
* priority = #routine
* supportingInfo = Reference(ecg-2026-11-19)
* supportingInfo[+] = Reference(ntprobnp-2026-11-19)
* note.text = "Disnea de esfuerzo y edema de tobillos de dos semanas de evolución."

Instance: aps-encounter-2026-11-19
InstanceOf: Encounter
Usage: #example
Title: "Encuentro APS que creó la derivación"
Description: "El encuentro de APS existe en el EHR de APS; la guía lo referencia, no lo remodela."
* status = #finished
* class = http://terminology.hl7.org/CodeSystem/v3-ActCode#AMB "Ambulatory"
* subject = Reference(maria-gonzalez)
* period.start = "2026-11-19T09:00:00-03:00"
* period.end = "2026-11-19T09:30:00-03:00"

Instance: ecg-2026-11-19
InstanceOf: Observation
Usage: #example
Title: "ECG de la derivación REF-2026-0001"
* status = #final
* code = http://loinc.org#11524-6 "EKG study"
* subject = Reference(maria-gonzalez)
* effectiveDateTime = "2026-11-18T10:00:00-03:00"
* valueString = "Ritmo sinusal, 72 lpm, sin isquemia aguda."

Instance: ntprobnp-2026-11-19
InstanceOf: Observation
Usage: #example
Title: "NT-proBNP de la derivación REF-2026-0001"
* status = #final
* code = http://loinc.org#33762-6 "Natriuretic peptide.B prohormone N-Terminal [Mass/volume] in Serum or Plasma"
* subject = Reference(maria-gonzalez)
* effectiveDateTime = "2026-11-18T10:00:00-03:00"
* valueQuantity = 850 'pg/mL' "pg/mL"

Instance: tarea-ref-2026-0001
InstanceOf: DerivacionTarea
Usage: #example
Title: "Tarea de derivación REF-2026-0001 (requested)"
Description: "El registro de estado del flujo de trabajo, en su creación (PI-0)."
* identifier.system = "http://aps.losaromos.example.org/referral"
* identifier.value = "REF-2026-0001"
* status = #requested
* businessStatus = DerivacionEstadoReferenciaCS#requested "Requested"
* intent = #order
* code = DerivacionTaskCodeCS#referral-workflow "Referral workflow"
* focus = Reference(ref-2026-0001)
* for = Reference(maria-gonzalez)
* authoredOn = "2026-11-19T09:30:00-03:00"
* lastModified = "2026-11-19T09:30:00-03:00"
* requester = Reference(rol-medico-aps)
* description = "acceptance decision"
* extension[slaAcceptanceDeadline].valueDateTime = "2026-11-26T17:00:00-03:00"

Instance: schedule-cardiologia
InstanceOf: Schedule
Usage: #example
Title: "Agenda de cardiología"
* actor = Reference(servicio-cardiologia)
* planningHorizon.start = "2026-12-01T08:00:00-03:00"
* planningHorizon.end = "2026-12-31T17:00:00-03:00"
* comment = "Agenda de la consulta de cardiología."

Instance: slot-cardiologia-1
InstanceOf: Slot
Usage: #example
Title: "Slot de cardiología (reservado)"
* schedule = Reference(schedule-cardiologia)
* status = #busy
* start = "2026-12-02T10:00:00-03:00"
* end = "2026-12-02T10:30:00-03:00"

Instance: cita-ref-2026-0001
InstanceOf: DerivacionCita
Usage: #example
Title: "Cita de la derivación REF-2026-0001 (proposed)"
Description: "La oferta de cita (PI-2): propuesta, aún sin confirmar por la paciente."
* identifier.system = "http://especialidad.example.org/appointment"
* identifier.value = "CITA-2026-0001"
* status = #proposed
* basedOn = Reference(ref-2026-0001)
* slot = Reference(slot-cardiologia-1)
* created = "2026-11-24T11:00:00-03:00"
* start = "2026-12-02T10:00:00-03:00"
* end = "2026-12-02T10:30:00-03:00"
* participant[0].actor = Reference(maria-gonzalez)
* participant[0].status = #needs-action
* participant[+].actor = Reference(rol-especialista)
* participant[=].status = #accepted
* participant[+].actor = Reference(location-cardiologia)
* participant[=].status = #accepted
* serviceType = DerivacionEspecialidadCS#cardiologia "Cardiology"
* patientInstruction = "Ayuno no necesario. Traer los exámenes previos."
* extension[offerNumber].valueInteger = 1

Instance: respuesta-cita-1
InstanceOf: AppointmentResponse
Usage: #example
Title: "Respuesta de la paciente a la oferta (accepted)"
* appointment = Reference(cita-ref-2026-0001)
* actor = Reference(maria-gonzalez)
* participantStatus = #accepted

Instance: encuentro-ref-2026-0001
InstanceOf: DerivacionEncuentro
Usage: #example
Title: "Encuentro de especialidad REF-2026-0001 (planned)"
Description: "La visita, creada en la reserva (planned); no se crea en la asistencia."
* identifier.system = "http://especialidad.example.org/encounter"
* identifier.value = "ENC-2026-0001"
* status = #planned
* class = http://terminology.hl7.org/CodeSystem/v3-ActCode#AMB "Ambulatory"
* subject = Reference(maria-gonzalez)
* basedOn = Reference(ref-2026-0001)
* appointment = Reference(cita-ref-2026-0001)
* period.start = "2026-12-02T10:00:00-03:00"
* period.end = "2026-12-02T10:30:00-03:00"
* participant.individual = Reference(rol-especialista)
* serviceType = DerivacionEspecialidadCS#cardiologia "Cardiology"

Instance: diagnostico-ref-2026-0001
InstanceOf: DerivacionDiagnostico
Usage: #example
Title: "Diagnóstico: insuficiencia cardiaca sistólica crónica"
* code.coding[icd10cm] = http://hl7.org/fhir/sid/icd-10-cm#I50.22 "Chronic systolic (congestive) heart failure"
* code.coding[snomed] = http://snomed.info/sct#417996009 "Systolic heart failure"
* code.text = "Insuficiencia cardiaca sistólica crónica (FEVI 35%)"
* subject = Reference(maria-gonzalez)
* encounter = Reference(encuentro-ref-2026-0001)
* clinicalStatus = http://terminology.hl7.org/CodeSystem/condition-clinical#active "Active"
* verificationStatus = http://terminology.hl7.org/CodeSystem/condition-ver-status#confirmed "Confirmed"
* note.text = "FEVI 35% por ecocardiograma. Sin isquemia aguda en el ECG."

Instance: plan-ref-2026-0001
InstanceOf: DerivacionPlanSeguimiento
Usage: #example
Title: "Plan de seguimiento para APS"
* status = #active
* intent = #plan
* subject = Reference(maria-gonzalez)
* encounter = Reference(encuentro-ref-2026-0001)
* author = Reference(rol-especialista)
* addresses = Reference(diagnostico-ref-2026-0001)
* activity[0].detail.description = "Control en APS en 2 semanas: presión arterial, peso, síntomas."
* activity[0].detail.status = #active
* activity[+].detail.description = "NT-proBNP de control en 3 meses."
* activity[=].detail.status = #active
* activity[+].reference = Reference(ref-2026-0001)

Instance: contrareferencia-ref-2026-0001
InstanceOf: DerivacionContrareferencia
Usage: #example
Title: "Contrareferencia REF-2026-0001"
Description: "El documento de vuelta del especialista a APS (PI-3)."
* identifier.system = "http://especialidad.example.org/counter-referral"
* identifier.value = "CR-2026-0001"
* status = #final
* type = http://loinc.org#11488-4 "Consult note"
* subject = Reference(maria-gonzalez)
* encounter = Reference(encuentro-ref-2026-0001)
* date = "2026-12-03T10:00:00-03:00"
* author = Reference(rol-especialista)
* title = "Counter-referral"
* section[diagnosis].title = "Diagnosis"
* section[diagnosis].code.text = "Diagnosis"
* section[diagnosis].text.status = #generated
* section[diagnosis].text.div = "<div xmlns=\"http://www.w3.org/1999/xhtml\">Chronic systolic heart failure, LVEF 35% (ICD-10-CM I50.22).</div>"
* section[diagnosis].entry = Reference(diagnostico-ref-2026-0001)
* section[plan].title = "Plan"
* section[plan].code.text = "Plan"
* section[plan].text.status = #generated
* section[plan].text.div = "<div xmlns=\"http://www.w3.org/1999/xhtml\">Start heart-failure treatment; control in APS in 2 weeks.</div>"
* section[plan].entry = Reference(plan-ref-2026-0001)
* section[followUpIndications].title = "Follow-up indications"
* section[followUpIndications].code.text = "Follow-up indications"
* section[followUpIndications].text.status = #generated
* section[followUpIndications].text.div = "<div xmlns=\"http://www.w3.org/1999/xhtml\">Blood pressure, weight and symptoms at each APS control; NT-proBNP in 3 months.</div>"
* section[followUpPlan].title = "Follow-up plan for APS"
* section[followUpPlan].code.text = "Follow-up plan for APS"
* section[followUpPlan].text.status = #generated
* section[followUpPlan].text.div = "<div xmlns=\"http://www.w3.org/1999/xhtml\">APS follow-up as in the CarePlan; new referral to cardiology if dyspnoea worsens.</div>"
* section[followUpPlan].entry = Reference(plan-ref-2026-0001)
* extension[referralIdentifier].valueIdentifier.system = "http://aps.losaromos.example.org/referral"
* extension[referralIdentifier].valueIdentifier.value = "REF-2026-0001"

Instance: documento-ref-2026-0001
InstanceOf: DerivacionDocumento
Usage: #example
Title: "Documento de contrareferencia REF-2026-0001"
* masterIdentifier.system = "http://especialidad.example.org/counter-referral"
* masterIdentifier.value = "CR-2026-0001"
* status = #current
* type = http://loinc.org#11488-4 "Consult note"
* subject = Reference(maria-gonzalez)
* author = Reference(rol-especialista)
* date = "2026-12-03T10:00:00-03:00"
* content.attachment.url = "Composition/contrareferencia-ref-2026-0001"
* content.attachment.contentType = #application/fhir+json
* context.encounter = Reference(encuentro-ref-2026-0001)
* context.related = Reference(ref-2026-0001)
* context.period.start = "2026-12-02T10:00:00-03:00"
* context.period.end = "2026-12-02T10:30:00-03:00"

Instance: notificacion-aceptacion-ref-2026-0001
InstanceOf: DerivacionNotificacion
Usage: #example
Title: "Notificación de aceptación a la paciente"
Description: "El administrativo de APS informa a la paciente de que la especialidad aceptó la derivación (PI-1, C5/Q3)."
* identifier.system = "http://aps.losaromos.example.org/notification"
* identifier.value = "NOTIF-2026-0001"
* status = #completed
* category = http://terminology.hl7.org/CodeSystem/communication-category#notification "Notification"
* subject = Reference(maria-gonzalez)
* basedOn = Reference(tarea-ref-2026-0001)
* topic.text = "accepted"
* sender = Reference(rol-admin-aps)
* recipient = Reference(maria-gonzalez)
* sent = "2026-11-21T09:00:00-03:00"
* medium = DerivacionCanalCS#phone "Phone"
* payload.contentString = "Su derivación a cardiología fue aceptada. Le ofreceremos una cita en los próximos días."
* extension[deliveryOutcome].valueCode = #delivered

Instance: bundle-pi0-ref-2026-0001
InstanceOf: Bundle
Usage: #example
Title: "Bundle de transacción PI-0 (creación de la derivación)"
Description: "La derivación viaja como recursos: ServiceRequest + Task en un Bundle de tipo transaction (OP-1)."
* type = #transaction
* entry[0].fullUrl = "urn:uuid:11111111-1111-4111-8111-111111111111"
* entry[0].resource = ref-2026-0001
* entry[0].request.method = #POST
* entry[0].request.url = "ServiceRequest"
* entry[1].fullUrl = "urn:uuid:22222222-2222-4222-8222-222222222222"
* entry[1].resource = tarea-ref-2026-0001
* entry[1].request.method = #POST
* entry[1].request.url = "Task"

Instance: bundle-pi3-ref-2026-0001
InstanceOf: Bundle
Usage: #example
Title: "Bundle de documento PI-3 (contrareferencia)"
Description: "La contrareferencia viaja como documento FHIR: la Composition es la primera entrada (OP-6)."
* type = #document
* timestamp = "2026-12-03T10:00:00-03:00"
* entry[0].fullUrl = "Composition/contrareferencia-ref-2026-0001"
* entry[0].resource = contrareferencia-ref-2026-0001
* entry[1].fullUrl = "DocumentReference/documento-ref-2026-0001"
* entry[1].resource = documento-ref-2026-0001
* entry[2].fullUrl = "Condition/diagnostico-ref-2026-0001"
* entry[2].resource = diagnostico-ref-2026-0001
* entry[3].fullUrl = "CarePlan/plan-ref-2026-0001"
* entry[3].resource = plan-ref-2026-0001
