import os

from flask import Flask, render_template

app = Flask(__name__)


def get_db_config():
    return {
        "host": os.getenv(
            "DB_HOST",
            "varehusdb.cf6um6awm1jz.eu-north-1.rds.amazonaws.com",
        ),
        "user": os.getenv("DB_USER", ""),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "varehusdb"),
    }


app.config["DB_CONFIG"] = get_db_config()

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
