# Ak2gruppe4

Flask-prosjekt for arbeidskrav med API mot databasen `varehusdb`.

Denne oppskriften dekker alt som trengs for å kjøre prosjektet:
- Frontend: GitHub Pages (`docs/`)
- Backend API: Render (Flask + MySQL)
- GUI: Tkinter (`gui.py`)

## 0. Krav

- Python 3.11+
- Pip
- Git
- (Valgfritt) MySQL-klient for lokal DB-setup

## 1. Kom i gang lokalt (anbefalt for alle i gruppa)

1. Klon repo.
2. Opprett virtuelt miljø og aktiver det.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Installer avhengigheter:

```powershell
pip install -r requirements.txt
```

4. Kopier `.env.example` til `.env` og fyll inn verdier.

Eksempel:

```env
DB_HOST=<rds-endepunkt>
DB_USER=<aws-bruker>
DB_PASSWORD=<aws-passord>
DB_NAME=varehusdb
CORS_ALLOWED_ORIGINS=https://sfsi25itdnettgruppe4.github.io,https://sfsi25itdnettgruppe4.github.io/Ak2gruppe4

# GUI-config
API_BASE_URL=https://ak2gruppe4.onrender.com
```

## 2. Start backend lokalt (valgfritt)

Kjør:

```powershell
python app.py
```

Test lokalt:
- `http://127.0.0.1:5000/api/varelager`
- `http://127.0.0.1:5000/api/ordrer`
- `http://127.0.0.1:5000/health/db`

## 3. Start GUI (for medelever)

GUI leser `API_BASE_URL` fra `.env`.
- Standard i prosjektet: `https://ak2gruppe4.onrender.com`
- Hvis dere vil bruke lokal backend: sett `API_BASE_URL=http://localhost:5000`

Kjør GUI:

```powershell
python gui.py
```

## 4. Database-setup for API-funksjoner

Kjør SQL-scriptet som oppretter stored procedure og faktura-tabell:

```powershell
mysql -u <bruker> -p varehusdb < db/setup_api_features.sql
```

Dette setter opp:
- `sp_list_kunder` (stored procedure)
- `faktura`-tabell (unikt fakturanummer per ordre)

## 5. Frontend på GitHub Pages

Frontend ligger i `docs/`:
- `docs/index.html`
- `docs/style.css`
- `docs/app.js`
- `docs/config.js`

GitHub Pages-oppsett:
1. Gå til GitHub repo -> Settings -> Pages.
2. Under "Build and deployment":
	 - Source: `Deploy from a branch`
	 - Branch: `main`
	 - Folder: `/docs`
3. Lagre, vent pa publisering.
4. URL for dette prosjektet:
	 - `https://sfsi25itdnettgruppe4.github.io/Ak2gruppe4/`

## 6. Backend på Render (dokumentert konfig)

Render-oppsett finnes i `render.yaml` (kilde for sannhet):
- Service type: `web`
- Name: `ak2gruppe4-api`
- Runtime: `python`
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Health check path: `/health/db`
- Plan: `free`

Alternativ A (anbefalt):
1. I Render, velg "Blueprint"/"New" fra repo med `render.yaml`.

Alternativ B (manuell):
1. Logg inn pa Render.
2. Opprett ny Web Service fra GitHub-repoet.
3. Branch: `main`
4. Build: `pip install -r requirements.txt`
5. Start: `gunicorn app:app`
6. Health check path: `/health/db`
7. Sett Environment Variables:
	 - `DB_HOST`
	 - `DB_USER`
	 - `DB_PASSWORD`
	 - `DB_NAME=varehusdb`
	 - `CORS_ALLOWED_ORIGINS=https://sfsi25itdnettgruppe4.github.io,https://sfsi25itdnettgruppe4.github.io/Ak2gruppe4`

## 7. API-URL i frontend

I `docs/config.js`:

```js
window.APP_CONFIG = {
	API_BASE_URL: "https://ak2gruppe4.onrender.com"
};
```

## 8. Viktige endepunkter

- `GET /health/db`
- `GET /api/varelager`
- `GET /api/ordrer`
- `GET /api/ordrer/<ordreNr>`
- `GET /api/kunder`
- `POST /api/kunder`
- `DELETE /api/kunder/<KNr>`
- `POST /api/ordrer/<ordreNr>/faktura` (PDF)

## 9. Feilsøking

- `WinError 10061` i GUI:
	- API peker mot localhost men backend kjører ikke. Sett `API_BASE_URL` i `.env` til Render-URL.
- `Access denied for user ...`:
	- Feil DB-bruker/passord eller manglende grants.
- 503 fra `/api/*`:
	- Sjekk `/health/db` for detaljert feil.
- CORS-feil i nettleser:
	- Sjekk `CORS_ALLOWED_ORIGINS` i Render.

## 10. Rask oppstart for medelever (kortversjon)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python gui.py
```

Hvis dere vil teste lokal backend:

```powershell
python app.py
```

## 11. License

[GPL-3.0 license](LICENSE)
