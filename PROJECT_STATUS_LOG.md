# Prosjektlogg og overlevering

Sist oppdatert: 2026-05-11
Repo: SFSI25ITDNETTGruppe4/Ak2gruppe4
Branch: main

## 1) Kort status nå

- Løsningen er nå publisert som **Release 1 (v1.0.0)**.
- Backend på Render er live: https://ak2gruppe4.onrender.com
- Frontend på GitHub Pages er live: https://sfsi25itdnettgruppe4.github.io/Ak2gruppe4/
- Databasekobling er verifisert i produksjon (health/db = ok true).
- Følgende API-endepunkter er verifisert live:
  - /api/varelager
  - /api/ordrer
  - /api/ordrer/<ordreNr>
  - /api/kunder
  - /health/db
- Faktura-endepunkt er implementert og tilgjengelig i produksjon:
  - POST /api/ordrer/<ordreNr>/faktura
  - Genererer PDF
  - Lagrer unikt fakturanummer i tabell `faktura`

## 2) Hva som er gjort (tidslinje)

Nylige commits på main:

- a52ea1e Arkiver sprint 1 TODO som historisk plan
- 960fd5b Lenke kravmatrise fra README
- 6efa6e1 Oppdater sjekkliste med verifisert status og bevis
- a5f8eaa Legg til kravmatrise med sporbarhet mot oppgavetekst
- 53a2560 Marker release 1 og videre versjonsstrategi
- 05ef0f2 Robust API-håndtering og enklere sikkerhetsgrep
- e1bef6b Rett feil i sortering og kunder-tabell
- 90608ae Klikk-sortering på kolonneoverskrifter
- d06740e Live søk/filter i alle tabeller
- 955d619 Zebra-striper i alle tabeller
- 4252db5 Aktiv tab-markering i navbar
- 02c98b3 Mørk header-bar med appnavn og gruppenavn

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

- Fullføre siste manuelle GUI-tester for kundesletting og fakturaflyt
- Fullføre presentasjonstest og ferdigstille rapporttekst

Middels prioritet:

- Legge inn skjermbilder og bevis i presentasjon/rapport
- Kortfatte og språkvaske rapportens siste versjon

Lav prioritet:

- Små forbedringer i GUI-tekst og mikroflyt dersom tid gjenstår

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
- Prosjektet er nå merket som Release 1 (v1.0.0), og videre arbeid håndteres som patcher, bugfixes og nye features.
