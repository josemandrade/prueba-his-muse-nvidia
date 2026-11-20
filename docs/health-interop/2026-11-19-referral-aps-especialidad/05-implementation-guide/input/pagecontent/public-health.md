# Base legal y reporte

## Base legal por punto

| PI | Base legal |
|---|---|
| PI-0 Creación | La relación asistencial cubre el intercambio de los datos de la derivación con la especialidad solicitada (spec §4, Q7). No se pide un consentimiento separado; ningún artefacto de consentimiento viaja (por eso BPPC/PCF se apartan — ver [Relación con IHE](ihe.html)). |
| PI-1 Aceptación / rechazo | La misma relación asistencial. La decisión de triaje es un acto clínico de la especialidad sobre la derivación recibida. |
| PI-2 Agendamiento | La misma relación asistencial. La oferta de cita a la paciente y su confirmación son parte de la atención derivada. |
| PI-3 Contrareferencia | La misma relación asistencial. La contrareferencia es el documento clínico que cierra el ciclo de atención. |
| PI-4 Consulta de estado | La misma relación asistencial. La consulta es de solo lectura sobre el registro de flujo de trabajo que el hub guarda. |

El paciente decide si acepta la derivación en sí en la creación (C8 del
caso): si la rechaza, no se crea ninguna derivación y APS registra la
decisión y el motivo localmente (entidad 12, sin equivalente FHIR).

## Reporte desidentificado e indicadores agregados

Los indicadores de [Reglas y retención](rules.html) se reportan
desidentificados y agregados:

- **Método de desidentificación:** los informes agregados no llevan
  identificadores de paciente (ni RUN, ni clave MPI, ni nombre); las
  cohortes se agrupan por servicio, prioridad y periodo.
- **Supresión de celdas pequeñas:** una celda con menos de 5 derivaciones
  no se publica (se muestra como "n < 5").
- **Periodo:** mensual, por servicio y prioridad.

| Medida | Población | Denominador | Numerador | Estratificador | Periodo |
|---|---|---|---|---|---|
| Tiempo medio de aceptación | Derivaciones creadas | Derivaciones con decisión | Suma de días hábiles creación → decisión | Servicio, prioridad | Mensual |
| Tasa de rechazo | Derivaciones creadas | Derivaciones creadas | Derivaciones rechazadas | Servicio, motivo | Mensual |
| Tiempo medio de oferta | Derivaciones aceptadas | Derivaciones aceptadas | Suma de días hábiles aceptación → oferta | Servicio | Mensual |
| Tasa de no-show | Citas reservadas | Citas reservadas | Primeros no-show | Servicio | Mensual |
| Tiempo medio de contrareferencia | Encuentros terminados | Encuentros terminados | Suma de días hábiles encuentro → contrareferencia | Servicio | Mensual |
| Ciclos cerrados | Derivaciones creadas | Derivaciones creadas | Derivaciones `counter-referred` | Servicio | Mensual |

No hay medicamentos en este caso, así que no hay página de medicamentos
controlados.
