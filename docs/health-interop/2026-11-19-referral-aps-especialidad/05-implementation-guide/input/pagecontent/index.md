# Derivación APS → especialidad con contrareferencia

Guía de implementación de prueba (FHIR R4, datos sintéticos) para la
derivación de un paciente desde atención primaria (APS) a una especialidad,
con contrareferencia de vuelta a APS. Construida con
health-interop-superpowers v0.39.0 a partir del caso de uso validado
2026-11-19 (`01-use-case-spec.md`), el modelo BPMN validado
(`02-bpmn-model.md`), las entidades y datos validados
(`03-entities-data.md`) y la propuesta FHIR validada
(`04-fhir-proposal.md` + `04-mapping-table.md`).

## El problema clínico

Un médico de APS identifica un problema de salud que excede la capacidad
resolutiva de APS y debe ser evaluado por un especialista. Hoy la derivación
viaja en papel, formulario, teléfono o sistemas desconectados, sin un ciclo
de retorno fiable: APS no sabe si la especialidad aceptó la derivación,
cuándo es la cita, si el paciente asistió o qué decidió el especialista.
Las derivaciones se pierden, los pacientes esperan sin información y la
contrareferencia — el diagnóstico, el plan y las indicaciones de seguimiento
que el especialista debe devolver a APS — muchas veces nunca llega,
rompiendo la continuidad de la atención.

Este caso construye el ciclo cerrado: APS crea la derivación, la especialidad
la acepta o la rechaza, agenda y atiende, y devuelve una contrareferencia;
APS sigue el estado de la derivación en cualquier momento y recupera el
resultado. El flujo es longitudinal (días a semanas entre pasos) y
multi-encuentro (una visita en APS y una visita en la especialidad), con una
máquina de estados explícita. Es un caso de solicitud y flujo de trabajo, no
de notificación de episodio: el estado de la derivación es, la mayor parte
del tiempo, el dato que más necesita APS.

## Usuarios, roles y departamentos

| Rol | Departamento / Organización | Qué hace |
|---|---|---|
| Médico APS | APS (CESFAM) | Identifica la necesidad, crea la derivación, recibe la contrareferencia, continúa el seguimiento en APS |
| Administrativo APS | APS (CESFAM) | Registra y sigue la derivación, informa al paciente (creación, aceptación/rechazo, resultado de la contrareferencia), es notificado de la oferta de cita, recupera la contrareferencia |
| Operador del hub de derivación | Hub de derivación | Recibe la derivación, la enruta al servicio de especialidad, guarda el estado, responde consultas de estado, escala en timeout |
| Agendador de especialidad | Servicio de especialidad (p. ej. cardiología) | Reserva y re-agenda la cita, ofrece la cita al paciente, persigue una oferta sin confirmar |
| Clínico de triaje | Servicio de especialidad | Acepta la derivación (nombrando servicio/profesional) o la rechaza con un motivo |
| Especialista | Servicio de especialidad | Atiende al paciente, registra diagnóstico y plan, emite la contrareferencia |
| Paciente | — | Recibe notificaciones, asiste a la cita; decide si acepta la derivación, si asiste y si acepta una re-cita |
| MPI | Master Patient Index (sistema) | Resuelve la identidad del paciente entre organizaciones (sin decisiones clínicas) |

## Puntos de interoperabilidad

| PI | Nombre | Flujo |
|---|---|---|
| PI-0 | Creación y envío de la derivación | APS → hub → especialidad |
| PI-1 | Aceptación / rechazo | Especialidad → hub → APS |
| PI-2 | Agendamiento (oferta, confirmación, reserva) | Especialidad ↔ paciente, vía hub |
| PI-3 | Retorno de la contrareferencia | Especialidad → hub → APS |
| PI-4 | Consulta de estado (solo lectura) | APS → hub → APS |

El proceso completo está en [Proceso (BPMN)](process.html); los recursos y
sus referencias, en [Diagrama de recursos](resources.html); las operaciones
en cada punto, en [Operaciones](operations.html); los diagramas de secuencia,
en [Diagramas de secuencia](sequences.html).

## Perfiles

La guía define sus propios perfiles (`Derivacion*`) sobre los recursos base
de FHIR R4 — no transcribe los perfiles de ninguna otra guía. La lista
completa, con sus restricciones y su terminología, está en
[Perfiles](profiles.html). El recurso que lleva el estado del flujo de
trabajo es el `Task` (`DerivacionTarea`): una derivación es una solicitud
(`ServiceRequest`) más un registro de estado (`Task`), y el estado vive en
el `Task`, no en el estado de la solicitud.

## Ejemplo trabajado

María González, 58 años, RUN sintético 11.111.111-1, CESFAM Los Aromos →
cardiología, sospecha de insuficiencia cardiaca (disnea de esfuerzo, edema
de tobillos). Todos los ejemplos de esta guía son sintéticos y validan
contra sus perfiles.

## Estado

Guía de prueba, versión 0.1.0, estado `draft`, FHIR R4 4.0.1. Canonical:
`https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/`. La única
dependencia es `hl7.fhir.r4.core 4.0.1`.
