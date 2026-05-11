# Rapportseksjon: Knytting mellom oppgavekrav og løsning

Nedenfor er en ferdig formulert del som kan brukes i rapporten for å vise tydelig hvordan prosjektet oppfyller kravene i oppgaveteksten.

## Oppfyllelse av oppgavekrav

Prosjektet er utviklet for å oppfylle de funksjonelle og tekniske kravene i arbeidskravet. Løsningen består av et Python-basert GUI, et Flask-basert API, og en MySQL-database. I tillegg er det laget en nettbasert frontend via GitHub Pages, slik at varelagerdata også kan vises i en nettleser, slik oppgaven krever.

### GUI koblet til database via Python
GUI-et er utviklet i Tkinter og fungerer som klient mot API-et. Dette gjør at brukergrensesnittet kan vise data fra databasen på en oversiktlig måte, samtidig som all databasekommunikasjon skjer kontrollert via backend. GUI-et viser varelager, ordrer, kundeliste og ordre-detaljer, og har i tillegg støtte for fakturagenerering og lagring av PDF.

### Sikring mot SQL-injection og robusthet
For å redusere risikoen for SQL-injection brukes parametriserte SQL-spørringer i backend. Brukerinput valideres før innsetting i databasen, blant annet ved kontroll av obligatoriske felt og postnummerformat. I tillegg er feilhåndtering lagt inn både i backend og GUI, slik at løsningen ikke stopper opp ved vanlige feil. Feilmeldinger presenteres via statusfelt i GUI-et i stedet for blokkérende popup-dialoger.

### Varelager i GUI og nettleser
Et sentralt krav i oppgaven er at varelageret skal vises både i Python-programmet og via API i nettleseren. Dette er løst ved at GUI-et henter og viser varelageret i en tabell, mens samme data også er tilgjengelig gjennom et REST-endepunkt som brukes av frontenden på GitHub Pages. Dermed gjenbrukes samme dataflyt i to ulike klienter.

### Ordreliste og ordredetaljer
Applikasjonen kan vise alle ordrer som ligger i databasen. Brukeren kan også velge en spesifikk ordre og se tilhørende kundeinformasjon, ordredetaljer, varelinjer, pris per vare, linjesummer og totalbeløp inkludert merverdiavgift. Dette er implementert både i backend og GUI, slik at løsningen dekker hele arbeidsflyten fra oversikt til detaljvisning.

### Fakturagenerering med unikt fakturanummer
Oppgaven krever at det skal genereres faktura i PDF-format, og at fakturanummeret skal være unikt og lagres i databasen. Dette er løst ved at backend oppretter eller gjenbruker et fakturanummer per ordre, lagrer det i tabellen faktura og genererer en PDF-faktura med moms og ordredetaljer. GUI-et lar brukeren velge ordre og lagre fakturaen lokalt som PDF.

### Kunder via Stored Procedures
Kundelisten er implementert i henhold til kravet om Stored Procedures. I backend kalles prosedyren sp_list_kunder for å hente kundedata fra databasen. I tillegg kan brukeren legge til og slette kunder via GUI-et. Ved sletting sjekkes det om kunden har tilknyttede ordrer, slik at databasen ikke blir satt i en ugyldig tilstand.

## Knytting til kode og bevis

Følgende filer og funksjoner viser direkte hvordan kravene er løst:

- [app.py](app.py): REST-API, databasekobling, parametriserte spørringer, stored procedure, fakturagenerering
- [gui.py](gui.py): Tkinter-GUI, visning av varelager, ordrer, kunder og faktura-flyt
- [docs/app.js](docs/app.js): Nettleserbasert visning av varelager og ordrer via API
- [CHECKLISTE.md](CHECKLISTE.md): Testbevis og status for kravene
- [KRAVMATRISE.md](KRAVMATRISE.md): Kompakt oversikt over hvert krav og hvor det er løst
- [PROJECT_STATUS_LOG.md](PROJECT_STATUS_LOG.md): Overleveringsstatus og verifiserte endepunkter

## Test og verifisering

Prosjektet er testet med en egen smoke-test mot sentrale endepunkter. Følgende ble verifisert 2026-05-07:

- `/health/db` svarte med HTTP 200 og `ok=True`
- `/api/varelager` svarte med HTTP 200 og `ok=True`
- `/api/ordrer` svarte med HTTP 200 og `ok=True`
- `/api/kunder` svarte med HTTP 200 og `ok=True`
- `gui.py` besto syntakskontroll
- GUI-et startet uten traceback

Dette gir et tydelig bevis på at kjerneløsningen fungerer i praksis.

## Kort vurdering av måloppnåelse

Vurdert opp mot oppgaveteksten oppfyller prosjektet i stor grad de viktigste funksjonskravene. Løsningen dekker dataflyt mellom GUI, API og database, og håndterer varelager, ordrer, kunder og faktura på en strukturert måte. Det som i hovedsak gjenstår er sluttføring av rapporttekst, full presentasjonsøving og eventuell siste manuelle kontroll av enkelte GUI-flyter før endelig innlevering.
