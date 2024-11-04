Profile: Legemiddeladministrasjon
Parent:   MedicationAdministration
Id:       lmdi-legemiddeladministrasjon
Title:    "Legemiddeladministrasjon"
Description: """Beskriver administrasjon av legemiddel til pasient på institusjon.

Dette er kjerneressursen for denne implementasjonsguiden. Den peker videre legemiddelet som ble gitt, pasienten som har fått administrert legemiddel, på hvilken institusjon det skjedde, tidspunkt for administrering, hvem som utførte (helsepersonell eller rolle ved institusjon) og dose med eventuell administrasjonsvei."""
* ^status = #draft
* ^date = "2024-06-24"
* ^publisher = "Folkehelseinstituttet"

* status from LegemiddeladministreringStatus
* status ^short = "Status administrering."
* status ^definition = "Status administrering. Skal vanligvis settes til 'Gjennomført' (completed), men 'Feilregistrert' (entered-in-error) MÅ benyttes hvis registreringen inneholder en alvorlig feil og skal slettes. "

* medication[x] ^short = "Legemiddeladministrasjon."

* subject only Reference(Patient)
* subject ^short = "Referanse til pasient"
* subject ^definition = "Det skal alltid være en referanse til pasienten som har blitt administrert legemiddel."

* context MS
* context only Reference(EpisodeOfCare)
* context ^short = "Referanse til aktuelt institusjonsopphold"
* context ^definition = "Referanse til hvilket institusjonsopphold eller avtale pasienten var på da legemiddelet ble administrert."
* context ^comment = "Encounter må vurderes om nødvendig, f.eks. hos spesialist."

* effective[x] ^short = "Tidspunkt eller periode for administrasjon"

* performer and performer.actor MS
* performer.actor only Reference (Practitioner) or Reference (PractitionerRole)
* performer.actor ^short = "Hvem som har administrert legemiddelet"
* performer.actor ^definition = "Utfører av administrering kan være helsepersonell eller en rolle knyttet til institusjonen eller pasienten. "
* performer.actor ^comment = "TODO #21 Tolkning: Det viktigste er helsepersonellets rolle ved institusjonen, og ikke selve helsepersonellet?"

* request MS
* request ^short = "Referanse til rekvisisjon"
* request ^definition = "Referanse til rekvisisjonen som denne administreringen er basert på (som for eksempel resept eller ordinering."

* dosage.route MS
* dosage.route ^short = "Administrasjonsvei"
* dosage.route ^definition = "Administrasjonsvei. Er begrenset til foreslått koding fra SNOMED CT-verdisettet til HL7 og Volven-kodeverket Administrasjonsvei (OID=7477) fra eResept. "
* dosage.route ^comment = "TODO #22 Diskuter om det bør være 0..1 hvis man ikke har registret administrasjonsvei."
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

* dosage.dose 1..1
* dosage.dose ^short = "Administrert mengde virkestoff"
* dosage.dose ^definition = "Mengde (dosering) av legemiddelets primære virkestoff."

* dosage.rateRatio MS

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
InstanceOf: Legemiddeladministrasjon
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

Instance: Administrering-2-Infusjon
InstanceOf: Legemiddeladministrasjon
Description: "Eksempel på administrering av legemiddel - infusjon"
* status = #completed
* medicationReference = Reference(https://fhir.legemidler.example.com/legemidler/0987654321)
* subject = Reference(https://fhi.no/fhir/lmdi/pasient/12345678)
* context = Reference(https://fhi.no/fhir/lmdi/institusjonsopphold/428ff23d-7a65-4c67-8059-6a1d07d287e3)
* performer.actor = Reference(https://fhir.npr.no/helsepersonell/1234567890)
* effectivePeriod.start = "2024-06-13T14:26:01+02:00"
* effectivePeriod.end = "2024-06-13T14:48:47+02:00"
* dosage.text = "4,5g D5W 250 ml. IV hver 6. time. Infuser over 30 minutter ved 8 ml/min"
* dosage.route.coding[SCT].system = "http://snomed.info/sct"
* dosage.route.coding[SCT].code = #47625008
* dosage.route.coding[SCT].display = "Intravenous route (qualifier value)"
* dosage.route.text = "Intravenøst"
* dosage.dose.value = 4500
* dosage.dose.unit = "mg"
* dosage.dose.system = "http://unitsofmeasure.org"
* dosage.dose.code = #mg
* dosage.rateRatio.numerator.value = 8.0
* dosage.rateRatio.numerator.system = "http://unitsofmeasure.org"
* dosage.rateRatio.numerator.code = #ml
* dosage.rateRatio.denominator.value = 1
* dosage.rateRatio.denominator.system = "http://unitsofmeasure.org"
* dosage.rateRatio.denominator.code = #min