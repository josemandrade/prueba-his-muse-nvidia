# Bundle de documento PI-3 (contrareferencia) - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Bundle de documento PI-3 (contrareferencia)**

## Example Bundle: Bundle de documento PI-3 (contrareferencia)



## Resource Content

```json
{
  "resourceType" : "Bundle",
  "id" : "bundle-pi3-ref-2026-0001",
  "type" : "document",
  "timestamp" : "2026-12-03T10:00:00-03:00",
  "entry" : [{
    "fullUrl" : "Composition/contrareferencia-ref-2026-0001",
    "resource" : {
      "resourceType" : "Composition",
      "id" : "contrareferencia-ref-2026-0001",
      "meta" : {
        "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-contrareferencia"]
      },
      "text" : {
        "status" : "extensions",
        "div" : "<div xmlns=\"http://www.w3.org/1999/xhtml\"><a name=\"Composition_contrareferencia-ref-2026-0001\"> </a><p class=\"res-header-id\"><b>Generated Narrative: Composition contrareferencia-ref-2026-0001</b></p><a name=\"contrareferencia-ref-2026-0001\"> </a><a name=\"hccontrareferencia-ref-2026-0001\"> </a><div style=\"display: inline-block; background-color: #fbffeb; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%\"><p style=\"margin-bottom: 0px\"/><p style=\"margin-bottom: 0px\">Profile: <a href=\"StructureDefinition-derivacion-contrareferencia.html\">Contrareferencia</a></p></div><p><b>Identificador de la derivación</b>: <code>http://aps.losaromos.example.org/referral</code>/REF-2026-0001</p><p><b>identifier</b>: <code>http://especialidad.example.org/counter-referral</code>/CR-2026-0001</p><p><b>status</b>: Final</p><p><b>type</b>: <span title=\"Codes:{http://loinc.org 11488-4}\">Consult note</span></p><p><b>encounter</b>: <a href=\"Encounter-encuentro-ref-2026-0001.html\">Encounter: identifier = http://especialidad.example.org/encounter#ENC-2026-0001; status = planned; class = Ambulatory (ActCode#AMB); serviceType = Cardiology; period = 2026-12-02 10:00:00-0300 --&gt; 2026-12-02 10:30:00-0300</a></p><p><b>date</b>: 2026-12-03 10:00:00-0300</p><p><b>author</b>: <a href=\"PractitionerRole-rol-especialista.html\">Carlos Rojas (official) (http://www.registrocivil.cl/run#33333333-3): Specialist at Servicio de Cardiología (http://especialidad.example.org/organization#CARDIOLOGIA)</a></p><p><b>title</b>: Counter-referral</p></div>"
      },
      "extension" : [{
        "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-referral-identifier",
        "valueIdentifier" : {
          "system" : "http://aps.losaromos.example.org/referral",
          "value" : "REF-2026-0001"
        }
      }],
      "identifier" : {
        "system" : "http://especialidad.example.org/counter-referral",
        "value" : "CR-2026-0001"
      },
      "status" : "final",
      "type" : {
        "coding" : [{
          "system" : "http://loinc.org",
          "code" : "11488-4",
          "display" : "Consult note"
        }]
      },
      "subject" : {
        "reference" : "Patient/maria-gonzalez"
      },
      "encounter" : {
        "reference" : "Encounter/encuentro-ref-2026-0001"
      },
      "date" : "2026-12-03T10:00:00-03:00",
      "author" : [{
        "reference" : "PractitionerRole/rol-especialista"
      }],
      "title" : "Counter-referral",
      "section" : [{
        "title" : "Diagnosis",
        "code" : {
          "text" : "Diagnosis"
        },
        "text" : {
          "status" : "generated",
          "div" : "<div xmlns=\"http://www.w3.org/1999/xhtml\">Chronic systolic heart failure, LVEF 35% (ICD-10-CM I50.22).</div>"
        },
        "entry" : [{
          "reference" : "Condition/diagnostico-ref-2026-0001"
        }]
      },
      {
        "title" : "Plan",
        "code" : {
          "text" : "Plan"
        },
        "text" : {
          "status" : "generated",
          "div" : "<div xmlns=\"http://www.w3.org/1999/xhtml\">Start heart-failure treatment; control in APS in 2 weeks.</div>"
        },
        "entry" : [{
          "reference" : "CarePlan/plan-ref-2026-0001"
        }]
      },
      {
        "title" : "Follow-up indications",
        "code" : {
          "text" : "Follow-up indications"
        },
        "text" : {
          "status" : "generated",
          "div" : "<div xmlns=\"http://www.w3.org/1999/xhtml\">Blood pressure, weight and symptoms at each APS control; NT-proBNP in 3 months.</div>"
        }
      },
      {
        "title" : "Follow-up plan for APS",
        "code" : {
          "text" : "Follow-up plan for APS"
        },
        "text" : {
          "status" : "generated",
          "div" : "<div xmlns=\"http://www.w3.org/1999/xhtml\">APS follow-up as in the CarePlan; new referral to cardiology if dyspnoea worsens.</div>"
        },
        "entry" : [{
          "reference" : "CarePlan/plan-ref-2026-0001"
        }]
      }]
    }
  },
  {
    "fullUrl" : "DocumentReference/documento-ref-2026-0001",
    "resource" : {
      "resourceType" : "DocumentReference",
      "id" : "documento-ref-2026-0001",
      "meta" : {
        "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-documento"]
      },
      "text" : {
        "status" : "generated",
        "div" : "<div xmlns=\"http://www.w3.org/1999/xhtml\"><a name=\"DocumentReference_documento-ref-2026-0001\"> </a><p class=\"res-header-id\"><b>Generated Narrative: DocumentReference documento-ref-2026-0001</b></p><a name=\"documento-ref-2026-0001\"> </a><a name=\"hcdocumento-ref-2026-0001\"> </a><div style=\"display: inline-block; background-color: #fbffeb; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%\"><p style=\"margin-bottom: 0px\"/><p style=\"margin-bottom: 0px\">Profile: <a href=\"StructureDefinition-derivacion-documento.html\">Documento de contrareferencia</a></p></div><p><b>masterIdentifier</b>: <code>http://especialidad.example.org/counter-referral</code>/CR-2026-0001</p><p><b>status</b>: Current</p><p><b>type</b>: <span title=\"Codes:{http://loinc.org 11488-4}\">Consult note</span></p><p><b>subject</b>: <a href=\"Patient-maria-gonzalez.html\">María González (official) Female, DoB: 1968-04-15 ( http://www.registrocivil.cl/run#11111111-1)</a></p><p><b>date</b>: 2026-12-03 10:00:00-0300</p><p><b>author</b>: <a href=\"PractitionerRole-rol-especialista.html\">Carlos Rojas (official) (http://www.registrocivil.cl/run#33333333-3): Specialist at Servicio de Cardiología (http://especialidad.example.org/organization#CARDIOLOGIA)</a></p><blockquote><p><b>content</b></p><h3>Attachments</h3><table class=\"grid\"><tr><td style=\"display: none\">-</td><td><b>ContentType</b></td><td><b>Url</b></td></tr><tr><td style=\"display: none\">*</td><td>application/fhir+json</td><td><a href=\"Composition-contrareferencia-ref-2026-0001.html\">Composition Counter-referral</a></td></tr></table></blockquote><h3>Contexts</h3><table class=\"grid\"><tr><td style=\"display: none\">-</td><td><b>Encounter</b></td><td><b>Period</b></td><td><b>Related</b></td></tr><tr><td style=\"display: none\">*</td><td><a href=\"Encounter-encuentro-ref-2026-0001.html\">Encounter: identifier = http://especialidad.example.org/encounter#ENC-2026-0001; status = planned; class = Ambulatory (ActCode#AMB); serviceType = Cardiology; period = 2026-12-02 10:00:00-0300 --&gt; 2026-12-02 10:30:00-0300</a></td><td>2026-12-02 10:00:00-0300 --&gt; 2026-12-02 10:30:00-0300</td><td><a href=\"ServiceRequest-ref-2026-0001.html\">ServiceRequest Cardiology</a></td></tr></table></div>"
      },
      "masterIdentifier" : {
        "system" : "http://especialidad.example.org/counter-referral",
        "value" : "CR-2026-0001"
      },
      "status" : "current",
      "type" : {
        "coding" : [{
          "system" : "http://loinc.org",
          "code" : "11488-4",
          "display" : "Consult note"
        }]
      },
      "subject" : {
        "reference" : "Patient/maria-gonzalez"
      },
      "date" : "2026-12-03T10:00:00-03:00",
      "author" : [{
        "reference" : "PractitionerRole/rol-especialista"
      }],
      "content" : [{
        "attachment" : {
          "contentType" : "application/fhir+json",
          "url" : "Composition/contrareferencia-ref-2026-0001"
        }
      }],
      "context" : {
        "encounter" : [{
          "reference" : "Encounter/encuentro-ref-2026-0001"
        }],
        "period" : {
          "start" : "2026-12-02T10:00:00-03:00",
          "end" : "2026-12-02T10:30:00-03:00"
        },
        "related" : [{
          "reference" : "ServiceRequest/ref-2026-0001"
        }]
      }
    }
  },
  {
    "fullUrl" : "Condition/diagnostico-ref-2026-0001",
    "resource" : {
      "resourceType" : "Condition",
      "id" : "diagnostico-ref-2026-0001",
      "meta" : {
        "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-diagnostico"]
      },
      "text" : {
        "status" : "generated",
        "div" : "<div xmlns=\"http://www.w3.org/1999/xhtml\"><a name=\"Condition_diagnostico-ref-2026-0001\"> </a><p class=\"res-header-id\"><b>Generated Narrative: Condition diagnostico-ref-2026-0001</b></p><a name=\"diagnostico-ref-2026-0001\"> </a><a name=\"hcdiagnostico-ref-2026-0001\"> </a><div style=\"display: inline-block; background-color: #fbffeb; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%\"><p style=\"margin-bottom: 0px\"/><p style=\"margin-bottom: 0px\">Profile: <a href=\"StructureDefinition-derivacion-diagnostico.html\">Diagnóstico de la contrareferencia</a></p></div><p><b>clinicalStatus</b>: <span title=\"Codes:{http://terminology.hl7.org/CodeSystem/condition-clinical active}\">Active</span></p><p><b>verificationStatus</b>: <span title=\"Codes:{http://terminology.hl7.org/CodeSystem/condition-ver-status confirmed}\">Confirmed</span></p><p><b>code</b>: <span title=\"Codes:{http://hl7.org/fhir/sid/icd-10-cm I50.22}, {http://snomed.info/sct 417996009}\">Insuficiencia cardiaca sistólica crónica (FEVI 35%)</span></p><p><b>subject</b>: <a href=\"Patient-maria-gonzalez.html\">María González (official) Female, DoB: 1968-04-15 ( http://www.registrocivil.cl/run#11111111-1)</a></p><p><b>encounter</b>: <a href=\"Encounter-encuentro-ref-2026-0001.html\">Encounter: identifier = http://especialidad.example.org/encounter#ENC-2026-0001; status = planned; class = Ambulatory (ActCode#AMB); serviceType = Cardiology; period = 2026-12-02 10:00:00-0300 --&gt; 2026-12-02 10:30:00-0300</a></p><p><b>note</b>: </p><blockquote><div><p>FEVI 35% por ecocardiograma. Sin isquemia aguda en el ECG.</p>\n</div></blockquote></div>"
      },
      "clinicalStatus" : {
        "coding" : [{
          "system" : "http://terminology.hl7.org/CodeSystem/condition-clinical",
          "code" : "active",
          "display" : "Active"
        }]
      },
      "verificationStatus" : {
        "coding" : [{
          "system" : "http://terminology.hl7.org/CodeSystem/condition-ver-status",
          "code" : "confirmed",
          "display" : "Confirmed"
        }]
      },
      "code" : {
        "coding" : [{
          "system" : "http://hl7.org/fhir/sid/icd-10-cm",
          "code" : "I50.22",
          "display" : "Chronic systolic (congestive) heart failure"
        },
        {
          "system" : "http://snomed.info/sct",
          "code" : "417996009",
          "display" : "Systolic heart failure"
        }],
        "text" : "Insuficiencia cardiaca sistólica crónica (FEVI 35%)"
      },
      "subject" : {
        "reference" : "Patient/maria-gonzalez"
      },
      "encounter" : {
        "reference" : "Encounter/encuentro-ref-2026-0001"
      },
      "note" : [{
        "text" : "FEVI 35% por ecocardiograma. Sin isquemia aguda en el ECG."
      }]
    }
  },
  {
    "fullUrl" : "CarePlan/plan-ref-2026-0001",
    "resource" : {
      "resourceType" : "CarePlan",
      "id" : "plan-ref-2026-0001",
      "meta" : {
        "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-plan-seguimiento"]
      },
      "text" : {
        "status" : "generated",
        "div" : "<div xmlns=\"http://www.w3.org/1999/xhtml\"><a name=\"CarePlan_plan-ref-2026-0001\"> </a><p class=\"res-header-id\"><b>Generated Narrative: CarePlan plan-ref-2026-0001</b></p><a name=\"plan-ref-2026-0001\"> </a><a name=\"hcplan-ref-2026-0001\"> </a><div style=\"display: inline-block; background-color: #fbffeb; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%\"><p style=\"margin-bottom: 0px\"/><p style=\"margin-bottom: 0px\">Profile: <a href=\"StructureDefinition-derivacion-plan-seguimiento.html\">Plan de seguimiento para APS</a></p></div><p><b>status</b>: Active</p><p><b>intent</b>: Plan</p><p><b>subject</b>: <a href=\"Patient-maria-gonzalez.html\">María González (official) Female, DoB: 1968-04-15 ( http://www.registrocivil.cl/run#11111111-1)</a></p><p><b>encounter</b>: <a href=\"Encounter-encuentro-ref-2026-0001.html\">Encounter: identifier = http://especialidad.example.org/encounter#ENC-2026-0001; status = planned; class = Ambulatory (ActCode#AMB); serviceType = Cardiology; period = 2026-12-02 10:00:00-0300 --&gt; 2026-12-02 10:30:00-0300</a></p><p><b>author</b>: <a href=\"PractitionerRole-rol-especialista.html\">Carlos Rojas (official) (http://www.registrocivil.cl/run#33333333-3): Specialist at Servicio de Cardiología (http://especialidad.example.org/organization#CARDIOLOGIA)</a></p><p><b>addresses</b>: <a href=\"Condition-diagnostico-ref-2026-0001.html\">Condition Insuficiencia cardiaca sistólica crónica (FEVI 35%)</a></p><blockquote><p><b>activity</b></p><h3>Details</h3><table class=\"grid\"><tr><td style=\"display: none\">-</td><td><b>Status</b></td><td><b>Description</b></td></tr><tr><td style=\"display: none\">*</td><td>active</td><td>Control en APS en 2 semanas: presión arterial, peso, síntomas.</td></tr></table></blockquote><blockquote><p><b>activity</b></p><h3>Details</h3><table class=\"grid\"><tr><td style=\"display: none\">-</td><td><b>Status</b></td><td><b>Description</b></td></tr><tr><td style=\"display: none\">*</td><td>active</td><td>NT-proBNP de control en 3 meses.</td></tr></table></blockquote><blockquote><p><b>activity</b></p><p><b>reference</b>: <a href=\"ServiceRequest-ref-2026-0001.html\">ServiceRequest Cardiology</a></p></blockquote></div>"
      },
      "status" : "active",
      "intent" : "plan",
      "subject" : {
        "reference" : "Patient/maria-gonzalez"
      },
      "encounter" : {
        "reference" : "Encounter/encuentro-ref-2026-0001"
      },
      "author" : {
        "reference" : "PractitionerRole/rol-especialista"
      },
      "addresses" : [{
        "reference" : "Condition/diagnostico-ref-2026-0001"
      }],
      "activity" : [{
        "detail" : {
          "status" : "active",
          "description" : "Control en APS en 2 semanas: presión arterial, peso, síntomas."
        }
      },
      {
        "detail" : {
          "status" : "active",
          "description" : "NT-proBNP de control en 3 meses."
        }
      },
      {
        "reference" : {
          "reference" : "ServiceRequest/ref-2026-0001"
        }
      }]
    }
  }]
}

```
