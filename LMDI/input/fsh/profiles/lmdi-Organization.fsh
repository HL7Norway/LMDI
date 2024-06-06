Profile: LmdiOrganization
Parent: Organization
Id: lmdi-organization
Title: "Organisasjon"
Description: "Organisasjon eller organisasjonsenhet. "
* ^status = #draft
* ^date = "2024-06-05"
* ^publisher = "Folkehelseinstituttet"

// Krav (nasjonalt): Basere på no-basis-Organization
// Krav: Organisasjons-ID som ENH eller RESH (identifier)
* identifier 1..* 
* identifier ^short = "Unik identifikasjon av behandlingsenhet / avdeling / intitusjon"

// Krav: Type organisasjon / organisatorisk nivå / betegnelse
* type MS
* type ^short = "Organisatorisk nivå / betegnelse"

// Krav: Navn (name)
* name MS
* name ^short = "Navn på organisasjonsenhet"
* name ^definition = "Eks. avdelingsnavn / institsjonsnavn / org navn"

// Krav: Kommune (.district.extension:municipalitycode, fra no-basis)
// TODO #8 Utvide Organisasjon med utvidelse for kommunenummer fra no-basis
* address MS
* address.district.extension contains NoBasisMunicipalitycode named municipalitycode 0..1
* address.district.extension[municipalitycode] ^short = "Coded value for municipality/county Norwegian kommune"
* address.district.extension[municipalitycode] ^definition = "Coded value for municipality/county Norwegian kommune"

// Krav: Del av organisasjon (ref:organization)
// * partOf MS <- NB! kan bare peke oppover

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

Instance: Organisasjon-1
InstanceOf: LmdiOrganization
Description: "Eksempel på organisasjon"
* identifier.system = "urn:oid:2.16.578.1.12.4.1.4.101"
* identifier.value = "1234567890"
* name = "Lykkedalen eldrehjem"
* address.district = "Sigdal kommune"
* address.district[0].extension[NoBasisMunicipalitycode].valueCoding = #3332