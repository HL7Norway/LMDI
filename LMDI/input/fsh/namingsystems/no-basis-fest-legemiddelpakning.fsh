// UNder utvikling i LMDI-prosjektet. 
// Mål: Være en del av no-basis. 
Instance: no-basis-fest-legemiddelpakning
InstanceOf: NamingSystem
Usage: #definition
* name = "festLegemiddelpakning"
* status = #draft
* kind = #identifier
* date = "2024-06-05"
* publisher = "Helsedirektoratet"
* responsible = "Direktoratet for medisinske produkter"
* description = "FEST-id for legemiddelpakninger"
* jurisdiction = urn:iso:std:iso:3166#NO "Norway"
* uniqueId[0].type = #uri
// Best om DMP/FEST/SAFEST har unike id/namespace som kan benyttes. 
// Volven har ikke noe, da FEST-id egentlig ikke er kodeverk, men katalog(database)-nøkler.
* uniqueId[=].value = "http://hl7.no/fhir/NamingSystem/festLegemiddelpakning"
* uniqueId[=].preferred = true
//* uniqueId[+].type = #oid
//* uniqueId[=].value = "2.16.578.1.12.4.1.4.102"
//* uniqueId[=].preferred = true
