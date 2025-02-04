Profile: LegemiddelregisterBundle
Parent: Bundle
Id: lmdi-bundle
Title: "LegemiddelregisterBundle"
Description: "Profil av Bundle for Legemiddelregisteret. Støtter bare batch-type og POST-operasjoner, med begrensninger på tillatte ressurstyper."

* type = #batch (exactly)
* type MS
* entry MS
* entry.request MS
* entry.request.method = #POST (exactly)
* entry.request.method MS
* entry.resource MS

* type ^short = "Må være av type batch"
* type ^definition = "Angir at bunten må være av type batch"

* entry.request.method ^short = "Må være POST"
* entry.request.method ^definition = "Angir at alle forespørsler i bunten må være av type POST"

* obeys lr-allowed-resources

// Invariant som sjekker at bare tillatte ressurstyper er inkludert
Invariant: lr-allowed-resources
Description: "Bundle kan bare inneholde følgende ressurstyper: Pasient, Helsepersonell, Legemiddel, LegemiddelAdministrasjon, Diagnose, Institusjonsopphold, Legemiddelrekvirering, Organisasjon, Helsepersonellrolle"
Severity: #error
Expression: "entry.all(
  resource.conformsTo('Pasient') or 
  resource.conformsTo('Helsepersonell') or 
  resource.conformsTo('Legemiddel') or 
  resource.conformsTo('LegemiddelAdministrasjon') or 
  resource.conformsTo('Diagnose') or 
  resource.conformsTo('Institusjonsopphold') or 
  resource.conformsTo('Legemiddelrekvirering') or 
  resource.conformsTo('Organisasjon') or 
  resource.conformsTo('Helsepersonellrolle')
)"

Instance: LegemiddelregisterBundle-1
InstanceOf: LegemiddelregisterBundle
Usage: #example
Title: "Eksempel på LegemiddelregisterBundle med administreringer"
Description: "Eksempel på en batch-bundle som inneholder to legemiddeladministreringer"
* type = #batch

// Pasient
* entry[0].resource = Pasient-20
* entry[0].request.method = #POST
* entry[0].request.url = "Patient"

// Legemiddel
* entry[1].resource = Medisin-10
* entry[1].request.method = #POST
* entry[1].request.url = "Medication"

// Helsepersonell
* entry[2].resource = Helsepersonell-10
* entry[2].request.method = #POST
* entry[2].request.url = "Practitioner"

// Helsepersonellrolle
* entry[3].resource = RolleHelsepersonell-10
* entry[3].request.method = #POST
* entry[3].request.url = "PractitionerRole"

// Institusjonsopphold
* entry[4].resource = Institusjonsopphold-2-Sykehjem
* entry[4].request.method = #POST
* entry[4].request.url = "EpisodeOfCare"

// Organisasjon
* entry[5].resource = Organisasjon-2-Eldrehjem
* entry[5].request.method = #POST
* entry[5].request.url = "Organization"

// Legemiddeladministrasjon
* entry[6].resource = Administrering-10
* entry[6].request.method = #POST
* entry[6].request.url = "MedicationAdministration"