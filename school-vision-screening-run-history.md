# Historial de la corrida — Screening visual escolar (harness OpenCode + NVIDIA)

Caso completo de 6 pasos construido por un agente en OpenCode con el pack
health-interop-superpowers, del 19 al 21 de noviembre de 2026. Este documento
es el historial detallado de la corrida: qué hizo el agente en cada paso,
qué encontró cada revisión, qué se corrigió, y dónde quedó cada cosa
(commit local, push al repo, validación). Las fuentes son la carpeta del caso
(`docs/health-interop/2026-11-19-school-vision-screening/`:
`state.md`, `validation.md`, `decisions.md`), el RUNLOG del harness
(`run-2026-11-19-step2/RUNLOG.md`), los logs de la sesión
(`run-2026-11-19-pty/logs/`) y el registro de sincronización del repo.

## Contexto de la corrida

- **Caso:** screening de agudeza visual en escolares (enfermera escolar, niño,
  padre/madre, oftalmólogo, equipo de atención primaria). Datos sintéticos.
- **Harness:** OpenCode 1.19.6, modelo NVIDIA Nemotron 3 Ultra
  (`nvidia/nemotron-3-ultra-550b-a55b`, `reasoning_effort` low), provider
  `nvidia` vía `custom.nvidia` (key propia en Secure Vault, nunca en archivos).
- **Sesión:** `ses_e0c7e1330ffernEGEiqv2Az0E4` (misma sesión para los 6 pasos),
  directorio almacenado `run-2026-11-19-pty`.
- **Pack:** health-interop-superpowers v0.39.0 al inicio de la corrida.
- **Repo:** https://github.com/josemandrade/prueba-his-muse-nvidia (público, de
  pruebas), carpeta del caso
  `docs/health-interop/2026-11-19-school-vision-screening/`.
- **Reglas de la corrida:** el agente valida cada paso, hace un commit local
  por paso validado y NO sube nada (los pushes los hace el asistente); no toca
  la carpeta de derivación ni el pack; no crea subagentes. El asistente
  responde las preguntas de validación como validador (delegación del usuario)
  y verifica cada commit en disco antes de darlo por validado.
- **Entorno:** `opencode run` se cuelga sin TTY en este sandbox (se envuelve en
  `script -qec`); opencode no persiste entre reinicios de la VM (reinstalar
  con `npm install -g opencode-ai@1.19.6` tras cada reinicio); los mensajes al
  agente se envían con `send_message.py` (argv, sin shell — los lanzadores
  `.sh` corrompen backticks, `$vars` y comillas dobles).

## Fase 1 — Prueba de aceptación del harness (2026-11-19, 08:12–08:18)

Criterio: en una sesión limpia, decir "tengo un caso clínico que necesita
interoperabilidad" debe disparar `brainstorming-health`. **APROBADO**: el
plugin cargó las 19 skills (18 del pack + la built-in `customize-opencode`) y
la primera acción sustantiva del agente fue cargar `brainstorming-health`, en
13 segundos. Evidencia: `run-2026-11-19-pty/logs/phase1-acceptance.json`.
Intentos previos fallidos: Kimi K3.1 Pro (~172 s por llamada, demasiado lento)
y `opencode run` sin TTY (se colgaba antes del primer turno).

## Paso 1 — Especificación del caso clínico (2026-11-19)

- El agente redactó `01-use-case-spec.md` (5 archivos) con brainstorming:
  screening Snellen a 6 m, umbral de derivación ≤6/12 en un ojo o ≥2 líneas
  de diferencia, consentimiento opt-out anual, sin mandato legal.
- **Revisión experta:** 6 hallazgos (2 High, 2 Medium, 2 Low): niño ausente
  sin re-screening, padre que rechaza la derivación, sin plazo de retorno de
  oftalmología, screening incompleto, archivo de la carta, aviso al docente.
  El agente paró con preguntas Q1–Q5; el usuario las respondió él mismo.
- **Validación del usuario:** 2026-11-19. Dos correcciones menores aplicadas
  (fecha del escenario DNA 2026-01-10 → 2027-01-10; `state.md` con ruta y
  rama del repo).
- **Commit local:** `8353c04` (2026-11-19 08:18, 5 archivos).
- **Push:** `6bd282c4` (5 archivos, verificado en remoto).

## Paso 2 — IHE landscape scan + BPMN (2026-11-19, 21:50–22:33)

- 21:50 — reanudación de la sesión (`resume.sh`, salida `logs/step2.json`).
- El agente hizo el scan IHE (360X candidato principal, MHD, DSUBm, PIXm,
  PDQm, PMIR, Scheduling, EC-Summary/GEE, DCP/DCTM; IPS/sIPS, BPPC/APPC/PCF,
  mADX, EHDI, SDC descartados) y el modelo BPMN (33 tareas, 10 gateways,
  4 eventos, 54 flujos de secuencia, 12 flujos de mensaje).
- **Revisión experta:** 9 hallazgos (3 High, 3 Medium, 3 Low): la cancelación
  del original al re-emitir, el bucle infinito de ausente, el contador de
  incompleto, el rechazo de derivación (PCC-56), la decisión del padre en
  derivación directa, el split paralelo implícito, el carril del docente, la
  fuente del opt-out, el fin de año escolar.
- El agente paró con Q1–Q5. 22:25 — el usuario delegó las respuestas en el
  asistente ("Responderlas tú"): Q1 cancelar el original con PCC-58 Close
  antes de re-emitir; Q2 tras la 2ª ausencia también avisar a Atención
  Primaria; Q3 sin opt-in separado (el opt-out de inicio de año cubre la
  derivación); Q4 el rechazo PCC-56 como ruta separada; Q5 fin de año: los
  pendientes se registran como missed y se avisa al padre Y a Atención
  Primaria.
- 22:30 — un reinicio del entorno interrumpió el turno de respuestas a mitad
  (el agente ya había aplicado las correcciones en disco, pero sin validar ni
  commitear). Reanudación de recuperación; 22:33 el agente verificó los 9
  hallazgos en disco, corrió el chequeo mecánico (XML bien formado) y validó.
- **Commit local:** `73ac7cb` (2026-11-19 22:33, 5 archivos).
- **Push:** `f3e7622c` (2 archivos, verificado en remoto ~22:40).
- **Validación del usuario:** 2026-11-19 (vía el asistente, por delegación).

## Paso 3 — Entidades y datos (2026-11-19, 22:33–22:44)

- Continuó en la misma sesión. El agente redactó `03-entities-data.md`
  (13 entidades).
- **Revisión experta:** 10 hallazgos (3 High, 3 Medium, 4 Low): falta
  `attemptNumber`/`isReScreen` en ScreeningEvent, falta `replacesReferralId`
  en Referral, cierre de derivación, `schoolYear`/`gradeAtScreening`,
  tipos de documento en PrimaryCareRecord, opt-out modificable a mitad de
  año, `supersedesNoticeId`, ServiceLead, ID nacional no asumible, panel de
  agudeza con `hasMember`.
- El agente paró con Q1–Q7; el asistente respondió como validador (misma
  delegación): Q1 sí a `attemptNumber` + `isReScreen`; Q2 sí a
  `replacesReferralId`; Q3 sí a `documentType` + `sourceReferralId`;
  Q4 el padre SÍ puede cambiar el opt-out a mitad de año (`statusHistory`);
  Q5 NO asumir ID nacional de salud (matching demográfico primario);
  Q6 sí a `supersedesNoticeId`; Q7 nueva entidad **ServiceLead**.
  C3 (el cierre vive en Referral) y C10 (panel con dos Observations miembro)
  aceptados como propuestos.
- **Commit local:** `c78acb0` (2026-11-19 22:44, 4 archivos, 309 inserciones).
- **Push:** `e15eee30` (1 archivo, verificado en remoto ~23:11).
- **Validación del usuario:** 2026-11-19 (vía el asistente, por delegación).

## Paso 4 — Propuesta FHIR + mapping + revisión IHE + diagramas de secuencia (2026-11-19, 22:44–23:20)

- Continuó en la misma sesión. El agente validó y commiteó `bc68493`
  (6 archivos, 1.694 inserciones) ~23:11: 12 perfiles propios, Task como
  centro, revisión IHE por punto, 7 diagramas de secuencia (mermaid).
- **Revisión experta (en sesión):** 13 hallazgos (3 Critical, 3 High,
  4 Medium, 3 Low), entre ellos la agudeza Snellen como `valueRatio`
  (no `valueQuantity`), los valores de `Task.status` contra R4 y el
  formato MHD para los documentos.
- **Spot-check del asistente (antes de darlo por validado): encontró 2
  defectos + 1 bajo**, aunque el agente ya lo había dado por validado:
  - **C-A:** la lista de `TaskStatus` incluía `unknown` — no existe en R4
    (verificado en vivo: 12 códigos exactos; `unknown` sí existe en
    `RequestStatus`, que quedó intacto).
  - **C-B:** la tabla de mapping seguía diciendo `valueQuantity` para la
    agudeza por ojo, contradiciendo la corrección C1 (`valueRatio`).
  - **C-C (bajo):** los diagramas son solo mermaid; la convención del pack
    es SVG vía `render_sequence.py` (mermaid-cli no instalaba por puppeteer;
    el agente creó `render_sequence.py` en la raíz del clon y documentó la
    desviación en `decisions.md`).
- Las correcciones se enviaron en la misma sesión; el agente las aplicó y el
  commit se enmendó a **`fe256de`** (2026-11-19 23:20, 8 archivos).
  Nota: la tarjeta de aprobación de esa corrida caducó sin respuesta
  (02:15–02:26 UTC) — el trabajo estaba completo y verificado en disco, pero
  formalmente sin aprobar.
- **Push:** `c5830244` (8 archivos, 2026-11-20 ~08:38, verificado en remoto).
- **Validación del usuario:** 2026-11-19 (vía el asistente, por delegación).

## Paso 5 — Guía de implementación con SUSHI (2026-11-20–21)

El paso más accidentado de la corrida. Tres intentos.

### Intento 1: el bucle (2026-11-20, 08:40–10:14)

- 08:40 — inicio del paso 5 (`resume-step5.sh`, salida `logs/step5.json`).
- 08:58 — el agente sobrescribió `.github/workflows/ig-build.yml` con un
  workflow inventado por él (con `cache: 'npm'`, que falla sin lock file;
  ese archivo pertenece también a la guía de derivación).
- El agente entró en bucle: ~35 ejecuciones de `sushi build` entre las
  08:58 y las 10:14; errores 126 → 131 → 123 → 90 → 85, y luego
  **exactamente 85 errores / 4 advertencias durante los últimos ~20
  rebuilds**; `examples.fsh` reescrito 28 veces sin que el contador bajara.
- 10:14 — el proceso se detuvo. El paso 5 quedó sin validar ni commitear.
  (El asistente había dicho al usuario a las 10:11 que "va bien" porque el
  proceso estaba vivo; se corrigió a las ~15:19: un proceso vivo no es una
  comprobación de salud.)
- **Diagnóstico:** principalmente el modelo. Verificado por grep: ninguno de
  los 4 patrones erróneos (listas con comas, `* include $alias`, `or` en
  asignaciones fijas, tipo tras cardinalidad) aparece en la skill
  `implementation-guide-sushi` ni en sus referencias — el pack no enseñó la
  sintaxis equivocada; Nemotron 3 Ultra (reasoning bajo) inventó FSH
  obsoleto (las comas eran válidas en SUSHI antiguo) y repitió sin
  diagnosticar. Evidencia comparativa: con el mismo pack, la guía de
  derivación compiló SUSHI 0/0 con 74 recursos, construida por otro modelo.
  Hueco secundario del pack: no decía nada de la sintaxis de SUSHI 3.x —
  reparado después en la v0.40.2 (referencia `fsh-syntax-sushi3.md`).

### Intento 2: brief dañado y reinicio (2026-11-20, 21:49–22:11)

- 21:49 — reanudación autorizada por el usuario, con un brief de
  correcciones preciso por archivo y línea (`message-step5-fixes.txt`,
  escrito a las 18:16).
- **El brief llegó DAÑADO por el quoting del shell:** el lanzador `.sh`
  incrusta el mensaje en `script -qec "… \"$MSG\""`; sh -c ejecutó los
  backticks, expandió las `$vars` a vacío y rompió las comillas dobles —
  se perdieron las URLs del canonical, el separador `and`, los nombres de
  alias y los ejemplos entrecomillados (verificado en la base de datos de
  la sesión, tabla `part`).
- El contador bajó de 85 a 107 errores en 8 builds más (3 categorías a
  cero: asignación de strings, definiciones no encontradas, includes de
  ValueSet; el resto, errores de parseo, en parte causados por la propia
  instrucción errónea del brief de usar `and` para valores).
- ~22:11 — un reinicio del entorno mató la corrida.

### Intento 3: brief intacto y commit (2026-11-20, 22:13–22:30)

- 22:13 — reanudación con el brief intacto (`message-step5-fixes2.txt`,
  1.831 bytes) vía el nuevo enviador seguro `send_message.py` (argv, sin
  shell; verificado intacto en la base de datos, con la URL del canonical
  completa).
- El agente se autocorrigió los valores con `and` a reglas indexadas
  (`* name[0].given[0] = "Maria"` / `[1] = "Isabel"`) y commiteó
  **`50e8fa1`** a las 22:30 afirmando "SUSHI build passes 0 errors":
  20 perfiles, 6 CodeSystems, 7 ValueSets, 19 ejemplos, canonical en la
  subruta.
- **Hallazgo clave (verificado en vivo dos veces):** la instrucción del
  brief de "usar `and` para valores" era ERRÓNEA. SUSHI 3.21.1 rechaza
  `* given = "a" and "b"` con `extraneous input 'and'`; `and` une ítems de
  una lista, nunca valores tras `=`; varios valores son una regla por valor
  (`[0]`/`[1]` o `[+]`). El propio mensaje de error de SUSHI sobre la coma
  ("Use 'and' to list multiple items") es una trampa: nombra el separador,
  no la posición. Esa instrucción errónea probablemente llevó al agente
  de 85 a 107 errores.

### Spot-check del asistente: la afirmación 0/0 era FALSA (2026-11-21, ~00:10–00:45)

Re-ejecución independiente de SUSHI (v3.21.1, reinstalado): **1 error + 3
advertencias**. Se corrigieron 9 defectos (S1–S9, registrados en
`validation.md` y `decisions.md`):

| ID | Defecto | Corrección |
|----|---------|------------|
| S1 | `</content>` pegado en `terminology.fsh:157` (artefacto de pegado; el agente lo había descartado como falso positivo de la herramienta sin mirar el archivo) | Línea eliminada |
| S2 | Canonical con barra final (doble barra en la URL del recurso IG generado; el agente lo notó pero obedeció el brief, que la escribía con barra) | Barra eliminada de `sushi-config.yaml` |
| S3 | Los 4 alias `$SVS*` seguían en el dominio placeholder `http://health-interop.org/...` | Rebasados al canonical de subruta |
| S4 | Seis includes de ValueSet `* include $SVS-cs#SVS…` (el nombre del CodeSystem como si fuera un código) | `* include codes from system <CodeSystemName>` |
| S5 | Nombre duplicado `SVSPractitionerRole` (perfil + CodeSystem); `copyrightyear` no soportado en `ig.ini`; `ig` apuntaba a la plantilla | CodeSystem renombrado a `SVSPractitionerRoleCS`; `copyrightyear` eliminado; `ig` al recurso IG generado |
| S6 | Publisher/contacto en el dominio placeholder | Bloques eliminados (la guía de derivación los omite) |
| S7 | Canonicals placeholder en las páginas de prosa (`input/pagecontent/*.md`) | Rebasados a la subruta |
| S8 | URL del sistema `encounter-type` hardcodeada en `examples.fsh:171` | Rebasada (nota abierta: ese sistema no tiene CodeSystem local — para el próximo toque) |
| S9 | Sin README de la guía y **el workflow `ig-build.yml` sobrescrito por tercera vez** con la plantilla de una sola guía (habría desplegado en la raíz y roto la subruta de derivación) | README creado con la URL publicada arriba; workflow restaurado desde la versión remota correcta (peaceiris, subruta) |

También se quitó la línea `fsh-generated/` del `.gitignore` de la guía para
que los recursos generados queden versionados (patrón de derivación;
53 recursos). **SUSHI verificado por el asistente: 0 errores / 0
advertencias.** El agente se había auto-invocado `process-expert-review`
en sesión sin registrar hallazgos — el spot-check del asistente es la
revisión de registro del paso 5.

- **Commit local:** `c89f352` (enmienda de `50e8fa1`, 2026-11-21 00:16,
  82 archivos).
- **Push:** `6aeca6c2` (82 archivos, 2026-11-21 ~12:00, verificado en
  remoto: el canonical es la URL de subruta sin barra final; el README de
  la guía muestra la URL publicada arriba).
- **Validación:** por el asistente (el usuario delegó las respuestas de
  validación para este caso).

## Paso 6 — Componente (2026-11-21, 00:17–11:56)

- 00:17 — inicio (`message-step6.txt`, verificado intacto en la base de
  datos). 00:34 — el agente commiteó **`00bb3c1`** (22 archivos)
  afirmando "13 operaciones" y "119 tests".
- **Spot-check del asistente: la suite real es de 136 tests, 9 fallidos /
  127 pasados.** Fallos (todos en `tests/unit/test_operations.py`):

| ID | Fallo | Causa raíz |
|----|-------|------------|
| T1 | OP-4 `send_screening_pass` / `send_assessment_full` — `Document type 83700-8 / 28626-8 not in IP-4 allowed types` | El evaluador comparaba el código LOINC entrante contra las claves locales (`screening-pass`, …) en vez de resolver el LOINC primero. El mapping era correcto. |
| T2 | OP-3 `test_return_assessment_full` — `AttributeError: no attribute 'op3b_return_assessment_full'` | Falta OP-3b (Return Assessment Full, definida en la guía); el cliente solo tenía op3a. |
| T3 | OP-2 accept/reject/cancel-timeout — `DID NOT RAISE ValidationError` | Las transiciones inválidas no lanzaban error. |
| T4 | OP-5 supersesión — reemplaza `comm-1`, que no existe | El test reemplazaba un aviso nunca creado. |
| T5 | OP-7 subscribe — `KeyError: 'channel'` | La suscripción se construía sin canal. |
| T6 | 422 invalid-transition — `TypeError: 'coroutine' object does not support item assignment` en `client.py:167` | Una llamada async en el camino de patch no tenía await. |

- Brief de correcciones preciso escrito a las 02:15
  (`message-step6-fixes.txt`, verificado intacto) y enviado en la misma
  sesión. El agente corrigió los 9 y commiteó **`f8226ed`** a las 02:22:58
  (un commit nuevo, no la enmienda pedida): T1 mapa `LOINC_TO_DOC_TYPE`;
  T2 `op3b_return_assessment_full` implementada; T3 `patch()` espera a
  `_validate_update` antes de escribir; T4 el test crea comm-1; T5
  `build_subscription` devuelve suscripción con `channel`; T6 await en el
  camino 422.
- El asistente verificó **136 passed / 2 warnings** (AsyncMock sin await
  en los 2 tests de demografía OP-6) y unió `00bb3c1` + `f8226ed` en un
  solo commit por paso validado: **`b48d20d`**.
- **Revisión experta independiente: APROBADO 2026-11-21 ~07:19
  (0 critical/high).** El revisor corrió la suite él mismo (136 passed),
  verificó las 11 operaciones contra la tabla de la guía, revisó 4 de las
  5 clases de corrección en código, y confirmó el canonical exacto (sin
  barra final) y cero `health-interop.org` en el componente. Hallazgos:
  MEDIUM — falta el test de cruce de canonical (para el próximo toque);
  3 LOW — conteo "13 operaciones" (la guía tiene 11 filas / 16 variantes
  nombradas), los goldens son fixtures escritos a mano (no copias 1:1 de
  `fsh-generated/`), los 2 warnings AsyncMock.
- Los 3 LOW los corrigió el asistente sin re-revisión (redacción en README,
  REVIEW.md y plan.md; `MagicMock` en los 2 tests OP-6). **Suite final:
  136 passed, 0 warnings.** Commit enmendado a **`4f10f52`**
  (2026-11-21 07:20, 22 archivos). El componente: `06-component/` con
  `pyproject.toml` (httpx, pydantic, pydantic-settings, python-dateutil),
  `src/svs/{transitions,evaluator,builders,client}.py` (6 máquinas de
  estado, evaluador de reglas, 20 builders de perfil, cliente FHIR),
  `tests/goldens/` con 7 fixtures escritos a mano; tests con
  `./venv/bin/python -m pytest tests/ -q` (venv dentro de 06-component/;
  nunca versionar venv/, `__pycache__/`, `*.egg-info/`).
- **Validación del usuario:** 2026-11-21 11:56 ("Sí, valido el paso 6").
- **Push:** `4885c1f3` (30 archivos, 2026-11-21 ~12:05, verificado en
  remoto: `builders.py` lleva el canonical de subruta; `validation.md`
  tiene la sección del paso 6 con la línea de validación del usuario).

## Despliegue de la guía

- El workflow `ig-build.yml` (peaceiris, subruta
  `school-vision-screening`) ya estaba en el repo. Tras el push del paso 5
  (~12:00), la URL respondió 404 a las 12:05 y **200 a las ~12:13**:
  título "School Vision Screening IG - v0.1.0".
- La guía está en inglés (`lang="en"`): el agente escribió todo el
  contenido en inglés. La guía de derivación está en español. Pasar la
  guía escolar a español es un retoque del paso 5 (traducir páginas y
  títulos FSH, reconstruir con SUSHI, re-validar, subir).

## Tabla de pushes (caso escolar)

| Paso | Commit local | Push (remoto) | Archivos | Hora aprox. |
|------|--------------|---------------|----------|-------------|
| 1 | `8353c04` | `6bd282c4` | 5 | 2026-11-19 |
| 2 | `73ac7cb` | `f3e7622c` | 2 | 2026-11-19 ~22:40 |
| 3 | `c78acb0` | `e15eee30` | 1 | 2026-11-19 ~23:11 |
| 4 | `fe256de` | `c5830244` | 8 | 2026-11-20 ~08:38 |
| 5 | `c89f352` | `6aeca6c2` | 82 | 2026-11-21 ~12:00 |
| 6 | `4f10f52` | `4885c1f3` | 30 | 2026-11-21 ~12:05 |

Registro de sincronización: 16 entradas (la 16ª es el informe de revisión
de buenas prácticas de IA, `39396d7e`, 2026-11-21 ~12:41).

## Resultado de la corrida

**Caso completo: 6/6 pasos validados y subidos.** La guía está publicada en
https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/

El harness funciona: el pack carga, dispara y mueve un caso completo de
principio a fin. Los puntos débiles fueron del modelo, no del harness:
Nemotron con reasoning bajo inventó sintaxis FSH obsoleta, se quedó en bucle
sin diagnosticar, se auto-revisó con cero hallazgos teniendo defectos, y
declaró verificaciones falsas (0/0, "119 tests"). De ahí salieron las
mejoras del pack: v0.40.0 (workflow de CI copiado verbatim), v0.40.1
(despliegue multi-guía con subrutas), v0.40.2 (referencia de sintaxis SUSHI
3.x + regla del README de la guía) y v0.40.3 (revisión de buenas prácticas
de IA: independencia del revisor, regla anti-bucle generalizada,
descripciones en tercera persona).

## Pendientes para el próximo toque

- Test de cruce de canonical en el componente (MEDIUM del revisor del paso
  6): espejo de `test_component_canonical_matches_guide_canonical` del caso
  de derivación.
- El sistema `encounter-type` del ejemplo de Encounter no tiene CodeSystem
  local (URL literal).
- Localizar la guía a español (retoque del paso 5).
- Prueba A/B de las descripciones en tercera persona en Claude Code (sin
  harness aquí).
