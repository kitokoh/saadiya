import unittest
import pandas as pd
import os
from leopardo_v2.app.features.my_groups.my_groups_model import MyGroupsModel
from leopardo_v2.app.core.database import get_db_path

class TestMyGroupsModel(unittest.TestCase):

    def setUp(self):
        self.db_path = get_db_path()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.model = MyGroupsModel()
        self.model._create_table_if_not_exists()
        self.model._load_initial_data()

    def test_get_groups(self):
        groups = self.model.get_groups()
        self.assertIsInstance(groups, pd.DataFrame)
        self.assertEqual(len(groups), 0)

    def test_add_group(self):
        self.model.add_group("Test Group", "A test group")
        groups = self.model.get_groups()
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups.iloc[-1]['name'], "Test Group")

    def test_update_group(self):
        self.model.add_group("Test Group", "A test group")
        self.model.update_group(0, "Test Group Updated", "An updated test group")
        groups = self.model.get_groups()
        self.assertEqual(groups.iloc[0]['name'], "Test Group Updated")

    def test_delete_group(self):
        self.model.add_group("Test Group", "A test group")
        self.model.delete_group(0)
        groups = self.model.get_groups()
        self.assertEqual(len(groups), 0)

if __name__ == '__main__':
    unittest.main()
