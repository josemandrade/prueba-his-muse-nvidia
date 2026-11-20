# Contrareferencia REF-2026-0001 - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Contrareferencia REF-2026-0001**

## Example Composition: Contrareferencia REF-2026-0001

Profile: [Contrareferencia](StructureDefinition-derivacion-contrareferencia.md)

**Identificador de la derivación**: `http://aps.losaromos.example.org/referral`/REF-2026-0001

**identifier**: `http://especialidad.example.org/counter-referral`/CR-2026-0001

**status**: Final

**type**: Consult note

**encounter**: [Encounter: identifier = http://especialidad.example.org/encounter#ENC-2026-0001; status = planned; class = Ambulatory (ActCode#AMB); serviceType = Cardiology; period = 2026-12-02 10:00:00-0300 --> 2026-12-02 10:30:00-0300](Encounter-encuentro-ref-2026-0001.md)

**date**: 2026-12-03 10:00:00-0300

**author**: [Carlos Rojas (official) (http://www.registrocivil.cl/run#33333333-3): Specialist at Servicio de Cardiología (http://especialidad.example.org/organization#CARDIOLOGIA)](PractitionerRole-rol-especialista.md)

**title**: Counter-referral



## Resource Content

```json
{
  "resourceType" : "Composition",
  "id" : "contrareferencia-ref-2026-0001",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-contrareferencia"]
  },
  "extension" : [{
    "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-referral-identifier",
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

```
