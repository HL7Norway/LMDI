Profile: LmdiObservation
Parent: Observation
Id: lmdi-observation-tmp
Title: "Observation TMP (Kun et eksempel med kroppsvekt)"
Description: "Observation"
* ^status = #draft
* ^date = "2024-06-06"
* ^publisher = "Folkehelseinstituttet"
// Krav: Vekt etc. 
// Bør kunne bruke no-domain-VitalSigns direkte (eller hvordan det ender opp)
// alternativt internasjonal VitalSigns. 
// Peker på subject = patient
// partOf = Reference(MedicationAdministration) ???
// Foreslår at status = final, dvs. man sender kun "endelige" målinger
* status = #final
// SNOMED CT <- Eksempel
* code.coding.system = "http://snomed.info/sct"
* valueQuantity MS
* valueQuantity.system = "http://unitsofmeasure.org"

// EKSEMPLER

Instance: Observasjon-1
InstanceOf: LmdiObservation
* status = #final
* code.coding.system = "http://snomed.info/sct"
* code.coding.code = #27113001
* code.coding.display = "kroppsvekt"
* valueQuantity.value = 99.0
* valueQuantity.unit = "kg"
* valueQuantity.system = "http://unitsofmeasure.org"
* valueQuantity.code = #kg