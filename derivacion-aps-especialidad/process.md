# Proceso (BPMN) - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* **Proceso (BPMN)**

## Proceso (BPMN)

### Proceso (BPMN)

El modelo BPMN validado del paso 2, en tres partes, con sus puntos de interoperabilidad. Los diagramas se muestran a tamaño nativo (2×) con desplazamiento y zoom; el SVG de cada parte está enlazado bajo su imagen. Las desviaciones de modelado conocidas están listadas en `02-bpmn-model.md`.

#### Parte A — Derivación y triaje

[SVG de la Parte A](02-bpmn-model-referral-triage.svg) · 52 formas / 43 flujos. Puntos: PI-0 creación y enrutado (m3, m11), PI-1 aceptación / rechazo (m4–m7). Carriles: APS doctor, APS admin, MPI, Hub operator, Triage clinician / specialist, Patient.

#### Parte B — Agendamiento y contrareferencia

[SVG de la Parte B](02-bpmn-model-scheduling-counterreferral.svg) · 65 formas / 59 flujos. Puntos: PI-2 agendamiento (h1–h3, h8, h9), PI-3 contrareferencia (h10, h11). Carriles: APS admin, APS doctor, Hub operator, Specialty scheduler, Specialist, Patient.

#### Parte C — Consulta de estado

[SVG de la Parte C](02-bpmn-model-status-query.svg) · 16 formas / 11 flujos. Punto: PI-4 consulta de estado (j1–j3, solo lectura). Carriles: APS doctor / admin, Hub operator.

#### Registro global de puntos de interoperabilidad

| | | |
| :--- | :--- | :--- |
| PI-0 Creación | m3 (APS → hub), m11 (hub → especialidad) | Creación de la derivación, resolución de identidad (OP-9), enrutado (OP-10) |
| PI-1 Aceptar / rechazar | m4–m7 (especialidad → hub → APS → paciente) | Decisión de triaje (OP-2), notificación (OP-12) |
| PI-2 Agendamiento | h1–h3, h8, h9 | Oferta / confirmación / reserva (OP-3), re-oferta / re-agendamiento (OP-4), asistencia / no-show (OP-5) |
| PI-3 Contrareferencia | h10, h11 | Envío del documento (OP-6), acuse de recibo |
| PI-4 Consulta de estado | j1–j3 | Consulta de solo lectura (OP-7) — "none applies" en IHE |

#### Desviaciones de modelado conocidas

* Las esperas de aceptación / confirmación son puertas basadas en eventos dibujadas como exclusivas (limitación del renderizador), nombradas "Decision received?".
* Los conteos son puertas basadas en datos que leen el registro de flujo de trabajo del hub.
* La cancelación es una fila de inicio por mensaje en las Partes A y B; no termina el flujo principal en curso (el registro del hub es la autoridad).
* Los flujos de mensaje h6/h7 terminan en puertas (desviación registrada).
* Las tareas de recepción de notificación terminan su rama sin evento de fin (convención: la recepción es el fin de la rama).

