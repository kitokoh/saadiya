import unittest
import pandas as pd
import os
from leopardo_v2.app.features.dms.dms_model import DmsModel
from leopardo_v2.app.core.database import get_db_path

class TestDmsModel(unittest.TestCase):

    def setUp(self):
        self.db_path = get_db_path()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.model = DmsModel()
        self.model._create_table_if_not_exists()
        self.model._load_initial_data()

    def test_get_documents(self):
        documents = self.model.get_documents()
        self.assertIsInstance(documents, pd.DataFrame)
        self.assertEqual(len(documents), 2)

    def test_add_document(self):
        self.model.add_document("Test Document", "Test", "/path/to/test.pdf")
        documents = self.model.get_documents()
        self.assertEqual(len(documents), 3)
        self.assertEqual(documents.iloc[-1]['title'], "Test Document")

    def test_update_document(self):
        self.model.update_document(0, "Quote 1 Updated", "Quote", "/path/to/quote1_updated.pdf")
        documents = self.model.get_documents()
        self.assertEqual(documents.iloc[0]['title'], "Quote 1 Updated")

    def test_delete_document(self):
        self.model.delete_document(0)
        documents = self.model.get_documents()
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents.iloc[0]['title'], "Contract A")

if __name__ == '__main__':
    unittest.main()
