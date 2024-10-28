import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QPushButton, QGraphicsOpacityEffect, QHBoxLayout, QFrame, QApplication
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QThread, pyqtSignal, QTranslator, QLocale
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from imports import *
import os

# Classe pour charger des images de manière asynchrone
class ImageLoader(QThread):
    image_loaded = pyqtSignal(QPixmap, int)

    def __init__(self, index, image_path):
        super().__init__()
                # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

        self.index = index
        self.image_path = image_path
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load("resources/lang/en_US/ui/carousel_translated.qm")
        elif language == "fr":
            self.translator.load("resources/lang/fr_FR/ui/carousel_translated.qm")
        elif language == "tr":
            self.translator.load("resources/lang/tr_TR/ui/carousel_translated.qm")
        elif language == "ar":
            self.translator.load("resources/lang/ar_AR/ui/carousel_translated.qm")

        # Installer le traducteur pour appliquer la nouvelle langue
        QApplication.instance().installTranslator(self.translator)
        
            # Sauvegarder le choix de l'utilisateur
        self.save_language_choice(language)


        # Réappliquer la traduction sur tous les éléments visibles de l'interface
        self.retranslateUi()

    def save_language_choice(self, language):
        """Sauvegarde le choix de langue de l'utilisateur dans un fichier JSON."""
        preferences = {'language': language}
        with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'w') as f:
            json.dump(preferences, f)
    def retranslateUi(self):
        # """Recharge les textes traduits dans l'interface."""
        # self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        # # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # # Par exemple, pour les actions du menu :
        # self.instance_action.setText(self.tr('Instance'))
        # self.media_action.setText(self.tr('Médias'))
        # self.group_action.setText(self.tr('Groupes'))
        # self.about_action.setText(self.tr('About'))
        # self.certificate_action.setText(self.tr('Certif'))
        # self.language_menu.setTitle(self.tr('Langue'))
        pass

    def init_language(self):
        """Initialise la langue par défaut à celle du système ou à celle choisie par l'utilisateur."""
        # Vérifiez si le fichier de préférences existe
        if os.path.exists(os.path.join(user_data_dir, 'resources', 'settings.json')):
            with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'r') as f:
                preferences = json.load(f)
                selected_language = preferences.get('language', 'en')  # Par défaut à l'anglais si non trouvé
        else:
            # Obtenir le code de langue du système
            system_locale = QLocale.system().name()[:2]  # Par exemple: 'fr', 'en', 'tr', etc.

            # Dictionnaire pour mapper les codes de langue aux traductions
            language_map = {
                'en': 'en',
                'fr': 'fr',
                'tr': 'tr',
                'ar': 'ar',
            }

            # Vérifier si la langue système est supportée, sinon utiliser l'anglais par défaut
            selected_language = language_map.get(system_locale, 'en')

        self.switch_language(selected_language)

    def run(self):
        if os.path.exists(self.image_path):
            pixmap = QPixmap(self.image_path)
            self.image_loaded.emit(pixmap, self.index)
        else:
            self.image_loaded.emit(QPixmap(), self.index)  # Envoyer un QPixmap vide si l'image n'existe pas

class CarouselWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
                # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

                # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()
        # Création de la disposition principale en vertical
        self.layout = QVBoxLayout(self)
        self.carousel = QStackedWidget(self)
        
        # Liste des éléments à afficher dans le carrousel
        self.items = [
            {"image": "resources/icons/robot-icons-30504.png", "text": self.tr("Bienvenue dans Nova360Pro, Votre Assistant")},
            {"image": "resources/images/9.jpg", "text": self.tr("Explorez nos fonctionnalités")},
            {"image": "resources/icons/automated_8345946.png", "text": self.tr("Découvrez des astuces professionnelles")}
        ]

        self.effects = []  # Liste pour stocker les effets d'animation
        self.indicators = []  # Liste pour les indicateurs de pagination
        self.image_threads = []  # Threads de chargement d'images asynchrone
        
        # Création du carrousel d'images
        for i, item in enumerate(self.items):
            widget = QFrame()
            widget_layout = QVBoxLayout(widget)

            # Image de fond
            label_image = QLabel()
            label_image.setAlignment(Qt.AlignCenter)
            label_image.setText(self.tr("Chargement..."))  # Texte par défaut en attendant que l'image se charge
            label_image.setStyleSheet("border-radius: 10px;")
            widget_layout.addWidget(label_image)

            # Texte superposé sur l'image
            label_text = QLabel(item["text"])
            label_text.setStyleSheet("""
                font-size: 24px; 
                font-weight: bold; 
                color: white; 
                background-color: rgba(0, 0, 0, 0.5);  /* Semi-transparent */
                padding: 20px;
                border-radius: 10px;
            """)
            label_text.setAlignment(Qt.AlignCenter)
            widget_layout.addWidget(label_text, alignment=Qt.AlignCenter)

            effect = QGraphicsOpacityEffect(widget)
            effect.setOpacity(1.0)
            widget.setGraphicsEffect(effect)
            self.effects.append(effect)

            self.carousel.addWidget(widget)

            # Charger les images de manière asynchrone
            thread = ImageLoader(i, item["image"])
            thread.image_loaded.connect(self.on_image_loaded)
            self.image_threads.append(thread)
            thread.start()

        self.layout.addWidget(self.carousel)

        # Ajout des indicateurs de pagination (petits cercles)
        self.pagination_layout = QHBoxLayout()
        for i in range(len(self.items)):
            indicator = QLabel(self.tr("●"))
            indicator.setStyleSheet("color: grey; font-size: 18px;")
            self.pagination_layout.addWidget(indicator, alignment=Qt.AlignCenter)
            self.indicators.append(indicator)

        self.layout.addLayout(self.pagination_layout)

        # Initialisation des indicateurs
        self.update_indicators(0)

        # Timer pour changer d'image automatiquement
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_image)
        self.timer.start(300000)  # Passer à la prochaine image toutes les 3 secondes
        self.current_index = 0

        # Boutons de navigation
        self.prev_button = QPushButton(self.tr("<"))
        self.prev_button.setStyleSheet("background-color: transparent; color: white; font-size: 24px;")
        self.prev_button.clicked.connect(self.prev_image)
        self.layout.addWidget(self.prev_button, alignment=Qt.AlignLeft)

        self.next_button = QPushButton(self.tr(">"))
        self.next_button.setStyleSheet("background-color: transparent; color: white; font-size: 24px;")
        self.next_button.clicked.connect(self.next_image)
        self.layout.addWidget(self.next_button, alignment=Qt.AlignRight)
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load("resources/lang/en_US/ui/carousel_translated.qm")
        elif language == "fr":
            self.translator.load("resources/lang/fr_FR/ui/carousel_translated.qm")
        elif language == "tr":
            self.translator.load("resources/lang/tr_TR/ui/carousel_translated.qm")
        elif language == "ar":
            self.translator.load("resources/lang/ar_AR/ui/carousel_translated.qm")

        # Installer le traducteur pour appliquer la nouvelle langue
        QApplication.instance().installTranslator(self.translator)
        
            # Sauvegarder le choix de l'utilisateur
        self.save_language_choice(language)


        # Réappliquer la traduction sur tous les éléments visibles de l'interface
        self.retranslateUi()

    def save_language_choice(self, language):
        """Sauvegarde le choix de langue de l'utilisateur dans un fichier JSON."""
        preferences = {'language': language}
        with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'w') as f:
            json.dump(preferences, f)
    def retranslateUi(self):
        """Recharge les textes traduits dans l'interface."""
        # self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        # # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # # Par exemple, pour les actions du menu :
        # self.instance_action.setText(self.tr('Instance'))
        # self.media_action.setText(self.tr('Médias'))
        # self.group_action.setText(self.tr('Groupes'))
        # self.about_action.setText(self.tr('About'))
        # self.certificate_action.setText(self.tr('Certif'))
        # self.language_menu.setTitle(self.tr('Langue'))
        pass

    def init_language(self):
        """Initialise la langue par défaut à celle du système ou à celle choisie par l'utilisateur."""
        # Vérifiez si le fichier de préférences existe
        if os.path.exists(os.path.join(user_data_dir, 'resources', 'settings.json')):
            with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'r') as f:
                preferences = json.load(f)
                selected_language = preferences.get('language', 'en')  # Par défaut à l'anglais si non trouvé
        else:
            # Obtenir le code de langue du système
            system_locale = QLocale.system().name()[:2]  # Par exemple: 'fr', 'en', 'tr', etc.

            # Dictionnaire pour mapper les codes de langue aux traductions
            language_map = {
                'en': 'en',
                'fr': 'fr',
                'tr': 'tr',
                'ar': 'ar',
            }

            # Vérifier si la langue système est supportée, sinon utiliser l'anglais par défaut
            selected_language = language_map.get(system_locale, 'en')

        self.switch_language(selected_language)

    # Slot pour mettre à jour l'image une fois chargée de manière asynchrone
    def on_image_loaded(self, pixmap, index):
        label_image = self.carousel.widget(index).layout().itemAt(0).widget()
        if pixmap.isNull():
            label_image.setText(self.tr("Image non disponible"))  # Message d'erreur si l'image n'est pas trouvée
        else:
            label_image.setPixmap(pixmap.scaled(self.width(), self.height() // 2, Qt.KeepAspectRatio))
            label_image.setText("")  # Retirer le texte "Chargement..."

    # Méthode pour créer une animation d'opacité fluide
    def animate_opacity(self, widget, start_opacity, end_opacity):
        anim = QPropertyAnimation(widget, b"opacity")
        anim.setDuration(1000)
        anim.setStartValue(start_opacity)
        anim.setEndValue(end_opacity)
        anim.finished.connect(lambda: self.on_animation_finished(widget, end_opacity))
        anim.start()

    # Gestionnaire de fin d'animation
    def on_animation_finished(self, widget, end_opacity):
        widget.setOpacity(end_opacity)  # S'assurer que l'opacité finale est bien appliquée

    # Passer à l'image suivante avec animation d'opacité
    def next_image(self):
        self.effects[self.current_index].setOpacity(1)
        self.animate_opacity(self.effects[self.current_index], 1, 0)
        self.current_index = (self.current_index + 1) % len(self.items)
        self.carousel.setCurrentIndex(self.current_index)
        self.animate_opacity(self.effects[self.current_index], 0, 1)
        self.update_indicators(self.current_index)

    # Passer à l'image précédente avec animation d'opacité
    def prev_image(self):
        self.effects[self.current_index].setOpacity(1)
        self.animate_opacity(self.effects[self.current_index], 1, 0)
        self.current_index = (self.current_index - 1) % len(self.items)
        self.carousel.setCurrentIndex(self.current_index)
        self.animate_opacity(self.effects[self.current_index], 0, 1)
        self.update_indicators(self.current_index)

    # Met à jour l'affichage des indicateurs de pagination
    def update_indicators(self, index):
        for i, indicator in enumerate(self.indicators):
            if i == index:
                indicator.setStyleSheet("color: white; font-size: 18px;")
            else:
                indicator.setStyleSheet("color: grey; font-size: 18px;")

    # Ajuster les dimensions lors du redimensionnement de la fenêtre
    def resizeEvent(self, event):
        for i in range(len(self.items)):
            label_image = self.carousel.widget(i).layout().itemAt(0).widget()
            if label_image.pixmap() is not None:  # Vérification si le pixmap existe
                label_image.setPixmap(label_image.pixmap().scaled(self.width(), self.height() // 2, Qt.KeepAspectRatio))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Charger la traduction selon la langue du système
    translator = QTranslator()
    system_locale = QLocale.system().name()  # ex : 'fr_FR', 'en_US', etc.
    qm_path = f"lang/{system_locale}/carousel.qm"  # Chemin de ton fichier .qm

    if translator.load(qm_path):
        app.installTranslator(translator)

    # Créer et afficher le widget du carrousel
    window = CarouselWidget()
    window.show()

    sys.exit(app.exec_())
