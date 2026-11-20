# Diagramas de secuencia

Un diagrama por flujo del BPMN, con sus participantes tomados de los
carriles. Cada mensaje nombra la operación que lo lleva (id OP-n,
interacción FHIR, perfil IHE + transacción donde aplica); bajo cada
diagrama, la tabla mensaje → operación → perfil IHE → resultado esperado.
Regla dura: cada operación OP-1…OP-12 aparece en al menos un diagrama; un
mensaje sin operación es una interacción inventada. Comprobación mecánica:
`python3 render_sequence.py --check` → 0 mensajes sin operación, 0
operaciones sin diagrama (39 mensajes de envío, 9 retornos).

Los mensajes a la paciente (teléfono / presencial) son mensajes no-FHIR
declarados como tales en su etiqueta. Una respuesta que llega en otra
sesión o día es su propio diagrama, enlazado por el identificador de la
derivación (REF-2026-0001) — nunca un retorno en el diagrama que envía.

## 1. Solicitud (PI-0)

<div style="overflow-x: auto; border: 1px solid #ccc; padding: 4px;">
<img src="04-sequence-request.png" alt="Diagrama de secuencia — solicitud (PI-0)" style="max-width: none; width: 2180px;" />
</div>

[SVG](04-sequence-request.svg) · BPMN Parte A.

| # | Mensaje | Operación | Perfil IHE | Resultado esperado |
|---|---|---|---|---|
| 1 | Médico APS → MPI: resolver identidad | OP-9 | PIXm ITI-83 `$ihe-pix` / PDQm ITI-78 | Clave MPI, o "no resuelta" (el médico corrige y reintenta; sin identidad no se crea la derivación) |
| 2 | Médico APS → Hub: crear derivación | OP-1 | 360X PCC-55 solo como patrón | Bundle de transacción aceptado (ServiceRequest + Task `requested`); el hub valida y enruta |
| 3 | Hub → Directorio: encontrar servicio | OP-10 | mCSD ITI-90 (full si exacto) | HealthcareService + Endpoint del servicio solicitado |
| 4 | Hub → Especialidad: reenviar derivación (m11) | OP-1 | 360X PCC-55 solo como patrón | Derivación recibida por la especialidad |
| 5 | Hub → APS admin: notificar creación | OP-12 | None applies (notificación propia) | Communication registrada; APS admin informa a la paciente |
| 6 | APS admin → Paciente: avisar de la creación | OP-12 | Non-FHIR (teléfono / presencial) | La paciente conoce la derivación y su destino |
| 7 | APS admin → Hub: suscribirse a los cambios (opt) | OP-11 | None applies (Subscription FHIR sobre Task) | 201 Created; el hub notifica en cada transición del Task |

## 2. Triaje (PI-1)

<div style="overflow-x: auto; border: 1px solid #ccc; padding: 4px;">
<img src="04-sequence-triage.png" alt="Diagrama de secuencia — triaje (PI-1)" style="max-width: none; width: 1280px;" />
</div>

[SVG](04-sequence-triage.svg) · BPMN Parte A.

| # | Mensaje | Operación | Perfil IHE | Resultado esperado |
|---|---|---|---|---|
| 1 | Clínico de triaje → Hub: registrar aceptación | OP-2 | None applies para la aceptación (360X no tiene transacción de aceptar) | Task `accepted` + `owner` = el servicio que acepta; el profesional que acepta va como agente de Provenance en la entrada de aceptación |
| 2 | Clínico de triaje → Hub: registrar rechazo | OP-2 | 360X PCC-56 solo como patrón (rama de rechazo) | Task `rejected` + `statusReason` |
| 3 | Hub → APS admin: reenviar decisión | OP-12 | None applies | Communication registrada; APS admin informa a la paciente |
| 4 | APS admin → Paciente: avisar de la decisión | OP-12 | Non-FHIR (teléfono / presencial) | La paciente conoce la aceptación o el rechazo con su motivo |

## 3. Agendamiento (PI-2)

<div style="overflow-x: auto; border: 1px solid #ccc; padding: 4px;">
<img src="04-sequence-schedule.png" alt="Diagrama de secuencia — agendamiento (PI-2)" style="max-width: none; width: 1580px;" />
</div>

[SVG](04-sequence-schedule.svg) · BPMN Parte B. El `loop` cubre el ciclo
de oferta hasta reservar o cancelar; el `alt` separa confirmar de
rechazar.

| # | Mensaje | Operación | Perfil IHE | Resultado esperado |
|---|---|---|---|---|
| 1 | Agendador → Servidor: buscar huecos | OP-3 | Scheduling ITI-115 `$find` (partial) | Slots libres |
| 2 | Agendador → Hub: ofrecer cita | OP-3 | None applies para la oferta (Scheduling no publica/notifica) | Appointment `proposed` |
| 3 | Hub → Paciente: oferta | OP-12 | Non-FHIR (teléfono / presencial) | La paciente recibe la oferta |
| 4 | Hub → APS admin: notificar oferta | OP-12 | None applies | Communication registrada |
| 5 | Agendador → Paciente: perseguir confirmación (opt, hasta 2 veces) | OP-12 | Non-FHIR (teléfono) | La paciente responde, o tras la segunda persecución la derivación vuelve al re-triaje de APS |
| 6 | Paciente → Hub: confirmar asistencia | OP-3 | None applies para la confirmación | AppointmentResponse `accepted`; Appointment → `pending` |
| 7 | Hub → Agendador: confirmación reenviada | OP-3 | None applies | El agendador recibe la confirmación |
| 8 | Agendador → Servidor: reservar cita | OP-3 | Scheduling ITI-117 `$book` (partial) | Appointment `booked`, Slot `busy` |
| 9 | Agendador → Hub: cita reservada | OP-3 | None applies | Appointment `booked` + Encounter `planned` |
| 10 | Hub → APS admin: notificar reserva | OP-12 | None applies | Communication registrada |
| 11 | Paciente → Hub: rechazar oferta | OP-4 | None applies | AppointmentResponse `declined`; el Appointment de la oferta pasa a `cancelled` |
| 12 | Hub → Agendador: rechazo reenviado | OP-4 | None applies | El agendador recibe el rechazo |
| 13 | Agendador → Hub: re-ofertar cita | OP-4 | Scheduling ITI-117 `$book` para la reserva posterior (partial) | Appointment NUEVO `proposed` (`offer-number` +1); el ciclo vuelve a empezar |

## 4. Atención (PI-2)

<div style="overflow-x: auto; border: 1px solid #ccc; padding: 4px;">
<img src="04-sequence-attend.png" alt="Diagrama de secuencia — atención (PI-2)" style="max-width: none; width: 1280px;" />
</div>

[SVG](04-sequence-attend.svg) · BPMN Parte B.

| # | Mensaje | Operación | Perfil IHE | Resultado esperado |
|---|---|---|---|---|
| 1 | Paciente → Especialista: llegada | OP-5 | Non-FHIR (llegada presencial) | La paciente está en la consulta |
| 2 | Especialista → Hub: registrar asistencia | OP-5 | None applies | Appointment `arrived`, Encounter `in-progress` |
| 3 | Especialista → Hub: encuentro terminado | OP-5 | None applies | Encounter `finished`, Appointment `fulfilled`; el Task avanza a `completed` |
| 4 | Especialista → Hub: registrar no-show | OP-5 | 360X PCC-61 solo como patrón | Appointment `noshow` + `cancelationReason`; Slot `free`; no hay Encounter |
| 5 | Hub → APS admin: notificar no-show | OP-12 | None applies | Communication registrada; APS decide el seguimiento |
| 6 | Especialista → Hub: re-agendar cita | OP-4 | None applies | Appointment NUEVO (mismo ciclo confirmar/perseguir); tras el segundo no-show el Task pasa a `failed` / `no-show` y la derivación se cierra |

## 5. Contrareferencia (PI-3)

<div style="overflow-x: auto; border: 1px solid #ccc; padding: 4px;">
<img src="04-sequence-result-return.png" alt="Diagrama de secuencia — contrareferencia (PI-3)" style="max-width: none; width: 1280px;" />
</div>

[SVG](04-sequence-result-return.svg) · BPMN Parte B.

| # | Mensaje | Operación | Perfil IHE | Resultado esperado |
|---|---|---|---|---|
| 1 | Especialista → Hub: enviar contrareferencia | OP-6 | 360X PCC-57 solo como patrón de contenido | Bundle de documento aceptado (Composition + DocumentReference + Condition + CarePlan) |
| 2 | Hub → APS admin: reenviar contrareferencia | OP-6 | MHD ITI-65 Provide Document Bundle (full si exacto) | Documento en APS |
| 3 | APS admin → Médico APS: entregar contrareferencia | OP-12 | None applies | El médico APS tiene el diagnóstico, el plan y el seguimiento |
| 4 | APS admin → Hub: acuse de recibo | OP-6 | None applies para el acuse | Communication registrada (`basedOn` → Task); Task `completed` / `counter-referred` — ciclo cerrado |

## 6. Consulta de estado (PI-4)

<div style="overflow-x: auto; border: 1px solid #ccc; padding: 4px;">
<img src="04-sequence-status-query.png" alt="Diagrama de secuencia — consulta de estado (PI-4)" style="max-width: none; width: 1040px;" />
</div>

[SVG](04-sequence-status-query.svg) · BPMN Parte C.

| # | Mensaje | Operación | Perfil IHE | Resultado esperado |
|---|---|---|---|---|
| 1 | APS → Hub: consultar estado | OP-7 | **None applies** (explícito — ningún perfil IHE lleva una consulta de estado de flujo de trabajo) | Task con `status`, `businessStatus`, `lastModified` y próximo paso esperado; o 404 |
| 2 | Hub → APS: estado actual (o no encontrado) | OP-7 | None applies | APS registra el estado en su historia; si no se encontró, verifica el identificador |

## 7. Cancelación

<div style="overflow-x: auto; border: 1px solid #ccc; padding: 4px;">
<img src="04-sequence-cancellation.png" alt="Diagrama de secuencia — cancelación" style="max-width: none; width: 1580px;" />
</div>

[SVG](04-sequence-cancellation.svg) · BPMN Partes A y B (fila de
cancelación).

| # | Mensaje | Operación | Perfil IHE | Resultado esperado |
|---|---|---|---|---|
| 1 | APS admin → Hub: solicitar cancelación | OP-8 | 360X PCC-58 solo como patrón (con tope de dirección: PCC-58 viaja solo Initiator → Recipient) | Task `cancelled` + `statusReason` (incl. "patient deceased") |
| 2 | Hub → Agendador: cancelar cita reservada (opt) | OP-8 | Scheduling ITI-117 `$book` cancel (partial) | Appointment `cancelled`; Slot `free` |
| 3 | Hub → Paciente: notificar cancelación | OP-12 | Non-FHIR (teléfono / presencial) | La paciente conoce la cancelación y su motivo |
| 4 | Hub → Especialista: notificar cancelación | OP-12 | None applies | Communication registrada; la especialidad conoce la cancelación |

La cancelación la puede iniciar APS (mostrada), la paciente o la
especialidad del mismo modo (misma OP-8, misma transición del Task; el
solicitante queda en Provenance).

## Cobertura de operaciones

| Operación | Diagramas |
|---|---|
| OP-1 Crear derivación | 1. Solicitud |
| OP-2 Registrar decisión de triaje | 2. Triaje |
| OP-3 Ofrecer / confirmar / reservar cita | 3. Agendamiento |
| OP-4 Re-ofertar / re-agendar | 3. Agendamiento, 4. Atención |
| OP-5 Registrar asistencia / no-show | 4. Atención |
| OP-6 Enviar contrareferencia | 5. Contrareferencia |
| OP-7 Consultar estado | 6. Consulta de estado |
| OP-8 Cancelar derivación | 7. Cancelación |
| OP-9 Resolver identidad | 1. Solicitud |
| OP-10 Encontrar servicio / endpoint | 1. Solicitud |
| OP-11 Suscribirse a los cambios | 1. Solicitud |
| OP-12 Notificar cambio de estado | 1. Solicitud, 2. Triaje, 3. Agendamiento, 4. Atención, 5. Contrareferencia, 7. Cancelación |
