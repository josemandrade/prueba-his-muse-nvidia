# Informe de validación — componente de derivación (paso 6)

Fecha: 2026-11-19. Guía: `05-implementation-guide/` (SUSHI 0 errores /
0 advertencias, 74 recursos). Componente: `06-component/`, Python 3.12
solo stdlib. Datos sintéticos en todo (María González, RUN 11.111.111-1).

## Qué se validó y con qué

| Qué | Herramienta / perfil | Resultado |
|---|---|---|
| 31 ejemplos compilados por SUSHI como goldens | `tests/golden.py` (comparación por valor) | **20/31 comparados por valor, 23 aserciones, todos coinciden**: ServiceRequest, Task, Bundle PI-0, Appointment, AppointmentResponse, Encounter, Schedule, Location, Communication, Composition, DocumentReference, Condition, CarePlan, Bundle PI-3, Patient, Practitioner, PractitionerRole (rol-medico-aps), HealthcareService, Endpoint, Organization (org-cesfam-los-aromos). Las 11 instancias no comparadas se listan en «Goldens no comparados» más abajo — la afirmación anterior «31/31» era incorrecta (C2, revisión experta del paso 6) |
| Máquinas de estado (Task, ServiceRequest, Appointment, Encounter, CarePlan) | `tests/test_transitions.py` (41 tests) | Cada transición legal pasa; cada ilegal lanza `ForbiddenTransition` (409), incluidos los guardados (`accepted → rejected` solo por fallo de agendamiento; `scheduled → no-show` solo en el segundo no-show; `rejected → cancelled` solo antes de la decisión de re-triaje) |
| SLA R1–R5 | `tests/test_sla.py` (26 tests) | Todos los plazos, escalaciones y el retorno R3 verificados contra `working_days.py` (lunes a viernes, 17:00) |
| Invariantes I1–I6 entre máquinas | `Referral.check_invariants()` en los 3 escenarios | 0 violaciones en los 3 escenarios (`summary.json`) |
| Cada `Coding` lleva `system`, `code` y `display` | `tests/test_validation.py` | Pasa sobre ejemplos + goldens (las Quantity UCUM quedan fuera: no son Coding; las definiciones de la guía quedan fuera: restringen códigos sin display) |
| Cada `Reference` resuelve al tipo esperado | `tests/test_validation.py` | Pasa: recursos del escenario + registro sembrado + goldens + externos conocidos del lado APS (encuentro APS, ECG y NT-proBNP, referenciados sin materializar) |
| Bundle de documento con la Composition primera | `tests/test_validation.py` | Pasa (OP-6) |
| Datos sintéticos (privacy checklist) | `tests/test_validation.py` | Pasa: único RUN `11.111.111-1`; sin `@`, sin teléfonos |
| Suite completa | `sh run_tests.sh` | **168 tests, todos en verde** |
| Escenarios end-to-end | `tests/test_scenarios.py` + CLI | aceptado → `counter-referred`; rechazado → `rejected`; no-show → `no-show`; 63 archivos JSON en `examples/` (59 recursos + 3 `summary.json`) |

## Lo que NO se validó aquí

- **El validador FHIR / IG Publisher no corrió sobre los ejemplos
  del componente**: no hay Java en este entorno (la misma limitación
  que en el paso 5; la validación completa corre en CI,
  `ig-build.yml`, aún no ejecutado). Los ejemplos del componente que
  coinciden con los goldens de SUSHI heredan la validación de la
  guía; los recursos que el componente construye y la guía no
  ejemplifica (Slot re-agendado, segundas ofertas, Provenance de
  re-apertura, Subscription) solo tienen la validación estructural
  de este informe (codings, referencias, transiciones).
- **Terminología en vivo**: los códigos (LOINC 11488-4, SNOMED CT
  84114007 / 417996009, ICD-10-CM I50.22) se verificaron en vivo en
  el paso 4; el componente los toma de `constants.py`, no los
  re-verifica.

## Goldens no comparados (11 de 31)

Corrección C2 (revisión experta del paso 6): de los 31 archivos de
instancia en `tests/goldens/`, 20 se comparan por valor (23
aserciones `assert_golden`). Los 11 restantes no se comparan:

- **Externos del lado APS, referenciados sin materializar (3)**:
  `Encounter-aps-encounter-2026-11-19`,
  `Observation-ecg-2026-11-19`, `Observation-ntprobnp-2026-11-19`.
  El componente los referencia (Bundle PI-0 `supportingInfo`) pero no
  los construye; pertenecen al HIS de APS.
- **Directorio / roles referenciados por id, nunca construidos por el
  flujo (7)**: `Organization-org-cardiologia`,
  `Organization-org-hub`, `Practitioner-especialista-cardiologia`,
  `PractitionerRole-rol-admin-aps`, `PractitionerRole-rol-agendador`,
  `PractitionerRole-rol-especialista`, `PractitionerRole-rol-triaje`.
  El flujo usa estos ids (destinatarios de notificaciones, actor de
  triaje, servicio aceptante) pero no materializa los recursos; el
  registro sembrado solo guarda el id de la organización. Los
  equivalentes de APS (`Organization-org-cesfam-los-aromos`,
  `Practitioner-medico-aps`, `PractitionerRole-rol-medico-aps`) sí se
  comparan como fixtures de OP-9/OP-10.
- **Divergencia deliberada y documentada (1)**:
  `Slot-slot-cardiologia-1`. El golden de la guía tiene el Slot en
  `busy` con el Appointment en `proposed`; el componente lo deja en
  `free` en la oferta y lo pasa a `busy` solo al reservar (texto de
  OP-3: el Slot se ocupa al reservar, no al ofertar). Es un ruling
  del componente (state.md 11.7 / README), no un error: el
  comportamiento NO se cambió, solo se registra aquí la divergencia.

## Fallos encontrados durante la validación (todos corregidos)

1. El Task de creación no llevaba el plazo de aceptación: `_recompute_deadlines`
   corría con `case_state` en `None` y la regla de nulidad lo borraba. Corregido:
   el estado se fija antes de recalcular.
2. El Bundle PI-0 llevaba id `bundle-ref-2026-0001` en vez de
   `bundle-pi0-ref-2026-0001`. Corregido.
3. Los Slots re-agendados no se volcaban en `examples/`: la referencia
   `Slot/slot-cardiologia-2` no resolvía. Corregido: `all_resources`
   incluye los Slots.
4. El conteo de re-agendamiento medía no-shows en vez de
   re-agendamientos (el primer no-show cerraba el Task). Corregido:
   el conteo se incrementa al re-agendar; el segundo no-show cierra.

## Correcciones de la revisión experta del paso 6 (C1–C6)

Revisión independiente NOT APPROVED (0 critical/high, 3 medium +
3 low); todas corregidas, suite en 168 tests en verde:

- **C1 (medium)**: R5 no se evaluaba tras el retorno por fallo de
  agendamiento — `evaluate_escalations` no recibía
  `retriage_return_at` y `_evaluator_state` no lo pasaba. Corregido:
  el disparador viaja en ambos; 3 tests nuevos (evaluador + segundo
  rechazo + vía R3).
- **C2 (medium)**: la afirmación «31/31 goldens» era falsa: 23
  aserciones comparan 20/31 instancias por valor. Corregido: cifra
  real en este informe y las 11 no comparadas listadas con su motivo
  en «Goldens no comparados» (sin cambiar el comportamiento del Slot).
- **C3 (medium)**: Communications con destinatario Organization
  violaban `DerivacionNotificacion` (solo Patient y DerivacionRol).
  Corregido: cada escalada va al responsable de la acción pendiente
  (R1 → clínico de triaje, R2 → agendador, R4 → especialista,
  cancelación → agendador); el operador del hub es ahora un
  PractitionerRole (`rol-operador-hub`, código `hub-operator` del
  DerivacionRolCS, sembrado en el registro) como emisor, destinatario
  del acuse y agente de la re-apertura. `build_communication`
  rechaza Organization como destinatario. Añadido el chequeo de
  targetProfile a `test_validation.py` (lee los
  StructureDefinitions generados por SUSHI), que caza esta clase de
  defecto sin Java. Ejemplos regenerados (63 JSON).
- **C4 (low)**: la suscripción exportada llevaba claves internas
  (`_active`, `notifications`). Corregido: `all_resources` vuelca
  una copia sin ellas; test nuevo en `test_op11.py`.
- **C5 (low)**: `decide_retriage` no dejaba Provenance. Corregido:
  la decisión de APS queda auditada (actor `aps-doctor`); el
  escenario rechazado pasa de 2 a 3 entradas de historial.
- **C6 (low)**: README decía «156 tests» con 161 en la suite.
  Corregido: 168 tests, con los conteos por archivo de la tabla de
  trazabilidad actualizados.

## Rulings del componente

En `../state.md` (Plan tasks 11.1–11.13) y resumidos en `README.md`.
