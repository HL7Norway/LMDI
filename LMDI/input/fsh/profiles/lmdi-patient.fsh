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
// ESS: Må kanskje være MS hvis det er mulighet for kjønn+fdato
* identifier 1..1 // TODO arv fra no-basis-Patient

// Krav: Hvis ikke ID, bruk 
// - kjønn
* gender MS
* gender ^short = "Kjønn"
* gender ^definition = "Pasientens kjønn skal oppgis sammen med fødselsdato hvis det ikke finnes pasient-ID."

// - fødselsdato <- dokumentasjon
* birthDate MS
* birthDate ^short = "Fødselsdato"
* birthDate ^definition = "Pasientens fødselsdato skal oppgis sammen med kjønn hvis det ikke finnes pasient-ID."

// Krav: Kommunenummer <- kan være del av tjeneste eller adresse?
// no-basis-Address/district - extention - municipalitycode
// Spør FHI: Er kommunenummer for bosted eller tjeneste? Yngve sier begge. 