/*
 * CodeSystems and ValueSets for School Vision Screening
 */

// Local CodeSystem for Screening Test Methods
CodeSystem: SVSScreeningTestMethod
Id: svs-screening-test-method
Title: "School Vision Screening Test Methods"
Description: "Methods used for visual acuity screening in school settings"
* ^status = #active
* ^experimental = false
* ^caseSensitive = true
* ^content = #complete
* ^property[+].code = #notSelectable
* ^property[=].type = #boolean
* ^property[=].description = "Indicates that the code is not intended for selection"
* #snellen "Snellen 6m chart" "Snellen chart at 6 metres"
* #tumbling-e "Tumbling E optotypes" "Tumbling E optotypes for children who cannot read letters"
* #lea-symbols "Lea symbols" "Lea symbols for pre-readers"
* #other "Other method" "Other screening method not listed"

// Local CodeSystem for Screening Outcomes
CodeSystem: SVSScreeningOutcome
Id: svs-screening-outcome
Title: "School Vision Screening Outcomes"
Description: "Possible outcomes of a vision screening encounter"
* ^status = #active
* ^experimental = false
* ^caseSensitive = true
* ^content = #complete
* #pass "Pass" "Visual acuity ≥6/9 in both eyes"
* #refer "Refer" "Visual acuity ≤6/12 in either eye OR ≥2 line difference between eyes"
* #absent "Absent" "Child was absent on screening day"
* #incomplete "Incomplete" "Screening could not be completed (uncooperative, one eye only)"

// Local CodeSystem for Referral Reasons
CodeSystem: SVSReferralReason
Id: svs-referral-reason
Title: "School Vision Screening Referral Reasons"
Description: "Reasons for referral to ophthalmology"
* ^status = #active
* ^experimental = false
* ^caseSensitive = true
* ^content = #complete
* #acuity-low "Acuity ≤6/12" "Visual acuity 6/12 or worse in either eye"
* #acuity-diff "Acuity difference ≥2 lines" "Difference of two or more lines between eyes"
* #incomplete-2nd "Incomplete after 2 attempts" "Screening incomplete after two attempts with partial data"

// Local CodeSystem for Accommodation Types
CodeSystem: SVSAccommodationType
Id: svs-accommodation-type
Title: "Classroom Accommodation Types"
Description: "Types of classroom accommodations for vision impairment"
* ^status = #active
* ^experimental = false
* ^caseSensitive = true
* ^content = #complete
* #glasses "Glasses needed" "Child requires prescription glasses"
* #front-seat "Front seat" "Child needs front row seating"
* #both "Glasses and front seat" "Child needs both glasses and front seat"
* #other "Other accommodation" "Other classroom accommodation"

// Local CodeSystem for School Health Service Roles
CodeSystem: SVSPractitionerRoleCS
Id: svs-practitioner-role
Title: "School Health Service Practitioner Roles"
Description: "Roles within the school health service for vision screening"
* ^status = #active
* ^experimental = false
* ^caseSensitive = true
* ^content = #complete
* #school-nurse "School Nurse" "Registered nurse conducting vision screening"
* #service-lead "Service Lead" "School health program lead / coordinator"

// Local CodeSystem for Document Types (IP-4)
CodeSystem: SVSDocumentType
Id: svs-document-type
Title: "School Vision Screening Document Types"
Description: "Types of documents exchanged with Primary Care (IP-4)"
* ^status = #active
* ^experimental = false
* ^caseSensitive = true
* ^content = #complete
* #screening-pass "Screening Pass" "Vision screening result: pass (≥6/9 both eyes)"
* #screening-decline "Screening Decline" "Vision screening result: parent declined referral"
* #screening-missed "Screening Missed" "Vision screening not completed (2nd absent)"
* #assessment-full "Full Assessment" "Complete ophthalmology assessment report"
* #referral-dna "Referral DNA" "Referral closed: did not attend (2nd DNA)"
* #referral-rejected "Referral Rejected" "Referral rejected by ophthalmology"
* #end-of-year-missed "End-of-Year Missed" "Screening missed at end of school year (pending re-screen)"

// ValueSet for Screening Test Methods
ValueSet: SVSScreeningTestMethodVS
Id: svs-screening-test-method-vs
Title: "School Vision Screening Test Methods ValueSet"
Description: "Allowed test methods for school vision screening"
* ^status = #active
* ^experimental = false
* include codes from system SVSScreeningTestMethod

// ValueSet for Screening Outcomes
ValueSet: SVSScreeningOutcomeVS
Id: svs-screening-outcome-vs
Title: "School Vision Screening Outcomes ValueSet"
Description: "Possible outcomes of a vision screening encounter"
* ^status = #active
* ^experimental = false
* include codes from system SVSScreeningOutcome

// ValueSet for Referral Reasons
ValueSet: SVSReferralReasonVS
Id: svs-referral-reason-vs
Title: "School Vision Screening Referral Reasons ValueSet"
Description: "Reasons for referral to ophthalmology"
* ^status = #active
* ^experimental = false
* include codes from system SVSReferralReason

// ValueSet for Accommodation Types
ValueSet: SVSAccommodationTypeVS
Id: svs-accommodation-type-vs
Title: "Classroom Accommodation Types ValueSet"
Description: "Types of classroom accommodations for vision impairment"
* ^status = #active
* ^experimental = false
* include codes from system SVSAccommodationType

// ValueSet for School Health Service Roles
ValueSet: SVSPractitionerRoleVS
Id: svs-practitioner-role-vs
Title: "School Health Service Practitioner Roles ValueSet"
Description: "Roles within the school health service"
* ^status = #active
* ^experimental = false
* include codes from system SVSPractitionerRoleCS

// ValueSet for Document Types (IP-4)
ValueSet: SVSDocumentTypeVS
Id: svs-document-type-vs
Title: "School Vision Screening Document Types ValueSet"
Description: "Types of documents exchanged with Primary Care"
* ^status = #active
* ^experimental = false
* include codes from system SVSDocumentType

// ValueSet for Snellen Acuity Interpretation (using standard ObservationInterpretation)
ValueSet: SVSAcuityInterpretationVS
Id: svs-acuity-interpretation-vs
Title: "Visual Acuity Interpretation ValueSet"
Description: "Interpretation codes for visual acuity results"
* ^status = #active
* ^experimental = false
* include ObsInterp#A "Abnormal (≤6/12)"
* include ObsInterp#N "Normal (≥6/9)"
* include ObsInterp#H "High"
* include ObsInterp#L "Low"