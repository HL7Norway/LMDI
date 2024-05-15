Profile:     LmdiPatient
Id:          lmdi-patient-profile
Parent:      Patient
Title:       "LMDI Patient Profile"
Description: "Kun et eksempel for å vise verktøy"
// The `Title` keyword defines the human-readable title on the profile's page in the built
// Implementation Guide. This is also visible in on the Artifacts page and in the Table of Contents
// in the built Implementation Guide.
//
// The `Description` keyword defines a short summary of the profile that appears at the top of the
// profile page under "Definition" and on the Artifacts page in the built Implementation Guide.
//
// Note that FSH files do not typically have extra white space between rules, but due to the large
// number of comments in this example, extra white space is included for better readability.

// ----- Begin rules:

// Require at least one value inside the `name` element
* name 1..*

// Mark elements as MustSupport
* name and name.given and name.family MS

// Do not allow `gender` to be included.
* gender 0..0
