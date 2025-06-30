import sqlite3
import os

DB_PATH = os.path.join("database", "data.db")

def create_connection():
    return sqlite3.connect(DB_PATH)

# Schreibt einen Eintrag in die Datenbank
def write_entry(name, betrag, datum, kategorie):
    conn = create_connection()
    cursor = conn.cursor()
    status = 200
    try:
        cursor.execute("INSERT INTO entries (name, betrag, datum, kategorie) VALUES (?, ?, ?, ?)", (name, betrag, datum, kategorie))
        conn.commit()
    except Exception as e:
        print("Fehler beim Einfügen:", e)
        status = 405
    finally:
        conn.close()
        return status

# Kategorie mit Budget schreiben oder aktualisieren
def write_category(kategorie, budget=100.0):
    conn = create_connection()
    cursor = conn.cursor()
    status = 200
    try:
        cursor.execute("""
            INSERT INTO category (kategorie, budget) 
            VALUES (?, ?)
            ON CONFLICT(kategorie)
            DO UPDATE SET budget = excluded.budget
        """, (kategorie, budget))
        conn.commit()
    except Exception as e:
        print("Fehler beim Einfügen der Kategorie:", e)
        status = 405
    finally:
        conn.close()
        return status

# Schreibt oder aktualisiert die Bilanz für einen bestimmten Monat
def write_balance(monat, bilanz):
    conn = create_connection()
    cursor = conn.cursor()
    status = 200
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
        status = 405
    finally:
        conn.close()
        return status

# Überprüft, ob eine Kategorie in der Datenbank existiert
def category_exists(kategorie):
    conn = create_connection()
    cursor = conn.cursor()
    status = 200
    result = None
    try:
        cursor.execute("SELECT 1 FROM category WHERE kategorie = ?", (kategorie,))
        result = cursor.fetchone()
    except Exception as e:
        print("Fehler beim lesen der Kategorie:", e)
        status = 405
    finally:
        conn.close()
        return status, result is not None

def get_category_budget(kategorie):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT budget FROM category WHERE kategorie = ?", (kategorie,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Ruft alle Einträge aus der Datenbank ab
def get_all_entries():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries")
    entries = cursor.fetchall()
    conn.close()
    return entries

# Ruft alle Kategorien aus der Datenbank ab
def get_all_categories():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM category")
    categories = cursor.fetchall()
    conn.close()
    return categories

# Ruft alle Bilanzen aus der Datenbank ab
def get_all_balances():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM balance")
    balances = cursor.fetchall()
    conn.close()
    return balances

# Ruft die Bilanz für einen bestimmten Monat ab
def get_balance_by_month(month):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM balance WHERE monat = ?", (month))
    balance = cursor.fetchone()
    conn.close()
    return balance


# Erstellt die Datenbank und die erforderlichen Tabellen
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

def remove_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Alte Datenbank gelöscht.")

if __name__ == "__main__":
    setup_database()
