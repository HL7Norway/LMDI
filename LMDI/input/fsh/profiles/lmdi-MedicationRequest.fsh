Profile: Legemiddelrekvirering
Parent: MedicationRequest
Id: lmdi-medicationrequest
Title: "Legemiddelrekvirering"
Description: "Legemiddelrekvirering - ordinering eller annen rekvirering av legemiddel"

// Metadata
* ^status = #draft
* ^date = "2025-01-16"
* ^publisher = "Folkehelseinstituttet"

// Deaktiverte elementer
* text 0..0
* recorder 0..0
* insurance 0..0
* encounter 0..0
* supportingInformation 0..0
* performer 0..0
* performerType 0..0
* basedOn 0..0
* note 0..0
* dispenseRequest 0..0
* detectedIssue 0..0
* eventHistory 0..0
* dosageInstruction.text 0..0

// Identifikator
* identifier 0..* MS
* identifier ^short = "Identifikator for rekvisisjon"
* identifier ^definition = "Must Support: En identifikator som unikt identifiserer en rekvirering må oppgis om en slik finnes"

// Status og intensjon
* status 1..1 MS
* status ^short = "Status for rekvireringen"
* status ^definition = "Must Support: Status er viktig for å kunne følge livssyklusen til en rekvisisjon og må støttes av alle systemer"
* status from http://hl7.org/fhir/ValueSet/medicationrequest-status
* status ^comment = "Gyldige verdier: active | on-hold | cancelled | completed | entered-in-error | stopped | draft"

* intent 1..1 MS
* intent ^short = "Intensjonen eller hensikten med rekvireringen: : proposal | plan | order | original-order | reflex-order | filler-order | instance-order | option"

// Referanser til andre ressurser
* medication[x] only Reference(Legemiddel)
* medication[x] 1..1 MS
* medication[x] ^short = "Referanse til legemiddel"

* subject 1..1 MS
* subject only Reference(Pasient)
* subject ^short = "Referanse til pasient"

* requester 1..1 MS
* requester only Reference(Helsepersonell)
* requester ^short = "Referanse til rekvirent"

* reasonReference only Reference(Diagnose)
* priorPrescription only Reference(Legemiddelrekvirering)

// Andre elementer
* reported[x] only boolean

// Kommentarer
//  priorPrescription må referere til Legemiddelrekvirering

// EKSEMPEL
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
