Profile: LmdiEpisodeOfCareInstitusjonsopphold
Parent: EpisodeOfCare
Id: lmdi-episodeofcare-institusjonsopphold
Title: "Institusjonsopphold"
Description: "Beskrivelse av pasientens opphold i institusjon. Dette kan være både av kortere og lengre karakter, slik som døgnopphold, innleggelse hos spesialist, sykehjem og aldershjem. "
* ^status = #draft
* ^date = "2024-06-12"
* ^publisher = "Folkehelseinstituttet"

* diagnosis ^comment = "TODO #15 Krav: Diagnose (utskrivningsdiagnose) (referanse). Sjekke om dette faktisk skal/bør være med." // TODO #15

* patient ^short = "Pasienten som institusjonsoppholdet gjelder."

* managingOrganization 1..1
* managingOrganization ^short = "Organisasjonen (institusjonen) som har ansvar for oppholdet"

* period MS
* period ^short = "Periode for pasientens (antatte) opphold i institusjon."

// EKSEMPLER
Instance: Institusjonsopphold-1-Sykehjem
InstanceOf: LmdiEpisodeOfCareInstitusjonsopphold
Description: "Eksempel på institusjonsopphold med EpisodeOfCare"
* status = #active
* patient = Reference(pasientreferanse-1234567)
* managingOrganization = Reference(sykehjemref-1234567)
* period.start = "2024-04-01"
* period.end = "2024-05-30"