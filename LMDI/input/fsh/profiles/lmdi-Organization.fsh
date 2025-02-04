// Hoveddefinisjon av organisasjonsprofil
Profile: Organisasjon
Parent: Organization
Id: lmdi-organization
Title: "Organisasjon"
Description: "Profil for organisasjoner i norsk helse- og omsorgstjeneste"
* ^version = "0.9.3"
* ^status = #draft
* ^date = "2025-01-27"
* ^publisher = "Folkehelseinstituttet"

// Grunnleggende kardinalitet
* text 0..0
* identifier 0..* MS
* active 0..0
* telecom 0..0

// Regler for identifikatorer
* identifier ^slicing.discriminator.type = #pattern
* identifier ^slicing.discriminator.path = "system"
* identifier ^slicing.rules = #closed
* identifier ^short = "Organisasjonsidentifikatorer (ENH/RESH)"
* identifier ^comment = "Identifikatorer skal angis på laveste mulige organisatoriske nivå. For eksempel organisasjonsnummer for sykehjemmet fremfor kommunen der det finnes."

// Oppdeling av identifikatortyper
* identifier contains
    ENH 0..1 and
    RESH 0..1
* identifier[ENH] ^short = "Organisasjonsnummer fra Enhetsregisteret"
* identifier[ENH] ^comment = "Identifikatorer skal angis på laveste relevante virksomhetsnivå i henhold til SSBs retningslinjer. For kommunale tjenester betyr dette på institusjonsnivå (f.eks sykehjem) der egen organisatorisk enhet er etablert, ikke på overordnet kommunenivå."
* identifier[ENH].system = "urn:oid:2.16.578.1.12.4.1.4.101" (exactly)
* identifier[ENH].value 1..1
* identifier[ENH].value ^short = "Organisasjonsnummer"

* identifier[RESH] ^short = "ID fra Register for enheter i spesialisthelsetjenesten"
* identifier[RESH] ^comment = "Det nivået aktiviteten har skjedd på."
* identifier[RESH].system = "urn:oid:2.16.578.1.12.4.1.4.102" (exactly)
* identifier[RESH].value 1..1
* identifier[RESH].value ^short = "RESH-ID"

// Organisasjonstype
* type 1..*
* type ^short = "Organisasjonstype"
* type ^definition = "Type organisasjon (f.eks. sykehus, avdeling, klinikk)"
* type from $organization-type (preferred)

// Navnekrav
* name 1..1 MS 
* name ^short = "Organisasjonsnavn"
* name ^definition = "Offisielt navn på organisasjonen"

// Adresse med kommunekode
* address MS
* address.type = #physical
* address.district MS
* address.district.extension contains NoBasisMunicipalitycode named municipalitycode 0..1

// Hierarkisk struktur
* partOf MS
* partOf ^short = "Overordnet organisasjon"
* partOf ^definition = "Organisasjonen som denne organisasjonen er en del av"
* partOf only Reference(Organisasjon)

// Definisjon av eksterne kodeverk og verdisett
Alias: $kommunenummer-alle = https://register.geonorge.no/subregister/sosi-kodelister/kartverket/kommunenummer-alle
Alias: $organization-type = http://terminology.hl7.org/CodeSystem/organization-type

// Utvidelse for kommunenummer (kopiert fra no-basis)
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

// Eksempelinstanser
Instance: Organisasjon-1-Sykehjem
InstanceOf: Organisasjon
Description: "Eksempel på sykehjem i primærhelsetjenesten"
* identifier[ENH].system = "urn:oid:2.16.578.1.12.4.1.4.101"
* identifier[ENH].value = "1234567890"
* name = "Lykkedalen sykehjem"
* type = $organization-type#prov "Healthcare Provider"
* address.type = #physical
* address.district = "Sigdal"
* address.district.extension[municipalitycode].valueCoding = $kommunenummer-alle#3025

Instance: Organisasjon-2-Avdeling
InstanceOf: Organisasjon
Description: "Eksempel på spesialistavdeling"
* identifier[RESH].system = "urn:oid:2.16.578.1.12.4.1.4.102"
* identifier[RESH].value = "4208723"
* name = "Avdeling for epilepsi, poliklinikk"
* type = $organization-type#dept "Hospital Department"
* address.type = #physical
* address.district = "Oslo"
* address.district.extension[municipalitycode].valueCoding = $kommunenummer-alle#0301
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
* address.district.extension[municipalitycode].valueCoding = $kommunenummer-alle#0301