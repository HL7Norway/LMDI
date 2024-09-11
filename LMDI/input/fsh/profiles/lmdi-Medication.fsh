Profile: Legemiddel
Parent:   Medication
Id:       lmdi-legemiddel
Title:    "Legemiddel"
Description: "Beskrivelse av legemiddel."
* ^status = #draft
* ^date = "2024-06-26"
* ^publisher = "Folkehelseinstituttet"

* code 1..1
* code.coding ^slicing.discriminator.type = #pattern
* code.coding ^slicing.discriminator.path = "system"
* code.coding ^slicing.rules = #open
* code.coding contains FD 0..1 
    and FM 0..1
    and FP 0..1
    and FV 0..1
* code.coding[FD].system = "http://dmp.no/fhir/NamingSystem/festLegemiddelDose"
* code.coding[FM].system = "http://dmp.no/fhir/NamingSystem/festLegemiddelMerkevare"
* code.coding[FP].system = "http://dmp.no/fhir/NamingSystem/festLegemiddelPakning"
* code.coding[FV].system = "http://dmp.no/fhir/NamingSystem/festLegemiddelVirkestoff"
* code.coding[FD] ^short = "FEST-id for legemiddel DOSE"
* code.coding[FM] ^short = "FEST-id for legemiddel MERKEVARE"
* code.coding[FP] ^short = "FEST-id for legemiddel PAKNING"
* code.coding[FV] ^short = "FEST-id for legemiddel VIRKESTOFF"
* code.coding[FD] ^comment = "URI for NamingSystem er midlertidig, må normeres som en del av no-basis."
* code.coding[FM] ^comment = "URI for NamingSystem er midlertidig, må normeres som en del av no-basis."
* code.coding[FP] ^comment = "URI for NamingSystem er midlertidig, må normeres som en del av no-basis."
* code.coding[FV] ^comment = "URI for NamingSystem er midlertidig, må normeres som en del av no-basis."

* form MS
* form ^short = "Legemiddelform"
* form.coding 1..*
* form.coding.system 1..1
* form.coding.code 1..1
* form.coding.display MS
* form.coding ^slicing.discriminator.type = #pattern
* form.coding ^slicing.discriminator.path = "system"
* form.coding ^slicing.rules = #closed
* form.coding contains 7448 0..1 and SCT 0..1
* form.coding 1..* 
* form.coding ^short = "Legemiddelform"
* form.coding ^comment = "Kodet legemiddelform. Inntil videre begrenset til Legemiddelform (7448) og kodesetteksempel basert på SNOMED CT fra HL7."
* form.coding[7448] ^short = "Kodeverk Legemiddelform (7448) fra FEST/eResept"
* form.coding[SCT] ^short = "SNOMED CT Form Codes"
* form.coding[7448].system = "urn:oid:2.16.578.1.12.4.1.1.7448" 
* form.coding[SCT].system = "http://snomed.info/sct" 

// Krav: Ingredienser/virkestoff navn (ingredienth) // Bør finnes indirekte for de flest
// Krav: Styrke (ingredient.strength[x]) // Bør finnes indirekte for de fleste

* batch MS
* batch ^short = "Batch-nummer for legemiddelet"

// EKSEMPLER

Instance: Medisin-1-LegemiddelDose-Oxycodone
InstanceOf: Legemiddel
Description: "Eksempel på legemiddel"
// "Oxycodone Orifarm mikst oppl 1 mg/ml"
* identifier.system = "http://dmp.no/fhir/NamingSystem/festLegemiddelDose"
* identifier.value = "ID_48BD33D2-2838-4B81-8225-02391B7A4516"
* code.coding.system = "http://snomed.info/sct"
* code.coding = #414984009
* code.coding.display = "Product containing oxycodone (medicinal product)"
* code.text = "Oxycodone"

Instance: Medisin-2-Paracetamol
InstanceOf: Legemiddel
Description: "Eksempel på legemiddel - Paracetamol - UTKAST"
* identifier.system = "http://dmp.no/fhir/NamingSystem/festLegemiddelMerkevare"
* identifier.value = "ID_2ABAC272-0BCF-43F0-84BE-984074D92E15"
* code.text = "Paracetamol"

Instance: Medisin-3-LegemiddelPakning-Monoket
InstanceOf: Legemiddel
Description: "Eksempel på legemiddel - paking"
* identifier.system = "http://dmp.no/fhir/NamingSystem/festLegemiddelPakning"
* identifier.value = "ID_0003602E-315E-4CDE-9EB0-6756BE9CD120"
* code.text = "Monoket OD SySk depotkaps, hard 50 mg"
