Profile: Helsepersonell
Id: lmdi-practitioner
Parent: Practitioner
Title: "Helsepersonell"
Description: """
Profil for å dokumentere helsepersonell som har foreskrevet eller administrert legemidler i Norge. 

Profilen er basert på den norske basisprofilen NoBasisPractitioner, men er begrenset til kun å inkludere:
- Helsepersonellnummer som unik identifikator

I denne profilen er personopplysninger som navn, kontaktinformasjon, fødselsdato og kjønn eksplisitt utelatt. Dette er gjort for å begrense behandling av personopplysninger til det som er nødvendig for formålet.

Profilen brukes i sammenheng med legemiddeladministrering og -rekvirering, der det er behov for å dokumentere hvilket helsepersonell som har vært involvert.
"""

* ^status = #draft
* ^date = "2024-06-12"
* ^publisher = "Folkehelseinstituttet"
* ^version = "0.1.0"
* ^experimental = true

// HPR-nummer
* identifier 1..1
* identifier ^short = "Helsepersonellnummer for helsepersonellet"
* identifier ^definition = "Helsepersonellnummer er en unik identifikator fra Helsepersonellregisteret som tildeles alt autorisert helsepersonell i Norge."
* identifier ^comment = """
Helsepersonellnummer er påkrevet i denne profilen og skal alltid oppgis. 
Andre identifikatorer som FNR/DNR støttes ikke i denne profilen da den er begrenset til kun autorisert helsepersonell med helsepersonellnummer."""

* identifier.system 1..1
* identifier.system = "urn:oid:2.16.578.1.12.4.1.4.4"
* identifier.system ^short = "Identifikatortype: Helsepersonellnummer"
* identifier.system ^definition = "URN OID for helsepersonellnummer (2.16.578.1.12.4.1.4.4) som identifiserer at dette er et nummer fra det norske Helsepersonellregisteret."
* identifier.system ^comment = "Skal være helsepersonellnummer (2.16.578.1.12.4.1.4.4)"

* identifier.value 1..1 
* identifier.value ^short = "Selve helsepersonellnummeret"
* identifier.value ^definition = """
Det faktiske helsepersonellnummeret som er tildelt helsepersonellet. 
Dette er et unikt nummer som tildeles ved autorisasjon."""
* identifier.value ^comment = "Helsepersonellnummer er et heltall"

// Spesialitet
// * qualification ^short = "Spesialitet"
// * qualification.code.coding.system 1..1
// * qualification.code.coding.system = "urn:oid:2.16.578.1.12.4.1.1.7426"
// * qualification.code.coding.system ^short = "Helsepersonellregisterets (HPR) klassifikasjon av spesialiteter (OID=7426)"
// * qualification.code.coding.system ^definition = "Dette kodeverket inneholder koder for spesialiteter i Helsepersonellregisteret. Kilde: Forskrift om spesialistgodkjenning av helsepersonell og turnusstillinger for leger."
// * qualification.code.coding.system ^comment = "MVP - satt til HPR-spesialieter (OID=7426)."

// Deaktiverte elementer
* text 0..0
* name 0..0
* telecom 0..0
* address 0..0
* gender 0..0
* birthDate 0..0
* photo 0..0
* qualification 0..0
* communication 0..0

Instance: Helsepersonell-1-HPR-nummer
InstanceOf: Helsepersonell
Description: "Eksempel på helsepersonell med HPR-nummer"
* identifier.system = "urn:oid:2.16.578.1.12.4.1.4.4"
* identifier.value = "9144900"