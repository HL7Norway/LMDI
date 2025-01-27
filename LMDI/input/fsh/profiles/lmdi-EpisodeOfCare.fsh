Profile: Institusjonsopphold
Parent: EpisodeOfCare
Id: lmdi-episodeofcare
Title: "Institusjonsopphold"
Description: "Beskrivelse av pasientens opphold i institusjon. Dette kan være både av kortere og lengre karakter, slik som døgnopphold, innleggelse hos spesialist, sykehjem og aldershjem."


* ^status = #draft
* ^date = "2024-06-12"
* ^publisher = "Folkehelseinstituttet"

* patient 1..1
* patient ^short = "Pasienten som institusjonsoppholdet gjelder."
* patient only Reference(Pasient)

* managingOrganization 1..1
* managingOrganization ^short = "Organisasjonen (institusjonen) som har ansvar for oppholdet"
* managingOrganization only Reference(Organisasjon)

* period MS
* period ^short = "Periode for pasientens (antatte) opphold i institusjon."

// TODO: Vurder behov for diagnose/utskrivningsdiagnose
* diagnosis ^comment = "Sjekke om utskrivningsdiagnose skal/bør være med."
