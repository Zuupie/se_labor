import sqlite3
import os

DB_PATH = os.path.join("database", "data.db")

def create_connection():
    return sqlite3.connect(DB_PATH)

def write_entry(name, betrag, datum, kategorie):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO entries (name, betrag, datum, kategorie) VALUES (?, ?, ?, ?)", (name, betrag, datum, kategorie))
        conn.commit()
    except Exception as e:
        print("Fehler beim Einfügen:", e)
    finally:
        conn.close()

def get_all_entries():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries")
    entries = cursor.fetchall()
    conn.close()
    return entries

def get_all_categories():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM category")
    categories = cursor.fetchall()
    conn.close()
    return categories

def setup_database():
    # Bestehende Datenbankdatei löschen (optional)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Alte Datenbank gelöscht.")

    conn = create_connection()
    cursor = conn.cursor()

    # Tabelle "entries" erstellen
    cursor.execute("""
    CREATE TABLE entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        betrag DOUBLE NOT NULL,
        datum TEXT NOT NULL,
        kategorie TEXT NOT NULL
            REFERENCES category(kategorie) ON DELETE CASCADE
                ON UPDATE CASCADE
    );
    """)
    # Tabelle "category" erstellen
    cursor.execute("""       
    CREATE TABLE category (
        kategorie TEXT PRIMARY KEY,
        budget DOUBLE NOT NULL DEFAULT 0.0
    );
    """)

    conn.commit()
    conn.close()
    print("Neue Datenbank mit Tabellen wurden erstellt.")

if __name__ == "__main__":
    setup_database()
