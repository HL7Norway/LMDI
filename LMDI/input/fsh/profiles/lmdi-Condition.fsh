// Documentation: https://www.hl7.org/fhir/R4/condition.html 
Profile: LmdiDiagnose
Parent: Condition
Id: lmdi-condition-diagnose
Title: "Diagnose"
Description: "Diagnosen som pasienten har fått rekvirert og administrert legemiddelet for"
* ^status = #draft
* ^date = "2024-05-27"
* ^publisher = "Folkehelseinstituttet"

// NB! Må peke på subject (pasient)
// MVP: ICPC-2 eller ICD-10
* code 1..1
* code ^short = "Diagnosekode"

// EKSEMPLER
Instance: Diagnose-1-ICD10-OID
InstanceOf: LmdiDiagnose
Description: "Eksempel på diagnose"
* subject = Reference(eksempel-pasient-1234567890)
* code.coding.system = "urn:oid:2.16.578.1.12.4.1.1.7110"
* code.coding = #R63.3
* code.coding.display = "Vanskeligheter med inntak og tilførsel av mat"

Instance: Diagnose-2-ICD10-HL7
InstanceOf: LmdiDiagnose
Description: "Eksempel på diagnose"
* subject = Reference(eksempel-pasient-1234567890)
* code.coding.system = "http://hl7.org/fhir/ValueSet/icd-10"
* code.coding = #R63.3
* code.coding.display = "Vanskeligheter med inntak og tilførsel av mat"