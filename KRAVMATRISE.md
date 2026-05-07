# KRAVMATRISE AK2

Sist oppdatert: 2026-05-07

| Krav fra oppgaven | Løsning | Bevis (fil/endepunkt) | Status |
|---|---|---|---|
| GUI koblet til database via Python | Tkinter GUI + Flask API + MySQL | `gui.py`, `app.py` | Oppfylt |
| Sikring mot SQL-injection | Parameterisert SQL med `%s`-parametre | `app.py` | Oppfylt |
| Validering av inndata | Validering av kundeinnslag (lengde/postnummer/felter) | `app.py` (`POST /api/kunder`) | Oppfylt |
| Robusthet mot utilsiktede stopp | Try/except i API og statusmeldinger i GUI | `app.py`, `gui.py` | Oppfylt |
| Vise varelager i GUI | Egen tabell med VNr, navn, antall, pris | `gui.py` (`show_varelager`) | Oppfylt |
| Vise varelager via API i nettleser | API + frontend i `docs/` | `GET /api/varelager`, `docs/app.js` | Oppfylt |
| Liste alle ordrer | Eget endepunkt og GUI-tab | `GET /api/ordrer`, `gui.py` | Oppfylt |
| Vise detaljer for valgt ordre | Kunde, ordrelinjer, summer inkl. mva | `GET /api/ordrer/<ordreNr>`, `gui.py` | Oppfylt |
| Generere faktura-PDF med unikt fakturanummer lagret i DB | PDF-generering, unikhet og lagring i tabell `faktura` | `POST /api/ordrer/<ordreNr>/faktura`, `app.py` | Oppfylt |
| Vise kunder via Stored Procedure | `sp_list_kunder` brukes i API | `GET /api/kunder`, `app.py` | Oppfylt |
| Legge til og fjerne kunder | `POST`/`DELETE` endepunkt + GUI-handlinger | `app.py`, `gui.py` | Oppfylt |
| Varelager i browser via API | GitHub Pages mot Render API | `https://sfsi25itdnettgruppe4.github.io/Ak2gruppe4/` | Oppfylt |

## Leveransekrav utenfor kode

| Krav | Status | Kommentar |
|---|---|---|
| Rapport (12-18 sider) | Pågår | Må ferdigstilles før innlevering |
| Presentasjon (maks 30 min) | Pågår | Innhold finnes, plassholdere må fylles |
| Gruppelogg | Delvis | Commit-historikk finnes, oppsummering bør samles |
| Individuell refleksjonsvideo | Ikke verifisert | Gjennomføres individuelt |

## Testbevis brukt i status

- Smoke-test 2026-05-07:
  - `/health/db` -> HTTP 200, `ok=True`
  - `/api/varelager` -> HTTP 200, `ok=True`
  - `/api/ordrer` -> HTTP 200, `ok=True`
  - `/api/kunder` -> HTTP 200, `ok=True`
  - `gui.py` syntaks -> OK
  - `gui.py` oppstart -> OK
