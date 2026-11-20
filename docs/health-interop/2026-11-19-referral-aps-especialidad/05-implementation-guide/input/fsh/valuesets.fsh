// Sistemas de códigos y ValueSets propios de esta guía. Los códigos son
// los que el caso de uso exige; ninguno se inventa como estándar: cada
// lista es local, versionada por la red, con su URL canónica en esta guía.

CodeSystem: DerivacionEstadoReferenciaCS
Id: derivacion-estado-referencia
Title: "Estado de la derivación"
Description: "Los nueve estados del caso de la derivación APS → especialidad (spec §3.1). El estado vive en Task.businessStatus, nunca como valor inventado de Task.status."
* #requested "Requested" "Derivación creada por APS, aún no recibida por el hub."
* #received "Received" "Derivación recibida por el hub y enrutada a la especialidad."
* #accepted "Accepted" "La especialidad aceptó la derivación (nombrando servicio y profesional)."
* #rejected "Rejected" "La especialidad rechazó la derivación (con motivo); APS re-triajea."
* #scheduled "Scheduled" "Cita reservada; la visita aún no ha empezado."
* #completed "Completed" "Visita atendida; la contrareferencia está pendiente."
* #counter-referred "Counter-referred" "Contrareferencia enviada y recibida por APS; el ciclo está cerrado."
* #no-show "No-show" "El paciente no asistió dos veces; la derivación se cerró sin completar."
* #cancelled "Cancelled" "Derivación cancelada antes de completarse (por APS, el paciente o la especialidad; también por fallecimiento del paciente)."

ValueSet: DerivacionEstadoReferencia
Id: derivacion-estado-referencia
Title: "Estado de la derivación"
Description: "Estados posibles de una derivación APS → especialidad."
* include codes from system DerivacionEstadoReferenciaCS

CodeSystem: DerivacionRolCS
Id: derivacion-rol
Title: "Rol en la derivación"
Description: "Los seis roles del caso de uso (spec §2). Dentro de una derivación, cada rol es una persona (el clínico de triaje no es el agendador — C1)."
* #aps-doctor "APS doctor" "Médico de APS que crea la derivación."
* #aps-admin "APS admin" "Administrativo de APS que registra y sigue la derivación e informa al paciente."
* #triage-clinician "Triage clinician" "Clínico de la especialidad que acepta o rechaza la derivación."
* #specialty-scheduler "Specialty scheduler" "Agendador de la especialidad que reserva y re-agenda la cita."
* #specialist "Specialist" "Especialista que atiende y emite la contrareferencia."
* #hub-operator "Hub operator" "Operador del hub de derivación (enruta, escala, registra cancelaciones, responde consultas de estado)."

ValueSet: DerivacionRolVS
Id: derivacion-rol
Title: "Rol en la derivación"
Description: "Roles que una persona puede tener en una derivación."
* include codes from system DerivacionRolCS

CodeSystem: DerivacionMotivoRechazoCS
Id: derivacion-motivo-rechazo
Title: "Motivo de rechazo"
Description: "Motivos de rechazo de la derivación (lista local de la especialidad; el texto libre acompaña al código)."
* #missing-exam "Missing exam" "Falta un examen necesario para el triaje (ejemplo trabajado: falta el ecocardiograma)."
* #wrong-specialty "Wrong specialty" "La derivación no corresponde a esta especialidad."
* #capacity "Capacity" "La especialidad no tiene capacidad para atender la derivación en plazo."

ValueSet: DerivacionMotivoRechazo
Id: derivacion-motivo-rechazo
Title: "Motivo de rechazo"
Description: "Motivos por los que la especialidad puede rechazar una derivación."
* include codes from system DerivacionMotivoRechazoCS

CodeSystem: DerivacionCanalCS
Id: derivacion-canal
Title: "Canal de notificación"
Description: "Canales por los que se envía una notificación (lista local; el caso no fija un canal por notificación)."
* #phone "Phone" "Llamada telefónica."
* #in-person "In person" "Aviso presencial."
* #system-message "System message" "Mensaje del sistema (portal o mensajería del EHR)."

ValueSet: DerivacionCanal
Id: derivacion-canal
Title: "Canal de notificación"
Description: "Canales de notificación de la derivación."
* include codes from system DerivacionCanalCS

CodeSystem: DerivacionEspecialidadCS
Id: derivacion-especialidad
Title: "Especialidad / servicio (catálogo local)"
Description: "Catálogo local de especialidades y servicios, versionado por la red (hub + servicios). El ejemplo trabajado es cardiología; la red amplía el catálogo sin tocar esta guía."
* #cardiologia "Cardiology" "Servicio de cardiología (ejemplo trabajado)."

ValueSet: DerivacionEspecialidad
Id: derivacion-especialidad
Title: "Especialidad / servicio (catálogo local)"
Description: "Especialidades y servicios a los que se puede derivar."
* include codes from system DerivacionEspecialidadCS

CodeSystem: DerivacionTaskCodeCS
Id: derivacion-task-code
Title: "Código de la tarea de derivación"
Description: "El Task de esta guía es siempre un registro de flujo de trabajo de derivación."
* #referral-workflow "Referral workflow" "Registro de estado del flujo de trabajo de una derivación."

ValueSet: DerivacionTaskCode
Id: derivacion-task-code
Title: "Código de la tarea de derivación"
Description: "Códigos de Task de esta guía."
* include codes from system DerivacionTaskCodeCS

CodeSystem: DerivacionResultadoEntregaCS
Id: derivacion-resultado-entrega
Title: "Resultado de la entrega de una notificación"
Description: "Resultados posibles de la entrega de una notificación (lista local)."
* #delivered "Delivered" "La notificación llegó al destinatario."
* #failed "Failed" "La entrega falló; el remitente reintenta (el fallo nunca cambia el estado de la derivación)."

ValueSet: DerivacionResultadoEntrega
Id: derivacion-resultado-entrega
Title: "Resultado de la entrega de una notificación"
Description: "Resultados posibles de la entrega de una notificación."
* include codes from system DerivacionResultadoEntregaCS

CodeSystem: DerivacionBaseCruceCS
Id: derivacion-base-cruce
Title: "Base del cruce de identidad"
Description: "Cómo se estableció el cruce de identidad en el MPI (lista local)."
* #identifier "Identifier" "El cruce se estableció por un identificador compartido."
* #demographics "Demographics" "El cruce se estableció por datos demográficos."

ValueSet: DerivacionBaseCruce
Id: derivacion-base-cruce
Title: "Base del cruce de identidad"
Description: "Bases posibles del cruce de identidad en el MPI."
* include codes from system DerivacionBaseCruceCS
