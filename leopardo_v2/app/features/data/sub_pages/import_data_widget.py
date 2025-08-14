import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog)

class ImportDataWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.import_contacts_button = QPushButton("Import Contacts")
        self.import_contacts_button.clicked.connect(lambda: self.import_data("Contacts"))
        layout.addWidget(self.import_contacts_button)

        self.import_groups_button = QPushButton("Import Groups")
        self.import_groups_button.clicked.connect(lambda: self.import_data("Groups"))
        layout.addWidget(self.import_groups_button)

        self.import_media_button = QPushButton("Import Media")
        self.import_media_button.clicked.connect(lambda: self.import_data("Media"))
        layout.addWidget(self.import_media_button)

    def import_data(self, data_type):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, f"Import {data_type}", "",
                                                  "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            print(f"Importing {data_type} from: {file_name}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = ImportDataWidget()
    widget.show()
    sys.exit(app.exec_())
