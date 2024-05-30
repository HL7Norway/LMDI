// Institusjonsopphold basert på Encounter
Profile: LmdiEncounterInstitusjonsopphold
Parent: Encounter
Id: lmdi-encounter-institusjonsopphold
Title: "Institusjonsopphold A"
Description: "Beskrivelse av pasientens opphold i institusjon - bruker Encounter."
* ^status = #draft
* ^date = "2024-05-30"

// Krav: identifier ESS: Finnes ingen nasjonal business-identifier for Encounter
// Krav: actualPeriod
* period MS
* period ^short = "Periode for pasientens opphold i institusjon."

// TODO #7 Vurdere Encounter opp mot EpisodeOfCare

// EKSEMPLER
// Kommer...