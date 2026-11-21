/*
 * Minimal Synthetic Examples for School Vision Screening IG
 * All data is synthetic - no real patient data
 */

// ============================================================
// Patient (Child) Example
// ============================================================
Instance: SVSPatientExample
InstanceOf: SVSPatient
Title: "Child Example - Maria Gonzalez"
Description: "Synthetic example of an 8-year-old child"
* identifier[0].system = "urn:oid:1.2.3.4.5.school-roll"
* identifier[0].value = "SCL-2026-0042"
* identifier[1].system = "http://terminology.hl7.org/CodeSystem/v2-0203"
* identifier[1].value = "NHS-1234567890"
* identifier[1].type.coding[0].system = "http://terminology.hl7.org/CodeSystem/v2-0203"
* identifier[1].type.coding[0].code = #NI
* identifier[1].type.coding[0].display = "National unique individual identifier"
* identifier[1].use = #official
* identifier[2].system = "urn:ihe:pixm:cross-ref"
* identifier[2].value = "PIXM-987654321"
* identifier[2].type.coding[0].system = "http://terminology.hl7.org/CodeSystem/v2-0203"
* identifier[2].type.coding[0].code = #PIXM
* identifier[2].type.coding[0].display = "PIXm Cross-reference"
* name[0].use = #official
* name[0].family = "Gonzalez"
* name[0].given[0] = "Maria"
* name[0].given[1] = "Isabel"
* birthDate = "2018-03-15"
* gender = #female
* address[0].use = #home
* address[0].line[0] = "Calle Principal 123"
* address[0].city = "Madrid"
* address[0].postalCode = "28001"
* address[0].country = "ES"
* telecom[0].system = #phone
* telecom[0].value = "+34-91-555-0123"
* telecom[0].use = #home
* managingOrganization = Reference(SVSOrganizationSchoolExample)

// ============================================================
// RelatedPerson (Parent) Example
// ============================================================
Instance: SVSRelatedPersonExample
InstanceOf: SVSRelatedPerson
Title: "Parent Example - Ana Gonzalez"
Description: "Mother of Maria Gonzalez"
* identifier[0].system = "urn:oid:1.2.3.4.5.guardian"
* identifier[0].value = "GRD-2026-0042"
* patient = Reference(SVSPatientExample)
* relationship[0].coding[0].system = "http://terminology.hl7.org/CodeSystem/v2-0131"
* relationship[0].coding[0].code = #MTH
* relationship[0].coding[0].display = "Mother"
* name[0].use = #official
* name[0].family = "Gonzalez"
* name[0].given[0] = "Ana"
* name[0].given[1] = "Maria"
* telecom[0].system = #phone
* telecom[0].value = "+34-91-555-0123"
* telecom[0].use = #home

// ============================================================
// Practitioner Example
// ============================================================
Instance: SVSPractitionerNurseExample
InstanceOf: SVSPractitioner
Title: "School Nurse Example - Carmen Ruiz"
Description: "School nurse conducting vision screening"
* identifier[0].system = "urn:oid:1.2.3.4.5.employee"
* identifier[0].value = "EMP-2026-015"
* identifier[1].system = "urn:oid:1.2.3.4.5.license"
* identifier[1].value = "LIC-ENF-2026-004521"
* identifier[1].type.coding[0].system = "http://terminology.hl7.org/CodeSystem/v2-0203"
* identifier[1].type.coding[0].code = #PRN
* identifier[1].type.coding[0].display = "Provider number"
* name[0].use = #official
* name[0].family = "Ruiz"
* name[0].given[0] = "Carmen"
* telecom[0].system = #phone
* telecom[0].value = "+34-91-555-0100"
* telecom[0].use = #work

// ============================================================
// Organization Examples
// ============================================================
Instance: SVSOrganizationSchoolExample
InstanceOf: SVSOrganization
Title: "School Example - Colegio Publico San Isidro"
Description: "Public school with vision screening program"
* identifier[0].system = "urn:oid:1.2.3.4.5.school-id"
* identifier[0].value = "SCH-28079-01"
* name = "Colegio Publico San Isidro"
* type.coding[0].system = "http://terminology.hl7.org/CodeSystem/organization-type"
* type.coding[0].code = #edu
* type.coding[0].display = "Educational facility"
* telecom[0].system = #phone
* telecom[0].value = "+34-91-555-0100"
* address[0].use = #work
* address[0].line[0] = "Calle Principal 123"
* address[0].city = "Madrid"
* address[0].postalCode = "28001"
* address[0].country = "ES"

Instance: SVSOrganizationClinicExample
InstanceOf: SVSOrganization
Title: "Ophthalmology Clinic Example"
Description: "Ophthalmology clinic receiving vision screening referrals"
* identifier[0].system = "urn:oid:1.2.3.4.5.clinic-id"
* identifier[0].value = "CLI-OPT-2026-001"
* name = "Clinica Oftalmologica Central"
* type.coding[0].system = "http://terminology.hl7.org/CodeSystem/organization-type"
* type.coding[0].code = #prov
* type.coding[0].display = "Healthcare Provider"
* telecom[0].system = #phone
* telecom[0].value = "+34-91-444-0200"
* address[0].use = #work
* address[0].line[0] = "Avenida de la Salud 45"
* address[0].city = "Madrid"
* address[0].postalCode = "28002"
* address[0].country = "ES"

Instance: SVSOrganizationPrimaryCareExample
InstanceOf: SVSOrganization
Title: "Primary Care Example - Centro de Salud Las Rosas"
Description: "Primary care center receiving screening results"
* identifier[0].system = "urn:oid:1.2.3.4.5.primary-care-id"
* identifier[0].value = "CS-28079-05"
* name = "Centro de Salud Las Rosas"
* type.coding[0].system = "http://terminology.hl7.org/CodeSystem/organization-type"
* type.coding[0].code = #prov
* type.coding[0].display = "Healthcare Provider"
* telecom[0].system = #phone
* telecom[0].value = "+34-91-555-0300"
* address[0].use = #work
* address[0].line[0] = "Calle de las Rosas 10"
* address[0].city = "Madrid"
* address[0].postalCode = "28003"
* address[0].country = "ES"

Instance: SVSOrganizationSchoolHealthServiceExample
InstanceOf: SVSOrganization
Title: "School Health Service - Servicio de Salud Escolar Madrid"
Description: "Regional school health service overseeing vision screening"
* identifier[0].system = "urn:oid:1.2.3.4.5.health-service-id"
* identifier[0].value = "HSE-MAD-001"
* name = "Servicio de Salud Escolar de Madrid"
* type.coding[0].system = "http://terminology.hl7.org/CodeSystem/organization-type"
* type.coding[0].code = #dept
* type.coding[0].display = "Department"
* telecom[0].system = #phone
* telecom[0].value = "+34-91-555-0101"
* address[0].use = #work
* address[0].line[0] = "Calle Salud Publica 5"
* address[0].city = "Madrid"
* address[0].postalCode = "28004"
* address[0].country = "ES"

// ============================================================
// Encounter Example
// ============================================================
Instance: SVSEncounterScreeningExample
InstanceOf: Encounter
Title: "Screening Encounter - Maria Gonzalez"
* identifier[0].system = "urn:oid:1.2.3.4.5.encounter-id"
* identifier[0].value = "ENC-2026-11-15-0042"
* status = #finished
* class.system = "http://terminology.hl7.org/CodeSystem/v3-ActCode"
* class.code = #AMB
* class.display = "Ambulatory"
* type.coding[0].system = "https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/CodeSystem/encounter-type"
* type.coding[0].code = #vision-screening
* type.coding[0].display = "Vision Screening"
* subject = Reference(SVSPatientExample)
* participant[0].individual = Reference(SVSPractitionerNurseExample)
* participant[0].type.coding[0].system = "http://terminology.hl7.org/CodeSystem/v3-ParticipationType"
* participant[0].type.coding[0].code = #PPRF
* participant[0].type.coding[0].display = "Primary performer"
* period.start = "2026-11-15T09:30:00Z"
* period.end = "2026-11-15T09:45:00Z"
* serviceProvider = Reference(SVSOrganizationSchoolHealthServiceExample)

// ============================================================
// ScreeningEvent: Observation Panel (Refer Result)
// ============================================================
Instance: SVSObservationScreeningPanelReferExample
InstanceOf: SVSObservationScreeningPanel
Title: "Screening Panel - Refer Result (Maria Gonzalez)"
Description: "Visual acuity screening panel showing refer result: right eye 6/12 (<=6/12)"
* identifier[0].system = "urn:oid:1.2.3.4.5.screening-event"
* identifier[0].value = "SCR-2026-11-15-0043"
* status = #final
* category[0].coding[0].system = "http://terminology.hl7.org/CodeSystem/observation-category"
* category[0].coding[0].code = #vital-signs
* category[0].coding[0].display = "Vital Signs"
* code.coding[0].system = "http://loinc.org"
* code.coding[0].code = #83700-8
* code.coding[0].display = "Visual acuity screening panel"
* subject = Reference(SVSPatientExample)
* encounter = Reference(SVSEncounterScreeningExample)
* effectiveDateTime = "2026-11-15T09:35:00Z"
* performer[0] = Reference(SVSPractitionerNurseExample)
* hasMember[0] = Reference(SVSObservationRightEyeAcuityReferExample)
* hasMember[1] = Reference(SVSObservationLeftEyeAcuityReferExample)
* note[0].text = "Test used: Snellen 6m; Outcome: Refer; Attempt: 1; Referral indicated: true"

// Right eye acuity member (6/12 = refer)
Instance: SVSObservationRightEyeAcuityReferExample
InstanceOf: SVSObservationRightEyeAcuity
Title: "Right Eye Acuity - Refer (6/12)"
* identifier[0].system = "urn:oid:1.2.3.4.5.acuity"
* identifier[0].value = "ACU-OD-2026-11-15-0043"
* status = #final
* category[0].coding[0].system = "http://terminology.hl7.org/CodeSystem/observation-category"
* category[0].coding[0].code = #vital-signs
* category[0].coding[0].display = "Vital Signs"
* code.coding[0].system = "http://loinc.org"
* code.coding[0].code = #29474-1
* code.coding[0].display = "Visual acuity right eye"
* subject = Reference(SVSPatientExample)
* effectiveDateTime = "2026-11-15T09:35:00Z"
* valueRatio.numerator.value = 6
* valueRatio.numerator.unit = "m"
* valueRatio.numerator.system = "http://unitsofmeasure.org"
* valueRatio.numerator.code = #m
* valueRatio.denominator.value = 12
* valueRatio.denominator.unit = "m"
* valueRatio.denominator.system = "http://unitsofmeasure.org"
* valueRatio.denominator.code = #m
* bodySite.coding[0].system = "http://snomed.info/sct"
* bodySite.coding[0].code = #363654007
* bodySite.coding[0].display = "Right eye"
* interpretation[0].coding[0].system = "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation"
* interpretation[0].coding[0].code = #A
* interpretation[0].coding[0].display = "Abnormal"

// Left eye acuity member (6/9 = pass)
Instance: SVSObservationLeftEyeAcuityReferExample
InstanceOf: SVSObservationLeftEyeAcuity
Title: "Left Eye Acuity - Pass (6/9)"
* identifier[0].system = "urn:oid:1.2.3.4.5.acuity"
* identifier[0].value = "ACU-OS-2026-11-15-0043"
* status = #final
* category[0].coding[0].system = "http://terminology.hl7.org/CodeSystem/observation-category"
* category[0].coding[0].code = #vital-signs
* category[0].coding[0].display = "Vital Signs"
* code.coding[0].system = "http://loinc.org"
* code.coding[0].code = #29473-3
* code.coding[0].display = "Visual acuity left eye"
* subject = Reference(SVSPatientExample)
* effectiveDateTime = "2026-11-15T09:35:00Z"
* valueRatio.numerator.value = 6
* valueRatio.numerator.unit = "m"
* valueRatio.numerator.system = "http://unitsofmeasure.org"
* valueRatio.numerator.code = #m
* valueRatio.denominator.value = 9
* valueRatio.denominator.unit = "m"
* valueRatio.denominator.system = "http://unitsofmeasure.org"
* valueRatio.denominator.code = #m
* bodySite.coding[0].system = "http://snomed.info/sct"
* bodySite.coding[0].code = #363655008
* bodySite.coding[0].display = "Left eye"
* interpretation[0].coding[0].system = "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation"
* interpretation[0].coding[0].code = #N
* interpretation[0].coding[0].display = "Normal"

// ============================================================
// Referral: ServiceRequest
// ============================================================
Instance: SVSServiceRequestReferralExample
InstanceOf: SVSServiceRequestReferral
Title: "Referral to Ophthalmology - Maria Gonzalez"
Description: "Referral from school nurse to ophthalmology for right eye acuity 6/12"
* identifier[0].system = "urn:oid:1.2.3.4.5.referral"
* identifier[0].value = "REF-2026-11-15-0043"
* identifier[1].system = "urn:ihe:pcc:360x:referral-id"
* identifier[1].value = "360X-REF-2026-11-15-0043"
* status = #active
* intent = #order
* category.coding[0].system = "http://terminology.hl7.org/CodeSystem/service-request-category"
* category.coding[0].code = #referral
* category.coding[0].display = "Referral"
* priority = #routine
* code.coding[0].system = "http://snomed.info/sct"
* code.coding[0].code = #307924000
* code.coding[0].display = "Referral to ophthalmologist"
* code.text = "Vision screening referral: acuity OD 6/12, OS 6/9"
* subject = Reference(SVSPatientExample)
* encounter = Reference(SVSEncounterScreeningExample)
* occurrenceDateTime = "2026-11-15T09:45:00Z"
* authoredOn = "2026-11-15T09:45:00Z"
* requester = Reference(SVSPractitionerNurseExample)
* performer[0] = Reference(SVSOrganizationClinicExample)
* reasonCode[0].coding[0].system = "http://snomed.info/sct"
* reasonCode[0].coding[0].code = #416070007
* reasonCode[0].coding[0].display = "Decreased visual acuity"
* reasonReference[0] = Reference(SVSObservationScreeningPanelReferExample)

// ============================================================
// Assessment: DiagnosticReport + Observations
// ============================================================
Instance: SVSDiagnosticReportAssessmentExample
InstanceOf: SVSDiagnosticReportAssessment
Title: "Ophthalmology Assessment - Maria Gonzalez"
Description: "Complete assessment: mild myopia OD, prescription -1.00 DS, follow-up 12 months"
* identifier[0].system = "urn:oid:1.2.3.4.5.assessment"
* identifier[0].value = "ASM-2026-11-22-0043"
* status = #final
* category[0].coding[0].system = "http://terminology.hl7.org/CodeSystem/v2-0074"
* category[0].coding[0].code = #OP
* category[0].coding[0].display = "Ophthalmology"
* code.coding[0].system = "http://loinc.org"
* code.coding[0].code = #28626-8
* code.coding[0].display = "Ophthalmology study"
* subject = Reference(SVSPatientExample)
* effectiveDateTime = "2026-11-22T10:30:00Z"
* issued = "2026-11-22T11:00:00Z"
* performer[0] = Reference(SVSPractitionerNurseExample)
* resultsInterpreter[0] = Reference(SVSPractitionerNurseExample)
* basedOn[0] = Reference(SVSServiceRequestReferralExample)
* result[0] = Reference(SVSObservationDiagnosisExample)
* result[1] = Reference(SVSObservationRefractionODExample)
* result[2] = Reference(SVSObservationRefractionOSExample)
* conclusion = "Mild myopia OD. Prescription: -1.00 DS OD. Follow-up: 12 months."
* conclusionCode[0].coding[0].system = "http://snomed.info/sct"
* conclusionCode[0].coding[0].code = #373124007
* conclusionCode[0].coding[0].display = "Myopia"

Instance: SVSObservationDiagnosisExample
InstanceOf: SVSObservationDiagnosis
Title: "Diagnosis - Mild Myopia OD"
* identifier[0].system = "urn:oid:1.2.3.4.5.diagnosis"
* identifier[0].value = "DIAG-2026-11-22-0043"
* status = #final
* category[0].coding[0].system = "http://terminology.hl7.org/CodeSystem/observation-category"
* category[0].coding[0].code = #diagnosis
* category[0].coding[0].display = "Diagnosis"
* code.coding[0].system = "http://snomed.info/sct"
* code.coding[0].code = #373124007
* code.coding[0].display = "Myopia"
* subject = Reference(SVSPatientExample)
* effectiveDateTime = "2026-11-22T10:30:00Z"
* valueCodeableConcept.coding[0].system = "http://snomed.info/sct"
* valueCodeableConcept.coding[0].code = #373124007
* valueCodeableConcept.coding[0].display = "Myopia"
* bodySite.coding[0].system = "http://snomed.info/sct"
* bodySite.coding[0].code = #363654007
* bodySite.coding[0].display = "Right eye"

Instance: SVSObservationRefractionODExample
InstanceOf: SVSObservationRefractionOD
Title: "Right Eye Refraction -1.00 DS"
* identifier[0].system = "urn:oid:1.2.3.4.5.refraction"
* identifier[0].value = "REFR-OD-2026-11-22-0043"
* status = #final
* category[0].coding[0].system = "http://terminology.hl7.org/CodeSystem/observation-category"
* category[0].coding[0].code = #exam
* category[0].coding[0].display = "Exam"
* code.coding[0].system = "http://loinc.org"
* code.coding[0].code = #29474-1
* code.coding[0].display = "Visual acuity right eye"
* subject = Reference(SVSPatientExample)
* effectiveDateTime = "2026-11-22T10:30:00Z"
* valueQuantity.value = -1.00
* valueQuantity.unit = "D"
* valueQuantity.system = "http://unitsofmeasure.org"
* valueQuantity.code = #D
* bodySite.coding[0].system = "http://snomed.info/sct"
* bodySite.coding[0].code = #363654007
* bodySite.coding[0].display = "Right eye"

Instance: SVSObservationRefractionOSExample
InstanceOf: SVSObservationRefractionOS
Title: "Left Eye Refraction - Normal"
* identifier[0].system = "urn:oid:1.2.3.4.5.refraction"
* identifier[0].value = "REFR-OS-2026-11-22-0043"
* status = #final
* category[0].coding[0].system = "http://terminology.hl7.org/CodeSystem/observation-category"
* category[0].coding[0].code = #exam
* category[0].coding[0].display = "Exam"
* code.coding[0].system = "http://loinc.org"
* code.coding[0].code = #29473-3
* code.coding[0].display = "Visual acuity left eye"
* subject = Reference(SVSPatientExample)
* effectiveDateTime = "2026-11-22T10:30:00Z"
* valueQuantity.value = 0.00
* valueQuantity.unit = "D"
* valueQuantity.system = "http://unitsofmeasure.org"
* valueQuantity.code = #D
* bodySite.coding[0].system = "http://snomed.info/sct"
* bodySite.coding[0].code = #363655008
* bodySite.coding[0].display = "Left eye"

Instance: SVSCarePlanFollowUpExample
InstanceOf: SVSCarePlanFollowUp
Title: "Follow-up Plan - 12 Month Review"
* identifier[0].system = "urn:oid:1.2.3.4.5.care-plan"
* identifier[0].value = "CP-2026-11-22-0043"
* status = #active
* intent = #plan
* category[0].coding[0].system = "http://terminology.hl7.org/CodeSystem/careplan-category"
* category[0].coding[0].code = #assess-plan
* category[0].coding[0].display = "Assessment Plan"
* subject = Reference(SVSPatientExample)
* encounter = Reference(SVSEncounterScreeningExample)
* period.start = "2026-11-22T10:30:00Z"
* period.end = "2027-11-22T10:30:00Z"
* activity[0].detail.kind = #ServiceRequest
* activity[0].detail.code.coding[0].system = "http://snomed.info/sct"
* activity[0].detail.code.coding[0].code = #373124007
* activity[0].detail.code.coding[0].display = "Myopia follow-up"
* activity[0].detail.scheduledPeriod.start = "2027-11-22T10:30:00Z"
* activity[0].detail.scheduledPeriod.end = "2027-11-22T10:30:00Z"
* activity[0].detail.status = #not-started
* activity[0].detail.description = "Follow-up in 12 months for myopia monitoring"

// ============================================================
// DocumentReference (IP-4) Examples
// ============================================================
Instance: SVSDocumentReferenceScreeningPassExample
InstanceOf: SVSDocumentReferenceIP4
Title: "DocumentReference - Screening Pass Result (IP-4)"
Description: "Primary Care receives screening pass result via MHD"
* identifier[0].system = "urn:oid:1.2.3.4.5.ip4-doc"
* identifier[0].value = "DOC-IP4-2026-11-15-0042-pass"
* status = #current
* type.coding[0].system = "http://loinc.org"
* type.coding[0].code = #83700-8
* type.coding[0].display = "Visual acuity screening panel"
* category[0].coding[0].system = "http://terminology.hl7.org/CodeSystem/document-class"
* category[0].coding[0].code = #screening-report
* category[0].coding[0].display = "Screening Report"
* subject = Reference(SVSPatientExample)
* date = "2026-11-15T10:00:00Z"
* author[0] = Reference(SVSPractitionerNurseExample)
* custodian = Reference(SVSOrganizationSchoolHealthServiceExample)
* description = "Vision screening pass result for Maria Gonzalez (6/9 both eyes)"
* content[0].attachment.url = "https://school-health.example.org/fhir/Observation/SCR-2026-11-15-0042"
* context.encounter[0] = Reference(SVSEncounterScreeningExample)
* context.period.start = "2026-11-15T09:35:00Z"
* context.period.end = "2026-11-15T09:35:00Z"
* context.related[0] = Reference(SVSObservationScreeningPanelReferExample)

// ============================================================
// List (Primary Care Document Log) Example
// ============================================================
Instance: SVSListPrimaryCareDocumentsExample
InstanceOf: SVSListPrimaryCareDocuments
Title: "Primary Care Document Log - Maria Gonzalez"
* identifier[0].system = "urn:oid:1.2.3.4.5.primary-care-docs"
* identifier[0].value = "PC-2026-001234-documents"
* status = #current
* mode = #working
* title = "School Vision Screening Documents for Maria Gonzalez"
* subject = Reference(SVSPatientExample)
* entry[0].item = Reference(SVSDocumentReferenceScreeningPassExample)