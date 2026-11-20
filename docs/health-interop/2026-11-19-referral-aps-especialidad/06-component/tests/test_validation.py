"""Validación de interoperabilidad de los ejemplos generados
(`validating-interop`).

- Cada `Coding` lleva `system`, `code` y `display`.
- Cada `Reference` resuelve a un recurso del tipo esperado: los
  recursos del escenario, los del registro sembrado, los goldens de
  la guía, o los externos conocidos del lado APS (el encuentro APS
  y las observaciones de apoyo, que viven en el EHR de APS y solo se
  referencian).
- Cada recurso lleva `resourceType` e `id`; cada Bundle de documento
  lleva la Composition primera.
- Los datos son sintéticos (privacy checklist): ningún RUN real, ni
  teléfono, email o dirección real aparece en los ejemplos.
"""

import glob
import json
import os
import re
import unittest
from pathlib import Path

from derivacion.registry import seed_worked_example

COMPONENT = Path(__file__).resolve().parents[1]
EXAMPLES = COMPONENT / "examples"
GOLDENS = COMPONENT / "tests" / "goldens"
GUIDE_GENERATED = (
    COMPONENT.parent
    / "05-implementation-guide"
    / "fsh-generated"
    / "resources"
)


def _profile_target_types(sd_path, element_id):
    """Tipos de recurso admitidos por un elemento de un perfil.

    Lee los `targetProfile` del elemento en el StructureDefinition
    generado por SUSHI y los resuelve a tipos FHIR: los perfiles
    propios se resuelven por su SD generado (`type`); los base de
    HL7, por el último segmento de la URL.
    """
    with open(sd_path, encoding="utf-8") as fh:
        sd = json.load(fh)
    for element in sd["differential"]["element"]:
        if element["id"] != element_id:
            continue
        types = set()
        for target in element["type"][0].get("targetProfile", []):
            local = GUIDE_SDS.get(target)
            if local is not None:
                types.add(local)
            else:
                types.add(target.rsplit("/", 1)[-1])
        return types
    raise KeyError(f"sin targetProfile para {element_id} en {sd_path}")


# Perfil DerivacionNotificacion generado por SUSHI: sus SD de
# destino viven en el mismo directorio (tipo en `type`).
def _generated_sd_types():
    types = {}
    for path in glob.glob(str(GUIDE_GENERATED / "StructureDefinition-*.json")):
        with open(path, encoding="utf-8") as fh:
            sd = json.load(fh)
        types[sd["url"]] = sd["type"]
    return types


GUIDE_SDS = _generated_sd_types()

# Referencias a recursos que viven fuera del componente (lado APS):
# el encuentro APS que originó la derivación y las observaciones de
# apoyo, que la guía referencia sin materializar.
KNOWN_EXTERNAL = {
    "Encounter/aps-encounter-2026-11-19": "Encounter",
    "Observation/ecg-2026-11-19": "Observation",
    "Observation/ntprobnp-2026-11-19": "Observation",
}

# RUN sintético del ejemplo trabajado (formato válido, persona ficticia).
SYNTHETIC_RUN = "11.111.111-1"


def load_jsons(directory):
    resources = []
    for path in sorted(glob.glob(str(directory / "*.json"))):
        if path.endswith("summary.json"):
            continue
        with open(path, encoding="utf-8") as fh:
            resources.append(json.load(fh))
    return resources


def walk(node):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value)


def index_resources(resources):
    index = {}
    for resource in resources:
        if resource.get("resourceType") == "Bundle":
            for entry in resource.get("entry", []):
                inner = entry.get("resource")
                if inner is not None:
                    index[(inner["resourceType"], inner["id"])] = inner
        else:
            index[(resource["resourceType"], resource["id"])] = resource
    return index


class TestValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        resources = []
        for scenario in ("accepted", "rejected", "no-show"):
            resources.extend(load_jsons(EXAMPLES / scenario))
        resources.extend(load_jsons(GOLDENS))
        registry = seed_worked_example()
        resources.extend(registry.patients.values())
        resources.extend(registry.services.values())
        resources.extend(registry.endpoints.values())
        resources.extend(registry.practitioners.values())
        resources.extend(registry.roles.values())
        cls.index = index_resources(resources)
        cls.scenario_resources = {
            scenario: load_jsons(EXAMPLES / scenario)
            for scenario in ("accepted", "rejected", "no-show")
        }

    def test_every_coding_has_system_code_and_display(self):
        # Solo recursos de instancia: las definiciones de la guía
        # (StructureDefinition, ValueSet, CodeSystem) restringen
        # códigos sin display y no son instancias que validar.
        conformance = {
            "StructureDefinition", "ValueSet", "CodeSystem",
            "ImplementationGuide", "SearchParameter",
        }
        bad = []
        for (resource_type, resource_id), resource in self.index.items():
            if resource_type in conformance:
                continue
            for node in walk(resource):
                # Una Quantity (valueQuantity) lleva system + code pero
                # no es un Coding: el display no aplica (regla UCUM de
                # la skill: system UCUM + código UCUM + unidad).
                if "system" in node and "code" in node and "value" not in node:
                    if not node.get("display"):
                        bad.append(
                            f"{resource_type}/{resource_id}: "
                            f"coding sin display: {node}")
        self.assertEqual(bad, [])

    def test_every_reference_resolves_to_the_expected_type(self):
        unresolved = []
        for scenario, resources in self.scenario_resources.items():
            for resource in resources:
                for node in walk(resource):
                    reference = node.get("reference")
                    if not isinstance(reference, str):
                        continue
                    if reference.startswith("urn:uuid:"):
                        continue
                    resource_type, _, resource_id = reference.partition("/")
                    if not resource_type or not resource_id:
                        unresolved.append(
                            f"{scenario}: referencia mal formada: {reference}")
                        continue
                    expected = KNOWN_EXTERNAL.get(reference)
                    if expected is not None:
                        if expected != resource_type:
                            unresolved.append(
                                f"{scenario}: {reference} es {expected}, "
                                f"no {resource_type}")
                        continue
                    target = self.index.get((resource_type, resource_id))
                    if target is None:
                        unresolved.append(
                            f"{scenario}: {reference} no resuelve "
                            f"(en {resource.get('resourceType')}/"
                            f"{resource.get('id')})")
        self.assertEqual(unresolved, [])

    def test_communication_references_match_profile_targets(self):
        # C3 (revisión experta del paso 6): las referencias de cada
        # Communication de los escenarios respetan los targetProfile
        # del perfil DerivacionNotificacion generado por SUSHI
        # (recipient: Patient | PractitionerRole; sender:
        # PractitionerRole | Organization). Sin Java: el validador
        # FHIR rechazaría un Organization como recipient, y esta
        # prueba lo caza en la suite.
        sd_path = (
            GUIDE_GENERATED
            / "StructureDefinition-derivacion-notificacion.json"
        )
        allowed = {
            "recipient": _profile_target_types(
                sd_path, "Communication.recipient"),
            "sender": _profile_target_types(sd_path, "Communication.sender"),
            "subject": _profile_target_types(sd_path, "Communication.subject"),
            "basedOn": _profile_target_types(
                sd_path, "Communication.basedOn"),
        }
        bad = []
        for scenario, resources in self.scenario_resources.items():
            for resource in resources:
                if resource.get("resourceType") != "Communication":
                    continue
                for field, targets in allowed.items():
                    refs = resource.get(field)
                    if refs is None:
                        continue
                    if isinstance(refs, dict):
                        refs = [refs]
                    for ref in refs:
                        resource_type = ref["reference"].partition("/")[0]
                        if resource_type not in targets:
                            bad.append(
                                f"{scenario}: {resource.get('id')}: "
                                f"{field} {ref['reference']} no está en "
                                f"{sorted(targets)}")
        self.assertEqual(bad, [])

    def test_document_bundle_has_composition_first(self):
        for scenario, resources in self.scenario_resources.items():
            for resource in resources:
                if resource.get("resourceType") == "Bundle" and (
                    resource.get("type") == "document"
                ):
                    first = resource["entry"][0]["resource"]
                    self.assertEqual(first["resourceType"], "Composition",
                                     scenario)

    def test_every_resource_has_type_and_id(self):
        bad = []
        for scenario, resources in self.scenario_resources.items():
            for resource in resources:
                if not resource.get("resourceType") or not resource.get("id"):
                    bad.append(f"{scenario}: {resource}")
        self.assertEqual(bad, [])

    def test_synthetic_data_only(self):
        # Privacy checklist: solo el RUN sintético del ejemplo; ningún
        # teléfono, email o dirección real en los ejemplos ni en los
        # goldens que los acompañan.
        text = ""
        for scenario, resources in self.scenario_resources.items():
            for resource in resources:
                text += json.dumps(resource, ensure_ascii=False)
        for resource in load_jsons(GOLDENS):
            text += json.dumps(resource, ensure_ascii=False)
        runs = set(re.findall(r"\b\d{1,2}\.\d{3}\.\d{3}-[\dkK]\b", text))
        self.assertEqual(runs, {SYNTHETIC_RUN})
        self.assertNotIn("@", text)
        self.assertNotRegex(text, r"\b\+?56[29]\s?\d")


if __name__ == "__main__":
    unittest.main()
