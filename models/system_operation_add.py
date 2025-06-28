from models.database_manager import write_entry
from datetime import datetime

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
    write_entry(name, betrag, datum, kategorie)
    

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
    return 200, datum