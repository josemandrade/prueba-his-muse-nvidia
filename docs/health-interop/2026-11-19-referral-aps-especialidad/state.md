# State — referral-aps-especialidad

- Last updated: 2026-11-20 09:37 America/Santiago
- Current step: ALL 6 STEPS VALIDATED 2026-11-19 (parent as
  validating user) and PUSHED 2026-11-20 (steps 5–6: bc9d1f41,
  9ee58258; README fix pushed 44d35cc9). Step 5 re-touch: guide
  canonical moved from the site root to the
  `derivacion-aps-especialidad` subpath (user decision 2026-11-20:
  one workflow per guide, with subpaths); SUSHI rebuilt 0/0,
  committed locally (8e54b49). Expert re-review of the re-touch:
  NOT APPROVED — 1 high (H1: the step 6 component still stamped
  the root canonical) + 1 medium (M1: README artefacts bullet).
- Current task: H1+M1 fixes applied 2026-11-20 (1b53d61, 119 files),
  focused re-check APPROVED 2026-11-20 ~09:35 (0 critical/high).
  Guide folder README added with the published URL at the top
  (user: the URL was missing from the guide's README). Next: push
  the rebuilt guide + component + guide README.
- Last completed: step 6 VALIDATED 2026-11-19 by the parent as
  validating user (expert review NOT APPROVED first, 3 medium + 3
  low C1–C6 fixed; focused re-check APPROVED, 0 critical/high/
  medium, 0 new findings) and committed locally (597a318, 170
  files). ALL 6 STEPS DONE. README fix (Published guide URL at
  top, next-step current) committed locally 2026-11-20 (ef1281b)
  and pushed (44d35cc9). Canonical re-touch committed locally
  2026-11-20 (8e54b49, 70 files), pending expert re-review + push.
  H1+M1 fixes committed locally 2026-11-20 (1b53d61, 119 files),
  pending focused re-check + push.
  Previous: step 5 VALIDATED 2026-11-19
  by the parent as validating user (expert review NOT APPROVED
  first, 2 medium + 7 low C1–C9 fixed; focused re-check APPROVED,
  0 new findings); committed locally (970530a).
- Recovery note (2026-11-19 10:36): the previous coordinator errored out
  mid-task (output token cap) after claiming Plan task 5 (IHE landscape
  scan, "12 profiles verified live") COMPLETE and "written into
  02-bpmn-model.md". That is NOT TRUE ON DISK: no 02-bpmn-model.md exists
  anywhere for this case (verified by the parent with a filesystem
  search). The scan results survive ONLY as the summary below. Plan task 5
  is reset to REDO. The renderer and checker it created DO exist and are
  reusable: render_bpmn.py and check_bpmn.py in the clone root (created
  10:28). No .bpmn files exist yet for this case. Also reconciling: the
  summary says "12 profiles" but lists 14 names (mCSD, Scheduling, MHD,
  360X, XBeR-WD, XDW, PIXm, PDQm, QEDm, DSUBm, ATNA, CT, XDS.b, BPPC) —
  recount during the redo; the list is a CHECKLIST to re-verify live, not
  established fact.
- Next action: local commit of step 6 (06-component/ + the four
  bookkeeping files only; never blind `git add -A`; do NOT include
  the school folder's pre-existing state.md edit). Then notify the
  user: all 6 steps finished. Pushes of steps 2–6 remain pending —
  step 2's retry card expired; the user re-approves when ready.
- Open questions: 3 in `03-entities-data.md` (§ Open questions) —
  LOINC codes for the worked example's exams, the local
  specialty/service catalogue + rejection-reason list, and the
  notification channel list — all deferred to step 4, no parent
  decision needed now.
- Blockers: none. Step 2 push PENDING (approval card expired ~30
  min; parent retries it with the user). STEP 1 PUSH SUCCEEDED 2026-11-19 11:01 (parent, after the
  user added the repo to the GitHub App installation — diagnosis confirmed):
  commit 155ffa026777a87dc1968f0153a99b7ef08ff41c, 6 files (root README.md +
  the 5 step 1 files), verified in remote (root README + spec download).
  Sync record created (first entry) at
  ~/workspace/harness-test-opencode/prueba-his-muse-nvidia.muse-github-snapshot-sync.json.
  Note: the state.md pushed in that commit still said BLOCKED (it was the
  disk content at push time); the correction rides with the next push.
- Resume by / next review date: none
- Waiting for: focused re-check of the step 5 expert-review fixes
  C1–C9 (parent spawns it) + parent validation as validating user
- Files changed in this task: 05-implementation-guide/plan.md,
  sushi-config.yaml, ig.ini, input/pagecontent/index.md,
  input/includes/menu.xml, input/pagecontent/{operations,mapping,
  terminology,ihe,lifecycle,rules,public-health,process,resources,
  sequences}.md, input/fsh/*.fsh, input/images/ (BPMN + grafo +
  secuencia PNG/SVG), render_sequence.py, 04-sequence-*.svg,
  .github/workflows/ig-build.yml, 05-implementation-guide/
  validation-report.md, README.md, decisions.md, validation.md,
  state.md (Plan task 10 complete, step 5 draft, uncommitted)
- Do not redo: step 1 spec draft; review fixes C1–C12; Q1–Q7 decisions; re-check
  fixes N1–N5; step 1 validation; local commit 6831859; scan redo (14
  profiles); step 2 BPMN draft (three parts, CHECK OK, PNGs inspected);
  step 2 expert-review fixes C1–C14 (m12, h19/h20, g32 reroute, g14
  reroute, renames, renderer fixes, scan wording; CHECK OK 0/0, PNGs
  re-looked); step 2 validation + local commit ed773d5

Tasks:
- Plan task 1: complete (step 1 spec drafted)
- Plan task 2: complete (review fixes C1–C12 applied to the spec text; Q1–Q7 recorded)
- Plan task 3: complete (re-check fixes N1–N5 applied to the spec text; decisions and validation recorded)
- Plan task 4: complete (step 1 committed 6831859; push SUCCEEDED 2026-11-19 11:01 after the App-installation fix, commit 155ffa02, verified in remote; sync record created)
- Plan task 5: complete (REDO — scan re-verified live, 14 profiles,
  written into 02-bpmn-model.md; recount reconciled: 14, not 12)
- Plan task 6: complete (VALIDATED 2026-11-19 by the parent as validating
  user) — step 2 BPMN three-part split model (Part A 52/43, Part B 65/59,
  Part C 16/11), mechanical check 0/0, PNGs inspected; expert review
  NOT APPROVED first (C1–C14), fixes applied, focused re-check APPROVED,
  polish N1/N2 applied
- Plan task 7: complete (expert-review fixes C1–C14) — C1 m12 rejection
  notice to patient + doctor notification named; C2 h19/h20 escalation
  flows to new APS admin task; C3 g32 rerouted to `Offer appointment`
  (same confirm/chase loop, counts reset per offer); C4 return end
  events point at Part A re-triage outcomes + rejected closure; C5
  patient-death cancellation recorded in the model doc; C6 duration
  labels ("5 working days (2 if urgent)", "3 working days") + urgency
  note; C7 "First re-scheduling?"; C8 h6/h7 deviation recorded; C9
  requester named + non-termination caveat recorded; C10 full
  working-days wording (supersedes the shorthand decision); C11 Part C
  wording aligned to spec §3.7; C12 end-event rename; C13 renderer
  fixes (opaque backing, own-shape nudge guard, extended nudges,
  canvas expansion) + g14 reroute to y=860 + g21 one-line label, all
  three PNGs re-rendered and re-looked; C14 ITI-118 / ITI-106 /
  360X Rev. 1.2 confirmed from the PDF. Mechanical check 0/0 on all
  three parts (A 52/43, B 65/59, C 16/11); STOPPED for the parent's
  focused re-check + step 2 validation; do NOT commit until validated.
  Re-check polish (2026-11-19 11:27): N1 cancellation task relabelled
  "Record cancellation (incl. patient death); notify all parties" in
  Parts A and B (grep: "patient death" now 1× in each .bpmn) + note in
  the modeling notes; N2 receipt-branch convention recorded in the
  modeling notes (t_pat_create, t_pat_notice2, t_admin_notify_offer,
  t_admin_esc — no end events added). Rebuilt, mechanical check CHECK
  OK 0/0 on all three parts, PNGs re-rendered at 2× and re-looked
  (cancellation label legible, no clipping/overlap). STOPPED for the
  parent's step 2 validation. Step 2 VALIDATED 2026-11-19 by the parent
  as validating user; committed locally (ed773d5). Step 2 push PENDING
  (approval card expired; parent retries it with the user).
- Plan task 8: complete (VALIDATED 2026-11-19 by the parent as validating
  user) — step 3 entities draft written 2026-11-19 12:02
  (`03-entities-data.md`, 13 entities); expert review NOT APPROVED
  (5 medium C1–C5 + 5 low C6–C10); all 10 fixes applied 2026-11-19
  12:06; focused re-check APPROVED; polish N1/N2 applied, N3 recorded
  as a spec widening for the next spec touch (spec NOT edited)
  for the parent's focused re-check + step 3 validation. Do NOT
  commit until validated. Do NOT push in this run.
  Re-check polish (2026-11-19 12:12): N1 §5 `cancelled` row
  (scheduler on decline; offer or booked appointment), N2 §3/§2
  `rejected` rows (hub operator records the scheduling-failure
  return) applied and re-read; N3 recorded in decisions.md as a
  noted spec widening (spec NOT edited). STOPPED for the parent's
  step 3 validation. Do NOT commit until validated. Do NOT push
  in this run.
  Step 3 VALIDATED 2026-11-19 by the parent as validating user;
  committed locally (e856f2a).
- Plan task 9: complete (VALIDATED 2026-11-19 by the parent as
  validating user; committed locally 018f114) — step 4 FHIR
  proposal + mapping table + IHE review per point) — `04-fhir-proposal.md`
  (440 lines: resource choices + rejected alternatives, 12 own
  profiles with base canonical URLs, lifecycle tables for Task /
  ServiceRequest / Appointment / Encounter / CarePlan, terminology
  table, 12 proposed operations OP-1…OP-12, IHE review per PI,
  gaps G1–G7, associations offered, 2 short synthetic JSON
  examples), `04-mapping-table.md` (550 lines, all 13 entities),
  `04-fhir-proposal-graph.svg` (12 nodes, Task centre; geometry
  verified mechanically 0 node-interior hits + 2 right-angle
  crossings, PNG rendered at 1.5× and inspected — 2 routing defects
  found by the check and fixed by re-routing; `content` label
  shortened to fit the 100 px gap; `→` replaced by `->` for the
  render font), README.md / decisions.md / validation.md /
  state.md updated. Expert review NOT APPROVED (4 medium C1–C4 +
  6 low C5–C10); all 10 fixes applied 2026-11-19 12:35 (ICD-10-CM
  I50.22 pinned, WHO ICD-10 note; OP-3 creates the Encounter at
  booking, OP-5 PATCHes it; ServiceRequest `revoked` on
  rejected-closure, mapping row split; graph `appointment` edge
  reversed and SVG re-rendered + visually re-checked; QEDm option
  "Diagnostic Reports"; fit summary reconciled to partial 13;
  PCC-58 row added with the direction cap; `businessStatus` 1..1
  in both files; Task `completed` pinned to the Encounter reaching
  `finished`; example.org placeholder note in the Examples
  section). Appointment status chain left as written (reviewer
  confirmed offered → `proposed`, confirmed → `pending`, booked
  → `booked` is correct R4). Focused re-check APPROVED 2026-11-19
  12:38 (all 10 fixes confirmed in the text; 1 new low N1,
  cosmetic stray "— +" in the mapping-table Diagnosis row, applied
  by the parent). Step 4 VALIDATED 2026-11-19 by the parent as
  validating user. Next: step 5 (Implementation Guide with SUSHI).

- Plan task 10.1: complete (step 5 scaffolding: sushi-config.yaml
  (id hl7.fhir.uv.test.derivacion-aps-especialidad, canonical
  https://josemandrade.github.io/prueba-his-muse-nvidia/), ig.ini,
  index.md, menu.xml; 11 stub pages created for the SUSHI build;
  SUSHI v3.21.1 compiles 0 errors / 0 warnings)
- Plan tasks 10.2–10.3: complete (valuesets.fsh: 6 CodeSystems +
  6 ValueSets; extensions.fsh: 14 extensions; SUSHI 0/0)
- Plan tasks 10.4–10.15: complete (12 perfiles Derivacion* en
  FSH; 3 errores de SUSHI corregidos: Communication.topic es
  CodeableConcept 0..1 (no una referencia a Task) y Task.owner es
  0..1 (no 0..*) — ver decisions.md; ValueSet DerivacionRol
  renombrado a DerivacionRolVS por colisión de nombre con el perfil
  DerivacionRol; SUSHI final 0 errores / 0 advertencias, 26
  StructureDefinitions + 6 CodeSystems + 6 ValueSets)
- Plan task 10.16: complete (ejemplos sintéticos: 31 instancias —
  un ejemplo por perfil + Bundle de transacción PI-0 + Bundle de
  documento PI-3 + recursos base de apoyo; 1 error corregido:
  CarePlan.activity.detail es un BackboneElement y su texto es
  detail.description, no detail.text; SUSHI 0 errores / 0
  advertencias, 70 recursos generados)
- Plan tasks 10.17–10.22: complete (páginas operations, mapping,
  terminology, ihe, lifecycle, rules + public-health; sin página de
  medicamentos controlados — el caso no tiene medicamentos)
- Plan task 10.23: complete (páginas process + resources; PNGs BPMN
  re-verificados: check_bpmn.py CHECK OK 0/0 en las tres partes;
  PNGs mirados a 2× — legibles, etiquetas con fondo opaco; grafo
  re-renderizado a 2× e inspeccionado, arista appointment con la
  dirección correcta tras C4)
- Plan tasks 10.24–10.30: complete (7 diagramas de secuencia con
  render_sequence.py adaptado del DAU: request, triage, schedule,
  attend, result-return, status-query, cancellation; check 0/0 —
  39 mensajes, 0 sin operación, 0 operaciones sin diagrama; PNGs
  mirados a 2×; 2 defectos corregidos: pestañas dibujadas después
  de las barras de activación, etiqueta OP-6 acortada)
- Plan task 10.31: complete (página sequences.md: 7 diagramas +
  tablas mensaje → operación → IHE → resultado esperado + cobertura
  OP-1…OP-12)
- Plan task 10.32: complete (workflow CI .github/workflows/ig-build.yml
  en la raíz del repo; sus pasos de prueba — push en verde, FSH roto
  en rojo sin desplegar — los hace el padre, requieren push)
- Plan task 10.33: complete (SUSHI final 0/0; informe
  05-implementation-guide/validation-report.md; enlaces internos 0
  problemas; canonical real verificado, sin example.org en ninguna
  URL canónica)
- Plan task 10.34: complete (expert-review fixes C1–C9 del paso 5:
  discriminador de slicing `title` en Composition; `owner` = servicio
  en OP-2 (operations.md + sequences.md); `DerivacionRolVS` en
  profiles.md; C8 en public-health.md; validation-report con el
  resultado real de SUSHI y el barrido example.org completo; 2
  ValueSets nuevos + invariantes de rango (C6); short de status
  corregido (C7); píldora `[la paciente rechaza]` a inset 16 (C8);
  mitigación G6 en CI (C9). SUSHI re-run 0/0, 8 VS / 8 CS, 74
  recursos; sequence check CHECK OK. Focused re-check APPROVED
  2026-11-19 13:18 (all 9 fixes confirmed in the text and generated
  JSON; 0 new findings). Step 5 VALIDATED 2026-11-19 by the parent
  as validating user. Next: step 6 (component building).

- Plan task 11.1: complete (andamiaje paso 6: `06-component/plan.md`,
  paquete `derivacion` (`__version__ = "0.1.0"`), `constants.py` con
  canonical / perfiles / ValueSets locales / códigos / plazos SLA /
  emisores nombrados C5/Q3, `run_tests.sh`; `run_tests.sh` corre)
- Plan task 11.2: complete (`transitions.py`: 5 máquinas — Task
  (estado del caso), ServiceRequest, Appointment, Encounter,
  CarePlan — + `ForbiddenTransition` (409) + re-apertura solo por
  hub-operator + invariantes I1/I4/I6; `test_transitions.py` 39 tests
  en verde, incl. transición prohibida por máquina)
- Plan task 11.2 Ruling: los días hábiles son lunes a viernes; la
  guía no define calendario de festivos, así que el componente no
  modela festivos. Los plazos SLA vencen a las 17:00 hora local, como
  el ejemplo compilado (`2026-11-26T17:00:00-03:00`).
- Plan task 11.2 Ruling: la escalada por timeout (R1) se dispara una
  vez por plazo incumplido y no se re-arma: la decisión desarma la
  regla y la escalada queda registrada; el operador del hub revisa
  las escaladas cada día hábil (plan de monitoreo de la guía).

- Plan task 11.3: complete (`working_days.py`: días hábiles lun–vie,
  vencimiento 17:00; `evaluator.py`: reglas R1–R5 — devuelve
  escaladas, nunca cambia el estado; `test_sla.py` 25 tests en
  verde, incl. el plazo de aceptación del ejemplo compilado
  2026-11-26T17:00:00-03:00 y R3 persecución → re-triaje tras la
  segunda persecución)

- Plan task 11.4: complete (`registry.py`: MPI local + directorio
  local sembrados con el ejemplo trabajado; `builders.py` base:
  Patient / Practitioner / PractitionerRole / HealthcareService /
  Endpoint / Organization; `tests/golden.py` comparador; 31
  goldens copiados de `fsh-generated/resources/`; `test_op09_op10.py`
  16 tests en verde, incl. goldens Patient / Rol / Servicio /
  Endpoint / Organization y el bloqueo sin identidad resuelta)
- Plan task 11.4 Ruling: el ejemplo compilado ordena los
  identificadores del Patient RUN primero y MPI después; el builder
  emite ese mismo orden para que el golden coincida.

- Plan task 11.5: complete (OP-1: `build_service_request`,
  `build_task`, `build_transaction_bundle`; `test_op01.py` 8 tests
  en verde + goldens ServiceRequest / Task / Bundle PI-0; el Bundle
  normaliza los fullUrl `urn:uuid:` frescos — Ruling documentada en
  `tests/test_op01.py`)

- Plan task 11.6: complete (OP-2/OP-12: `build_communication`,
  `build_provenance`; `test_op02_op12.py` 6 tests en verde + golden
  Communication de aceptación; `Task.owner` es el servicio que
  acepta y el profesional va como agente de Provenance — corrección
  R4 del paso 5; `Communication.topic` es el nombre codificado de
  la transición, no una referencia)

- Plan task 11.7: complete (OP-3: `build_appointment`,
  `build_appointment_response`, `build_encounter`, `build_slot`,
  `build_schedule`, `build_location`; `test_op03.py` 7 tests en
  verde + goldens Appointment / AppointmentResponse / Encounter /
  Schedule / Location)
- Plan task 11.7 Ruling: el ejemplo compilado muestra el Slot
  `busy` con el Appointment en `proposed`; la guía (OP-3) dice que
  el Slot pasa a `busy` en la reserva, no en la oferta. El componente
  sigue el texto de OP-3: libre en la oferta, ocupado en la reserva,
  libre en no-show/cancelación. El golden del Slot no se compara
  tal cual; se prueban las reglas del Slot.
- Plan task 11.8 Ruling: el retorno por fallo de agendamiento mueve
  el Task `accepted` → `rejected` (con el plazo de re-triaje desde
  el retorno y `retriage_decided = false`). Lo exige el paso 3
  validado (C4: "durante un re-triaje por fallo de agendamiento la
  derivación está en estado `rejected`") y la tabla de mapeo §2
  (`rejected` en espera de re-triaje → `active`), pero la tabla de
  ciclo de vida del paso 4 / paso 5 no lista `accepted` → `rejected`.
  El componente la implementa como transición guardada (solo por
  retorno de fallo de agendamiento, OP-4 / R3) en `transitions.py`;
  queda señalada para la revisión experta del paso 6.

- Plan task 11.8: complete (OP-4 + motor `workflow.py`: `Referral`
  con OP-1 crear/enrutar, OP-2 triaje/re-triaje, OP-3
  ofrecer/confirmar/reservar, OP-4 re-oferta/re-agendamiento por
  conflicto, `apply_sla_actions` R1–R5; `test_op04.py` 12 tests en
  verde; suite total 114 tests)
- Plan task 11.8 Ruling: el conteo de decline pertenece al CICLO de
  oferta, no a cada Appointment: no se reinicia en la re-oferta
  tras un rechazo (si no, el gateway "First decline?" del BPMN
  nunca vería el segundo rechazo); se reinicia solo cuando empieza
  un ciclo nuevo tras un no-show (N5). El de chase sí se reinicia
  en cada oferta. El texto de la extensión
  (`offer-decline-count`, "Se reinicia por oferta") se lee como
  "por ciclo de oferta".
- Plan task 11.8 Ruling: los diagramas de secuencia del paso 5
  registran Communication en la reserva (diagrama 3, fila 10: Hub
  → APS admin) y en cada persecución (diagrama 3, fila 5), aunque
  la tabla de emisores nombrados no los listara. El componente
  añade los triggers `booked` (hub → APS admin, system-message) y
  `chase` (scheduler → paciente, phone) a `NOTIFICATION_SENDERS`.
  El reenvío del rechazo al agendador NO es Communication (diagrama
  3, fila 12: OP-4 sin registro; la AppointmentResponse es la señal).
- Plan task 11.8 Ruling: R3 NO se marca como disparada en
  `escalations_fired` tras una persecución: la persecución se sigue
  por el conteo de chase; si no, la segunda persecución y el
  retorno nunca se evaluarían. Las escalaciones R1/R2/R4/R5 sí
  disparan una sola vez por plazo. El hub notifica como
  Organization `org-hub` (no hay PractitionerRole de operador del
  hub en los ejemplos de la guía).

- Plan task 11.9: complete (OP-5: `record_arrival`,
  `finish_encounter`, `record_no_show`, `reschedule_after_no_show`,
  `check_invariants`; `test_op05.py` 7 tests en verde; suite total
  122 tests). Transición guardada `scheduled` → `no-show` solo en
  el segundo no-show (`transitions.py` + test).
- Plan task 11.9 Ruling: en un no-show el Encounter `planned` de
  la cita perdida queda como está y se conserva en `encounters`
  como historia: la guía no define un estado `cancelled` de
  encuentro para el no-show (mapeo §6: "no hay estado `cancelled`
  de encuentro"), y la invariante I4 lo admite (solo prohíbe
  `in-progress`/`finished` con un Appointment `noshow`). Queda
  señalada para la revisión experta. En el re-agendamiento la
  reserva crea un Encounter NUEVO (id derivado del Appointment).
- Plan task 11.9 Ruling: el conteo de re-agendamiento mide
  re-agendamientos (0–1), no no-shows: el primer no-show deja el
  Task en `scheduled` (conteo 0); el re-agendamiento lo lleva a 1;
  el segundo no-show cierra el Task. La re-reserva tras un no-show
  no registra transición del Task (ya está en `scheduled`).

- Plan task 11.10: complete (OP-6: `build_condition`,
  `build_care_plan`, `build_composition`, `build_document_reference`,
  `build_document_bundle` + `send_counter_referral` /
  `acknowledge_counter_referral`; `test_op06.py` 9 tests en verde,
  incl. el Bundle de documento completo contra el golden; suite
  total 131 tests)
- Plan task 11.10 Ruling: el Task pasa a `counter-referred` con el
  acuse de recibo de APS, no con el envío (sequences.md diagrama 5,
  fila 4; operations.md OP-6). El envío deja el Task en `completed`,
  desarma R4 y bloquea la cancelación (OP-8: "solo antes de que se
  envíe la contrareferencia"). El acuse es una Communication con
  `payload.contentReference` → DocumentReference (trigger nuevo
  `counter-referral-receipt`, aps-admin → hub, desde el diagrama 5).

- Plan task 11.11: complete (OP-7 `query_status` — estado actual,
  último cambio, próximo paso, solo lectura — y OP-8 `cancel` /
  `reopen`; `test_op07_op08.py` 12 tests en verde; suite total 143
  tests)
- Plan task 11.11 Ruling: la re-apertura restaura el Task y el
  ServiceRequest (`active`), pero NO la cita cancelada: el
  agendador debe re-ofertar. La guía no dice qué pasa con la cita
  al re-abrir; restaurar la reserva sin re-ofertar inventaría una
  cita que la paciente no confirmó. Queda señalada para la revisión
  experta. La cancelación exige motivo; `rejected` con la decisión
  de re-triaje tomada no se puede cancelar (N1, `ForbiddenTransition`).

- Plan task 11.12: complete (OP-11: `build_subscription` +
  `subscribe` / `unsubscribe`; `test_op11.py` 5 tests en verde;
  suite total 148 tests). Sin golden de Subscription en la guía:
  el builder sigue el texto de OP-11 tal cual (`criteria`,
  rest-hook, payload FHIR JSON).

- Plan task 11.13: complete (escenarios end-to-end `scenarios.py`
  + CLI `cli.py` + `examples/` (3 escenarios, 56 archivos JSON) +
  `README.md` completo con trazabilidad + `validating-interop`
  (`tests/test_validation.py` 5 tests + `validation-report.md`);
  suite total 161 tests en verde)
- Plan task 11.13 Ruling: los conteos en cero no viajan como
  extensiones del Task (el ejemplo de la guía no los lleva); solo
  aparecen cuando son > 0. El id del Bundle PI-0 es
  `bundle-pi0-<sr>` (la guía). `Referral.create` toma por defecto
  el detalle completo del ejemplo trabajado (encuentro APS,
  supportingInfo ECG/NT-proBNP, nota, reasonDisplay).
- Plan task 11.13 (validating-interop): 4 defectos encontrados y
  corregidos durante la validación (ver `validation-report.md`):
  plazo de aceptación perdido en la creación, id del Bundle PI-0,
  Slots no volcados en los ejemplos, conteo de re-agendamiento que
  medía no-shows. El validador FHIR / IG Publisher NO corrió sobre
  los ejemplos del componente (no hay Java aquí; corre en CI).
