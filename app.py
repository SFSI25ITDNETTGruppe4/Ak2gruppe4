"""Backend for arbeidskravet i Python og database.

Denne filen dekker API-delen av oppgaven: databasekobling, trygg SQL,
ordre- og kundehenting, samt generering av faktura-PDF med unikt
fakturanummer lagret i databasen.

For å kjøre appen lokalt må disse avhengighetene være installert:
- Flask
- PyMySQL
- python-dotenv
- flask-cors
- reportlab

I tillegg må .env inneholde DB_HOST, DB_USER, DB_PASSWORD og DB_NAME.
"""

import os
import io
import secrets
from datetime import datetime

import pymysql
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask, jsonify, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

load_dotenv()

app = Flask(__name__)


def get_allowed_origins():
    raw = os.getenv("CORS_ALLOWED_ORIGINS", "")
    if raw.strip():
        return [origin.strip() for origin in raw.split(",") if origin.strip()]
    return ["http://127.0.0.1:5000", "http://localhost:5000"]


CORS(
    app,
    resources={
        r"/api/*": {"origins": get_allowed_origins()},
        r"/health/*": {"origins": get_allowed_origins()},
    },
)


def get_db_config():
    # Support both DB_* and generic HOST/USER/PASSWORD names used by some hosts.
    return {
        "host": os.getenv("DB_HOST") or os.getenv("HOST") or "",
        "user": os.getenv("DB_USER") or os.getenv("USER") or "",
        "password": os.getenv("DB_PASSWORD") or os.getenv("PASSWORD") or "",
        "database": os.getenv("DB_NAME") or os.getenv("DATABASE") or "varehusdb",
    }


app.config["DB_CONFIG"] = get_db_config()

#Husk at for at dette skal virke må miljøvariablene være satt riktigt, og at databasen er tilgjengelig. Det kan være lurt å teste databasekoblingen først via /health/db-endepunktet

def get_db_connection():
    config = app.config["DB_CONFIG"]
    return pymysql.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"],
        connect_timeout=5,
        cursorclass=pymysql.cursors.DictCursor,
    )


def fetch_all(query, params=None):
    # Felles hjelpefunksjon for lesespørringer. Parametre sendes separat for å
    # unngå stringbygging av SQL i rutene.
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            rows = cursor.fetchall()
        connection.close()
        return rows, None
    except Exception as exc:
        return None, str(exc)


def check_db_connection():
    config = app.config["DB_CONFIG"]

    missing = [k.upper() for k, v in config.items() if not v]
    if missing:
        return False, f"Missing environment variables: {', '.join(missing)}"

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        connection.close()
        return True, "Database connection successful"
    except Exception as exc:
        return False, str(exc)


def ensure_invoice_table(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS faktura (
            FakturaID INT AUTO_INCREMENT PRIMARY KEY,
            FakturaNr VARCHAR(40) NOT NULL UNIQUE,
            OrdreNr INT NOT NULL,
            Opprettet DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            TotalForMoms DECIMAL(12, 2) NOT NULL,
            MomsBelop DECIMAL(12, 2) NOT NULL,
            TotalMedMoms DECIMAL(12, 2) NOT NULL,
            UNIQUE KEY uk_faktura_ordre (OrdreNr)
        )
        """
    )


def generate_unique_invoice_number(cursor, ordre_nr):
    date_part = datetime.utcnow().strftime("%Y%m%d")
    for _ in range(20):
        token = secrets.randbelow(10000)
        faktura_nr = f"FAK-{date_part}-{ordre_nr}-{token:04d}"
        cursor.execute("SELECT 1 FROM faktura WHERE FakturaNr = %s", (faktura_nr,))
        if not cursor.fetchone():
            return faktura_nr
    raise RuntimeError("Klarte ikke generere unikt fakturanummer")


def build_invoice_pdf(ordre, linjer, totaler, faktura_nr):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(40, y, "Faktura")
    y -= 28

    pdf.setFont("Helvetica", 10)
    pdf.drawString(40, y, f"Fakturanummer: {faktura_nr}")
    y -= 16
    pdf.drawString(40, y, f"OrdreNr: {ordre['OrdreNr']}")
    y -= 16
    pdf.drawString(40, y, f"Dato: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y -= 28

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(40, y, "Kunde")
    y -= 18
    pdf.setFont("Helvetica", 10)
    pdf.drawString(40, y, ordre.get("Navn") or "Ukjent kunde")
    y -= 14
    pdf.drawString(40, y, ordre.get("Adresse") or "")
    y -= 14
    pdf.drawString(40, y, f"{ordre.get('Postnummer') or ''} {ordre.get('By') or ''}".strip())
    y -= 26

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(40, y, "VNr")
    pdf.drawString(85, y, "Vare")
    pdf.drawRightString(360, y, "Antall")
    pdf.drawRightString(450, y, "Pris")
    pdf.drawRightString(540, y, "Linjesum")
    y -= 10
    pdf.line(40, y, 545, y)
    y -= 14

    pdf.setFont("Helvetica", 10)
    for linje in linjer:
        if y < 120:
            pdf.showPage()
            y = height - 50
            pdf.setFont("Helvetica", 10)
        pdf.drawString(40, y, str(linje["VNr"]))
        pdf.drawString(85, y, str(linje["Betegnelse"])[:42])
        pdf.drawRightString(360, y, str(linje["Antall"]))
        pdf.drawRightString(450, y, f"{float(linje['Pris']):.2f} kr")
        pdf.drawRightString(540, y, f"{float(linje['LinjeSum']):.2f} kr")
        y -= 14

    y -= 8
    pdf.line(340, y, 545, y)
    y -= 18
    pdf.drawRightString(520, y, "Subtotal:")
    pdf.drawRightString(545, y, f"{float(totaler['total_før_moms']):.2f} kr")
    y -= 16
    pdf.drawRightString(520, y, "MVA 25%:")
    pdf.drawRightString(545, y, f"{float(totaler['moms_25_prosent']):.2f} kr")
    y -= 18
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawRightString(520, y, "Total:")
    pdf.drawRightString(545, y, f"{float(totaler['total_med_moms']):.2f} kr")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/varelager")
def api_varelager():
    # Oppgavekrav: vise varelager via API, slik at data også kan brukes i nettleser.
    query = """
        SELECT VNr, Betegnelse, Antall, Pris
        FROM vare
        ORDER BY Betegnelse ASC
        LIMIT 500
    """
    rows, error = fetch_all(query)
    if error:
        return jsonify({"ok": False, "message": error}), 503
    return jsonify({"ok": True, "count": len(rows), "items": rows})

# denne ruten viser de 300 siste ordrene, sortert etter ordreNr synkende. Det er ikke et krav i oppgaven, men det er ofte mer praktisk å vise de siste ordrene først, og begrense antallet for å unngå store datamengder i responsen.

@app.route("/api/ordrer")
def api_ordrer():
    query = """
        SELECT OrdreNr, OrdreDato, SendtDato, BetaltDato, KNr
        FROM ordre
        ORDER BY OrdreNr DESC
        LIMIT 300
    """
    rows, error = fetch_all(query)
    if error:
        return jsonify({"ok": False, "message": error}), 503
    return jsonify({"ok": True, "count": len(rows), "items": rows})
#denne ruten viser detaljer for en spesifikk ordre, inkludert kundeinfo, varelinjer og totaler. Den bruker parameterisert SQL for å unngå SQL-injeksjon, og håndterer både tilfeller der ordren ikke finnes og der den finnes


@app.route("/api/ordrer/<int:ordreNr>")
def api_ordrer_detaljer(ordreNr):
    """Hent detaljer for en spesifikk ordre: varer, antall, pris, kunde info, total"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Oppgavekrav: valgt ordre skal vise både kundeinfo, varelinjer og total.
            ordre_query = """
                SELECT o.OrdreNr, o.OrdreDato, o.SendtDato, o.BetaltDato,
                       k.KNr,
                       CONCAT(k.Fornavn, ' ', k.Etternavn) AS Navn,
                       k.Adresse,
                       k.PostNr AS Postnummer,
                      p.Poststed AS `By`
                FROM ordre o
                LEFT JOIN kunde k ON o.KNr = k.KNr
                LEFT JOIN poststed p ON k.PostNr = p.PostNr
                WHERE o.OrdreNr = %s
            """
            cursor.execute(ordre_query, (ordreNr,))
            ordre_data = cursor.fetchone()
            
            if not ordre_data:
                connection.close()
                return jsonify({"ok": False, "message": "Ordre ikke funnet"}), 404
            
            # Hent orderlinjer med varenavn
            linjer_query = """
                  SELECT ol.OrdreNr, ol.VNr, v.Betegnelse, ol.Antall,
                      ol.PrisPrEnhet AS Pris,
                      (ol.Antall * ol.PrisPrEnhet) as LinjeSum
                  FROM ordrelinje ol
                JOIN vare v ON ol.VNr = v.VNr
                WHERE ol.OrdreNr = %s
                ORDER BY ol.VNr
            """
            cursor.execute(linjer_query, (ordreNr,))
            linjer = cursor.fetchall()
            
            # Beregn total (med 25% moms som standard)
            total_før_moms = sum(float(linje['LinjeSum']) for linje in linjer) if linjer else 0
            moms = total_før_moms * 0.25
            total_med_moms = total_før_moms + moms
            
            connection.close()
            
            return jsonify({
                "ok": True,
                "ordre": ordre_data,
                "linjer": linjer,
                "totaler": {
                    "total_før_moms": round(total_før_moms, 2),
                    "moms_25_prosent": round(moms, 2),
                    "total_med_moms": round(total_med_moms, 2)
                }
            })
    except Exception as exc:
        return jsonify({"ok": False, "message": str(exc)}), 503
#denne ruten håndterer både GET og POST for kunder. GET henter alle kunder via en Stored Procedure, mens POST legger til en ny kunde med validering av input. Den støtter både "Navn" som ett felt og "Fornavn"/"Etternavn" som separate felt, og returnerer passende feilmeldinger ved valideringsfeil eller databasefeil.


@app.route("/api/kunder", methods=["GET", "POST"])
def api_kunder():
    """GET: Liste alle kunder via Stored Procedure. POST: Legg til ny kunde"""
    if request.method == "GET":
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                # Oppgavekrav: kundelisten skal hentes via Stored Procedure.
                cursor.callproc("sp_list_kunder")
                kunder = cursor.fetchall()
            connection.close()
            return jsonify({"ok": True, "count": len(kunder), "items": kunder})
        except Exception as exc:
            return jsonify({"ok": False, "message": str(exc)}), 503
    
    elif request.method == "POST":
        data = request.get_json() or {}
        navn = data.get("Navn", "").strip()
        fornavn = data.get("Fornavn", "").strip()
        etternavn = data.get("Etternavn", "").strip()
        adresse = data.get("Adresse", "").strip()
        postnummer = data.get("Postnummer", data.get("PostNr", "")).strip()
        
        # Støtt både Navn-felt og Fornavn/Etternavn-felter
        if navn and (not fornavn and not etternavn):
            parts = navn.split(maxsplit=1)
            fornavn = parts[0]
            etternavn = parts[1] if len(parts) > 1 else "Ukjent"

        # Validering
        if not all([fornavn, etternavn, adresse, postnummer]):
            return jsonify({"ok": False, "message": "Fornavn, etternavn, adresse og postnummer er påkrevd"}), 400
        
        if len(fornavn) > 50 or len(etternavn) > 50 or len(adresse) > 100:
            return jsonify({"ok": False, "message": "Fornavn/etternavn/adresse er for langt"}), 400

        if len(postnummer) != 4 or not postnummer.isdigit():
            return jsonify({"ok": False, "message": "Postnummer må være 4 siffer"}), 400
        
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                insert_query = """
                    INSERT INTO kunde (Fornavn, Etternavn, Adresse, PostNr)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (fornavn, etternavn, adresse, postnummer))
                connection.commit()
                cursor.execute("SELECT MAX(KNr) AS KNr FROM kunde")
                new_knr = cursor.fetchone()["KNr"]
            connection.close()
            
            return jsonify({
                "ok": True, 
                "message": "Kunde lagt til",
                "KNr": new_knr
            }), 201
        except Exception as exc:
            return jsonify({"ok": False, "message": str(exc)}), 503
        

#denne ruten sletter en kunde basert på KNr, men bare hvis kunden ikke har noen tilknyttede ordrer. Den sjekker først for eksisterende ordrer, og returnerer en konfliktfeil hvis det finnes noen. Hvis kunden slettes, returneres en suksessmelding. Hvis kunden ikke finnes, returneres en 404-feil.

@app.route("/api/kunder/<int:KNr>", methods=["DELETE"])
def api_slett_kunde(KNr):
    """Slett en kunde (hvis den ikke har ordrer)"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Sjekk om kunden har ordrer
            check_query = "SELECT COUNT(*) as antall FROM ordre WHERE KNr = %s"
            cursor.execute(check_query, (KNr,))
            result = cursor.fetchone()
            
            if result['antall'] > 0:
                connection.close()
                return jsonify({
                    "ok": False, 
                    "message": f"Kan ikke slette kunde - har {result['antall']} ordre(r)"
                }), 409
            
            # Slett kunden
            delete_query = "DELETE FROM kunde WHERE KNr = %s"
            cursor.execute(delete_query, (KNr,))
            connection.commit()
            
            if cursor.rowcount == 0:
                connection.close()
                return jsonify({"ok": False, "message": "Kunde ikke funnet"}), 404
            
            connection.close()
            return jsonify({"ok": True, "message": "Kunde slettet"}), 200
            
    except Exception as exc:
        return jsonify({"ok": False, "message": str(exc)}), 503


@app.route("/health/db")
def health_db():
    ok, message = check_db_connection()
    status = 200 if ok else 503
    return jsonify({"ok": ok, "message": message}), status

#denne ruten håndterer generering av PDF-faktura for en gitt ordre. Den henter ordre- og kundeinfo, samt varelinjer, og beregner totaler med moms. Den sjekker om det allerede finnes en faktura for ordren, og hvis ikke, genererer den et unikt fakturanummer og lagrer fakturainformasjonen i databasen

@app.route("/api/ordrer/<int:ordreNr>/faktura", methods=["POST"])
def api_generer_faktura(ordreNr):
    # Oppgavekrav: generer PDF-faktura med moms og et unikt fakturanummer som lagres.
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            ensure_invoice_table(cursor)

            ordre_query = """
                SELECT o.OrdreNr, o.OrdreDato,
                       k.KNr,
                       CONCAT(k.Fornavn, ' ', k.Etternavn) AS Navn,
                       k.Adresse,
                       k.PostNr AS Postnummer,
                       p.Poststed AS `By`
                FROM ordre o
                LEFT JOIN kunde k ON o.KNr = k.KNr
                LEFT JOIN poststed p ON k.PostNr = p.PostNr
                WHERE o.OrdreNr = %s
            """
            cursor.execute(ordre_query, (ordreNr,))
            ordre_data = cursor.fetchone()
            if not ordre_data:
                connection.close()
                return jsonify({"ok": False, "message": "Ordre ikke funnet"}), 404

            linjer_query = """
                SELECT ol.OrdreNr, ol.VNr, v.Betegnelse, ol.Antall,
                       ol.PrisPrEnhet AS Pris,
                       (ol.Antall * ol.PrisPrEnhet) AS LinjeSum
                FROM ordrelinje ol
                JOIN vare v ON ol.VNr = v.VNr
                WHERE ol.OrdreNr = %s
                ORDER BY ol.VNr
            """
            cursor.execute(linjer_query, (ordreNr,))
            linjer = cursor.fetchall()
            if not linjer:
                connection.close()
                return jsonify({"ok": False, "message": "Ordren har ingen ordrelinjer"}), 409

            subtotal = sum(float(linje["LinjeSum"]) for linje in linjer)
            moms = subtotal * 0.25
            total = subtotal + moms
            totaler = {
                "total_før_moms": round(subtotal, 2),
                "moms_25_prosent": round(moms, 2),
                "total_med_moms": round(total, 2),
            }

            cursor.execute("SELECT FakturaNr FROM faktura WHERE OrdreNr = %s", (ordreNr,))
            existing = cursor.fetchone()
            if existing:
                faktura_nr = existing["FakturaNr"]
            else:
                faktura_nr = generate_unique_invoice_number(cursor, ordreNr)
                insert_query = """
                    INSERT INTO faktura (
                        FakturaNr, OrdreNr, TotalForMoms, MomsBelop, TotalMedMoms
                    ) VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(
                    insert_query,
                    (faktura_nr, ordreNr, totaler["total_før_moms"], totaler["moms_25_prosent"], totaler["total_med_moms"]),
                )
                connection.commit()

        connection.close()

        pdf_buffer = build_invoice_pdf(ordre_data, linjer, totaler, faktura_nr)
        response = send_file(
            pdf_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"{faktura_nr}.pdf",
        )
        response.headers["X-Invoice-Number"] = faktura_nr
        return response
    except Exception as exc:
        return jsonify({"ok": False, "message": str(exc)}), 503

if __name__ == "__main__":
    app.run(debug=True)
