# Recursos

El grafo de recursos de la propuesta FHIR (paso 4), con el `Task` en el
centro y el `Bundle` como marco. Las flechas son referencias FHIR; la
etiqueta es el elemento que lleva la referencia.

<div style="overflow-x: auto; border: 1px solid #ccc; padding: 4px;">
<img src="04-fhir-proposal-graph.png" alt="Grafo de recursos FHIR — Task en el centro, Bundle como marco" style="max-width: none; width: 2840px;" />
</div>

[SVG del grafo](04-fhir-proposal-graph.svg) · 12 nodos · 0 aristas a
través de un nodo · 2 cruces en ángulo recto.

## Lectura del grafo

- **Centro: `Task` (`DerivacionTarea`).** Lleva el estado del caso en
  `businessStatus` (9 estados) y apunta a la solicitud con `focus`.
- **La derivación viaja como recursos** (Bundle de transacción PI-0:
  `ServiceRequest` + `Task`); **la contrareferencia viaja como
  documento** (Bundle de documento PI-3: `Composition` primera entrada +
  `DocumentReference` + `Condition` + `CarePlan`).
- **`Encounter.appointment` → `Appointment`**: la flecha apunta del
  encuentro a la cita (la referencia la lleva el encuentro).
- **`Communication.basedOn` → `Task`** es la clave de unión de las
  notificaciones; **`Composition.section.entry`** enlaza el diagnóstico y
  el plan al documento de contrareferencia.
- Los recursos de apoyo (`Practitioner` / `PractitionerRole`,
  `Organization` / `HealthcareService` / `Location` / `Endpoint`,
  `Slot` / `Schedule`, `Observation`, `AppointmentResponse`) no tienen
  perfil propio: se usan como recursos base R4.

La lista completa de perfiles está en [Perfiles](profiles.html); el
mapeo campo a campo, en [Mapeo de datos](mapping.html).
