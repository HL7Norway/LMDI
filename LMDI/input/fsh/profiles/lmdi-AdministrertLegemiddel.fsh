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

// Subject kan bare være pasient
// Legge til støtte for no-basies-Patient senere
// * subject only Reference(Patient or $no-basis-Patient)
* subject only Reference(Patient)
