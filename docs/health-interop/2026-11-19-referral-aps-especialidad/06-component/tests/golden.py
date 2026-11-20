"""Comparador de goldens: copias textuales de los JSON compilados por
SUSHI (`05-implementation-guide/fsh-generated/resources/`).

La comparación es por valor (el orden de las claves no importa; el
orden de los arrays sí). Las normalizaciones permitidas están
documentadas en `state.md` (Rulings) y se aplican SOLO a través de
`normalize`: nunca se edita el golden para que pase el test.
"""

import json
import os
from difflib import unified_diff

GOLDENS_DIR = os.path.join(os.path.dirname(__file__), "goldens")


def load_golden(name):
    """Carga un golden por nombre de archivo (sin `.json`)."""
    with open(os.path.join(GOLDENS_DIR, name + ".json"), encoding="utf-8") as fh:
        return json.load(fh)


def diff_dicts(actual, expected):
    """Devuelve un diff legible entre dos dicts JSON, o '' si son iguales."""
    actual_text = json.dumps(actual, indent=2, sort_keys=True, ensure_ascii=False)
    expected_text = json.dumps(expected, indent=2, sort_keys=True, ensure_ascii=False)
    if actual_text == expected_text:
        return ""
    return "\n".join(
        unified_diff(
            expected_text.splitlines(),
            actual_text.splitlines(),
            fromfile="golden",
            tofile="actual",
            lineterm="",
        )
    )


def assert_golden(testcase, actual, golden_name, normalize=None):
    """Compara `actual` (dict) con el golden `golden_name`.

    `normalize` es una función que transforma AMBOS lados antes de
    comparar (solo para las normalizaciones documentadas en `state.md`).
    """
    expected = load_golden(golden_name)
    if normalize is not None:
        actual = normalize(actual)
        expected = normalize(expected)
    diff = diff_dicts(actual, expected)
    testcase.assertEqual(diff, "", f"el recurso no coincide con el golden {golden_name}")
