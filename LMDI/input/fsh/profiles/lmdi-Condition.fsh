Profile: LmdiDiagnose
Parent: Condition
Id: lmdi-condition-diagnose
Title: "Diagnose"
Description: "Diagnosen som pasienten har fått rekvirert og administrert legemiddelet for"
* ^status = #draft
* ^date = "2024-05-27"

// Krav: 
// MVP: ICPC-2 eller ICD-10
* code 1..1
* code ^short = "Diagnosekode"

// NB! Må peke på subject!

// Documentation: https://www.hl7.org/fhir/R4/condition.html 