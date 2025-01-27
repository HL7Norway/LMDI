Profile: Legemiddelrekvirering
Parent: MedicationRequest
Id: lmdi-medicationrequest
Title: "Legemiddelrekvirering"
Description: "Legemiddelrekvirering - ordinering eller annen rekvirering av legemiddel"

* ^status = #draft
* ^date = "2025-01-16"
* ^publisher = "Folkehelseinstituttet"

* identifier 0..* MS
* identifier ^short = "Identifikator for rekvisisjon"
* identifier ^definition = "Must Support: En identifikator som unikt identifiserer en rekvirering må oppgis om en slik finnes"
* identifier ^comment = "TODO / ESS / Krav: ForskrivningsID. Det er ytret behov for en (business-)identifier for forskrivning. Dette finnes ikke hvis det ikke er snakk om en faktisk instans, som f.eks. en M1 Resept (eResept). Mulig dette kan benyttes for interne ID'er ved f.eks. forordning på sykehus. Uvisst behov. "

* status 1..1 MS
* status ^short = "Status for rekvireringen"
* status ^definition = "Must Support: Status er viktig for å kunne følge livssyklusen til en rekvisisjon og må støttes av alle systemer"
* status from http://hl7.org/fhir/ValueSet/medicationrequest-status
* status ^comment = "Gyldige verdier: active | on-hold | cancelled | completed | entered-in-error | stopped | draft"

* intent 1..1 MS
* intent ^short = "Intensjonen eller hensikten med rekvireringen"
* intent ^comment = "Gyldige verdier: proposal | plan | order | original-order | reflex-order | filler-order | instance-order | option"

* medication[x] only Reference(Legemiddel)
* medication[x] 1..1 MS
* medication[x] ^short = "Referanse til legemiddel"

* subject 1..1 MS
* subject only Reference(Pasient)
* subject ^short = "Referanse til pasient"

* requester 1..1 MS
* requester only Reference(Helsepersonell)
* requester ^short = "Referanse til rekvirent"


// Deaktiverte elementer
* text 0..0
* recorder 0..0
* insurance 0..0



Instance: Rekvirering-1
InstanceOf: Legemiddelrekvirering
Description: "Eksempel på legemiddelrekvirering av Paracet"
* identifier.system = "urn:oid:2.16.578.1.12.4.1.1.reseptid"
* identifier.value = "REK123456"
* status = #active
* intent = #order
* medicationReference = Reference(Medisin-2-Paracetamol)
* subject = Reference(Pasient-2-FNR)
* requester = Reference(Helsepersonell-1-HPR-nummer)
* authoredOn = "2025-01-27"
* dosageInstruction.text = "1-2 tabletter ved behov mot smerter, maksimalt 8 tabletter per døgn"
* dispenseRequest.validityPeriod.start = "2025-01-27"
* dispenseRequest.validityPeriod.end = "2025-07-27"
* dispenseRequest.quantity.value = 100
* dispenseRequest.quantity.unit = "tabletter"
* dispenseRequest.expectedSupplyDuration.value = 30
* dispenseRequest.expectedSupplyDuration.unit = "d"