Profile: Legemiddel
Parent:   Medication
Id:       lmdi-legemiddel
Title:    "Legemiddel"
Description: "Beskrivelse av legemiddel."
* ^status = #draft
* ^date = "2024-05-30"

// Se basis-profiler og evt. eResept/PLL
// MedicationKnowledge under utvikling, se R5 for status
// Krav: Legemiddel-id (identifier), må mulig settes av FHI
* identifier MS
* identifier ^short = "Legemiddelets identifikasjon"
* identifier ^definition = "Legemiddelets identifikasjon i henhold til TODO"
// Krav: Kode, som FEST-id, SNOMED-CT etc., obligatorisk
// Opprette NamingSystem for FEST #12 <- issue
// Slicing? Hva kan LMR ta i mot? Hvilket nivå skal man rapportere på? Hva med "ukurrante" legemidler? 
* code 1..1
// * code.system = etc. 
// Krav: Legemiddelform, obligatorisk? HL7 Form vs FEST-form. IDMP/SAFEST?
* form MS
* form ^short = "Legemiddelform"
// Krav: Ingredienser/virkestoff navn (ingredienth) // Bør finnes indirekte for de flest
// Krav: Styrke (ingredient.strength[x]) // Bør finnes indirekte for de fleste
// Krav: Batchnummer
* batch MS
* batch ^short = "Batch-nummer for legemiddelet"
// Krav: Merkevarenavn, handelsnavn
// Krav: Definerte døgnsoder (DDD) <- bør refereres til

// EKSEMPLER

Instance: Medisin-1
InstanceOf: Legemiddel
Description: "Eksempel på legemiddel"
* identifier.system = "http://ehelse.no/fhir/CodeSystem/FEST/LegemiddelMerkevare"
* identifier.value = "ID_9e6c620b-5d09-4f27-9ee1-b108e7f338ab"
* code.coding.system = "http://snomed.info/sct"
* code.coding = #430127000
* code.coding.display = "Oxycodone-containing product in oral dose form"
* code.text = "Oxycodone"

Instance: Medisin-2
InstanceOf: Legemiddel
Description: "Eksempel på legemiddel - Paracetamol - UTKAST"
* identifier.system = "http://ehelse.no/fhir/CodeSystem/FEST/LegemiddelMerkevare"
* identifier.value = "ID_2ABAC272-0BCF-43F0-84BE-984074D92E15"
* code.text = "Paracetamol"
