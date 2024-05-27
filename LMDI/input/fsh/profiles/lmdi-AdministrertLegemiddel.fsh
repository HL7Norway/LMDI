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

// Krav: Legemiddel, påkrevd
// * medication 1..1 (allerede 1..1 i ressursen)
// YFS: legg til no-basis-Medication

// * subject only Reference(Patient or $no-basis-Patient)
* subject only Reference(Patient)

// Krav: Opphold, må støtte
* context MS // peke på encounter

// Krav: Tidspunkt for administrasjon, påkrevd dateTime
* effective[x] only dateTime

// Krav: Helsepersonell, må støtte
* performer and performer.actor MS

// Krav: Referanse til rekvisisjon, må støtte
* request MS

// Krav: Administrasjonsvei
// ESS: Diskuter om det bør være 0..1 MS
* dosage.route 1..1

// Krav: Administrert mengde
* dosage.dose 1..1

// Krav: Infusjon
// ESS: Er vel del av administrasjonsvei? 
