# Prosjektplan AK2

## 1. Mal
Levere en fungerende Python-app med GUI og databasekobling som oppfyller kravene i oppgaven, samt rapport og presentasjon.

## 2. Omfang (krav som ma leveres)
- GUI-app i Python koblet til database
- SQL i Python, inkl. bruk av Stored Procedures
- Sikring mot SQL injection
- Validering av inndata
- Feilhandtering som hindrer krasj
- Vise varelager (varenummer, navn, antall, pris)
- Vise varelager via API i nettleser
- Liste alle ordrer
- Vise detaljer for valgt ordre
- Generere faktura (PDF) med unikt fakturanummer lagret i databasen
- Vise kunder (via Stored Procedures)
- Legge til og fjerne kunder
- Rapport (12-18 sider), presentasjon, gruppelogg, individuell refleksjon

## 3. Foreslatt gjennomforing (4 sprinter)

### Sprint 1: Oppsett og grunnmur
- Avklare rollefordeling i gruppa
- Klargjore GitHub-flyt (pull -> add -> commit -> push)
- Sette opp prosjektstruktur (gui, db, api, rapport)
- Lage databasekobling og test mot databasen
- Lage enkel GUI-startside

Leveranse sprint 1:
- Programmet starter
- DB-tilkobling fungerer
- Teamet bruker samme Git-rutine

### Sprint 2: Kjernefunksjoner i app
- Implementere visning av varelager i GUI
- Implementere liste over ordrer
- Implementere ordredetaljer for valgt ordre
- Legge inn validering pa inndata
- Parametriserte SQL-sporringer for anti-injection

Leveranse sprint 2:
- Bruker kan se varer, ordre og ordredetaljer
- Input-validering og trygg SQL er pa plass

### Sprint 3: API, kunder og faktura
- Lage API-endepunkt for varelager
- Vise API-data i nettleser
- Implementere kunder med Stored Procedures
- Legge til/fjerne kunder
- Lage PDF-faktura med moms og unikt fakturanummer

Leveranse sprint 3:
- API fungerer i nettleser
- Kundeoperasjoner fungerer
- Faktura kan genereres og lagres riktig

### Sprint 4: Kvalitet, rapport og presentasjon
- Feiltesting og stabilisering
- Teste alle krav systematisk med sjekkliste
- Skrive ferdig rapport med begrunnelser og utfordringer
- Lage presentasjon (maks 30 min)
- Samle gruppeloggen fra commit-historikk + korte notater

Leveranse sprint 4:
- Alt kravstoff demonstrerbart
- Rapport og presentasjon klare

## 4. Rolleforslag i gruppa
- Backend/DB-ansvarlig: SQL, Stored Procedures, datamodell
- GUI-ansvarlig: skjermbilder, brukerflyt, validering
- API-ansvarlig: endepunkt, JSON, nettleservisning
- Dokumentasjonsansvarlig: rapport, presentasjon, gruppelogg

Merk: Alle skal bidra i kode og commits. Rollene er hovedansvar, ikke silo.

## 5. Arbeidsflyt i Git/GitHub
- Start alltid med: git pull
- Etter arbeid: git status -> git add . -> git commit -m "..." -> git push
- Sma commits ofte, med tydelige meldinger
- Commit-loggen brukes som grunnlag for gruppeloggen

## 6. Definisjon av ferdig (Definition of Done)
En funksjon regnes som ferdig nar:
- Den virker i appen
- Den er testet av minst ett annet gruppemedlem
- Feilhandtering er lagt til
- Eventuelle SQL-kall er sikre og validerte
- Endringen er committed og pushet med tydelig melding

## 7. Risiko og tiltak
- Risiko: Merge-konflikter
  - Tiltak: Pull ofte, korte brancher, sma commits
- Risiko: Uklare ansvarsforhold
  - Tiltak: Fast ukemote med oppdatert oppgaveliste
- Risiko: Tidsklemme mot slutten
  - Tiltak: Prioriter must-have krav forst, nice-to-have etterpa
- Risiko: Feil i DB/API sent i lopet
  - Tiltak: Integrasjonsteste fra sprint 2, ikke vente til slutt

## 8. Ukentlig rytme (anbefalt)
- 1 planmote (30-45 min)
- 2 arbeidsokter med konkret mal for hver okt
- 1 kort demo internt i gruppa av hva som er gjort


