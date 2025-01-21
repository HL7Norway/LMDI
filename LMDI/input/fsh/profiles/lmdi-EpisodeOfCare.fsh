Profile: Institusjonsopphold
Parent: EpisodeOfCare
Id: lmdi-episodeofcare
Title: "Institusjonsopphold"
Description: "Beskrivelse av pasientens opphold i institusjon. Dette kan være både av kortere og lengre karakter, slik som døgnopphold, innleggelse hos spesialist, sykehjem og aldershjem."


* ^status = #draft
* ^date = "2024-06-12"
* ^publisher = "Folkehelseinstituttet"

* condition only Reference(Diagnose)

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

// Eksempler
Instance: Institusjonsopphold-1-Sykehjem
InstanceOf: Institusjonsopphold
Description: "Eksempel på institusjonsopphold med EpisodeOfCare"
* status = #active
* patient = Reference(pasientreferanse-1234567)
* managingOrganization = Reference(sykehjemref-1234567)
* period.start = "2024-04-01"
* period.end = "2024-05-30"

Instance: pasientreferanse-1234567
InstanceOf: Patient
Description: "Eksempel på en pasient"

Instance: sykehjemref-1234567
InstanceOf: Organization
Description: "Eksempel på et sykehjem"