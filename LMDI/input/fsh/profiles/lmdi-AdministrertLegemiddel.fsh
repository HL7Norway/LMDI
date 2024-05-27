Profile: AdministrertLegemiddel
Parent:   MedicationAdministration
Id:       lmdi-administrert-legemiddel
Title:    "Administrert legemiddel"
Description: "Beskriver administrasjon av legemiddel til pasient på institusjon."
* ^status = #draft
* ^date = "2024-05-27"

// Se på følgende kilder:
// eResept
// Pasientens legemiddelliste / sentral forskrivningsmodul (eResept)
// HSØ Lukket legemiddelsløyfe - H-resept
// IDMP/UNICOM
// "https://hl7.org/fhir/R4/medicationadministration.html" <- R4

// TODO Se på navngivning iht. "Best Practice / HL7 Norge"
// YFS: Hva med LegemiddelAdministrasjon ?

// Subject kan bare være pasient
// Legge til støtte for no-basies-Patient senere

// Krav: Status administrering = completeded, påkrevd
// Allerede 1..1
// * status = http://terminology.hl7.org/CodeSystem/medication-admin-status#completed
* status = #completed
* status ^short = "Status administrering."
* status ^definition = "Status administrering. Skal alltid være satt til utført = completed. "

// Krav: Legemiddel, påkrevd
// * medication 1..1 (allerede 1..1 i ressursen)
// YFS: legg til no-basis-Medication

// * subject only Reference(Patient or $no-basis-Patient)
* subject only Reference(Patient)
* subject ^short = "Referanse til pasient"

// Krav: Opphold, må støtte
* context MS // peke på encounter
* context ^short = "Referanse til aktuelt opphold"
* context ^definition = "Referanse til hvilket opphold eller avtale pasienten var på da legemiddelet ble administrert."

// Krav: Tidspunkt for administrasjon, påkrevd dateTime
// NB! R5 bruker "occurence"
* effective[x] only dateTime
* effective[x] ^short = "Tidspunkt for administrasjon"

// Krav: Helsepersonell, må støtte
// TODO #9 Spørsmål: Skal det (på sikt) være flere som administerer, f.eks pasient selv (dispenser), eller kun helsepersonell?
* performer and performer.actor MS
* performer ^short = "Helsepersonell som har administrert legemiddelet"

// Krav: Referanse til rekvisisjon, må støtte
* request MS
* request ^short = "Referanse til rekvisisjon"

// Krav: Administrasjonsvei
// ESS: Diskuter om det bør være 0..1 MS
// Eksempler SNOMDED CT: https://www.hl7.org/fhir/R4/valueset-route-codes.html
// Volven: https://volven.no/produkt.asp?id=521599&catID=3&subID=8 <- gjenbrukes?
* dosage.route 1..1
* dosage.route ^short = "Administrasjonsvei"

// Krav: Administrert mengde
* dosage.dose 1..1
* dosage.dose ^short = "Administrert mengde"

// Krav: Infusjon
// ESS: Er vel del av administrasjonsvei? 

Instance: Administrering-1
InstanceOf: AdministrertLegemiddel
Description: "Eksempel på administrering av legemiddel"
* status = #completed
* medicationReference.reference = "Medisin-1"
* subject.reference = "Pasient-1"
* effectiveDateTime = "2024-05-28"