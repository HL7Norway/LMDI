// TODO #5 "Helsepersonell" skal baseres på no-basis-practitioner
// Se: https://simplifier.net/HL7Norwayno-basis/NoBasisPractitioner/~overview 

Profile:     LmdiPractitioner
Id:          lmdi-practitioner
Parent:      Practitioner
Title:       "Helsepersonell"
Description: """Helsepersonell som har foreskrevet eller administrert legemiddelet. 

Basisprofil for Norwegian Practitioner information. Defined by The Norwegian Directorate of eHealth and HL7 Norway. Should be used as a basis for further profiling in use-cases where specific identity information is needed. The basis profile is open, but derived profiles should close down the information elements according to specification relevant to the use-case.

2019-03 - The no-basis-Practitioner resource main use-case is to represent the actual Practitioner, e.g. a person. The resource can include information about how to identify the practitioner in addition to the practitioner's education, qualifications and speciality. The resource can also include approvals and other centrally registered capabilities recorded for the practitioner.

(Engelsk tekst Hentet fra no-basis-practitioner.)
"""
* ^status = #draft
* ^date = "2024-06-12"
* ^publisher = "Folkehelseinstituttet"

* identifier 1..1
* identifier.value 1..1 
* identifier.value ^short = "Selve identifikatoren"
* identifier.system = "urn:oid:2.16.578.1.12.4.1.4.4"
* identifier.system ^short = "Nummer fra Helsepersonellregisteret (HPR)"
* identifier.system ^definition = "In Norway all registered health care personnel is registered in the Helsepersonellregister (HPR) and is assigned a HPR-number that is used to identify the health care practitioner. Health care personnel not registered in HPR can use FNR for identification."
* identifier.system ^comment = "Midlertidig låst til HPR. Engelsk beskrivelse fra no-basis-practitioner."

* qualification MS
* qualification ^short = "Spesialitet"
* qualification.code.coding.system = "urn:oid:2.16.578.1.12.4.1.1.7426"
* qualification.code.coding.system ^short = "Helsepersonellregisterets (HPR) klassifikasjon av spesialiteter (OID=7426)"
* qualification.code.coding.system ^definition = "Dette kodeverket inneholder koder for spesialiteter i Helsepersonellregisteret. Kilde: Forskrift om spesialistgodkjenning av helsepersonell og turnusstillinger for leger."
* qualification.code.coding.system ^comment = "MVP - satt til HPR-spesialieter (OID=7426)."

// EKSEMPLER
Instance: Helsepersonell-1-HPR-nummer
InstanceOf: LmdiPractitioner
Description: "Eksempel på helsepersonell med HPR-nummer"
* identifier.system = "urn:oid:2.16.578.1.12.4.1.4.4"
* identifier.value = "9144900"
* name.family = "Lin"
* name.given = "Rita"
* qualification.code.coding.system = "urn:oid:2.16.578.1.12.4.1.1.7426"
* qualification.code.coding.code = #1
* qualification.code.coding.display = "Allmennmedisin"