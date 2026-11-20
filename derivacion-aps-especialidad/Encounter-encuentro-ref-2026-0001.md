# Encuentro de especialidad REF-2026-0001 (planned) - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Encuentro de especialidad REF-2026-0001 (planned)**

## Example Encounter: Encuentro de especialidad REF-2026-0001 (planned)

Profile: [Encuentro de especialidad](StructureDefinition-derivacion-encuentro.md)

**identifier**: `http://especialidad.example.org/encounter`/ENC-2026-0001

**status**: Planned

**class**: [ActCode: AMB](http://terminology.hl7.org/7.5.0/CodeSystem-v3-ActCode.html#v3-ActCode-AMB) (Ambulatory)

**serviceType**: Cardiology

**subject**: [María González (official) Female, DoB: 1968-04-15 ( http://www.registrocivil.cl/run#11111111-1)](Patient-maria-gonzalez.md)

**basedOn**: [ServiceRequest Cardiology](ServiceRequest-ref-2026-0001.md)

### Participants

| | |
| :--- | :--- |
| - | **Individual** |
| * | [Carlos Rojas (official) (http://www.registrocivil.cl/run#33333333-3): Specialist at Servicio de Cardiología (http://especialidad.example.org/organization#CARDIOLOGIA)](PractitionerRole-rol-especialista.md) |

**appointment**: [Appointment: extension = 1; identifier = http://especialidad.example.org/appointment#CITA-2026-0001; status = proposed; serviceType = Cardiology; start = 2026-12-02 10:00:00-0300; end = 2026-12-02 10:30:00-0300; created = 2026-11-24 11:00:00-0300; patientInstruction = Ayuno no necesario. Traer los exámenes previos.](Appointment-cita-ref-2026-0001.md)

**period**: 2026-12-02 10:00:00-0300 --> 2026-12-02 10:30:00-0300



## Resource Content

```json
{
  "resourceType" : "Encounter",
  "id" : "encuentro-ref-2026-0001",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-encuentro"]
  },
  "identifier" : [{
    "system" : "http://especialidad.example.org/encounter",
    "value" : "ENC-2026-0001"
  }],
  "status" : "planned",
  "class" : {
    "system" : "http://terminology.hl7.org/CodeSystem/v3-ActCode",
    "code" : "AMB",
    "display" : "Ambulatory"
  },
  "serviceType" : {
    "coding" : [{
      "system" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/CodeSystem/derivacion-especialidad",
      "code" : "cardiologia",
      "display" : "Cardiology"
    }]
  },
  "subject" : {
    "reference" : "Patient/maria-gonzalez"
  },
  "basedOn" : [{
    "reference" : "ServiceRequest/ref-2026-0001"
  }],
  "participant" : [{
    "individual" : {
      "reference" : "PractitionerRole/rol-especialista"
    }
  }],
  "appointment" : [{
    "reference" : "Appointment/cita-ref-2026-0001"
  }],
  "period" : {
    "start" : "2026-12-02T10:00:00-03:00",
    "end" : "2026-12-02T10:30:00-03:00"
  }
}

```
