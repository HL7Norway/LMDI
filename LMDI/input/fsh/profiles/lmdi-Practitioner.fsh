Profile:     LmdiPractitioner
Id:          lmdi-practitioner
Parent:      Practitioner
Title:       "Helsepersonell"
Description: "Helsepersonell som har foreskrevet eller administrert legemiddelet"
* ^status = #draft
* ^date = "2024-06-05"
* ^publisher = "Folkehelseinstituttet"

// TODO #5 "Helsepersonell" skal baseres på no-basis-practitioner
// Se: https://simplifier.net/HL7Norwayno-basis/NoBasisPractitioner/~overview 
// Krav: Identifikator
* identifier 1..1
* identifier.value 1..1 
* identifier.value ^short = "Selve identifikatoren"
// MVP: HPR-nummer
* identifier.system = "urn:oid:2.16.578.1.12.4.1.4.4"
* identifier.system ^short = "Nummer fra Helsepersonellregisteret (NPR)"
* identifier.system ^definition = "In Norway all registered health care personnel is registered in the Helsepersonellregister (HPR) and is assigned a HPR-number that is used to identify the health care practitioner. Health care personnel not registered in HPR can use FNR for identification."
* identifier.system ^comment = "Midlertidig låst til HPR. Engelsk beskrivelse fra no-basis-practitioner."

// Krav: Spesialitet (qualification)
* qualification MS
* qualification ^short = "Spesialitet"
// MVP: urn:oid:2.16.578.1.12.4.1.1.7426 - Godkjent spesialitet for helsepersonell registrert i HPR.
* qualification.code.coding.system = "urn:oid:2.16.578.1.12.4.1.1.7426"
* qualification.code.coding.system ^short = "Helsepersonellregisterets (HPR) klassifikasjon av spesialiteter (OID=7426)"
* qualification.code.coding.system ^definition = "Dette kodeverket inneholder koder for spesialiteter i Helsepersonellregisteret. Kilde: Forskrift om spesialistgodkjenning av helsepersonell og turnusstillinger for leger."


// EKSEMPLER
Instance: Helsepersonell-1-HPR-nummer
InstanceOf: LmdiPractitioner
Description: "Eksempel på helsepersonell med HPR-nummer"
* identifier.system = "urn:oid:2.16.578.1.12.4.1.4.4"
* identifier.value = "9144900"
* name.family = "Lin"
* name.given = "Rita"
