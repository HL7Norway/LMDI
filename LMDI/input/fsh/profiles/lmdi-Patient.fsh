Profile: Pasient
Id: lmdi-patient
Parent: Patient
Title: "Pasient"
Description: "Pasienten som har fått rekvirert eller administrert legemiddel"
* ^status = #draft
* ^date = "2025-03-10"
* ^publisher = "Folkehelseinstituttet"

// Deaktiverte felter
* active 0..0
* communication 0..0
* contact 0..0
* deceased[x] 0..0
* generalPractitioner 0..0
* link 0..0
* managingOrganization 0..0
* maritalStatus 0..0
* multipleBirth[x] 0..0
* name 0..0
* photo 0..0
* telecom 0..0
* text 0..0

// Adresse
* address MS
* address.city 0..0
* address.text 0..0
* address.line 0..0
* address.district ^short = "Kommune"
* address.district.extension contains LmdiMunicipalitycode named municipalitycode 0..1
* address.district.extension[municipalitycode] ^short = "Kodet verdi for kommune"
* address.district.extension[municipalitycode] ^definition = "Kodet verdi for kommune"
* address.district.value 0..0
* address.use from http://hl7.org/fhir/ValueSet/address-use (required)
* address.use ^binding.description = "Tillatte verdier er home, temp eller old"
* address.use ^short = "home | temp | old"
* address.use ^definition = "Adressetype begrenset til home, temp eller old"
* address.use obeys address-use-constraint
* address.state ^short = "Fylkesnavn"
* address.postalCode 0..0
// Fødselsdato
* birthDate MS
* birthDate ^short = "Fødselsdato"
* birthDate ^definition = "Pasientens fødselsdato."

// Kjønn
* gender MS
* gender ^short = "Kjønn"
* gender ^definition = "Pasientens kjønn."

// Identifikatorer
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
* identifier[FNR].system = "urn:oid:2.16.578.1.12.4.1.4.1" 
* identifier[FNR].system ^short = "Unik identifikator som representerer det norske fødselsnummersystemet"
* identifier[FNR].value 1..1
* identifier[FNR].value ^short = "Fødselsnummeret (11 siffer)"
* identifier[FNR].value ^example.label = "Fødselsnummer"
* identifier[FNR].value ^example.valueString = "12345678901"

* identifier[DNR] ^short = "D-nummer"
* identifier[DNR].system = "urn:oid:2.16.578.1.12.4.1.4.2" 
* identifier[DNR].system ^short = "Unik identifikator som representerer det norske d-nummersystemet"
* identifier[DNR].value 1..1
* identifier[DNR].value ^short = "D-nummer (11 siffer)"
* identifier[DNR].value ^example.label = "D-nummer"
* identifier[DNR].value ^example.valueString = "12345678901"

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


Invariant: address-use-constraint
Description: "Kun home, temp eller old er tillatt for address.use"
Severity: #error
Expression: "address.use.empty() or address.use in ('home' | 'temp' | 'old')"

