// Hoveddefinisjon av organisasjonsprofil
Profile: Organisasjon
Parent: Organization
Id: lmdi-organization
Title: "Organisasjon"
Description: """
Organisasjoner i norsk helse- og omsorgstjeneste, som post, avdeling, klinikk, sykehus og sykehjem. 

Denne profilen av Organization benyttes for å beskrive helseinstitusjoner og skal representere organisasjonen på lavest mulig nivå i organisasjonshierarkiet (f.eks. en avdeling eller klinikk eller post).

For organisasjonen som er del av en større organisasjon, skal dette angis ved hjelp av partOf-relasjonen. Alle “organisasjonshierarki” skal inkludere minst et organisasjonsnummer fra Enhetsregisteret (identifier:ENH) 
"""
* ^version = "0.9.3"
* ^status = #draft
* ^date = "2025-02-27"
* ^publisher = "Folkehelseinstituttet"

// Deaktiverte felter
* text 0..0
* active 0..0
* telecom 0..0
* contact 0..0
* endpoint 0..0
* address.text 0..0
* address.line 0..0
* address.postalCode 0..0

// Identifikatorer - hovedregler
* identifier 0..* MS
* identifier ^slicing.discriminator.type = #pattern
* identifier ^slicing.discriminator.path = "system"
* identifier ^slicing.rules = #closed
* identifier ^short = "ID fra Nasjonalt register for enheter i spesialisthelsetjenesten (RESH) eller Organisasjonsnummeret i Enhetsregister"
* identifier ^comment = "Der aktiviteten har skjedd."

// Identifikatorer - ENH og RESH
* identifier contains
    ENH 0..1 and
    RESH 0..1

* identifier[ENH] ^short = "Organisasjonsnummer fra Enhetsregisteret (ENH)"
* identifier[ENH] ^comment = "Identifikatorer skal angis på laveste relevante virksomhetsnivå i henhold til SSBs retningslinjer. For kommunale tjenester betyr dette på institusjonsnivå (f.eks sykehjem) der egen organisatorisk enhet er etablert, ikke på overordnet kommunenivå."
* identifier[ENH].system = "urn:oid:2.16.578.1.12.4.1.4.101" (exactly)
* identifier[ENH].value 1..1
* identifier[ENH].value ^short = "Organisasjonsnummer"

* identifier[RESH] ^short = "ID fra Register for enheter i spesialisthelsetjenesten (RESH)"
* identifier[RESH] ^comment = "Det nivået aktiviteten har skjedd på."
* identifier[RESH].system = "urn:oid:2.16.578.1.12.4.1.4.102" (exactly)
* identifier[RESH].value 1..1
* identifier[RESH].value ^short = "RESH-ID"

// Organisasjonstype og navn
* type 1..*
* type ^short = "Organisasjonstype"
* type ^definition = "Type organisasjon (f.eks. sykehus, avdeling, klinikk)"
* type from $organization-type (preferred)

* name 1..1 MS 
* name ^short = "Organisasjonsnavn"
* name ^definition = "Offisielt navn på organisasjonen"
* name ^comment = "Kan være navn på post, avdelingsnavn, klinikknavn, sykehusnavn eller sykehjemsnavn"

// Hierarkisk struktur
* partOf MS
* partOf ^short = "Overordnet organisasjon"
* partOf ^definition = "Organisasjonen som denne organisasjonen er en del av"
* partOf only Reference(Organisasjon)

// Adresse
* address MS
* address ^short = "Gjeldende fysisk adresse"
* address.type = #physical

* address.district.extension ^slicing.discriminator.type = #value
* address.district.extension ^slicing.discriminator.path = "url"
* address.district.extension ^slicing.rules = #open
* address.district.extension contains LmdiMunicipalitycode named municipalitycode 0..1

* address.district.extension[municipalitycode] ^short = "Coded value for municipality/county Norwegian kommune"
* address.district.extension[municipalitycode] ^definition = "Coded value for municipality/county Norwegian kommune"
* address.district.extension[municipalitycode] only LmdiMunicipalitycode

* address.state ^short = "Fylkesnavn"

* address.extension contains LmdiUrbanDistrict named urbanDistrict 0..1
* address.extension[urbanDistrict] ^short = "Bydel"

// EKSEMPLER
Instance: Organisasjon-1-Sykehjem
InstanceOf: Organisasjon
Description: "Eksempel på sykehjem i primærhelsetjenesten"
* identifier[ENH].system = "urn:oid:2.16.578.1.12.4.1.4.101"
* identifier[ENH].value = "1234567890"
* name = "Lykkedalen sykehjem"
* type = $organization-type#prov "Healthcare Provider"
* address.type = #physical
* address.district = "Sigdal"
* address.district.extension[municipalitycode].valueCoding = $kommunenummer-alle#3025 "Sigdal"

Instance: Organisasjon-2-Avdeling
InstanceOf: Organisasjon
Description: "Eksempel på spesialistavdeling"
* identifier[RESH].system = "urn:oid:2.16.578.1.12.4.1.4.102"
* identifier[RESH].value = "4208723"
* name = "Avdeling for epilepsi, poliklinikk"
* type = $organization-type#dept "Hospital Department"
* partOf = Reference(Organisasjon-3-Sykehus)

Instance: Organisasjon-3-Sykehus
InstanceOf: Organisasjon
Description: "Eksempel på sykehusorganisasjon"
* identifier[ENH].system = "urn:oid:2.16.578.1.12.4.1.4.101"
* identifier[ENH].value = "993467049"
* identifier[RESH].system = "urn:oid:2.16.578.1.12.4.1.4.102"
* identifier[RESH].value = "4001031"
* name = "Oslo universitetssykehus HF"
* type = $organization-type#prov "Healthcare Provider"
* address.type = #physical
* address.district = "Oslo"
* address.district.extension[municipalitycode].valueCoding = $kommunenummer-alle#0301 "Oslo"
* address.extension[urbanDistrict].valueCoding = $VsLmdiUrbanDistrict#01 "Gamle Oslo"