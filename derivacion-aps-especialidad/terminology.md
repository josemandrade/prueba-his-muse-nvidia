# Terminología - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* **Terminología**

## Terminología

### Terminología

Servidor de terminología para expansión y validación: `https://tx.hl7chile.cl/r4` (el servidor que usan las guías del MINSAL). SNOMED CT: edición chilena (`http://snomed.info/sct/21000325107`), versión según la reporte el servidor al construir la guía. LOINC: versión según la reporte el servidor (LOINC 2.73 vista 2026-11-19). UCUM 2.0.1. ICD-10-CM: versión según la reporte el servidor al construir la guía.

#### CodeSystems y ValueSets locales

Cada lista local es un CodeSystem propio de la guía con su ValueSet; la guía no inventa un catálogo estándar para ninguna de ellas.

| | | | |
| :--- | :--- | :--- | :--- |
| [`DerivacionEstadoReferenciaCS`](CodeSystem-derivacion-estado-referencia.md) | [`DerivacionEstadoReferencia`](ValueSet-derivacion-estado-referencia.md) | `requested`,`received`,`accepted`,`rejected`,`scheduled`,`completed`,`counter-referred`,`no-show`,`cancelled` | [`DerivacionTarea.businessStatus`](StructureDefinition-derivacion-tarea.md) |
| [`DerivacionRolCS`](CodeSystem-derivacion-rol.md) | [`DerivacionRolVS`](ValueSet-derivacion-rol.md) | `aps-doctor`,`aps-admin`,`triage-clinician`,`specialty-scheduler`,`specialist`,`hub-operator` | [`DerivacionRol.code`](StructureDefinition-derivacion-rol.md) |
| [`DerivacionMotivoRechazoCS`](CodeSystem-derivacion-motivo-rechazo.md) | [`DerivacionMotivoRechazo`](ValueSet-derivacion-motivo-rechazo.md) | `missing-exam`,`wrong-specialty`,`capacity`(+ texto libre) | [`DerivacionTarea.statusReason`](StructureDefinition-derivacion-tarea.md) |
| [`DerivacionCanalCS`](CodeSystem-derivacion-canal.md) | [`DerivacionCanal`](ValueSet-derivacion-canal.md) | `phone`,`in-person`,`system-message` | [`DerivacionNotificacion.medium`](StructureDefinition-derivacion-notificacion.md) |
| [`DerivacionEspecialidadCS`](CodeSystem-derivacion-especialidad.md) | [`DerivacionEspecialidad`](ValueSet-derivacion-especialidad.md) | `cardiologia`(el catálogo lo versiona la red; el ejemplo trabajado es cardiología) | [`DerivacionSolicitud.code`](StructureDefinition-derivacion-solicitud.md),[`DerivacionServicio.type`](StructureDefinition-derivacion-servicio.md) |
| [`DerivacionTaskCodeCS`](CodeSystem-derivacion-task-code.md) | [`DerivacionTaskCode`](ValueSet-derivacion-task-code.md) | `referral-workflow` | [`DerivacionTarea.code`](StructureDefinition-derivacion-tarea.md) |
| [`DerivacionResultadoEntregaCS`](CodeSystem-derivacion-resultado-entrega.md) | [`DerivacionResultadoEntrega`](ValueSet-derivacion-resultado-entrega.md) | `delivered`,`failed` | Extensión`DerivacionDeliveryOutcome`en[`DerivacionNotificacion`](StructureDefinition-derivacion-notificacion.md) |
| [`DerivacionBaseCruceCS`](CodeSystem-derivacion-base-cruce.md) | [`DerivacionBaseCruce`](ValueSet-derivacion-base-cruce.md) | `identifier`,`demographics` | Extensión`DerivacionMatchBasis`(contexto Patient; cruce de identidad del MPI) |

#### Terminologías externas

| | | | |
| :--- | :--- | :--- | :--- |
| Motivo de derivación | SNOMED CT | `http://snomed.info/sct` | 84114007 "Heart failure (disorder)" (ejemplo trabajado: sospecha de insuficiencia cardiaca) |
| Diagnóstico (contrareferencia) | ICD-10-CM (primario) + SNOMED CT (segunda codificación) | `http://hl7.org/fhir/sid/icd-10-cm`,`http://snomed.info/sct` | I50.22 "Chronic systolic (congestive) heart failure" (facturable, 5 caracteres) + 417996009 "Systolic heart failure". Chile usa la CIE-10 de la OMS, donde no existe un código específico de insuficiencia sistólica (I50 solo tiene I50.0 / I50.1 / I50.9) — la segunda codificación SNOMED CT lleva el significado preciso. |
| Exámenes / resultados | LOINC | `http://loinc.org` | ECG: 11524-6 "EKG study" (Active, v2.72). NT-proBNP: 33762-6 (Active, v2.73, pg/mL UCUM; miembro del panel 55405-5). |
| Tipo de documento de contrareferencia | LOINC | `http://loinc.org` | 11488-4 "Consult note" (Active, v2.73); variante de cardiología: 34099-2 "Cardiology Consult Note". |
| Tipo de documento de derivación (solo referencia) | LOINC | `http://loinc.org` | 57133-1 "Referral Note" (Active, v2.67): el tipo de documento para una derivación que viaja como documento. En este diseño la derivación viaja como recursos, no como documento. |
| Prioridad | R4`RequestPriority`(Required) | `http://hl7.org/fhir/request-priority` | `routine`/`urgent`— los valores R4 cubren el caso; no hay ValueSet local. |
| Clase de encuentro | v3`ActEncounterCode`(Extensible) | `http://terminology.hl7.org/CodeSystem/v3-ActCode` | `AMB`(ambulatorio). |
| Categoría de notificación | R4`CommunicationCategory`(Example) | `http://terminology.hl7.org/CodeSystem/communication-category` | `notification`. |
| Unidades | UCUM | `http://unitsofmeasure.org` | UCUM 2.0.1 (p. ej. pg/mL para NT-proBNP). |

#### Sistemas de identificadores (ejemplos sintéticos)

| | |
| :--- | :--- |
| Clave MPI | `http://mpi.red.example.org` |
| RUN | `http://www.registrocivil.cl/run` |
| Identificador de la derivación (APS) | `http://aps.losaromos.example.org/referral` |
| Identificador del servicio | `http://especialidad.example.org/service` |
| Identificador de la cita | `http://especialidad.example.org/appointment` |
| Identificador del encuentro | `http://especialidad.example.org/encounter` |
| Identificador de la contrareferencia | `http://especialidad.example.org/counter-referral` |
| Identificador de la notificación | `http://aps.losaromos.example.org/notification` |

Todos los identificadores de los ejemplos son sintéticos. Los dominios `example.org` son sistemas de identificador de ejemplo, no el canonical de la guía (que es `https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/`).

