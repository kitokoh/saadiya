import sys
import subprocess
from PyQt5 import QtWidgets, QtCore

class MultiLangApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Translations dictionary
        self.translations = {
            'TR': {
                'welcome': 'Yönetim Uygulamasına Hoş Geldiniz',
                'check_admin': 'Bu komut dosyası yönetici olarak çalıştırılmalıdır.',
                'menu_start': 'Menu başarıyla başlatıldı.',
                'menu_error': 'Menu dosyası bulunamadı! Lütfen "menu.exe" dosyasını kontrol edin.',
                # Add more translations...
                'success': 'İşlem başarılı!',
                'error': 'Hata oluştu!',
                'completion': 'Tüm işlemler başarıyla tamamlandı.',
            },
            'FR': {
                'welcome': 'Bienvenue dans l\'application de gestion',
                'check_admin': 'Ce script doit être exécuté en tant qu\'administrateur.',
                'menu_start': 'Menu démarré avec succès.',
                'menu_error': 'Le fichier de menu est introuvable ! Veuillez vérifier "menu.exe".',
                # Add more translations...
                'success': 'Opération réussie !',
                'error': 'Une erreur est survenue !',
                'completion': 'Tous les processus ont été complétés avec succès.',
            }
        }

        self.current_language = 'TR'  # Default language

        self.init_ui()

    def init_ui(self):
        # Create layout and buttons
        layout = QtWidgets.QVBoxLayout()

        self.status_label = QtWidgets.QLabel(self.translations[self.current_language]['welcome'])
        layout.addWidget(self.status_label)

        # List of operations
        self.operations = {
            'Menu': 'menu.exe',
            'Antivirus': 'blocAntivirus.exe',
            'Setup': 'setup.exe',
            # Add other operations...
        }

        for op_name, exe_name in self.operations.items():
            button = QtWidgets.QPushButton(op_name)
            button.clicked.connect(lambda checked, name=exe_name: self.run_process(name))
            layout.addWidget(button)

        self.setLayout(layout)
        self.setWindowTitle("Multi-Language PyQt Application")
        self.resize(400, 300)

    def run_process(self, exe_name):
        try:
            result = subprocess.run(exe_name, check=True)
            self.status_label.setText(self.translations[self.current_language]['success'])
        except Exception as e:
            self.status_label.setText(self.translations[self.current_language]['error'])

    def change_language(self, lang):
        self.current_language = lang
        self.status_label.setText(self.translations[self.current_language]['welcome'])
        # Update buttons and other UI elements based on new language

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MultiLangApp()
    window.show()
    sys.exit(app.exec_())
