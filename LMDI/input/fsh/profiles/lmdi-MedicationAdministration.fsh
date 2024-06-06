Profile: AdministrertLegemiddel
Parent:   MedicationAdministration
Id:       lmdi-administrert-legemiddel
Title:    "Administrert legemiddel"
Description: "Beskriver administrasjon av legemiddel til pasient på institusjon."
* ^status = #draft
* ^date = "2024-05-27"
* ^publisher = "Folkehelseinstituttet"

// Se på følgende kilder:
// eResept
// Pasientens legemiddelliste / sentral forskrivningsmodul (eResept)
// HSØ Lukket legemiddelsløyfe - H-resept
// IDMP/UNICOM
// "https://hl7.org/fhir/R4/medicationadministration.html" <- R4

// TODO Se på navngivning iht. "Best Practice / HL7 Norge"
// Legge til støtte for no-basies-Patient senere

// Krav: Status administrering = completeded, påkrevd (allerede 1..1 i ressurs)
// Må nok også tillate #entered-in-error 
* status from LegemiddeladministreringStatus
// * status = #entered-in-error
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
// TODO #13 Legge inn støtte for at både Practitioner og PractitionerRole i MedicationAdministration
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

// VALUE SETS

ValueSet: LegemiddeladministreringStatus
Id: lmdi-medicationadministration-status
Title: "Status for legemiddeladministrasjon"
Description: "Verdisett som begrenses status til Legemiddeladministrasjon til henholdsvis 'Gjennomført' eller 'Feilregistrert'."
* ^version = "0.1.0"
* ^status = #draft
* ^experimental = true
* ^date = "2024-06-05"
* ^publisher = "Folkehelseinstituttet"
* http://hl7.org/fhir/ValueSet/medication-admin-status#completed "Gjennomført"
* http://hl7.org/fhir/ValueSet/medication-admin-status#entered-in-error "Feilregistrert"


// EKSEMPLER

Instance: Administrering-1
InstanceOf: AdministrertLegemiddel
Description: "Eksempel på administrering av legemiddel"
* status = #completed
* medicationReference = Reference(https://fhir.legemidler.example.com/legemidler/123456780)
* subject = Reference(https://fhi.no/fhir/lmdi/pasient/12345678)
* performer.actor = Reference(https://fhir.npr.no/helsepersonell/1234567890)
* effectiveDateTime = "2024-05-28"
* dosage.text = "Svelge to spiseskjéer"
* dosage.route.coding.system = "http://snomed.info/sct"
* dosage.route.coding.code = #421521009
* dosage.route.coding.display = "Swallow"
* dosage.route.text = "oralt"
* dosage.dose.value = 2.0
* dosage.dose.unit = "metric tablespoon"
* dosage.dose.system = "http://unitsofmeasure.org"
* dosage.dose.code = #tsp_us
