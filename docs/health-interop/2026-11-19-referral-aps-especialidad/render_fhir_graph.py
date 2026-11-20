#!/usr/bin/env python3
"""Render the FHIR resource graph for the referral proposal as an SVG,
in the style of clinFHIR GraphBuilder: each resource is a rectangle
with title and type, references are directional arrows labelled with
the element that carries the reference.

Centre: Task (DerivacionTarea) — the workflow state record.

Usage: python3 render_fhir_graph.py [output.svg]
Default output: docs/health-interop/2026-11-19-referral-aps-especialidad/04-fhir-proposal-graph.svg
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else (
    ROOT / "04-fhir-proposal-graph.svg"
)

W, H = 1420, 760
NODE_W, NODE_H = 260, 110
HEADER_H = 30

# node: id, x, y, resource type, header colour, profile, [field lines], dashed?
NODES = [
    ("patient", 40, 110, "Patient", "#0e7490",
     "DerivacionPaciente", ["RUN · birthDate", "telecom 1..*"], False),
    ("practitioner", 400, 110, "PractitionerRole", "#b45309",
     "DerivacionRol", ["practitioner 1..1", "code: six roles"], False),
    ("servicerequest", 760, 110, "ServiceRequest", "#7c3aed",
     "DerivacionSolicitud", ["intent = order", "priority routine / urgent"], False),
    ("appointment", 1120, 110, "Appointment", "#0f766e",
     "DerivacionCita", ["proposed -> pending -> booked", "slot 0..*"], False),
    ("organization", 40, 330, "Organization", "#6d28d9",
     "Organization (mCSD)", ["providedBy target"], False),
    ("hs", 400, 330, "HealthcareService", "#6d28d9",
     "DerivacionServicio", ["type: local catalogue", "endpoint 0..*"], False),
    ("task", 760, 330, "Task", "#d97706",
     "DerivacionTarea", ["businessStatus: 9 states", "focus -> ServiceRequest"], False),
    ("encounter", 1120, 330, "Encounter", "#15803d",
     "DerivacionEncuentro", ["class = AMB", "planned -> finished"], False),
    ("docref", 40, 550, "DocumentReference", "#1d4ed8",
     "DerivacionDocumento", ["LOINC 11488-4", "content -> Composition"], False),
    ("composition", 400, 550, "Composition", "#1d4ed8",
     "DerivacionContrareferencia", ["type LOINC 11488-4", "status = final"], False),
    ("condition", 760, 550, "Condition", "#15803d",
     "DerivacionDiagnostico", ["ICD-10-CM I50.22", "SNOMED 417996009"], False),
    ("careplan", 1120, 550, "CarePlan", "#be185d",
     "DerivacionPlanSeguimiento", ["status active", "addresses -> Condition"], False),
]

# edge: (path d, label, label x, label y, anchor)
# Routing verified mechanically (no edge through a node interior):
# two right-angle crossings, no shared segments:
#   C1 (1090,495): "encounter" (Composition→Encounter) x "encounter" (Condition→Encounter)
#   C2 (1090,520): "encounter" (Composition→Encounter) x "addresses" (CarePlan→Condition)
EDGES = [
    ("M860,330 V220", "focus", 872, 275, "start"),
    ("M760,385 H670 V275 H170 V220", "for", 420, 266, "middle"),
    ("M800,330 V250 H530 V220", "requester", 665, 241, "middle"),
    ("M1120,165 H1020", "basedOn", 1070, 156, "middle"),
    ("M860,440 V470 H530 V440", "owner", 695, 461, "middle"),
    ("M1250,330 V220", "appointment", 1262, 275, "start"),
    ("M530,660 V690 H1090 V470 H1180 V440", "encounter", 810, 681, "middle"),
    ("M300,605 H400", "content", 350, 596, "middle"),  # full element: content.attachment.url,
    ("M710,550 V495 H850 V550", "section.entry", 780, 486, "middle"),
    ("M890,550 V495 H1250 V440", "encounter", 1070, 486, "middle"),
    ("M1120,550 V520 H1020 V550", "addresses", 1070, 511, "middle"),
    ("M400,410 H300", "providedBy", 350, 401, "middle"),
]


def node_svg(n):
    nid, x, y, rtype, color, profile, fields, dashed = n
    dash = ' stroke-dasharray="7 4"' if dashed else ""
    parts = []
    parts.append(
        f'<rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" rx="8" '
        f'fill="#ffffff" stroke="{color}" stroke-width="2"{dash}/>'
    )
    parts.append(
        f'<rect x="{x}" y="{y}" width="{NODE_W}" height="{HEADER_H}" rx="8" fill="{color}"/>'
        f'<rect x="{x}" y="{y + HEADER_H - 8}" width="{NODE_W}" height="8" fill="{color}"/>'
    )
    parts.append(
        f'<text x="{x + NODE_W // 2}" y="{y + 21}" text-anchor="middle" '
        f'font-family="sans-serif" font-size="16" font-weight="bold" fill="#ffffff">'
        f'{escape(rtype)}</text>'
    )
    ty = y + HEADER_H + 22
    parts.append(
        f'<text x="{x + NODE_W // 2}" y="{ty}" text-anchor="middle" '
        f'font-family="sans-serif" font-size="13" font-weight="bold" fill="#1f2937">'
        f'{escape(profile)}</text>'
    )
    for i, line in enumerate(fields):
        parts.append(
            f'<text x="{x + NODE_W // 2}" y="{ty + 20 + i * 19}" text-anchor="middle" '
            f'font-family="sans-serif" font-size="12" fill="#4b5563">'
            f'{escape(line)}</text>'
        )
    return "\n".join(parts)


def label_svg(text, lx, ly, anchor):
    # a white pill behind the label so it stays readable over lines
    width = len(text) * 7.4 + 12
    x = lx - width / 2 if anchor == "middle" else lx
    return (
        f'<rect x="{x:.0f}" y="{ly - 13:.0f}" width="{width:.0f}" height="18" rx="9" '
        f'fill="#ffffff" stroke="#9ca3af" stroke-width="0.7"/>'
        f'<text x="{lx}" y="{ly:.0f}" text-anchor="{anchor}" '
        f'font-family="sans-serif" font-size="12.5" fill="#111827">{escape(text)}</text>'
    )


def main():
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}">'
    )
    parts.append(
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#374151"/></marker></defs>'
    )
    parts.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>')
    # Bundle envelope (dashed frame)
    parts.append(
        '<rect x="25" y="40" width="1370" height="660" rx="14" '
        'fill="none" stroke="#6b7280" stroke-width="2" stroke-dasharray="10 6"/>'
    )
    parts.append(
        '<text x="48" y="72" font-family="sans-serif" font-size="17" '
        'font-weight="bold" fill="#374151">Bundle (transaction / document)</text>'
    )
    parts.append(
        '<text x="48" y="94" font-family="sans-serif" font-size="13" fill="#6b7280">'
        'un sobre por evento: PI-0 push (transaction) · PI-3 counter-referral (document)</text>'
    )
    # edges first, then nodes on top
    for d, label, lx, ly, anchor in EDGES:
        parts.append(
            f'<path d="{d}" fill="none" stroke="#374151" stroke-width="1.8" '
            f'marker-end="url(#arrow)"/>'
        )
    for d, label, lx, ly, anchor in EDGES:
        parts.append(label_svg(label, lx, ly, anchor))
    for n in NODES:
        parts.append(node_svg(n))
    parts.append(
        '<text x="710" y="730" text-anchor="middle" font-family="sans-serif" '
        'font-size="13" fill="#6b7280">Las flechas son referencias FHIR; la etiqueta es el '
        'elemento que lleva la referencia. El Bundle es el sobre que lleva los recursos.</text>'
    )
    parts.append("</svg>")
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
