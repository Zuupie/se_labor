from models.system_operation_add import add_entry
from models.database_manager import remove_database, setup_database, get_all_entries, get_all_categories, write_category, get_all_balances, write_balance
from models.state_machine import initialize_state_machine
import unittest
from models.system_operation_add import add_entry

class Test_add_entry(unittest.TestCase):
    def setup(self):
        # Initialisierung der Datenbank
        setup_database()

        # Initialisierung der Zustandsmaschine
        initialize_state_machine()
        write_category("Essen", 100.0)
        write_category("Transport", 50.0)

    def setup_sm_only(self):
        remove_database()
        initialize_state_machine()

    def test_add_entry_valid(self):
        self.setup()
        status = add_entry("Tomaten", 20, "2023-10-02", "Essen")
        self.assertEqual(status, 200)

    def test_add_entry_invalid_name(self):
        self.setup()
        status = add_entry("", 2000, None, "Essen")
        self.assertEqual(status, 401)

    def test_add_entry_invalid_name2(self):
        self.setup()
        status = add_entry(None, 2000, None, "Essen")
        self.assertEqual(status, 401)

    def test_add_entry_invalid_name3(self):
        self.setup()
        status = add_entry(2, 2000, None, "Essen")
        self.assertEqual(status, 401)

    def test_add_entry_invalid_amount(self):
        self.setup()
        status = add_entry("Steak", "abc", None, "Essen")
        self.assertEqual(status, 402)

    def test_add_entry_invalid_amount2(self):
        self.setup()
        status = add_entry("Steak", "", None, "Essen")
        self.assertEqual(status, 402)

    def test_add_entry_invalid_amount3(self):
        self.setup()
        status = add_entry("Steak", None, None, "Essen")
        self.assertEqual(status, 402)

    def test_add_entry_db_write_fail(self):
        self.setup_sm_only()
        status = add_entry("Steak", 1, None, "Essen")
        self.assertEqual(status, 405)


if __name__ == '__main__':
    unittest.main()

