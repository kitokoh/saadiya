import os
import sqlite3
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox

class EditInstanceDialog(QDialog):
    def __init__(self, instance, parent=None):
        super().__init__(parent)
        self.instance = instance
        self.setWindowTitle(self.tr("Éditer Instance"))
        self.layout = QFormLayout(self)

        # Champs d'édition
        self.name_field = QLineEdit(instance['name'])
        self.description_field = QLineEdit(instance['description'])
        self.user_field = QLineEdit(instance['user'])
        self.expire_date_field = QLineEdit(instance['expire_date'])

        self.layout.addRow(self.tr("Nom :"), self.name_field)
        self.layout.addRow(self.tr("Description :"), self.description_field)
        self.layout.addRow(self.tr("Utilisateur :"), self.user_field)
        self.layout.addRow(self.tr("Date d'expiration :"), self.expire_date_field)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def get_instance_data(self):
        return {
            "name": self.name_field.text(),
            "description": self.description_field.text(),
            "user": self.user_field.text(),
            "expire_date": self.expire_date_field.text()
        }
