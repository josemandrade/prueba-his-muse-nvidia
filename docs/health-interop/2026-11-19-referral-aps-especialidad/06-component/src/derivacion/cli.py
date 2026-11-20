"""CLI del componente de derivación.

Uso:
    PYTHONPATH=src python3 -m derivacion.cli <escenario> [--out DIR]

Escenarios: accepted, rejected, no-show (ver `derivacion.scenarios`).
Escribe un JSON por recurso en DIR (`<ResourceType>-<id>.json`) más
`summary.json` con el estado final, y resume el recorrido en stdout.
Solo stdlib; no envía nada a ningún servidor.
"""

import argparse
import json
import sys
from pathlib import Path

from derivacion.scenarios import SCENARIOS, all_resources, summary


def run_scenario(name, out_dir):
    """Ejecuta el escenario y vuelca sus recursos en `out_dir`."""
    referral = SCENARIOS[name]()
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for resource in all_resources(referral):
        filename = f"{resource['resourceType']}-{resource['id']}.json"
        (out / filename).write_text(
            json.dumps(resource, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        written.append(filename)
    if getattr(referral, "counter_referral_bundle", None) is not None:
        filename = "Bundle-bundle-pi3-ref-2026-0001.json"
        (out / filename).write_text(
            json.dumps(
                referral.counter_referral_bundle, indent=2,
                ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        written.append(filename)
    (out / "summary.json").write_text(
        json.dumps(summary(referral), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return referral, written


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Componente de derivación APS → especialidad "
                    "(guía validada, paso 6).")
    parser.add_argument(
        "scenario", choices=sorted(SCENARIOS),
        help="recorrido a ejecutar")
    parser.add_argument(
        "--out", default=None,
        help="directorio de salida (por defecto, examples/<escenario>)")
    args = parser.parse_args(argv)
    out_dir = args.out or str(
        Path(__file__).resolve().parents[2] / "examples" / args.scenario)
    referral, written = run_scenario(args.scenario, out_dir)
    result = summary(referral)
    print(f"escenario: {args.scenario}")
    print(f"estado final: {result['case_state']} "
          f"(Task.status {result['task_status']})")
    print(f"ServiceRequest: {result['service_request_status']}")
    print(f"citas: {result['appointments']}")
    print(f"encuentros: {result['encounters']}")
    print(f"notificaciones: {result['notifications']}; "
          f"entradas de historial: {result['history']}")
    print(f"violaciones de invariantes: {result['invariant_violations'] or 'ninguna'}")
    print(f"archivos: {len(written)} recursos + summary.json en {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
