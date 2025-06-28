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

def write_category(kategorie, budget=0.0):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO category (kategorie, budget) VALUES (?, ?)", (kategorie, budget))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Kategorie '{kategorie}' existiert bereits.")
    except Exception as e:
        print("Fehler beim Einfügen der Kategorie:", e)
    finally:
        conn.close()

def category_exists(kategorie):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM category WHERE kategorie = ?", (kategorie,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

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

def get_all_balances():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM balance")
    balances = cursor.fetchall()
    conn.close()
    return balances

def get_balance_by_month(month):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM balance WHERE monat = ?", (month))
    balance = cursor.fetchone()
    conn.close()
    return balance

def write_balance(monat, bilanz):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO balance (monat, bilanz)
            VALUES (?, ?)
            ON CONFLICT(monat)
            DO UPDATE SET bilanz = excluded.bilanz
        """, (monat, bilanz))
        conn.commit()
        print(f"Bilanz für {monat} wurde geschrieben oder aktualisiert.")
    except Exception as e:
        print("Fehler beim Schreiben der Bilanz:", e)
    finally:
        conn.close()


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
    # Tabelle "balance" erstellen
    cursor.execute("""       
    CREATE TABLE balance (
        monat TEXT PRIMARY KEY,
        bilanz DOUBLE NOT NULL DEFAULT 0.0
    );
    """)

    conn.commit()
    conn.close()
    print("Neue Datenbank mit Tabellen wurden erstellt.")

if __name__ == "__main__":
    setup_database()
