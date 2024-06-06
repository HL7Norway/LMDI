// Adresse med kommunenummer. Skal baseres på no-basis-adress. 
Profile: LmdiAdresse
Parent: Address
Id: lmdi-address
Title: "Adresse"
Description: "Adresse som inneholder utvidelse for kommune"
* ^status = #draft
* ^experimental = true
* ^date = "2024-05-30"
// Extension: Kommunenummer
* district.extension contains NoBasisMunicipalitycode named municipalitycode 0..1
* district.extension[municipalitycode] ^short = "Coded value for municipality/county Norwegian kommune"
* district.extension[municipalitycode] ^definition = "Coded value for municipality/county Norwegian kommune"

// Kopiert fra Thomas sin fsh-no-basis
// Kommentert vekk og puttet i lmdi-Organization.fsh inntil videre. 

// EKSEMPLER
// FSH genererer ikke eksempler for datatyper, ergo Usage=inline for å unngå feilmeldinger. 
// Instance: Adresse-1
// InstanceOf: LmdiAdresse
// Description: "Eksempel på adresse med kun kommunenummer"
// Usage: #inline
