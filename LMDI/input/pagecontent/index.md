# Legemiddeldata fra institusjon til Legemiddelregisteret (LMDI)

Komplette og oppdaterte helsedata på legemidler er tilgjengelig for analyse og forskning med tanke på å forbedre kvalitet, styring, helseovervåking, beredskap og kunnskapsforvaltning i helsetjenesten

## Mål

Samle inn legemiddeldata på individnivå fra polikliniske og innlagte pasienter i institusjon til Legemiddelregisteret (LMR). Som et ledd i dette utvikles det en implementasjonsguide (IG) basert på en felles informasjonsmodell og HL7 FHIR (dette dokumentet). Dette skal benyttes for innsending av data fra institusjon til LMR ved hjelp av datadeling (sikret REST API).

## Utvikling

- All koding av profiler skjer med [FHIR Shorthand](https://www.hl7.org/fhir/uv/shorthand/) (FSH)
- Dokumentasjon genereres med [IG Publisher](https://confluence.hl7.org/display/FHIR/IG+Publisher+Documentation)

I første omgang utvikles implementasjonsguiden for [FHIR R4](https://www.hl7.org/fhir/R4/), da dette er anbefalingen fra Helsedirektoratet og HL7 Norge. Tilrettelegging for R4B eller R5 må vurderes på et senere tidspunkt. 

## Samhandlingsarkitektur

Hovedmålet er datadeling ved hjelp av RESTful API i henhold til [HL7 FHIR sin spesifikasjon](https://hl7.org/fhir/R4/http.html), og etter [anbefaling fra Helsedirektoratet](https://www.ehelse.no/standardisering/standarder/anbefaling-om-bruk-av-hl7-fhir-for-datadeling). 

Inntil videre er profilene og implementasjonsguiden ([se siste build](https://hl7norway.github.io/LMDI/currentbuild/)) agnostiske til om det skal genereres dokumenter eller forskjellig mønster for REST API (f.eks. *reference* vs *logical id*). 

## Plan

Versjon 0.9 sommer 2024. 

## Status og historikk

- 2024-05-28: Versjon 0.5 klar for teknisk gjennomgang og kommentering fra torsdag 29.5.2025
- 2024-05-23: Versjon 0.2

## Kontaktpersoner

- Yngve Flater-Sandberg ([Vali](https://www.vali.no/))
- Line A. Sæle ([FHI](https://www.fhi.no/))
- [Espen Stranger Seland](https://github.com/rockphotog) ([Vali](https://www.vali.no/))


## TEST 2

<figure>
  {% include images/test.svg %}
  <figcaption>Test 2</figcaption>
</figure>


## TEST 4

<figure>
  {% include test.svg %}
  <figcaption>Test 4</figcaption>
</figure>




