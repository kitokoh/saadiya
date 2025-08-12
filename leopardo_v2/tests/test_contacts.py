import unittest
import pandas as pd
import os
from leopardo_v2.app.features.contacts.contacts_model import ContactsModel
from leopardo_v2.app.core.database import get_db_path


class TestContactsModel(unittest.TestCase):

    def setUp(self):
        self.db_path = get_db_path()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.model = ContactsModel()
        self.model._create_table_if_not_exists()
        self.model.add_contact("John Doe", "john.doe@example.com", "123-456-7890")
        self.model.add_contact("Jane Smith", "jane.smith@example.com", "098-765-4321")



    def test_get_contacts(self):
        contacts = self.model.get_contacts()
        self.assertIsInstance(contacts, pd.DataFrame)
        self.assertEqual(len(contacts), 2)

    def test_add_contact(self):
        self.model.add_contact("Test User", "test@example.com", "1234567890")
        contacts = self.model.get_contacts()
        self.assertEqual(len(contacts), 3)
        self.assertEqual(contacts.iloc[-1]['name'], "Test User")


    def test_update_contact(self):
        self.model.update_contact(0, "John Doe Updated", "john.doe.updated@example.com", "111-111-1111")
        contacts = self.model.get_contacts()
        self.assertEqual(contacts.iloc[0]['name'], "John Doe Updated")


    def test_delete_contact(self):
        self.model.delete_contact(0)
        contacts = self.model.get_contacts()
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts.iloc[0]['name'], "Jane Smith")


if __name__ == '__main__':
    unittest.main()
