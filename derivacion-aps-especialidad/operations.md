# Operaciones - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* **Operaciones**

## Operaciones

### Operaciones

Las operaciones en cada punto de interoperabilidad, con su interacción FHIR, sus entradas, sus salidas, su ejemplo trabajado y el perfil IHE que las apoya (o la declaración de que la guía las posee). Las transacciones de esta guía son propias; nunca se presentan como transacciones IHE. La relación completa con IHE, punto por punto, está en [Relación con IHE](ihe.md). Cada operación aparece en al menos un diagrama de secuencia ([Diagramas de secuencia](sequences.md)).

Ejemplo trabajado en todas las operaciones: María González, 58 años, RUN sintético 11.111.111-1, CESFAM Los Aromos → cardiología, derivación REF-2026-0001.

#### OP-1 — Crear derivación (PI-0)

| | |
| :--- | :--- |
| **Interacción** | `POST [base]/Bundle`(`type = transaction`:[`ServiceRequest`](StructureDefinition-derivacion-solicitud.md)+[`Task`](StructureDefinition-derivacion-tarea.md)[`status = requested`]) |
| **Entradas** | El conjunto mínimo de datos de PI-0 (spec §3.7): paciente con clave MPI + datos de contacto, motivo (SNOMED CT 84114007), servicio solicitado (catálogo local), prioridad, profesional solicitante |
| **Salidas** | El identificador de la derivación + el Task; el hub valida, enruta (`Task.status = received`) y reenvía a la especialidad |
| **Ejemplo** | [Bundle de transacción PI-0](Bundle-bundle-pi0-ref-2026-0001.md)—[ServiceRequest REF-2026-0001](ServiceRequest-ref-2026-0001.md),[Task REF-2026-0001](Task-tarea-ref-2026-0001.md) |
| **IHE** | Sub-paso de identidad:[PIXm ITI-83](https://profiles.ihe.net/ITI/PIXm/)(`$ihe-pix`, full si se implementa exacto) y[PDQm ITI-78](https://profiles.ihe.net/ITI/PDQm/)(full si exacto). Búsqueda de enrutado:[mCSD ITI-90](https://profiles.ihe.net/ITI/mCSD/)(full si exacto). El envío en sí: 360X PCC-55 solo como patrón (partial). Ninguna transacción IHE lleva un envío FHIR`ServiceRequest`+`Task`. |

#### OP-2 — Registrar la decisión de triaje (PI-1)

| | |
| :--- | :--- |
| **Interacción** | `PATCH [base]/Task/{id}`(`status = accepted`+`owner`= el servicio que acepta; el profesional que acepta va como agente de Provenance en la entrada de aceptación, o`status = rejected`+`statusReason`) + Provenance |
| **Entradas** | La decisión del clínico de triaje (aceptar nombrando servicio y profesional, o rechazar con motivo) |
| **Salidas** | El Task en`accepted`o`rejected`; el hub reenvía la decisión a APS (Communication) y el administrativo de APS informa a la paciente |
| **Ejemplo** | [Notificación de aceptación](Communication-notificacion-aceptacion-ref-2026-0001.md)(la Communication que lleva la decisión a la paciente) |
| **IHE** | 360X PCC-56 Referral Decline solo como patrón (partial — la rama de rechazo). La rama de aceptación no tiene transacción 360X (la aceptación es implícita en 360X); en esta guía la aceptación es una transición explícita del Task. La transición en sí es propia de la guía. |

#### OP-3 — Ofrecer / confirmar / reservar cita (PI-2)

| | |
| :--- | :--- |
| **Interacción** | `GET [base]/Slot?schedule=…&status=free`/ Scheduling`$find`(ITI-115) → crear el Appointment (`status = proposed`) +`AppointmentResponse`(`needs-action`) → el hub reenvía la oferta a la paciente y notifica al administrativo de APS → la paciente confirma (`AppointmentResponse.participantStatus = accepted`, Appointment →`pending`) → el agendador reserva (Scheduling`$book`, ITI-117; Appointment →`booked`, Slot →`busy`) → crear el Encounter (`status = planned`,`appointment`→ el Appointment) en la reserva |
| **Entradas** | Disponibilidad del servicio; la oferta (fecha, lugar, instrucciones) |
| **Salidas** | Appointment`booked`+ Encounter`planned`+ Slot`busy`; la oferta, la confirmación y la reserva quedan en el historial del Task |
| **Ejemplo** | [Cita REF-2026-0001 (proposed)](Appointment-cita-ref-2026-0001.md),[Respuesta de la paciente (accepted)](AppointmentResponse-respuesta-cita-1.md),[Encuentro REF-2026-0001 (planned)](Encounter-encuentro-ref-2026-0001.md) |
| **IHE** | [Scheduling](https://profiles.ihe.net/ITI/Scheduling/)ITI-115`$find`+ ITI-117`$book`(partial — la mitad de reserva; el ciclo oferta/confirmación/persecución es propio de la guía). 360X PCC-60 Appointment Notification solo como patrón (partial — notifica al iniciador; no es una reserva). |

#### OP-4 — Re-ofertar / re-agendar (PI-2)

| | |
| :--- | :--- |
| **Interacción** | Rechazo → el Appointment de la oferta pasa a`cancelled`; la re-oferta es un Appointment NUEVO (OP-3 de nuevo,`offer-number`+1). Conflicto antes de la cita → mismo Appointment, nuevo Slot (Scheduling`$book`modify, ITI-117). No-show → el Appointment viejo queda`noshow`; la oferta re-agendada es un Appointment NUEVO por el mismo ciclo confirmar/perseguir (N5) |
| **Entradas** | El rechazo de la paciente, el conflicto de agenda o el no-show; los conteos del Task (`offer-decline-count`,`offer-chase-count`,`rescheduling-count`) |
| **Salidas** | Un Appointment nuevo (`proposed`) o el mismo Appointment con nuevo Slot; los conteos actualizados en el Task |
| **Ejemplo** | [Cita REF-2026-0001](Appointment-cita-ref-2026-0001.md)(`offer-number`= 1; una re-oferta sería un Appointment nuevo con`offer-number`= 2) |
| **IHE** | Scheduling ITI-117`$book`(partial — modificar una cita reservada). Las reglas de re-oferta y re-agendamiento (conteos, ciclo) son propias de la guía. |

#### OP-5 — Registrar asistencia / no-show (PI-2)

| | |
| :--- | :--- |
| **Interacción** | Asistencia:`PATCH Appointment/{id}`(`status = arrived`, luego`fulfilled`al terminar el encuentro) +`PATCH Encounter/{id}`(`planned`→`in-progress`en la asistencia, →`finished`al terminar el encuentro). No-show:`PATCH Appointment/{id}`(`status = noshow`+`cancelationReason`) + Slot →`free`+ Communication a APS; tras el segundo no-show el Task pasa a`failed`/`businessStatus = no-show`y la derivación se cierra |
| **Entradas** | La asistencia o la ausencia de la paciente en la cita |
| **Salidas** | Appointment`fulfilled`+ Encounter`finished`(o`noshow`+ Slot`free`); el Task avanza a`completed`(o a`failed`en el segundo no-show) |
| **Ejemplo** | [Encuentro REF-2026-0001](Encounter-encuentro-ref-2026-0001.md)(el encuentro que OP-5 lleva de`planned`a`finished`) |
| **IHE** | 360X PCC-61 No-show Notification solo como patrón (partial). El registro de asistencia en sí es propio de la guía. |

#### OP-6 — Enviar contrareferencia (PI-3)

| | |
| :--- | :--- |
| **Interacción** | `POST [base]/Bundle`(`type = document`: Composition primera entrada + DocumentReference + Condition + CarePlan) → el hub la enruta a APS → APS acusa recibo (`POST Communication`,`basedOn`→ Task,`payload.contentReference`→ DocumentReference) → Task →`completed`/`businessStatus = counter-referred` |
| **Entradas** | El diagnóstico (ICD-10-CM I50.22 + SNOMED CT 417996009), el plan y el plan de seguimiento del especialista |
| **Salidas** | El documento de contrareferencia en APS; el acuse de recibo; el Task en`counter-referred`(ciclo cerrado) |
| **Ejemplo** | [Bundle de documento PI-3](Bundle-bundle-pi3-ref-2026-0001.md)—[Composition](Composition-contrareferencia-ref-2026-0001.md),[DocumentReference](DocumentReference-documento-ref-2026-0001.md),[Condition](Condition-diagnostico-ref-2026-0001.md),[CarePlan](CarePlan-plan-ref-2026-0001.md) |
| **IHE** | [MHD](https://profiles.ihe.net/ITI/MHD/)ITI-65 Provide Document Bundle (full para la pierna de transporte del documento, si la guía implementa ITI-65 exacto con metadatos XDS); 360X PCC-57 Referral Outcome solo como patrón de contenido (partial). La transición del Task + el acuse son propios de la guía.[DSUBm](https://profiles.ihe.net/ITI/DSUBm/)ITI-110 (partial — APS se suscribe a que el documento esté disponible). |

#### OP-7 — Consultar el estado de la derivación (PI-4)

| | |
| :--- | :--- |
| **Interacción** | `GET [base]/Task?focus:ServiceRequest.identifier={referral-id}`(o`GET [base]/Task/{id}`) → el Task con`status`,`businessStatus`,`lastModified`, los plazos SLA y los conteos, más el próximo paso esperado (`Task.description`). Solo lectura; la consulta nunca cambia el estado |
| **Entradas** | El identificador de la derivación |
| **Salidas** | El estado actual, el último cambio de estado y el próximo paso esperado (spec §3.7), o`not found`(APS verifica el id) |
| **Ejemplo** | [Task REF-2026-0001](Task-tarea-ref-2026-0001.md)(el recurso que OP-7 lee) |
| **IHE** | **None applies**— ningún perfil IHE lleva una consulta de estado de flujo de trabajo (QEDm PCC-44 cubre solo datos clínicos; DSUBm cubre solo eventos de documento). Búsqueda FHIR simple. |

#### OP-8 — Cancelar derivación (cualquier PI, antes de completarse)

| | |
| :--- | :--- |
| **Interacción** | `PATCH [base]/Task/{id}`(`status = cancelled`+`statusReason`, incl. "patient deceased") +`PATCH Appointment/{id}`(`status = cancelled`+`cancelationReason`) donde haya cita reservada + Slot →`free`+ Communication a APS, paciente y especialidad + entrada Provenance |
| **Entradas** | La solicitud de cancelación (APS, paciente o especialidad) con su motivo |
| **Salidas** | El Task en`cancelled`(terminal, salvo el único camino de corrección: re-apertura por el operador del hub); todas las partes notificadas |
| **Ejemplo** | [Tarea REF-2026-0001](Task-tarea-ref-2026-0001.md)(el Task que OP-8 lleva a`cancelled`) |
| **IHE** | 360X PCC-58 Referral Cancellation solo como patrón (partial — y con tope de dirección: PCC-58 viaja solo Initiator → Recipient, mientras este caso permite que la especialidad o la paciente inicien la cancelación); Scheduling ITI-117`$book`(partial — cancela la cita reservada). La transición del Task + el abanico de avisos son propios de la guía. |

#### OP-9 — Resolver la identidad del paciente (PI-0, apoyo)

| | |
| :--- | :--- |
| **Interacción** | Antes de la creación:`GET [base]/Patient/$ihe-pix?identifier=…`(PIXm ITI-83) devuelve la clave MPI; o`GET [base]/Patient?family=…&given=…`(PDQm ITI-78) encuentra a la paciente por demográficos |
| **Entradas** | El identificador local o los demográficos de la paciente |
| **Salidas** | La clave MPI (o la paciente encontrada); sin identidad resuelta no se crea la derivación |
| **Ejemplo** | [María González](Patient-maria-gonzalez.md)(la paciente con su clave MPI y su RUN) |
| **IHE** | [PIXm](https://profiles.ihe.net/ITI/PIXm/)ITI-83 (full si se implementa exacto);[PDQm](https://profiles.ihe.net/ITI/PDQm/)ITI-78 (full si exacto). PMIR ITI-93 es la asociación del lado del MPI (alimentación/fusión), ofrecida, no una transacción de PI-0. |

#### OP-10 — Encontrar el servicio / endpoint (PI-0, apoyo)

| | |
| :--- | :--- |
| **Interacción** | `GET [base]/HealthcareService?type=…&active=true`(+`Endpoint`) — el directorio devuelve el servicio de especialidad solicitado y su endpoint |
| **Entradas** | La especialidad solicitada (catálogo local) |
| **Salidas** | El servicio y su endpoint de enrutado |
| **Ejemplo** | [Servicio de cardiología](HealthcareService-servicio-cardiologia.md)(con su endpoint) |
| **IHE** | [mCSD](https://profiles.ihe.net/ITI/mCSD/)ITI-90 Find Matching Care Services (full si se implementa exacto). |

#### OP-11 — Suscribirse a los cambios de estado (todos los PI, apoyo)

| | |
| :--- | :--- |
| **Interacción** | `POST [base]/Subscription`(`criteria = "Task?focus:ServiceRequest.identifier={referral-id}"`,`channel.type = rest-hook`,`channel.endpoint`= URL del suscriptor,`channel.payload = application/fhir+json`) → el hub notifica en cada transición del Task |
| **Entradas** | El identificador de la derivación y el endpoint del suscriptor |
| **Salidas** | La suscripción activa; una notificación por cada transición del Task |
| **Ejemplo** | [Task REF-2026-0001](Task-tarea-ref-2026-0001.md)(el recurso sobre el que se suscribe OP-11) |
| **IHE** | **None applies**— una`Subscription`FHIR sobre un evento que no es de documento es propia de la guía (DSUB/DSUBm suscriben solo eventos de documento). |

#### OP-12 — Notificar un cambio de estado (todos los PI, apoyo)

| | |
| :--- | :--- |
| **Interacción** | `POST [base]/Communication`(`status = completed`,`basedOn`→ Task,`sender`,`recipient`,`sent`,`medium`,`payload`= el aviso) → el sistema del destinatario. Los emisores nombrados son C5/Q3 |
| **Entradas** | La transición que disparó el aviso, el emisor y el destinatario nombrados, el canal |
| **Salidas** | La Communication registrada (el registro del envío, no el contenido en sí) |
| **Ejemplo** | [Notificación de aceptación](Communication-notificacion-aceptacion-ref-2026-0001.md)(el administrativo de APS informa a la paciente) |
| **IHE** | **None applies**para la notificación en sí — un envío`Communication`es propio de la guía. (DSUBm ITI-110/111/112 cubre solo la notificación de eventos de documento — aplica a que la contrareferencia esté disponible, OP-6, no a los avisos de cambio de estado.) |

#### Resumen por punto

| | | |
| :--- | :--- | :--- |
| PI-0 | OP-1, OP-9, OP-10 (+ OP-11, OP-12) | PIXm ITI-83, PDQm ITI-78, mCSD ITI-90 (full en los sub-pasos); 360X PCC-55 patrón |
| PI-1 | OP-2 (+ OP-8, OP-12) | 360X PCC-56 patrón (rama de rechazo) |
| PI-2 | OP-3, OP-4, OP-5 (+ OP-8, OP-12) | Scheduling ITI-115/117 (mitad de reserva); 360X PCC-60/61 patrón |
| PI-3 | OP-6 (+ OP-12) | MHD ITI-65 (pierna de documento); 360X PCC-57 patrón; DSUBm ITI-110 (disponibilidad) |
| PI-4 | OP-7 | None applies (explícito) |

