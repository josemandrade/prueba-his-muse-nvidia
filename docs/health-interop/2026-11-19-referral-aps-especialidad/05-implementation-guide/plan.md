# Plan — Guía de Implementación (paso 5)

Caso: derivación APS → especialidad con contrareferencia. Fuente de verdad:
`04-fhir-proposal.md` y `04-mapping-table.md` (validados 2026-11-19), BPMN
`02-bpmn-model.md` (validado 2026-11-19), entidades `03-entities-data.md`
(validado 2026-11-19). La guía se construye en FSH y se compila con SUSHI
(v3.21.1 en este entorno).

## Decisiones del plan

- La guía es una **guía de prueba** para este caso, no una guía nacional. Su
  `id` es `hl7.fhir.uv.test.derivacion-aps-especialidad`, versión `0.1.0`, y
  su canonical es `https://josemandrade.github.io/prueba-his-muse-nvidia/`
  (el sitio de GitHub Pages del repo de prueba, donde el workflow despliega
  la guía; mismo patrón que el caso DAU). El id usa el reino `uv` porque la
  plantilla `hl7.base.template` solo acepta los reinos `us`, `uv` y `eu` en
  el id, y este no es un trabajo de un grupo HL7: se usa
  `fhir.base.template#1.0.0` (genérica, con Jekyll en CI). Nota: el repo de
  prueba contiene otro caso (screening visual escolar); si ese caso publica
  su propia guía, habrá que decidir una ruta de despliegue propia para ella
  — esta canonical es la raíz del sitio, que hoy ocupa esta guía.
- El canonical de la guía **sustituye** al placeholder de la propuesta
  (`http://derivacion.example.org/fhir/`). No queda `example.org` en la
  guía: todos los CodeSystem, ValueSet, perfiles y extensiones usan el
  canonical `https://josemandrade.github.io/prueba-his-muse-nvidia/` (paso
  4, ítem abierto — cerrado aquí). Los sistemas de identificadores
  sintéticos de los ejemplos (MPI, RUN, APS) usan dominios `example.org`
  solo como sistemas de identificador de ejemplo, no como canonical de la
  guía — es la convención de los ejemplos sintéticos, no un placeholder.
- Los perfiles son **propios** (`Derivacion*`), sobre los recursos base de
  FHIR R4. No se transcribe ningún perfil de otra guía; la base
  `CorePacienteCl` queda como asociación ofrecida, no asumida (la propuesta
  § Asociaciones). La única dependencia es `hl7.fhir.r4.core 4.0.1`.
- Java no está disponible en este entorno, así que el IG Publisher no corre
  en local. La validación local es SUSHI (compila el FSH y valida los
  ejemplos contra sus perfiles). La validación completa con el IG Publisher
  corre en el workflow de Git (Plan task 10.32).
- Los ejemplos son sintéticos (REF-2026-0001, María González, RUN
  11.111.111-1). Nunca datos reales.
- Las tareas se numeran "Plan task 10.N" (el caso usa el recurso FHIR
  `Task`; la numeración continúa la del `state.md` del caso, donde el paso
  5 es la Plan task 10).

## Archivos

| Archivo | Responsabilidad |
|---|---|
| `05-implementation-guide/sushi-config.yaml` | Identidad, versión, dependencias, páginas |
| `05-implementation-guide/ig.ini` | Entrada del IG Publisher / Auto-IG Builder |
| `05-implementation-guide/input/fsh/valuesets.fsh` | CodeSystems y ValueSets locales |
| `05-implementation-guide/input/fsh/extensions.fsh` | Extensiones (SLA, conteos, resto) |
| `05-implementation-guide/input/fsh/patient.fsh` | Perfil DerivacionPaciente |
| `05-implementation-guide/input/fsh/servicerequest.fsh` | Perfil DerivacionSolicitud |
| `05-implementation-guide/input/fsh/task.fsh` | Perfil DerivacionTarea (centro) |
| `05-implementation-guide/input/fsh/appointment.fsh` | Perfil DerivacionCita |
| `05-implementation-guide/input/fsh/encounter.fsh` | Perfil DerivacionEncuentro |
| `05-implementation-guide/input/fsh/composition.fsh` | Perfil DerivacionContrareferencia |
| `05-implementation-guide/input/fsh/documentreference.fsh` | Perfil DerivacionDocumento |
| `05-implementation-guide/input/fsh/condition.fsh` | Perfil DerivacionDiagnostico |
| `05-implementation-guide/input/fsh/careplan.fsh` | Perfil DerivacionPlanSeguimiento |
| `05-implementation-guide/input/fsh/communication.fsh` | Perfil DerivacionNotificacion |
| `05-implementation-guide/input/fsh/practitionerrole.fsh` | Perfil DerivacionRol |
| `05-implementation-guide/input/fsh/healthcareservice.fsh` | Perfil DerivacionServicio |
| `05-implementation-guide/input/fsh/examples.fsh` | Ejemplos sintéticos (instancias) |
| `05-implementation-guide/input/pagecontent/index.md` | Caso de uso, usuarios, roles, puntos |
| `05-implementation-guide/input/pagecontent/process.md` | Proceso (BPMN) |
| `05-implementation-guide/input/pagecontent/resources.md` | Diagrama de recursos |
| `05-implementation-guide/input/pagecontent/profiles.md` | Perfiles involucrados |
| `05-implementation-guide/input/pagecontent/terminology.md` | Terminología |
| `05-implementation-guide/input/pagecontent/operations.md` | Operaciones en cada punto |
| `05-implementation-guide/input/pagecontent/sequences.md` | Diagramas de secuencia |
| `05-implementation-guide/input/pagecontent/mapping.md` | Mapeo de datos a recursos |
| `05-implementation-guide/input/pagecontent/ihe.md` | Relación con IHE |
| `05-implementation-guide/input/pagecontent/lifecycle.md` | Ciclo de vida de cada recurso |
| `05-implementation-guide/input/pagecontent/rules.md` | Reglas de evaluación, retención |
| `05-implementation-guide/input/pagecontent/public-health.md` | Base legal, reporte agregado |
| `05-implementation-guide/input/includes/menu.xml` | Menú horizontal (navbar) |
| `04-sequence-<flow>.svg` (+ `.png` en `input/images/`) | Diagramas de secuencia |
| `.github/workflows/ig-build.yml` | Workflow de Git (raíz del repo) |

### Plan task 10.1: Andamiaje de la guía

**Files:**
- Create: `05-implementation-guide/sushi-config.yaml`, `05-implementation-guide/ig.ini`, `05-implementation-guide/input/pagecontent/index.md`, `05-implementation-guide/input/includes/menu.xml`
- Test: `sushi .` compila sin errores

**Interfaces:**
- Consumes: la propuesta validada (`04-fhir-proposal.md`), el caso de uso (`01-use-case-spec.md`)
- Produces: la carpeta de la guía con su identidad (id `hl7.fhir.uv.test.derivacion-aps-especialidad`, versión `0.1.0`, FHIR R4 4.0.1, dependencia solo `hl7.fhir.r4.core`, canonical `https://josemandrade.github.io/prueba-his-muse-nvidia/`)

- [ ] **Step 1: Write the failing test** — `sushi .` en la carpeta vacía: FAIL, no hay `sushi-config.yaml`
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code** — config + ig.ini + index.md + menu.xml
- [ ] **Step 4: Run SUSHI and the tests to verify they pass** — SUSHI compila sin errores
- [ ] **Step 5: Update `state.md` with `Plan task 10.1: complete`**

### Plan task 10.2: ValueSets y CodeSystems locales

**Files:**
- Create: `05-implementation-guide/input/fsh/valuesets.fsh`
- Test: `sushi .` compila; los ValueSets contienen los códigos del caso

**Interfaces:**
- Consumes: la tabla de mapeo (`04-mapping-table.md` §3, §8, §9, §11), la propuesta (terminología)
- Produces: `DerivacionEstadoReferenciaCS`/`VS` (9 estados), `DerivacionRolCS`/`VS` (6 roles), `DerivacionMotivoRechazoCS`/`VS`, `DerivacionCanalCS`/`VS`, `DerivacionEspecialidadCS`/`VS` (cardiología + resto del catálogo local), `DerivacionTaskCodeCS`/`VS` (`referral-workflow`)

- [ ] **Step 1: Write the failing test** — `sushi .`: FAIL, el ValueSet `DerivacionEstadoReferencia` no existe
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass** — SUSHI compila; cada ValueSet contiene sus códigos
- [ ] **Step 5: Update `state.md` with `Plan task 10.2: complete`**

### Plan task 10.3: Extensiones

**Files:**
- Create: `05-implementation-guide/input/fsh/extensions.fsh`
- Test: `sushi .` compila; las extensiones existen con su `url` y su `value[x]`

**Interfaces:**
- Consumes: la tabla de mapeo (§3 Task: SLA + conteos; §1, §5, §7, §10, §11)
- Produces: `DerivacionSlaAcceptanceDeadline`, `DerivacionSlaOfferDeadline`, `DerivacionSlaCounterreferralDeadline`, `DerivacionSlaRetriageDeadline`, `DerivacionSlaConfirmationDeadline` (dateTime, en Task), `DerivacionOfferDeclineCount`, `DerivacionOfferChaseCount`, `DerivacionReschedulingCount` (integer, en Task), `DerivacionOfferNumber` (integer, en Appointment), `DerivacionReferralIdentifier` (Identifier, en Composition), `DerivacionPreferredContactChannel` (code, en Patient), `DerivacionDeliveryOutcome` (code, en Communication), `DerivacionMatchBasis` + `DerivacionMatchConfidence` (en Patient del MPI)

- [ ] **Step 1: Write the failing test** — `sushi .`: FAIL, la extensión `sla-acceptance-deadline` no existe
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass** — SUSHI compila; cada extensión tiene su contexto y su `value[x]`
- [ ] **Step 5: Update `state.md` with `Plan task 10.3: complete`**

### Plan task 10.4: Perfil DerivacionPaciente

**Files:**
- Create: `05-implementation-guide/input/fsh/patient.fsh`
- Test: `sushi .` compila; el ejemplo de paciente valida contra el perfil

**Interfaces:**
- Consumes: propuesta (perfil `DerivacionPaciente`: `identifier` 1..*, `telecom` 1..*, `name` 1..1, `birthDate` 1..1); mapeo §1
- Produces: `DerivacionPaciente` (Patient, id `derivacion-paciente`)

- [ ] **Step 1: Write the failing test** — el ejemplo `maria-gonzalez` no valida (el perfil no existe)
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.4: complete`**

### Plan task 10.5: Perfil DerivacionSolicitud

**Files:**
- Create: `05-implementation-guide/input/fsh/servicerequest.fsh`
- Test: `sushi .` compila; el ejemplo de solicitud valida contra el perfil

**Interfaces:**
- Consumes: propuesta (`intent = order` fijo, `subject` 1..1, `code` 1..1, `reasonCode` 1..*, `priority` 1..1, `requester` 1..1, `authoredOn` 1..1); mapeo §2
- Produces: `DerivacionSolicitud` (ServiceRequest, id `derivacion-solicitud`)

- [ ] **Step 1: Write the failing test** — el ejemplo `ref-2026-0001` no valida (el perfil no existe)
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.5: complete`**

### Plan task 10.6: Perfil DerivacionTarea (centro)

**Files:**
- Create: `05-implementation-guide/input/fsh/task.fsh`
- Test: `sushi .` compila; el ejemplo de Task valida; golden antes/después `requested` → `received` y test de transición prohibida (`requested` → `scheduled`)

**Interfaces:**
- Consumes: propuesta (Task: `focus` 1..1 → ServiceRequest, `for` 1..1 → Patient, `intent = order` fijo, `businessStatus` 1..1, `statusReason` 0..1, extensiones SLA + conteos); mapeo §3; tabla de ciclo de vida del Task
- Produces: `DerivacionTarea` (Task, id `derivacion-tarea`) — el centro del grafo

- [ ] **Step 1: Write the failing test** — el ejemplo `tarea-ref-2026-0001` no valida (el perfil no existe)
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass** — SUSHI compila; el golden `requested` → `received` pasa; la transición prohibida `requested` → `scheduled` se rechaza
- [ ] **Step 5: Update `state.md` with `Plan task 10.6: complete`**

### Plan task 10.7: Perfil DerivacionCita

**Files:**
- Create: `05-implementation-guide/input/fsh/appointment.fsh`
- Test: `sushi .` compila; el ejemplo de cita valida contra el perfil

**Interfaces:**
- Consumes: propuesta (`basedOn` 1..* → ServiceRequest, `slot` 0..* → Slot, `participant` 1..*, `patientInstruction` 0..1); mapeo §5 (cadena `proposed` → `pending` → `booked` → `arrived` → `fulfilled`)
- Produces: `DerivacionCita` (Appointment, id `derivacion-cita`)

- [ ] **Step 1: Write the failing test** — el ejemplo de cita no valida (el perfil no existe)
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.7: complete`**

### Plan task 10.8: Perfil DerivacionEncuentro

**Files:**
- Create: `05-implementation-guide/input/fsh/encounter.fsh`
- Test: `sushi .` compila; el ejemplo de encuentro valida contra el perfil

**Interfaces:**
- Consumes: propuesta (`class = AMB` fijo, `subject` 1..1, `basedOn` 1..* → ServiceRequest, `appointment` 0..1, `serviceType` 1..1); mapeo §6 (`planned` → `in-progress` → `finished`; no hay Encounter en no-show)
- Produces: `DerivacionEncuentro` (Encounter, id `derivacion-encuentro`)

- [ ] **Step 1: Write the failing test** — el ejemplo de encuentro no valida (el perfil no existe)
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.8: complete`**

### Plan task 10.9: Perfil DerivacionContrareferencia

**Files:**
- Create: `05-implementation-guide/input/fsh/composition.fsh`
- Test: `sushi .` compila; el ejemplo de contrareferencia valida contra el perfil

**Interfaces:**
- Consumes: propuesta (`status = final` fijo al enviar, `type` = LOINC 11488-4, `subject` 1..1, `author` 1..1, secciones Diagnosis / Plan / Follow-up indications / Follow-up plan for APS); mapeo §7
- Produces: `DerivacionContrareferencia` (Composition, id `derivacion-contrareferencia`)

- [ ] **Step 1: Write the failing test** — el ejemplo de contrareferencia no valida (el perfil no existe)
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.9: complete`**

### Plan task 10.10: Perfil DerivacionDocumento

**Files:**
- Create: `05-implementation-guide/input/fsh/documentreference.fsh`
- Test: `sushi .` compila; el ejemplo de documento valida contra el perfil

**Interfaces:**
- Consumes: propuesta (`status = current` fijo al enviar, `type` = LOINC 11488-4, `subject` 1..1, `content.attachment.url` → Composition, `context.related` → ServiceRequest); mapeo §7
- Produces: `DerivacionDocumento` (DocumentReference, id `derivacion-documento`)

- [ ] **Step 1: Write the failing test** — el ejemplo de documento no valida (el perfil no existe)
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.10: complete`**

### Plan task 10.11: Perfil DerivacionDiagnostico

**Files:**
- Create: `05-implementation-guide/input/fsh/condition.fsh`
- Test: `sushi .` compila; el ejemplo de diagnóstico valida contra el perfil

**Interfaces:**
- Consumes: propuesta (`code` 1..1 ICD-10-CM I50.22 + SNOMED CT 417996009, `subject` 1..1, `encounter` 1..1, `clinicalStatus = active`, `verificationStatus = confirmed`); mapeo §7
- Produces: `DerivacionDiagnostico` (Condition, id `derivacion-diagnostico`)

- [ ] **Step 1: Write the failing test** — el ejemplo de diagnóstico no valida (el perfil no existe)
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.11: complete`**

### Plan task 10.12: Perfil DerivacionPlanSeguimiento

**Files:**
- Create: `05-implementation-guide/input/fsh/careplan.fsh`
- Test: `sushi .` compila; el ejemplo de plan valida contra el perfil

**Interfaces:**
- Consumes: propuesta (`status = active`, `intent = plan` fijo, `subject` 1..1, `addresses` 1..* → Condition, `activity.reference` → ServiceRequest / Appointment / Task); mapeo §7
- Produces: `DerivacionPlanSeguimiento` (CarePlan, id `derivacion-plan-seguimiento`)

- [ ] **Step 1: Write the failing test** — el ejemplo de plan no valida (el perfil no existe)
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.12: complete`**

### Plan task 10.13: Perfil DerivacionNotificacion

**Files:**
- Create: `05-implementation-guide/input/fsh/communication.fsh`
- Test: `sushi .` compila; el ejemplo de notificación valida contra el perfil

**Interfaces:**
- Consumes: propuesta (`status = completed` fijo, `basedOn` 1..* → Task, `sender` 1..1, `recipient` 1..*, `sent` 1..1, `medium` 1..* lista local); mapeo §11 (emisores nombrados C5/Q3)
- Produces: `DerivacionNotificacion` (Communication, id `derivacion-notificacion`)

- [ ] **Step 1: Write the failing test** — el ejemplo de notificación no valida (el perfil no existe)
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.13: complete`**

### Plan task 10.14: Perfil DerivacionRol

**Files:**
- Create: `05-implementation-guide/input/fsh/practitionerrole.fsh`
- Test: `sushi .` compila; el ejemplo de rol valida contra el perfil

**Interfaces:**
- Consumes: propuesta (`practitioner` 1..1, `organization` 1..1, `code` 1..* ValueSet `DerivacionRol`, seis roles); mapeo §8
- Produces: `DerivacionRol` (PractitionerRole, id `derivacion-rol`)

- [ ] **Step 1: Write the failing test** — el ejemplo de rol no valida (el perfil no existe)
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.14: complete`**

### Plan task 10.15: Perfil DerivacionServicio

**Files:**
- Create: `05-implementation-guide/input/fsh/healthcareservice.fsh`
- Test: `sushi .` compila; el ejemplo de servicio valida contra el perfil

**Interfaces:**
- Consumes: propuesta (`providedBy` 1..1 → Organization, `type` 1..1 catálogo local, `active` 1..1, `endpoint` 0..* → Endpoint); mapeo §9 (mCSD ITI-90)
- Produces: `DerivacionServicio` (HealthcareService, id `derivacion-servicio`)

- [ ] **Step 1: Write the failing test** — el ejemplo de servicio no valida (el perfil no existe)
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.15: complete`**

### Plan task 10.16: Ejemplos sintéticos

**Files:**
- Create: `05-implementation-guide/input/fsh/examples.fsh`
- Test: `sushi .` compila; cada ejemplo valida contra su perfil (el informe de validación queda junto a la guía)

**Interfaces:**
- Consumes: los 12 perfiles (Plan tasks 10.4–10.15), el ejemplo trabajado (María González, 58, RUN 11.111.111-1, CESFAM Los Aromos → cardiología, sospecha de insuficiencia cardiaca)
- Produces: un ejemplo por perfil + Bundle de transacción PI-0 (ServiceRequest + Task) + Bundle de documento PI-3 (Composition primera entrada + DocumentReference + Condition + CarePlan)

- [ ] **Step 1: Write the failing test** — `sushi .`: FAIL, los ejemplos no existen
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass** — SUSHI compila; cada ejemplo valida contra su perfil
- [ ] **Step 5: Update `state.md` with `Plan task 10.16: complete`**

### Plan task 10.17: Página de operaciones

**Files:**
- Create: `05-implementation-guide/input/pagecontent/operations.md`
- Test: `sushi .` compila; cada operación enlaza a su ejemplo generado y a su perfil IHE (o dice que la guía la posee)

**Interfaces:**
- Consumes: propuesta (OP-1…OP-12 con su PI, entradas/salidas y perfil IHE), los ejemplos (Plan task 10.16)
- Produces: `operations.md` — las 12 operaciones, cada una con interacción FHIR, entradas, salidas, ejemplo y perfil IHE (PI-4: "none applies" explícito)

- [ ] **Step 1: Write the failing test** — la página `operations.html` no existe en la salida
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.17: complete`**

### Plan task 10.18: Página de mapeo

**Files:**
- Create: `05-implementation-guide/input/pagecontent/mapping.md`
- Test: `sushi .` compila; cada entidad de la tabla de mapeo enlaza a su perfil

**Interfaces:**
- Consumes: `04-mapping-table.md` (13 entidades, campo a campo)
- Produces: `mapping.md` — entidades → recursos, con la regla de transformación y qué pasa si falta el dato

- [ ] **Step 1: Write the failing test** — la página `mapping.html` no existe en la salida
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.18: complete`**

### Plan task 10.19: Página de terminología

**Files:**
- Create: `05-implementation-guide/input/pagecontent/terminology.md`
- Test: `sushi .` compila; cada CodeSystem/ValueSet local enlaza a su página generada

**Interfaces:**
- Consumes: propuesta (terminología: LOINC 11524-6 / 33762-6 / 57133-1 / 11488-4 / 34099-2, SNOMED CT 84114007 / 417996009, ICD-10-CM I50.22, UCUM, servidor `https://tx.hl7chile.cl/r4`), `valuesets.fsh`
- Produces: `terminology.md` — CodeSystems y ValueSets locales con sus códigos y enlaces, más las terminologías externas con sus URLs canónicas

- [ ] **Step 1: Write the failing test** — la página `terminology.html` no existe en la salida
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.19: complete`**

### Plan task 10.20: Página de relación con IHE

**Files:**
- Create: `05-implementation-guide/input/pagecontent/ihe.md`
- Test: `sushi .` compila; cada perfil IHE citado enlaza a profiles.ihe.net

**Interfaces:**
- Consumes: propuesta (revisión IHE por punto: full 3 / partial 13 filas / none 1 — PI-4 explícito; asociaciones ofrecidas; G1–G7)
- Produces: `ihe.md` — fit por punto con actores, transacciones, huecos y riesgos; las asociaciones ofrecidas (no asumidas)

- [ ] **Step 1: Write the failing test** — la página `ihe.html` no existe en la salida
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.20: complete`**

### Plan task 10.21: Página de ciclo de vida

**Files:**
- Create: `05-implementation-guide/input/pagecontent/lifecycle.md`
- Test: `sushi .` compila; cada tabla de ciclo de vida nombra su operación + PI

**Interfaces:**
- Consumes: propuesta (tablas de ciclo de vida de Task, ServiceRequest, Appointment, Encounter, CarePlan)
- Produces: `lifecycle.md` — una tabla por (recurso, máquina): operación que dispara (con PI), transiciones prohibidas; invariantes entre máquinas con su test de transición prohibida

- [ ] **Step 1: Write the failing test** — la página `lifecycle.html` no existe en la salida
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.21: complete`**

### Plan task 10.22: Páginas de reglas y de salud pública

**Files:**
- Create: `05-implementation-guide/input/pagecontent/rules.md`, `05-implementation-guide/input/pagecontent/public-health.md`
- Test: `sushi .` compila; ambas páginas existen en la salida

**Interfaces:**
- Consumes: spec §5 (retención), spec §4 (base legal Q7), `03-entities-data.md` (calidad de datos), propuesta (G2, G6, G7)
- Produces: `rules.md` — reglas de evaluación (SLA como reglas con ventana, acción y re-arme), indicadores, plan de monitoreo, retención (una vez, por clase de producto); `public-health.md` — base legal por PI, reporte desidentificado, indicadores agregados. Sin página de medicamentos controlados: el caso no tiene medicamentos (se registra en `decisions.md`).

- [ ] **Step 1: Write the failing test** — las páginas `rules.html` / `public-health.html` no existen en la salida
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.22: complete`**

### Plan task 10.23: Páginas de proceso y de recursos

**Files:**
- Create: `05-implementation-guide/input/pagecontent/process.md`, `05-implementation-guide/input/pagecontent/resources.md`
- Test: `sushi .` compila; las páginas referencian los PNG por nombre de archivo; `check_bpmn.py --check` 0/0

**Interfaces:**
- Consumes: BPMN (3 partes, validadas), `04-fhir-proposal-graph.svg` (Task centro), los PNG re-renderizados en `input/images/`
- Produces: `process.md` (BPMN, versión y fecha de validación) y `resources.md` (grafo, centro Task y por qué), cada una con su PNG a ancho nativo, contenedor con scroll y controles de zoom

- [ ] **Step 1: Write the failing test** — las páginas `process.html` / `resources.html` no existen en la salida
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code** — re-renderizar los PNG desde la fuente, mirar cada PNG, escribir las páginas
- [ ] **Step 4: Run SUSHI and the tests to verify they pass** — `check_bpmn.py --check` 0 diagonales / 0 cruces; SUSHI compila
- [ ] **Step 5: Update `state.md` with `Plan task 10.23: complete`**

### Plan task 10.24: Diagrama de secuencia — solicitud

**Files:**
- Create: `04-sequence-request.svg` (+ PNG en `input/images/`), sección en `04-sequence-diagrams.md`
- Test: `python3 render_sequence.py --check` — cada mensaje nombra una operación; OP-1, OP-9, OP-10, OP-11 aparecen

**Interfaces:**
- Consumes: BPMN Parte A (creación, identidad, enrutado), propuesta (OP-1, OP-9, OP-10, OP-11)
- Produces: el diagrama de solicitud (APS → hub → especialidad; identidad PIXm/PDQm y directorio mCSD como sub-pasos; suscripción OP-11 como `opt`)

- [ ] **Step 1: Write the failing test** — `render_sequence.py --check`: FAIL, OP-1 sin diagrama
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code** — el diagrama en `render_sequence.py`, renderizar el PNG y MIRARLO
- [ ] **Step 4: Run SUSHI and the tests to verify they pass** — `--check` pasa para estas operaciones; el PNG es legible
- [ ] **Step 5: Update `state.md` with `Plan task 10.24: complete`**

### Plan task 10.25: Diagrama de secuencia — triaje

**Files:**
- Create: `04-sequence-triage.svg` (+ PNG en `input/images/`), sección en `04-sequence-diagrams.md`
- Test: `python3 render_sequence.py --check` — OP-2 y OP-12 aparecen

**Interfaces:**
- Consumes: BPMN Parte A (aceptar/rechazar, re-triaje), propuesta (OP-2, OP-12)
- Produces: el diagrama de triaje (`alt` aceptar vs rechazar, con el motivo; la decisión llega a APS y al paciente — el aviso al paciente es mensaje no-FHIR, canal telefónico/presencial)

- [ ] **Step 1: Write the failing test** — `render_sequence.py --check`: FAIL, OP-2 sin diagrama
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code** — el diagrama, renderizar el PNG y MIRARLO
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.25: complete`**

### Plan task 10.26: Diagrama de secuencia — agendamiento

**Files:**
- Create: `04-sequence-schedule.svg` (+ PNG en `input/images/`), sección en `04-sequence-diagrams.md`
- Test: `python3 render_sequence.py --check` — OP-3 y OP-4 aparecen

**Interfaces:**
- Consumes: BPMN Parte B (oferta, confirmación, persecución, re-oferta, reserva), propuesta (OP-3, OP-4)
- Produces: el diagrama de agendamiento (`loop` sobre los intentos de re-agendamiento; la oferta al paciente es mensaje no-FHIR; Scheduling ITI-115/117 para la mitad de reserva)

- [ ] **Step 1: Write the failing test** — `render_sequence.py --check`: FAIL, OP-3 sin diagrama
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code** — el diagrama, renderizar el PNG y MIRARLO
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.26: complete`**

### Plan task 10.27: Diagrama de secuencia — asistencia

**Files:**
- Create: `04-sequence-attend.svg` (+ PNG en `input/images/`), sección en `04-sequence-diagrams.md`
- Test: `python3 render_sequence.py --check` — OP-5 aparece

**Interfaces:**
- Consumes: BPMN Parte B (asistencia, no-show, re-agendamiento), propuesta (OP-5)
- Produces: el diagrama de asistencia (`alt` asistir vs no-show; el segundo no-show cierra la derivación)

- [ ] **Step 1: Write the failing test** — `render_sequence.py --check`: FAIL, OP-5 sin diagrama
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code** — el diagrama, renderizar el PNG y MIRARLO
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.27: complete`**

### Plan task 10.28: Diagrama de secuencia — retorno del resultado

**Files:**
- Create: `04-sequence-result-return.svg` (+ PNG en `input/images/`), sección en `04-sequence-diagrams.md`
- Test: `python3 render_sequence.py --check` — OP-6 y OP-12 aparecen

**Interfaces:**
- Consumes: BPMN Parte B (encuentro, contrareferencia, acuse de recibo), propuesta (OP-6, OP-12)
- Produces: el diagrama de retorno (documento MHD ITI-65, acuse de APS; la contrareferral llega en otra sesión — diagrama propio, enlazado por el id de la derivación)

- [ ] **Step 1: Write the failing test** — `render_sequence.py --check`: FAIL, OP-6 sin diagrama
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code** — el diagrama, renderizar el PNG y MIRARLO
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.28: complete`**

### Plan task 10.29: Diagrama de secuencia — consulta de estado

**Files:**
- Create: `04-sequence-status-query.svg` (+ PNG en `input/images/`), sección en `04-sequence-diagrams.md`
- Test: `python3 render_sequence.py --check` — OP-7 aparece; PI-4 es "none applies" explícito

**Interfaces:**
- Consumes: BPMN Parte C (consulta de solo lectura), propuesta (OP-7)
- Produces: el diagrama de consulta de estado (búsqueda FHIR simple sobre el Task; sin perfil IHE)

- [ ] **Step 1: Write the failing test** — `render_sequence.py --check`: FAIL, OP-7 sin diagrama
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code** — el diagrama, renderizar el PNG y MIRARLO
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.29: complete`**

### Plan task 10.30: Diagrama de secuencia — cancelación

**Files:**
- Create: `04-sequence-cancellation.svg` (+ PNG en `input/images/`), sección en `04-sequence-diagrams.md`
- Test: `python3 render_sequence.py --check` — OP-8 aparece; 0 mensajes sin operación, 0 operaciones sin diagrama

**Interfaces:**
- Consumes: BPMN Partes A y B (fila de cancelación), propuesta (OP-8, PCC-58 con su tope de dirección)
- Produces: el diagrama de cancelación (cualquier parte pide cancelar; el hub registra y avisa a todas las partes; la cita reservada se cancela)

- [ ] **Step 1: Write the failing test** — `render_sequence.py --check`: FAIL, OP-8 sin diagrama
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code** — el diagrama, renderizar el PNG y MIRARLO
- [ ] **Step 4: Run SUSHI and the tests to verify they pass** — `--check` OK: 0 mensajes sin operación, 0 operaciones sin diagrama
- [ ] **Step 5: Update `state.md` with `Plan task 10.30: complete`**

### Plan task 10.31: Página de diagramas de secuencia

**Files:**
- Create: `05-implementation-guide/input/pagecontent/sequences.md`
- Test: `sushi .` compila; cada diagrama enlaza su PNG por nombre de archivo; los conteos mecánicos quedan en `validation.md`

**Interfaces:**
- Consumes: los 7 diagramas (Plan tasks 10.24–10.30), `04-sequence-diagrams.md`
- Produces: `sequences.md` — una sección por flujo (flujo, camino BPMN, diagrama, tabla mensaje → operación → perfil IHE → resultado esperado), con su entrada de menú propia

- [ ] **Step 1: Write the failing test** — la página `sequences.html` no existe en la salida
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code**
- [ ] **Step 4: Run SUSHI and the tests to verify they pass**
- [ ] **Step 5: Update `state.md` with `Plan task 10.31: complete`**

### Plan task 10.32: CI/CD de la guía (workflow de Git)

**Files:**
- Create: `.github/workflows/ig-build.yml` (raíz del repo, no dentro de `05-implementation-guide/`)
- Test: el workflow en sí — un push que construye en verde y un push con un FSH roto que construye en rojo y no despliega

**Interfaces:**
- Consumes: la carpeta de la guía (`05-implementation-guide/` con `sushi-config.yaml` e `ig.ini`), los perfiles y ejemplos validados
- Produces: un workflow que valida la guía en cada push/PR y la despliega desde `main`; el registro en el Auto-IG Builder queda N/A (la guía vive en una subcarpeta de un repo de prueba, no en la raíz — el builder no puede construirla desde ahí)

- [ ] **Step 1: Write the workflow file**
- [ ] **Step 2: Push it to a branch and open a pull request — the workflow must run and pass** — lo hace el padre (requiere push; fuera de esta tarea)
- [ ] **Step 3: Break one FSH file on purpose and push — the workflow must fail and not deploy** — lo hace el padre (requiere push; fuera de esta tarea)
- [ ] **Step 4: Revert the break, merge to `main`, and confirm the deploy** — lo hace el padre (requiere push; fuera de esta tarea)
- [ ] **Step 5: Update `state.md` with `Plan task 10.32: complete`**

### Plan task 10.33: Cierre — SUSHI final, informe de validación, enlaces

**Files:**
- Create: `05-implementation-guide/validation-report.md` (informe de validación de los ejemplos)
- Test: `sushi .` 0 errores y 0 advertencias que cambien el significado; cada enlace interno de las páginas existe en `fsh-generated/resources/`

**Interfaces:**
- Consumes: toda la guía (Plan tasks 10.1–10.32)
- Produces: la guía completa y validada, lista para la revisión experta y la validación del usuario

- [ ] **Step 1: Write the failing test** — `sushi .` con advertencias sin revisar: FAIL
- [ ] **Step 2: Run the test to verify it fails**
- [ ] **Step 3: Write the minimal FSH and code** — corregir cada advertencia que cambie el significado; verificar cada enlace interno
- [ ] **Step 4: Run SUSHI and the tests to verify they pass** — SUSHI 0/0; informe de validación junto a la guía
- [ ] **Step 5: Update `state.md` with `Plan task 10.33: complete`**
