Profile: LmdiObservation
Parent: Observation
Id: lmdi-observation-tmp
Title: "Observasjon (kladd)"
Description: "Observation"
* ^status = #draft
* ^date = "2024-06-06"
* ^publisher = "Folkehelseinstituttet"
// Krav: Vekt etc. 
// Bør kunne bruke no-domain-VitalSigns direkte (eller hvordan det ender opp)
// alternativt internasjonal --> VitalSigns <---. 
// Peker på subject = patient
// partOf = Reference(MedicationAdministration) ???
// Foreslår at status = final, dvs. man sender kun "endelige" målinger
* status = #final
// SNOMED CT <- Eksempel
* code.coding.system = "http://snomed.info/sct"
* valueQuantity MS
* valueQuantity.system = "http://unitsofmeasure.org"

// EKSEMPLER
// Vekt
Instance: Observasjon-1-Kroppsvekt
InstanceOf: LmdiObservation
Description: "Eksempel på observasjon - kroppsvekt"
* status = #final
* code.coding.system = "http://snomed.info/sct"
* code.coding.code = #27113001
* code.coding.display = "kroppsvekt"
* valueQuantity.value = 99.0
* valueQuantity.unit = "kg"
* valueQuantity.system = "http://unitsofmeasure.org"
* valueQuantity.code = #kg

// Høyde
Instance: Observasjon-2-Hoyde
InstanceOf: LmdiObservation
Description: "Eksempel på observasjon - høyde"
* status = #final
* code.coding.system = "http://snomed.info/sct"
* code.coding.code = #1153637007
* code.coding.display = "kropphøyde"
* valueQuantity.value = 187.5
* valueQuantity.unit = "cm"
* valueQuantity.system = "http://unitsofmeasure.org"
* valueQuantity.code = #cm


// TODO #16 Observasjon.Laboratorieverdier - hvilke typer er aktuelle?