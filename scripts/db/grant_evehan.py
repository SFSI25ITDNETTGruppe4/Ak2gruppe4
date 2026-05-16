import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME", "varehusdb"),
)

target_user = os.getenv("GRANT_TARGET_USER")
target_password = os.getenv("GRANT_TARGET_PASSWORD")
target_database = os.getenv("GRANT_TARGET_DATABASE", os.getenv("DB_NAME", "varehusdb"))

if not target_user or not target_password:
    raise SystemExit(
        "Missing GRANT_TARGET_USER or GRANT_TARGET_PASSWORD in environment."
    )

try:
    with conn.cursor() as cur:
        if "'" in target_user or "`" in target_user:
            raise ValueError("Invalid characters in GRANT_TARGET_USER")

        escaped_password = target_password.replace("\\", "\\\\").replace("'", "\\'")
        cur.execute(
            f"CREATE USER IF NOT EXISTS '{target_user}'@'%' IDENTIFIED BY '{escaped_password}'"
        )
        cur.execute(
            f"ALTER USER '{target_user}'@'%' IDENTIFIED BY '{escaped_password}'"
        )
        cur.execute(
            f"GRANT ALL PRIVILEGES ON `{target_database}`.* TO '{target_user}'@'%'"
        )
        cur.execute("FLUSH PRIVILEGES")
    conn.commit()
    print(f"Grants updated for {target_user}@%")
finally:
    conn.close()
