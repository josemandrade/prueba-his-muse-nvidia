# Artifacts Summary - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* **Artifacts Summary**

## Artifacts Summary

This page provides a list of the FHIR artifacts defined as part of this implementation guide.

### Structures: Resource Profiles 

These define constraints on FHIR resources for systems conforming to this implementation guide.

| | |
| :--- | :--- |
| [Cita de la derivación](StructureDefinition-derivacion-cita.md) | La oferta y la reserva de la cita de especialidad. Perfil propio de esta guía, sobre el recurso base Appointment de FHIR R4. La decisión del paciente vive en el AppointmentResponse, no en la cita; una cita cancelada o no asistida nunca se reutiliza. |
| [Contrareferencia](StructureDefinition-derivacion-contrareferencia.md) | El documento clínico de vuelta del especialista a APS: diagnóstico, plan, indicaciones de seguimiento y plan de seguimiento para APS. Perfil propio de esta guía, sobre el recurso base Composition de FHIR R4. |
| [Diagnóstico de la contrareferencia](StructureDefinition-derivacion-diagnostico.md) | El diagnóstico que el especialista devuelve a APS. Perfil propio de esta guía, sobre el recurso base Condition de FHIR R4. |
| [Documento de contrareferencia](StructureDefinition-derivacion-documento.md) | La entrada de índice de la contrareferencia. Perfil propio de esta guía, sobre el recurso base DocumentReference de FHIR R4. |
| [Encuentro de especialidad](StructureDefinition-derivacion-encuentro.md) | La visita atendida en la especialidad. Perfil propio de esta guía, sobre el recurso base Encounter de FHIR R4. La cita es la reserva; la visita es el encuentro — nunca ambas a la vez sin regla, y la regla aquí es: reserva = Appointment, visita = Encounter. |
| [Notificación](StructureDefinition-derivacion-notificacion.md) | El registro de una notificación enviada en un cambio de estado de la derivación. Perfil propio de esta guía, sobre el recurso base Communication de FHIR R4. Una notificación enviada por error se corrige con una notificación nueva, nunca borrando el registro. |
| [Paciente de la derivación](StructureDefinition-derivacion-paciente.md) | Persona derivada desde APS a una especialidad. Perfil propio de esta guía, sobre el recurso base Patient de FHIR R4. La clave MPI y el RUN son los identificadores que viajan; los datos de contacto son obligatorios (C12) — sin ellos la creación se bloquea. |
| [Plan de seguimiento para APS](StructureDefinition-derivacion-plan-seguimiento.md) | El plan de seguimiento que el especialista deja a APS. Perfil propio de esta guía, sobre el recurso base CarePlan de FHIR R4. Una actualización del plan es una versión nueva, nunca una sobrescritura silenciosa. |
| [Rol en la derivación](StructureDefinition-derivacion-rol.md) | El rol que un profesional tiene en una derivación. Perfil propio de esta guía, sobre el recurso base PractitionerRole de FHIR R4. Una persona puede tener más de un rol en distintas derivaciones, pero dentro de una derivación cada rol es una persona. |
| [Servicio de especialidad](StructureDefinition-derivacion-servicio.md) | El servicio de especialidad al que se deriva (p. ej. cardiología), con su endpoint de enrutado. Perfil propio de esta guía, sobre el recurso base HealthcareService de FHIR R4. |
| [Solicitud de derivación](StructureDefinition-derivacion-solicitud.md) | La derivación que APS crea y el hub enruta: una solicitud de un servicio de especialidad. Perfil propio de esta guía, sobre el recurso base ServiceRequest de FHIR R4. El estado de la derivación NO vive aquí (vive en DerivacionTarea); ServiceRequest.status es solo un espejo grueso. |
| [Tarea de derivación (registro de estado)](StructureDefinition-derivacion-tarea.md) | El registro de estado del flujo de trabajo de una derivación: lleva el estado del caso, los relojes SLA y los conteos de los ciclos. Es el centro del grafo de recursos y lo primero que lee cada paso posterior. Perfil propio de esta guía, sobre el recurso base Task de FHIR R4. |

### Structures: Extension Definitions 

These define constraints on FHIR data types for systems conforming to this implementation guide.

| | |
| :--- | :--- |
| [Base del cruce de identidad](StructureDefinition-derivacion-match-basis.md) | 
| | |
| :--- | :--- |
| Cómo se estableció el cruce de identidad en el MPI: identifier | demographics. |
 |
| [Canal de contacto preferido](StructureDefinition-derivacion-preferred-contact-channel.md) | 
| | | |
| :--- | :--- | :--- |
| Canal preferido del paciente para las notificaciones: phone | in-person | system-message (ValueSet DerivacionCanal). |
 |
| [Confianza del cruce de identidad](StructureDefinition-derivacion-match-confidence.md) | Confianza del cruce de identidad del MPI, de 0 a 1. Opcional. |
| [Conteo de persecuciones de esta oferta](StructureDefinition-derivacion-offer-chase-count.md) | Número de veces que el agendador ha perseguido una oferta sin confirmar (0–2). Se reinicia por oferta (N5). |
| [Conteo de re-agendamientos](StructureDefinition-derivacion-rescheduling-count.md) | Número de re-agendamientos de esta derivación (0–1). No se reinicia: un solo re-agendamiento por derivación. |
| [Conteo de rechazos de esta oferta](StructureDefinition-derivacion-offer-decline-count.md) | Número de veces que el paciente ha rechazado esta oferta (0–2). Se reinicia por oferta (N5). |
| [Identificador de la derivación](StructureDefinition-derivacion-referral-identifier.md) | El identificador de la derivación (el mismo de ServiceRequest.identifier) en la Composition de la contrareferencia. Ningún campo base de Composition lleva el id de la derivación; el enlace también viaja en DocumentReference.context.related. |
| [Número de oferta (de esta derivación)](StructureDefinition-derivacion-offer-number.md) | Contador por derivación: 1ª oferta, re-oferta (2ª), etc. Cada oferta es un Appointment nuevo. |
| [Plazo de aceptación](StructureDefinition-derivacion-sla-acceptance-deadline.md) | Fecha límite para la decisión de aceptación/rechazo: creación + 5 días hábiles (2 si es urgente). |
| [Plazo de confirmación](StructureDefinition-derivacion-sla-confirmation-deadline.md) | Fecha límite para confirmar una oferta: oferta + 3 días hábiles. Presente solo mientras una oferta está abierta. |
| [Plazo de contrareferencia](StructureDefinition-derivacion-sla-counterreferral-deadline.md) | Fecha límite para enviar la contrareferencia: encuentro + 5 días hábiles. |
| [Plazo de oferta de cita](StructureDefinition-derivacion-sla-offer-deadline.md) | Fecha límite para ofrecer la cita: aceptación + 10 días hábiles. |
| [Plazo de re-triaje](StructureDefinition-derivacion-sla-retriage-deadline.md) | Fecha límite para la decisión de re-triaje de APS: rechazo (o retorno por fallo de agendamiento) + 5 días hábiles. |
| [Resultado de la entrega](StructureDefinition-derivacion-delivery-outcome.md) | 
| | |
| :--- | :--- |
| Resultado de la entrega de una notificación: delivered | failed. Communication.status = completed significa enviada; el resultado de la entrega es esta extensión. |
 |

### Terminology: Value Sets 

These define sets of codes used by systems conforming to this implementation guide.

| | |
| :--- | :--- |
| [Base del cruce de identidad](ValueSet-derivacion-base-cruce.md) | Bases posibles del cruce de identidad en el MPI. |
| [Canal de notificación](ValueSet-derivacion-canal.md) | Canales de notificación de la derivación. |
| [Código de la tarea de derivación](ValueSet-derivacion-task-code.md) | Códigos de Task de esta guía. |
| [Especialidad / servicio (catálogo local)](ValueSet-derivacion-especialidad.md) | Especialidades y servicios a los que se puede derivar. |
| [Estado de la derivación](ValueSet-derivacion-estado-referencia.md) | Estados posibles de una derivación APS → especialidad. |
| [Motivo de rechazo](ValueSet-derivacion-motivo-rechazo.md) | Motivos por los que la especialidad puede rechazar una derivación. |
| [Resultado de la entrega de una notificación](ValueSet-derivacion-resultado-entrega.md) | Resultados posibles de la entrega de una notificación. |
| [Rol en la derivación](ValueSet-derivacion-rol.md) | Roles que una persona puede tener en una derivación. |

### Terminology: Code Systems 

These define new code systems used by systems conforming to this implementation guide.

| | |
| :--- | :--- |
| [Base del cruce de identidad](CodeSystem-derivacion-base-cruce.md) | Cómo se estableció el cruce de identidad en el MPI (lista local). |
| [Canal de notificación](CodeSystem-derivacion-canal.md) | Canales por los que se envía una notificación (lista local; el caso no fija un canal por notificación). |
| [Código de la tarea de derivación](CodeSystem-derivacion-task-code.md) | El Task de esta guía es siempre un registro de flujo de trabajo de derivación. |
| [Especialidad / servicio (catálogo local)](CodeSystem-derivacion-especialidad.md) | Catálogo local de especialidades y servicios, versionado por la red (hub + servicios). El ejemplo trabajado es cardiología; la red amplía el catálogo sin tocar esta guía. |
| [Estado de la derivación](CodeSystem-derivacion-estado-referencia.md) | Los nueve estados del caso de la derivación APS → especialidad (spec §3.1). El estado vive en Task.businessStatus, nunca como valor inventado de Task.status. |
| [Motivo de rechazo](CodeSystem-derivacion-motivo-rechazo.md) | Motivos de rechazo de la derivación (lista local de la especialidad; el texto libre acompaña al código). |
| [Resultado de la entrega de una notificación](CodeSystem-derivacion-resultado-entrega.md) | Resultados posibles de la entrega de una notificación (lista local). |
| [Rol en la derivación](CodeSystem-derivacion-rol.md) | Los seis roles del caso de uso (spec §2). Dentro de una derivación, cada rol es una persona (el clínico de triaje no es el agendador — C1). |

### Example: Example Instances 

These are example instances that show what data produced and consumed by systems conforming with this implementation guide might look like.

| | |
| :--- | :--- |
| [Administrativo APS en la derivación REF-2026-0001](PractitionerRole-rol-admin-aps.md) |  |
| [Agenda de cardiología](Schedule-schedule-cardiologia.md) |  |
| [Agendador en la derivación REF-2026-0001](PractitionerRole-rol-agendador.md) |  |
| [Bundle de documento PI-3 (contrareferencia)](Bundle-bundle-pi3-ref-2026-0001.md) | La contrareferencia viaja como documento FHIR: la Composition es la primera entrada (OP-6). |
| [Bundle de transacción PI-0 (creación de la derivación)](Bundle-bundle-pi0-ref-2026-0001.md) | La derivación viaja como recursos: ServiceRequest + Task en un Bundle de tipo transaction (OP-1). |
| [CESFAM Los Aromos](Organization-org-cesfam-los-aromos.md) |  |
| [Cita de la derivación REF-2026-0001 (proposed)](Appointment-cita-ref-2026-0001.md) | La oferta de cita (PI-2): propuesta, aún sin confirmar por la paciente. |
| [Clínico de triaje en la derivación REF-2026-0001](PractitionerRole-rol-triaje.md) |  |
| [Consulta de cardiología](Location-location-cardiologia.md) |  |
| [Contrareferencia REF-2026-0001](Composition-contrareferencia-ref-2026-0001.md) | El documento de vuelta del especialista a APS (PI-3). |
| [Diagnóstico: insuficiencia cardiaca sistólica crónica](Condition-diagnostico-ref-2026-0001.md) |  |
| [Documento de contrareferencia REF-2026-0001](DocumentReference-documento-ref-2026-0001.md) |  |
| [ECG de la derivación REF-2026-0001](Observation-ecg-2026-11-19.md) |  |
| [Encuentro APS que creó la derivación](Encounter-aps-encounter-2026-11-19.md) | El encuentro de APS existe en el EHR de APS; la guía lo referencia, no lo remodela. |
| [Encuentro de especialidad REF-2026-0001 (planned)](Encounter-encuentro-ref-2026-0001.md) | La visita, creada en la reserva (planned); no se crea en la asistencia. |
| [Endpoint del servicio de cardiología](Endpoint-endpoint-cardiologia.md) |  |
| [Especialista de cardiología (sintético)](Practitioner-especialista-cardiologia.md) |  |
| [Especialista en la derivación REF-2026-0001](PractitionerRole-rol-especialista.md) |  |
| [Hub de derivación](Organization-org-hub.md) |  |
| [María González (paciente sintética)](Patient-maria-gonzalez.md) | Paciente de la derivación REF-2026-0001. |
| [Médico APS (sintético)](Practitioner-medico-aps.md) |  |
| [Médico APS en la derivación REF-2026-0001](PractitionerRole-rol-medico-aps.md) |  |
| [NT-proBNP de la derivación REF-2026-0001](Observation-ntprobnp-2026-11-19.md) |  |
| [Notificación de aceptación a la paciente](Communication-notificacion-aceptacion-ref-2026-0001.md) | El administrativo de APS informa a la paciente de que la especialidad aceptó la derivación (PI-1, C5/Q3). |
| [Plan de seguimiento para APS](CarePlan-plan-ref-2026-0001.md) |  |
| [Respuesta de la paciente a la oferta (accepted)](AppointmentResponse-respuesta-cita-1.md) |  |
| [Servicio de cardiología](HealthcareService-servicio-cardiologia.md) |  |
| [Servicio de cardiología (organización)](Organization-org-cardiologia.md) |  |
| [Slot de cardiología (reservado)](Slot-slot-cardiologia-1.md) |  |
| [Solicitud de derivación REF-2026-0001](ServiceRequest-ref-2026-0001.md) | Derivación de María González a cardiología por sospecha de insuficiencia cardiaca (PI-0). |
| [Tarea de derivación REF-2026-0001 (requested)](Task-tarea-ref-2026-0001.md) | El registro de estado del flujo de trabajo, en su creación (PI-0). |

