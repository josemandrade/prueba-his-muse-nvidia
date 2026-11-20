# Notificación de aceptación a la paciente - Derivación APS → especialidad con contrareferencia v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Notificación de aceptación a la paciente**

## Example Communication: Notificación de aceptación a la paciente

Profile: [Notificación](StructureDefinition-derivacion-notificacion.md)

**Resultado de la entrega**: delivered

**identifier**: `http://aps.losaromos.example.org/notification`/NOTIF-2026-0001

**basedOn**: [Task Referral workflow](Task-tarea-ref-2026-0001.md)

**status**: Completed

**category**: Notification

**medium**: Phone

**subject**: [María González (official) Female, DoB: 1968-04-15 ( http://www.registrocivil.cl/run#11111111-1)](Patient-maria-gonzalez.md)

**topic**: accepted

**sent**: 2026-11-21 09:00:00-0300

**recipient**: [María González (official) Female, DoB: 1968-04-15 ( http://www.registrocivil.cl/run#11111111-1)](Patient-maria-gonzalez.md)

**sender**: [Ana Pérez (official) (http://www.registrocivil.cl/run#22222222-2): APS admin at CESFAM Los Aromos (http://aps.losaromos.example.org/organization#CESFAM-LOS-AROMOS)](PractitionerRole-rol-admin-aps.md)

### Payloads

| | |
| :--- | :--- |
| - | **Content[x]** |
| * | Su derivación a cardiología fue aceptada. Le ofreceremos una cita en los próximos días. |



## Resource Content

```json
{
  "resourceType" : "Communication",
  "id" : "notificacion-aceptacion-ref-2026-0001",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-notificacion"]
  },
  "extension" : [{
    "url" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/StructureDefinition/derivacion-delivery-outcome",
    "valueCode" : "delivered"
  }],
  "identifier" : [{
    "system" : "http://aps.losaromos.example.org/notification",
    "value" : "NOTIF-2026-0001"
  }],
  "basedOn" : [{
    "reference" : "Task/tarea-ref-2026-0001"
  }],
  "status" : "completed",
  "category" : [{
    "coding" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/communication-category",
      "code" : "notification",
      "display" : "Notification"
    }]
  }],
  "medium" : [{
    "coding" : [{
      "system" : "https://josemandrade.github.io/prueba-his-muse-nvidia/derivacion-aps-especialidad/CodeSystem/derivacion-canal",
      "code" : "phone",
      "display" : "Phone"
    }]
  }],
  "subject" : {
    "reference" : "Patient/maria-gonzalez"
  },
  "topic" : {
    "text" : "accepted"
  },
  "sent" : "2026-11-21T09:00:00-03:00",
  "recipient" : [{
    "reference" : "Patient/maria-gonzalez"
  }],
  "sender" : {
    "reference" : "PractitionerRole/rol-admin-aps"
  },
  "payload" : [{
    "contentString" : "Su derivación a cardiología fue aceptada. Le ofreceremos una cita en los próximos días."
  }]
}

```
