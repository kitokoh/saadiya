import unittest
import pandas as pd
import os
from leopardo_v2.app.features.project_management.project_management_model import ProjectManagementModel
from leopardo_v2.app.core.database import get_db_path

class TestProjectManagementModel(unittest.TestCase):

    def setUp(self):
        self.db_path = get_db_path()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.model = ProjectManagementModel()
        self.model._create_table_if_not_exists()
        self.model._load_initial_data()

    def test_get_projects(self):
        projects = self.model.get_projects()
        self.assertIsInstance(projects, pd.DataFrame)
        self.assertEqual(len(projects), 2)

    def test_add_project(self):
        self.model.add_project("Test Project", "A test project", "In Progress")
        projects = self.model.get_projects()
        self.assertEqual(len(projects), 3)
        self.assertEqual(projects.iloc[-1]['name'], "Test Project")

    def test_update_project(self):
        self.model.update_project(0, "Project Alpha Updated", "The updated first project", "Completed")
        projects = self.model.get_projects()
        self.assertEqual(projects.iloc[0]['name'], "Project Alpha Updated")

    def test_delete_project(self):
        self.model.delete_project(0)
        projects = self.model.get_projects()
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects.iloc[0]['name'], "Project Beta")

if __name__ == '__main__':
    unittest.main()
