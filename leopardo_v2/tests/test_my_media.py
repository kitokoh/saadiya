import unittest
import pandas as pd
import os
from leopardo_v2.app.features.my_media.my_media_model import MyMediaModel
from leopardo_v2.app.core.database import get_db_path

class TestMyMediaModel(unittest.TestCase):

    def setUp(self):
        self.db_path = get_db_path()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.model = MyMediaModel()
        self.model._create_table_if_not_exists()
        self.model._load_initial_data()

    def test_get_media(self):
        media = self.model.get_media()
        self.assertIsInstance(media, pd.DataFrame)
        self.assertEqual(len(media), 0)

    def test_add_media(self):
        self.model.add_media("Test Media", "Image", "/path/to/test.jpg")
        media = self.model.get_media()
        self.assertEqual(len(media), 1)
        self.assertEqual(media.iloc[-1]['title'], "Test Media")

    def test_update_media(self):
        self.model.add_media("Test Media", "Image", "/path/to/test.jpg")
        self.model.update_media(0, "Test Media Updated", "Image", "/path/to/test_updated.jpg")
        media = self.model.get_media()
        self.assertEqual(media.iloc[0]['title'], "Test Media Updated")

    def test_delete_media(self):
        self.model.add_media("Test Media", "Image", "/path/to/test.jpg")
        self.model.delete_media(0)
        media = self.model.get_media()
        self.assertEqual(len(media), 0)

if __name__ == '__main__':
    unittest.main()
