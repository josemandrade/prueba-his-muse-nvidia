# Componente de derivación APS → especialidad (paso 6)

Implementación en Python de la [guía validada](../05-implementation-guide/)
(derivación APS → especialidad con contrareferencia, SUSHI 0 errores,
74 recursos, canónica
`https://josemandrade.github.io/prueba-his-muse-nvidia/`). Construye
SOLO lo que la guía dice: el flujo de derivación (crear → triaje →
agendar → atender → contrareferencia → consultar estado → cancelar),
con el Task como centro (`businessStatus` = los 9 estados del caso),
los plazos SLA, los conteos de decline/chase/re-agendamiento y las
notificaciones con emisor nombrado.

Fuente de verdad: `05-implementation-guide/` (`operations.md`,
`lifecycle.md`, `plan.md`, FSH y ejemplos compilados) más
`04-fhir-proposal.md` y `04-mapping-table.md`. Los 31 ejemplos
compilados por SUSHI viven como goldens en `tests/goldens/` (copias
textuales, nunca editados); los tests comparan contra ellos.

## Stack

**Python 3.12, solo stdlib** (`json`, `unittest`, `argparse`,
`datetime`). Sin dependencias nuevas.

- `pytest` **no está instalado** en este entorno; los tests usan
  `unittest` (stdlib): `PYTHONPATH=src python3 -m unittest discover -s tests -v`
  o `sh run_tests.sh`.
- Sin Java, sin SUSHI para correr el componente (SUSHI solo hizo
  falta para compilar la guía, paso 5). La validación completa
  (IG Publisher / validador FHIR) corre en CI (`ig-build.yml`).

## Datos sintéticos siempre

Todos los datos son ficticios (María González, 58, RUN sintético
11.111.111-1, MPI-2026-0042, CESFAM Los Aromos → cardiología,
REF-2026-0001, sospecha de insuficiencia cardiaca, ICD-10-CM I50.22
+ SNOMED CT 417996009). **Nada de datos reales de pacientes** en el
código, los ejemplos, los tests ni este README.

Desviaciones conocidas respecto de la guía: están registradas como
`Ruling:` en `../state.md` (también resumidas abajo).

## Cómo correr los tests

```sh
cd 06-component
sh run_tests.sh
# o bien:
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

168 tests, todos en verde. Cada test se escribió antes que el código
(RED-GREEN); el plan en `plan.md` detalla la descomposición en las
Plan tasks 11.1–11.13.

## Cómo correr el componente

```sh
cd 06-component
PYTHONPATH=src python3 -m derivacion.cli accepted [--out DIR]
PYTHONPATH=src python3 -m derivacion.cli rejected [--out DIR]
PYTHONPATH=src python3 -m derivacion.cli no-show [--out DIR]
```

Cada escenario escribe un JSON por recurso en el directorio de
salida (por defecto `examples/<escenario>/`) más `summary.json` con
el estado final, y resume el recorrido en stdout. No envía nada a
ningún servidor: el registro MPI y el directorio son en memoria,
sembrados con el ejemplo trabajado (`derivacion.registry`,
`seed_worked_example`).

## Ejemplos trabajados

Los tres recorridos están generados en `examples/`:

| Escenario | Recorrido | Estado final |
|---|---|---|
| `accepted` | creación → aceptación → oferta → confirmación → reserva → atención → contrareferencia acusada | `counter-referred` (Task `completed`, ServiceRequest `completed`) |
| `rejected` | creación → triaje rechaza (capacidad) → APS resuelve en APS | `rejected` (ServiceRequest `revoked`) |
| `no-show` | creación → … → reserva → no-show → re-agendamiento → reserva → segundo no-show | `no-show` (Task `failed`, ServiceRequest `revoked`) |

En los tres, `summary.json` reporta `invariant_violations: []`
(I1–I6 limpias).

## Trazabilidad

Operación → módulo → función → test:

| Operación | Módulo | Función | Test |
|---|---|---|---|
| OP-1 crear + enrutar | `workflow.py` | `Referral.create`, `route`, `transaction_bundle` | `test_op01.py` (8), `test_op04.py` (guardas de identidad/servicio) |
| OP-2 triaje + re-triaje | `workflow.py` | `triage`, `decide_retriage` | `test_op04.py` (16) |
| OP-3 ofrecer / confirmar / reservar | `workflow.py`, `builders.py` | `offer_appointment`, `respond_to_offer`, `book_appointment`, `build_appointment`, `build_appointment_response`, `build_encounter`, `build_slot`, `build_schedule`, `build_location` | `test_op03.py` (7), `test_op04.py` |
| OP-4 re-ofertar / re-agendar | `workflow.py` | `respond_to_offer` (rechazo), `offer_appointment` (re-oferta), `reschedule_before_visit`, `reschedule_after_no_show`, `return_to_retriage`, `chase_offer` | `test_op04.py` (16) |
| OP-5 asistencia / no-show | `workflow.py` | `record_arrival`, `finish_encounter`, `record_no_show` | `test_op05.py` (7) |
| OP-6 contrareferencia | `workflow.py`, `builders.py` | `send_counter_referral`, `acknowledge_counter_referral`, `build_condition`, `build_care_plan`, `build_composition`, `build_document_reference`, `build_document_bundle` | `test_op06.py` (9) |
| OP-7 consulta de estado | `workflow.py` | `query_status` | `test_op07_op08.py` (12) |
| OP-8 cancelar / re-abrir | `workflow.py` | `cancel`, `reopen` | `test_op07_op08.py` (12) |
| OP-9 resolver identidad | `registry.py` | `resolve_patient` (MPI local) | `test_op09_op10.py` (16) |
| OP-10 encontrar servicio | `registry.py` | `find_service` (directorio local) | `test_op09_op10.py` (16) |
| OP-11 suscripción | `workflow.py`, `builders.py` | `subscribe`, `unsubscribe`, `build_subscription` | `test_op11.py` (6) |
| OP-12 notificar | `workflow.py`, `builders.py` | `_notify`, `build_communication` | `test_op02_op12.py` (6), `test_op04.py`, `test_op05.py`, `test_op06.py`, `test_op07_op08.py` |
| SLA (R1–R5) | `evaluator.py`, `working_days.py` | `evaluate_escalations`, `sla_deadlines`, `apply_sla_actions` | `test_sla.py` (26), `test_op04.py` (R3), `test_op06.py` (R4) |
| Escenarios end-to-end | `scenarios.py`, `cli.py` | `accepted_scenario`, `rejected_scenario`, `no_show_scenario`, `main` | `test_scenarios.py` (8) |

Transiciones → función → test de transición prohibida:

| Máquina | Función | Test |
|---|---|---|
| Task (9 estados del caso) | `transitions.validate_task_transition` | `test_transitions.py` (41): una prueba de `ForbiddenTransition` por cada transición prohibida de la tabla, incluidos los guardados (`accepted → rejected` solo por fallo de agendamiento; `scheduled → no-show` solo en el segundo no-show; `rejected → cancelled` solo antes de la decisión de re-triaje) |
| ServiceRequest, Appointment, Encounter, CarePlan | `validate_service_request_transition`, `validate_appointment_transition`, `validate_encounter_transition`, `validate_careplan_transition` | `test_transitions.py` (41) |
| Invariantes I1–I6 | `transitions.check_invariants`, `Referral.check_invariants` | `test_op05.py`, `test_op06.py`, `test_scenarios.py` |

Guardas → módulo → función → golden que falla si se rompen:

| Guarda | Módulo | Función | Golden |
|---|---|---|---|
| Identidad resuelta antes de crear (OP-9) | `workflow.py` | `Referral.create` | `Bundle-bundle-pi0-ref-2026-0001` (el Bundle no se crea sin paciente en el MPI) |
| Servicio en el directorio (OP-10) | `registry.py` | `find_service` | `HealthcareService-servicio-cardiologia` |
| `Task.owner` = el servicio que acepta; el profesional va como agente de Provenance (corrección R4 del paso 5) | `workflow.py`, `builders.py` | `triage`, `build_provenance` | `Communication-notificacion-aceptacion-ref-2026-0001`, `Task-tarea-ref-2026-0001` |
| `Communication.topic` es CodeableConcept, no referencia (corrección R4 del paso 5) | `builders.py` | `build_communication` | `Communication-notificacion-aceptacion-ref-2026-0001` |
| Cadena de estados de Appointment `proposed → pending → booked` | `transitions.py` | `validate_appointment_transition` | `Appointment-cita-ref-2026-0001` |
| Encounter existe desde la reserva (`planned`), nunca en la asistencia | `workflow.py` | `book_appointment`, `record_arrival` | `Encounter-encuentro-ref-2026-0001` |
| No hay Encounter en un no-show | `workflow.py` | `record_no_show` | `Appointment-cita-ref-2026-0001` (el no-show vive solo en la cita) |

## Reglas del flujo que el componente hace cumplir

- **El Task es la autoridad.** Cada transición valida la tabla de
  `transitions.py` antes de construir el recurso y deja una entrada
  de Provenance con el rol que la hizo. Un `ForbiddenTransition`
  es un 409.
- **Los plazos SLA nunca cambian el estado.** Un vencimiento
  dispara una escalación (hub → especialidad + APS) o el retorno a
  re-triaje (R3), nunca un cierre por tiempo. Una escalación
  dispara una sola vez por plazo; R3 se sigue por el conteo de
  chase, no por la regla disparada.
- **Los conteos pertenecen al ciclo de oferta.** El de decline NO
  se reinicia en la re-oferta tras un rechazo (si no, el gateway
  "First decline?" del BPMN nunca vería el segundo rechazo); se
  reinicia solo cuando empieza un ciclo nuevo tras un no-show (N5).
  El de chase se reinicia en cada oferta. El de re-agendamiento
  (0–1) no se reinicia nunca.
- **El Slot pasa a `busy` en la reserva, no en la oferta**
  (OP-3). El ejemplo compilado muestra el Slot `busy` con el
  Appointment en `proposed`; el componente sigue el texto de OP-3.
- **La contrareferencia cierra el ciclo con el acuse de recibo**,
  no con el envío. El envío desarma R4 y bloquea la cancelación.
- **La cancelación exige motivo** y notifica a paciente, APS y
  especialidad. La re-apertura es solo del operador del hub, solo
  al estado previo a la cancelación; la cita cancelada no se
  restaura (el agendador debe re-ofertar).
- **Días hábiles lunes a viernes, plazos a las 17:00 local.**
  La guía no define calendario de festivos; el componente no
  modela festivos.

## Rulings (decisiones del componente)

Todas están registradas como `Ruling:` en `../state.md` (Plan tasks
11.1–11.13). Las que cambian lo que la guía dice o rellenan un
vacío de la guía:

1. **Retorno por fallo de agendamiento** (`accepted → rejected`):
   lo exige el paso 3 validado (C4) aunque la tabla del paso 4 no
   lo liste. Transición guardada, solo por OP-4/R3.
2. **Conteo de decline por ciclo de oferta**, no por Appointment
   (el texto de la extensión dice "por oferta"; léase "por ciclo").
3. **Triggers `booked` y `chase`** añadidos a la tabla de emisores
   nombrados (los diagramas de secuencia registran Communication
   en la reserva y en cada persecución).
4. **Encounter `planned` de una cita perdida** queda como está y
   se conserva en la historia (la guía no define un `cancelled` de
   encuentro para el no-show).
5. **Re-apertura no restaura la cita cancelada.**
6. **Conteos en cero no viajan** como extensiones del Task (el
   ejemplo de la guía no los lleva).

## Pendiente (fuera de este componente)

- La validación completa de la guía (IG Publisher / validador FHIR)
  corre en CI (`ig-build.yml`); no hay Java en este entorno.
- Las filas §11 y §3/§4 de la tabla de mapeo del paso 4 siguen
  pendientes de corrección en su próximo toque (correcciones R4
  encontradas en el paso 5; la guía ya es correcta donde la tabla
  estaba mal).
