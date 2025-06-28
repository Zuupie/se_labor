from models.database_manager import create_connection

def add_user(name, email):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
    except Exception as e:
        print("Fehler beim Einfügen:", e)
    finally:
        conn.close()

def get_all_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users
