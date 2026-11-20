# Reglas y retención - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* **Reglas y retención**

## Reglas y retención

### Reglas y retención

#### Reglas de evaluación (plazos SLA)

Cada plazo es una regla de evaluación con su ventana, su acción y su re-arme. Un incumplimiento de plazo dispara una escalada, nunca un cambio de estado (ver [Ciclo de vida](lifecycle.md)).

| | | | |
| :--- | :--- | :--- | :--- |
| R1 Plazo de aceptación | Creación + 5 días hábiles (2 si es urgente) | El hub escala a la especialidad y notifica a APS; sigue esperando (el ciclo vuelve a entrar en la espera) | La decisión (aceptar/rechazar) desarma la regla; un nuevo intento no existe — la derivación solo tiene una decisión de triaje |
| R2 Plazo de oferta de cita | Aceptación + 10 días hábiles | El hub escala a la especialidad y notifica a APS (h19) | La oferta desarma la regla |
| R3 Plazo de confirmación | Oferta + 3 días hábiles | El agendador persigue a la paciente (hasta 2 veces); tras la segunda persecución sin confirmar, la derivación vuelve al re-triaje de APS | La confirmación o el rechazo desarman la regla; cada oferta tiene su propio presupuesto de confirmación/persecución (los conteos se reinician por oferta) |
| R4 Plazo de contrareferencia | Encuentro + 5 días hábiles | El hub escala a la especialidad y notifica a APS (h20) | El envío de la contrareferencia desarma la regla; una contrareferencia que llega tarde se acepta igualmente (el plazo dispara escalada, no rechazo) |
| R5 Plazo de re-triaje | Rechazo (o retorno por fallo de agendamiento) + 5 días hábiles | El hub escala a APS | La decisión de re-triaje desarma la regla |

Las reglas de conteo (un re-oferta por rechazo, dos persecuciones por oferta, un re-agendamiento por derivación) viven como extensiones del Task (`offer-decline-count`, `offer-chase-count`, `rescheduling-count`) y las leen las puertas basadas en datos del BPMN.

#### Indicadores

| | | |
| :--- | :--- | :--- |
| Tiempo medio de aceptación | Creación → decisión de triaje (días hábiles), por servicio y prioridad | Detectar servicios con triaje lento |
| Tasa de rechazo | Derivaciones rechazadas / derivaciones creadas, por servicio y motivo | Detectar derivaciones mal dirigidas o con exámenes faltantes |
| Tiempo medio de oferta de cita | Aceptación → oferta (días hábiles) | Detectar cuellos de botella de agenda |
| Tasa de no-show | Primer no-show / citas reservadas; segundo no-show / re-agendamientos | Detectar pacientes que necesitan otro canal de contacto |
| Tiempo medio de contrareferencia | Encuentro → contrareferencia recibida (días hábiles) | Detectar cierres de ciclo lentos |
| Ciclos cerrados | Derivaciones`counter-referred`/ derivaciones creadas (por periodo) | La medida de continuidad de la atención del caso |

#### Plan de monitoreo

* **Frecuencia:** los indicadores se calculan cada mes, por servicio y por prioridad (routine / urgent).
* **Quién responde:** el operador del hub revisa las escaladas cada día hábil; el responsable de cada servicio responde a las escaladas de su servicio en el día hábil siguiente.
* **Fuera de horario:** las escaladas fuera de horario se registran y se atienden el siguiente día hábil; ningún plazo se cierra fuera de horario (los plazos son días hábiles).

#### Retención

* **Registros de flujo de trabajo (Task + historial Provenance):** el hub los retiene mientras la derivación esté abierta y 5 años tras su cierre (la política de registros de la red, spec §5). El hub no retiene el detalle clínico que enruta en tránsito.
* **Documentos clínicos (Composition + DocumentReference de la contrareferencia):** cada organización retiene su copia bajo su propia política de registros (spec §5).
* **Registros de auditoría (AuditEvent):** retención de auditoría de la red; los eventos son solo-añadir.
* La ventana de retención de cada clase de producto se registra una sola vez, aquí, por clase de producto.

