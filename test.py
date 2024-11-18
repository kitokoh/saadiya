from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QApplication
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import sys


class PromptDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr("Créer un Prompt"))
        self.setMinimumSize(600, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 15px;
                border: 2px solid #E4E7EB;
                padding: 15px;
                box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.1);
            }
        """)
        self.init_ui()

    def init_ui(self):
        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Titre principal
        title = QLabel(self.tr("💡 Rédigez un Prompt Unique"))
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                color: #2C3E50;
                margin-bottom: 5px;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Sous-titre subtil
        subtitle = QLabel(self.tr("Décrivez vos idées avec précision et créativité."))
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setStyleSheet("""
            QLabel {
                color: #7F8C8D;
            }
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # Zone de texte pour le prompt
        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText(self.tr("Commencez à écrire ici..."))
        self.text_input.setStyleSheet("""
            QTextEdit {
                background-color: #F9FAFB;
                border: 2px solid #E4E7EB;
                border-radius: 10px;
                padding: 12px;
                font-size: 16px;
                color: #34495E;
                transition: border-color 0.3s ease;
            }
            QTextEdit:focus {
                border-color: #3498DB;
            }
        """)
        layout.addWidget(self.text_input)

        # Boutons d'action en bas
        button_layout = QHBoxLayout()

        # Bouton Annuler
        cancel_button = QPushButton(QIcon("icons/cancel.png"), self.tr("Annuler"))
        cancel_button.setShortcut("Esc")  # Raccourci pour annuler
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        # Bouton Envoyer
        self.submit_button = QPushButton(QIcon("icons/send.png"), self.tr("Envoyer"))
        self.submit_button.setEnabled(False)  # Désactivé par défaut
        self.submit_button.setShortcut("Ctrl+Return")  # Raccourci pour envoyer
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                box-shadow: 0px 5px 15px rgba(52, 152, 219, 0.4);
                transition: background-color 0.3s ease, box-shadow 0.3s ease;
            }
            QPushButton:hover {
                background-color: #2980B9;
                box-shadow: 0px 8px 20px rgba(41, 128, 185, 0.6);
            }
            QPushButton:disabled {
                background-color: #BDC3C7;
                color: #ECF0F1;
                box-shadow: none;
            }
        """)
        self.submit_button.clicked.connect(self.submit_prompt)
        button_layout.addWidget(self.submit_button)

        layout.addLayout(button_layout)

        # Vérification si la zone de texte est remplie
        self.text_input.textChanged.connect(self.check_input)

        self.setLayout(layout)

    def check_input(self):
        """Active le bouton 'Envoyer' seulement si la zone de texte n'est pas vide."""
        self.submit_button.setEnabled(bool(self.text_input.toPlainText().strip()))

    def submit_prompt(self):
        """Ferme la boîte de dialogue et retourne le texte."""
        self.accept()

    def get_prompt(self):
        """Retourne le texte écrit par l'utilisateur."""
        return self.text_input.toPlainText().strip()


# Exemple d'utilisation
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = PromptDialog()
    if dialog.exec_() == QDialog.Accepted:
        print(dialog.tr("Prompt soumis :"), dialog.get_prompt())
    sys.exit(app.exec_())
