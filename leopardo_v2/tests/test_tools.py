import unittest
import os
import sqlite3
from ..app.features.tools.sub_pages.watermark_widget import MediaProcessor
from ..app.features.tools.sub_pages.links_widget import DatabaseManager

class TestTools(unittest.TestCase):

    def setUp(self):
        self.db_path = 'test_tools.db'
        self.db = DatabaseManager()
        self.db.conn = sqlite3.connect(self.db_path)
        self.db.create_tables()

    def tearDown(self):
        self.db.conn.close()
        os.remove(self.db_path)

    def test_add_category(self):
        self.db.add_category('Test Category')
        categories = self.db.get_categories()
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0][1], 'Test Category')

    def test_add_link(self):
        self.db.add_category('Test Category')
        cat_id = self.db.get_categories()[0][0]
        self.db.add_link('Test Link', 'http://test.com', cat_id)
        links = self.db.get_links_by_category(cat_id)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0][1], 'Test Link')

if __name__ == '__main__':
    unittest.main()
