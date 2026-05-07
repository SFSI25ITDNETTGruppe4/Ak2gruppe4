# CHECKLISTE FØR DEMO OG INNLEVERING

Sist oppdatert: 2026-05-07

Statusnøkler:
- [x] Verifisert
- [~] Delvis verifisert / dokumentert, men bør demo-testes manuelt
- [ ] Ikke verifisert i denne sjekklisten

## 1) Oppsett

- [~] Kjør `pip install -r requirements.txt` (bevis: dokumentert i `README.md`, ikke re-kjørt i denne økten)
- [~] Kopier `.env.example` til `.env` (bevis: dokumentert i `README.md`, ikke re-kjørt i denne økten)
- [x] Bekreft at `API_BASE_URL` i `.env` peker til riktig miljø (bevis: live-kall mot `https://ak2gruppe4.onrender.com` ga HTTP 200)

## 2) Backend/API

- [x] `GET /health/db` svarer med `ok: true` (bevis: smoke-test 2026-05-07, HTTP 200, `ok=True`)
- [x] `GET /api/varelager` returnerer varer (bevis: smoke-test 2026-05-07, HTTP 200, `ok=True`)
- [x] `GET /api/ordrer` returnerer ordrer (bevis: smoke-test 2026-05-07, HTTP 200, `ok=True`)
- [~] `GET /api/ordrer/<ordreNr>` returnerer ordrelinjer, kunde, totaler (bevis: implementert i `app.py`, bør kjøres med kjent OrdreNr i siste testrunde)
- [~] `GET /api/kunder` fungerer via stored procedure (bevis: smoke-test 2026-05-07, HTTP 200, `ok=True`; tilleggssjekk av SP i DB anbefales)
- [ ] `POST /api/kunder` fungerer med gyldige data (må verifiseres eksplisitt i siste demo-test)
- [ ] `DELETE /api/kunder/<KNr>` fungerer for kunde uten ordrer (må verifiseres eksplisitt i siste demo-test)
- [ ] `POST /api/ordrer/<ordreNr>/faktura` returnerer PDF (må verifiseres eksplisitt i siste demo-test)

## 3) Database

- [~] `sp_list_kunder` finnes i databasen (bevis: API-rute bruker `cursor.callproc("sp_list_kunder")`; bør verifiseres med SQL-klient)
- [~] Tabell `faktura` finnes i databasen (bevis: opprettes ved behov i `ensure_invoice_table()`)
- [~] Fakturanummer blir unikt og lagres for ordre (bevis: `UNIQUE` på `FakturaNr` + gjenbruk per ordre i `app.py`; bør demo-verifiseres med fakturakall)

## 4) GUI

- [x] GUI starter uten crash (`python gui.py`) (bevis: smoke-test 2026-05-07)
- [~] Varelager-tab viser data (bevis: støttet av API 200 + implementasjon i `gui.py`; bør klikk-testes rett før demo)
- [~] Ordre-tab viser data (bevis: støttet av API 200 + implementasjon i `gui.py`; bør klikk-testes rett før demo)
- [~] Ordredetaljer åpner og viser riktig summer (bevis: implementert i `gui.py`; bør klikk-testes rett før demo)
- [~] Kundeliste lastes (bevis: API 200 + bugfix for tabellfylling er gjort)
- [ ] Legg til kunde fungerer med validering (må verifiseres manuelt i siste demo-test)
- [ ] Slett kunde fungerer og gir tydelig feilmelding ved konflikt (må verifiseres manuelt i siste demo-test)
- [ ] Faktura-PDF kan genereres og lagres fra GUI (må verifiseres manuelt i siste demo-test)

## 5) Frontend (GitHub Pages)

- [x] URL laster: `https://sfsi25itdnettgruppe4.github.io/Ak2gruppe4/` (bevis: HTTP 200 i live-sjekk 2026-05-07)
- [ ] "Last varelager" fungerer (må verifiseres manuelt i nettleser)
- [ ] "Last ordre" fungerer (må verifiseres manuelt i nettleser)
- [ ] Ingen CORS-feil i nettleserens console (må verifiseres manuelt i nettleser)

## 6) Render

- [x] Service deployer grønt i Render (bevis: live-endepunkt svarer HTTP 200)
- [~] Build command: `pip install -r requirements.txt` (bevis: dokumentert i `render.yaml`/`README.md`)
- [~] Start command: `gunicorn app:app` (bevis: dokumentert i `render.yaml`/`README.md`)
- [x] Health check path: `/health/db` (bevis: live-kall HTTP 200)
- [~] Alle env vars satt (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, CORS_ALLOWED_ORIGINS) (bevis: app er oppe; eksplisitt skjermbilde fra Render anbefales)

## 7) Dokumentasjon

- [x] README er oppdatert med full oppstartsguide
- [~] API.md matcher faktisk API (bør ta siste hurtigsjekk mot `app.py`)
- [~] PROJECT_STATUS_LOG.md er oppdatert med siste status (bør oppdateres med release v1.0.0)
- [x] Commit-meldinger er tydelige og beskriver endringen

## 8) Rapport og presentasjon

- [x] Kravmatrise: hvert krav koblet til funksjon/bevis (se `KRAVMATRISE.md`)
- [ ] Skjermbilder av GUI, frontend og API-test (mangler innliming i presentasjonen)
- [~] Kort testprotokoll (happy path + feilsituasjon) (delvis: smoke-test logget i `README.md`)
- [~] Begrunnelse for teknologi (Tkinter, Flask, Render, RDS) (delvis i docs; ferdigstilles i rapport)
- [ ] Presentasjon testet på 30 min eller mindre (må gjennomføres)
