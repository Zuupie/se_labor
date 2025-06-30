from models.database_manager import write_entry, write_category, write_balance, category_exists, get_category_budget, get_all_entries
from datetime import datetime
from models.state_machine import change_state, get_current_state
from datetime import datetime

def add_entry(name, betrag, datum, kategorie):
    status, datum = validate_entry(name, betrag, datum, kategorie)
    match status:
        case 401:
            print("Ungültiger Name:", name)
            return 401
        case 402:
            print("Ungültiger Betrag:", betrag)
            return 402
        case 200:
            print("Eintrag ist gültig:", name, betrag, datum, kategorie)

    #Zustandswechsel, falls noch kein Eintrag existiert
    if get_current_state() == "keinen Eintrag":
        change_state("Einen Eintrag") 

    # Eintrag ist gültig, also schreibe ihn in die Datenbank
    db_antwort = write_entry(name, betrag, datum, kategorie)
    print(f"Eintrag '{name}' mit Betrag {betrag} am {datum} in Kategorie '{kategorie}' wurde hinzugefügt.")

    # Aktualisiere die Bilanz für den Monat des Eintrags
    if db_antwort == 200:
        recalculate_balance(datum, betrag)
    else:
        return db_antwort

    return status

def recalculate_balance(datum, betrag):
    # Datum im Format YYYY-MM extrahieren und dafür aus str Datum ein datetime Objekt machen
    dt = datetime.strptime(datum, "%Y-%m-%d")
    jahr_monat = dt.strftime("%Y-%m")
    
    # Alle Einträge für den Monat abrufen
    entries = get_all_entries()
    total = sum(entry[2] for entry in entries if entry[3].startswith(jahr_monat))

    # Bilanz schreiben oder aktualisieren
    write_balance(jahr_monat, total)
    print(f"Bilanz für {jahr_monat} wurde aktualisiert: {total}")

def get_current_date():
    # Gibt das aktuelle Datum im Format YYYY-MM-DD zurück
    return datetime.now().strftime("%Y-%m-%d")


def validate_entry(name, betrag, datum, kategorie):
    print("Validating entry:", name, betrag, datum, kategorie)

    if (not isinstance(name, str)) or name is None or len(name) == 0:
        return 401, datum 
    elif betrag is None or not isinstance(betrag, (int, float)):
        return 402, datum
    elif datum is None or len(datum) == 0:
        datum = get_current_date()
        print("Datum wurde nicht angegeben, verwende aktuelles Datum:", datum)

    status, kat_existiert = category_exists(kategorie)

    if status == 200 and kat_existiert:
        print(f"Kategorie '{kategorie}' existiert.")
        #Budget für die Kategorie abrufen
        budget = get_category_budget(kategorie)
        if not budget:
            return 405, datum
        print(f"Altes Budget für Kategorie '{kategorie}': {budget}")
        #Budget aktualisieren
        new_budget = budget - betrag
        write_category(kategorie, new_budget)
        if new_budget < 0:
            print(f"Warnung: Budget für Kategorie '{kategorie}' wird negativ ({new_budget}).")
        else:
            print(f"Neues Budget für Kategorie '{kategorie}': {new_budget}")
    elif status == 200 and not kat_existiert:
        # Kategorie existiert nicht, also erstellen (mit default Budget von 100.0)
        print(f"Kategorie '{kategorie}' wurde nicht gefunden.")
        write_category(kategorie)
        print(f"Kategorie '{kategorie}' wurde erstellt.")
    else:
        return 405, datum

    return 200, datum
