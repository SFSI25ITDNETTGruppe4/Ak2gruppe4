import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME", "varehusdb")

print(f"Connecting to {host} as {user} on {database}...")

conn = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    cursorclass=pymysql.cursors.DictCursor,
)

try:
    with conn.cursor() as cur:
        print("Dropping existing procedure if it exists...")
        cur.execute("DROP PROCEDURE IF EXISTS sp_list_kunder")

        print("Creating procedure sp_list_kunder...")
        cur.execute(
            """
            CREATE PROCEDURE sp_list_kunder()
            BEGIN
                SELECT k.KNr,
                       CONCAT(k.Fornavn, ' ', k.Etternavn) AS Navn,
                       k.Adresse,
                       k.PostNr AS Postnummer,
                       p.Poststed AS `By`
                FROM kunde k
                LEFT JOIN poststed p ON k.PostNr = p.PostNr
                ORDER BY Navn ASC;
            END
            """
        )

        print("Verifying procedure call...")
        cur.callproc("sp_list_kunder")
        rows = cur.fetchall()
        print(f"Procedure works. Returned {len(rows)} rows.")

    conn.commit()
    print("Setup completed successfully.")
finally:
    conn.close()
