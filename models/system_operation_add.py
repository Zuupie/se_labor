from models.database_manager import write_entry, write_category, write_balance, category_exists, get_category_budget, get_all_entries
from datetime import datetime
from models.state_machine import change_state, get_current_state

def add_entry(name, betrag, datum, kategorie):
    status, datum = validate_entry(name, betrag, datum, kategorie)
    match status:
        case 401:
            print("Ungültiger Name:", name)
            return
        case 402:
            print("Ungültiger Betrag:", betrag)
            return
        case 200:
            print("Eintrag ist gültig:", name, betrag, datum, kategorie)
    #Zustandswechsel, falls noch kein Eintrag existiert
    if get_current_state() == "keinen Eintrag":
        change_state("Einen Eintrag") 
    # Eintrag ist gültig, also schreibe ihn in die Datenbank
    write_entry(name, betrag, datum, kategorie)
    print(f"Eintrag '{name}' mit Betrag {betrag} am {datum} in Kategorie '{kategorie}' wurde hinzugefügt.")
    # und aktualisiere die Bilanz für den Monat............
    

def get_current_date():
    # Gibt das aktuelle Datum im Format YYYY-MM-DD zurück
    return datetime.now().strftime("%Y-%m-%d")


def validate_entry(name, betrag, datum, kategorie):
    print("Validating entry:", name, betrag, datum, kategorie)
    if name is None or len(name) == 0:
        return 401, datum 
    elif betrag is None or not isinstance(betrag, (int, float)):
        return 402, datum
    elif datum is None or len(datum) == 0:
        datum = get_current_date()
        print("Datum wurde nicht angegeben, verwende aktuelles Datum:", datum)

    if category_exists(kategorie):
        print(f"Kategorie '{kategorie}' existiert.")
        #Budget für die Kategorie abrufen
        budget = get_category_budget(kategorie)
        print(f"Altes Budget für Kategorie '{kategorie}': {budget}")
        #Budget aktualisieren
        new_budget = budget - betrag
        write_category(kategorie, new_budget)
        if new_budget < 0:
            print(f"Warnung: Budget für Kategorie '{kategorie}' wird negativ ({new_budget}).")
        else:
            print(f"Neues Budget für Kategorie '{kategorie}': {new_budget}")
    else:
        # Kategorie existiert nicht, also erstellen (mit default Budget von 100.0)
        print(f"Kategorie '{kategorie}' wurde nicht gefunden.")
        write_category(kategorie)
        print(f"Kategorie '{kategorie}' wurde erstellt.")

    return 200, datum