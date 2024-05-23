Profile:     LmdiPatient
Id:          lmdi-patient-profile
Parent:      Patient
Title:       "LMDI Patient Profile"
Description: "Kun et eksempel for å vise verktøy"
* ^status = #draft
* ^date = "2024-05-23"

// Krav til profil:
// Skal baseres på no-basis-patient

// Eksempler under inntil videre
// Require at least one value inside the `name` element
* name 1..*

// Mark elements as MustSupport
* name and name.given and name.family MS

// Do not allow `gender` to be included.
* gender 0..0
