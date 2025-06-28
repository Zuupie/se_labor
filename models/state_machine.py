def initialize_state_machine():
    global current_state
    current_state = "keinen Eintrag"
    print("Zustandsmaschine initialisiert. Aktueller Zustand:", current_state)

def change_state(new_state):
    global current_state
    print(f"Zustandswechsel von '{current_state}' zu '{new_state}'")
    current_state = new_state

def get_current_state():
    return current_state