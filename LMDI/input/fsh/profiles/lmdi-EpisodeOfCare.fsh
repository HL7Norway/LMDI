// Institusjonsopphold basert på EpisodeOfCare
Profile: LmdiEpisodeOfCareInstitusjonsopphold
Parent: EpisodeOfCare
Id: lmdi-episodeofcare-institusjonsopphold
Title: "Institusjonsopphold B"
Description: "Beskrivelse av pasientens opphold i institusjon."
* ^status = #draft
* ^date = "2024-05-30"

// Krav: actualPeriod
* period MS
* period ^short = "Periode for pasientens opphold i institusjon."

// TODO #7 Vurdere Encounter opp mot Encounter

// EKSEMPLER
Instance: Institusjonsopphold-B-1
InstanceOf: LmdiEpisodeOfCareInstitusjonsopphold
Description: "Eksempel på institusjonsopphold med EpisodeOfCare"
* status = #active
* patient = Reference(pasientreferanse-1234567)
* managingOrganization = Reference(sykehjemref-1234567)
* period.start = "2024-04-01"
* period.end = "2024-05-30"