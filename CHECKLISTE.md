# CHECKLISTE FØR DEMO OG INNLEVERING

## 1) Oppsett

- [ ] Kjør `pip install -r requirements.txt`
- [ ] Kopier `.env.example` til `.env`
- [ ] Bekreft at `API_BASE_URL` i `.env` peker til riktig miljø

## 2) Backend/API

- [ ] `GET /health/db` svarer med `ok: true`
- [ ] `GET /api/varelager` returnerer varer
- [ ] `GET /api/ordrer` returnerer ordrer
- [ ] `GET /api/ordrer/<ordreNr>` returnerer ordrelinjer, kunde, totaler
- [ ] `GET /api/kunder` fungerer via stored procedure
- [ ] `POST /api/kunder` fungerer med gyldige data
- [ ] `DELETE /api/kunder/<KNr>` fungerer for kunde uten ordrer
- [ ] `POST /api/ordrer/<ordreNr>/faktura` returnerer PDF

## 3) Database

- [ ] `sp_list_kunder` finnes i databasen
- [ ] Tabell `faktura` finnes i databasen
- [ ] Fakturanummer blir unikt og lagres for ordre

## 4) GUI

- [ ] GUI starter uten crash (`python gui.py`)
- [ ] Varelager-tab viser data
- [ ] Ordre-tab viser data
- [ ] Ordredetaljer åpner og viser riktig summer
- [ ] Kundeliste lastes
- [ ] Legg til kunde fungerer med validering
- [ ] Slett kunde fungerer og gir tydelig feilmelding ved konflikt
- [ ] Faktura-PDF kan genereres og lagres fra GUI

## 5) Frontend (GitHub Pages)

- [ ] URL laster: `https://sfsi25itdnettgruppe4.github.io/Ak2gruppe4/`
- [ ] "Last varelager" fungerer
- [ ] "Last ordre" fungerer
- [ ] Ingen CORS-feil i nettleserens console

## 6) Render

- [ ] Service deployer grønt i Render
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `gunicorn app:app`
- [ ] Health check path: `/health/db`
- [ ] Alle env vars satt (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, CORS_ALLOWED_ORIGINS)

## 7) Dokumentasjon

- [ ] README er oppdatert med full oppstartsguide
- [ ] API.md matcher faktisk API
- [ ] PROJECT_STATUS_LOG.md er oppdatert med siste status
- [ ] Commit-meldinger er tydelige og beskriver endringen

## 8) Rapport og presentasjon

- [ ] Kravmatrise: hvert krav koblet til funksjon/bevis
- [ ] Skjermbilder av GUI, frontend og API-test
- [ ] Kort testprotokoll (happy path + feilsituasjon)
- [ ] Begrunnelse for teknologi (Tkinter, Flask, Render, RDS)
- [ ] Presentasjon testet på 30 min eller mindre
