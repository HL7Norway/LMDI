Profile:     LmdiPractitionerRole
Id:          lmdi-practitionerrole
Parent:      PractitionerRole
Title:       "Rolle helsepersonell"
Description: "Rollen til helsepersonellet eller personen som har foreskrevet eller administrert legemiddelet"
* ^status = #draft
* ^date = "2024-06-12"
* ^publisher = "Folkehelseinstituttet"

* code ^short = "Kode for helsepersonells rolle."
* code ^comment = "Det finnes p.t. ikke gode nok kodeverk/verdisett, spesielt innenfor primærhelsetjenesten. Som placeholder settes HL7 FHIR sitt eksempel-verdisett basert på SNOMED CT. Se issue #14 på GitHub."
* code.coding.system = "http://snomed.info/sct"
// Alternativ: required | extensible | preferred | example
* code.coding.code from http://hl7.org/fhir/ValueSet/practitioner-role (example)

// EKSEMPLER
Instance: RolleHelsepersonell-1-Hjemmehjelp
InstanceOf: LmdiPractitionerRole
Description: "Eksempel på rolle (Hjemmehjelp), ikke komplett kodeverk"
* code.coding.system = "http://snomed.info/sct"
* code.coding.code = #5275007
* code.coding.display = "Auxiliary nurse (occupation)"
* code.text = "Hjemmehjelp (Helsefagarbeider)"