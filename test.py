import customtkinter
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database="varehusdb"
    )

try:
    conn = get_connection()
    cursor = conn.cursor()

    # Correct SQL syntax
    cursor.execute("SELECT * FROM kunde")

    results = cursor.fetchall()
    print(results)

    cursor.close()
    conn.close()

except mysql.connector.Error as err:
    print(f"Error: {err}")

"""
def button_callback():
    print("button pressed")

app = customtkinter.CTk()
app.title("my app")
app.geometry("400x150")

button = customtkinter.CTkButton(app, text="my button", command=button_callback)
button.grid(row=0, column=0, padx=20, pady=20)

app.mainloop()
"""