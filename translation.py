import os
from PyQt5.QtCore import QTranslator, QLocale, QCoreApplication
from PyQt5.QtWidgets import QApplication

class TranslatorManager:
    def __init__(self):
        self.translator = QTranslator()
        self.current_language = None

    def load_translations1(self):
        """Charge les fichiers de traduction selon la langue du système."""
        locale = QLocale.system().name()  # Ex. 'fr_FR', 'en_US', etc.
        self.set_language(locale)

    def set_language1(self, language_code):
        """Change la langue de l'application dynamiquement."""
        translations_path = os.path.join(os.path.dirname(__file__), 'lang', language_code)

        if os.path.exists(translations_path):
            try:
                self.translator = QTranslator()  # Réinitialiser le traducteur
                qm_files = [f for f in os.listdir(translations_path) if f.endswith('.qm')]

                if not qm_files:
                    print(f"Aucun fichier .qm trouvé pour la langue {language_code}.")
                    return

                for file in qm_files:
                    file_path = os.path.join(translations_path, file)
                    if self.translator.load(file_path):
                        QApplication.installTranslator(self.translator)
                        self.current_language = language_code  # Mémoriser la langue actuelle
                        print(f"Langue changée : {language_code}, fichier chargé : {file_path}")
                    else:
                        print(f"Échec du chargement du fichier : {file_path}")
            except Exception as e:
                print(f"Erreur lors du changement de langue : {e}")
        else:
            print(f"Le dossier de traductions {translations_path} n'existe pas pour {language_code}.")

    def retranslate_ui(self, window):
        """Appelle cette méthode pour rafraîchir les textes de l'interface après changement de langue."""
        window.setWindowTitle(QCoreApplication.translate("MainWindow", "Application multilingue"))
        if hasattr(window, 'language_selector'):
            window.language_selector.setItemText(0, QCoreApplication.translate("MainWindow", "Français (fr_FR)"))
            window.language_selector.setItemText(1, QCoreApplication.translate("MainWindow", "Anglais (en_US)"))
            window.language_selector.setItemText(2, QCoreApplication.translate("MainWindow", "Arabe (ar_SA)"))
            window.language_selector.setItemText(3, QCoreApplication.translate("MainWindow", "Turc (tr_TR)"))

    def load_translations(self):
        """Charge les fichiers de traduction selon la langue du système."""
        locale = QLocale.system().name()  # Ex. 'fr_FR', 'en_US', etc.
        translations_path = os.path.join(os.path.dirname(__file__), 'lang', locale, 'ui')

        if os.path.exists(translations_path):
            qm_files = [f for f in os.listdir(translations_path) if f.endswith('.qm')]
            if not qm_files:
                print(f"Aucun fichier .qm trouvé dans {translations_path}.")
                return

            try:
                for file in qm_files:
                    file_path = os.path.join(translations_path, file)
                    if self.translator.load(file_path):
                        QApplication.installTranslator(self.translator)
                        print(f"Chargement de la traduction : {file_path}")
                    else:
                        print(f"Échec du chargement du fichier : {file_path}")
            except Exception as e:
                print(f"Erreur lors du chargement des traductions : {e}")
        else:
            print(f"Le dossier de traductions {translations_path} n'existe pas.")

    def set_language(self, language_code):
        """Change la langue de l'application dynamiquement."""
        translations_path = os.path.join(os.path.dirname(__file__), 'lang', language_code, 'ui')

        if os.path.exists(translations_path):
            try:
                self.translator = QTranslator()  # Réinitialiser le traducteur
                current_file = os.path.basename(__file__)
                current_base_name = os.path.splitext(current_file)[0]

                # Rechercher un fichier de traduction correspondant au nom du fichier Python actuel
                qm_file = f"{current_base_name}_translated.qm"
                qm_file_path = os.path.join(translations_path, qm_file)

                if os.path.exists(qm_file_path):
                    if self.translator.load(qm_file_path):
                        QApplication.installTranslator(self.translator)
                        print(f"Langue changée : {language_code}, fichier chargé : {qm_file_path}")
                    else:
                        print(f"Échec du chargement du fichier : {qm_file_path}")
                else:
                    print(f"Aucun fichier .qm correspondant trouvé : {qm_file_path}")
            except Exception as e:
                print(f"Erreur lors du changement de langue : {e}")
        else:
            print(f"Le dossier de traductions {translations_path} n'existe pas pour {language_code}.")
