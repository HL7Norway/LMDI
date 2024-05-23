Profile:     LmdiPatient
Id:          lmdi-patient
Parent:      Patient
Title:       "LMDI Patient Profile"
Description: "Kun et eksempel for å vise verktøy"
* ^status = #draft
* ^date = "2024-05-23"

// Krav til profil:
// Krav (nasjonalt): Baseres på no-basis-patient <- profileres
// Parent: no-basis-Patient

// Krav: MÅ være FNR eller DNR <- profileres
// Krav: Hvis ikke ID, bruk kjønn+fødselsdato <- dokumentasjon
// Krav: Må STØTTE ha navn! <- eksempel
* name MS
// Krav: Kommunenummer <- kan være del av tjeneste eller adresse?
// no-basis-Address/district - extention - municipalitycode
// Spør FHI: Er kommunenummer for bosted eller tjeneste? Yngve sier begge. 