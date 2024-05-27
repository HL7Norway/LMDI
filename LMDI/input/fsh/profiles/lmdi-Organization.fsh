Profile: LmdiOrganization
Parent: Organization
Id: lmdi-organization
Title: "Organisasjon"
Description: "TODO #4"
* ^status = #draft
* ^date = "2024-05-23"

// Krav (nasjonalt): Basere på no-basis-Organization
// Krav: Organisasjons-ID som ENH eller RESH (identifier)
* identifier 1..* 
* identifier ^short = "Unik identifikasjon av behandlingsenhet / avdeling / intitusjon"

// Krav: Type organisasjon / organisatorisk nivå / betegnelse
* type MS
* type ^short = "Organisatorisk nivå / betegnelse"

// Krav: Navn (name)
* name MS
* name ^short = "Navn på organisasjonsenhet"
* name ^definition = "Eks. avdelingsnavn / institsjonsnavn / org navn"

// Krav: Kommune (.district.extension:municipalitycode, fra no-basis)
// TODO #8 Utvide Organisasjon med utvidelse for kommunenummer fra no-basis
* address MS

// Krav: Del av organisasjon (ref:organization)
// * partOf MS <- NB! kan bare peke oppover