"""Tests de OP-11 (suscripción a los cambios de estado).

Fuente: operations.md (OP-11): `criteria =
"Task?focus:ServiceRequest.identifier={referral-id}"`, `channel.type
= rest-hook`, `channel.payload = application/fhir+json`. No hay
golden de Subscription en la guía: el builder sigue el texto de
OP-11 tal cual.
"""

import unittest

from derivacion.builders import build_subscription
from derivacion.registry import seed_worked_example
from derivacion.workflow import Referral, WorkflowError
from tests.test_op04 import CREATED, ROUTED, dt, make_accepted

ENDPOINT = "https://aps.losaromos.example.org/fhir/r4/subscription/derivacion"


def make_received():
    """Una derivación recibida por el hub, antes del triaje."""
    registry = seed_worked_example()
    referral = Referral.create(
        registry, "REF-2026-0001", "maria-gonzalez", "rol-medico-aps",
        "cardiologia", "84114007", "routine", authored_on=CREATED,
        now=CREATED)
    referral.route(now=ROUTED)
    return referral


class TestSubscriptionBuilder(unittest.TestCase):
    def test_subscription_follows_op11(self):
        subscription = build_subscription(
            resource_id="suscripcion-ref-2026-0001",
            referral_id="REF-2026-0001",
            endpoint=ENDPOINT,
        )
        self.assertEqual(subscription["resourceType"], "Subscription")
        self.assertEqual(subscription["status"], "active")
        self.assertEqual(
            subscription["criteria"],
            "Task?focus:ServiceRequest.identifier=REF-2026-0001")
        self.assertEqual(subscription["channel"]["type"], "rest-hook")
        self.assertEqual(subscription["channel"]["endpoint"], ENDPOINT)
        self.assertEqual(subscription["channel"]["payload"],
                         "application/fhir+json")


class TestSubscribeWorkflow(unittest.TestCase):
    def test_subscriber_is_notified_on_each_task_transition(self):
        referral = make_accepted()
        subscription = referral.subscribe(ENDPOINT, now=dt(2026, 11, 21, 10, 0))
        self.assertEqual(len(referral.subscriptions), 1)
        referral.offer_appointment(
            "slot-cardiologia-1", "schedule-cardiologia",
            dt(2026, 12, 2, 10, 0), dt(2026, 12, 2, 10, 30),
            now=dt(2026, 11, 24, 11, 0))
        # La oferta no mueve el Task: no hay notificación.
        self.assertEqual(subscription["notifications"], [])
        referral.respond_to_offer("accepted", now=dt(2026, 11, 25, 9, 0))
        referral.book_appointment(now=dt(2026, 11, 25, 10, 0))
        # La reserva sí mueve el Task (accepted → scheduled).
        self.assertEqual(
            [n["state"] for n in subscription["notifications"]],
            ["scheduled"])

    def test_unsubscribe_stops_delivery(self):
        referral = make_received()
        subscription = referral.subscribe(ENDPOINT, now=dt(2026, 11, 21, 10, 0))
        referral.unsubscribe(subscription["id"], now=dt(2026, 11, 22, 9, 0))
        self.assertEqual(subscription["status"], "off")
        referral.triage("rejected", now=dt(2026, 11, 22, 10, 0),
                        reason_code="capacity")
        self.assertEqual(subscription["notifications"], [])

    def test_unsubscribe_unknown_id_is_forbidden(self):
        referral = make_accepted()
        with self.assertRaises(WorkflowError):
            referral.unsubscribe("suscripcion-inexistente",
                                 now=dt(2026, 11, 22, 9, 0))

    def test_two_subscribers_both_notified(self):
        referral = make_received()
        first = referral.subscribe(ENDPOINT, now=dt(2026, 11, 21, 10, 0))
        second = referral.subscribe(
            "https://especialidad.example.org/fhir/r4/subscription/derivacion",
            now=dt(2026, 11, 21, 10, 0))
        referral.triage("rejected", now=dt(2026, 11, 22, 10, 0),
                        reason_code="capacity")
        self.assertEqual(len(first["notifications"]), 1)
        self.assertEqual(len(second["notifications"]), 1)
        self.assertEqual(first["notifications"][0]["state"], "rejected")

    def test_exported_subscription_has_no_internal_keys(self):
        # C4 (revisión experta): la suscripción lleva contabilidad
        # interna (`_active`, `notifications`) que no es FHIR; al
        # exportar (all_resources → CLI) se vuelca sin esas claves,
        # aunque en memoria la contabilidad siga funcionando.
        from derivacion.scenarios import all_resources
        referral = make_accepted()
        referral.subscribe(ENDPOINT, now=dt(2026, 11, 21, 10, 0))
        referral.offer_appointment(
            "slot-cardiologia-1", "schedule-cardiologia",
            dt(2026, 12, 2, 10, 0), dt(2026, 12, 2, 10, 30),
            now=dt(2026, 11, 24, 11, 0))
        referral.respond_to_offer("accepted", now=dt(2026, 11, 25, 9, 0))
        referral.book_appointment(now=dt(2026, 11, 25, 10, 0))
        exported = [r for r in all_resources(referral)
                    if r["resourceType"] == "Subscription"]
        self.assertEqual(len(exported), 1)
        self.assertNotIn("_active", exported[0])
        self.assertNotIn("notifications", exported[0])
        self.assertEqual(exported[0]["status"], "active")
        self.assertEqual(exported[0]["criteria"],
                         "Task?focus:ServiceRequest.identifier=REF-2026-0001")


if __name__ == "__main__":
    unittest.main()
