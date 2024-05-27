Profile: Legemiddel
Parent:   Medication
Id:       lmdi-legemiddel
Title:    "Legemiddel"
Description: "Beskrivelse av legemiddel."
* ^status = #draft
* ^date = "2024-05-27"

// Se basis-profiler og evt. eResept/PLL
// MedicationKnowledge under utvikling, se R5 for status
// Krav: Legemiddel-id (identifier), må mulig settes av FHI
* identifier MS
* identifier ^short = "Legemiddelets identifikasjon"
* identifier ^definition = "Legemiddelets identifikasjon i henhold til TODO"
// Krav: Kode, som FEST-id, SNOMED-CT etc., obligatorisk
* code 1..1
// Krav: Legemiddelform, obligatorisk? HL7 Form vs FEST-form. IDMP/SAFEST?
* form MS
* form ^short = "Legemiddelform"
// Krav: Ingredienser/virkestoff navn (ingredienth)
// Krav: Styrke (ingredient.strength[x])
// Krav: Batchnummer
* batch MS
* batch ^short = "Batch-nummer for legemiddelet"
// Krav: Merkevarenavn, handelsnavn
// Krav: Definerte døgnsoder (DDD) <- bør refereres til

Instance: Medisin-1
InstanceOf: Legemiddel
Description: "Eksempel på legemiddel"
* identifier.value = "FEST-XXX-9e6c620b-5d09-4f27-9ee1-b108e7f338ab"
* code.coding.system = "http://snomed.info/sct"
* code.coding = #430127000
* code.coding.display = "Oral Form Oxycodone (product)"
* code.text = "Oxycodone"