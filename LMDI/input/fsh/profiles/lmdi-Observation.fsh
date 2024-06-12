// Bør kunne bruke no-domain-VitalSigns direkte (eller hvordan det ender opp)
// alternativt internasjonal --> VitalSigns <---. 
// partOf = Reference(MedicationAdministration) ???

Profile: LmdiObservation
Parent: Observation
Id: lmdi-observation-tmp
Title: "Observasjon (kladd)"
Description: "Observation. Kommentar: For høyde og vekt skal denne baseres på nasjonal eller internasjonal Vital Signs IG når den foreligger. "
* ^status = #draft
* ^date = "2024-06-12"
* ^publisher = "Folkehelseinstituttet"

* status = #final
* status ^comment = "Kun endelige observasjoner skal være med."

* code.coding.system = "http://snomed.info/sct"
* code.coding.system ^comment = "SNOMED CT er brukt som eksempel, Vital Signs IG etc. vil åpne for andre kodeverk om nødvendig."

* valueQuantity MS
// constrains/MS under fra Vital Signs IG
// * valueQuantity.value 1..1 MS
// * valueQuantity.unit 1..1 MS
// * valueQuantity.system 1..1 MS
// * valueQuantity.code 1..1 MS
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