Profile:     LmdiPatient
Id:          lmdi-patient
Parent:      Patient
Title:       "Pasient"
Description: "Informasjon om pasienten"
* ^status = #draft
* ^date = "2024-06-07"
* ^publisher = "Folkehelseinstituttet"

// TODO #6 "Pasient" skal baseres på no-basis-Patient
// Krav: MÅ være FNR eller DNR <- profileres
// ESS: Må kanskje være MS hvis det er mulighet for kjønn+fdato
// Spør FHI: Er kommunenummer for bosted eller tjeneste? Yngve sier begge. 
// Slice med FNR + DNR, TODO usikker på mutual excl. 

// Identifikator - Fødselsnummer eller D-nummer
* identifier MS
* identifier ^short = "Identifikator for pasienten."
* identifier ^definition = "Identifikator for pasienten. Skal være fødselsnummer (FNR) eller D-nummer (DNR)."
* identifier ^slicing.discriminator.type = #pattern
* identifier ^slicing.discriminator.path = "code"
* identifier ^slicing.rules = #closed
* identifier contains
    FNR 0..1 and
    DNR 0..1
* identifier[FNR] ^short = "Fødselsnummer"
* identifier[DNR] ^short = "D-nummer"
* identifier[FNR].system = "urn:oid:2.16.578.1.12.4.1.4.1" 
* identifier[DNR].system = "urn:oid:2.16.578.1.12.4.1.4.2" 
* identifier[DNR].system ^short = "The identification of the D-nummer"
* identifier[FNR].system ^short = "The identification of the Fødselsnummer"
* identifier[FNR].value 1..1
* identifier[DNR].value 1..1

// Kjønn
* gender MS
* gender ^short = "Kjønn"
* gender ^definition = "Pasientens kjønn. Skal oppgis sammen med fødselsdato hvis det ikke finnes pasient-ID."

// Fødselsdato
* birthDate MS
* birthDate ^short = "Fødselsdato"
* birthDate ^definition = "Pasientens fødselsdato. Skal oppgis sammen med kjønn hvis det ikke finnes pasient-ID."


// EKSEMPLER

Instance: Pasient-1-Uten-FNR
InstanceOf: LmdiPatient
Description: "Eksempel på pasient med kjønn og fødselsdato"
* name.family = "Nobar"
* name.given = "Pia"
* gender = #female
* birthDate = "1958-09-19"
// (3024) Bærum. I mangel av no-basis extension (se Organization)
* address.district = "Bærum"

Instance: Pasient-2-FNR
InstanceOf: LmdiPatient
Description: "Eksempel på pasient med fødselsnummer"
* identifier[FNR].system = "urn:oid:2.16.578.1.12.4.1.4.1"
* identifier[FNR].value = "13031353453"
* name.family = "Kopter"
* name.given = "Rosa Eli"
// (3024) Bærum. I mangel av no-basis extension (se Organization)
* address.district = "Bærum"
