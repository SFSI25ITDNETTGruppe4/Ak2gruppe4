# Prosjektlogg og overlevering

Sist oppdatert: 2026-04-26
Repo: SFSI25ITDNETTGruppe4/Ak2gruppe4
Branch: main

## 1) Kort status nå

- Backend på Render er live: https://ak2gruppe4.onrender.com
- Frontend på GitHub Pages er live: https://sfsi25itdnettgruppe4.github.io/Ak2gruppe4/
- Databasekobling er verifisert i produksjon (health/db = ok true).
- Følgende API-endepunkter er verifisert live:
  - /api/varelager
  - /api/ordrer
  - /api/ordrer/<ordreNr>
  - /api/kunder
  - /health/db
- Faktura-endepunkt er implementert:
  - POST /api/ordrer/<ordreNr>/faktura
  - Genererer PDF
  - Lagrer unikt fakturanummer i tabell `faktura`

## 2) Hva som er gjort (tidslinje)

Nylige commits på main:

- 3841641 Fiks Pages build ved å fjerne ugyldig submodule-gitlink
- 84b2067 Implementer faktura-PDF med unikt fakturanummer i database
- dc137c9 Legg til prosjektlogg for overlevering og oppstart
- 5e457fe Fix SQL alias for order details endpoint
- f5a66a2 Fiks DB-config fallback og fjern hardkodet credential-spor
- 95edeb6 Legg til Tkinter GUI med alle tabs
- 07f28a3 Legg til API-dokumentasjon
- 73acb24 Implementer ordredetaljer og kund-API endepunkter

## 3) Funksjonalitet som finnes nå

Backend i app.py:

- GET /api/varelager
- GET /api/ordrer
- GET /api/ordrer/<ordreNr> med kunde, ordrelinjer og totaler (inkl. mva)
- GET /api/kunder via stored procedure
- POST /api/kunder
- DELETE /api/kunder/<KNr>
- GET /health/db
- POST /api/ordrer/<ordreNr>/faktura

Database:

- Stored procedure `sp_list_kunder` er opprettet
- Tabell `faktura` er lagt til for fakturanummer og summer
- SQL-kall i API bruker parametre (ikke string-konkatenasjon)

GUI i gui.py:

- Varelager-visning
- Ordre-liste
- Ordredetaljer-vindu
- Kunde-liste
- Legg til/slett kunde
- API-statusvisning
- Generer og lagre faktura-PDF for valgt ordre

## 4) Sikkerhet og konfigurasjon

- Hardkodet passord er fjernet fra aktiv kode.
- DB-konfig i app.py støtter både:
  - DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
  - HOST, USER, PASSWORD, DATABASE (fallback)
- Ikke legg passord i kode eller README.
- Bruk miljøvariabler i Render.

## 5) Frontend-hosting status

- GitHub Pages var tidligere nede pga. feilet Pages-build.
- Feilårsak: ugyldig submodule-gitlink `Ak2gruppe4` i git-indeks.
- Dette er rettet i commit `3841641`.
- Ny Pages-build ble kjørt og fullført med success.

## 6) Hva som gjenstår mot oppgavetekst

Høy prioritet:

- Strammere inputvalidering i GUI (for eksempel samme regler som API for postnummer/navn)
- Testskript eller enkel testplan som dokumenterer funksjonene

Middels prioritet:

- Forbedre feilmeldinger og brukerflyt i GUI
- Legge inn tydelig visning av fakturanummer etter fakturagenerering

Lav prioritet:

- UI-polish i GUI
- Mer dokumentasjon i rapportformat

## 7) Board/backlog status

- Følgende er markert complete/done og closed:
  - #1
  - #6
  - #9
  - #10
  - #11
  - #12
  - #13
  - #14
  - #20
  - #24
  - #25
- Backlog-kolonnen er ryddet for de oppgavene som ble ferdigstilt i denne økten.

## 8) Rapportnotat (kan brukes direkte i sluttrapport)

- Krav om faktura er implementert med servergenerert PDF og unik nøkkel i DB.
- Løsningen er idempotent per ordre: finnes faktura fra før, gjenbrukes samme fakturanummer.
- GitHub Pages er konfigurert på `main` + `/docs` og verifisert live etter build-fiks.
- API + GUI + Pages er nå koblet mot live backend på Render.
