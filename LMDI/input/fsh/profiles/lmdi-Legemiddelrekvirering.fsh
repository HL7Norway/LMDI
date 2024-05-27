Profile: Legemiddelrekvirering
Parent: MedicationRequest
Id: Legemiddelrekvirering
Title: "Legemiddelrekvirering"
Description: "Legemiddelrekvirering - ordinering, resept eller annen rekvirering av legemiddel"
* ^status = #draft
* ^date = "2024-05-27"

// Krav: ForskrivningsID
// * identifier MS

// Krav: Status rekvisisjon (status), allerede 1..1
// * status 1..1
* status ^short = "Status rekvisisjon"

// Krav: Hensikt (intent), allerede 1..1
* intent ^short = "Hensikt med forskrivningen"

// Krav: Legemiddel (medication), allerede 1..1
* medication[x] ^short = "Referanse til legemiddel"

// Krav: Pasient (subject), allerede 1..1, men åpen
* subject only Reference(Patient)
* subject ^short = "Referanse til pasient"

// Krav: Rekvirent (practitioner)
* requester 1..1
* requester ^short = "Referanse til rekvirent"
* requester only Reference(Practitioner)

// Krav: Diagnose (reasonCode)
// Krav: Dosering ???
// Krav: Indikasjon ???
// Krav: Legemiddelforordnetføropphold
// Krav: Tid oppstart
// Krav: Seponeringsårsak 
// Krav: Tid seponering
// Krav: Type legemiddelbruk