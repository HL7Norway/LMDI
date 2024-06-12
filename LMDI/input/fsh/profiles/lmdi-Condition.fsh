// Documentation: https://www.hl7.org/fhir/R4/condition.html 
Profile: LmdiDiagnose
Parent: Condition
Id: lmdi-condition-diagnose
Title: "Diagnose"
Description: "Diagnosen som pasienten har fått rekvirert og administrert legemiddelet for"
* ^status = #draft
* ^date = "2024-06-12"
* ^publisher = "Folkehelseinstituttet"

// NB! Må peke på subject (pasient)
// MVP: ICPC-2, ICD-10, ICD-11, SNOMED CT
* code 1..1
* code ^short = "Diagnosekode. Det er mulig å bruke ICD-10, ICD-11, ICPC-2 og SNOMED CT."
* code.coding ^slicing.discriminator.type = #pattern
* code.coding ^slicing.discriminator.path = "system"
* code.coding ^slicing.rules = #closed
* code.coding contains 
      SCT 0..1 and
      ICD10 0..1 and 
      ICD11 0..1 and 
      ICPC2 0..1
* code.coding[SCT] ^alias = "SNOMED CT"
* code.coding[ICD10] ^alias = "ICD-10"
* code.coding[ICD11] ^alias = "ICD-11"
* code.coding[ICPC2] ^alias = "ICPC-2"
* code.coding[SCT].system = "http://snomed.info/sct"
* code.coding[SCT].code 1..1
* code.coding[ICD10].system = "urn:oid:2.16.578.1.12.4.1.1.7110"
* code.coding[ICD10].code 1..1
// Kilde for URI: https://build.fhir.org/ig/HL7/UTG/CodeSystem-ICD11MMS.html
* code.coding[ICD11].system = "http://id.who.int/icd/release/11/mms"
* code.coding[ICD11].code 1..1
* code.coding[ICPC2].system = "urn:oid:2.16.578.1.12.4.1.1.7170"
* code.coding[ICPC2].code 1..1

// EKSEMPLER
Instance: Diagnose-1-ICD10-OID
InstanceOf: LmdiDiagnose
Description: "Eksempel på diagnose ICD-10"
* subject = Reference(eksempel-pasient-1234567890)
* code.coding[ICD10].system = "urn:oid:2.16.578.1.12.4.1.1.7110"
* code.coding[ICD10] = #R63.3
* code.coding[ICD10].display = "Vanskeligheter med inntak og tilførsel av mat"

Instance: Diagnose-2-SNOMED-CT
InstanceOf: LmdiDiagnose
Description: "Eksempel på diagnose SNOMED CT og ICD-10"
* subject = Reference(eksempel-pasient-1234567890)
* code.coding[SCT].system = "http://snomed.info/sct"
* code.coding[SCT] = #276241001
* code.coding[SCT].display = "frykt for høyder"
* code.coding[ICD10].system = "urn:oid:2.16.578.1.12.4.1.1.7110"
* code.coding[ICD10] = #F40.2
* code.coding[ICD10].display = "Spesifikke (isolerte) fobier"
* code.text = "Høydeskrekk"