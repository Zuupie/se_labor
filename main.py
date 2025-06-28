from models.system_operation_add import add_entry
from models.database_manager import setup_database, get_all_entries, get_all_categories, write_category, get_all_balances, write_balance
from models.state_machine import initialize_state_machine

# Initialisierung der Datenbank
setup_database()

# Initialisierung der Zustandsmaschine
initialize_state_machine()

write_category("Essen", 100.0)
write_category("Transport", 50.0)

#write_balance("2023-10", 200.0)
#write_balance("2023-11", 150.0)
#write_balance("2023-11", 300.0)

# Eintrag hinzufügen
add_entry("Tomaten", 200.5, "2023-10-02", "Essen")
add_entry("Taxi", 15.0, "2023-10-02", "Transport")
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

# Alle Kategorien anzeigen
print("---------------- Alle Bilanzen -----------------")
balances = get_all_balances()
for balance in balances:
    print(balance)
