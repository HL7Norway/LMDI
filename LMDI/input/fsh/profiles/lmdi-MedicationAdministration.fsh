Profile: AdministrertLegemiddel
Parent:   MedicationAdministration
Id:       lmdi-administrert-legemiddel
Title:    "Administrert legemiddel"
Description: """Beskriver administrasjon av legemiddel til pasient på institusjon."""
* ^status = #draft
* ^date = "2024-06-12"
* ^publisher = "Folkehelseinstituttet"

// Se på følgende kilder:
// eResept, Pasientens legemiddelliste / sentral forskrivningsmodul (eResept)
// HSØ Lukket legemiddelsløyfe - H-resept, IDMP/UNICOM
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
* subject ^definition = "Det skal alltid være en referanse til pasienten som har blitt administrert legemiddel."

// Krav: Opphold, må støtte
* context MS // peke på EpisodeOfCare
* context only Reference(EpisodeOfCare)
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
* performer.actor ^short = "Hvem som har administrert legemiddelet"
* performer.actor ^definition = "Utfører av administrering kan være helsepersonell eller en rolle knyttet til institusjonen eller pasienten. "

// Krav: Referanse til rekvisisjon, må støtte
* request MS
* request ^short = "Referanse til rekvisisjon"

// Krav: Administrasjonsvei.  
// ESS: Diskuter om det bør være 0..1 MS.
// ESS: Legger opp til både 7477 og SCT.
// TODO: #18 Administrasjonsvei (Volven OID=7477) - bruke som utkast
* dosage.route 1..1
* dosage.route ^short = "Administrasjonsvei"
* dosage.route ^definition = "Aministrasjonsvei. Er begrenset til foreslått koding fra SNOMED CT-verdisettet til HL7 og Volven-kodeverket Administrasjonsvei (OID=7477) fra eResept. "
* dosage.route.coding ^slicing.discriminator.type = #pattern
* dosage.route.coding ^slicing.discriminator.path = "system"
* dosage.route.coding ^slicing.rules = #closed
* dosage.route.coding contains SCT 0..1 and 7477 0..1
* dosage.route.coding[SCT] ^short = "SNOMED CT"
* dosage.route.coding[SCT] ^definition = "Administrasjonsvei kodet med SNOMED CT, hentet fra verdisett foreslått av HL7."
* dosage.route.coding[SCT].system = "http://snomed.info/sct"
* dosage.route.coding[SCT].code from http://hl7.org/fhir/ValueSet/route-codes (required)
* dosage.route.coding[7477] ^short = "Administrasjonsvei (OID=7477)"
* dosage.route.coding[7477] ^definition = "Administrasjonsvei (OID=7477) fra kodeverkssamling Resept."
* dosage.route.coding[7477].system = "urn:oid:2.16.578.1.12.4.1.1.7477"
// * dosage.route.coding[7477].code from http://xxx (required)

// Krav: Administrert mengde
// TODO #19 Sjekk hvordan Pasientent legemiddelliste (PLL) bruker dose med FHIR
* dosage.dose 1..1
* dosage.dose ^short = "Administrert mengde"
* dosage.dose ^definition = "Administrert mengde av legemiddelet som det blir referert til."

// Krav: Infusjon
// ESS: Er vel del av administrasjonsvei? Som f.eks. SCT#intravenøs administrasjonsvei 47625008, SCT#26643006 Oral route

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

Instance: Administrering-1-Oralt
InstanceOf: AdministrertLegemiddel
Description: "Eksempel på administrering av legemiddel"
* status = #completed
* medicationReference = Reference(https://fhir.legemidler.example.com/legemidler/123456780)
* subject = Reference(https://fhi.no/fhir/lmdi/pasient/12345678)
* context = Reference(https://fhi.no/fhir/lmdi/institusjonsopphold/428ff23d-7a65-4c67-8059-6a1d07d287e3)
* performer.actor = Reference(https://fhir.npr.no/helsepersonell/1234567890)
* effectiveDateTime = "2024-05-28"
* dosage.text = "Svelge to spiseskjéer"
* dosage.route.coding[SCT].system = "http://snomed.info/sct"
* dosage.route.coding[SCT].code = #421521009
* dosage.route.coding[SCT].display = "Swallow"
* dosage.route.text = "oralt"
* dosage.dose.value = 2.0
* dosage.dose.unit = "metric tablespoon"
* dosage.dose.system = "http://unitsofmeasure.org"
* dosage.dose.code = #tsp_us
