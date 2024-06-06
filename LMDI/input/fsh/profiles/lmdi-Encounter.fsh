// Institusjonsopphold basert på Encounter
// Encounter passer bedre for selve hendelsen/timen der legemiddeladministrering skjer,
// men sistnevnte er en "encounter" i seg selv. 
// Encounter kan passe for spesialisthelsetjenesten, men EpisodeOfCare bør også fungere der. 

Profile: LmdiEncounterInstitusjonsopphold
Parent: Encounter
Id: lmdi-encounter-institusjonsopphold
Title: "På vei ut (Institusjonsopphold A)"
Description: "Beskrivelse av pasientens opphold i institusjon - bruker Encounter (Mulig bruke denne for spesialisthelsetjenesten)"
* ^status = #draft
* ^experimental = true
* ^date = "2024-06-06"
* ^publisher = "Folkehelseinstituttet"

// Krav: identifier ESS: Finnes ingen nasjonal business-identifier for Encounter
// Krav: actualPeriod
* period MS
* period ^short = "Periode for pasientens opphold i institusjon." 