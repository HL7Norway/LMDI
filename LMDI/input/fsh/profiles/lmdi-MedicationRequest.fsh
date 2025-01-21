Profile: Legemiddelrekvirering
Parent: MedicationRequest
Id: lmdi-medicationrequest
Title: "Legemiddelrekvirering"
Description: "Legemiddelrekvirering - ordinering, resept eller annen rekvirering av legemiddel"

* ^status = #draft
* ^date = "2025-01-16"
* ^publisher = "Folkehelseinstituttet"

* identifier 0..* MS
* identifier ^short = "Identifikator for rekvisisjon"
* identifier ^definition = "Must Support: En identifikator som unikt identifiserer en rekvisisjon må oppgis om en slik finnes"
* identifier ^comment = "TODO / ESS / Krav: ForskrivningsID. Det er ytret behov for en (business-)identifier for forskrivning. Dette finnes ikke hvis det ikke er snakk om en faktisk instans, som f.eks. en M1 Resept (eResept). Mulig dette kan benyttes for interne ID'er ved f.eks. forordning på sykehus. Uvisst behov. "

* status 1..1 MS
* status ^short = "Status for rekvisisjon"
* status ^definition = "Must Support: Status er viktig for å kunne følge livssyklusen til en resept/rekvisisjon og må støttes av alle systemer"
* status from http://hl7.org/fhir/ValueSet/medicationrequest-status
* status ^comment = "Gyldige verdier: active | on-hold | cancelled | completed | entered-in-error | stopped | draft"

* intent 1..1 MS
* intent ^short = "Hensikten med forskrivningen"

* medication[x] only Reference(Legemiddel)
* medication[x] 1..1 MS
* medication[x] ^short = "Referanse til legemiddel"

* subject 1..1 MS
* subject only Reference(Pasient)
* subject ^short = "Referanse til pasient"

* requester 1..1 MS
* requester only Reference(Helsepersonell)
* requester ^short = "Referanse til rekvirent"

// Krav/forslag som bør vurderes
// Krav/forslag: Diagnose (reasonCode)
// Krav/forslag: Dosering
// Krav/forslag: Indikasjon
// Krav/forslag: Legemiddelforordnetføropphold
// Krav/forslag: Tid oppstart
// Krav/forslag: Seponeringsårsak 
// Krav/forslag: Tid seponering
// Krav/forslag: Type legemiddelbruk

// Deaktiverte elementer
* text 0..0
* recorder 0..0
* insurance 0..0