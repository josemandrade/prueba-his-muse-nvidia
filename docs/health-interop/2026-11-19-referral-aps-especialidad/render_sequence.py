#!/usr/bin/env python3
"""Render the sequence diagrams for the DAU case as SVG (one per flow),
following the pack's sequence-diagrams skill: every message names the
operation that carries it (operation id, FHIR interaction, IHE profile
when one applies); solid arrow = synchronous, open arrow = asynchronous,
dashed arrow = return with the outcome; alt/opt fragments for the
branches; a note where a rule constrains the flow.

Usage: python3 render_sequence.py [--check]
Default: writes the 5 SVGs to the case folder and the 5 PNGs (2x) to the
guide's input/images/.
--check: verify the operation-reference rule mechanically (every message
names an operation from the proposal; every operation appears in at
least one diagram) and exit without writing files.

Flows (from the BPMN v7 paths, not invented): admission, discharge,
abandonment, network-pull, document-retrieval.

Readability rules (same hard gate as render_bpmn.py):
- Messages are horizontal, lifelines are vertical: no diagonals, ever.
- Message labels are short (operation id + interaction, at most 2
  lines); the detail lives in the operation table under the diagram
  (sequences.md), not on the arrow.
- Labels get a white pill behind them so they stay readable where
  they cross a lifeline. The two lines of a label sit 19 px apart,
  so their pills (18 px tall) never overlap each other.
- A fragment tab must clear the first message's label: the tab sits
  70 px above the first arrow, and the separator guard is left-anchored
  inside the fragment, never centred on a fixed offset (a centred guard
  spills out of a narrow fragment, and a tab that overlaps a label pill
  hides the end of its own guard text). Tabs are drawn AFTER the
  activation bars: a tab that crosses a lifeline is otherwise covered
  by the bar (this hid the middle of the cancellation opt tab).
- The cairosvg default font has no U+2192 (rightwards arrow): write
  ">" in subtitles, or the arrows render as empty boxes.
- Render the PNG at 2x the SVG size and LOOK at it at display size,
  by zones, before shipping. A diagram nobody can read is worse than
  no diagram.
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

import cairosvg

ROOT = Path(__file__).resolve().parent
CASE = ROOT  # this file lives in the case folder
PNG_DIR = CASE / "05-implementation-guide/input/images"

MARGIN = 40
ROW_H = 72
TOP_TITLE = 30
PART_Y = 84
PART_H = 56
FONT = "sans-serif"

# Operation inventory: the 12 operations of the proposal/guide
# (operations.md). Every message names one of these; every one of these
# appears in at least one diagram. A return is the outcome of the message
# above it, so it carries no operation of its own. A patient-facing
# message (phone / in person) is declared as non-FHIR on its label.
OPERATIONS = [f"OP-{i}" for i in range(1, 13)]

# Arrow: (kind, from_idx, to_idx, label_lines, op)
# kind: "sync" (solid + filled head), "async" (solid + open head),
# "return" (dashed + open head, label below the arrow). op is None for
# returns: a return is the outcome of the message above it.
# Fragment: {"type": "alt"|"opt"|"loop", "first": arrow idx,
# "last": arrow idx, "guards": [guard per operand],
# "sep_after": arrow idx (alt only)}.
# Activation: (participant idx, first arrow idx, last arrow idx).

DIAGRAMS = {
    "request": {
        "title": "Solicitud — crear la derivación y enrutarla (PI-0)",
        "subtitle": (
            "BPMN Parte A: Médico APS > ¿Paciente acepta la derivación? "
            "> Resolver identidad vía MPI > Crear derivación (conjunto "
            "mínimo de datos) > Hub recibe y enruta > Especialidad recibe"
        ),
        "participants": [
            ("Médico APS", ""),
            ("Administrativo APS", ""),
            ("MPI", ""),
            ("Hub de derivación", ""),
            ("Directorio de servicios", "mCSD"),
            ("Especialidad", "clínico de triaje"),
            ("Paciente", ""),
        ],
        "arrows": [
            ("sync", 0, 2, ["OP-9 Resolver identidad",
                            "PIXm ITI-83 $ihe-pix / PDQm ITI-78"],
             "OP-9"),
            ("return", 2, 0, ["clave MPI / no resuelta"], None),
            ("sync", 0, 3, ["OP-1 Crear derivación",
                            "POST /Bundle (ServiceRequest + Task)"],
             "OP-1"),
            ("sync", 3, 4, ["OP-10 Encontrar servicio",
                            "mCSD ITI-90 Find Matching Care Services"],
             "OP-10"),
            ("return", 4, 3, ["HealthcareService + Endpoint"], None),
            ("sync", 3, 5, ["OP-1 Reenviar derivación",
                            "POST /Bundle (m11)"],
             "OP-1"),
            ("return", 5, 3, ["derivación recibida"], None),
            ("sync", 3, 1, ["OP-12 Notificar creación a APS",
                            "POST /Communication (hub -> APS)"],
             "OP-12"),
            ("sync", 1, 6, ["OP-12 Avisar a la paciente",
                            "aviso no-FHIR: teléfono / presencial"],
             "OP-12"),
            ("sync", 1, 3, ["OP-11 Suscribirse a los cambios",
                            "POST /Subscription (Task?focus=...)"],
             "OP-11"),
            ("return", 3, 1, ["201 Created"], None),
        ],
        "fragments": [
            {"type": "opt", "first": 9, "last": 10,
             "guards": ["si APS quiere seguir el estado"],
             "sep_after": None},
        ],
        "activations": [(2, 0, 1), (3, 2, 8)],
        "notes": [
            "Sin identidad resuelta no se crea la derivación: el médico "
            "APS corrige los datos y reintenta (OP-9). Si el paciente "
            "rechaza la derivación en la creación, no se crea nada y APS "
            "registra la decisión y el motivo localmente (entidad 12, sin "
            "equivalente FHIR).",
            "El identificador de la derivación (REF-2026-0001) es la clave "
            "de continuación: enlaza este diagrama con los de triaje, "
            "agendamiento, atención, contrareferencia, consulta de estado "
            "y cancelación. Una respuesta que llega en otra sesión o día "
            "es su propio diagrama, nunca un retorno en el diagrama que "
            "envía.",
            "OP-11 es opcional: APS se suscribe a las transiciones del "
            "Task; el hub notifica en cada transición (una Subscription "
            "FHIR sobre un evento que no es de documento es propia de la "
            "guía — DSUBm suscribe solo eventos de documento).",
        ],
    },
    "triage": {
        "title": "Triaje — aceptar o rechazar la derivación (PI-1)",
        "subtitle": (
            "BPMN Parte A: Especialidad recibe > Triaje > ¿Aceptar o "
            "rechazar? > Hub reenvía la decisión a APS > APS informa a "
            "la paciente"
        ),
        "participants": [
            ("Clínico de triaje", "especialidad"),
            ("Hub de derivación", ""),
            ("Administrativo APS", ""),
            ("Paciente", ""),
        ],
        "arrows": [
            ("sync", 0, 1, ["OP-2 Registrar aceptación",
                            "PATCH /Task accepted + owner"],
             "OP-2"),
            ("sync", 0, 1, ["OP-2 Registrar rechazo",
                            "PATCH /Task rejected + statusReason"],
             "OP-2"),
            ("sync", 1, 2, ["OP-12 Reenviar decisión a APS",
                            "POST /Communication (hub -> APS)"],
             "OP-12"),
            ("sync", 2, 3, ["OP-12 Avisar a la paciente",
                            "aviso no-FHIR: teléfono / presencial"],
             "OP-12"),
        ],
        "fragments": [
            {"type": "alt", "first": 0, "last": 1,
             "guards": ["aceptar — nombra servicio y profesional",
                        "rechazar — con motivo"],
             "sep_after": 0},
        ],
        "activations": [(1, 0, 2)],
        "notes": [
            "Plazo de aceptación: 5 días hábiles desde la creación (2 si "
            "es urgente). Si vence, el hub escala a la especialidad y "
            "notifica a APS; el ciclo vuelve a entrar en la espera — un "
            "timeout nunca cierra la derivación.",
            "Si la especialidad rechaza, APS re-triaje en 5 días hábiles: "
            "re-derivar con más información o a otra especialidad es una "
            "derivación NUEVA (nuevo Task + ServiceRequest; ver diagrama "
            "de solicitud); la primera se cierra como rejected solo cuando "
            "APS decide el resultado del re-triaje.",
            "360X no tiene transacción de aceptar (la aceptación es "
            "implícita); en esta guía la aceptación es una transición "
            "explícita del Task (OP-2). PCC-56 Referral Decline es solo "
            "el patrón de la rama de rechazo.",
        ],
    },
    "schedule": {
        "title": "Agendamiento — ofrecer, confirmar y reservar la cita (PI-2)",
        "subtitle": (
            "BPMN Parte B: Especialidad aceptada > Ofrecer cita > "
            "Paciente confirma o rechaza > Reservar (Appointment + Slot) "
            "> Crear Encounter (planned)"
        ),
        "participants": [
            ("Agendador de especialidad", ""),
            ("Servidor de agendamiento", "Scheduling ITI-115/117"),
            ("Hub de derivación", ""),
            ("Administrativo APS", ""),
            ("Paciente", ""),
        ],
        "arrows": [
            ("sync", 0, 1, ["OP-3 Buscar huecos",
                            "Scheduling $find ITI-115"],
             "OP-3"),
            ("return", 1, 0, ["Slots libres"], None),
            ("sync", 0, 2, ["OP-3 Ofrecer cita",
                            "POST /Appointment (proposed)"],
             "OP-3"),
            ("sync", 2, 4, ["OP-12 Oferta a la paciente",
                            "aviso no-FHIR: teléfono / presencial"],
             "OP-12"),
            ("sync", 2, 3, ["OP-12 Notificar oferta a APS",
                            "POST /Communication"],
             "OP-12"),
            ("sync", 0, 4, ["OP-12 Perseguir confirmación",
                            "aviso no-FHIR: teléfono (hasta 2 veces)"],
             "OP-12"),
            ("sync", 4, 2, ["OP-3 Confirmar asistencia",
                            "POST /AppointmentResponse accepted"],
             "OP-3"),
            ("sync", 2, 0, ["OP-3 Confirmación reenviada",
                            "AppointmentResponse -> agendador"],
             "OP-3"),
            ("sync", 0, 1, ["OP-3 Reservar cita",
                            "Scheduling $book ITI-117"],
             "OP-3"),
            ("return", 1, 0, ["Appointment booked"], None),
            ("sync", 0, 2, ["OP-3 Cita reservada",
                            "PATCH /Appointment booked; POST /Encounter planned"],
             "OP-3"),
            ("sync", 2, 3, ["OP-12 Notificar reserva a APS",
                            "POST /Communication"],
             "OP-12"),
            ("sync", 4, 2, ["OP-4 Rechazar oferta",
                            "POST /AppointmentResponse declined"],
             "OP-4"),
            ("sync", 2, 0, ["OP-4 Rechazo reenviado",
                            "AppointmentResponse -> agendador"],
             "OP-4"),
            ("sync", 0, 2, ["OP-4 Re-ofertar cita",
                            "POST /Appointment nuevo (proposed)"],
             "OP-4"),
        ],
        "fragments": [
            {"type": "loop", "first": 2, "last": 14,
             "guards": ["hasta reservar la cita o cancelar la derivación"],
             "sep_after": None},
            {"type": "opt", "first": 5, "last": 5,
             "guards": ["si no hay respuesta en 3 días hábiles"],
             "sep_after": None},
            {"type": "alt", "first": 6, "last": 14,
             "guards": ["la paciente confirma",
                        "la paciente rechaza"],
             "sep_after": 11},
        ],
        "activations": [(1, 0, 1), (1, 8, 9), (2, 2, 14)],
        "notes": [
            "Cada oferta es un Appointment NUEVO (offer-number +1); los "
            "conteos de rechazo y persecución se reinician por oferta. "
            "Una cita propuesta no se reserva hasta que la paciente "
            "confirma: proposed > pending (paciente confirmó) > booked "
            "(agendador reserva).",
            "Plazo de oferta: 10 días hábiles desde la aceptación. Si "
            "vence, el hub escala a la especialidad y notifica a APS. Si "
            "la especialidad no puede agendar, la derivación vuelve al "
            "re-triaje de APS (ver diagrama de triaje, mismo Task id).",
            "Scheduling no tiene transacción de publicar o notificar: "
            "ITI-115/116/117/118 son find/hold/book/search iniciados por "
            "el cliente. La oferta, la confirmación y la persecución son "
            "el ciclo propio de la guía (OP-3/OP-4).",
        ],
    },
    "attend": {
        "title": "Atención — asistir o no asistir a la cita (PI-2)",
        "subtitle": (
            "BPMN Parte B: Cita reservada > Esperar fecha/hora > ¿Paciente "
            "asistió? > Atender (Encounter finished) o registrar no-show"
        ),
        "participants": [
            ("Paciente", ""),
            ("Especialista", ""),
            ("Hub de derivación", ""),
            ("Administrativo APS", ""),
        ],
        "arrows": [
            ("sync", 0, 1, ["OP-5 Llegada de la paciente",
                            "llegada presencial (no-FHIR)"],
             "OP-5"),
            ("sync", 1, 2, ["OP-5 Registrar asistencia",
                            "PATCH /Appointment arrived; PATCH /Encounter in-progress"],
             "OP-5"),
            ("sync", 1, 2, ["OP-5 Encuentro terminado",
                            "PATCH /Encounter finished; PATCH /Appointment fulfilled"],
             "OP-5"),
            ("sync", 1, 2, ["OP-5 Registrar no-show",
                            "PATCH /Appointment noshow + cancelationReason"],
             "OP-5"),
            ("sync", 2, 3, ["OP-12 Notificar no-show a APS",
                            "POST /Communication"],
             "OP-12"),
            ("sync", 1, 2, ["OP-4 Re-agendar cita",
                            "nuevo Appointment (mismo ciclo)"],
             "OP-4"),
        ],
        "fragments": [
            {"type": "alt", "first": 0, "last": 5,
             "guards": ["la paciente asiste",
                        "la paciente no asiste"],
             "sep_after": 2},
        ],
        "activations": [(2, 1, 5)],
        "notes": [
            "No hay Encounter en un no-show: el no-show vive solo en el "
            "Appointment (noshow + cancelationReason) y el Slot vuelve a "
            "free. La oferta re-agendada es un Appointment NUEVO y sigue "
            "el mismo ciclo confirmar/perseguir del diagrama de "
            "agendamiento (OP-3/OP-4).",
            "Tras el segundo no-show el Task pasa a failed / "
            "businessStatus = no-show y la derivación se cierra (OP-5). "
            "El plazo de contrareferencia corre desde el Encounter "
            "finished, no desde el Appointment arrived.",
            "360X PCC-61 No-show Notification es solo el patrón de la "
            "rama de no-show; el registro de asistencia en sí es propio "
            "de la guía (OP-5).",
        ],
    },
    "result-return": {
        "title": "Contrareferencia — devolver el resultado a APS (PI-3)",
        "subtitle": (
            "BPMN Parte B: Especialista escribe contrareferencia "
            "(diagnóstico, plan, seguimiento) > Hub la enruta a APS > APS "
            "acusa recibo > Task counter-referred (ciclo cerrado)"
        ),
        "participants": [
            ("Especialista", ""),
            ("Hub de derivación", ""),
            ("Administrativo APS", ""),
            ("Médico APS", ""),
        ],
        "arrows": [
            ("sync", 0, 1, ["OP-6 Enviar contrareferencia",
                            "POST /Bundle (document)"],
             "OP-6"),
            ("sync", 1, 2, ["OP-6 Reenviar contrareferencia",
                            "MHD ITI-65 Provide Document Bundle"],
             "OP-6"),
            ("sync", 2, 3, ["OP-12 Entregar contrareferencia al médico",
                            "POST /Communication (APS interno)"],
             "OP-12"),
            ("sync", 2, 1, ["OP-6 Acuse de recibo",
                            "POST /Communication (basedOn -> Task)"],
             "OP-6"),
        ],
        "fragments": [],
        "activations": [(1, 0, 3)],
        "notes": [
            "Plazo de contrareferencia: 5 días hábiles desde el Encounter "
            "finished. Si vence, el hub escala a la especialidad y "
            "notifica a APS. Una contrareferencia que llega tarde se "
            "acepta igualmente: el plazo dispara escalada, no rechazo.",
            "El Task pasa a completed / businessStatus = "
            "counter-referred cuando el hub registra el acuse de recibo "
            "de APS (misma transacción). El ciclo queda cerrado; una "
            "corrección es una versión nueva del documento, no un cambio "
            "de estado.",
            "Asociación ofrecida: APS puede suscribirse a que el documento "
            "esté disponible (DSUBm ITI-110); la suscripción y la "
            "notificación tienen la misma forma que OP-11 con criteria "
            "sobre DocumentReference. La pierna de documento es MHD ITI-65 "
            "(full si se implementa exacto); 360X PCC-57 es solo el patrón "
            "de contenido.",
        ],
    },
    "status-query": {
        "title": "Consulta de estado — preguntar dónde va la derivación (PI-4)",
        "subtitle": (
            "BPMN Parte C: APS necesita el estado > Consultar al hub > "
            "Hub devuelve estado actual, último cambio y próximo paso "
            "(o no encontrado)"
        ),
        "participants": [
            ("Médico / administrativo APS", ""),
            ("Hub de derivación", ""),
        ],
        "arrows": [
            ("sync", 0, 1, ["OP-7 Consultar estado",
                            "GET /Task?focus:ServiceRequest.identifier=REF-2026-0001"],
             "OP-7"),
            ("return", 1, 0, ["Task (status, businessStatus, lastModified, próximo paso)"], None),
            ("return", 1, 0, ["404 not found — verificar id"], None),
        ],
        "fragments": [
            {"type": "alt", "first": 1, "last": 2,
             "guards": ["derivación encontrada",
                        "no encontrada"],
             "sep_after": 1},
        ],
        "activations": [(1, 0, 2)],
        "notes": [
            "PI-4 es solo lectura: la consulta nunca cambia el estado. "
            "Si el id no existe, APS verifica el identificador de la "
            "derivación.",
            "None applies (explícito): ningún perfil IHE lleva una "
            "consulta de estado de flujo de trabajo. QEDm PCC-44 cubre "
            "solo datos clínicos; DSUBm cubre solo eventos de documento. "
            "La OP-7 de la guía es búsqueda FHIR simple sobre el Task.",
        ],
    },
    "cancellation": {
        "title": "Cancelación — cancelar la derivación antes de completarse",
        "subtitle": (
            "BPMN Partes A y B (fila de cancelación): APS, paciente o "
            "especialidad solicita cancelar > Hub cancela Task y cita > "
            "Avisa a todas las partes"
        ),
        "participants": [
            ("Administrativo APS", ""),
            ("Hub de derivación", ""),
            ("Agendador de especialidad", ""),
            ("Paciente", ""),
            ("Especialista", ""),
        ],
        "arrows": [
            ("sync", 0, 1, ["OP-8 Solicitar cancelación",
                            "PATCH /Task cancelled + statusReason"],
             "OP-8"),
            ("sync", 1, 2, ["OP-8 Cancelar cita reservada",
                            "PATCH /Appointment cancelled (Scheduling $book cancel, ITI-117)"],
             "OP-8"),
            ("return", 2, 1, ["Slot liberado"], None),
            ("sync", 1, 3, ["OP-12 Notificar cancelación a la paciente",
                            "aviso no-FHIR: teléfono / presencial"],
             "OP-12"),
            ("sync", 1, 4, ["OP-12 Notificar cancelación a la especialidad",
                            "POST /Communication"],
             "OP-12"),
        ],
        "fragments": [
            {"type": "opt", "first": 1, "last": 2,
             "guards": ["si hay cita reservada"],
             "sep_after": None},
        ],
        "activations": [(1, 0, 4)],
        "notes": [
            "El diagrama muestra la cancelación solicitada por APS; la "
            "paciente o la especialidad la inician del mismo modo (misma "
            "OP-8, misma transición del Task; el solicitante queda en "
            "Provenance). El administrativo APS informa al médico APS.",
            "La cancelación es posible en cualquier punto antes de "
            "completarse. El fallecimiento del paciente es un motivo de "
            "cancelación (statusReason 'patient deceased'). El único "
            "camino de corrección es la re-apertura por el operador del "
            "hub.",
            "360X PCC-58 Referral Cancellation es solo el patrón, con "
            "tope de dirección: PCC-58 viaja solo Initiator > Recipient, "
            "mientras este caso permite que la especialidad o la paciente "
            "inicien la cancelación.",
        ],
    },
}


def wrap(text, max_len):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > max_len:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return lines


def text_w(s, px):
    return len(s) * px * 0.58


def pill(s, x, y, size=12.5, fill="#ffffff", stroke="#9ca3af"):
    w = text_w(s, size) + 12
    return (
        f'<rect x="{x - w / 2:.0f}" y="{y - 13:.0f}" width="{w:.0f}" '
        f'height="18" rx="9" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="0.7"/>'
        f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{size}" fill="#111827">'
        f'{escape(s)}</text>'
    )


def check():
    """Mechanical check of the operation-reference rule."""
    used = {}
    msgs_without_op = []
    for name, d in DIAGRAMS.items():
        for i, (kind, _f, _t, _lines, op) in enumerate(d["arrows"]):
            if kind == "return":
                continue
            if op is None:
                msgs_without_op.append(f"{name} arrow {i}")
            elif op not in OPERATIONS:
                msgs_without_op.append(f"{name} arrow {i} (unknown op {op!r})")
            else:
                used.setdefault(op, []).append(name)
    missing = [op for op in OPERATIONS if op not in used]
    n_msgs = sum(
        1 for d in DIAGRAMS.values()
        for a in d["arrows"] if a[0] != "return"
    )
    n_returns = sum(
        1 for d in DIAGRAMS.values()
        for a in d["arrows"] if a[0] == "return"
    )
    print(f"diagrams: {len(DIAGRAMS)}")
    print(f"operations in inventory: {len(OPERATIONS)}")
    print(f"send messages: {n_msgs} (returns: {n_returns})")
    print(f"messages without a known operation: {len(msgs_without_op)}")
    for m in msgs_without_op:
        print(f"  MISSING OP: {m}")
    print(f"operations without a diagram: {len(missing)}")
    for op in missing:
        print(f"  NO DIAGRAM: {op}")
    for op in OPERATIONS:
        print(f"  {op}: {', '.join(used.get(op, []))}")
    ok = not msgs_without_op and not missing
    print("CHECK " + ("OK" if ok else "FAILED"))
    return ok


def render(name, d):
    parts = d["participants"]
    n = len(parts)
    col_w = 480 if n == 2 else 300
    w = 2 * MARGIN + n * col_w
    col_x = [MARGIN + col_w / 2 + i * col_w for i in range(n)]

    # --- vertical layout: one row per arrow, extra room at fragment edges
    frag_first = {f["first"] for f in d["fragments"]}
    frag_last = {f["last"] for f in d["fragments"]}
    y = PART_Y + PART_H + 46
    ys = []
    for i in range(len(d["arrows"])):
        if i in frag_first:
            y += 30
        ys.append(y)
        y += ROW_H
        if i in frag_last:
            y += 20
    last_y = ys[-1]
    notes_top = last_y + 52

    # --- notes (wrapped) and total height
    note_lines = []
    max_note = int((w - 2 * MARGIN - 32) / 7.0)
    for note in d["notes"]:
        note_lines.append(wrap(note, max_note))
    notes_h = sum(len(lines) * 18 + 20 for lines in note_lines) + 8 * (
        len(note_lines) - 1
    )
    h = notes_top + notes_h + 52

    out = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}">'
    )
    out.append(
        '<defs>'
        '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#374151"/></marker>'
        '<marker id="arrow-open" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10" fill="none" stroke="#374151" '
        'stroke-width="1.6"/></marker>'
        '<marker id="arrow-ret" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10" fill="none" stroke="#6b7280" '
        'stroke-width="1.5"/></marker>'
        '</defs>'
    )
    out.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>')

    # title + subtitle
    out.append(
        f'<text x="{MARGIN}" y="{TOP_TITLE}" font-family="{FONT}" '
        f'font-size="18" font-weight="bold" fill="#111827">'
        f'{escape(d["title"])}</text>'
    )
    sub = wrap(d["subtitle"], int((w - 2 * MARGIN) / 7.0))
    for i, line in enumerate(sub):
        out.append(
            f'<text x="{MARGIN}" y="{TOP_TITLE + 22 + i * 17}" '
            f'font-family="{FONT}" font-size="13" fill="#6b7280">'
            f'{escape(line)}</text>'
        )

    # --- fragments (behind the arrows)
    tabs = []
    for f in d["fragments"]:
        first, last = f["first"], f["last"]
        involved = set()
        for i in range(first, last + 1):
            involved.add(d["arrows"][i][1])
            involved.add(d["arrows"][i][2])
        lo = min(involved)
        hi = max(involved)
        fx0 = col_x[lo] - (col_w / 2 - 14)
        fx1 = col_x[hi] + (col_w / 2 - 14)
        fy0 = ys[first] - 70
        fy1 = ys[last] + 36
        out.append(
            f'<rect x="{fx0:.0f}" y="{fy0:.0f}" width="{fx1 - fx0:.0f}" '
            f'height="{fy1 - fy0:.0f}" fill="#f9fafb" stroke="#6b7280" '
            f'stroke-width="1.5"/>'
        )
        # Tabs are drawn after the activation bars (below): a tab that
        # crosses a lifeline would otherwise be covered by the bar.
        tabs.append((fx0, fy0, f'{f["type"]} [{f["guards"][0]}]'))
        if f["sep_after"] is not None:
            sep_y = (ys[f["sep_after"]] + ys[f["sep_after"] + 1]) / 2
            out.append(
                f'<line x1="{fx0:.0f}" y1="{sep_y:.0f}" x2="{fx1:.0f}" '
                f'y2="{sep_y:.0f}" stroke="#6b7280" stroke-width="1.2" '
                f'stroke-dasharray="6 4"/>'
            )
            g2 = f'[{f["guards"][1]}]'
            # The pill is centred on its own width (pill() measures at
            # size 12.5): inset 16 from the fragment border so the pill
            # never straddles it (C8: "[la paciente rechaza]" sat on the
            # border because the old centre used the size-12 width).
            gw = text_w(g2, 12.5) + 12
            out.append(pill(g2, fx0 + 16 + gw / 2, sep_y - 6))

    # --- lifelines
    life_bottom = last_y + 36
    for x in col_x:
        out.append(
            f'<line x1="{x:.0f}" y1="{PART_Y + PART_H}" x2="{x:.0f}" '
            f'y2="{life_bottom}" stroke="#9ca3af" stroke-width="1.2" '
            f'stroke-dasharray="5 4"/>'
        )

    # --- activation bars
    def active_at(p, i):
        return any(a[0] == p and a[1] <= i <= a[2] for a in d["activations"])

    for (p, first, last) in d["activations"]:
        x = col_x[p]
        out.append(
            f'<rect x="{x - 6:.0f}" y="{ys[first] - 8:.0f}" width="12" '
            f'height="{ys[last] - ys[first] + 16:.0f}" fill="#ffffff" '
            f'stroke="#374151" stroke-width="1.2"/>'
        )

    # --- fragment tabs (on top of the activation bars)
    for (fx0, fy0, tab) in tabs:
        tw = text_w(tab, 12) + 16
        out.append(
            f'<rect x="{fx0:.0f}" y="{fy0:.0f}" width="{tw:.0f}" height="22" '
            f'fill="#ffffff" stroke="#6b7280" stroke-width="1.5"/>'
            f'<text x="{fx0 + 8:.0f}" y="{fy0 + 15:.0f}" '
            f'font-family="{FONT}" font-size="12" font-weight="bold" '
            f'fill="#111827">{escape(tab)}</text>'
        )

    # --- arrows + labels
    for i, (kind, f, t, lines, _op) in enumerate(d["arrows"]):
        y0 = ys[i]
        x1, x2 = col_x[f], col_x[t]
        ltr = x2 > x1
        # arrows attach to the activation bar edge when the endpoint is
        # active on this row, else to the lifeline centre
        if active_at(f, i):
            x1 += -6 if ltr else 6
        if active_at(t, i):
            x2 += -6 if ltr else 6
        if kind == "sync":
            out.append(
                f'<line x1="{x1:.0f}" y1="{y0}" x2="{x2:.0f}" y2="{y0}" '
                f'stroke="#374151" stroke-width="1.8" '
                f'marker-end="url(#arrow)"/>'
            )
        elif kind == "async":
            out.append(
                f'<line x1="{x1:.0f}" y1="{y0}" x2="{x2:.0f}" y2="{y0}" '
                f'stroke="#374151" stroke-width="1.8" '
                f'marker-end="url(#arrow-open)"/>'
            )
        else:  # return: dashed, open head, label below
            out.append(
                f'<line x1="{x1:.0f}" y1="{y0}" x2="{x2:.0f}" y2="{y0}" '
                f'stroke="#6b7280" stroke-width="1.5" '
                f'stroke-dasharray="7 4" marker-end="url(#arrow-ret)"/>'
            )
        mid = (x1 + x2) / 2
        if kind == "return":
            out.append(pill(lines[0], mid, y0 + 20, size=12, fill="#f3f4f6",
                            stroke="#d1d5db"))
        else:
            for j, line in enumerate(lines):
                out.append(pill(line, mid, y0 - 10 - (len(lines) - 1 - j) * 19))

    # --- participant boxes (on top of the lifelines)
    for (name, sub), x in zip(parts, col_x):
        bw = col_w - 30
        out.append(
            f'<rect x="{x - bw / 2:.0f}" y="{PART_Y}" width="{bw:.0f}" '
            f'height="{PART_H}" rx="8" fill="#ffffff" stroke="#374151" '
            f'stroke-width="1.8"/>'
        )
        name_lines = wrap(name, int((bw - 16) / 7.8))[:2]
        total = len(name_lines) * 17 + (17 if sub else 0)
        ty = PART_Y + (PART_H - total) / 2 + 13
        for line in name_lines:
            out.append(
                f'<text x="{x:.0f}" y="{ty:.0f}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="13" font-weight="bold" '
                f'fill="#111827">{escape(line)}</text>'
            )
            ty += 17
        if sub:
            out.append(
                f'<text x="{x:.0f}" y="{ty:.0f}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="11" fill="#6b7280">'
                f'{escape(sub)}</text>'
            )

    # --- notes
    ny = notes_top
    for lines in note_lines:
        bh = len(lines) * 18 + 20
        out.append(
            f'<rect x="{MARGIN}" y="{ny}" width="{w - 2 * MARGIN}" '
            f'height="{bh}" rx="8" fill="#fef9c3" stroke="#d97706" '
            f'stroke-width="1"/>'
        )
        for j, line in enumerate(lines):
            out.append(
                f'<text x="{MARGIN + 14}" y="{ny + 22 + j * 18}" '
                f'font-family="{FONT}" font-size="12.5" fill="#451a03">'
                f'{escape(line)}</text>'
            )
        ny += bh + 8

    out.append(
        f'<text x="{w // 2}" y="{h - 18}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="12" fill="#6b7280">'
        'Cada mensaje nombra la operación que lo lleva; el detalle '
        '(entradas, ejemplo, resultado esperado) está en la tabla de '
        'operaciones de sequences.md.</text>'
    )
    out.append("</svg>")
    return "\n".join(out), w, h


def main():
    if "--check" in sys.argv:
        sys.exit(0 if check() else 1)
    for name, d in DIAGRAMS.items():
        svg, w, h = render(name, d)
        svg_path = CASE / f"04-sequence-{name}.svg"
        svg_path.write_text(svg, encoding="utf-8")
        png_path = PNG_DIR / f"04-sequence-{name}.png"
        cairosvg.svg2png(
            bytestring=svg.encode("utf-8"),
            write_to=str(png_path),
            output_width=2 * w,
            output_height=2 * h,
        )
        print(
            f"wrote {svg_path} ({svg_path.stat().st_size} bytes, "
            f"{w}x{h}) and {png_path} ({png_path.stat().st_size} bytes, "
            f"{2 * w}x{2 * h})"
        )


if __name__ == "__main__":
    main()
