# Primary Care Document Log - Maria Gonzalez - v0.1.0

* [**Table of Contents**](toc.md)
* [**Artifacts Summary**](artifacts.md)
* **Primary Care Document Log - Maria Gonzalez**

## Example List: Primary Care Document Log - Maria Gonzalez

Profile: [Primary Care Vision Screening Document Log](StructureDefinition-svs-list-primary-care-documents.md)

### School Vision Screening Documents for Maria Gonzalez

| | |
| :--- | :--- |
| Mode: Working List | Status: Current |
| Subject:[Maria Isabel Gonzalez (official) Female, DoB: 2018-03-15 ( PIXm Cross-reference: PIXM-987654321)](Patient-SVSPatientExample.md) | |

* **Items**: [DocumentReference: identifier = urn:oid:1.2.3.4.5.ip4-doc#DOC-IP4-2026-11-15-0042-pass; status = current; type = Visual acuity screening panel; category = Screening Report; date = 2026-11-15 10:00:00+0000; description = Vision screening pass result for Maria Gonzalez (6/9 both eyes)](DocumentReference-SVSDocumentReferenceScreeningPassExample.md)



## Resource Content

```json
{
  "resourceType" : "List",
  "id" : "SVSListPrimaryCareDocumentsExample",
  "meta" : {
    "profile" : ["https://josemandrade.github.io/prueba-his-muse-nvidia/school-vision-screening/StructureDefinition/svs-list-primary-care-documents"]
  },
  "identifier" : [{
    "system" : "urn:oid:1.2.3.4.5.primary-care-docs",
    "value" : "PC-2026-001234-documents"
  }],
  "status" : "current",
  "mode" : "working",
  "title" : "School Vision Screening Documents for Maria Gonzalez",
  "subject" : {
    "reference" : "Patient/SVSPatientExample"
  },
  "entry" : [{
    "item" : {
      "reference" : "DocumentReference/SVSDocumentReferenceScreeningPassExample"
    }
  }]
}

```
