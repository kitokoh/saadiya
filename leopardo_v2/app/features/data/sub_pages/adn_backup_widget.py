import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox)

class AdnBackupWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.backup_button = QPushButton("Create ADN Backup")
        self.backup_button.clicked.connect(self.create_backup)
        layout.addWidget(self.backup_button)

    def create_backup(self):
        QMessageBox.information(self, "Backup Successful", "Your ADN data has been successfully backed up.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = AdnBackupWidget()
    widget.show()
    sys.exit(app.exec_())
