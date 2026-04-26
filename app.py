import os

import pymysql
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

load_dotenv()

app = Flask(__name__)


def get_db_config():
    return {
        "host": os.getenv("DB_HOST", ""),
        "user": os.getenv("DB_USER", ""),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "varehusdb"),
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


@app.route("/health/db")
def health_db():
    ok, message = check_db_connection()
    status = 200 if ok else 503
    return jsonify({"ok": ok, "message": message}), status

if __name__ == "__main__":
    app.run(debug=True)
