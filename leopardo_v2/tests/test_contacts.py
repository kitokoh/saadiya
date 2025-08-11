import unittest
import pandas as pd
from leopardo_v2.app.features.contacts.contacts_model import ContactsModel

class TestContactsModel(unittest.TestCase):

    def setUp(self):
        self.model = ContactsModel()

    def test_get_contacts(self):
        contacts = self.model.get_contacts()
        self.assertIsInstance(contacts, pd.DataFrame)
        self.assertEqual(len(contacts), 2)

    def test_add_contact(self):
        self.model.add_contact("Test User", "test@example.com", "1234567890")
        contacts = self.model.get_contacts()
        self.assertEqual(len(contacts), 3)
        self.assertEqual(contacts.iloc[-1]['Name'], "Test User")

    def test_update_contact(self):
        self.model.update_contact(0, "John Doe Updated", "john.doe.updated@example.com", "111-111-1111")
        contacts = self.model.get_contacts()
        self.assertEqual(contacts.iloc[0]['Name'], "John Doe Updated")

    def test_delete_contact(self):
        self.model.delete_contact(0)
        contacts = self.model.get_contacts()
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts.iloc[0]['Name'], "Jane Smith")

if __name__ == '__main__':
    unittest.main()
