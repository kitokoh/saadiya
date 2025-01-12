import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QFrame

from licenceYonetimi.validatelicens import LicenseValidator


def get_serial_number():
    """Essaie de récupérer le numéro de série via différentes méthodes."""
    try:
        serial_number = os.popen("wmic bios get serialnumber").read().strip().split("\n")[1].strip()
        if serial_number:
            return serial_number
    except IndexError:
        pass
    
    try:
        serial_number = os.popen("powershell (Get-WmiObject win32_bios).SerialNumber").read().strip()
        return serial_number
    except IndexError:
        print("Erreur : Impossible de récupérer le numéro de série via PowerShell.")
        return None
def get_windows_username():
    """Récupère le nom de l'utilisateur Windows courant."""
    try:
        # Méthode 1 : Utiliser os.getlogin()
        username = os.getlogin()
        if username:
            return username
    except Exception as e:
        print(f"Erreur avec os.getlogin() : {e}")

    try:
        # Méthode 2 : Utiliser la variable d'environnement USERNAME
        username = os.getenv("USERNAME")
        if username:
            return username
    except Exception as e:
        print(f"Erreur avec os.getenv() : {e}")

    print("Erreur : Impossible de récupérer le nom d'utilisateur.")
    return None

def get_subfolders(directory_path):
    """Retourne la liste des sous-dossiers directs d'un dossier donné."""
    try:
        # Vérifie si le chemin existe et est un dossier
        if not os.path.isdir(directory_path):
            print(f"Le chemin spécifié n'est pas un dossier : {directory_path}")
            return []

        # Récupère les sous-dossiers
        subfolders = [name for name in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, name))]
        return subfolders
    except Exception as e:
        print(f"Erreur lors de la récupération des sous-dossiers : {e}")
        return []
class UpdateLicenseDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Configurer la fenêtre
        self.setWindowTitle(self.tr("Mise à jour de votre licence Nova360 AI"))
        self.setFixedSize(450, 300)
        self.setStyleSheet("background-color: #f0f0f0;")

        # Initialize LicenseValidator
        self.validator = LicenseValidator()

        # Disposition principale
        layout = QVBoxLayout()

        # Conteneur de fond
        frame = QFrame(self)
        frame.setStyleSheet("background-color: #ffffff; border-radius: 10px; padding: 20px;")
        frame_layout = QVBoxLayout(frame)

        # Titre et sous-titre
        title = QLabel(self.tr("Activation de votre licence"))
        title.setStyleSheet("font-weight: bold; font-size: 16px; color: #333333;")
        frame_layout.addWidget(title)

        subtitle = QLabel(self.tr("Veuillez coller le code de licence envoyé par email pour activer toutes les fonctionnalités :"))
        subtitle.setStyleSheet("font-size: 13px; color: #555555; margin-bottom: 10px;")
        frame_layout.addWidget(subtitle)

        # Champ de saisie du code de licence
        self.license_input = QLineEdit(self)
        self.license_input.setPlaceholderText("XXXXX-XXXXX-XXXXX-XXXXX-XXXXX-XXXXX")
        self.license_input.setStyleSheet("padding: 10px; font-size: 12px; border: 1px solid #ccc; border-radius: 5px;")
        frame_layout.addWidget(self.license_input)

        # Bouton pour valider la licence
        validate_btn = QPushButton(self.tr("Valider la licence"))
        validate_btn.setStyleSheet("background-color: #007BFF; color: white; padding: 10px; border: none; border-radius: 5px; font-weight: bold;")
        validate_btn.clicked.connect(self.validate_license)
        frame_layout.addWidget(validate_btn)

        # Ajouter le conteneur au layout principal
        layout.addWidget(frame)
        self.setLayout(layout)

    def validate_license(self):
        """Valide et met à jour la licence avec LicenseValidator."""
        license_code = self.license_input.text().strip()

        if not license_code:
            QMessageBox.warning(self, "Erreur de validation", "Veuillez entrer un code de licence valide.", QMessageBox.Ok)
            return

        if not self.validator.validate_license(license_code):
            QMessageBox.warning(self, "Licence invalide", "Le code de licence fourni est incorrect ou expiré.", QMessageBox.Ok)
            return

        try:
            # Met à jour le fichier python.txt avec la nouvelle licence
            self.validator.update_python_file(license_code)
            QMessageBox.information(self, "Mise à jour réussie", "Votre licence a été mise à jour avec succès. Vous pouvez désormais utiliser toutes les fonctionnalités.", QMessageBox.Ok)
            self.clear_fields()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur système", f"Une erreur est survenue lors de la mise à jour de la licence : {e}", QMessageBox.Ok)

    def clear_fields(self):
        """Efface le champ de saisie."""
        self.license_input.clear()
