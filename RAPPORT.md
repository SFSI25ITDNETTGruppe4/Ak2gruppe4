# Prosjektrapport – AK2

---

> **Merknad:** Dette dokumentet inneholder fullstendig rapporttekst klar til bruk i Word.
> Før endelig innlevering: legg inn skjermbilder der figurreferanser er markert, fyll inn dato/signaturer på forsiden, og gjør en siste språksjekk.

---

## Forord

Denne rapporten er en prosjektrapport knyttet til Arbeidskrav 2 i emnet Programmering ved Fagskolen Innlandet. Besvarelsen dokumenterer utvikling, implementasjon og testing av en Python-basert applikasjon for lager-, ordre- og fakturahåndtering, utført som en obligatorisk del av første studieår.

Bakgrunnen for arbeidet er et arbeidskrav der oppgaven var å utvikle en praktisk og funksjonell løsning som kombinerer Python, relasjonsdatabase, API-utvikling og grafisk brukergrensesnitt. Rapporten beskriver hvordan løsningen er satt opp, hvordan arbeidet er gjennomført, og hvilke praktiske erfaringer som er gjort underveis.

## Målgruppe

Målgruppe for denne rapporten er primært:

- Faglærer som skal vurdere besvarelsen
- Medstudenter i klassen

Rapporten kan også være nyttig for andre som ønsker et praktisk eksempel på hvordan Python-GUI, API og SQL-database kan kombineres i et helhetlig system.

## Forfattere og faglig bakgrunn

Rapporten er utarbeidet av:

- Even Alexander Vangberg Hansen, student ved Fagskolen Innlandet, utdanning i IT-drift og sikkerhet.
- Ram Singh Gill, student ved Fagskolen Innlandet, utdanning i IT-drift og sikkerhet.

Begge forfatterne har grunnleggende opplæring i programmering og databaser gjennom studiet, og prosjektet er gjennomført som en del av dette utdanningsløpet.

## Arbeidsprosess og gjennomføring

Arbeidet med prosjektet har pågått over flere uker i løpet av vårsemesteret 2026. Utviklingen ble gjennomført iterativt, med veksling mellom implementasjon, testing og feilretting. Arbeidet ble utført gjennom jevnlige arbeidsøkter flere ganger per uke, både individuelt og i samarbeid.

Gruppen har benyttet GitHub for versjonskontroll og samarbeid, med hyppige commits og tydelige commit-meldinger. Planlegging, avklaringer og statusoppdateringer har blitt gjennomført via Microsoft Teams. Arbeidsmetoden har vært preget av praktisk problemløsning, der funksjonskravene i oppgaven har styrt prioriteringene i utviklingsarbeidet.

## Takk

Vi ønsker å rette takk til faglærer ved Fagskolen Innlandet for veiledning og faglige avklaringer underveis i prosjektet. Videre takkes medstudenter for diskusjoner og nyttige erfaringsdelinger knyttet til både tekniske og metodiske utfordringer.

---

## Sammendrag

Prosjektet har hatt som mål å levere en Python-basert GUI-applikasjon som kommuniserer med en MySQL-database for lager- og ordrehåndtering. Oppgaven stilte krav til sikker SQL-bruk, inputvalidering, visning av varelager og ordrer, ordre-detaljvisning med moms og kundeinformasjon, kundehåndtering via stored procedures, og generering av faktura i PDF med unikt fakturanummer lagret i databasen.

Løsningen er gjennomført med Flask som API-lag, PyMySQL for databasekommunikasjon, Tkinter som GUI-rammeverk, samt GitHub Pages og Render for publisering av henholdsvis web-frontend og backend. En stored procedure (`sp_list_kunder`) er implementert og brukes aktivt for å hente kundelisten. Fakturagenerering er realisert via et dedikert API-endepunkt som genererer PDF og lagrer unikt fakturanummer i tabellen `faktura`.

Resultatet er en fungerende helhet der brukeren kan:

- Se varelager i GUI og i nettleser via API
- Se ordreliste og detaljer per ordre (inkludert varelinjer, pris, moms og kundeinformasjon med navn og adresse)
- Vise, legge til og slette kunder
- Generere faktura-PDF med unikt fakturanummer

Arbeidet har også inkludert feilretting i produksjonsmiljø, dokumentasjon av oppstart og drift, smoke-testing etter hver større endring, samt en sjekkliste før demo og innlevering.

Konklusjonen er at prosjektet i stor grad oppfyller funksjonskravene i oppgaven. Det som gjenstår er primært ytterligere kvalitetssikring av GUI-validering og sluttpolering av rapport og presentasjon.

---

## Innholdsfortegnelse

1. Innledning
   - 1.1 Problemstilling
2. Teori
   - 2.1 Database og SQL
   - 2.2 SQL-injection og sikkerhet
   - 2.3 Stored procedures
   - 2.4 API-teori
   - 2.5 GUI-teori
   - 2.6 Faktura og unik identifikator
3. Metode
   - 3.1 Arbeidsprosess
   - 3.2 Teknologistack
   - 3.3 Samarbeid og arbeidsflyt
   - 3.4 Arkitektur
   - 3.5 Datainnsamling
   - 3.6 Utvalg og testgrunnlag
   - 3.7 Begrensninger
   - 3.8 Kvalitets- og risikohåndtering
4. Resultat
   - 4.1 Leverte funksjoner
   - 4.2 API-endepunkter
   - 4.3 Produksjonsstatus
   - 4.4 Hovedfunn
   - 4.5 Oppfyllelse av oppgavekrav
   - 4.6 Dokumentasjon
5. Drøfting
   - 5.1 Vurdering av metodevalg
   - 5.2 Faglig vurdering av løsning
   - 5.3 Feil og læringspunkter
   - 5.4 Bransjerelevans og overføringsverdi
6. Konklusjon
   - 6.1 Svar på problemstillingen
   - 6.2 Viktigste funn

Referanseliste

Vedlegg

---

## 1 Innledning

Denne rapporten beskriver arbeidet med utvikling av en Python-basert applikasjon med grafisk brukergrensesnitt (GUI) som kobler seg til en database brukt for handel og lagerstyring. Problemstillingen tar utgangspunkt i hvordan en slik applikasjon kan utvikles for å håndtere varelager, ordrer, kunder og fakturering på en sikker og strukturert måte.

Rapporten er avgrenset til å omfatte funksjonaliteten som er spesifisert i arbeidskravet: bruk av SQL i Python, sikring mot SQL-injection, bruk av stored procedures, visning av data via både GUI og nettleser, samt generering av PDF-faktura med unikt fakturanummer.

Videre tar rapporten for seg hvordan arbeidskravet er løst i praksis, hva som har fungert godt, og hvilke utfordringer som har oppstått. Metodisk er arbeidskravet gjennomført iterativt, med fokus på planlegging, testing og feilretting. Rapporten er strukturert slik at den først presenterer problemstilling og relevant teori, deretter metode og teknologivalg, før resultatene drøftes og vurderes. Avslutningsvis oppsummeres erfaringer og lærepunkter fra arbeidet.

### 1.1 Problemstilling

Hvordan kan vi utvikle en robust Python-applikasjon med GUI som oppfyller kravene til lager- og ordrebehandling, samtidig som løsningen er sikker mot SQL-injection, bruker stored procedures, og er tilgjengelig både via GUI og nettleser?

---

## 2 Teori

### 2.1 Database og SQL

En relasjonsdatabase er brukt som datagrunnlag for varer, ordrer og kunder. SQL brukes til å hente, oppdatere og slette data. Korrekt datamodell og riktige joins er avgjørende for å hente fullstendige ordredata med kundeinformasjon, varelinjer og summer.

### 2.2 SQL-injection og sikkerhet

SQL-injection er en angrepsform der ondsinnet input kan manipulere SQL-spørringer og gi uautorisert tilgang til data. For å redusere denne risikoen brukes parametriserte spørringer i all ny kode. I stedet for å sette brukerinput direkte inn i SQL-strengen sendes verdiene som separate parametre til databasedriveren, slik at de aldri kan tolkes som SQL-kode.

### 2.3 Stored procedures

En stored procedure er en forhåndsdefinert SQL-rutine som er lagret og kjøres på databaseserveren. Dette gir bedre kapsling av logikk, reduserer datamengden som overføres og kan forbedre ytelse. I dette prosjektet brukes stored procedure `sp_list_kunder` for å hente kundelisten, i henhold til et eksplisitt krav i oppgaveteksten.

### 2.4 API-teori

Et REST-API (Application Programming Interface) er et grensesnitt som lar ulike applikasjoner kommunisere over HTTP. API-et i dette prosjektet er bygget med Flask og leverer data i JSON-format. HTTP-statuskoder brukes for å signalisere suksess og feil (200, 201, 400, 404, 409, 503). CORS (Cross-Origin Resource Sharing) er konfigurert for å tillate forespørsler fra godkjente frontend-domener.

### 2.5 GUI-teori

Et grafisk brukergrensesnitt (GUI) gjør det mulig for brukeren å interagere med applikasjonen uten å skrive kommandoer. Tkinter ble valgt som GUI-rammeverk fordi det er innebygd i Python og krever ingen ekstra installasjon, har lav oppstartsterskel og er godt dokumentert, gir tilstrekkelig funksjonalitet for oppgavens krav, og tillot gruppen å fokusere på funksjonalitet fremfor GUI-rammeverkets detaljer.

### 2.6 Faktura og unik identifikator

Fakturagenerering krever både dokumentproduksjon og datakonsistens. En PDF-faktura gir et standardisert format for kvittering og dokumentasjon. Unikt fakturanummer lagres i databasen for sporbarhet og for å hindre at samme ordre får duplikatnummer. Dette løses teknisk ved å kontrollere om et fakturanummer allerede finnes for en ordre, og enten gjenbruke det eksisterende eller opprette et nytt unikt nummer.

---

## 3 Metode

### 3.1 Arbeidsprosess

Prosjektet ble gjennomført i fire hovedfaser.

I den første fasen ble grunnmuren etablert ved oppsett av GitHub-repository med hensiktsmessig mappestruktur, databaseforbindelser og et grunnleggende API. Den andre fasen fokuserte på implementering av kjernefunksjonalitet, inkludert håndtering av varelager, ordrer og kunder. I den tredje fasen ble løsningen satt i produksjon: API-et ble publisert på Render som backend, mens frontend ble tilgjengeliggjort via GitHub Pages. Den siste fasen bestod av implementering av fakturagenerering i PDF-format, testing, hardening og dokumentasjon.

*[Figur: GitHub-repositoriet for prosjektarbeidet – sett inn skjermbilde]*

### 3.2 Teknologistack

Prosjektet benytter følgende teknologier:

- Python 3.11 og nyere versjoner
- Flask (web-rammeverk for API)
- PyMySQL (databasekobling)
- python-dotenv (miljøvariabler)
- flask-cors (CORS-håndtering)
- reportlab (PDF-generering)
- Tkinter (GUI)
- GitHub og GitHub Pages (versjonskontroll og frontend-hosting)
- Render (backend-hosting)
- AWS RDS (MySQL-database i skyen)

*[Figur: Illustrasjon av teknologistacken – sett inn diagram]*

### 3.3 Samarbeid og arbeidsflyt

Vi har samarbeidet asynkront gjennom hele prosjektet ved hjelp av Microsoft Teams og GitHub. Teams er brukt til planlegging, avklaringer og raske statusoppdateringer, mens GitHub har vært hovedplattform for kode, historikk og oppgaveflyt.

Arbeidsflyten har bestått av hyppige commits med tydelige commit-meldinger, pull/push-rutiner og løpende verifisering av endringer. Commitloggen har fungert som sporbar dokumentasjon på hva som er gjort, når det er gjort, og av hvem.

For oppgavestyring og fordeling av arbeid har gruppen brukt GitHub Projects, der oppgaver er flyttet mellom backlog, pågående arbeid og ferdigstilte aktiviteter.

*[Figur: GitHub Projects – sett inn skjermbilde av kanban-tavlen]*

Lenker brukt i prosjektet:

- GitHub repository: https://github.com/SFSI25ITDNETTGruppe4/Ak2gruppe4
- GitHub Pages: https://sfsi25itdnettgruppe4.github.io/Ak2gruppe4/
- Render API (backend): https://ak2gruppe4.onrender.com

### 3.4 Arkitektur

Systemet er bygget opp med en lagdelt arkitektur som skiller mellom brukergrensesnitt, backend og database. Applikasjonen består av både et Python-basert GUI og en nettleserløsning, som begge benytter det samme API-et for datatilgang.

GUI-et er utviklet i Python med Tkinter og fungerer som klient mot et REST-API bygget i Flask. All forretningslogikk, validering av inndata og sikker databasekommunikasjon håndteres i backend. Dette inkluderer bruk av parametriserte SQL-spørringer for å beskytte mot SQL-injection og stored procedure for uthenting av kundedata.

Databasen inneholder all informasjon om varer, kunder, ordrer og fakturaer, og sørger for at fakturanummer er unike. Den nettleserbaserte løsningen henter varelagerdata via API-et og gjør det mulig å vise lagerstatus i en nettleser. Denne arkitekturen muliggjør gjenbruk av funksjonalitet på tvers av klienter og gir en fleksibel og oversiktlig løsning.

### 3.5 Datainnsamling

Datagrunnlaget i prosjektet er den eksisterende varehusdatabasen som ble levert som en del av oppgaven. Databasen inneholder tabeller for varer (`Produkt`), kunder (`Kunde`), ordrer (`Ordre`) og ordrelinjer (`OrdreDetaljer`). Data er hentet via SQL-spørringer og stored procedure, og presentert i GUI og via API uten å endre det underliggende datagrunnlaget. For testformål har vi benyttet de eksisterende radene i databasen, og verifisert at visning, beregninger og operasjoner gir korrekte resultater basert på disse dataene.

### 3.6 Utvalg og testgrunnlag

Utvalget i prosjektet har bestått av de dataene som allerede finnes i den tilgjengelige varehusdatabasen, inkludert varer, kunder og ordrer. Testing er gjennomført ved å bruke disse dataene i både GUI, API og nettleserløsningen, med fokus på å verifisere korrekt datavisning, beregninger og databaseoperasjoner. Dette gir et tilstrekkelig grunnlag for å vurdere om løsningen fungerer etter hensikten innenfor rammene av prosjektet.

### 3.7 Begrensninger

Prosjektet har enkelte begrensninger knyttet til tid, omfang og testmetodikk. Testing er gjennomført manuelt og som smoke-test, og dekker ikke alle tenkelige feilsituasjoner eller randtilfeller. Løsningen er avhengig av den eksisterende databasestrukturen og tilgjengelige testdata, noe som begrenser fleksibiliteten i enkelte funksjoner. Utviklingsarbeidet har hatt fokus på å oppfylle funksjonskravene i oppgaven, fremfor visuell utforming og fullstendig automatisert testing.

### 3.8 Kvalitets- og risikohåndtering

**Identifiserte risikoer:**

Prosjektet har hatt flere mulige risikoer knyttet til både tekniske og organisatoriske forhold. En sentral risiko var kompleksiteten i samspillet mellom GUI, API og database, der feil i én komponent kunne påvirke hele løsningen. Det var også risiko knyttet til databaseoperasjoner, spesielt med tanke på SQL-injection, feilaktig håndtering av inndata og generering av unike fakturanumre. Gruppearbeidet innebar videre en risiko for skjev arbeidsfordeling og tidsutfordringer. Det lå i tillegg en risiko for at sensitiv informasjon, som databasetilkoblingsdetaljer, utilsiktet kunne bli lagret i versjonskontroll.

**Tiltak:**

For å redusere teknisk risiko ble løsningen bygget med tydelig separasjon mellom klient, backend og database, slik at feil lettere kunne identifiseres og isoleres. Parametriserte SQL-spørringer og validering av brukerinput ble tatt i bruk for å øke sikkerheten. Bruk av stored procedure bidro til mer kontrollert databaseaksess. Organisatoriske risikoer ble håndtert gjennom regelmessig kommunikasjon og bruk av GitHub Projects for oppgavefordeling. `.gitignore` ble brukt til å utelate sensitive filer fra versjonskontroll, og miljøvariabler via `.env`-fil ble brukt for å holde tilkoblingsdetaljer utenfor koden.

---

## 4 Resultat

Dette kapittelet viser resultatene av arbeidet med utvikling og implementasjon av den Python-baserte applikasjonen. Resultatene beskrives med utgangspunkt i funksjonalitet som er ferdigstilt og verifisert gjennom testing av GUI, API og database.

### 4.1 Leverte funksjoner

Prosjektet har resultert i en fungerende applikasjon for håndtering av varelager, ordrer, kunder og fakturering.

**Varelager:** Løsningen gir oversikt over varelageret med varenummer, betegnelse, antall og pris. Varelageret er tilgjengelig både i det Python-baserte GUI-et og via nettleser gjennom API-et.

**Ordrer og detaljer:** Applikasjonen kan vise alle registrerte ordrer. Brukeren kan velge en bestemt ordre og se tilhørende kundeinformasjon (navn og adresse), ordrelinjer med varer og antall, pris per vare, pris multiplisert med antall per linje, totalbeløp, og totalbeløp inkludert merverdiavgift (MVA).

**Kundehåndtering:** Kundelisten hentes via stored procedure `sp_list_kunder`. Kunder kan legges til og slettes fra GUI-et. Ved sletting kontrolleres det om kunden har tilknyttede ordrer, slik at databasen ikke settes i en ugyldig tilstand.

**Faktura:** Det er implementert funksjonalitet for generering av faktura i PDF-format med unikt fakturanummer. Fakturanummeret lagres i databasen og samme ordre kan ikke få to ulike fakturanumre.

*[Figur: Skjermbilde av varelageret i GUI – sett inn bilde]*

*[Figur: Skjermbilde av varelager i nettleser via GitHub Pages – sett inn bilde]*

### 4.2 API-endepunkter

Som en del av løsningen er det utviklet et REST-API som fungerer som bindeledd mellom klientene og databasen. API-et leverer data i JSON-format og brukes av det Python-baserte GUI-et og av frontend-nettsiden.

Implementerte endepunkter:

| Endepunkt | Metode | Beskrivelse |
|---|---|---|
| `/api/varelager` | GET | Henter full vareliste |
| `/api/ordrer` | GET | Henter alle ordrer |
| `/api/ordrer/<ordreNr>` | GET | Henter detaljer for én ordre inkludert kundeinformasjon og linjer |
| `/api/kunder` | GET | Henter alle kunder via stored procedure |
| `/api/kunder` | POST | Legger til ny kunde |
| `/api/kunder/<KNr>` | DELETE | Sletter kunde |
| `/api/ordrer/<ordreNr>/faktura` | POST | Genererer PDF-faktura og lagrer fakturanummer |
| `/health/db` | GET | Sjekker at databaseforbindelsen er aktiv |

### 4.3 Produksjonsstatus

Løsningen er publisert og i drift per innleveringstidspunkt:

- **Backend (Render):** https://ak2gruppe4.onrender.com – Flask-API kjører i produksjonsmiljø med miljøvariabler for databasetilkobling.
- **Frontend (GitHub Pages):** https://sfsi25itdnettgruppe4.github.io/Ak2gruppe4/ – Nettbasert visning av varelager og ordrer, verifisert live.
- **Database (AWS RDS):** MySQL-database tilgjengelig fra Render-backend. Stored procedure og faktura-tabell er opprettet og i bruk.
- **GUI:** Kjøres lokalt, kobler seg mot live Render-backend. Testet og verifisert på Windows 11 med Python 3.13.

Løsningen er merket som **Release 1 (v1.0.0)** og tilgjengelig som GitHub Release.

### 4.4 Hovedfunn

Følgende ble bekreftet gjennom smoke-testing og manuell verifisering:

- Alle kjerne-API-endepunkter svarte med HTTP 200 og forventet data
- GUI startet uten feil og viste korrekte data fra live database
- Stored procedure `sp_list_kunder` ble kalt korrekt og returnerte kundelisten
- Fakturagenerering produserte gyldig PDF og lagret fakturanummer i `faktura`-tabellen
- Nettleserfrontend på GitHub Pages viste oppdaterte varelagerdata via API
- SQL-injection-sikring ble verifisert ved at alle databasekall bruker parametriserte spørringer

### 4.5 Oppfyllelse av oppgavekrav

Tabellen nedenfor viser direkte kobling mellom hvert krav i oppgaveteksten og løsningen som er implementert:

| Krav fra oppgaven | Løsning | Filer |
|---|---|---|
| GUI koblet til database via Python | Tkinter GUI + Flask API + MySQL | `gui.py`, `app.py` |
| Sikring mot SQL-injection | Parametriserte SQL-spørringer | `app.py` |
| Validering av inndata | Kontroll av felt, lengde og postnummer | `app.py` |
| Robusthet mot utilsiktede stopp | Try/except i API, statusmeldinger i GUI | `app.py`, `gui.py` |
| Varelager i GUI (VNr, navn, antall, pris) | Tabelvisning i GUI | `gui.py` |
| Varelager via API i nettleser | GitHub Pages frontend mot Render API | `docs/app.js`, `GET /api/varelager` |
| Liste alle ordrer | Eget GUI-fane og API-endepunkt | `gui.py`, `GET /api/ordrer` |
| Detaljer per ordre (varer, antall, pris, pris×antall, kunde m/adresse, total inkl. moms) | Detaljvisning med alle felter | `gui.py`, `GET /api/ordrer/<ordreNr>` |
| Faktura-PDF med unikt fakturanummer lagret i DB | PDF-generering, kontroll mot `faktura`-tabell | `app.py`, `POST /api/ordrer/<ordreNr>/faktura` |
| Kunder via Stored Procedure | `sp_list_kunder` kalt fra backend | `app.py`, `GET /api/kunder` |
| Legge til og slette kunder | POST/DELETE + GUI-handlinger | `app.py`, `gui.py` |

### 4.6 Dokumentasjon

I tillegg til kildekoden er prosjektet dokumentert med følgende filer i repoet:

- `README.md` – oppsett, drift og oversikt
- `KRAVMATRISE.md` – krav koblet mot løsning
- `CHECKLISTE.md` – testbevis og status
- `PROJECT_STATUS_LOG.md` – overleveringsstatus
- `API.md` – API-referanse

Fullstendig logg og versjonshistorikk finnes på GitHub: https://github.com/SFSI25ITDNETTGruppe4/Ak2gruppe4

---

## 5 Drøfting

### 5.1 Vurdering av metodevalg

Metode- og teknologivalgene i prosjektet er gjort med utgangspunkt i oppgavens kriterier, tilgjengelig tid og gruppens forkunnskaper. Det ble valgt å benytte et REST-API som mellomlag mellom klient og database, noe som ga en tydelig separasjon av ansvar og gjorde løsningen enklere å teste, vedlikeholde og bygge videre på. Flask ble brukt som API-rammeverk fordi det er enkelt, oversiktlig og godt egnet for prosjekter med klare funksjonskrav.

Tkinter ble valgt som GUI-rammeverk på grunn av lav oppstartsterskel og enkel integrasjon mot backend-løsningen. Dette gjorde det mulig å fokusere på funksjonalitet fremfor GUI-teknologiens detaljer.

**Fordeler:**

- Iterativ utvikling ga rask fremdrift og løpende mulighet til å justere kurs
- Små og hyppige commits ga god sporbarhet i Git-historikken
- Tidlig produksjonssetting avdekket realistiske feil som ikke vises i lokalt miljø

**Ulemper:**

- En del feil oppstod sent i deploy-fasen, noe som krevde ekstra tid til feilretting
- Noe dokumentasjon ble skrevet etter den intensive kodefasen, og ikke parallelt

### 5.2 Faglig vurdering av løsning

Løsningen demonstrerer god kobling mellom databasedesign, API-lag og GUI. Valg av Tkinter var pragmatisk og egnet for kravnivået. Bruk av parametriserte SQL-kall og inputvalidering forbedrer sikkerhet og robusthet.

Vurdert opp mot oppgaveteksten oppfyller prosjektet de viktigste funksjonskravene. Løsningen dekker dataflyt mellom GUI, API og database, og håndterer varelager, ordrer, kunder og faktura på en strukturert måte. Vi har i tillegg utfordret oss til å lære GitHub, tredjepartsløsninger som Render og skyinfrastruktur via AWS RDS. Det at dette ble en fungerende del av leveransen, er vi svært fornøyde med.

### 5.3 Feil og læringspunkter

Det største arbeidet underveis har vært å få dataflyten stabil mellom GUI, API og database, samtidig som brukeropplevelsen ble ryddigere. Blant annet ble popup-dialoger byttet ut med en mer diskret statuslinje, og tabellvisningen ble justert for bedre søk, sortering og oppdatering. Det ble gjort flere runder med feilretting og hardening for å sikre at løsningen oppfører seg stabilt både lokalt og mot den publiserte backend-tjenesten.

Et konkret læringspunkt var bruken av smoke-testing som arbeidsmetode. En smoke test er en rask kontroll av de viktigste funksjonene i løsningen – i praksis at applikasjonen starter, at sentrale API-endepunkter svarer korrekt, og at GUI-et åpner uten feil. Målet er ikke å teste absolutt alt, men å bekrefte at kjerneløsningen er stabil nok til videre bruk og demonstrasjon. Vi gjennomførte smoke-test etter hver større endring som en del av arbeidsrutinen, og dette fanget opp feil tidlig og ga trygghet for at løsningen fungerte som forventet.

Et annet viktig læringspunkt var håndteringen av miljøvariabler og hemmeligheter. Tidlig i prosjektet risikerte vi å legge databasepassord i kildekoden. Vi lærte å bruke `.env`-fil og `.gitignore` for å holde sensitiv informasjon utenfor versjonskontroll.

### 5.4 Bransjerelevans og overføringsverdi

Prosjektet etterligner en realistisk mini-produksjonsflyt med API, skyhosting, database, klientgrensesnitt og dokumentasjon. De tekniske løsningene og arbeidsmetodene som er brukt – versjonskontroll, iterativ utvikling, REST-API, produksjonssetting og testing – er direkte relevante for web- og systemutvikling i praksis.

---

## 6 Konklusjon

### 6.1 Svar på problemstillingen

Prosjektet viser at det er mulig å utvikle en robust Python-basert lager- og ordreapp med GUI, API og database som oppfyller kravene i oppgaven. Løsningen er sikret mot SQL-injection, benytter stored procedure for kundedata, og er tilgjengelig både via GUI og nettleser. Vi fikk også jobbet med en realistisk arbeidsmetodikk og prosjektstruktur, noe som ga god oversikt over hvor innsatsen skulle legges.

### 6.2 Viktigste funn

- API- og GUI-funksjonalitet er implementert i henhold til krav
- Stored procedure-kravet er oppfylt med `sp_list_kunder`
- Faktura-PDF med unikt fakturanummer lagres i databasen
- Løsningen er tilgjengelig både via GUI og nettleser
- Smoke-testing etter endringer var et effektivt kvalitetsgrep
- Bruk av skyinfrastruktur (Render + AWS RDS + GitHub Pages) ga en realistisk produksjonsopplevelse

---

## Referanseliste

Bootstrap. (u.å.). *Bootstrap – The most popular HTML, CSS, and JS library in the world*. Hentet 24.03.2026 fra https://getbootstrap.com/

Flask. (2026). *Welcome to Flask*. https://flask.palletsprojects.com/

MySQL Tutorial. (2026). *Python MySQL*. https://www.mysqltutorial.org/python-mysql/

MySQL Tutorial. (2026). *MySQL Stored Procedures*. https://www.mysqltutorial.org/mysql-stored-procedure-tutorial.aspx

MySQL Tutorial. (2026). *Calling MySQL stored procedures in Python*. https://www.mysqltutorial.org/calling-mysql-stored-procedures-python/

Real Python. (2026). *Prevent Python SQL Injection*. https://realpython.com/prevent-python-sql-injection/

Python Software Foundation. (2026). *tkinter — Python interface to Tcl/Tk*. https://docs.python.org/3/library/tkinter.html

Amazon Web Services. (2026). *Amazon RDS*. https://aws.amazon.com/rds/

GitHub. (2026). *GitHub Foundations Learning Path*. https://learn.microsoft.com/en-us/training/paths/github-foundations/

---

## Vedlegg

### Vedlegg A: Nettbasert frontend

Frontend (GitHub Pages):
https://sfsi25itdnettgruppe4.github.io/Ak2gruppe4/

### Vedlegg B: Backend / API

- **Backend API (Render):** REST-basert API for lager-, ordre- og kundedata  
  https://ak2gruppe4.onrender.com/
- **API helsesjekk:** Verifisering av databaseforbindelse og API-status  
  https://ak2gruppe4.onrender.com/health/db

### Vedlegg C: Kildekode og versjonskontroll

- **GitHub repository:** Kildekode for GUI, API og frontend  
  https://github.com/SFSI25ITDNETTGruppe4/Ak2gruppe4

---

> **Merknad for endelig innlevering:**
> - Fyll inn dato, navn og signaturer på forsiden
> - Legg inn skjermbilder der figurreferanser er markert i teksten
> - Sjekk alle APA-kildehenvisninger
> - Gjør en siste språksjekk og korting ned til 12–18 sider
