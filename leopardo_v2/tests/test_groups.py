import unittest
import pandas as pd
import os
from leopardo_v2.app.features.groups.groups_model import GroupsModel
from leopardo_v2.app.core.database import get_db_path

class TestGroupsModel(unittest.TestCase):

    def setUp(self):
        self.db_path = get_db_path()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.model = GroupsModel()

    def test_get_groups(self):
        groups = self.model.get_groups()
        self.assertIsInstance(groups, pd.DataFrame)
        self.assertEqual(len(groups), 2)

    def test_add_group(self):
        self.model.add_group("Test Group", "A test group")
        groups = self.model.get_groups()
        self.assertEqual(len(groups), 3)
        self.assertEqual(groups.iloc[-1]['name'], "Test Group")

    def test_update_group(self):
        self.model.update_group(0, "Marketing Team Updated", "The updated marketing team")
        groups = self.model.get_groups()
        self.assertEqual(groups.iloc[0]['name'], "Marketing Team Updated")

    def test_delete_group(self):
        self.model.delete_group(0)
        groups = self.model.get_groups()
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups.iloc[0]['name'], "Sales Team")

if __name__ == '__main__':
    unittest.main()
