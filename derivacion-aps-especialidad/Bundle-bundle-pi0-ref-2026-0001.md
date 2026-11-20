# Bundle de transacción PI-0 (creación de la derivación) - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Bundle de transacción PI-0 (creación de la derivación)**

## Example Bundle: Bundle de transacción PI-0 (creación de la derivación)



## Resource Content

```json
{
  "resourceType" : "Bundle",
  "id" : "bundle-pi0-ref-2026-0001",
  "type" : "transaction",
  "entry" : [{
    "fullUrl" : "urn:uuid:11111111-1111-4111-8111-111111111111",
    "resource" : {
      "resourceType" : "ServiceRequest",
      "id" : "ref-2026-0001",
      "meta" : {
        "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-solicitud"]
      },
      "text" : {
        "status" : "generated",
        "div" : "<div xmlns=\"http://www.w3.org/1999/xhtml\"><a name=\"ServiceRequest_ref-2026-0001\"> </a><p class=\"res-header-id\"><b>Generated Narrative: ServiceRequest ref-2026-0001</b></p><a name=\"ref-2026-0001\"> </a><a name=\"hcref-2026-0001\"> </a><div style=\"display: inline-block; background-color: #fbffeb; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%\"><p style=\"margin-bottom: 0px\"/><p style=\"margin-bottom: 0px\">Profile: <a href=\"StructureDefinition-derivacion-solicitud.html\">Solicitud de derivación</a></p></div><p><b>identifier</b>: <code>http://aps.losaromos.example.org/referral</code>/REF-2026-0001</p><p><b>status</b>: Active</p><p><b>intent</b>: Order</p><p><b>priority</b>: Routine</p><p><b>code</b>: <span title=\"Codes:{https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-especialidad cardiologia}\">Cardiology</span></p><p><b>subject</b>: <a href=\"Patient-maria-gonzalez.html\">María González (official) Female, DoB: 1968-04-15 ( http://www.registrocivil.cl/run#11111111-1)</a></p><p><b>encounter</b>: <a href=\"Encounter-aps-encounter-2026-11-19.html\">Encounter: status = finished; class = Ambulatory (ActCode#AMB); period = 2026-11-19 09:00:00-0300 --&gt; 2026-11-19 09:30:00-0300</a></p><p><b>authoredOn</b>: 2026-11-19 09:30:00-0300</p><p><b>requester</b>: <a href=\"PractitionerRole-rol-medico-aps.html\">Ana Pérez (official) (http://www.registrocivil.cl/run#22222222-2): APS doctor at CESFAM Los Aromos (http://aps.losaromos.example.org/organization#CESFAM-LOS-AROMOS)</a></p><p><b>performerType</b>: <span title=\"Codes:{https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-especialidad cardiologia}\">Cardiology</span></p><p><b>performer</b>: <a href=\"HealthcareService-servicio-cardiologia.html\">Cardiology (Cardiology) by Servicio de Cardiología (http://especialidad.example.org/organization#CARDIOLOGIA) (http://especialidad.example.org/service#cardiologia)</a></p><p><b>reasonCode</b>: <span title=\"Codes:{http://snomed.info/sct 84114007}\">Suspected heart failure: exertional dyspnoea, ankle oedema</span></p><p><b>supportingInfo</b>: </p><ul><li><a href=\"Observation-ecg-2026-11-19.html\">Observation EKG study</a></li><li><a href=\"Observation-ntprobnp-2026-11-19.html\">Observation Natriuretic peptide.B prohormone N-Terminal [Mass/volume] in Serum or Plasma</a></li></ul><p><b>note</b>: </p><blockquote><div><p>Disnea de esfuerzo y edema de tobillos de dos semanas de evolución.</p>\n</div></blockquote></div>"
      },
      "identifier" : [{
        "system" : "http://aps.losaromos.example.org/referral",
        "value" : "REF-2026-0001"
      }],
      "status" : "active",
      "intent" : "order",
      "priority" : "routine",
      "code" : {
        "coding" : [{
          "system" : "https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-especialidad",
          "code" : "cardiologia",
          "display" : "Cardiology"
        }]
      },
      "subject" : {
        "reference" : "Patient/maria-gonzalez"
      },
      "encounter" : {
        "reference" : "Encounter/aps-encounter-2026-11-19"
      },
      "authoredOn" : "2026-11-19T09:30:00-03:00",
      "requester" : {
        "reference" : "PractitionerRole/rol-medico-aps"
      },
      "performerType" : {
        "coding" : [{
          "system" : "https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-especialidad",
          "code" : "cardiologia",
          "display" : "Cardiology"
        }]
      },
      "performer" : [{
        "reference" : "HealthcareService/servicio-cardiologia"
      }],
      "reasonCode" : [{
        "coding" : [{
          "system" : "http://snomed.info/sct",
          "code" : "84114007",
          "display" : "Heart failure (disorder)"
        }],
        "text" : "Suspected heart failure: exertional dyspnoea, ankle oedema"
      }],
      "supportingInfo" : [{
        "reference" : "Observation/ecg-2026-11-19"
      },
      {
        "reference" : "Observation/ntprobnp-2026-11-19"
      }],
      "note" : [{
        "text" : "Disnea de esfuerzo y edema de tobillos de dos semanas de evolución."
      }]
    },
    "request" : {
      "method" : "POST",
      "url" : "ServiceRequest"
    }
  },
  {
    "fullUrl" : "urn:uuid:22222222-2222-4222-8222-222222222222",
    "resource" : {
      "resourceType" : "Task",
      "id" : "tarea-ref-2026-0001",
      "meta" : {
        "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-tarea"]
      },
      "text" : {
        "status" : "extensions",
        "div" : "<div xmlns=\"http://www.w3.org/1999/xhtml\"><a name=\"Task_tarea-ref-2026-0001\"> </a><p class=\"res-header-id\"><b>Generated Narrative: Task tarea-ref-2026-0001</b></p><a name=\"tarea-ref-2026-0001\"> </a><a name=\"hctarea-ref-2026-0001\"> </a><div style=\"display: inline-block; background-color: #fbffeb; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%\"><p style=\"margin-bottom: 0px\"/><p style=\"margin-bottom: 0px\">Profile: <a href=\"StructureDefinition-derivacion-tarea.html\">Tarea de derivación (registro de estado)</a></p></div><p><b>Plazo de aceptación</b>: 2026-11-26 17:00:00-0300</p><p><b>identifier</b>: <code>http://aps.losaromos.example.org/referral</code>/REF-2026-0001</p><p><b>status</b>: Requested</p><p><b>businessStatus</b>: <span title=\"Codes:{https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-estado-referencia requested}\">Requested</span></p><p><b>intent</b>: order</p><p><b>code</b>: <span title=\"Codes:{https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-task-code referral-workflow}\">Referral workflow</span></p><p><b>description</b>: acceptance decision</p><p><b>focus</b>: <a href=\"ServiceRequest-ref-2026-0001.html\">ServiceRequest Cardiology</a></p><p><b>for</b>: <a href=\"Patient-maria-gonzalez.html\">María González (official) Female, DoB: 1968-04-15 ( http://www.registrocivil.cl/run#11111111-1)</a></p><p><b>authoredOn</b>: 2026-11-19 09:30:00-0300</p><p><b>lastModified</b>: 2026-11-19 09:30:00-0300</p><p><b>requester</b>: <a href=\"PractitionerRole-rol-medico-aps.html\">Ana Pérez (official) (http://www.registrocivil.cl/run#22222222-2): APS doctor at CESFAM Los Aromos (http://aps.losaromos.example.org/organization#CESFAM-LOS-AROMOS)</a></p></div>"
      },
      "extension" : [{
        "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-sla-acceptance-deadline",
        "valueDateTime" : "2026-11-26T17:00:00-03:00"
      }],
      "identifier" : [{
        "system" : "http://aps.losaromos.example.org/referral",
        "value" : "REF-2026-0001"
      }],
      "status" : "requested",
      "businessStatus" : {
        "coding" : [{
          "system" : "https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-estado-referencia",
          "code" : "requested",
          "display" : "Requested"
        }]
      },
      "intent" : "order",
      "code" : {
        "coding" : [{
          "system" : "https://josemandrade.github.io/prueba-his-muse-nvidia/CodeSystem/derivacion-task-code",
          "code" : "referral-workflow",
          "display" : "Referral workflow"
        }]
      },
      "description" : "acceptance decision",
      "focus" : {
        "reference" : "ServiceRequest/ref-2026-0001"
      },
      "for" : {
        "reference" : "Patient/maria-gonzalez"
      },
      "authoredOn" : "2026-11-19T09:30:00-03:00",
      "lastModified" : "2026-11-19T09:30:00-03:00",
      "requester" : {
        "reference" : "PractitionerRole/rol-medico-aps"
      }
    },
    "request" : {
      "method" : "POST",
      "url" : "Task"
    }
  }]
}

```
