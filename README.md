# Ak2gruppe4

Flask-prosjekt for arbeidskrav med API mot databasen `varehusdb`.

Denne oppskriften bruker:
- Frontend: GitHub Pages (`docs/`)
- Backend API: Render (Flask + MySQL)

## 1. Lokal oppstart (backend)

1. Opprett `.env` i prosjektroten (bruk `.env.example` som mal).
2. Installer avhengigheter:

```powershell
pip install -r requirements.txt
```

3. Kjor appen:

```powershell
python app.py
```

4. Test API lokalt:
- `http://127.0.0.1:5000/api/varelager`
- `http://127.0.0.1:5000/api/ordrer`
- `http://127.0.0.1:5000/health/db`

## 2. Frontend pa GitHub Pages

Frontend ligger i `docs/`:
- `docs/index.html`
- `docs/style.css`
- `docs/app.js`
- `docs/config.js`

Steg:
1. Gå til GitHub repo -> Settings -> Pages.
2. Under "Build and deployment":
	- Source: `Deploy from a branch`
	- Branch: `main`
	- Folder: `/docs`
3. Lagre, vent pa publisering.
4. Nettadressen blir typisk:
	- `https://<github-user>.github.io/<repo-navn>/`

## 3. Backend pa Render

Render-oppsett finnes i `render.yaml`, `requirements.txt` og `Procfile`.

Steg:
1. Logg inn pa Render.
2. Opprett ny Web Service fra GitHub-repoet.
3. Velg branch dere vil deploye (f.eks. `main`).
4. Build/start skal være:
	- Build: `pip install -r requirements.txt`
	- Start: `gunicorn app:app`
5. Sett Environment Variables i Render:
	- `DB_HOST`
	- `DB_USER`
	- `DB_PASSWORD`
	- `DB_NAME=varehusdb`
	- `CORS_ALLOWED_ORIGINS=https://<github-user>.github.io`

Hvis dere bruker repo-path i Pages URL, kan dere sette flere origins kommaseparert:

```env
CORS_ALLOWED_ORIGINS=https://<github-user>.github.io,https://<github-user>.github.io/<repo-navn>
```

## 4. API-URL i frontend

I `docs/config.js`, sett Render-URL:

```js
window.APP_CONFIG = {
	 API_BASE_URL: "https://your-render-service.onrender.com"
};
```

Da kaller frontend:
- `https://your-render-service.onrender.com/api/varelager`
- `https://your-render-service.onrender.com/api/ordrer`

## 5. CORS

API-et tillater CORS via `CORS_ALLOWED_ORIGINS` i `app.py`.
Kun origin(er) i denne variabelen slipper til API-rutene.

## 6. Feilsoking

- `Access denied for user ...`:
  - Feil DB-bruker/passord eller manglende grants i MySQL.
- CORS-feil i nettleser:
  - Sjekk `CORS_ALLOWED_ORIGINS` i Render.
- 503 fra `/api/*`:
  - Sjekk `/health/db` for detaljert feilmelding.

## License

[GPL-3.0 license](LICENSE)
