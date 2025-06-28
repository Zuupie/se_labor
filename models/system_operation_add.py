from models.database_manager import create_connection

def add_entry(name, betrag, datum, kategorie):
    match validate_entry(name, betrag, datum, kategorie):
        case 401:
            print("Ungültiger Name:", name)
            return
        case 402:
            print("Ungültiger Betrag:", betrag)
            return
        case 403:
            print("Ungültiges Datum:", datum)
            # get_datum()
        case 200:
            print("Eintrag ist gültig:", name, betrag, datum, kategorie)

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
    users = cursor.fetchall()
    conn.close()
    return users

# Muss noch implementiert werden
# Diese Funktion soll die Eingaben validieren und entsprechende Fehlercodes zurückgeben
def validate_entry(name, betrag, datum, kategorie):
    print("Validating entry:", name, betrag, datum, kategorie)
    return 200
