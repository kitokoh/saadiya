import unittest
import sys
from PyQt5.QtWidgets import QApplication
from leopardo_v2.app.features.content_generator.view import ContentGeneratorWidget
from leopardo_v2.app.core.database import DatabaseManager

class TestContentGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)

    def test_widget_creation(self):
        """
        Tests if the ContentGeneratorWidget can be created without errors.
        """
        try:
            db_manager = DatabaseManager()
            widget = ContentGeneratorWidget(db_manager)
            self.assertIsNotNone(widget)
        except Exception as e:
            self.fail(f"ContentGeneratorWidget creation failed with an exception: {e}")

if __name__ == '__main__':
    unittest.main()
