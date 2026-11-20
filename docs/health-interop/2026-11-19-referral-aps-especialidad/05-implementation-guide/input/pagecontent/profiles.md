# Perfiles

La guía define sus propios perfiles (`Derivacion*`) sobre los recursos
base de FHIR R4. No transcribe los perfiles de ninguna otra guía. La base
de cada perfil es el recurso base de FHIR R4 (URL canónica en la tabla); el
usuario puede elegir otra base para cualquier perfil — por ejemplo, para el
paciente, `CorePacienteCl` de la guía chilena
(`https://hl7chile.cl/fhir/ig/clcore/StructureDefinition/CorePacienteCl`,
paquete `hl7.fhir.cl.clcore`, última 1.9.4, verificable en el registro FHIR).
Si se elige esa base, la guía añade el paquete como dependencia y el
`Parent:` del perfil es esa base; por defecto es el recurso base R4.

El centro es el [`DerivacionTarea`](StructureDefinition-derivacion-tarea.html):
lleva el estado del flujo de trabajo, y cada paso posterior lo lee primero.
El diagrama de recursos, con el Task en el centro y por qué, está en
[Diagrama de recursos](resources.html).

## Perfiles propios

| Perfil | Recurso base | Restricciones clave | Ejemplo |
|---|---|---|---|
| [`DerivacionPaciente`](StructureDefinition-derivacion-paciente.html) | [Patient](http://hl7.org/fhir/StructureDefinition/Patient) | `identifier` 1..* (clave MPI + RUN); `telecom` 1..* (contacto obligatorio, C12); `name` 1..1; `birthDate` 1..1 | [María González](Patient-maria-gonzalez.html) |
| [`DerivacionSolicitud`](StructureDefinition-derivacion-solicitud.html) | [ServiceRequest](http://hl7.org/fhir/StructureDefinition/ServiceRequest) | `intent = order` (fijo); `subject` 1..1; `code` 1..1 (servicio solicitado, catálogo local); `reasonCode` 1..* (SNOMED CT); `priority` 1..1 (`routine` / `urgent`); `requester` 1..1; `authoredOn` 1..1 | [REF-2026-0001](ServiceRequest-ref-2026-0001.html) |
| [`DerivacionTarea`](StructureDefinition-derivacion-tarea.html) | [Task](http://hl7.org/fhir/StructureDefinition/Task) | `focus` 1..1 → ServiceRequest; `for` 1..1 → Patient; `intent = order` (fijo); `businessStatus` 1..1 (ValueSet local `DerivacionEstadoReferencia`); `statusReason` 0..1; extensiones SLA + conteos | [Tarea REF-2026-0001](Task-tarea-ref-2026-0001.html) |
| [`DerivacionCita`](StructureDefinition-derivacion-cita.html) | [Appointment](http://hl7.org/fhir/StructureDefinition/Appointment) | `basedOn` 1..* → ServiceRequest; `slot` 0..* → Slot; `participant` 1..* (paciente + especialista + lugar); `patientInstruction` 0..1 | [Cita REF-2026-0001](Appointment-cita-ref-2026-0001.html) |
| [`DerivacionEncuentro`](StructureDefinition-derivacion-encuentro.html) | [Encounter](http://hl7.org/fhir/StructureDefinition/Encounter) | `class = AMB` (fijo); `subject` 1..1; `basedOn` 1..* → ServiceRequest; `appointment` 0..1; `serviceType` 1..1 (catálogo local) | [Encuentro REF-2026-0001](Encounter-encuentro-ref-2026-0001.html) |
| [`DerivacionContrareferencia`](StructureDefinition-derivacion-contrareferencia.html) | [Composition](http://hl7.org/fhir/StructureDefinition/Composition) | `status = final` (fijo al enviar); `type` = LOINC 11488-4 "Consult note"; `subject` 1..1; `author` 1..1; secciones Diagnosis, Plan, Follow-up indications, Follow-up plan for APS | [Contrareferencia REF-2026-0001](Composition-contrareferencia-ref-2026-0001.html) |
| [`DerivacionDocumento`](StructureDefinition-derivacion-documento.html) | [DocumentReference](http://hl7.org/fhir/StructureDefinition/DocumentReference) | `status = current` (fijo al enviar); `type` = LOINC 11488-4; `subject` 1..1; `content.attachment.url` → Composition; `context.related` → ServiceRequest | [Documento REF-2026-0001](DocumentReference-documento-ref-2026-0001.html) |
| [`DerivacionDiagnostico`](StructureDefinition-derivacion-diagnostico.html) | [Condition](http://hl7.org/fhir/StructureDefinition/Condition) | `code` 1..1 (ICD-10-CM I50.22 + SNOMED CT 417996009); `subject` 1..1; `encounter` 1..1; `clinicalStatus = active`; `verificationStatus = confirmed` | [Diagnóstico REF-2026-0001](Condition-diagnostico-ref-2026-0001.html) |
| [`DerivacionPlanSeguimiento`](StructureDefinition-derivacion-plan-seguimiento.html) | [CarePlan](http://hl7.org/fhir/StructureDefinition/CarePlan) | `status = active`; `intent = plan` (fijo); `subject` 1..1; `addresses` 1..* → Condition; `activity.reference` → ServiceRequest / Appointment / Task | [Plan REF-2026-0001](CarePlan-plan-ref-2026-0001.html) |
| [`DerivacionNotificacion`](StructureDefinition-derivacion-notificacion.html) | [Communication](http://hl7.org/fhir/StructureDefinition/Communication) | `status = completed` (fijo); `basedOn` 1..* → Task; `sender` 1..1; `recipient` 1..*; `sent` 1..1; `medium` 1..* (lista local de canales) | [Notificación de aceptación](Communication-notificacion-aceptacion-ref-2026-0001.html) |
| [`DerivacionRol`](StructureDefinition-derivacion-rol.html) | [PractitionerRole](http://hl7.org/fhir/StructureDefinition/PractitionerRole) | `practitioner` 1..1; `organization` 1..1; `code` 1..* (ValueSet `DerivacionRolVS`, seis roles) | [Médico APS](PractitionerRole-rol-medico-aps.html) |
| [`DerivacionServicio`](StructureDefinition-derivacion-servicio.html) | [HealthcareService](http://hl7.org/fhir/StructureDefinition/HealthcareService) | `providedBy` 1..1 → Organization; `type` 1..1 (catálogo local); `active` 1..1; `endpoint` 0..* → Endpoint | [Servicio de cardiología](HealthcareService-servicio-cardiologia.html) |

## Extensiones

Las extensiones viven una sola vez en la guía y se reutilizan. Una
extensión solo se usa donde ningún campo base lleva el significado.

| Extensión | Contexto | Valor | Para qué |
|---|---|---|---|
| [`derivacion-sla-acceptance-deadline`](StructureDefinition-derivacion-sla-acceptance-deadline.html) | Task | dateTime | Plazo de aceptación: creación + 5 días hábiles (2 si es urgente) |
| [`derivacion-sla-offer-deadline`](StructureDefinition-derivacion-sla-offer-deadline.html) | Task | dateTime | Plazo de oferta de cita: aceptación + 10 días hábiles |
| [`derivacion-sla-counterreferral-deadline`](StructureDefinition-derivacion-sla-counterreferral-deadline.html) | Task | dateTime | Plazo de contrareferencia: encuentro + 5 días hábiles |
| [`derivacion-sla-retriage-deadline`](StructureDefinition-derivacion-sla-retriage-deadline.html) | Task | dateTime | Plazo de re-triaje: rechazo (o retorno por fallo de agendamiento) + 5 días hábiles |
| [`derivacion-sla-confirmation-deadline`](StructureDefinition-derivacion-sla-confirmation-deadline.html) | Task | dateTime | Plazo de confirmación: oferta + 3 días hábiles (solo mientras una oferta está abierta) |
| [`derivacion-offer-decline-count`](StructureDefinition-derivacion-offer-decline-count.html) | Task | integer | Rechazos de esta oferta (0–2; se reinicia por oferta) |
| [`derivacion-offer-chase-count`](StructureDefinition-derivacion-offer-chase-count.html) | Task | integer | Persecuciones de esta oferta (0–2; se reinicia por oferta) |
| [`derivacion-rescheduling-count`](StructureDefinition-derivacion-rescheduling-count.html) | Task | integer | Re-agendamientos de esta derivación (0–1; no se reinicia) |
| [`derivacion-offer-number`](StructureDefinition-derivacion-offer-number.html) | Appointment | integer | Número de oferta de esta derivación (1ª oferta, re-oferta…) |
| [`derivacion-referral-identifier`](StructureDefinition-derivacion-referral-identifier.html) | Composition | Identifier | El identificador de la derivación en la contrareferencia |
| [`derivacion-preferred-contact-channel`](StructureDefinition-derivacion-preferred-contact-channel.html) | Patient | code | Canal preferido del paciente para las notificaciones |
| [`derivacion-delivery-outcome`](StructureDefinition-derivacion-delivery-outcome.html) | Communication | code | Resultado de la entrega: delivered / failed |
| [`derivacion-match-basis`](StructureDefinition-derivacion-match-basis.html) | Patient | code | Base del cruce de identidad del MPI: identifier / demographics |
| [`derivacion-match-confidence`](StructureDefinition-derivacion-match-confidence.html) | Patient | decimal | Confianza del cruce de identidad del MPI (0–1) |

## Recursos base sin perfil propio

La guía usa los recursos base de FHIR R4 sin restringirlos en un perfil
propio donde la tabla de mapeo no lo exige: `Provenance` (historial de
estados), `Bundle` (sobre de las operaciones de envío), `Subscription`
(avisos de cambio de estado, propio de la guía), `Schedule`, `Slot`,
`Location`, `Endpoint` y `AppointmentResponse`.

## Terminología de los perfiles

Cada campo codificado tiene su terminología en la tabla de la propuesta
(§ Terminología) y en [Terminología](terminology.html): SNOMED CT para el
motivo de derivación, ICD-10-CM + SNOMED CT para el diagnóstico, LOINC
para los exámenes y el tipo de documento, y los ValueSets locales de esta
guía para el estado, el rol, el motivo de rechazo, el canal y el catálogo
de especialidades.
