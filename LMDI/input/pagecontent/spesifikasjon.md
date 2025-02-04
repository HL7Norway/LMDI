

### Etablering av integrasjon mot Legemiddelregisteret

**Hvitelisting av IP-adresse**

For å få tilgang til API-et for overføring av data kreves det at vi registrerer avsendersystemets IP-adressen i vår oversikt over hvitelistede adresser. Både enkeltadresser og adresseområder kan hvitelistes.


**Sertifikater**

Data som overføres til API-et skal være kryptert og signert (se [SignertKryptertBundle](SignertKryptertBundle.html)). Ved signering benyttes privat nøkkel i avsenders virksomhetssertifikat. Den offentlige delen av dette sertifikatet må sendes til Legemiddelregisteret. Ved kryptering av data benyttes offentlig nøkkel i Legemiddelregisterets virksomhetssertifikat. Dette kan lastes ned [her](nedlastinger.html)


**HelseId**

APIet er beskyttet av HelseID og krever at klienter autentiserer seg med Client Credentials Grant.

For å få tilgang:

1. Registrer klient i HelseID selvbetjeningsportal
2. Søk om tilgang til API-et fhi:lmr.fhirmottak med scope fhi:lmr.fhirmottak/all
3. Implementer OAuth 2.0 client credentials flow
4. Inkluder access token som Bearer token i Authorization-header for API-kall




### Overføring av data til Legemiddelregisteret

Institusjoner som skal overføre data til Legemiddelregisteret, må følge den definerte protokollen. Protokollen beskriver krav til overføringsfrekvens, datastruktur og sikkerhet. Du finner mer informasjon her: [Protokoll for overføring av data](protokoll.html).

2) Lag en LegemiddelregisterBundle
[LegemiddelregisterBundle](StructureDefinition-lmdi-bundle.html) er en spesialisert FHIR Bundle-profil utviklet for innsending av data til Legemiddelregisteret. Den er begrenset til batch-type bundles og tillater kun POST-operasjoner, noe som sikrer konsistent datahåndtering og sporbarhet. Bundlen kan kun inneholde spesifikke ressurstyper som er relevante for legemiddelregistrering: Pasient, Helsepersonell, Legemiddel, LegemiddelAdministrasjon, Diagnose, Institusjonsopphold, Legemiddelrekvirering, Organisasjon og Helsepersonellrolle. 

3) Når data overføres til Legemiddelregisteret, må dette skje via en `SignertKryptertBundle`, som sikrer både kryptering og signering av innholdet. Denne prosessen innebærer å komprimere, kryptere og signere en FHIR-basert `LegemiddelregisterBundle` før den sendes til API-et. Les mer om hvordan du oppretter en `SignertKryptertBundle` i [denne veiledningen](SignertKryptertBundle.html).


4) Send bundle via API
KryptertSignertBundle sendes til Legemiddelregisterets FHIR-mottak.
Responskoder
200 OK: LegemiddelregisterBundleResponse


5) Håndter respons fra API-et




