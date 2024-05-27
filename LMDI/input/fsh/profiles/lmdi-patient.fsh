Profile:     LmdiPatient
Id:          lmdi-patient
Parent:      Patient
Title:       "Pasient"
Description: "Informasjon om pasienten"
* ^status = #draft
* ^date = "2024-05-23"

// Krav til profil:
// TODO #6 "Pasient" skal baseres på no-basis-Patient
// Parent: no-basis-Patient

// Krav: MÅ være FNR eller DNR <- profileres
// ESS: Må kanskje være MS hvis det er mulighet for kjønn+fdato
// Slice med FNR + DNR, TODO usikker på mutual excl.
* identifier MS
* identifier ^short = "Identifikator for pasienten."
* identifier ^definition = "Identifikator for pasienten. Skal være fødselsnummer (FNR) eller D-nummer (DNR)."
* identifier ^slicing.discriminator.type = #pattern
* identifier ^slicing.discriminator.path = "code"
* identifier ^slicing.rules = #closed
* identifier contains
    FNR 0..1 and
    DNR 0..1
* identifier[FNR].system = "urn:oid:2.16.578.1.12.4.1.4.1" 
* identifier[DNR].system = "urn:oid:2.16.578.1.12.4.1.4.2" 
* identifier[DNR].system ^short = "The identification of the D-nummer"
* identifier[FNR].system ^short = "The identification of the Fødselsnummer"
* identifier[FNR].value 1..1
* identifier[DNR].value 1..1

// Krav: Hvis ikke ID, bruk 
// - kjønn
* gender MS
* gender ^short = "Kjønn"
* gender ^definition = "Pasientens kjønn. Skal oppgis sammen med fødselsdato hvis det ikke finnes pasient-ID."

// - fødselsdato <- dokumentasjon
* birthDate MS
* birthDate ^short = "Fødselsdato"
* birthDate ^definition = "Pasientens fødselsdato. Skal oppgis sammen med kjønn hvis det ikke finnes pasient-ID."

// Krav: Kommunenummer <- kan være del av tjeneste eller adresse?
// no-basis-Address/district - extention - municipalitycode
// Spør FHI: Er kommunenummer for bosted eller tjeneste? Yngve sier begge. 

Instance: PatientExample
InstanceOf: LmdiPatient
Description: "Eksempel på pasient
* name.family = "Seland"
* name.given[0] = "Espen"
* gender = #male
* birthDate = "1977-03-12"