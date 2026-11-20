# Mapeo de datos

Las entidades del caso (`03-entities-data.md`, §1–§13) mapeadas a recursos
FHIR, campo a campo. La tabla completa, con cardinalidades y notas, está en
`04-mapping-table.md` (fuente de verdad del paso 4); esta página es su
resumen navegable en la guía. Los nombres de entidad son los del paso 3;
los nombres de campo son los del paso 3.

## Resumen por entidad

| Entidad (§3) | Recurso | Perfil |
|---|---|---|
| 1. Patient | `Patient` | [`DerivacionPaciente`](StructureDefinition-derivacion-paciente.html) |
| 2. Referral request | `ServiceRequest` | [`DerivacionSolicitud`](StructureDefinition-derivacion-solicitud.html) |
| 3. Workflow state record | `Task` | [`DerivacionTarea`](StructureDefinition-derivacion-tarea.html) |
| 4. Triage decision | Transición del Task + Provenance (sin recurso propio) | [`DerivacionTarea`](StructureDefinition-derivacion-tarea.html) |
| 5. Appointment (+ Slot) | `Appointment` + `Slot` (+ `Schedule`) | [`DerivacionCita`](StructureDefinition-derivacion-cita.html) |
| 6. Specialty encounter | `Encounter` | [`DerivacionEncuentro`](StructureDefinition-derivacion-encuentro.html) |
| 7. Counter-referral | `Composition` + `DocumentReference` + `Condition` + `CarePlan` | [`DerivacionContrareferencia`](StructureDefinition-derivacion-contrareferencia.html), [`DerivacionDocumento`](StructureDefinition-derivacion-documento.html), [`DerivacionDiagnostico`](StructureDefinition-derivacion-diagnostico.html), [`DerivacionPlanSeguimiento`](StructureDefinition-derivacion-plan-seguimiento.html) |
| 8. Practitioner | `Practitioner` + `PractitionerRole` | [`DerivacionRol`](StructureDefinition-derivacion-rol.html) |
| 9. Organisation / care service | `Organization` + `HealthcareService` + `Location` + `Endpoint` | [`DerivacionServicio`](StructureDefinition-derivacion-servicio.html) |
| 10. MPI identity record | `Patient` del MPI + transacciones PIXm/PMIR (no se intercambia como recurso en el flujo) | [`DerivacionPaciente`](StructureDefinition-derivacion-paciente.html) |
| 11. Notification | `Communication` | [`DerivacionNotificacion`](StructureDefinition-derivacion-notificacion.html) |
| 12. Declined-referral record | **Sin equivalente FHIR** (registro local de APS) | — |
| 13. Cancellation record | Transición del Task + `Appointment` + `Communication` + Provenance (sin recurso propio) | [`DerivacionTarea`](StructureDefinition-derivacion-tarea.html) |

## Reglas de transformación

- **El estado vive en el Task, no en la solicitud.** `Task.businessStatus`
  lleva el estado del caso textual (los nueve estados); `Task.status`
  lleva el valor grueso de R4. `ServiceRequest.status` es un espejo
  grueso, que el hub mantiene consistente en la misma transacción que
  cada transición del Task.
- **Los estados del caso no son valores FHIR.** `offered`, `confirmed`,
  `re-scheduled`, `attended` (cita) y `scheduled` (encuentro) son lenguaje
  del caso: se mapean a `proposed` / `pending` / `booked` / `arrived` /
  `fulfilled` (cita) y a `planned` (encuentro). Nunca se inventa un valor
  de ValueSet.
- **Una corrección nunca sobrescribe.** Un dato erróneo se corrige con una
  versión nueva (mismo identificador, versión +1, supersede la anterior)
  o con una entrada compensatoria en el historial del Task. El historial
  es solo-añadir.
- **Un rechazo o una cancelación no van en el estado de la solicitud.**
  La regla del pack: nunca se pone aceptar/rechazar en el estado de la
  solicitud (además `ServiceRequest` no tiene `statusReason`); el motivo
  viaja en `Task.statusReason` y/o en `Appointment.cancelationReason`.
- **Lo que falta, bloquea.** Un campo obligatorio que falta bloquea el
  paso que lo necesita (creación, aceptación, oferta): el paso falla la
  validación, no avanza en blanco. La única excepción es el plazo de
  confirmación, que dispara una persecución en vez de un bloqueo.
- **Lo que no viaja, no se inventa.** La entidad 12 (derivación
  rechazada por el paciente en la creación) no tiene recurso: no se crea
  nada y nada viaja; registrarla como `Task` o `Communication`
  inventaría una derivación que el caso deliberadamente no tiene.

## Correcciones R4 encontradas en el paso 5

Dos filas de la tabla de mapeo del paso 4 eran incorrectas en R4 y la
guía las corrige (registrado en `decisions.md`):

- **`Communication.topic` (§11):** en R4 es un CodeableConcept 0..1, no
  una referencia al Task. La guía lleva el nombre codificado de la
  transición en `topic`; el enlace al Task es `basedOn` y el aviso
  legible es `payload.contentString`.
- **`Task.owner` (§3/§4):** en R4 es 0..1, no 0..*. La guía pone en
  `owner` el servicio que acepta (el responsable del trabajo); el
  profesional que acepta se registra como agente de Provenance en la
  entrada de aceptación del historial.
