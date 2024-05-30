// PLACEHOLDER ADDRESS
Profile: LmdiAdresse
Parent: Address
Id: lmdi-address
Title: "Adresse"
Description: "Adresse som inneholder utvidelse for kommune"
* ^status = #draft
* ^date = "2024-05-30"
// Extension: Kommunenummer
* extension(no-basis-municipalitycode)

// Kopiert fra Thomas sin fsh-no-basis
Extension: NoBasisMunicipalitycode
Id: no-basis-municipalitycode
Title: "no-basis-municipalitycode"
Description: "Coded value for municipality/county Norwegian kommune"
* ^version = "2.0.16"
* ^date = "2021-04-09"
* ^context.type = #element
* ^context.expression = "Address.district"
* value[x] only Coding
* value[x].system ^definition = "All Norwegian kommunenummer/municipalitycodes are published by SSB"
* value[x].code ^short = "Actual kommunenummer"
* value[x].code ^definition = "Norwegian kommunenummer/municipalitycode"

// EKSEMPLER
// FSH genererer ikke eksempler for datatyper, ergo Usage=inline for å unngå feilmeldinger. 
Instance: Adresse-1
InstanceOf: LmdiAdresse
Description: "Eksempel på adresse med kun kommunenummer"
Usage: #inline
