from models.system_operation_add import add_entry, get_all_entries
from models.database_manager import setup_database

# Initialisierung der Datenbank
setup_database()

# Eintrag hinzufügen
add_entry("Tomaten", 20.5, "2023-10-01", "Essen")
add_entry("Taxi", 15.0, "2023-10-02", "Transport")
add_entry("Tennis", 30.0, "2023-10-03", "Freizeit")
add_entry("Döner", 25.0, "2023-10-04", "Essen")


# Alle Einträge anzeigen
entries = get_all_entries()
for entry in entries:
    print(entry)
