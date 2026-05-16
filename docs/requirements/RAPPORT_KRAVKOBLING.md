# Rapport: Oppfyllelse av krav og valgt løsning

Denne delen er skrevet for å kunne brukes direkte i sluttrapporten. Teksten forklarer hva som er laget, hvorfor løsningene er valgt, og hvordan prosjektet oppfyller kravene i oppgaveteksten.

## Innledning

Prosjektet er utviklet som en helhetlig løsning med Python-basert GUI, Flask-basert API og MySQL-database i bunn. I tillegg er det laget en nettleserfrontend via GitHub Pages, slik at sentrale data også kan vises utenfor desktop-applikasjonen. Målet har vært å dekke kravene i oppgaven med en løsning som er funksjonell, robust og enkel å demonstrere.

## Valg av teknologi

Tkinter er brukt til GUI-et fordi det gir en enkel og stabil måte å bygge et desktopgrensesnitt i ren Python. Flask er valgt til API-laget fordi det passer godt til en lettvekts REST-løsning og gjør det tydelig hvor data hentes, valideres og returneres. MySQL er brukt som databasesystem fordi oppgaven krever varig lagring av data, og fordi løsningen allerede er knyttet mot en strukturert relasjonsdatabase. GitHub Pages er brukt for den nettbaserte frontenden, slik at samme data også kan presenteres i en nettleser.

## Oppfyllelse av oppgavekrav

### GUI koblet til database via Python

GUI-et er laget i Tkinter og fungerer som klient mot API-et. Det betyr at brukergrensesnittet kan vise data fra databasen på en ryddig måte, samtidig som all databasekommunikasjon går kontrollert gjennom backend. GUI-et viser varelager, ordrer, kunder og ordredetaljer, og har i tillegg støtte for fakturagenerering og lagring av PDF.

### Sikring mot SQL-injection og bedre robusthet

For å redusere risikoen for SQL-injection brukes parametriserte SQL-spørringer i backend. Brukerinput valideres før data sendes videre til databasen, blant annet ved kontroll av obligatoriske felt og postnummerformat. Feilhåndtering er lagt inn både i backend og GUI, slik at vanlige feil ikke stopper applikasjonen. I GUI-et brukes statusfeltet til å vise meldinger, i stedet for blokkérende popup-dialoger.

### Varelager i GUI og nettleser

Et sentralt krav er at varelageret skal kunne vises både i Python-programmet og via API i nettleseren. Dette er løst ved at GUI-et henter og viser varelager i en tabell, mens samme data også er tilgjengelig gjennom et REST-endepunkt som brukes av frontenden på GitHub Pages. På den måten gjenbrukes samme datakilde i to ulike klienter.

### Ordreliste og ordredetaljer

Applikasjonen kan vise alle ordrer som ligger i databasen. Brukeren kan også velge en bestemt ordre og se tilhørende kundeinformasjon, varelinjer, pris per vare, linjesummer og totalbeløp inkludert merverdiavgift. Dette er implementert både i backend og GUI, slik at løsningen dekker hele arbeidsflyten fra oversikt til detaljvisning.

### Fakturagenerering med unikt fakturanummer

Oppgaven krever at det skal genereres faktura i PDF-format, og at fakturanummeret skal være unikt og lagres i databasen. Dette er løst ved at backend oppretter eller gjenbruker et fakturanummer per ordre, lagrer det i databasen og genererer en PDF-faktura med moms og ordredetaljer. GUI-et lar brukeren velge ordre og lagre fakturaen lokalt som PDF.

### Kunder via stored procedure

Kundelisten er implementert i tråd med kravet om stored procedures. I backend kalles `sp_list_kunder` for å hente kundedata fra databasen. Brukeren kan i tillegg legge til og slette kunder via GUI-et. Ved sletting kontrolleres det om kunden har tilknyttede ordrer, slik at databasen ikke settes i en ugyldig tilstand.

## Arkitektur og dataflyt

Løsningen er bygd opp i tre tydelige lag: GUI, API og database. GUI-et viser data og sender forespørsler, API-et håndterer validering og databaseoperasjoner, og databasen lagrer varer, kunder, ordrer og fakturaer. Denne oppdelingen gjør koden enklere å teste, lettere å vedlikeholde og tydeligere å forklare i rapporten.

## Utfordringer underveis

Det største arbeidet underveis har vært å få dataflyten stabil mellom GUI, API og database, samtidig som brukeropplevelsen ble ryddigere. Blant annet ble popup-dialoger byttet ut med en mer diskret statuslinje, og tabellvisningen ble justert for bedre søk, sortering og oppdatering. Det ble også gjort flere runder med feilretting og hardening for å sikre at løsningen oppfører seg stabilt både lokalt og mot den publiserte backend-tjenesten.

## Test og verifisering

Prosjektet er testet med smoke-test mot sentrale endepunkter. Dette ble gjort både for å verifisere at løsningen fungerte som forventet og som en del av lærepunktene i prosjektet, slik at vi fikk bekreftet hvordan GUI, API og database oppfører seg i praksis. Følgende ble verifisert i siste testløp:

En smoke test er en rask kontroll av de viktigste funksjonene i løsningen. I praksis betyr det at vi starter applikasjonen, tester de mest sentrale API-endepunktene, og sjekker at GUI-et åpner uten feil. Målet er ikke å teste absolutt alt, men å bekrefte at kjerneløsningen er stabil nok til videre bruk og demonstrasjon.

- `/health/db` svarte med HTTP 200 og `ok=True`
- `/api/varelager` svarte med HTTP 200 og `ok=True`
- `/api/ordrer` svarte med HTTP 200 og `ok=True`
- `/api/kunder` svarte med HTTP 200 og `ok=True`
- `gui.py` besto syntakskontroll
- GUI-et startet uten traceback

Dette gir et tydelig bevis på at kjerneløsningen fungerer i praksis.

## Knytting til kode og bevis

Følgende filer brukes som dokumentasjon og bevis i rapporten:

- [app.py](../../app.py): REST-API, databasekobling, parametriserte spørringer, stored procedure og fakturagenerering
- [gui.py](../../gui.py): Tkinter-GUI, visning av varelager, ordrer, kunder og fakturaflyt
- [docs/app.js](../app.js): Nettleserbasert visning av varelager og ordrer via API
- [CHECKLISTE.md](../project/CHECKLISTE.md): Testbevis og status for kravene
- [KRAVMATRISE.md](KRAVMATRISE.md): Kompakt oversikt over hvert krav og hvor det er løst
- [PROJECT_STATUS_LOG.md](../project/PROJECT_STATUS_LOG.md): Overleveringsstatus og verifiserte endepunkter

## Kort vurdering av måloppnåelse

Vurdert opp mot oppgaveteksten oppfyller prosjektet de viktigste funksjonskravene. Løsningen dekker dataflyt mellom GUI, API og database, og håndterer varelager, ordrer, kunder og faktura på en strukturert måte. Det som gjenstår før endelig innlevering er primært siste språkpolish, full presentasjonsøving og eventuelle manuelle kontrollpunkter som ikke lar seg automatisere helt.
