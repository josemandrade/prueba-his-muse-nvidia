# Plan — Componente (paso 6)

Caso: derivación APS → especialidad con contrareferencia. Fuente de
verdad: `05-implementation-guide/` (operations.md, lifecycle.md,
rules.md, sushi-config.yaml, FSH y ejemplos compilados en
`fsh-generated/resources/`), `04-fhir-proposal.md` y
`04-mapping-table.md`. Todo validado; el paso 6 construye SOLO lo que
la guía dice. Se construye según la GUÍA, no según las filas de la
tabla de mapeo del paso 4 que la guía corrige (`Communication.topic`
es CodeableConcept 0..1, no una referencia; `Task.owner` es 0..1, el
servicio que acepta, y el profesional va como agente de Provenance).

Ejemplo trabajado en todo el componente: María González, 58 años, RUN
sintético 11.111.111-1, CESFAM Los Aromos → cardiología, derivación
REF-2026-0001, sospecha de insuficiencia cardiaca (SNOMED CT
84114007), diagnóstico ICD-10-CM I50.22 + SNOMED CT 417996009.

## Decisiones del plan

- **Stack: Python 3.12, solo stdlib** (`json`, `datetime`, `unittest`).
  `pytest` NO está instalado en este entorno; stdlib evita instalar
  dependencias y que el componente dependa de la red. Tests con
  `unittest`: `PYTHONPATH=src python3 -m unittest discover -s tests -v`
  o `sh run_tests.sh`.
- **Datos sintéticos siempre** (María González, RUN 11.111.111-1,
  MPI-2026-0042). Nada de datos reales en código, ejemplos, tests ni
  README.
- **Goldens**: copias textuales de los JSON compilados por SUSHI en
  `05-implementation-guide/fsh-generated/resources/` (los 31 ejemplos),
  en `06-component/tests/goldens/`. La comparación pasa por
  `tests/golden.py`, que normaliza SOLO lo documentado en las Rulings
  de `state.md`. Nunca se edita el golden para que pase el test.
- **Referencias**: los builders emiten referencias lógicas
  (`Patient/maria-gonzalez`, como los ejemplos compilados). El
  ensamblador de Bundle las deja como están en los Bundles de tipo
  document (la guía: `fullUrl` = `ResourceType/id`); en el Bundle de
  transacción PI-0 usa `urn:uuid:` como los ejemplos compilados.
- **Reloj inyectable**: todo el componente recibe `now` (datetime con
  zona America/Santiago) como parámetro; los tests fijan `now` para
  que los plazos SLA y los `lastModified` sean deterministas.
- **Días hábiles**: lunes a viernes. La guía no define calendario de
  festivos; el componente no modela festivos (Ruling en `state.md`).
- **Plazos a las 17:00**: los plazos SLA vencen a las 17:00 hora local,
  como el ejemplo compilado (`2026-11-26T17:00:00-03:00`).
- **MPI y directorio locales**: OP-9 y OP-10 se implementan contra un
  registro en memoria sembrado con el ejemplo trabajado (sin MPI ni
  directorio reales, la guía define las interacciones FHIR; el
  componente las ejecuta contra el registro local). Sin identidad
  resuelta no se crea la derivación.
- **Re-apertura de cancelación**: el único camino de corrección de un
  `cancelled` es la re-apertura explícita por el operador del hub, al
  estado previo (registrado en el historial Provenance). Implementada
  en `transitions.py` como la única transición saliente de
  `cancelled`.

## Archivos

| Archivo | Responsabilidad |
|---|---|
| `06-component/plan.md` | Este plan (descomposición en tareas) |
| `06-component/README.md` | Cómo correr el componente, tests y ejemplos; tabla de trazabilidad operación→código |
| `06-component/run_tests.sh` | `PYTHONPATH=src python3 -m unittest discover -s tests -v` |
| `06-component/src/derivacion/__init__.py` | Paquete; `__version__ = "0.1.0"` |
| `06-component/src/derivacion/constants.py` | Canonical, sistemas, códigos y ValueSets de la guía; duraciones SLA |
| `06-component/src/derivacion/transitions.py` | Una tabla por máquina (Task, ServiceRequest, Appointment, Encounter, CarePlan); `ForbiddenTransition`; invariantes I1–I6 |
| `06-component/src/derivacion/working_days.py` | Suma de días hábiles (lun–vie) + vencimiento 17:00 |
| `06-component/src/derivacion/evaluator.py` | Reglas SLA R1–R5: evalúa qué escaladas vencen a una fecha dada (nunca cambia estado) |
| `06-component/src/derivacion/builders.py` | Constructores de los 12 perfiles + Provenance + Subscription + Slot/Schedule + ensambladores de Bundle |
| `06-component/src/derivacion/validate.py` | Validación de perfil: campos requeridos, valores fijos, pertenencia a ValueSets locales, invariantes de extensiones |
| `06-component/src/derivacion/registry.py` | Registro en memoria: MPI (OP-9) y directorio de servicios (OP-10) |
| `06-component/src/derivacion/workflow.py` | El agregado de la derivación: aplica OP-1…OP-12 en orden, con validación de transiciones, conteos, plazos y notificaciones |
| `06-component/src/derivacion/cli.py` | CLI: corre los tres escenarios (aceptado, rechazado, no-show) y vuelca los JSON |
| `06-component/tests/golden.py` | Comparador de goldens (normalizaciones documentadas) |
| `06-component/tests/goldens/*.json` | Copias textuales de los 31 ejemplos compilados por SUSHI |
| `06-component/tests/test_*.py` | Un archivo por operación / módulo |
| `06-component/examples/*.json` | Salidas de los tres escenarios (aceptado, rechazado, no-show) |

## Tareas (una operación por tarea; RED-GREEN por tarea)

| Plan task | Tarea | Gate |
|---|---|---|
| 11.1 | Andamiaje: paquete, `constants.py`, `run_tests.sh`, README esqueleto | `run_tests.sh` corre (0 tests, exit 0) |
| 11.2 | `transitions.py`: 5 máquinas + invariantes I1–I6 | `test_transitions.py` verde, incl. transición prohibida por máquina e invariante |
| 11.3 | `working_days.py` + `evaluator.py` (R1–R5) | `test_sla.py` verde: plazos exactos del ejemplo trabajado + escaladas que vencen |
| 11.4 | Builders base + registro local: OP-9 identidad, OP-10 servicio | `test_op09_op10.py` verde + goldens Patient / Rol / Servicio / Endpoint |
| 11.5 | OP-1 crear derivación (ServiceRequest + Task + Bundle transaction) | `test_op01.py` verde + goldens SR / Task / Bundle PI-0 |
| 11.6 | OP-2 triaje + OP-12 notificar + Provenance | `test_op02_op12.py` verde + golden Communication aceptación |
| 11.7 | OP-3 ofrecer / confirmar / reservar (+ Encounter `planned`) | `test_op03.py` verde + goldens Appointment / AppointmentResponse / Encounter |
| 11.8 | OP-4 re-ofertar / re-agendar + conteos por oferta | `test_op04.py` verde: rechazo → Appointment nuevo; conflicto → mismo Appointment nuevo Slot; conteos 0–2 |
| 11.9 | OP-5 asistencia / no-show | `test_op05.py` verde: `arrived` → `fulfilled`; 1er no-show re-agenda; 2º no-show cierra `no-show` |
| 11.10 | OP-6 contrareferencia (Composition + DocumentReference + Condition + CarePlan + Bundle document) | `test_op06.py` verde + goldens Composition / DocumentReference / Condition / CarePlan / Bundle PI-3 |
| 11.11 | OP-7 consulta de estado + OP-8 cancelar (+ re-apertura) | `test_op07_op08.py` verde: solo lectura; cancelación en cualquier punto; re-apertura solo por hub |
| 11.12 | OP-11 suscripción + notificación a suscriptores | `test_op11.py` verde: `criteria` exacto; una notificación por transición |
| 11.13 | Escenarios end-to-end + CLI + ejemplos + README + `validating-interop` | `test_scenarios.py` verde; `examples/*.json` generados; README completo |

## Trazabilidad (se completa en README.md al final)

Cada operación OP-1…OP-12 → módulo → función → test. Cada transición
del ciclo de vida → función → test de transición prohibida. Cada
guarda (plazo SLA, conteo, canal, identidad) → módulo → función →
golden que prueba que bloquea.

## Estado final (2026-11-19)

Plan tasks 11.1–11.13 completas. Suite: 168 tests en verde
(`sh run_tests.sh`). Ejemplos generados: 63 archivos JSON en
`examples/` (accepted, rejected, no-show). `validating-interop`
corrido (`tests/test_validation.py` + `validation-report.md`).
Pendiente: revisión experta independiente (la hace el parent) y
validación del paso 6.
