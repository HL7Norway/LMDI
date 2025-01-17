// TODO #6 "Pasient" skal baseres på no-basis-Patient
// Spør FHI: Er kommunenummer for bosted og/eller tjeneste? Yngve sier begge. 

Profile:     Pasient
Id:          lmdiPasient
Parent:      Patient
Title:       "Pasient"
Description: "Informasjon om pasienten"
* ^status = #draft
* ^date = "2025-01-08"
* ^publisher = "Folkehelseinstituttet"

* active 0..0

* address MS
* address.city 0..0
* address.district.extension contains NoBasisMunicipalitycode named municipalitycode 0..1
* address.district.extension[municipalitycode] ^short = "Coded value for municipality Norwegian kommune"
* address.district.extension[municipalitycode] ^definition = "Coded value for municipality Norwegian kommune"
* address.text 0..0
* address.line 0..0

* birthDate MS
* birthDate ^short = "Fødselsdato"
* birthDate ^definition = "Pasientens fødselsdato."

* communication 0..0

* contact 0..0

* deceased[x] 0..0


* gender MS
* gender ^short = "Kjønn"
* gender ^definition = "Pasientens kjønn."

* generalPractitioner 0..0

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

* link 0..0

* managingOrganization 0..0

* maritalStatus 0..0

* multipleBirth[x] 0..0

* name 0..0

* photo 0..0

* telecom 0..0

* text 0..0



// EKSEMPLER

Instance: Pasient-1-Uten-FNR
InstanceOf: Pasient
Description: "Eksempel på pasient med kjønn og fødselsdato"
* gender = #female
* birthDate = "1958-09-19"
// (3024) Bærum. I mangel av no-basis extension (se Organization)
* address.district = "Bærum"

Instance: Pasient-2-FNR
InstanceOf: Pasient
Description: "Eksempel på pasient med fødselsnummer"
* identifier[FNR].system = "urn:oid:2.16.578.1.12.4.1.4.1"
* identifier[FNR].value = "13031353453"
// (3024) Bærum. I mangel av no-basis extension (se Organization)
* address.district = "Bærum"
