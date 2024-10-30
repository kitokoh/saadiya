from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QVBoxLayout, QWidget, QDialog, QLabel, QPushButton, QMessageBox, QMenu, QComboBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTranslator, QLocale, QLibraryInfo

from media_manager import MediaTable
from group_manager import GroupTable
from instances_table import InstanceTable
from .wp_robot_install import WpRobot

class AboutDialog(QDialog):
    """Boîte de dialogue pour 'À propos'."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("À propos de AI FB ROBOT Pro"))
        layout = QVBoxLayout()
        label = QLabel(self.tr("AI FB ROBOT Pro v1.0\n\nDéveloppé par Ibrahim Hakkı.\n\nCette application utilise des techniques d'automatisation IA pour faciliter la gestion des médias, groupes et instances dans les réseaux sociaux."))
        layout.addWidget(label)
        close_button = QPushButton(self.tr("Fermer"))
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)

class CertificateDialog(QDialog):
    """Boîte de dialogue pour 'Certificat'."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Certificat"))
        layout = QVBoxLayout()
        label = QLabel(self.tr("Votre certificat est valide jusqu'au 31 décembre 202x.\n\nAssurez-vous de le renouveler avant cette date pour maintenir l'accès aux fonctionnalités premium."))
        layout.addWidget(label)
        close_button = QPushButton(self.tr("Fermer"))
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)

class BlogMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        #self.resize(900, 600)
        self.setGeometry(100, 210, 900, 600)

        self.setWindowIcon(QIcon('resources/icons/facebook-icon-png-770.png'))  # Spécifiez le chemin de l'icône

        # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()

        menubar_font = QFont("Arial", 10, QFont.Bold)
        menubar = self.menuBar()
        menubar.setFont(menubar_font)
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #f0f0f0;
                padding: 5px;
            }
            QMenuBar::item {
                padding: 8px 25px;
            }
            QMenuBar::item:selected {
                background-color: #d3d3d3;
            }
            QMenu {
                padding: 10px;
            }
        """)

        # Menus avec self.tr pour les traductions


        instance_action = QAction(QIcon("resourcses/icons/facebook-icon-png-745.png"), self.tr('Instance'), self)
        instance_action.setToolTip(self.tr('Afficher la liste des instances'))
        instance_action.triggered.connect(self.open_instance)
        menubar.addAction(instance_action)

        media_action = QAction(QIcon("resosurces/icons/facebook-icon-png-745.png"), self.tr('Medias'), self)
        media_action.setToolTip(self.tr('Afficher la liste des médias'))
        media_action.triggered.connect(self.open_media)
        menubar.addAction(media_action)

        group_action = QAction(QIcon("resourcess/icons/facebook-icon-png-745.png"), self.tr('Groups'), self)
        group_action.setToolTip(self.tr('Afficher la liste des groupes'))
        group_action.triggered.connect(self.open_group)
        menubar.addAction(group_action)

        about_action = QAction(QIcon("resourcess/icons/facebook-icon-png-745.png"), self.tr('About'), self)
        about_action.setToolTip(self.tr('Informations sur l\'application'))
        about_action.triggered.connect(self.open_about)
        menubar.addAction(about_action)

        certificate_action = QAction(QIcon("resourcses/icons/facebook-icon-png-745.png"), self.tr('Certif'), self)
        certificate_action.setToolTip(self.tr('Informations sur votre certificat'))
        certificate_action.triggered.connect(self.open_certificate)
        menubar.addAction(certificate_action)

        settings_menu = menubar.addMenu(QIcon("resourcses/icons/facebook-icon-png-745.png"), self.tr('Params'))

        dark_mode_action = QAction(self.tr('Activer le mode sombre'), self, checkable=True)
        dark_mode_action.setToolTip(self.tr('Basculer vers le mode sombre'))
        dark_mode_action.triggered.connect(self.toggle_dark_mode)
        settings_menu.addAction(dark_mode_action)

        theme_action = QAction(self.tr('Personnaliser le thème'), self)
        theme_action.setToolTip(self.tr('Changer les couleurs du thème'))
        theme_action.triggered.connect(self.customize_theme)
        settings_menu.addAction(theme_action)

        instance_install = QAction(QIcon("resourcres/icons/facebook-icon-png-745.png"), self.tr('Install'), self)
        instance_install.setToolTip(self.tr('Install Instances'))
        instance_install.triggered.connect(self.open_install)
        menubar.addAction(instance_install)

        # Ajouter le menu des langues
        self.language_menu = QMenu(self.tr('Langue'), self)
        switch_language_en = QAction(self.tr('Anglais'), self)
        switch_language_en.triggered.connect(lambda: self.switch_language("en"))
        self.language_menu.addAction(switch_language_en)

        switch_language_fr = QAction(self.tr('Français'), self)
        switch_language_fr.triggered.connect(lambda: self.switch_language("fr"))
        self.language_menu.addAction(switch_language_fr)

        switch_language_tr = QAction(self.tr('Turc'), self)
        switch_language_tr.triggered.connect(lambda: self.switch_language("tr"))
        self.language_menu.addAction(switch_language_tr)

        switch_language_ar = QAction(self.tr('Arabe'), self)
        switch_language_ar.triggered.connect(lambda: self.switch_language("ar"))
        self.language_menu.addAction(switch_language_ar)

        menubar.addMenu(self.language_menu)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.instance_table = InstanceTable(self)
        layout.addWidget(self.instance_table)

    def init_language(self):
        """Initialise la langue par défaut à celle du système."""
        system_locale = QLocale.system().name()[:2]
        self.switch_language(system_locale)

    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load("lang/en_US/ui/main_fb_robot.qm")
        elif language == "fr":
            self.translator.load("lang/fr_FR/ui/main_fb_robot.qm")
        elif language == "tr":
            self.translator.load("lang/tr_TR/modules/main_fb_robot.qm")
        elif language == "ar":
            self.translator.load("lang/ar_AR/ui/main_fb_robot.qm")
        QApplication.instance().installTranslator(self.translator)
        self.retranslateUi()

    def retranslateUi(self):
        """Recharge les textes traduits dans l'interface."""
        self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        # Ici, mettez à jour tous les labels, boutons, et textes affichés avec self.tr()

    def open_media(self):
        self.setCentralWidget(MediaTable(self))

    def open_instance(self):
        self.setCentralWidget(InstanceTable(self))
    def open_install(self):
        self.setCentralWidget(WpRobot())

    def open_group(self):
        self.setCentralWidget(GroupTable(self))

    def open_about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

    def open_certificate(self):
        certificate_dialog = CertificateDialog(self)
        certificate_dialog.exec_()

    def toggle_dark_mode(self, checked):
        if checked:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2e2e2e;
                }
                QLabel, QMenuBar, QPushButton, QMenu {
                    color: white;
                }
                QAction {
                    font-size: 14px;
                }
            """)
        else:
            self.setStyleSheet("")

    def customize_theme(self):
        QMessageBox.information(self, self.tr("Personnalisation du thème"), self.tr("Cette fonctionnalité sera disponible dans une future version."))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = BlogMainWindow()
    window.show()
    sys.exit(app.exec_())
