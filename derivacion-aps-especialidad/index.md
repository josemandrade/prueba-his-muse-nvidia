# Derivación APS → especialidad - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* **Derivación APS → especialidad**

## Derivación APS → especialidad

| | |
| :--- | :--- |
| *Official URL*:https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/ImplementationGuide/hl7.fhir.uv.test.derivacion-aps-especialidad | *Version*:0.1.0 |
| Draft as of 2026-11-20 | *Computable Name*:DerivacionAPSEspecialidad |

### Derivación APS → especialidad con contrareferencia

Guía de implementación de prueba (FHIR R4, datos sintéticos) para la derivación de un paciente desde atención primaria (APS) a una especialidad, con contrareferencia de vuelta a APS. Construida con health-interop-superpowers v0.39.0 a partir del caso de uso validado 2026-11-19 (`01-use-case-spec.md`), el modelo BPMN validado (`02-bpmn-model.md`), las entidades y datos validados (`03-entities-data.md`) y la propuesta FHIR validada (`04-fhir-proposal.md` + `04-mapping-table.md`).

#### El problema clínico

Un médico de APS identifica un problema de salud que excede la capacidad resolutiva de APS y debe ser evaluado por un especialista. Hoy la derivación viaja en papel, formulario, teléfono o sistemas desconectados, sin un ciclo de retorno fiable: APS no sabe si la especialidad aceptó la derivación, cuándo es la cita, si el paciente asistió o qué decidió el especialista. Las derivaciones se pierden, los pacientes esperan sin información y la contrareferencia — el diagnóstico, el plan y las indicaciones de seguimiento que el especialista debe devolver a APS — muchas veces nunca llega, rompiendo la continuidad de la atención.

Este caso construye el ciclo cerrado: APS crea la derivación, la especialidad la acepta o la rechaza, agenda y atiende, y devuelve una contrareferencia; APS sigue el estado de la derivación en cualquier momento y recupera el resultado. El flujo es longitudinal (días a semanas entre pasos) y multi-encuentro (una visita en APS y una visita en la especialidad), con una máquina de estados explícita. Es un caso de solicitud y flujo de trabajo, no de notificación de episodio: el estado de la derivación es, la mayor parte del tiempo, el dato que más necesita APS.

#### Usuarios, roles y departamentos

| | | |
| :--- | :--- | :--- |
| Médico APS | APS (CESFAM) | Identifica la necesidad, crea la derivación, recibe la contrareferencia, continúa el seguimiento en APS |
| Administrativo APS | APS (CESFAM) | Registra y sigue la derivación, informa al paciente (creación, aceptación/rechazo, resultado de la contrareferencia), es notificado de la oferta de cita, recupera la contrareferencia |
| Operador del hub de derivación | Hub de derivación | Recibe la derivación, la enruta al servicio de especialidad, guarda el estado, responde consultas de estado, escala en timeout |
| Agendador de especialidad | Servicio de especialidad (p. ej. cardiología) | Reserva y re-agenda la cita, ofrece la cita al paciente, persigue una oferta sin confirmar |
| Clínico de triaje | Servicio de especialidad | Acepta la derivación (nombrando servicio/profesional) o la rechaza con un motivo |
| Especialista | Servicio de especialidad | Atiende al paciente, registra diagnóstico y plan, emite la contrareferencia |
| Paciente | — | Recibe notificaciones, asiste a la cita; decide si acepta la derivación, si asiste y si acepta una re-cita |
| MPI | Master Patient Index (sistema) | Resuelve la identidad del paciente entre organizaciones (sin decisiones clínicas) |

#### Puntos de interoperabilidad

| | | |
| :--- | :--- | :--- |
| PI-0 | Creación y envío de la derivación | APS → hub → especialidad |
| PI-1 | Aceptación / rechazo | Especialidad → hub → APS |
| PI-2 | Agendamiento (oferta, confirmación, reserva) | Especialidad ↔ paciente, vía hub |
| PI-3 | Retorno de la contrareferencia | Especialidad → hub → APS |
| PI-4 | Consulta de estado (solo lectura) | APS → hub → APS |

El proceso completo está en [Proceso (BPMN)](process.md); los recursos y sus referencias, en [Diagrama de recursos](resources.md); las operaciones en cada punto, en [Operaciones](operations.md); los diagramas de secuencia, en [Diagramas de secuencia](sequences.md).

#### Perfiles

La guía define sus propios perfiles (`Derivacion*`) sobre los recursos base de FHIR R4 — no transcribe los perfiles de ninguna otra guía. La lista completa, con sus restricciones y su terminología, está en [Perfiles](profiles.md). El recurso que lleva el estado del flujo de trabajo es el `Task` (`DerivacionTarea`): una derivación es una solicitud (`ServiceRequest`) más un registro de estado (`Task`), y el estado vive en el `Task`, no en el estado de la solicitud.

#### Ejemplo trabajado

María González, 58 años, RUN sintético 11.111.111-1, CESFAM Los Aromos → cardiología, sospecha de insuficiencia cardiaca (disnea de esfuerzo, edema de tobillos). Todos los ejemplos de esta guía son sintéticos y validan contra sus perfiles.

#### Estado

Guía de prueba, versión 0.1.0, estado `draft`, FHIR R4 4.0.1. Canonical: `https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/`. La única dependencia es `hl7.fhir.r4.core 4.0.1`.



## Resource Content

```json
{
  "resourceType" : "ImplementationGuide",
  "id" : "hl7.fhir.uv.test.derivacion-aps-especialidad",
  "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/ImplementationGuide/hl7.fhir.uv.test.derivacion-aps-especialidad",
  "version" : "0.1.0",
  "name" : "DerivacionAPSEspecialidad",
  "title" : "Derivación APS → especialidad con contrareferencia",
  "status" : "draft",
  "date" : "2026-11-20T12:49:56+00:00",
  "description" : "Guía de implementación de prueba para la derivación de un paciente desde atención primaria (APS) a una especialidad, con contrareferencia de vuelta a APS. Un caso de uso clínico con su flujo BPMN, sus perfiles FHIR R4 propios y sus operaciones en cada punto de interoperabilidad. Datos sintéticos.",
  "packageId" : "hl7.fhir.uv.test.derivacion-aps-especialidad",
  "license" : "CC0-1.0",
  "fhirVersion" : ["4.0.1"],
  "dependsOn" : [{
    "id" : "hl7tx",
    "extension" : [{
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/implementationguide-dependency-comment",
      "valueMarkdown" : "Automatically added as a dependency - all IGs depend on HL7 Terminology"
    }],
    "uri" : "http://terminology.hl7.org/ImplementationGuide/hl7.terminology",
    "packageId" : "hl7.terminology.r4",
    "version" : "7.5.0"
  },
  {
    "id" : "hl7ext",
    "extension" : [{
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/implementationguide-dependency-comment",
      "valueMarkdown" : "Automatically added as a dependency - all IGs depend on the HL7 Extension Pack"
    }],
    "uri" : "http://hl7.org/fhir/extensions/ImplementationGuide/hl7.fhir.uv.extensions",
    "packageId" : "hl7.fhir.uv.extensions.r4",
    "version" : "5.4.0"
  },
  {
    "id" : "hl7_fhir_r4_core",
    "uri" : "http://hl7.org/fhir",
    "packageId" : "hl7.fhir.r4.core",
    "version" : "4.0.1"
  }],
  "definition" : {
    "extension" : [{
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-internal-dependency",
      "valueCode" : "hl7.fhir.uv.tools.r4#1.3.0"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "copyrightyear"
      },
      {
        "url" : "value",
        "valueString" : "2026+"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "releaselabel"
      },
      {
        "url" : "value",
        "valueString" : "CI Build"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "autoload-resources"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "path-liquid"
      },
      {
        "url" : "value",
        "valueString" : "template/liquid"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "path-liquid"
      },
      {
        "url" : "value",
        "valueString" : "input/liquid"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "path-qa"
      },
      {
        "url" : "value",
        "valueString" : "temp/qa"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "path-temp"
      },
      {
        "url" : "value",
        "valueString" : "temp/pages"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "path-output"
      },
      {
        "url" : "value",
        "valueString" : "output"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "path-suppressed-warnings"
      },
      {
        "url" : "value",
        "valueString" : "input/ignoreWarnings.txt"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "path-history"
      },
      {
        "url" : "value",
        "valueString" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/history.html"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "template-html"
      },
      {
        "url" : "value",
        "valueString" : "template-page.html"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "template-md"
      },
      {
        "url" : "value",
        "valueString" : "template-page-md.html"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "apply-contact"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "apply-context"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "apply-copyright"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "apply-jurisdiction"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "apply-license"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "apply-publisher"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "apply-version"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "apply-wg"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "active-tables"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "fmm-definition"
      },
      {
        "url" : "value",
        "valueString" : "http://hl7.org/fhir/versions.html#maturity"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "propagate-status"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "excludelogbinaryformat"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    },
    {
      "extension" : [{
        "url" : "code",
        "valueCode" : "tabbed-snapshots"
      },
      {
        "url" : "value",
        "valueString" : "true"
      }],
      "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-parameter"
    }],
    "resource" : [{
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "PractitionerRole"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "PractitionerRole-rol-admin-aps.html"
      }],
      "reference" : {
        "reference" : "PractitionerRole/rol-admin-aps"
      },
      "name" : "Administrativo APS en la derivación REF-2026-0001",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-rol"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Schedule"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Schedule-schedule-cardiologia.html"
      }],
      "reference" : {
        "reference" : "Schedule/schedule-cardiologia"
      },
      "name" : "Agenda de cardiología",
      "exampleBoolean" : true
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "PractitionerRole"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "PractitionerRole-rol-agendador.html"
      }],
      "reference" : {
        "reference" : "PractitionerRole/rol-agendador"
      },
      "name" : "Agendador en la derivación REF-2026-0001",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-rol"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:extension"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-match-basis.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-match-basis"
      },
      "name" : "Base del cruce de identidad",
      "description" : "Cómo se estableció el cruce de identidad en el MPI: identifier | demographics.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "ValueSet"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "ValueSet-derivacion-base-cruce.html"
      }],
      "reference" : {
        "reference" : "ValueSet/derivacion-base-cruce"
      },
      "name" : "Base del cruce de identidad",
      "description" : "Bases posibles del cruce de identidad en el MPI.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "CodeSystem"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "CodeSystem-derivacion-base-cruce.html"
      }],
      "reference" : {
        "reference" : "CodeSystem/derivacion-base-cruce"
      },
      "name" : "Base del cruce de identidad",
      "description" : "Cómo se estableció el cruce de identidad en el MPI (lista local).",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Bundle"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Bundle-bundle-pi3-ref-2026-0001.html"
      }],
      "reference" : {
        "reference" : "Bundle/bundle-pi3-ref-2026-0001"
      },
      "name" : "Bundle de documento PI-3 (contrareferencia)",
      "description" : "La contrareferencia viaja como documento FHIR: la Composition es la primera entrada (OP-6).",
      "exampleBoolean" : true
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Bundle"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Bundle-bundle-pi0-ref-2026-0001.html"
      }],
      "reference" : {
        "reference" : "Bundle/bundle-pi0-ref-2026-0001"
      },
      "name" : "Bundle de transacción PI-0 (creación de la derivación)",
      "description" : "La derivación viaja como recursos: ServiceRequest + Task en un Bundle de tipo transaction (OP-1).",
      "exampleBoolean" : true
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:extension"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-preferred-contact-channel.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-preferred-contact-channel"
      },
      "name" : "Canal de contacto preferido",
      "description" : "Canal preferido del paciente para las notificaciones: phone | in-person | system-message (ValueSet DerivacionCanal).",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "ValueSet"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "ValueSet-derivacion-canal.html"
      }],
      "reference" : {
        "reference" : "ValueSet/derivacion-canal"
      },
      "name" : "Canal de notificación",
      "description" : "Canales de notificación de la derivación.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "CodeSystem"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "CodeSystem-derivacion-canal.html"
      }],
      "reference" : {
        "reference" : "CodeSystem/derivacion-canal"
      },
      "name" : "Canal de notificación",
      "description" : "Canales por los que se envía una notificación (lista local; el caso no fija un canal por notificación).",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Organization"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Organization-org-cesfam-los-aromos.html"
      }],
      "reference" : {
        "reference" : "Organization/org-cesfam-los-aromos"
      },
      "name" : "CESFAM Los Aromos",
      "exampleBoolean" : true
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-cita.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-cita"
      },
      "name" : "Cita de la derivación",
      "description" : "La oferta y la reserva de la cita de especialidad. Perfil propio de esta guía, sobre el recurso base Appointment de FHIR R4. La decisión del paciente vive en el AppointmentResponse, no en la cita; una cita cancelada o no asistida nunca se reutiliza.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Appointment"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Appointment-cita-ref-2026-0001.html"
      }],
      "reference" : {
        "reference" : "Appointment/cita-ref-2026-0001"
      },
      "name" : "Cita de la derivación REF-2026-0001 (proposed)",
      "description" : "La oferta de cita (PI-2): propuesta, aún sin confirmar por la paciente.",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-cita"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "PractitionerRole"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "PractitionerRole-rol-triaje.html"
      }],
      "reference" : {
        "reference" : "PractitionerRole/rol-triaje"
      },
      "name" : "Clínico de triaje en la derivación REF-2026-0001",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-rol"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:extension"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-match-confidence.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-match-confidence"
      },
      "name" : "Confianza del cruce de identidad",
      "description" : "Confianza del cruce de identidad del MPI, de 0 a 1. Opcional.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Location"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Location-location-cardiologia.html"
      }],
      "reference" : {
        "reference" : "Location/location-cardiologia"
      },
      "name" : "Consulta de cardiología",
      "exampleBoolean" : true
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:extension"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-offer-chase-count.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-offer-chase-count"
      },
      "name" : "Conteo de persecuciones de esta oferta",
      "description" : "Número de veces que el agendador ha perseguido una oferta sin confirmar (0–2). Se reinicia por oferta (N5).",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:extension"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-rescheduling-count.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-rescheduling-count"
      },
      "name" : "Conteo de re-agendamientos",
      "description" : "Número de re-agendamientos de esta derivación (0–1). No se reinicia: un solo re-agendamiento por derivación.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:extension"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-offer-decline-count.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-offer-decline-count"
      },
      "name" : "Conteo de rechazos de esta oferta",
      "description" : "Número de veces que el paciente ha rechazado esta oferta (0–2). Se reinicia por oferta (N5).",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-contrareferencia.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-contrareferencia"
      },
      "name" : "Contrareferencia",
      "description" : "El documento clínico de vuelta del especialista a APS: diagnóstico, plan, indicaciones de seguimiento y plan de seguimiento para APS. Perfil propio de esta guía, sobre el recurso base Composition de FHIR R4.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Composition"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Composition-contrareferencia-ref-2026-0001.html"
      }],
      "reference" : {
        "reference" : "Composition/contrareferencia-ref-2026-0001"
      },
      "name" : "Contrareferencia REF-2026-0001",
      "description" : "El documento de vuelta del especialista a APS (PI-3).",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-contrareferencia"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "ValueSet"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "ValueSet-derivacion-task-code.html"
      }],
      "reference" : {
        "reference" : "ValueSet/derivacion-task-code"
      },
      "name" : "Código de la tarea de derivación",
      "description" : "Códigos de Task de esta guía.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "CodeSystem"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "CodeSystem-derivacion-task-code.html"
      }],
      "reference" : {
        "reference" : "CodeSystem/derivacion-task-code"
      },
      "name" : "Código de la tarea de derivación",
      "description" : "El Task de esta guía es siempre un registro de flujo de trabajo de derivación.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-diagnostico.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-diagnostico"
      },
      "name" : "Diagnóstico de la contrareferencia",
      "description" : "El diagnóstico que el especialista devuelve a APS. Perfil propio de esta guía, sobre el recurso base Condition de FHIR R4.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Condition"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Condition-diagnostico-ref-2026-0001.html"
      }],
      "reference" : {
        "reference" : "Condition/diagnostico-ref-2026-0001"
      },
      "name" : "Diagnóstico: insuficiencia cardiaca sistólica crónica",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-diagnostico"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-documento.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-documento"
      },
      "name" : "Documento de contrareferencia",
      "description" : "La entrada de índice de la contrareferencia. Perfil propio de esta guía, sobre el recurso base DocumentReference de FHIR R4.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "DocumentReference"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "DocumentReference-documento-ref-2026-0001.html"
      }],
      "reference" : {
        "reference" : "DocumentReference/documento-ref-2026-0001"
      },
      "name" : "Documento de contrareferencia REF-2026-0001",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-documento"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Observation"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Observation-ecg-2026-11-19.html"
      }],
      "reference" : {
        "reference" : "Observation/ecg-2026-11-19"
      },
      "name" : "ECG de la derivación REF-2026-0001",
      "exampleBoolean" : true
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Encounter"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Encounter-aps-encounter-2026-11-19.html"
      }],
      "reference" : {
        "reference" : "Encounter/aps-encounter-2026-11-19"
      },
      "name" : "Encuentro APS que creó la derivación",
      "description" : "El encuentro de APS existe en el EHR de APS; la guía lo referencia, no lo remodela.",
      "exampleBoolean" : true
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-encuentro.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-encuentro"
      },
      "name" : "Encuentro de especialidad",
      "description" : "La visita atendida en la especialidad. Perfil propio de esta guía, sobre el recurso base Encounter de FHIR R4. La cita es la reserva; la visita es el encuentro — nunca ambas a la vez sin regla, y la regla aquí es: reserva = Appointment, visita = Encounter.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Encounter"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Encounter-encuentro-ref-2026-0001.html"
      }],
      "reference" : {
        "reference" : "Encounter/encuentro-ref-2026-0001"
      },
      "name" : "Encuentro de especialidad REF-2026-0001 (planned)",
      "description" : "La visita, creada en la reserva (planned); no se crea en la asistencia.",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-encuentro"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Endpoint"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Endpoint-endpoint-cardiologia.html"
      }],
      "reference" : {
        "reference" : "Endpoint/endpoint-cardiologia"
      },
      "name" : "Endpoint del servicio de cardiología",
      "exampleBoolean" : true
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "ValueSet"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "ValueSet-derivacion-especialidad.html"
      }],
      "reference" : {
        "reference" : "ValueSet/derivacion-especialidad"
      },
      "name" : "Especialidad / servicio (catálogo local)",
      "description" : "Especialidades y servicios a los que se puede derivar.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "CodeSystem"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "CodeSystem-derivacion-especialidad.html"
      }],
      "reference" : {
        "reference" : "CodeSystem/derivacion-especialidad"
      },
      "name" : "Especialidad / servicio (catálogo local)",
      "description" : "Catálogo local de especialidades y servicios, versionado por la red (hub + servicios). El ejemplo trabajado es cardiología; la red amplía el catálogo sin tocar esta guía.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Practitioner"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Practitioner-especialista-cardiologia.html"
      }],
      "reference" : {
        "reference" : "Practitioner/especialista-cardiologia"
      },
      "name" : "Especialista de cardiología (sintético)",
      "exampleBoolean" : true
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "PractitionerRole"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "PractitionerRole-rol-especialista.html"
      }],
      "reference" : {
        "reference" : "PractitionerRole/rol-especialista"
      },
      "name" : "Especialista en la derivación REF-2026-0001",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-rol"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "ValueSet"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "ValueSet-derivacion-estado-referencia.html"
      }],
      "reference" : {
        "reference" : "ValueSet/derivacion-estado-referencia"
      },
      "name" : "Estado de la derivación",
      "description" : "Estados posibles de una derivación APS → especialidad.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "CodeSystem"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "CodeSystem-derivacion-estado-referencia.html"
      }],
      "reference" : {
        "reference" : "CodeSystem/derivacion-estado-referencia"
      },
      "name" : "Estado de la derivación",
      "description" : "Los nueve estados del caso de la derivación APS → especialidad (spec §3.1). El estado vive en Task.businessStatus, nunca como valor inventado de Task.status.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Organization"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Organization-org-hub.html"
      }],
      "reference" : {
        "reference" : "Organization/org-hub"
      },
      "name" : "Hub de derivación",
      "exampleBoolean" : true
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:extension"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-referral-identifier.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-referral-identifier"
      },
      "name" : "Identificador de la derivación",
      "description" : "El identificador de la derivación (el mismo de ServiceRequest.identifier) en la Composition de la contrareferencia. Ningún campo base de Composition lleva el id de la derivación; el enlace también viaja en DocumentReference.context.related.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Patient"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Patient-maria-gonzalez.html"
      }],
      "reference" : {
        "reference" : "Patient/maria-gonzalez"
      },
      "name" : "María González (paciente sintética)",
      "description" : "Paciente de la derivación REF-2026-0001.",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-paciente"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "ValueSet"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "ValueSet-derivacion-motivo-rechazo.html"
      }],
      "reference" : {
        "reference" : "ValueSet/derivacion-motivo-rechazo"
      },
      "name" : "Motivo de rechazo",
      "description" : "Motivos por los que la especialidad puede rechazar una derivación.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "CodeSystem"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "CodeSystem-derivacion-motivo-rechazo.html"
      }],
      "reference" : {
        "reference" : "CodeSystem/derivacion-motivo-rechazo"
      },
      "name" : "Motivo de rechazo",
      "description" : "Motivos de rechazo de la derivación (lista local de la especialidad; el texto libre acompaña al código).",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Practitioner"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Practitioner-medico-aps.html"
      }],
      "reference" : {
        "reference" : "Practitioner/medico-aps"
      },
      "name" : "Médico APS (sintético)",
      "exampleBoolean" : true
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "PractitionerRole"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "PractitionerRole-rol-medico-aps.html"
      }],
      "reference" : {
        "reference" : "PractitionerRole/rol-medico-aps"
      },
      "name" : "Médico APS en la derivación REF-2026-0001",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-rol"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-notificacion.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-notificacion"
      },
      "name" : "Notificación",
      "description" : "El registro de una notificación enviada en un cambio de estado de la derivación. Perfil propio de esta guía, sobre el recurso base Communication de FHIR R4. Una notificación enviada por error se corrige con una notificación nueva, nunca borrando el registro.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Communication"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Communication-notificacion-aceptacion-ref-2026-0001.html"
      }],
      "reference" : {
        "reference" : "Communication/notificacion-aceptacion-ref-2026-0001"
      },
      "name" : "Notificación de aceptación a la paciente",
      "description" : "El administrativo de APS informa a la paciente de que la especialidad aceptó la derivación (PI-1, C5/Q3).",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-notificacion"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Observation"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Observation-ntprobnp-2026-11-19.html"
      }],
      "reference" : {
        "reference" : "Observation/ntprobnp-2026-11-19"
      },
      "name" : "NT-proBNP de la derivación REF-2026-0001",
      "exampleBoolean" : true
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:extension"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-offer-number.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-offer-number"
      },
      "name" : "Número de oferta (de esta derivación)",
      "description" : "Contador por derivación: 1ª oferta, re-oferta (2ª), etc. Cada oferta es un Appointment nuevo.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-paciente.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-paciente"
      },
      "name" : "Paciente de la derivación",
      "description" : "Persona derivada desde APS a una especialidad. Perfil propio de esta guía, sobre el recurso base Patient de FHIR R4. La clave MPI y el RUN son los identificadores que viajan; los datos de contacto son obligatorios (C12) — sin ellos la creación se bloquea.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-plan-seguimiento.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-plan-seguimiento"
      },
      "name" : "Plan de seguimiento para APS",
      "description" : "El plan de seguimiento que el especialista deja a APS. Perfil propio de esta guía, sobre el recurso base CarePlan de FHIR R4. Una actualización del plan es una versión nueva, nunca una sobrescritura silenciosa.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "CarePlan"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "CarePlan-plan-ref-2026-0001.html"
      }],
      "reference" : {
        "reference" : "CarePlan/plan-ref-2026-0001"
      },
      "name" : "Plan de seguimiento para APS",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-plan-seguimiento"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:extension"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-sla-acceptance-deadline.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-sla-acceptance-deadline"
      },
      "name" : "Plazo de aceptación",
      "description" : "Fecha límite para la decisión de aceptación/rechazo: creación + 5 días hábiles (2 si es urgente).",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:extension"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-sla-confirmation-deadline.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-sla-confirmation-deadline"
      },
      "name" : "Plazo de confirmación",
      "description" : "Fecha límite para confirmar una oferta: oferta + 3 días hábiles. Presente solo mientras una oferta está abierta.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:extension"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-sla-counterreferral-deadline.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-sla-counterreferral-deadline"
      },
      "name" : "Plazo de contrareferencia",
      "description" : "Fecha límite para enviar la contrareferencia: encuentro + 5 días hábiles.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:extension"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-sla-offer-deadline.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-sla-offer-deadline"
      },
      "name" : "Plazo de oferta de cita",
      "description" : "Fecha límite para ofrecer la cita: aceptación + 10 días hábiles.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:extension"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-sla-retriage-deadline.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-sla-retriage-deadline"
      },
      "name" : "Plazo de re-triaje",
      "description" : "Fecha límite para la decisión de re-triaje de APS: rechazo (o retorno por fallo de agendamiento) + 5 días hábiles.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "AppointmentResponse"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "AppointmentResponse-respuesta-cita-1.html"
      }],
      "reference" : {
        "reference" : "AppointmentResponse/respuesta-cita-1"
      },
      "name" : "Respuesta de la paciente a la oferta (accepted)",
      "exampleBoolean" : true
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:extension"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-delivery-outcome.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-delivery-outcome"
      },
      "name" : "Resultado de la entrega",
      "description" : "Resultado de la entrega de una notificación: delivered | failed. Communication.status = completed significa enviada; el resultado de la entrega es esta extensión.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "ValueSet"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "ValueSet-derivacion-resultado-entrega.html"
      }],
      "reference" : {
        "reference" : "ValueSet/derivacion-resultado-entrega"
      },
      "name" : "Resultado de la entrega de una notificación",
      "description" : "Resultados posibles de la entrega de una notificación.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "CodeSystem"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "CodeSystem-derivacion-resultado-entrega.html"
      }],
      "reference" : {
        "reference" : "CodeSystem/derivacion-resultado-entrega"
      },
      "name" : "Resultado de la entrega de una notificación",
      "description" : "Resultados posibles de la entrega de una notificación (lista local).",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-rol.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-rol"
      },
      "name" : "Rol en la derivación",
      "description" : "El rol que un profesional tiene en una derivación. Perfil propio de esta guía, sobre el recurso base PractitionerRole de FHIR R4. Una persona puede tener más de un rol en distintas derivaciones, pero dentro de una derivación cada rol es una persona.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "ValueSet"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "ValueSet-derivacion-rol.html"
      }],
      "reference" : {
        "reference" : "ValueSet/derivacion-rol"
      },
      "name" : "Rol en la derivación",
      "description" : "Roles que una persona puede tener en una derivación.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "CodeSystem"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "CodeSystem-derivacion-rol.html"
      }],
      "reference" : {
        "reference" : "CodeSystem/derivacion-rol"
      },
      "name" : "Rol en la derivación",
      "description" : "Los seis roles del caso de uso (spec §2). Dentro de una derivación, cada rol es una persona (el clínico de triaje no es el agendador — C1).",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "HealthcareService"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "HealthcareService-servicio-cardiologia.html"
      }],
      "reference" : {
        "reference" : "HealthcareService/servicio-cardiologia"
      },
      "name" : "Servicio de cardiología",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-servicio"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Organization"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Organization-org-cardiologia.html"
      }],
      "reference" : {
        "reference" : "Organization/org-cardiologia"
      },
      "name" : "Servicio de cardiología (organización)",
      "exampleBoolean" : true
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-servicio.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-servicio"
      },
      "name" : "Servicio de especialidad",
      "description" : "El servicio de especialidad al que se deriva (p. ej. cardiología), con su endpoint de enrutado. Perfil propio de esta guía, sobre el recurso base HealthcareService de FHIR R4.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Slot"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Slot-slot-cardiologia-1.html"
      }],
      "reference" : {
        "reference" : "Slot/slot-cardiologia-1"
      },
      "name" : "Slot de cardiología (reservado)",
      "exampleBoolean" : true
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-solicitud.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-solicitud"
      },
      "name" : "Solicitud de derivación",
      "description" : "La derivación que APS crea y el hub enruta: una solicitud de un servicio de especialidad. Perfil propio de esta guía, sobre el recurso base ServiceRequest de FHIR R4. El estado de la derivación NO vive aquí (vive en DerivacionTarea); ServiceRequest.status es solo un espejo grueso.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "ServiceRequest"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "ServiceRequest-ref-2026-0001.html"
      }],
      "reference" : {
        "reference" : "ServiceRequest/ref-2026-0001"
      },
      "name" : "Solicitud de derivación REF-2026-0001",
      "description" : "Derivación de María González a cardiología por sospecha de insuficiencia cardiaca (PI-0).",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-solicitud"
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "StructureDefinition:resource"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "StructureDefinition-derivacion-tarea.html"
      }],
      "reference" : {
        "reference" : "StructureDefinition/derivacion-tarea"
      },
      "name" : "Tarea de derivación (registro de estado)",
      "description" : "El registro de estado del flujo de trabajo de una derivación: lleva el estado del caso, los relojes SLA y los conteos de los ciclos. Es el centro del grafo de recursos y lo primero que lee cada paso posterior. Perfil propio de esta guía, sobre el recurso base Task de FHIR R4.",
      "exampleBoolean" : false
    },
    {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/resource-information",
        "valueString" : "Task"
      },
      {
        "url" : "http://hl7.org/fhir/StructureDefinition/implementationguide-page",
        "valueUri" : "Task-tarea-ref-2026-0001.html"
      }],
      "reference" : {
        "reference" : "Task/tarea-ref-2026-0001"
      },
      "name" : "Tarea de derivación REF-2026-0001 (requested)",
      "description" : "El registro de estado del flujo de trabajo, en su creación (PI-0).",
      "exampleCanonical" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-tarea"
    }],
    "page" : {
      "extension" : [{
        "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
        "valueUrl" : "toc.html"
      }],
      "nameUrl" : "toc.html",
      "title" : "Table of Contents",
      "generation" : "html",
      "page" : [{
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "index.html"
        }],
        "nameUrl" : "index.html",
        "title" : "Derivación APS → especialidad",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "process.html"
        }],
        "nameUrl" : "process.html",
        "title" : "Proceso (BPMN)",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "resources.html"
        }],
        "nameUrl" : "resources.html",
        "title" : "Diagrama de recursos",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "profiles.html"
        }],
        "nameUrl" : "profiles.html",
        "title" : "Perfiles",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "terminology.html"
        }],
        "nameUrl" : "terminology.html",
        "title" : "Terminología",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "operations.html"
        }],
        "nameUrl" : "operations.html",
        "title" : "Operaciones",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "sequences.html"
        }],
        "nameUrl" : "sequences.html",
        "title" : "Diagramas de secuencia",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "mapping.html"
        }],
        "nameUrl" : "mapping.html",
        "title" : "Mapeo de datos",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "ihe.html"
        }],
        "nameUrl" : "ihe.html",
        "title" : "Relación con IHE",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "lifecycle.html"
        }],
        "nameUrl" : "lifecycle.html",
        "title" : "Ciclo de vida",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "rules.html"
        }],
        "nameUrl" : "rules.html",
        "title" : "Reglas y retención",
        "generation" : "markdown"
      },
      {
        "extension" : [{
          "url" : "http://hl7.org/fhir/tools/StructureDefinition/ig-page-name",
          "valueUrl" : "public-health.html"
        }],
        "nameUrl" : "public-health.html",
        "title" : "Base legal y reporte",
        "generation" : "markdown"
      }]
    },
    "parameter" : [{
      "code" : "path-resource",
      "value" : "input/capabilities"
    },
    {
      "code" : "path-resource",
      "value" : "input/examples"
    },
    {
      "code" : "path-resource",
      "value" : "input/extensions"
    },
    {
      "code" : "path-resource",
      "value" : "input/models"
    },
    {
      "code" : "path-resource",
      "value" : "input/operations"
    },
    {
      "code" : "path-resource",
      "value" : "input/profiles"
    },
    {
      "code" : "path-resource",
      "value" : "input/resources"
    },
    {
      "code" : "path-resource",
      "value" : "input/vocabulary"
    },
    {
      "code" : "path-resource",
      "value" : "input/maps"
    },
    {
      "code" : "path-resource",
      "value" : "input/testing"
    },
    {
      "code" : "path-resource",
      "value" : "input/history"
    },
    {
      "code" : "path-resource",
      "value" : "fsh-generated/resources"
    },
    {
      "code" : "path-pages",
      "value" : "template/config"
    },
    {
      "code" : "path-pages",
      "value" : "input/images"
    },
    {
      "code" : "path-tx-cache",
      "value" : "input-cache/txcache"
    }]
  }
}

```
