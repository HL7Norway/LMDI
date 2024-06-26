Profile: Legemiddelrekvirering
Parent: MedicationRequest
Id: Legemiddelrekvirering
Title: "Legemiddelrekvirering"
Description: "Legemiddelrekvirering - ordinering, resept eller annen rekvirering av legemiddel"
* ^status = #draft
* ^date = "2024-06-12"
* ^publisher = "Folkehelseinstituttet"

* identifier ^comment = "TODO / ESS / Krav: ForskrivningsID. Det er ytret behov for en (business-)identifier for forskrivning. Dette finnes ikke hvis det ikke er snakk om en faktisk instans, som f.eks. en M1 Resept (eResept). Mulig dette kan benyttes for interne ID'er ved f.eks. forordning på sykehus. Uvisst behov. "

* status ^short = "Status rekvisisjon"

* intent ^short = "Hensikten med forskrivningen"

* medication[x] ^short = "Referanse til legemiddel"

* subject only Reference(Patient)
* subject ^short = "Referanse til pasient"

* requester 1..1
* requester ^short = "Referanse til rekvirent"
* requester only Reference(Practitioner)

// Krav/forslag: Diagnose (reasonCode)
// Krav/forslag: Dosering ???
// Krav/forslag: Indikasjon ???
// Krav/forslag: Legemiddelforordnetføropphold
// Krav/forslag: Tid oppstart
// Krav/forslag: Seponeringsårsak 
// Krav/forslag: Tid seponering
// Krav/forslag: Type legemiddelbruk