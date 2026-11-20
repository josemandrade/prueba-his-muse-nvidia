# Informe de validación — Paso 5: Guía de Implementación (Derivación APS → especialidad)

Fecha: 2026-11-19. Guía versión 0.1.0, FHIR R4 4.0.1, canonical
`https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/`.
SUSHI v3.21.1 (`npm install -g fsh-sushi`, instalado 2026-11-19).

## SUSHI final

| Comprobación | Resultado |
|---|---|
| `sushi .` (corrida final tras las correcciones C1–C9, 2026-11-19) | **0 errores / 0 advertencias**, exit 0 |
| Perfiles (StructureDefinition) | 12 |
| Extensiones | 14 |
| ValueSets / CodeSystems | 8 / 8 |
| Instancias (ejemplos) | 31 |
| Recursos generados (`fsh-generated/resources/`) | 74 (26 SD + 8 CS + 8 VS + 31 instancias + ImplementationGuide) |
| Advertencias transitorias de carga de paquetes | Varían entre corridas: la corrida final dio 0, pero el re-chequeo independiente del revisor dio 1 advertencia (`Failed to load automatically-provided hl7.fhir.uv.extensions.r4#latest`) y una corrida anterior 1 (`hl7.terminology.r4#latest`). Son de red/caché, no cambian el significado: **0 errores siempre**. |

## Canonical (cierra el ítem abierto del paso 4)

- Canonical de la guía: `https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/`
  (raíz de GitHub Pages del repo de prueba, donde el workflow CI despliega
  la guía). IG id `hl7.fhir.uv.test.derivacion-aps-especialidad`, versión
  0.1.0, estado draft, única dependencia `hl7.fhir.r4.core 4.0.1`.
- Barrido de `example.org` en la guía: las únicas ocurrencias son sistemas
  de identificador sintéticos en los ejemplos (`http://mpi.red.example.org`,
  `http://aps.losaromos.example.org/...`,
  `http://especialidad.example.org/...`, `http://hub.example.org/...`), la
  dirección sintética del Endpoint `https://especialidad.example.org/fhir`
  (no es una URL canónica) y la
  tabla de sistemas de identificador en `terminology.md`. Ninguna URL
  canónica generada contiene `example.org` (verificado en
  `fsh-generated/resources/`: todas las `url` empiezan por el canonical
  real). Los dominios `example.org` son sistemas de identificador de
  ejemplo, no el canonical de la guía.
- Caveat registrado: el repo de prueba tiene un segundo caso (screening
  visual escolar); si ese caso publica su propia guía necesitará su propia
  decisión de ruta de despliegue — este canonical es la raíz del sitio, que
  hoy ocupa esta guía.

## Enlaces internos

- Comprobación mecánica sobre las 12 páginas (`input/pagecontent/*.md`):
  cada enlace `.html` existe en `fsh-generated/resources/` o es otra página
  de la guía; cada `.png`/`.svg` existe en `input/images/`. **0 problemas.**
- Las 7 SVG de secuencia se copiaron a `input/images/` (la fuente vive en
  la carpeta del caso, `04-sequence-*.svg`); igual que las 3 SVG BPMN y la
  SVG del grafo de recursos.
- Anchos de imagen: las secuencias se muestran a ancho nativo SVG (el PNG
  es 2×, se ve nítido); los BPMN y el grafo, a ancho nativo PNG, todo con
  desplazamiento horizontal.

## Diagramas de secuencia

- Comprobación mecánica `python3 render_sequence.py --check`: **7
  diagramas, 12 operaciones, 39 mensajes de envío, 9 retornos, 0 mensajes
  sin operación, 0 operaciones sin diagrama. CHECK OK.**
- Inspección visual de los 7 PNG a 2× (2026-11-19): todos legibles —
  etiquetas con píldora blanca, fragmentos (loop/alt/opt) con pestañas
  legibles, notas legibles.
- Dos defectos encontrados en la inspección y corregidos en
  `render_sequence.py` (no en el contenido BPMN/FHIR):
  1. La pestaña `opt [si hay cita reservada]` del diagrama de cancelación
     quedaba tapada por la mitad por la barra de activación del hub (las
     pestañas se dibujaban antes que las barras). Corregido: las pestañas
     se dibujan DESPUÉS de las barras de activación; verificado en el
     recorte — la pestaña se lee completa. Lección registrada en el
     docstring del generador.
  2. La etiqueta `POST /Bundle (document: Composition + DocumentReference
     + Condition + CarePlan)` de contrareferencia era demasiado ancha
     (cruzaba dos columnas). Acortada a `POST /Bundle (document)`; el
     detalle vive en la tabla de operaciones de `sequences.md`.
  3. La píldora `[la paciente rechaza]` del separador `alt` del diagrama
     de agendamiento quedaba a 7 unidades del borde izquierdo del
     fragmento (el centro se calculaba con el ancho a tamaño 12 y la
     píldora se mide a 12.5). Corregido en `render_sequence.py`: el
     centro se calcula con el mismo ancho que la píldora y el inset es
     16 — verificado en el recorte, la píldora queda claramente dentro
     del fragmento. Lección registrada en el comentario del código.

## BPMN y grafo de recursos (re-verificación del paso 5)

- `check_bpmn.py --check` en las tres partes: **0 segmentos diagonales,
  0 cruces, 0 elementos DI sin id. CHECK OK en las tres.**
- Inspección visual de los 3 PNG BPMN a 2× (2026-11-19): legibles; las
  etiquetas tienen fondo blanco opaco (la impresión inicial de "línea a
  través de la etiqueta" era un artefacto del escalado — verificado en
  recortes a resolución completa: "Verify referral id", "timeout — 3
  working days", "Counter-delay escalation to APS" y "Accept / reject
  notice" se leen completas).
- Grafo de recursos re-renderizado a 2× (2840×1520) e inspeccionado: 12
  nodos, Task en el centro, marco Bundle; la arista `appointment` apunta
  del Encounter a la Appointment (corrección C4 del paso 4, verificada).

## Correcciones R4 encontradas en el paso 5 (SUSHI las detectó)

1. `Communication.topic` es CodeableConcept 0..1 en R4, no una referencia
   al Task — la guía lleva el nombre codificado de la transición en
   `topic`; el enlace al Task es `basedOn`.
2. `Task.owner` es 0..1 en R4, no 0..* — la guía pone en `owner` el
   servicio que acepta; el profesional que acepta se registra como agente
   de Provenance.
3. `CarePlan.activity.detail` es un BackboneElement cuya narrativa es
   `detail.description` (con `detail.status` 1..1 cuando existe detail).
4. El ValueSet `DerivacionRol` colisionaba por nombre con el perfil
   `DerivacionRol` — renombrado a `DerivacionRolVS` (id `derivacion-rol`
   sin cambio).
5. `businessStatus` 1..1 en ambos archivos (alineado por C8 del paso 4).

Las filas correspondientes de la tabla de mapeo del paso 4 (§11, §3/§4)
son incorrectas en R4 y deben corregirse en el próximo toque de la tabla
de mapeo (registrado en `decisions.md`); no se tocó la tabla validada
del paso 4 en este paso.

## Lo que NO se verificó localmente

- **IG Publisher / validador FHIR:** Java no está disponible en este
  entorno, así que el Publisher no corre en local. La validación completa
  (Publisher + validador) corre en CI (`.github/workflows/ig-build.yml`,
  Plan task 10.32). El workflow en sí no se probó: sus pasos de prueba
  (un push que construye en verde y un push con un FSH roto que construye
  en rojo y no despliega) requieren push y los hace el padre.
- **Despliegue en Pages:** pendiente del push + la ejecución del workflow
  en verde; el canonical asume que Pages se habilita con fuente GitHub
  Actions.

## Páginas de la guía (12)

index, process (BPMN), resources (grafo), profiles, terminology,
operations, sequences, mapping, ihe, lifecycle, rules, public-health.
Sin página de medicamentos controlados: el caso no tiene medicamentos.
