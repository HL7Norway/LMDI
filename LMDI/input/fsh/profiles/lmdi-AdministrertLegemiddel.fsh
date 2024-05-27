// UTKAST - PLACEHOLDER
Profile: AdministrertLegemiddel
Parent:   MedicationAdministration
Id:       lmdi-administrert-legemiddel
Title:    "Administrert legemiddel"
Description: "Identifisering av legemiddel administrert til pasient på institusjon."
* ^status = #draft
* ^date = "2024-05-16"

// Se på følgende kilder:
// eResept
// Pasientens legemiddelliste / sentral forskrivningsmodul (eResept)
// HSØ Lukket legemiddelsløyfe - H-resept
// IDMP/UNICOM
// "https://hl7.org/fhir/R4/medicationadministration.html" <- R4

// TODO Se på navngivning iht. "Best Practice / HL7 Norge"

// Subject kan bare være pasient
// Legge til støtte for no-basies-Patient senere

// Krav: Status administrering = completeded, påkrevd
* status 1..1 
* status = #completeded

// Krav: Legemiddel, påkrevd
// * medication 1..1 (allerede 1..1 i ressursen)


// * subject only Reference(Patient or $no-basis-Patient)
* subject only Reference(Patient)

// Krav: Opphold, må støtte
* context MS // peke på encounter

// Krav: Tidspunkt for administrasjon, påkrevd dateTime
// occurence
// effective

// Krav: Helsepersonell, må støtte
// performer AND performer.actor MS

// Krav: Referanse til rekvisisjon, må støtte
* request MS

// Krav: Administrasjonsvei
// * dosage.route MS

// Krav: Administrert mengde
// * dosage.dose MS
* dosage MS

// Krav: Infusjon
// ESS: Er vel del av administrasjonsvei? 

