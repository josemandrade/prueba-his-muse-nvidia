# Ciclo de vida

Una tabla por (recurso, máquina): la operación que dispara cada
transición (con su PI), las transiciones prohibidas y las invariantes
entre máquinas, cada una con su test de transición prohibida. El estado
del caso vive en el `Task`; los demás recursos son espejos o máquinas
propias que el hub mantiene consistentes.

## Task (`DerivacionTarea`) — la máquina de estados de la derivación

| Estado del caso (`businessStatus`) | `Task.status` | Próximos estados permitidos (operación + PI) | Prohibido |
|---|---|---|---|
| `requested` | `requested` | `received` (OP-1 enrutado, PI-0); `cancelled` (OP-8, cualquier PI) | Cualquier otro estado — una derivación no puede aceptarse, agendarse o completarse antes de recibirse. |
| `received` | `received` | `accepted` (OP-2 aceptar, PI-1); `rejected` (OP-2 rechazar, PI-1); `cancelled` (OP-8) | `scheduled`, `completed`, `counter-referred`, `no-show` — no hay cita antes del triaje. |
| `accepted` | `accepted` | `scheduled` (OP-3/OP-4 reserva, PI-2); `cancelled` (OP-8) | `completed`, `counter-referred`, `no-show` — no hay visita antes de la reserva. |
| `rejected` | `rejected` | (terminal, tras la decisión de re-triaje de APS — la re-derivación es un Task + ServiceRequest NUEVOS, OP-1, PI-0); `cancelled` (OP-8, antes de la decisión de re-triaje) | `scheduled`, `completed`, `counter-referred` — una derivación rechazada nunca avanza; se cierra como `rejected` una vez APS decide el resultado del re-triaje (N1). La derivación se queda en `rejected` con el reloj de re-triaje corriendo hasta que APS decide. |
| `scheduled` | `ready` | `completed` (OP-5 encuentro terminado, PI-2 — el Encounter llegó a `finished`); `cancelled` (OP-8) | `counter-referred` — no hay contrareferencia antes de la visita. El `no-show` NO es una transición del Task desde aquí (el no-show vive en el Appointment; el Task se mueve en el segundo no-show). |
| `completed` | `in-progress` | `counter-referred` (OP-6, PI-3); `cancelled` (OP-8 — solo antes de enviarse la contrareferencia) | `scheduled`, `accepted` — la visita está hecha; el único camino es la contrareferencia. |
| `counter-referred` | `completed` | — (terminal) | Todas las transiciones — el ciclo está cerrado. Una corrección es una versión nueva del documento, no un cambio de estado. |
| `no-show` | `failed` | — (terminal) | Todas las transiciones — la derivación se cerró tras el segundo no-show. Una derivación nueva necesita un Task nuevo. |
| `cancelled` | `cancelled` | — (terminal, salvo el único camino de corrección: re-apertura al estado previo a la cancelación con una entrada explícita de re-apertura, solo el operador del hub) | Todas las demás transiciones — una derivación cancelada no puede avanzar; el hub rechaza los cambios de estado de derivaciones terminales. |

Condición terminal basada en tiempo: los plazos SLA no son estados — un
incumplimiento de plazo dispara una escalada (hub → especialidad + APS, o
hub → APS para el timeout de re-triaje, o la persecución del agendador
para el timeout de confirmación), nunca un cambio de estado. Una
derivación nunca se cierra solo por timeout.

## ServiceRequest (`DerivacionSolicitud`) — espejo grueso

| `ServiceRequest.status` | Próximos estados permitidos (operación + PI) | Prohibido |
|---|---|---|
| `draft` | `active` (OP-1 crear, PI-0) | Cualquier otro estado — un borrador no se ha enviado. |
| `active` | `completed` (OP-6, PI-3); `revoked` (OP-8 cancelar, `no-show` terminal PI-2, o cierre por rechazo en la decisión de re-triaje de APS, PI-1) | `draft`, `on-hold` — el caso no tiene paso de espera; una suspensión es una cancelación + re-derivación, nunca una espera. |
| `completed` | — (terminal) | Todas las transiciones. |
| `revoked` | — (terminal) | Todas las transiciones. |

## Appointment (`DerivacionCita`) — la cadena oferta/reserva

| `Appointment.status` | Próximos estados permitidos (operación + PI) | Prohibido |
|---|---|---|
| `proposed` | `pending` (OP-3 confirmar, PI-2); `cancelled` (OP-3 rechazar → la cita de la oferta se cancela y la re-oferta es un Appointment NUEVO, PI-2) | `booked` — una cita propuesta no se reserva hasta que la paciente confirma. |
| `pending` | `booked` (OP-3 reservar, PI-2); `cancelled` (OP-8, PI-2) | `proposed`, `noshow` — una cita pendiente no vuelve a propuesta ni puede ser un no-show. |
| `booked` | `arrived` (OP-5 asistir, PI-2); `noshow` (OP-5 no-show, PI-2); `cancelled` (OP-8, PI-2); `booked` (mismo Appointment, nuevo Slot — re-agendamiento tras un conflicto previo a la asistencia, PI-2) | `proposed`, `pending` — una cita reservada no vuelve al ciclo de oferta; una oferta re-agendada tras un no-show es un Appointment NUEVO. |
| `arrived` | `fulfilled` (OP-5 encuentro terminado, PI-2) | Todos los demás estados — la llegada lleva a la visita. |
| `fulfilled` | — (terminal para este Appointment) | Todas las transiciones. |
| `noshow` | (terminal para este Appointment — la oferta re-agendada es un Appointment NUEVO, `proposed`, OP-4, PI-2) | `booked`, `arrived`, `fulfilled` — un Appointment no-show nunca se reutiliza. |
| `cancelled` | — (terminal) | Todas las transiciones — un Appointment cancelado nunca se reutiliza. |

El Slot vuelve a `free` en `noshow` y en `cancelled` (`Slot.status`
`busy` → `free`).

## Encounter (`DerivacionEncuentro`)

| `Encounter.status` | Próximos estados permitidos (operación + PI) | Prohibido |
|---|---|---|
| `planned` (creado por OP-3 en la reserva, PI-2) | `in-progress` (OP-5 asistir, PI-2); `cancelled` (OP-8 — solo antes de empezar la visita) | `finished` — una visita no puede terminar antes de empezar. |
| `in-progress` | `finished` (OP-5 encuentro terminado, PI-2) | `planned`, `cancelled` — una visita en curso no puede des-empezarse ni cancelarse (una cancelación tras empezar la visita se registra en el Task, no cancelando el Encounter). |
| `finished` | — (terminal) | Todas las transiciones. |

## CarePlan (`DerivacionPlanSeguimiento`) — el plan de seguimiento

| `CarePlan.status` | Próximos estados permitidos (operación + PI) | Prohibido |
|---|---|---|
| `draft` | `active` (OP-6 enviar, PI-3) | Cualquier otro estado. |
| `active` | `completed` (APS completa el seguimiento, PI-3); `revoked` (el especialista retira el plan — versión nueva, PI-3) | `draft` — un plan activo no vuelve a borrador. |
| `completed` / `revoked` | — (terminal) | Todas las transiciones. Una actualización del plan es una versión nueva enlazada por `replaces` / `basedOn`, nunca una sobrescritura silenciosa. |

`Communication` no tiene tabla de ciclo de vida: una notificación se envía
(`status = completed`) o no se envía; el resultado de la entrega es la
extensión `delivery-outcome`. `Condition` tampoco tiene tabla de flujo de
trabajo aquí: sus estados clínico/de verificación (`active` / `confirmed`)
no cambian en este caso.

## Invariantes entre máquinas

| # | Invariante | Test de transición prohibida |
|---|---|---|
| I1 | El Task es la autoridad: ningún paso lee `ServiceRequest.status` para decidir el estado; cada transición del Task que cambia el estado grueso actualiza el ServiceRequest en la misma transacción (OP-1, OP-6, OP-8, cierre por no-show, cierre por rechazo). | Un Task en `accepted` con su ServiceRequest en `revoked` es inconsistente: el test lo rechaza. |
| I2 | Una derivación en estado terminal del Task (`counter-referred`, `rejected`, `no-show`, `cancelled`) no admite más transiciones en ninguna máquina (salvo la re-apertura explícita de una cancelación errónea, solo por el operador del hub). | Un PATCH que mueva un Task `counter-referred` a `scheduled` se rechaza con 409. |
| I3 | Un Appointment `noshow` o `cancelled` nunca se reutiliza; la re-oferta y la oferta re-agendada tras un no-show son Appointments nuevos. | Un PATCH que mueva un Appointment `noshow` a `booked` se rechaza con 409. |
| I4 | No hay Encounter en un no-show: el no-show vive solo en el Appointment. Un Encounter `planned` existe desde la reserva. | Un Encounter creado en la asistencia (sin existir en la reserva) se rechaza. |
| I5 | El plazo de contrareferencia corre desde el Encounter `finished`, no desde el Appointment `arrived`. | Un Task `completed` con `sla-counterreferral-deadline` calculado desde `arrived` es inconsistente: el test lo rechaza. |
| I6 | Un Task `rejected` (cierre) tiene su ServiceRequest en `revoked` en la misma transacción (el cierre por rechazo revoca la solicitud vieja; la re-derivación es una solicitud NUEVA). | Un Task `rejected` (cerrado) con su ServiceRequest en `active` es inconsistente: el test lo rechaza. |
