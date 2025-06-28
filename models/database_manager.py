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
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    );
    """)

    conn.commit()
    conn.close()
    print("Neue Datenbank mit Tabelle wurden erstellt.")

if __name__ == "__main__":
    setup_database()
