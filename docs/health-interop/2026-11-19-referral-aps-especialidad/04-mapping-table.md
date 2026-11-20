# Mapping Table: Derivación APS → especialidad con contrareferencia

Companion to `04-fhir-proposal.md` (step 4, FHIR R4). Every entity
from `03-entities-data.md` (§1–§13) maps to exactly one FHIR R4
resource, except where the table honestly says "no FHIR equivalent".
Entity names are the step 3 names; field names are the step 3 field
names. Case-language states (e.g. `offered`, `scheduled`) are mapped
to the R4 value-set values — never invented. R4 value sets verified
live 2026-11-19 at hl7.org/fhir/R4: `AppointmentStatus` (10 values,
Required), `TaskStatus` (12 values, Required), `EncounterStatus`
(9 values, Required — no `scheduled`; the value is `planned`),
`RequestStatus` (7 values, Required).

Conventions used in this table:

- **Profile**: our own profile, named `Derivacion*` (Spanish, as in
  the DAU case's `DAUPaciente` / `EncuentroUrgenciaAlta`); base =
  the FHIR R4 base resource (canonical URL stated in
  `04-fhir-proposal.md`). The user may choose a different base for
  any profile (e.g. `CorePacienteCl` for `Patient`).
- **businessStatus**: the `Task.businessStatus` carries the case
  state verbatim (local ValueSet `DerivacionEstadoReferencia`);
  `Task.status` carries the coarse R4 mapping. The Task is the
  authority for where the referral stands; `ServiceRequest.status`
  is a coarse mirror, kept consistent.
- **Extension**: local extensions live under
  `http://derivacion.example.org/fhir/StructureDefinition/` (guide's
  own namespace; the canonical base URL is fixed in step 5 when the
  guide's canonical is set). An extension is used only where no base
  field carries the meaning.
- **No FHIR equivalent**: the honest answer for an entity or field
  that travels in no FHIR resource in this design.

## 1. Patient → Patient (`DerivacionPaciente`)

Base: `http://hl7.org/fhir/StructureDefinition/Patient`.
Alternative base offered: `CorePacienteCl`
(`https://hl7chile.cl/fhir/ig/clcore/StructureDefinition/CorePacienteCl`).

| Step 3 field | FHIR element | Cardinality / binding | Notes |
|---|---|---|---|
| MPI key | `Patient.identifier` (system = MPI, e.g. `http://mpi.red.example.org`) | 0..* | The cross-organisation key; the identifier that travels. |
| Full name | `Patient.name` (HumanName, `use = official`) | 0..* | Structured text. |
| Date of birth / age | `Patient.birthDate` | 0..1 | Age is derived, never stored. |
| National identifier (RUN) | `Patient.identifier` (system = RUN, e.g. `http://www.registrocivil.cl/run`) | 0..* | Synthetic in examples (11.111.111-1). |
| Contact data (phone, address, preferred channel) | `Patient.telecom` (phone / email) + `Patient.address` | 0..* | Required (C12). Missing contact data blocks creation. Preferred channel: `Patient.telecom.use` + a local extension `preferred-contact-channel` (phone / in-person / system-message) — no base field carries the channel preference. |
| Sex / gender as recorded | `Patient.gender` | 0..1, Required binding (`AdministrativeGender`) | `male \| female \| other \| unknown`. |

Rejected alternative: a separate `RelatedPerson` for the patient —
the patient is the subject, never a related person. The MPI identity
record (§10) is the MPI's own `Patient` resource, not a second
patient record in the flow.

## 2. Referral request → ServiceRequest (`DerivacionSolicitud`)

Base: `http://hl7.org/fhir/StructureDefinition/ServiceRequest`.
`intent = order` (1..1). One `ServiceRequest` per referral.

| Step 3 field | FHIR element | Cardinality / binding | Notes |
|---|---|---|---|
| Referral identifier | `ServiceRequest.identifier` | 0..* | Created by APS at creation; persistent until the loop closes (the 360X persistent identifier). Dedup key with the MPI key. |
| Patient (MPI key + contact data) | `ServiceRequest.subject` → Patient (§1) | 1..1 | The patient is linked, not copied; contact data travels on the Patient. |
| Reason for referral | `ServiceRequest.reasonCode` (SNOMED CT 84114007 "Heart failure (disorder)" + free-text note) + `ServiceRequest.code` | `reasonCode` 0..*, Example binding; `code` 0..1, Example binding | `code` = the requested service (local specialty/service catalogue, §9) — the referral asks for a service, and `code` carries what is requested. `reasonCode` carries why. |
| Clinical summary | `ServiceRequest.supportingInfo` → Composition / DocumentReference / Observation (the APS clinical summary) + `ServiceRequest.note` (free-text note) | 0..* | The summary travels as supporting information, not as a single text field. The worked example's summary is the APS encounter note (narrative + the §2 exams). |
| Relevant exams / results | `ServiceRequest.supportingInfo` → Observation / DiagnosticReport (LOINC-coded) | 0..* | Worked example: ECG → Observation `code` LOINC 11524-6 "EKG study"; NT-proBNP → Observation `code` LOINC 33762-6, value in pg/mL (UCUM). Attachments by reference (`DocumentReference`). |
| Requesting practitioner | `ServiceRequest.requester` → PractitionerRole (§8) | 0..1 | The APS doctor in the requesting role. |
| Requested specialty / service | `ServiceRequest.performerType` (local specialty/service catalogue) + `ServiceRequest.performer` → HealthcareService (§9) | `performerType` 0..1, Example binding; `performer` 0..* | `performerType` names the requested specialty; `performer` names the service once routed. |
| Priority | `ServiceRequest.priority` | 0..1, Required binding (`RequestPriority`: `routine \| urgent \| asap \| stat`) | `routine` / `urgent` (C6/Q6); urgent halves the acceptance SLA. No local ValueSet needed — the R4 values cover the case. |
| Creation date/time | `ServiceRequest.authoredOn` | 0..1 | Stamped at creation; the acceptance clock starts here. |

`ServiceRequest.status` (Required, `RequestStatus`, 7 values) is the
coarse mirror of the workflow record — never the authority:

| Case state (§2/§3) | `ServiceRequest.status` | Rule |
|---|---|---|
| `draft` | `draft` | Being written in the APS encounter. |
| `requested`, `received`, `accepted`, `scheduled`, `completed` | `active` | The request is in force; the fine state lives on the Task. |
| `rejected` (re-triage pending) | `active` | The request is in force until APS decides the re-triage outcome. |
| `rejected` (closed) | `revoked` | The APS re-triage decision closes the referral as `rejected`; the hub revokes the ServiceRequest in the same transaction as the Task's terminal `rejected` (a re-referral is a NEW ServiceRequest). |
| `counter-referred` | `completed` | The specialty assessment was fully performed. |
| `no-show` (terminal) | `revoked` | Closed without completion; reason on the Task (`statusReason`). |
| `cancelled` | `revoked` | Terminated before full completion; reason on the Task. |

`ServiceRequest` has no `statusReason` — the reason always travels
on the `Task.statusReason` and/or the cancelling
`Appointment.cancelationReason`. Rejection is never put on
`ServiceRequest.status` (the pack rule: never put accept/reject on
the request status). Correction by a new version: same identifier,
`ServiceRequest.replaces` → the previous version, version number
+1; never edited in place. A re-referral after rejection is a NEW
`ServiceRequest` (new identifier), not a correction.

Rejected alternatives: `ReferralRequest` (merged into
`ServiceRequest` in R4 — must never be proposed); `CarePlan` (the
referral is a request for a service, not a plan); `Task` alone (the
request and the workflow record are different entities — spec §8).

## 3. Workflow state record → Task (`DerivacionTarea`) — CENTRE

Base: `http://hl7.org/fhir/StructureDefinition/Task`. This is the
centre of the resource graph: it carries the workflow state, and
every later step reads it first. `focus` → ServiceRequest (§2),
`intent = order`, `for` → Patient (§1).

| Step 3 field | FHIR element | Cardinality / binding | Notes |
|---|---|---|---|
| Referral identifier | `Task.identifier` (same value as `ServiceRequest.identifier`) | 0..* | The join key between request and workflow record. |
| Current state | `Task.status` (R4 coarse mapping, table below) + `Task.businessStatus` (case state verbatim, local ValueSet `DerivacionEstadoReferencia`) | `status` 1..1, Required; `businessStatus` 1..1, Example binding, constrained to the local ValueSet | The case state list is the case's own vocabulary, not a standard — it lives in `businessStatus`, never as an invented `status` value. |
| State history | `Task.relevantHistory` → Provenance (one per transition: who, when, from, to, reason) | 0..* | Append-only. The history is the audit trail; states are never edited in place. |
| Last state change | `Task.lastModified` | 0..1 | Derived from the latest Provenance entry. |
| Next expected step | `Task.description` (short text, e.g. "acceptance decision", "appointment offer", "counter-referral") | 0..1 | Derived from the current state. |
| Acceptance deadline | Extension `sla-acceptance-deadline` (dateTime) on Task | 0..1 | Derived: creation + 5 working days (2 if urgent). |
| Offer deadline | Extension `sla-offer-deadline` (dateTime) on Task | 0..1 | Derived: acceptance + 10 working days. |
| Counter-referral deadline | Extension `sla-counterreferral-deadline` (dateTime) on Task | 0..1 | Derived: encounter + 5 working days. |
| Re-triage deadline | Extension `sla-retriage-deadline` (dateTime) on Task | 0..1 | Derived: rejection (or scheduling-failure return) + 5 working days. |
| Confirmation deadline | Extension `sla-confirmation-deadline` (dateTime) on Task | 0..1 | Derived: offer + 3 working days; present while an offer is open. |
| Decline count (this offer) | Extension `offer-decline-count` (integer, 0–2) on Task | 0..1 | Resets per offer (N5). |
| Chase count (this offer) | Extension `offer-chase-count` (integer, 0–2) on Task | 0..1 | Resets per offer (N5). |
| Re-scheduling count | Extension `rescheduling-count` (integer, 0–1) on Task | 0..1 | Does not reset (one re-scheduling per referral). |
| Escalation history | `Task.note` (Annotation: SLA breached, escalated to, timestamp) + Provenance | 0..* | A breach is a note + a Provenance entry, not a state. |
| Accepting service / practitioner | `Task.owner` → HealthcareService (§9) / PractitionerRole (§8) | 0..* | Set at acceptance; the accepting service and practitioner. |
| Rejection reason | `Task.statusReason` (local rejection-reason list: "missing exam", "wrong specialty", "capacity" + free text) | 0..1, Example binding | Required when `rejected`. |
| Cancellation reason | `Task.statusReason` (coded + free text; "patient deceased" included) | 0..1 | Required when `cancelled`. |
| Routing (requested specialty service + endpoint) | `Task.owner` → HealthcareService (§9) + `Task.location` → Location / Endpoint (directory) | 0..* / 0..1 | The hub's routing decision, from the mCSD directory. |

Case state → `Task.status` (R4 `TaskStatus`, 12 values, Required):

| Case state | `Task.status` | `businessStatus` |
|---|---|---|
| `requested` | `requested` | `requested` |
| `received` | `received` | `received` |
| `accepted` | `accepted` | `accepted` |
| `rejected` | `rejected` | `rejected` |
| `scheduled` | `ready` | `scheduled` |
| `completed` | `in-progress` | `completed` |
| `counter-referred` | `completed` | `counter-referred` |
| `no-show` | `failed` | `no-show` |
| `cancelled` | `cancelled` | `cancelled` |

`scheduled` → `ready` ("the task is ready to be performed, but no
action has yet been taken" — the appointment is booked, the visit
has not started). `completed` (visit attended, counter-referral
due) → `in-progress` (the work is started but not complete — the
counter-referral is still owed). `no-show` → `failed` ("the task
was attempted but could not be completed") with `statusReason`
"patient did not attend twice". The full lifecycle table with
allowed / forbidden transitions and the operation + PI per
transition is in `04-fhir-proposal.md` (§ Lifecycle tables).

The `draft` Task status is not used for the referral workflow
record: the record is created `requested` at PI-0. `on-hold` is
not used either: a medical suspension of the referral is a
cancellation + re-referral in this case, never a hold (the case has
no hold step). `entered-in-error` is reserved for a workflow
record that should never have existed (voided, retained for audit).

Correction of a wrong state: a compensating transition recorded as
a new Provenance entry (who, when, from, to, reason); the history
is append-only. Cancellation recorded in error is undone only by
re-opening to the pre-cancellation state with an explicit re-open
entry (hub operator performs it; APS and the specialty are
notified).

## 4. Triage decision → Task transition + Provenance (no separate resource)

The triage decision is not a resource of its own: it is the Task
transition (`accepted` / `rejected`) with its data. One triage
decision per referral; a re-triage after rejection belongs to a NEW
referral.

| Step 3 field | FHIR element | Cardinality / binding | Notes |
|---|---|---|---|
| Referral identifier | `Task.identifier` (§3) | 0..* | Join key. |
| Decision | `Task.status` (`accepted` / `rejected`) | 1..1, Required | The decision IS the transition. No separate decision resource. |
| Accepting service | `Task.owner` → HealthcareService (§9, local catalogue) | 0..* | Required when `accept`. |
| Accepting practitioner | `Task.owner` → PractitionerRole (§8) | 0..* | Required when `accept`. |
| Rejection reason | `Task.statusReason` (local rejection-reason list + free text) | 0..1 | Required when `reject`. Worked example: "missing echocardiogram". |
| Decision date/time | `Task.lastModified` + Provenance.recorded | 0..1 | Stamped at decision. |
| Triage notes | `Task.note` (Annotation) | 0..* | Free text. |

Supersession: a wrong decision is corrected by a new decision entry
that supersedes it (same referral identifier, Provenance entry with
the reason); the workflow record notes the supersession.
Supersession corrects recorded data (e.g. the accepting
practitioner); a reversal of the decision itself goes through
cancellation (§13), not supersession. The triage clinician is the
only actor who may record or supersede the decision (C1).

Rejected alternative: a `ClinicalImpression` for the triage
decision — it records an assessment, not a workflow decision; the
decision belongs on the Task that carries the workflow state.

## 5. Appointment (+ Slot) → Appointment + Slot (+ Schedule) (`DerivacionCita`)

Base: `http://hl7.org/fhir/StructureDefinition/Appointment`,
`http://hl7.org/fhir/StructureDefinition/Slot`,
`http://hl7.org/fhir/StructureDefinition/Schedule`.

| Step 3 field | FHIR element | Cardinality / binding | Notes |
|---|---|---|---|
| Appointment identifier | `Appointment.identifier` | 0..* | Specialty-created. A re-offer is a NEW Appointment (new identifier, C2); the declined offer's appointment goes to `cancelled`. |
| Slot identifier | `Appointment.slot` → Slot; `Slot.identifier` | 0..* | Required once booked. `Slot.status`: `busy` (booked) → `free` (no-show, cancel, re-schedule). |
| Referral identifier | `Appointment.basedOn` → ServiceRequest (§2) | 0..* | The join key. |
| Date / time | `Appointment.start` / `Appointment.end` | 0..1 each (required except for `proposed` / `cancelled` / `waitlist`, R4 app-3) | From the specialty availability (`Schedule` + `Slot`). |
| Place (service, room) | `Appointment.participant.actor` → Location + `Appointment.serviceType` (local location list) | 0..* | The service is the specialty service; the room is a Location. |
| Preparation instructions | `Appointment.patientInstruction` | 0..1 | May be "none". |
| Offer date/time | `Appointment.created` | 0..1 | Stamped at offer. |
| Confirmation status | `AppointmentResponse.participantStatus` (`needs-action` / `accepted` / `declined` / `tentative`) on the patient's `AppointmentResponse` | 1..1, Required binding | The patient's decision lives on the `AppointmentResponse`, distinct from referral acceptance (`Task.status`). |
| Confirmation deadline | Extension `sla-confirmation-deadline` on the Task (§3); `AppointmentResponse` carries no deadline | — | The deadline is workflow state, held by the hub (§3). |
| Offer number (this referral) | Extension `offer-number` (integer) on Appointment | 0..1 | Per-referral counter (1st offer, re-offer). |

Case state → `Appointment.status` (R4 `AppointmentStatus`, 10
values, Required):

| Case state (§5) | `Appointment.status` | Rule |
|---|---|---|
| `offered` | `proposed` | "None of the participant(s) have finalized their acceptance" — the offer is out, the patient has not confirmed. `AppointmentResponse.participantStatus = needs-action`. |
| `confirmed` | `pending` | "Some or all of the participant(s) have not finalized their acceptance" — the patient has confirmed (`AppointmentResponse.participantStatus = accepted`) but the slot is not yet finally booked. |
| `booked` | `booked` | "All participant(s) have been considered and the appointment is confirmed to go ahead" — the Slot is `busy`. |
| `re-scheduled` | `booked` (same Appointment, new Slot, version +1) after a pre-attendance conflict; a NEW Appointment (`proposed`) after a no-show | A conflict before the appointment date re-books the same Appointment onto a new Slot. A no-show closes the old Appointment (`noshow`) and the re-scheduled offer is a new Appointment — it goes through the same confirm/chase loop (N5), with its own confirmation deadline and its own decline/chase counts. |
| `attended` | `arrived`, then `fulfilled` | `arrived` when the patient arrives; `fulfilled` when the encounter finishes ("the encounter resource will exist and will track further status changes"). |
| `no-show` | `noshow` | `cancelationReason` = "patient did not attend"; the Slot returns to `free`. |
| `cancelled` | `cancelled` | `cancelationReason` carries the reason (R4 permits it for cancelled or no-show appointments). |

There is no `offered`, `confirmed`, `re-offered` or `attended`
value in R4 `Appointment.status` — the case states above are the
mapping, not FHIR values. A confirmation arriving after the
confirmation deadline but before the scheduler has chased is still
accepted (the deadline triggers a chase, not a closure); a
confirmation arriving after the referral has returned to APS
re-triage is rejected — the offer is dead. A booking for a slot
already taken is rejected by the specialty schedule.

Rejected alternative: modeling the offer as an `Encounter` — an
offer is not a visit; the encounter is created only when the
patient attends (§6).

## 6. Specialty encounter → Encounter (`DerivacionEncuentro`)

Base: `http://hl7.org/fhir/StructureDefinition/Encounter`.

| Step 3 field | FHIR element | Cardinality / binding | Notes |
|---|---|---|---|
| Encounter identifier | `Encounter.identifier` | 0..* | Specialty-created. |
| Appointment identifier | `Encounter.appointment` → Appointment (§5) | 0..1 | Links the visit to its booking. |
| Referral identifier | `Encounter.basedOn` → ServiceRequest (§2) | 0..* | Links the visit to the referral. |
| Date / time (actual) | `Encounter.period` | 0..1 | Actual visit period. |
| Attending specialist | `Encounter.participant.individual` → PractitionerRole (§8, specialist) | 0..* | The specialist who attended. |
| Encounter notes | `Encounter.note` / the counter-referral Composition (§7) | 0..* | Visit notes; the clinical output is the counter-referral, not a note. |

Also set: `Encounter.subject` → Patient (§1, 0..1),
`Encounter.class` = `AMB` (ambulatory, v3 ActEncounterCode —
outpatient specialty consultation; binding Extensible),
`Encounter.serviceType` = the specialty service (local catalogue),
`Encounter.statusHistory` for the branch history.

Case state → `Encounter.status` (R4 `EncounterStatus`, 9 values,
Required — no `scheduled`; the value is `planned`):

| Case state (§6) | `Encounter.status` | Rule |
|---|---|---|
| `scheduled` (appointment booked) | `planned` | "The Encounter has not yet started." The Encounter exists from booking; it is not created at attendance. |
| `in-progress` (patient attended) | `in-progress` | The patient is present and meeting the specialist. (`arrived` is the brief waiting state between arrival and the start of the visit; the case does not model it separately.) |
| `finished` (visit done, counter-referral due) | `finished` | The Encounter has ended; the counter-referral clock runs. |

No Encounter is created when the patient does not attend — the
no-show lives on the Appointment only (§5). There is no `cancelled`
encounter state and no encounter-level attendance field: attendance
is recorded once, on the Appointment (`arrived` / `noshow`). An
encounter recorded in error is corrected by voiding it (`status =
entered-in-error` + a replacement Encounter, never an overwrite);
the workflow record is notified so the counter-referral clock
follows the replacement. The APS encounter that created the
referral exists in the APS EHR and is linked by
`ServiceRequest.encounter` → that Encounter; it is not re-modeled
here.

Rejected alternative: one Encounter per referral spanning both
visits — the referral spans several encounters (APS visit,
specialty visit), each its own Encounter, all linked to the
referral by `basedOn`.

## 7. Counter-referral → Composition + DocumentReference + Condition + CarePlan (`DerivacionContrareferencia`)

Base: `http://hl7.org/fhir/StructureDefinition/Composition`,
`http://hl7.org/fhir/StructureDefinition/DocumentReference`,
`http://hl7.org/fhir/StructureDefinition/Condition`,
`http://hl7.org/fhir/StructureDefinition/CarePlan`.

The counter-referral travels as a FHIR document (a document
Bundle whose first entry is the Composition), so MHD can carry it
and APS can acknowledge receipt of the document. The Composition
is the document; the DocumentReference is the index entry for it;
the Condition and the CarePlan are the computable clinical
content, referenced as Composition section entries.

**Composition (`DerivacionContrareferencia`)**

| Step 3 field | FHIR element | Cardinality / binding | Notes |
|---|---|---|---|
| Counter-referral identifier | `Composition.identifier` | 0..1 | Specialty-created. |
| Referral identifier | Extension `referral-identifier` (Identifier) on Composition | 0..1 | The join key. No base field carries the referral id on a Composition — the link also travels via `DocumentReference.context.related` → ServiceRequest (below). |
| Specialty encounter identifier | `Composition.encounter` → Encounter (§6) | 0..1 | Links the document to the visit. |
| Diagnosis | Composition section "Diagnosis" (narrative) + entry → Condition (below) | — | The section carries the diagnosis as the specialist wrote it; the Condition carries it coded. |
| Plan | Composition section "Plan" (narrative) + entry → CarePlan (below) | — | — |
| Follow-up indications | Composition section "Follow-up indications" (narrative) | — | Free text, as the specialist wrote it. |
| Follow-up plan for APS | Composition section "Follow-up plan for APS" (narrative) + entry → CarePlan (below) | — | The part APS acts on: controls, exams, or a new referral. |
| Issue date/time | `Composition.date` | 1..1 | Stamped at sending. |
| Receipt acknowledgement (APS) | Not on the Composition — see DocumentReference below | — | Acknowledgement is a Communication (§11), not a Composition field. |

Also set: `Composition.status` = `final` (Required,
`CompositionStatus`: `preliminary | final | amended |
entered-in-error`), `Composition.type` = LOINC 11488-4 "Consult
note" (verified live 2026-11-19 at loinc.org: "A consultation note
is generated by a provider upon request for an opinion or advice
from another provider… typically sent to the referring provider
when the consultation is completed" — Active, v2.73; the
cardiology-specific variant is LOINC 34099-2 "Cardiology Consult
Note", used in the worked example), `Composition.subject` →
Patient (§1), `Composition.author` → PractitionerRole (§8,
specialist), `Composition.title` = "Counter-referral".

**DocumentReference (`DerivacionDocumento`)**

| Step 3 field | FHIR element | Cardinality / binding | Notes |
|---|---|---|---|
| Counter-referral identifier | `DocumentReference.masterIdentifier` | 0..1 | Same value as `Composition.identifier`. |
| Referral identifier | `DocumentReference.context.related` → ServiceRequest (§2) | 0..* | The link from the document to the referral. |
| Specialty encounter identifier | `DocumentReference.context.encounter` → Encounter (§6) | 0..* | — |
| Issue date/time | `DocumentReference.date` | 0..1 | Stamped at sending. |
| Receipt acknowledgement (APS) | `DocumentReference` has no acknowledgement field — APS acknowledges receipt with a Communication (§11, `basedOn` → Task, `payload.contentReference` → DocumentReference) | — | The acknowledgement is a separate message, not a document field. |

Also set: `DocumentReference.status` = `current` (Required,
`DocumentReferenceStatus`: `current | superseded |
entered-in-error`), `DocumentReference.type` = LOINC 11488-4
"Consult note", `DocumentReference.subject` → Patient (§1),
`DocumentReference.author` → PractitionerRole (§8, specialist),
`DocumentReference.content.attachment.url` → the Composition
(`[base]/Composition/{id}` — the document itself),
`DocumentReference.content.attachment.contentType` =
`application/fhir+json`, `DocumentReference.context.period` =
the encounter period.

A wrong counter-referral is corrected by a new version: same
identifier, `DocumentReference.status` of the old version →
`superseded` (never overwrite), new version `relatesTo` (`code =
replaces`) → the old DocumentReference; APS is notified of the
supersession. A second counter-referral is a correction, not a
second return.

**Condition (`DerivacionDiagnostico`) — the diagnosis entry**

| Step 3 field | FHIR element | Cardinality / binding | Notes |
|---|---|---|---|
| Diagnosis | `Condition.code` (ICD-10-CM I50.22 "Chronic systolic (congestive) heart failure" — billable 5-character code; I50.2 itself is a non-billable category header) + SNOMED CT 417996009 "Systolic heart failure" as the second coding) + `Condition.note` (free-text note) | 0..1, Example binding | Worked example: heart failure with reduced ejection fraction. ICD-10-CM I50.22 verified 2026-11-19 (ICD-10-CM coding references); Chile uses WHO ICD-10, in which no systolic-specific code exists (I50 has only I50.0 / I50.1 / I50.9), so the SNOMED CT second coding carries the precise meaning. SNOMED CT 417996009 per the pack's standing ruling (verified in prior audit work). |
| — | `Condition.subject` → Patient (§1); `Condition.encounter` → Encounter (§6); `Condition.clinicalStatus` = `active`; `Condition.verificationStatus` = `confirmed` | — | The diagnosis is confirmed at the specialty visit. |

**CarePlan (`DerivacionPlanSeguimiento`) — the follow-up plan entry**

| Step 3 field | FHIR element | Cardinality / binding | Notes |
|---|---|---|---|
| Plan | `CarePlan.activity` with `detail` (narrative plan, structured sections) | 0..* | The specialist's plan as activities. |
| Follow-up indications | `CarePlan.activity.detail` (text + `code`, SNOMED CT, Example) | 0..* | Each indication is one activity. |
| Follow-up plan for APS | `CarePlan` itself + `CarePlan.activity.reference` → ServiceRequest (a new referral if another specialty is needed) / Appointment (a control) / Task | 0..* | `activity` uses `reference` OR `detail`, never both; prefer `reference` to the follow-up request/appointment. |

Also set: `CarePlan.status` = `active` (Required,
`RequestStatus`), `CarePlan.intent` = `plan` (Required, 1..1 ∈
{`proposal`, `plan`, `order`, `option`} — no `directive` in R4),
`CarePlan.subject` → Patient (§1), `CarePlan.encounter` →
Encounter (§6), `CarePlan.author` → PractitionerRole (§8,
specialist), `CarePlan.addresses` → Condition (the diagnosis
above). A plan update is a new version linked by `replaces` /
`basedOn` to the previous version — never a silent overwrite.

Lifecycle of the counter-referral (§7): `draft` (specialist
writing — `Composition.status = preliminary`) → `sent` (pushed
via hub — `Composition.status = final`, `DocumentReference.status
= current`) → `received` (APS acknowledges receipt — the final
state; the referral is `counter-referred`). A counter-referral
arriving after its deadline is still accepted — the deadline
triggers escalation, not rejection. A counter-referral for a
referral already `cancelled` is rejected by the hub.

## 8. Practitioner → Practitioner + PractitionerRole (`DerivacionRol`)

Base: `http://hl7.org/fhir/StructureDefinition/Practitioner`,
`http://hl7.org/fhir/StructureDefinition/PractitionerRole`.

| Step 3 field | FHIR element | Cardinality / binding | Notes |
|---|---|---|---|
| Practitioner identifier | `Practitioner.identifier` (organisation-local) | 0..* | — |
| Name | `Practitioner.name` (HumanName) | 0..* | Structured text. |
| Role in this referral | `PractitionerRole.code` (local ValueSet `DerivacionRol`: APS doctor / APS admin / triage clinician / specialty scheduler / specialist / hub operator) | 0..* | One of the six roles per referral; one person may hold more than one role across referrals, but within one referral each role is one person. |
| Organisation | `PractitionerRole.organization` → Organization (§9) | 0..1 | The practitioner's own organisation. |
| Contact (for the role's notifications) | `PractitionerRole.telecom` | 0..* | Optional. |

Also set: `PractitionerRole.practitioner` → Practitioner,
`PractitionerRole.active` = `true` while the person holds the
role. A referral naming a practitioner who has left is corrected
by the owning organisation re-assigning the step to another
practitioner of the same role, recorded in the workflow record
history (Provenance). The hub operator is a PractitionerRole
(organisation = referral hub) — hub transitions are human-operated
(C1), so the §3 state-history "actor" field has a defined value.

## 9. Organisation / care service → Organization + HealthcareService + Location + Endpoint (`DerivacionServicio`)

Base: `http://hl7.org/fhir/StructureDefinition/Organization`,
`http://hl7.org/fhir/StructureDefinition/HealthcareService`,
`http://hl7.org/fhir/StructureDefinition/Location`,
`http://hl7.org/fhir/StructureDefinition/Endpoint`.

| Step 3 field | FHIR element | Cardinality / binding | Notes |
|---|---|---|---|
| Organisation identifier | `Organization.identifier` | 0..* | — |
| Organisation name | `Organization.name` | 0..1 | APS (CESFAM Los Aromos), specialty service organisation, referral hub. |
| Care-service identifier | `HealthcareService.identifier` (local specialty/service catalogue) | 0..* | The requested / accepting service. |
| Care-service name | `HealthcareService.name` | 0..1 | e.g. "Cardiology". |
| Endpoint (where the hub sends the referral) | `HealthcareService.endpoint` → Endpoint (`Endpoint.address`, `Endpoint.connectionType` = `hl7-fhir-rest`) | 0..* | Required for routing; the hub reads it from the directory (mCSD ITI-90). |
| Accepting referrals? | `HealthcareService.active` (boolean) | 0..1 | Derived from the directory: the hub routes only to services the directory lists as accepting. |

Also set: `HealthcareService.providedBy` → Organization,
`HealthcareService.type` = the specialty (local catalogue),
`HealthcareService.location` → Location (where the service is
delivered). The specialty/service catalogue is a local code
system (`http://derivacion.example.org/fhir/CodeSystem/especialidad`,
versioned by the network); step 4 records its codes, it does not
invent a standard one. A service that stops accepting referrals is
a directory change — the hub re-reads the directory on each
routing decision.

## 10. MPI identity record → Patient (MPI's golden record) + Provenance + PIXm/PMIR transactions

The MPI identity record is not exchanged as a resource in the
referral flow: it is the MPI's internal record, represented by the
MPI's `Patient` resource and queried/fed through IHE
transactions. The flow uses the transactions, not a resource
exchange.

| Step 3 field | FHIR element | Cardinality / binding | Notes |
|---|---|---|---|
| MPI key | `Patient.identifier` (MPI system) on the MPI's Patient | 0..* | The cross-organisation key; the same identifier travels on the referral's Patient (§1). |
| Local identifiers (one per organisation) | `Patient.identifier` (one per organisation, each with its own system) on the MPI's Patient | 0..* | At least the APS one. |
| Match basis (identifier / demographics) | Extension `match-basis` (code: identifier / demographics) on the MPI's Patient | 0..1 | How the cross-reference was established. |
| Match confidence | Extension `match-confidence` (decimal 0–1) on the MPI's Patient | 0..1 | Optional. |
| Merge history | `Patient.link` (`type = replaced-by`, `other` → the surviving Patient) + Provenance (target → Patient, activity = merge, agent, recorded) | 0..* | A merge never deletes a local identifier — it links it to the surviving MPI key, so a referral that travelled with the old key still resolves. |

Transactions (IHE, see `04-fhir-proposal.md` § IHE review):
PIXm ITI-83 (`GET [base]/Patient/$ihe-pix`) resolves the MPI key
before creation; PDQm ITI-78 finds the patient by demographics;
PMIR ITI-93 is the MPI-side identity feed (create/update/delete/
merge of the golden Patient). An identity feed arriving after the
referral was created is applied to the workflow state record (the
MPI key is updated); the referral itself is not re-created.

## 11. Notification → Communication (`DerivacionNotificacion`)

Base: `http://hl7.org/fhir/StructureDefinition/Communication`.
A notification is a record of a send, not the message content
itself.

| Step 3 field | FHIR element | Cardinality / binding | Notes |
|---|---|---|---|
| Notification identifier | `Communication.identifier` | 0..* | Sender-created. |
| Referral identifier | `Communication.basedOn` → Task (§3) | 0..* | The join key — the notification is about a referral workflow record. |
| Sender (named) | `Communication.sender` → PractitionerRole (§8) / Organization (§9) | 0..1 | APS admin / specialty scheduler (via hub) / specialist / hub. |
| Recipient | `Communication.recipient` → Patient (§1) / PractitionerRole (§8) | 0..* | Patient / APS admin / APS doctor / specialty. |
| Triggering state change | `Communication.topic` → Task (§3) + `Communication.payload.contentString` (e.g. "state changed to accepted") | 0..* / 0..* | The transition that triggered the send; the Task carries the state, the payload carries the human-readable notice. |
| Channel | `Communication.medium` (local channel list: phone / in person / system message) | 0..* | Example binding (`CommunicationMedium` is not a closed list in R4 — the local list is recorded as the guide's ValueSet). |
| Sent date/time | `Communication.sent` | 0..1 | Stamped at send. |
| Delivery outcome | Extension `delivery-outcome` (code: `delivered` / `failed`) on Communication | 0..1 | R4 `Communication.status` has no delivered/failed — `status = completed` means sent; the delivery outcome is an extension. A failed delivery is re-tried by the sender; a failed notification never changes the referral state. |

Also set: `Communication.status` = `completed` (Required,
`EventStatus`), `Communication.subject` → Patient (§1),
`Communication.category` = `notification`
(`CommunicationCategory`, Example binding). A notification sent in
error is corrected by a new Communication stating the correction
("the previous notice was wrong; the state is X") — never by
deleting the sent record. A notification arriving after the
referral has moved on is still delivered with its original
timestamp.

Named senders (C5/Q3): referral creation → APS admin informs the
patient; acceptance/rejection → APS admin informs the patient;
appointment offer → specialty scheduler sends it via the hub, APS
admin is notified of the offer; counter-referral outcome → APS
admin informs the patient. Escalations are also notifications
(hub → specialty + APS on SLA breach; hub → APS on re-triage
timeout).

## 12. Declined-referral record → no FHIR equivalent (local APS record)

| Step 3 field | FHIR element | Notes |
|---|---|---|
| All fields | **No FHIR equivalent — local APS record** | The patient declines the referral itself at creation: NO referral is created, no referral identifier exists, nothing travels to the hub or the specialty. There is deliberately no resource to exchange. The APS EHR keeps the record internally (APS record identifier, patient MPI key, decision `declined`, reason, recorded date/time). |

A wrongly recorded decline is corrected by a new APS record entry
superseding it (the patient later accepts and a referral is
created — that is a new referral, not an un-decline). This entity
is the only one of the thirteen with no FHIR resource: recording
it as a `Task` or `Communication` would invent a referral where
the case deliberately has none.

## 13. Cancellation record → Task transition + Appointment + Communication + Provenance

The cancellation is not a resource of its own: it is the Task
transition to `cancelled` with its reason, the Appointment
cancellation where one was booked, the notifications to all
parties, and the Provenance entry.

| Step 3 field | FHIR element | Cardinality / binding | Notes |
|---|---|---|---|
| Cancellation identifier | `Task.identifier` (same referral identifier) + Provenance `id` for the cancellation entry; the cancellation request itself carries its own identifier in the cancel operation's `Task.note` (see OP-8) | — | The cancellation is identified by (referral identifier + cancellation entry); a post-re-open cancellation is a NEW entry with a new cancellation identifier, not a reuse of the undone one. |
| Referral identifier | `Task.identifier` (§3) | 0..* | Join key. |
| Requester | Provenance.agent (`who` → PractitionerRole / Patient, `type` = the requesting role: APS / patient / specialty) on the cancellation Provenance entry | 0..* | The requester is recorded on the audit entry, not on the Task. |
| Reason | `Task.statusReason` (coded + free text; "patient deceased" included) | 0..1 | Required. |
| Request date/time | Provenance.recorded on the cancellation entry | 1..1 | — |
| Appointment cancelled? | `Appointment.status = cancelled` + `Appointment.cancelationReason` (§5) | — | Required when an appointment was booked; the booking is voided, not completed. The Slot returns to `free`. |
| Parties notified | Communication (§11, one per party: APS, patient, specialty) | — | The hub notifies all parties; each notification is a Communication. |

Lifecycle: `requested` → `recorded` (terminal — the referral is
`cancelled`). A cancellation arriving after the referral reached
a terminal state is rejected (nothing left to cancel). A
cancellation arriving while the appointment is being booked is
accepted — the booking is voided. Correction: re-open only, with
an explicit entry and notification to APS and the specialty (§3).

## Supporting resources (no step 3 entity of their own)

| Resource | Use in this case | Notes |
|---|---|---|
| `Provenance` | The append-only state history of the Task (§3): one entry per transition (who, when, from, to, reason); the merge history of the MPI record (§10); the cancellation entry (§13). | `Provenance.target` → Task / Patient; `Provenance.recorded`; `Provenance.agent.who` → PractitionerRole / Patient; `Provenance.activity` (local ValueSet: state-transition / merge / cancellation / re-open). Linked from `Task.relevantHistory`. |
| `Bundle` | The envelope for the push operations: `type = transaction` for PI-0 (ServiceRequest + Task) and the cancel fan-out; `type = document` for PI-3 (Composition first entry + DocumentReference + Condition + CarePlan). | One Bundle per event, not one Bundle per referral. The Bundle is the envelope, never the workflow record. |
| `Subscription` | Push notification of Task state changes (guide's own — DSUBm is document events only). `criteria = "Task?focus:ServiceRequest.identifier={referral-id}"`, `channel.type = rest-hook`, `channel.endpoint` = the subscriber's URL, `channel.payload` = `application/fhir+json` (full resource — R4 §2.46.4 security note applies: sending the entire resource creates security concerns the server must manage). | Optional subscription per consumer (APS subscribes to its referrals' Tasks); the hub also pushes Communication directly (OP-12). `status = error` → the hub retries and logs; on expiry (`end`) the subscription stops and the subscriber must re-subscribe. |
| `Schedule` | The specialty's availability behind the Slot (§5). | `Schedule.actor` → HealthcareService (§9); `Schedule.planningHorizon`. Used by ITI-115 `$find`. |
| `Location` | The place of the appointment (§5) and the service delivery point (§9). | `Location.name`, `Location.address`, `Location.managingOrganization` → Organization. |
| `Endpoint` | Where the hub sends the referral (§9). | `Endpoint.address`, `Endpoint.connectionType = hl7-fhir-rest`, `Endpoint.payloadType` = the resource types accepted. Read from the mCSD directory (ITI-90). |
| `AuditEvent` | Security audit for every exchange (ATNA, cross-cutting). | `AuditEvent.type`, `agent`, `entity` → the exchanged resource, `outcome` (0/4/8/12 — there is no `denied` value in R4; a blocked disclosure is `outcome = 4` + `outcomeDesc`). The audit trail is append-only. |
| `AppointmentResponse` | The patient's answer to an offer (§5). | `AppointmentResponse.appointment` → Appointment; `AppointmentResponse.actor` → Patient; `AppointmentResponse.participantStatus` (`accepted | declined | tentative | needs-action`). |

## Entities with no FHIR equivalent — summary

| Entity | Verdict | Reason |
|---|---|---|
| 12. Declined-referral record | No FHIR equivalent | Nothing is created and nothing travels; a resource would invent a referral the case deliberately has none. |
| 4. Triage decision | No separate resource (Task transition + Provenance) | The decision IS the workflow transition. |
| 13. Cancellation record | No separate resource (Task transition + Appointment + Communication + Provenance) | The cancellation IS the workflow transition to `cancelled`. |

All other entities map to exactly one resource (with the
counter-referral mapping to a document set of four resources that
travel together: Composition + DocumentReference + Condition +
CarePlan).
