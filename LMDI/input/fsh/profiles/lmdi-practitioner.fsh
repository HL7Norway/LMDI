Profile:     LmdiPractitioner
Id:          lmdi-practitioner
Parent:      Practitioner
Title:       "Helsepersonell"
Description: "Helsepersonell som har foreskrevet eller administrert legemiddelet"
* ^status = #draft
* ^date = "2024-05-27"

// Krav til profil:
// TODO #5 "Helsepersonell" skal baseres på no-basis-practitioner

// Krav: Identifikator
* identifier 1..1
* identifier.value 1..1 
// MVP: HPR-nummer
* identifier.system = "urn:oid:2.16.578.1.12.4.1.4.4"

// Krav: Spesialitet (qualification)
* qualification MS