import unittest
import pandas as pd
import os
from leopardo_v2.app.features.crm.crm_model import CrmModel
from leopardo_v2.app.core.database import get_db_path

class TestCrmModel(unittest.TestCase):

    def setUp(self):
        self.db_path = get_db_path()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.model = CrmModel()
        self.model._create_table_if_not_exists()
        self.model._load_initial_data()


    def test_get_customers(self):
        customers = self.model.get_customers()
        self.assertIsInstance(customers, pd.DataFrame)
        self.assertEqual(len(customers), 2)

    def test_add_customer(self):
        self.model.add_customer("Test Customer", "test@example.com", "1234567890", "Lead")
        customers = self.model.get_customers()
        self.assertEqual(len(customers), 3)
        self.assertEqual(customers.iloc[-1]['name'], "Test Customer")

    def test_update_customer(self):
        self.model.update_customer(0, "Customer A Updated", "customer.a.updated@example.com", "111-111-1111", "Contacted")
        customers = self.model.get_customers()
        self.assertEqual(customers.iloc[0]['name'], "Customer A Updated")

    def test_delete_customer(self):
        self.model.delete_customer(0)
        customers = self.model.get_customers()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers.iloc[0]['name'], "Customer B")

if __name__ == '__main__':
    unittest.main()
