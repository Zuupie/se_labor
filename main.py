from models.system_operation_add import add_entry
from models.database_manager import setup_database, get_all_entries, get_all_categories

# Initialisierung der Datenbank
setup_database()

name = ""
# Eintrag hinzufügen
add_entry("Tomaten", 20.5, "2023-10-02", "Essen")
#add_entry("Taxi", 15.0, "2023-10-02", "Transport")
#add_entry("Tennis", 30.0, "2023-10-03", "Freizeit")
#add_entry("Döner", 25.0, "2023-10-04", "Essen")


# Alle Einträge anzeigen
print("---------------- Alle Einträge -----------------")
entries = get_all_entries()
for entry in entries:
    print(entry)

# Alle Kategorien anzeigen
print("---------------- Alle Kategorien -----------------")
categories = get_all_categories()
for category in categories:
    print(category)
