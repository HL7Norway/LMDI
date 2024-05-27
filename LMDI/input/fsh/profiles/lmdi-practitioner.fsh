Profile:     LmdiPractitioner
Id:          lmdi-practitioner
Parent:      Practitioner
Title:       "Helsepersonell"
Description: "Helsepersonell som har foreskrevet eller administrert legemiddelet"
* ^status = #draft
* ^date = "2024-05-27"

// TODO #5 "Helsepersonell" skal baseres på no-basis-practitioner
// Se: https://simplifier.net/HL7Norwayno-basis/NoBasisPractitioner/~overview 
// Krav: Identifikator
* identifier 1..1
* identifier.value 1..1 
* identifier.value ^short = "Selve identifikatoren"
// MVP: HPR-nummer
* identifier.system = "urn:oid:2.16.578.1.12.4.1.4.4"
* identifier.system ^short = "MIDLERTIDIG låst til HPR"

// Krav: Spesialitet (qualification)
* qualification MS
* qualification ^short = "Spesialitet"
// MVP: urn:oid:2.16.578.1.12.4.1.1.7426 - Godkjent spesialitet for helsepersonell registrert i HPR.
// Se Volven https://volven.no/produkt.asp?id=521762&catID=3&subID=8
* qualification.code.coding.system = "urn:oid:2.16.578.1.12.4.1.1.7426" 

Instance: Helsepersonell-1
InstanceOf: LmdiPractitioner
Description: "Eksempel på helsepersonell med HPR-nummer"
* identifier.system = "urn:oid:2.16.578.1.12.4.1.4.4"
* identifier.value = "9144900"
* name.family = "Lin"
* name.given = "Rita"