# Prosjektlogg og overlevering

Sist oppdatert: 2026-04-26
Repo: SFSI25ITDNETTGruppe4/Ak2gruppe4
Branch: main

## 1) Kort status nå

- Backend på Render er live: https://ak2gruppe4.onrender.com
- Databasekobling er verifisert i produksjon (health/db = ok true).
- Følgende API-endepunkter er verifisert live:
  - /api/varelager (ok true, count 161)
  - /api/ordrer (ok true, count 300)
  - /api/ordrer/<ordreNr> (ok true, testet med 22696, linjer 3)
  - /api/kunder (ok true, count 512)
- Stored procedure sp_list_kunder er opprettet i RDS og brukes av /api/kunder.
- Tkinter GUI er lagt til og kan brukes mot lokal eller produksjons-API.

## 2) Hva som er gjort (tidslinje)

Nylige commits på main:

- 5e457fe Fix SQL alias for order details endpoint
- f5a66a2 Fiks DB-config fallback og fjern hardkodet credential-spor
- 95edeb6 Legg til Tkinter GUI med alle tabs
- 07f28a3 Legg til API-dokumentasjon
- 73acb24 Implementer ordredetaljer og kund-API endepunkter
- 6d7551b Test: Legg til index.html i rot for GitHub Pages
- e7f68ab Legg til .nojekyll for å deaktivere Jekyll processing
- 01ec844 Sett frontend API-URL til live Render backend
- 0acf8e7 Sett opp GitHub Pages frontend og Render backend med CORS
- 17c5479 Implementer varelager- og ordreliste via API og nettvisning

## 3) Funksjonalitet som finnes nå

Backend i app.py:

- GET /api/varelager
- GET /api/ordrer
- GET /api/ordrer/<ordreNr> med:
  - kundeinformasjon
  - ordrelinjer
  - totaler med moms
- GET /api/kunder via stored procedure
- POST /api/kunder
- DELETE /api/kunder/<KNr>
- GET /health/db

Database:

- Stored procedure sp_list_kunder er opprettet
- Skjema er tilpasset reelle tabeller:
  - kunde med Fornavn, Etternavn, Adresse, PostNr
  - ordrelinje-tabell: ordrelinje
  - poststed-join for by

GUI i gui.py:

- Varelager-visning
- Ordre-liste
- Ordredetaljer-vindu
- Kunde-liste
- Legg til kunde
- Slett kunde
- API-statusvisning

## 4) Sikkerhet og konfigurasjon

Gjort:

- Hardkodet passord er fjernet fra aktiv kode.
- DB-konfig i app.py støtter både:
  - DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
  - HOST, USER, PASSWORD, DATABASE (fallback)

Viktig:

- Ikke legg passord i kode eller README.
- Bruk kun miljøvariabler i Render.
- Roter DB-passord hvis dere mistenker at noe har vært eksponert tidligere.

## 5) Kjent arbeidsstatus for frontend-hosting

- GitHub Pages har tidligere gitt 404 i denne sessionen.
- Backend er uansett oppe og verifisert.
- Frontend kan testes via lokal fil/GUI eller videre feilsøkes på Pages når ønskelig.

## 6) Hvordan plukke opp arbeidet raskt

1. Les API.md for kontrakter på endepunkter.
2. Kjør lokal backend:
   - python app.py
3. Kjør GUI:
   - python gui.py
4. Sett API_BASE_URL i gui.py til:
   - http://localhost:5000 for lokal testing
   - https://ak2gruppe4.onrender.com for produksjon
5. Verifiser raskt med:
   - /health/db
   - /api/varelager
   - /api/ordrer
   - /api/ordrer/<gyldigOrdreNr>
   - /api/kunder

## 7) Hva som gjenstår mot oppgavetekst

Høy prioritet:

- PDF-faktura med unikt fakturanummer lagret i database
- Strammere inputvalidering i GUI og API (utover dagens nivå)
- Testskript eller enkel testplan som dokumenterer funksjonene

Middels prioritet:

- Ferdigstille og stabilisere frontend i nettleser (GitHub Pages eller alternativ)
- Forbedre feilbeskjeder/brukerflyt i GUI

Lav prioritet:

- UI-polish i GUI
- Mer dokumentasjon i rapportformat

## 8) Praktiske notater til gruppa

- Service er live og DB fungerer nå i produksjon.
- Hvis produksjon plutselig feiler igjen, sjekk først:
  - Render Environment variabler
  - RDS Security Group port 3306
  - RDS status i AWS (available)
- For overlevering bør denne loggen oppdateres med dato ved hver større endring.
