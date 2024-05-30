// Institusjonsopphold basert på EpisodeOfCare
Profile: LmdiEpisodeOfCareInstitusjonsopphold
Parent: EpisodeOfCare
Id: lmdi-episodeofcare-institusjonsopphold
Title: "Institusjonsopphold B"
Description: "Beskrivelse av pasientens opphold i institusjon."
* ^status = #draft
* ^date = "2024-05-30"

// Krav: identifier ESS: Finnes ingen nasjonal business-identifier for Encounter
// Krav: actualPeriod
* period MS
* period ^short = "Periode for pasientens opphold i institusjon."

// TODO #7 Vurdere Encounter opp mot EpisodeOfCare

// EKSEMPLER
// Kommer...