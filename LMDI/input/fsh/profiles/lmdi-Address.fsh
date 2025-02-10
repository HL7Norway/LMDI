// // Adresse med kommunenummer. Skal baseres på no-basis-adress. 
// Profile: Adresse
// Parent: Address
// Id: lmdi-address
// Title: "Adresse"
// Description: "Adresse som inneholder utvidelse for kommune"
// * ^status = #draft
// * ^experimental = true
// * ^date = "2024-05-30"
// // Extension: Kommunenummer
// * district.extension contains NoBasisMunicipalitycode named municipalitycode 0..1
// * district.extension[municipalitycode] ^short = "Coded value for municipality/county Norwegian kommune"
// * district.extension[municipalitycode] ^definition = "Coded value for municipality/county Norwegian kommune"

// // Kopiert fra Thomas sin fsh-no-basis
// // Kommentert vekk og puttet i lmdi-Organization.fsh inntil videre. 

// // EKSEMPLER
// Instance: EksempelAdresse
// InstanceOf: Adresse
// Description: "Eksempel på adresse med kun kommunenummer"
// Usage: #inline
// * district = "Oslo"
// * district.extension[municipalitycode].valueCoding = urn:oid:2.16.578.1.12.4.1.1.3402#0301 "Oslo"
// * city = "Oslo"
// * postalCode = "0001"
// * country = "NO"

