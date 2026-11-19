# BPMN Model: Derivación APS → especialidad con contrareferencia

Use case: `01-use-case-spec.md` (validated 2026-11-19). Pack
health-interop-superpowers v0.39.0.

## IHE landscape scan

Scan run 2026-11-19, each profile verified live at profiles.ihe.net /
ihe.net / wiki.ihe.net (never from memory). The scan surveys candidates
only; fit per interoperability point is decided in step 4
(`04-fhir-proposal.md`). A candidate is a possibility to keep in mind
while modeling, not a decision. Profiles from the previous (lost) scan
summary are re-verified here one by one — the summary is a checklist,
not established fact.

| Profile | Version / status (live) | What it could cover in this case | Needs / notes |
|---------|------------------------|----------------------------------|---------------|
| Scheduling (ITI) | v1.0.0 Publication, FHIR R4, Active 2024-12-12 — https://profiles.ihe.net/ITI/Scheduling/ (checked 2026-11-19) | PI-2 appointment offer/booking: Find Potential Appointments [ITI-115] (`$find`), Hold [ITI-116] (`$hold`, optional), Book [ITI-117] (`$book`), Search Patient Appointments [ITI-118]. Actors Scheduling Client / Scheduling Server. | Candidate for the full PI-2 loop (offer, re-offer, re-schedule). Step 4 to confirm fit per point. |
| QEDm (PCC) | v3.0.0 Publication, FHIR R4, Active 2024-12-12 — https://profiles.ihe.net/PCC/QEDm/ (checked 2026-11-19) | Clinical-data pull: Mobile Query for Existing Data [PCC-44] over observations, allergies, problems, diagnostic results, medications, immunizations, procedures, encounters, provenance. | Only for clinical data elements. Does NOT cover workflow state (Task/Appointment/ServiceRequest status), so it cannot carry the PI-4 status query itself — only the clinical pull inside it. |
| mCSD (ITI) | v4.0.0 Publication, FHIR R4 — https://profiles.ihe.net/ITI/mCSD/ (checked 2026-11-19) | Care-services directory: Find Matching Care Services [ITI-90], Request Care Services Updates [ITI-91], Care Services Feed [ITI-130]. Organization / HealthcareService / PractitionerRole / Location / Endpoint. | Candidate for routing: the hub finds the requested specialty service (and its endpoint) in the directory. Step 4 to confirm per point. |
| MHD (ITI) | v4.2.5 Publication, FHIR R4, Active 2026-10-18 — https://profiles.ihe.net/ITI/MHD/ (checked 2026-11-19) | Document exchange over FHIR REST: Provide Document Bundle [ITI-65], Simplified Publish [ITI-105], Find/Retrieve Document Lists and References [ITI-66/67], Retrieve Document [ITI-68], Generate Metadata [ITI-106]. Actors Document Source / Document Recipient / Document Consumer / Document Responder. | Candidate for PI-0 and PI-3 where the referral / counter-referral travels as a document. It carries documents, not workflow state — acceptance/rejection and status tracking are not MHD. |
| XBeR-WD (PCC) | Trial Implementation — https://wiki.ihe.net/index.php/Cross-enterprise_Basic_eReferral_Workflow_Definition (checked 2026-11-19) | The eReferral workflow definition itself: built on XDW, in an XDS.b context. Three tasks: Request Referral, Schedule Referral (optional), Perform Referral. Defines the workflow for the eReferral document and the related documents. | The closest IHE match to this whole case — but Trial Implementation and XDS/CDA-based, not FHIR. Candidate as the workflow pattern for PI-0–PI-3 state tracking; step 4 to judge fit (pattern vs conformance). |
| XDW (ITI) | ITI TF Vol. 1 ch. 30 — https://profiles.ihe.net/ITI/TF/Volume1/ch-30.html (checked 2026-11-19) | Workflow infrastructure: the Workflow Document records task creation and history as tasks move through the workflow, with references to input/output documents. Actors Content Creator / Content Consumer / Content Updater; grouped with XDS / XDM / XDR actors for transport. | The generic platform XBeR-WD is built on. Candidate for the referral state tracking (PI-1, PI-4) as a shared Workflow Document — document-based, not FHIR. Step 4 to judge. |
| 360X (PCC) | Rev. 1.2 Trial Implementation, 2021-04-14, PCC TF V11.0 supplement — confirmed from the supplement PDF itself ("Rev. 1.2 – Trial Implementation", "Date: April 14, 2021", https://www.ihe.net/uploadedFiles/Documents/PCC/IHE_PCC_Suppl_360X.pdf, checked 2026-11-19); listed on https://profiles.ihe.net/PCC/index.html under Trial Implementation supplements | Closed-loop referral: Referral Request + Result of Referral between providers on different EHRs, with a persistent referral identifier until the loop closes. Transport Direct / XDM / XDR; CDA content (LOINC 57133-1 referral request). Actors Referral Initiator / Referral Recipient. | The IHE closed-loop referral profile — but CDA + Direct/XDM/XDR, not FHIR, and Trial Implementation. Candidate as the pattern for PI-0 + PI-3; the transaction numbers (PCC-55–61 per the pack's scan list) were NOT re-verified in this pass — step 4 to confirm. |
| PIXm (ITI) | v3.1.0 Publication, FHIR R4 — https://profiles.ihe.net/ITI/PIXm/ (checked 2026-11-19) | Patient identity cross-reference: Mobile Patient Identifier Cross-reference Query [ITI-83] (`GET [base]/Patient/$ihe-pix`), plus the identity feed [ITI-104]. Actors Consumer / Manager / Source. | Candidate for the MPI role: resolve the patient identity across organisations at PI-0 (and wherever the referral needs the MPI key). |
| PDQm (ITI) | v3.2.0 Publication, FHIR R4 — https://profiles.ihe.net/ITI/PDQm/ (checked 2026-11-19) | Patient demographics query: Mobile Patient Demographics Query [ITI-78] (GET/POST Patient search, required for the Supplier), Patient Demographics Match [ITI-119] (`Patient.$match`, optional). Actors Consumer / Supplier. | Candidate for the patient search at PI-0 (find the patient by demographics/identifier before creating the referral). ITI-119 is `$match`, not a plain search. |
| DSUBm (ITI) | v1.0.0 Publication, FHIR R4 — https://profiles.ihe.net/ITI/DSUBm/ (checked 2026-11-19) | Document subscription: Resource Subscription [ITI-110], Resource Publish [ITI-111], Resource Notify [ITI-112], Resource Subscription Search [ITI-113], SubscriptionTopic Search [ITI-114]. Actors Resource Notification Subscriber / Broker / Publisher / Recipient. | Document events ONLY (SubscriptionTopic for DocumentReference). Candidate for notifying APS when a counter-referral document is published — it cannot carry referral state changes (Task status), which are not document events. |
| ATNA (ITI) | Final Text, ITI TF Vol. 1 ch. 9 — https://profiles.ihe.net/ITI/TF/Volume1/ch-9.html (checked 2026-11-19); RESTful ATNA supplement Trial Implementation (Retrieve ATNA Audit Event [ITI-81], Retrieve Syslog Event [ITI-82]) | Audit and node authentication for every exchange: Authenticate Node [ITI-19], Record Audit Event [ITI-20]. Cross-cutting security for all PIs. | Applies to every point as the audit/security layer, not to any single PI. FHIR AuditEvent feed/query via RESTful ATNA is Trial Implementation. |
| CT (ITI) | Final Text, ITI TF Vol. 1 ch. 7 — https://wiki.ihe.net/index.php/CT (checked 2026-11-19) | Consistent time across the network: NTP-based synchronisation, median error under 1 second. Cross-cutting for every timestamped event (SLA clocks, audit times). | Applies to every point as infrastructure, not to any single PI. |
| XDS.b (ITI) | Final Text, ITI TF Vol. 1 ch. 10 — https://profiles.ihe.net/ITI/TF/Volume1/ch-10.html (checked 2026-11-19) | Classic document sharing (SOAP/ebXML, affinity domain): Provide and Register Document Set-b [ITI-41], Register Document Set-b [ITI-42], Registry Stored Query [ITI-18], Retrieve Document Set [ITI-43]. Actors Document Source / Repository / Registry / Consumer. | The classic alternative to MHD for PI-0/PI-3 documents. It carries documents, not workflow state: per XDS.b ch. 10, placing and tracking orders (e.g. eReferral) is not supported by XDS — no facility for tracking an order's progress. |
| BPPC (ITI) | Final Text, ITI TF Vol. 1 ch. 19 — https://profiles.ihe.net/ITI/TF/Volume1/ch-19.html (checked 2026-11-19) | Patient privacy consents for document sharing: records the consent and lets XDS Consumers enforce the privacy policy that authorised a document's publication. CDA-based. | SET ASIDE for this case: no consent artifact travels — the referral is covered by the care relationship (spec §4, Q7). Its FHIR successor PCF is set aside for the same reason. |

**Scan result (2026-11-19): 14 profiles verified live** — the previous
summary said "12 profiles" but listed 14 names; the recount is 14
(Scheduling, QEDm, mCSD, MHD, XBeR-WD, XDW, 360X, PIXm, PDQm, DSUBm,
ATNA, CT, XDS.b, BPPC). The picture for this case: document exchange
has two full candidates (MHD / XDS.b); the referral workflow itself has
two document-based candidates (360X, XBeR-WD on XDW) — both
Trial Implementation and CDA/XDS-based, not FHIR; scheduling has one
full FHIR candidate (Scheduling ITI-115/117); identity has two FHIR
candidates (PIXm, PDQm); the directory has one (mCSD); status queries
have no profile that carries workflow state — QEDm covers clinical data
only, DSUBm covers document events only; ATNA and CT apply to every
point as cross-cutting infrastructure; BPPC is set aside (no consent
artifact travels). Step 4 decides fit per point.

## Model split

The model is split in three parts (one pool per organisation/system in
each; PI ids are global across the three diagrams; the single PI
register below lives here).

| Part | File | Pools | Covers |
|------|------|-------|--------|
| A — referral-triage | `02-bpmn-model-referral-triage.bpmn` (+ `.svg`, `.png`) | APS (doctor, admin), MPI, hub, specialty (triage), patient | Creation, identity, routing, accept/reject, re-triage, cancellation |
| B — scheduling-counterreferral | `02-bpmn-model-scheduling-counterreferral.bpmn` (+ `.svg`, `.png`) | APS (admin, doctor), hub, specialty (scheduler, specialist), patient | Offer, confirmation/chases, re-offer, booking, encounter, counter-referral, no-show, cancellation |
| C — status-query | `02-bpmn-model-status-query.bpmn` (+ `.svg`, `.png`) | APS (doctor / admin), hub | PI-4 read-only status query |

Part A ends at acceptance (Part B starts there); Part B ends at
counter-referral / no-show / return to re-triage. Part C can be
invoked at any point in the referral lifecycle.

## PI register (single, global)

| PI | Name | Legs (message flows) | Diagram |
|----|------|----------------------|---------|
| PI-0 | Referral creation | m3 APS → hub; m11 hub → specialty (routed) | A |
| PI-1 | Accept / reject | m4/m5 specialty → hub; m6/m7 hub → APS; m12 hub → patient (rejection notice, via APS admin); m9 acceptance notice to patient | A |
| PI-2 | Appointment offer / booking | h1 specialty → hub; h2 hub → patient; h3 hub → APS admin (notification); h8 re-offer, scheduler → hub; h9 appointment booked, scheduler → specialist | B |
| PI-3 | Counter-referral return | h10 specialty → hub; h11 hub → APS | B |
| PI-4 | Status query (read-only) | j1 APS → hub; j2/j3 hub → APS (current state, last state change, next expected step — spec §3.7) | C |

## State machine

One referral = one request + one workflow state record; state lives in
the workflow record (held by the hub), not in the request status.
Two paths (spec §3.5):

- Accepted: `requested → received → accepted → scheduled → completed
  → counter-referred`.
- Rejected: `requested → received → rejected → APS re-triage → [new
  referral | different specialty | resolve in APS] → closed as
  rejected`. A re-referral is a NEW referral; the first closes as
  `rejected` only once APS has decided the re-triage outcome. A
  scheduling-failure return (Part B, second decline or unconfirmed
  after the second chase) lands on the same Part A re-triage entry
  with the same three outcomes and the same rejected closure.

Terminal states: `counter-referred`, `rejected`, `no-show` (after a
failed re-scheduling), `cancelled` (any point before completion, by
APS / patient / specialty; also on patient death, reason "patient
deceased").

## SLAs (spec §3.6)

| Deadline | Value | Modelled as |
|----------|-------|-------------|
| Acceptance | 5 working days from creation (2 if urgent) | Part A, event-based gateway `Decision received?` in the hub: message branch vs timer branch labelled "timeout — 5 working days (2 if urgent)"; on timeout the hub escalates to the specialty and notifies APS, then keeps waiting (loop-back re-enters the gateway). One wait covers both durations: the timer is data-driven — the referral priority (routine/urgent) travels in the minimum data set and the hub applies 2 working days when it is urgent, 5 otherwise. |
| Appointment offer | 10 working days from acceptance | Part B, non-interrupting boundary timer ("10 working days") on `Offer appointment`; breach notifies the hub, which escalates to the specialty and notifies APS (h19). |
| Confirmation | 3 working days from offer | Part B, event-based gateway `Decision received?` in the scheduler, timer branch labelled "timeout — 3 working days"; timer branch chases the patient (data-based gateway `Chased twice?`: no → chase and wait again; yes → return to APS re-triage). |
| Counter-referral | 5 working days from the specialty encounter | Part B, non-interrupting boundary timer ("5 working days") on `Write counter-referral`; breach notifies the hub, which escalates to the specialty and notifies APS (h20). |
| Re-triage decision | 5 working days from rejection | Part A, non-interrupting boundary timer ("5 working days") on `Re-triage within 5 working days`; breach notifies the hub, which escalates to APS |

On timeout of the acceptance / offer / counter-referral SLAs the hub
escalates to the specialty and notifies APS. All SLA values are working
days, and the diagram labels now carry the full "working days" wording
everywhere — no shorthand remains.

## Part A — referral-triage

Pools in order: APS (doctor, admin), MPI, hub, specialty (triage),
patient. The doctor assesses the need; if the patient declines, the
decline is recorded and no referral is created. Identity is resolved
via the MPI before creation (no local identifier travels without the
MPI key). The referral (minimum data set) goes APS → hub (PI-0) and
the hub routes it to the requested specialty service (PI-0, second
leg). The specialty triages and accepts (naming the service /
practitioner) or rejects with a reason (PI-1); the hub forwards the
decision to APS and the APS admin informs the patient. On rejection
the APS doctor re-triages within 5 working days: re-refer with more
information, refer to a different specialty, or resolve in APS — each
closes the first referral as `rejected` and starts a new referral
instance where applicable. The acceptance wait is an event-based
gateway (drawn as an exclusive gateway — the renderer draws only
exclusive / parallel gateways) with a message branch and a timer
branch labelled with its duration. The APS admin informs the patient
of acceptance AND of rejection (m12 carries the rejection notice to
the patient; the acceptance path names the doctor notification too).
Cancellation: a message start event in the hub loop row
(`Cancellation requested (APS / patient / specialty)` → `Record
cancellation; notify all parties` → `Cancelled (terminal)`); any party
(APS, patient, specialty) may request it at any point before
completion. Patient death is a cancellation cause handled by this row:
the hub records the cancellation with reason "patient deceased" and
notifies APS + specialty (spec §3.1/C11). The row records the
cancellation; it does not terminate the in-flight main flow in the
diagram (see Modeling notes) — the hub's record is the authority, and
every later step reads the workflow record first.

## Part B — scheduling-counterreferral

Pools: APS (admin, doctor), hub, specialty (scheduler, specialist),
patient. The scheduler offers an appointment (PI-2); the hub forwards
the offer to the patient and notifies the APS admin. The patient
accepts (confirmation) or declines. On decline the scheduler re-offers
once (data-based gateway `First decline?` — the count lives in the
workflow record held by the hub); a second decline returns the
referral to APS re-triage. On no confirmation within 3 working days
the scheduler chases the patient (data-based gateway `Chased twice?`:
chase and wait again, at most twice; then return to APS re-triage).
The return lands on Part A's re-triage entry: the same three outcomes
(new referral | different specialty | resolve in APS) apply, and the
first referral closes as `rejected` once APS decides (N1). Booking
creates the Appointment + Slot; the specialist waits until
the appointment date (timer catch event) and attends. If the patient
does not attend, the no-show is recorded and re-scheduling is
attempted once (data-based gateway `First re-scheduling?` — the count
of re-schedulings lives in the workflow record held by the hub;
after a second no-show the referral closes as `no-show` per Q5) and
APS is notified. The re-scheduled offer goes through the SAME
offer/confirm loop as the first offer (N5): re-booking routes back to
`Offer appointment`, so the patient gets the same 3-working-day
confirmation wait, the same chase rules and the same one re-offer on
decline; a second decline or unconfirmed after the second chase
returns the referral to APS re-triage. The patient's agreement to the
new date IS the confirmation of the re-scheduled offer in that loop;
the chase/re-offer counts reset per offer (each offer has its own
confirm/chase budget). After the encounter the specialist writes the
counter-referral (diagnosis, plan, follow-up indications + follow-up
plan for APS) within 5 working days (PI-3); the hub forwards it to
APS, the admin notifies the doctor, and the referral closes as
`counter-referred`. SLA escalations notify APS as well as the
specialty: the hub's escalation tasks forward the delay to the APS
admin (h19 offer delay, h20 counter-referral delay), who notifies the
APS doctor. Cancellation: same message-start row as Part A,
in the hub loop row.

## Part C — status-query

Pools: APS (doctor / admin — one lane; PI-4 is a read-only lookup any
APS staff member can make) and hub. The APS queries the hub (PI-4);
the hub looks the referral up in the workflow record it holds and
returns the current state, the last state change and the next expected
step, or `not found` (APS then verifies the referral id). PI-4 never changes referral state and can
be invoked at any point in the lifecycle. No profile carries workflow
state for this query (see scan: QEDm covers clinical data only, DSUBm
covers document events only) — step 4 decides the mechanism.

## Modeling notes

- Every connecting line is orthogonal, never diagonal; each parallel
  channel has its own y (7–15 px apart); two flows leaving the same
  gateway in the same direction leave from different points; a
  boundary-event flow never goes through its own task; flows to
  different targets never share a segment.
- Loop-backs (rejection, re-scheduling, re-offer, escalation wait)
  run in their own row below the main flow and re-enter through the
  gateway that owns the retry decision.
- Data-based gateways (`First decline?`, `Chased twice?`) read the
  workflow record held by the hub — the count of declines / chases is
  state, not a diagram counter.
- The cancellation row in Parts A and B is annotated in the diagram
  itself: the task reads `Record cancellation (incl. patient death);
  notify all parties` — patient death closes the referral as
  `cancelled` with reason "patient deceased" (APS + specialty
  notified), per the state machine above.
- Notification-receipt tasks end their branch by convention:
  `t_pat_create` and `t_pat_notice2` (Part A, Patient pool) and
  `t_admin_notify_offer` and `t_admin_esc` (Part B, APS admin lane)
  have no outgoing sequence flow and no end event — receipt of the
  notification is the end of that branch.
- The acceptance and confirmation waits are event-based gateways
  (message vs timer); the renderer draws them as exclusive gateways
  and they are named `Decision received?` in both parts. Their timer
  branches carry duration labels ("timeout — 5 working days (2 if
  urgent)", "timeout — 3 working days"); the urgent 2-day acceptance
  SLA has no separate branch — the wait is data-driven (see SLAs).
- Message flows h6/h7 land on the decision gateways directly
  (`Decision received?`, `Confirmed?`) instead of on message catch
  events: recorded deviation. The gateway's decision IS the message
  receipt in this rendering; a catch event per decision would duplicate
  the gateway and crowd the scheduler row. The .bpmn stays
  schema-valid (gateways are flow nodes).
- The cancellation row records the cancellation in the hub's workflow
  record; it does not terminate the in-flight main flow in the
  diagram. The hub's record is the authority — every later step reads
  the workflow record first, so a cancelled referral cannot advance.
  The start event names the requester (APS / patient / specialty);
  patient death is a cancellation cause (reason "patient deceased",
  hub notifies APS + specialty).
- Known right-angle crossings of two message flows (readable per the
  skill; no shared segments): Part A — m5 vertical x=1075 crosses m4
  horizontal y=800; m7 horizontal y=578 crosses m6 vertical x=1115;
  m12 vertical x=790 crosses m10 horizontal y=420 and f22 horizontal
  y=800. Part B — m_reoffer horizontal y=550 crosses m_fwd_confirm vertical
  x=685; m_fwd_decline horizontal y=560 crosses m_fwd_confirm
  vertical x=685 and m_fwd_confirm horizontal y=570 crosses
  m_fwd_decline vertical x=445; m_retriage vertical x=885 crosses
  m_esc_offer y=512 and m_esc_counter y=524; m_retriage_fwd_patient
  vertical x=885 crosses m_offer_fwd horizontal y=1035; h19 vertical
  x=390 crosses h3 horizontal y=325, h2 horizontal y=330 and h3
  horizontal y=120; h20 vertical x=790 crosses h4/h10 horizontal
  y=420; h20 horizontal y=160 crosses h15 vertical x=1185, h11
  vertical x=1285 and h13 vertical x=1485; g32 vertical x=70 crosses
  g21 horizontal y=690; g32 horizontal y=960 crosses h9 vertical
  x=710; g14 horizontal y=860 crosses h9 vertical x=710.
- The message-event marker is drawn as a vector envelope (the ✉ glyph
  is missing from the PNG font); the `→` character is not used in
  labels for the same reason.
- Renderer fixes made during the expert-review fix pass (clone root,
  not the pack): `render_bpmn.py` now gives every outside label an
  opaque white backing (a label centred on its own flow line, or on a
  pool/lane boundary line, reads clean instead of struck through); a
  nudge may no longer push a label onto its own shape (this was
  hiding the "10 working days" / "5 working days" boundary-timer
  labels behind their own circles); the nudge list is extended
  (0, ±84/±98/±112) for crowded spots; the canvas expands to fit
  labels nudged past its edge (the "Accept / reject notice" label
  was clipped at the right edge).
- Builder: `build_bpmn.py` + `parts_data.py` generate the three
  `.bpmn` files from explicit element/flow tables (all waypoints
  hand-laid-out). `render_bpmn.py` / `check_bpmn.py` live in the clone
  root. Two tool fixes made during this step, both in the clone root
  (not the pack): `check_bpmn.py` now tests only flow-node shapes
  (participants/lanes are containers, not crossed shapes — its
  docstring already said so); `render_bpmn.py` draws the message
  envelope as vector lines.

## Files

| File | Content |
|------|---------|
| `02-bpmn-model-referral-triage.bpmn` | Part A — 52 shapes, 43 flows |
| `02-bpmn-model-referral-triage.svg` / `.png` | Part A render (PNG at 2×) |
| `02-bpmn-model-scheduling-counterreferral.bpmn` | Part B — 65 shapes, 59 flows |
| `02-bpmn-model-scheduling-counterreferral.svg` / `.png` | Part B render (PNG at 2×) |
| `02-bpmn-model-status-query.bpmn` | Part C — 16 shapes, 11 flows |
| `02-bpmn-model-status-query.svg` / `.png` | Part C render (PNG at 2×) |
| `build_bpmn.py`, `parts_data.py` | Builder + geometry tables (kept: the geometry is the model) |

## Mechanical check (2026-11-19)

`python3 check_bpmn.py --check` on each part: **0 diagonal segments,
0 shape crossings, 0 DI elements missing id, 0 collapsed sub-processes
without isExpanded=false — CHECK OK** on all three parts. PNGs rendered
at 2× and inspected visually; labels legible at display size.
Re-checked 2026-11-19 after the expert-review fixes C1–C14 (Part A
52 shapes / 43 flows, Part B 65 / 59, Part C 16 / 11).
