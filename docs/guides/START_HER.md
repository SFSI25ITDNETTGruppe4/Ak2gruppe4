# Start her - kjore programmet lokalt

Denne guiden er for deg som vil komme raskt i gang pa en ny PC.

## 1. Gaa til prosjektmappen

```powershell
cd "c:\Users\8968\OneDrive - Hatteland\Programering\SKOLEPROSJEKT\AK2gruppe4\Ak2gruppe4"
```

## 2. Opprett og aktiver virtuelt miljo

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Hvis aktivering er blokkert i PowerShell, kjor en gang:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## 3. Installer avhengigheter

```powershell
pip install -r requirements.txt
```

## 4. Sett opp miljofil

Hvis `.env` mangler:

```powershell
Copy-Item .env.example .env
```

Sjekk at disse verdiene er satt i `.env`:
- `DB_HOST`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`
- `API_BASE_URL`

## 5. Velg hvordan du vil kjore

### Alternativ A: Kjor GUI mot live backend (enklest)

I `.env`:
- `API_BASE_URL=https://ak2gruppe4.onrender.com`

Start GUI:

```powershell
python gui.py
```

### Alternativ B: Kjor backend lokalt + GUI lokalt

Start backend i ett terminalvindu:

```powershell
python app.py
```

Test backend:
- http://127.0.0.1:5000/health/db
- http://127.0.0.1:5000/api/varelager

Sett sa i `.env`:
- `API_BASE_URL=http://localhost:5000`

Start GUI i et nytt terminalvindu:

```powershell
python gui.py
```

## 6. Frontend i nettleser (docs)

Frontend for GitHub Pages ligger i `docs/`.
For live versjon:
- https://sfsi25itdnettgruppe4.github.io/Ak2gruppe4/

## Feilsoking

- Feil: `Access denied for user`
  - Sjekk DB-bruker/passord i `.env`.
- Feil: `WinError 10061`
  - GUI peker mot lokal backend som ikke kjorer. Bruk live URL eller start `app.py`.
- CORS-feil i nettleser
  - Sjekk `CORS_ALLOWED_ORIGINS` i backend-miljo (Render eller lokal).
