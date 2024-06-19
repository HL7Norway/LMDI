### Oppgaver, åpne saker og videre arbeid

Oppgaver og videre arbeid.

Det finnes en liste med åpne saker under [åpne saker på GitHub](https://github.com/HL7Norway/LMDI/issues). De viktigste for videre diskusjon og arbeid er gjengitt på denne siden.

#### Arbeidsgruppemøte 21.6.24

Temaer:

- Identifisering av legemidler (FEST, SAFEST/IDMP/SNOMED CT etc. ), id vs. avansert
- Administrasjonsvei - kardinalitet og kodeverk
- Diagnose - opphold/behandling, resept/ordinering
- Organisasjonsnivå/enheter

#### Diskuter om det bør være 0..1 hvis man ikke har registret administrasjonsvei. - 22

Forslag er kun MS (must support) og 0..1.

[Sak og diskusjon på GitHub](https://github.com/HL7Norway/LMDI/issues/22)

#### Verdisett administrasjonsvei (MedicationAdministration) - 18

- Volven: Administrasjonsvei (OID=7477) - fra eResept
- SNOMED CT https://www.hl7.org/fhir/R4/valueset-route-codes.html (HL7)
- Andre?
- Låser til SNOMED CT-verdisettet til HL7 inntil videre.
- Finnes ikke en offisiell mapping mellom 7477 og SCT.

[Sak og diskusjon på GitHub](https://github.com/HL7Norway/LMDI/issues/18)

#### Legemiddel - Pris - 28

Hvilke muligheter har LMR for å hente inn denne?

[Sak og diskusjon på GitHub](https://github.com/HL7Norway/LMDI/issues/28)

#### Organisasjon / Lokasjon - 27

- Kan enhet som ansvarlig for administrasjon være forskjellig fra enhet som har administrativt/behandlings-ansvar for pasienten?
- Hvilket nivå på enhet skal rapporteres?
- Antall nivå vil være naturlig å ta med i rapportering?
- Få rett rapportering av Kommunenr
- Er kommunenummer på institusjon overflødig?

[Sak og diskusjon på GitHub](https://github.com/HL7Norway/LMDI/issues/27)

#### Legemiddel (kur), m/ flere virkestoff - 26

Ved rapportering av kur (f.eks fra CMS i HSØ) angis flere virkestoff / ATC administrert til samme tidspunkt. Behov for å støtte en slik struktur i legemiddel.

[Sak og diskusjon på GitHub](https://github.com/HL7Norway/LMDI/issues/26)

#### Støtte for rapportering av ÅrsakTilBytte mangler - 33

Det er et generelt åpent spørsmål om hvor mye fra rekvisisjon (resept, ordinasjon) som kan eller må være med, evt som passer i en fase to. Se også sak 32 under. 

[Sak og diskusjon på GitHub](https://github.com/HL7Norway/LMDI/issues/33)

#### Støtte for rapportering av MedicationRequest (som ikke enda er administrert el.) - 32

Det nevnes behov for å kunne ta i mot data om MedicationRequest, før de er administrert.
Støtter modellen denne type use-case?

[Sak og diskusjon på GitHub](https://github.com/HL7Norway/LMDI/issues/32)

#### Krav: Diagnose (utskrivningsdiagnose) (referanse). Sjekke om dette faktisk skal/bør være med - 15

- Mulig utskrivningsdiagnose ikke er fastsatt underveis i oppholdet / ved administrering? Når skal data sendes?
- Det oversendes ingen informasjon før det er skjedd en administrasjon, og det finnes komplette data rundt.
- Hva med utskrivningsdiagnose - er data tilgjengelig? Kan det hentes fra andre registre?
- Skal denne flyttes fra opphold til forskrivning?

[Sak og diskusjon på GitHub](https://github.com/HL7Norway/LMDI/issues/15)

#### Observasjon.Laboratorieverdier - hvilke typer er aktuelle? - 16

(Fra informasjonsmodellen)

[Sak og diskusjon på GitHub](https://github.com/HL7Norway/LMDI/issues/16)




[Sak og diskusjon på GitHub]()


---

{% include footer.md %}

