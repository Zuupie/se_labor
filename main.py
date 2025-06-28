from models.system_operation_add import add_user, get_all_users

# Benutzer hinzufügen
add_user("Alice", "alice@example.com")
add_user("Bob", "bob@example.com")

# Alle Benutzer anzeigen
users = get_all_users()
for user in users:
    print(user)
