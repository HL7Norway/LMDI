// TODO #8 Utvide Organisasjon med utvidelse for kommunenummer fra no-basis

Profile: LmdiOrganization
Parent: Organization
Id: lmdi-organization
Title: "Organisasjon"
Description: "Organisasjon eller organisasjonsenhet. "
* ^status = #draft
* ^date = "2024-06-12"
* ^publisher = "Folkehelseinstituttet"

* identifier ^slicing.discriminator.type = #pattern
* identifier ^slicing.discriminator.path = "system"
* identifier ^slicing.rules = #closed
* identifier contains ENH 0..1 and RESH 0..1
* identifier 1..* 
* identifier ^short = "Unik identifikasjon av enhet basert på organisasjonsnummer eller RESH-id."
* identifier ^comment = "Skal baseres på no-basis-Organization."
* identifier[ENH] ^short = "Organisasjonsnummer fra Enhetsregisteret"
* identifier[RESH] ^short = "Id fra Register for enheter i spesialisthelsetjenesten (RESH)"
* identifier[ENH].system = "urn:oid:2.16.578.1.12.4.1.4.101" 
* identifier[RESH].system = "urn.oid:2.16.578.1.12.4.1.4.102" 
* identifier[ENH].value 1..1
* identifier[RESH].value 1..1

* type MS
* type ^short = "Organisatorisk nivå / betegnelse"
* type ^comment = "Mangler gode kodeverk. De som er i no-basis-organization er ikke tilstrekkelig. "

* name MS
* name ^short = "Navn på organisasjonsenhet"
* name ^definition = "Eks. avdelingsnavn / institsjonsnavn / org navn"
* name ^comment = "Inkluderer helst hvis opplysningen finnes."

* address MS
* address.district.extension contains NoBasisMunicipalitycode named municipalitycode 0..1
* address.district.extension[municipalitycode] ^short = "Coded value for municipality/county Norwegian kommune"
* address.district.extension[municipalitycode] ^definition = "Coded value for municipality/county Norwegian kommune"

* partOf MS
* partOf ^short = "Del av organisasjon"
* partOf ^comment = "Er det behov for nivåer, rekursjon? NB! Kan bare peke oppover."

// Kopiert fra Thomas sin fsh-no-basis
Alias: $kommunenummer-alle = https://register.geonorge.no/subregister/sosi-kodelister/kartverket/kommunenummer-alle
Extension: NoBasisMunicipalitycode
Id: no-basis-municipalitycode
Title: "no-basis-municipalitycode"
Description: "Coded value for municipality/county Norwegian kommune"
* ^version = "2.0.16"
* ^date = "2021-04-09"
* ^context.type = #element
* ^context.expression = "Address.district"
* value[x] only Coding
* value[x] from $kommunenummer-alle (required)
* value[x].system ^definition = "All Norwegian kommunenummer/municipalitycodes are published by SSB"
* value[x].code ^short = "Actual kommunenummer"
* value[x].code ^definition = "Norwegian kommunenummer/municipalitycode"

// EKSEMPLER

Instance: Organisasjon-1-Eldrehjem
InstanceOf: LmdiOrganization
Description: "Eksempel på organisasjon - Primærhelsetjeneste"
* identifier[ENH].system = "urn:oid:2.16.578.1.12.4.1.4.101"
* identifier[ENH].value = "1234567890"
* name = "Lykkedalen eldrehjem"
* address.district = "Sigdal"
* address.district[0].extension[NoBasisMunicipalitycode].valueCoding = #3034

Instance: Organisasjon-2-Spesialist-RESH
InstanceOf: LmdiOrganization
Description: "Eksempel på organisasjon - spesialisthelsetjenesten med RESH."
* identifier[RESH].system = "urn.oid:2.16.578.1.12.4.1.4.102"
* identifier[RESH].value = "4208723"
* name = "Avdeling for epilepsi, poliklinikk" 
* partOf = Reference(Organisasjon-3-Spesialist-topp)

// OUS -> Nevroklinikken -> Avdeling for epilepsi, poliklinikk
// Offisielt navn: Avdeling for epilepsi, poliklinikk
// Kortnavn: SSE avd for epilepsi,poliklinikk
// Rekvirentkode: SSE-POL
// TODO #24 Lage eksempel på partOf med OUS for lmdi-Organization

Instance: Organisasjon-3-Spesialist-topp
InstanceOf: LmdiOrganization
Description: "Eksempel på organisasjon - spesialisthelsetjenesten med RESH - toppnivå."
* identifier[ENH].system = "urn:oid:2.16.578.1.12.4.1.4.101"
* identifier[ENH].value = "993467049"
* identifier[RESH].system = "urn.oid:2.16.578.1.12.4.1.4.102"
* identifier[RESH].value = "4001031"
* name = "Oslo universitetssykehus HF"
