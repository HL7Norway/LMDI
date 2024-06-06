Profile:     LmdiPractitionerRole
Id:          lmdi-practitionerrole
Parent:      PractitionerRole
Title:       "Rolle helsepersonell"
Description: "Rollen til helsepersonellet eller personen som har foreskrevet eller administrert legemiddelet"
* ^status = #draft
* ^date = "2024-06-05"
* ^publisher = "Folkehelseinstituttet"
// Evt begrensninger på roller. 
// Utilstrekkelige kodeverk i no-basis-PractitionerRole. Meldt inn som issue hos no-basis-r4.
// Se også issue #14 

// EKSEMPLER
Instance: RolleHelsepersonell-1
InstanceOf: LmdiPractitionerRole
Description: "Eksempel på rolle (Hjemmehjelp), ikke komplett kodeverk"
* code.text = "Hjemmehjelp"