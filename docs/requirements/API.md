# API-dokumentasjon - Varehus App

Base URL: `https://ak2gruppe4.onrender.com` (Production) eller `http://localhost:5000` (Development)

## Endpoints

### 📦 **Varelager**
```
GET /api/varelager
Returnerer alle varer på lager (varenummer, navn, antall, pris)

Response:
{
  "ok": true,
  "count": 150,
  "items": [
    {
      "VNr": 1,
      "Betegnelse": "Widget A",
      "Antall": 100,
      "Pris": 599.99
    }
  ]
}
```

---

### 📋 **Ordrer - Liste**
```
GET /api/ordrer
Returnerer alle ordrer (siste først, maks 300)

Response:
{
  "ok": true,
  "count": 45,
  "items": [
    {
      "OrdreNr": 1001,
      "OrdreDato": "2026-04-20",
      "SendtDato": "2026-04-21",
      "BetaltDato": "2026-04-21",
      "KNr": 5
    }
  ]
}
```

---

### 📄 **Ordrer - Detaljer**
```
GET /api/ordrer/<ordreNr>
Returnerer full ordre med varer, kunde-info og totalt (med moms)

Eksempel: GET /api/ordrer/1001

Response:
{
  "ok": true,
  "ordre": {
    "OrdreNr": 1001,
    "OrdreDato": "2026-04-20",
    "Navn": "Olsen AS",
    "Adresse": "Hovedgata 10",
    "Postnummer": "0150",
    "By": "Oslo"
  },
  "linjer": [
    {
      "VNr": 1,
      "Betegnelse": "Widget A",
      "Antall": 5,
      "Pris": 599.99,
      "LinjeSum": 2999.95
    }
  ],
  "totaler": {
    "total_før_moms": 2999.95,
    "moms_25_prosent": 750.00,
    "total_med_moms": 3749.95
  }
}
```

---

### 👥 **Kunder - Liste**
```
GET /api/kunder
Returnerer alle kunder (via Stored Procedure)

Response:
{
  "ok": true,
  "count": 25,
  "items": [
    {
      "KNr": 1,
      "Navn": "Olsen AS",
      "Adresse": "Hovedgata 10",
      "Postnummer": "0150",
      "By": "Oslo"
    }
  ]
}
```

---

### ➕ **Kunder - Legg til**
```
POST /api/kunder
Content-Type: application/json

Request:
{
  "Navn": "Ny Kunde AS",
  "Adresse": "Gata 5",
  "Postnummer": "0200",
  "By": "Bergen"
}

Response (201 Created):
{
  "ok": true,
  "message": "Kunde lagt til",
  "KNr": 26
}

Error Response (400 Bad Request):
{
  "ok": false,
  "message": "Alle felter er påkrevd"
}
```

---

### ❌ **Kunder - Slett**
```
DELETE /api/kunder/<KNr>
Sletter kunde hvis den ikke har aktive ordrer

Eksempel: DELETE /api/kunder/26

Response (200 OK):
{
  "ok": true,
  "message": "Kunde slettet"
}

Error Response (409 Conflict):
{
  "ok": false,
  "message": "Kan ikke slette kunde - har 3 ordre(r)"
}

Error Response (404 Not Found):
{
  "ok": false,
  "message": "Kunde ikke funnet"
}
```

---

### 🧾 **Faktura - Generer PDF**
```
POST /api/ordrer/<ordreNr>/faktura
Genererer faktura-PDF med moms og lagrer unikt fakturanummer i databasen.

Eksempel: POST /api/ordrer/22696/faktura

Response (200 OK):
- Content-Type: application/pdf
- Header: X-Invoice-Number: FAK-20260426-22696-1234
- Body: PDF-fil

Error Response (404 Not Found):
{
  "ok": false,
  "message": "Ordre ikke funnet"
}

Error Response (409 Conflict):
{
  "ok": false,
  "message": "Ordren har ingen ordrelinjer"
}
```

---

### 🏥 **Helse-sjekk**
```
GET /health/db
Sjekker databasetilkobling

Response (200 OK):
{
  "ok": true,
  "message": "Database connection successful"
}

Response (503 Service Unavailable):
{
  "ok": false,
  "message": "Database connection failed"
}
```

---

## CORS

API'en støtter CORS for følgende origin-er (fra `.env`):
- `CORS_ALLOWED_ORIGINS=https://sfsi25itdnettgruppe4.github.io,https://sfsi25itdnettgruppe4.github.io/Ak2gruppe4,http://127.0.0.1:5000,http://localhost:5000`

---

## Error Handling

Alle endpoints returnerer JSON med struktur:
```json
{
  "ok": true/false,
  "message": "Feilmelding hvis noe gikk galt",
  "items": [...] eller "count": 5
}
```

**HTTP Status Codes:**
- `200` - OK
- `201` - Created
- `400` - Bad Request (validering feilet)
- `404` - Not Found
- `409` - Conflict (f.eks. sletting av kunde med ordrer)
- `503` - Service Unavailable (database error)

---

## Database Setup

For at API'en skal virke fullt ut, kjør dette SQL-scriptet:
```bash
mysql -u <bruker> -p varehusdb < db/setup_api_features.sql
```

Dette oppretter:
- Stored Procedure: `sp_list_kunder()`
- Tabell: `faktura` for unikt fakturanummer per ordre
- Sjekker tabell-strukturer

