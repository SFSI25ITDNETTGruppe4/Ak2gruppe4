import os

import pymysql
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask, jsonify, render_template, request

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

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/varelager")
def api_varelager():
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


@app.route("/api/ordrer/<int:ordreNr>")
def api_ordrer_detaljer(ordreNr):
    """Hent detaljer for en spesifikk ordre: varer, antall, pris, kunde info, total"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Hent ordreinfo + kundeinfo
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


@app.route("/api/kunder", methods=["GET", "POST"])
def api_kunder():
    """GET: Liste alle kunder via Stored Procedure. POST: Legg til ny kunde"""
    if request.method == "GET":
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                # Kall Stored Procedure for å liste kunder
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

if __name__ == "__main__":
    app.run(debug=True)
