import sqlite3
import os

DB_PATH = os.path.join("database", "data.db")

def create_connection():
    return sqlite3.connect(DB_PATH)

def setup_database():
    # Bestehende Datenbankdatei löschen (optional)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Alte Datenbank gelöscht.")

    conn = create_connection()
    cursor = conn.cursor()

    # Neue Tabelle anlegen
    cursor.execute("""
    CREATE TABLE entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        betrag DOUBLE NOT NULL,
        datum TEXT NOT NULL,
        kategorie TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()
    print("Neue Datenbank mit Tabelle wurden erstellt.")

if __name__ == "__main__":
    setup_database()
