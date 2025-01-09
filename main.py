import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTabWidget, QTabBar, QFrame, QLabel, QWidget,
    QSplitter, QStackedWidget
)

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                             QLabel, QHeaderView, QAbstractItemView, QComboBox, 
                             QDialog, QDialogButtonBox, QFormLayout, QMenu, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from Home.giris import SplitScreenView
from PyQt5.QtWebEngineWidgets import QWebEngineView
from Home.login import Nova360ProApp
from Home.parametre import Nova360Ultimate
from upgrade import SpecialOfferWindow
from PyQt5.QtCore import Qt, QTranslator, QLocale, QLibraryInfo, QPropertyAnimation

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Navigateur Moderne")
        self.setWindowIcon(QIcon("browser_icon.png"))
        self.setGeometry(0, 60, 1200, 800)

        # Activer les paramètres pour personnalisation
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)

        self.initUI()

    def initUI(self):
        # Conteneur principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Disposition principale avec un séparateur
        self.main_layout = QVBoxLayout(central_widget)  # Passez à QVBoxLayout pour inclure la barre supérieure
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Créer la barre supérieure avec les boutons
       # self.create_top_bar(self.main_layout)

        # Créer le conteneur principal avec un séparateur
        self.central_container = QSplitter(Qt.Horizontal)
        self.central_container.setChildrenCollapsible(False)

        # Créer le menu latéral
        self.create_side_menu()

        # Conteneur principal du navigateur
        self.browser_container = QWidget()
        self.browser_layout = QVBoxLayout(self.browser_container)
        self.browser_layout.setContentsMargins(0, 0, 0, 0)

        # Ajouter les onglets
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.update_search_bar_visibility)
        self.tab_widget.setStyleSheet(self.tab_widget_style())

        self.browser_layout.addWidget(self.tab_widget)

        # Ajouter la barre de recherche
        self.create_search_bar(self.browser_layout)

        # Ajouter le menu latéral et le conteneur navigateur au séparateur
        self.central_container.addWidget(self.side_menu)
        self.central_container.addWidget(self.browser_container)

        # Ajuster la taille initiale
        self.central_container.setSizes([200, 1000])
        self.main_layout.addWidget(self.central_container, stretch=1)

        # Ajouter un premier onglet avec une page web
        self.add_new_tab(QUrl("https://www.nova360.turknovatech.com"), "Nova360", "new_tab_icon.ico")
    def open_instance(self):
       # self.setCentralWidget(InstanceTable(self))
       pass
    def open_about_window(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

    def find_tab_by_name(self, name):
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == name:
                return i  # Renvoie l'index si trouvé
        return -1  # Aucun onglet trouvé

    def open_accueil_window1(self):
        tab_name = "Accueil"  # Nom de l'onglet
        existing_tab_index = self.find_tab_by_name(tab_name)
        
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.tab_widget.setCurrentIndex(existing_tab_index)
        else:
            # Sinon, créez un nouvel onglet
            accueil_widget = QLabel("Accueil - Contenu ici")  # Remplacez par le widget réel
            self.add_new_tab(accueil_widget, tab_name, "accueil_icon.ico")



    def open_update_window(self):
        QMessageBox.information(self, "Upgrade", "Mettez à niveau votre plan.")

    def open_certif_window(self):
        QMessageBox.information(self, "Nova360 - Certif", "Certification pour Nova360.")
    def open_telecommande_window1(self):
        """
        Ouvre la fenêtre Télécommande avec une interface de base.
        """
        telecommande_window = QDialog(self)
        telecommande_window.setWindowTitle("Télécommande")
        telecommande_window.setFixedSize(400, 300)
        telecommande_window.setStyleSheet("""
            QDialog {
                background-color: #1E1E2F;
                color: #FFFFFF;
                border-radius: 10px;
            }
        """)

        # Layout principal
        layout = QVBoxLayout(telecommande_window)

        # Label principal
        title_label = QLabel("Télécommande - Contrôle central")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Boutons de contrôle
        buttons_layout = QVBoxLayout()
        buttons = [
            ("Open Panel", self.open_panel_action),
            ("Start Robots", self.start_robots_action),
            ("Choice Module", self.choice_module_action),
        ]

        for text, action in buttons:
            button = QPushButton(text)
            button.setFixedHeight(40)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2C2C3D;
                    color: #FFFFFF;
                    border: 1px solid #3D3D4E;
                    border-radius: 10px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #3A3A4E;
                }
            """)
            button.clicked.connect(action)
            buttons_layout.addWidget(button)

        layout.addLayout(buttons_layout)
        telecommande_window.setLayout(layout)

        # Afficher la fenêtre
        telecommande_window.exec_()

    def open_panel_action(self):
        """
        Action associée au bouton 'Open Panel'.
        """
        QMessageBox.information(self, "Action", "Open Panel action triggered.")
    def start_robots_action(self):
        """
        Action associée au bouton 'Start Robots'.
        """
        QMessageBox.information(self, "Action", "Start Robots action triggered.")
    def choice_module_action(self):
        """
        Action associée au bouton 'Choice Module'.
        """
        QMessageBox.information(self, "Action", "Choice Module action triggered.")

    def open_uninstall_window(self):
        """
        Ouvre la fenêtre de désinstallation.
        """
        QMessageBox.warning(self, "Tools - Uninstall", "Uninstall tool triggered.")
    def open_instances_window(self):
        """
        Ouvre la fenêtre 'Instances'.
        """
        QMessageBox.information(self, "Instances", "Gestion des instances.")
    def switch_language(self):
        """
        Permet de basculer entre différentes langues.
        """
        QMessageBox.information(self, "Langue", "Change language feature triggered.")
    def open_upgrade_window(self):
        """
        Ouvre la fenêtre 'Upgrade'.
        """
        QMessageBox.information(self, "Upgrade", "Upgrade your plan.")

    # Ajoutez les méthodes pour les boutons
    def minimize_window(self):
        self.showMinimized()

    def maximize_window(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def close_window(self):
        self.close()









    def create_search_bar(self, layout):
        search_bar_frame = QFrame()
        search_bar_frame.setStyleSheet("background-color: #333;")
        search_bar_layout = QHBoxLayout(search_bar_frame)
        search_bar_layout.setContentsMargins(5, 5, 5, 5)

        # Boutons de navigation
        self.back_button = QPushButton("<")
        self.forward_button = QPushButton(">")
        self.refresh_button = QPushButton("⟳")
        self.home_button = QPushButton("🏠")

        for btn in [self.back_button, self.forward_button, self.refresh_button, self.home_button]:
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(self.button_style())
            search_bar_layout.addWidget(btn)

        # Barre de recherche
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Rechercher ou entrer une URL")
        self.url_bar.setStyleSheet(self.url_bar_style())
        search_bar_layout.addWidget(self.url_bar, stretch=1)

        # Connecter les boutons
        self.back_button.clicked.connect(self.navigate_back)
        self.forward_button.clicked.connect(self.navigate_forward)
        self.refresh_button.clicked.connect(self.refresh_page)
        self.home_button.clicked.connect(self.navigate_home)
        self.url_bar.returnPressed.connect(self.load_url)

        layout.addWidget(search_bar_frame)

        # Bouton pour ajouter un nouvel onglet
        self.new_tab_button = QPushButton("+")
        self.new_tab_button.setFixedSize(30, 30)
        self.new_tab_button.setStyleSheet(self.button_style())
        self.new_tab_button.clicked.connect(self.open_new_tab)
        search_bar_layout.addWidget(self.new_tab_button)
        def open_google_tab(self):
            url = QUrl("https://www.nova360.turknovatech.com")
            self.add_new_tab(url, "Nova360", "google_icon.ico")

    def add_new_tab(self, content, label, icon_path="default_icon.ico"):
        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(label)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Créez le contenu de l'onglet selon le type de `content`
        if isinstance(content, QUrl):  # Si le contenu est une URL
            browser = QWebEngineView()
            browser.setUrl(content)
            browser.setStyleSheet("""
                QWebEngineView {
                    background-color: white;
                    color: black;
                }
            """)  # Applique un fond blanc et un texte noir
            widget_to_add = browser
        elif isinstance(content, QWidget):  # Si le contenu est un widget personnalisé
            content.setStyleSheet("""
                QWidget {
                    background-color: white;
                    color: black;
                }
            """)  # Applique un fond blanc et un texte noir
            widget_to_add = content
        else:
            raise TypeError(f"Type non supporté pour 'content': {type(content)}")

        # Ajoutez l'onglet
        index = self.tab_widget.addTab(widget_to_add, "")
        self.tab_widget.setTabIcon(index, QIcon(icon_path))
        self.tab_widget.setTabText(index, label)
        self.tab_widget.setCurrentIndex(index)

        # Connectez les signaux si nécessaire
        if isinstance(content, QUrl):  # Seulement pour les QWebEngineView
            widget_to_add.urlChanged.connect(self.update_url)

        # Ajout d'un style général pour l'onglet
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                background: white;
            }
            QTabWidget::tab-bar {
                background: lightgray;
            }
            QTabBar::tab {
                background: lightgray;
                color: black;
                padding: 5px;
            }
            QTabBar::tab:selected {
                background: white;
                color: black;
            }
        """)

    def add_new_tab1(self, url, label, icon_path="default_icon.ico"):
        browser = QWebEngineView()
        browser.setUrl(url)

        index = self.tab_widget.addTab(browser, "")
        self.tab_widget.setTabIcon(index, QIcon(icon_path))
        self.tab_widget.setTabText(index, label)
        self.tab_widget.setCurrentIndex(index)

        browser.urlChanged.connect(self.update_url)

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)

    def update_url(self, url):
        self.url_bar.setText(url.toString())

    def load_url(self):
        current_browser = self.tab_widget.currentWidget()
        url = QUrl(self.url_bar.text())
        if url.scheme() == "":
            url.setScheme("http")
        current_browser.setUrl(url)

    def navigate_back(self):
        current_browser = self.tab_widget.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            current_browser.back()

    def navigate_forward(self):
        current_browser = self.tab_widget.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            current_browser.forward()

    def refresh_page(self):
        current_browser = self.tab_widget.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            current_browser.reload()

    def navigate_home(self):
        current_browser = self.tab_widget.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            current_browser.setUrl(QUrl("https://www.nova360.turknovatech.com"))

    def update_search_bar_visibility(self, index):
        current_widget = self.tab_widget.widget(index)
        if isinstance(current_widget, QWebEngineView):
            self.url_bar.show()
        else:
            self.url_bar.hide()

    def tab_widget_style(self):
        return """
        QTabWidget::pane { border: 0; }
        QTabBar::tab {
            background: #3A3A3A;
            color: #FFFFFF;
            padding: 5px 15px;
            margin: 2px;
            border-radius: 5px;
        }
        QTabBar::tab:selected {
            background: #555555;
        }
        QTabBar::tab:hover {
            background: #4A4A4A;
        }
        """

    def button_style(self):
        return """
        QPushButton {
            background-color: #3A3A3A;
            color: #FFFFFF;
            border: none;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #555555;
        }
        QPushButton:pressed {
            background-color: #2A2A2A;
        }
        """

    def url_bar_style(self):
        return """
        QLineEdit {
            background-color: #3A3A3A;
            color: #FFFFFF;
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 5px;
        }
        QLineEdit:focus {
            border: 1px solid #AAAAAA;
        }
        """
    def open_new_tab(self,tab_name="Dashboard", icon_path="icons/dashboard_icon.ico"):
        self.add_new_tab(QUrl("https://www.nova360.turknovatech.com"), "Nova360", "new_tab_icon.ico")


    def create_top_bar(self, layout):
        self.top_bar_frame = QFrame()
        self.top_bar_frame.setStyleSheet("background-color: #282828;")
        self.top_bar_frame.setFixedHeight(40)

        top_bar_layout = QHBoxLayout(self.top_bar_frame)
        top_bar_layout.setContentsMargins(5, 5, 5, 5)

        # Boutons natifs
        self.minimize_button = QPushButton("─")
        self.maximize_button = QPushButton("❐")
        self.close_button = QPushButton("✖")
        self.new_tab_button = QPushButton("+")  # Bouton pour nouvel onglet

        for btn in [self.new_tab_button, self.minimize_button, self.maximize_button, self.close_button]:
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(self.button_style())
            top_bar_layout.addWidget(btn, alignment=Qt.AlignRight)

        # Ajouter les onglets à la barre supérieure
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.update_search_bar_visibility)
        self.tab_widget.setStyleSheet(self.tab_widget_style())
        self.tab_widget.setTabBarAutoHide(False)

        top_bar_layout.insertWidget(0, self.tab_widget, stretch=1)
        layout.addWidget(self.top_bar_frame)

        # Connecter les boutons natifs
        self.minimize_button.clicked.connect(self.showMinimized)
        self.maximize_button.clicked.connect(self.toggle_maximized)
        self.close_button.clicked.connect(self.close)
        self.new_tab_button.clicked.connect(lambda: self.add_new_tab(QUrl("https://www.nova360.turknovatech.com"), "Nova360"))


    def toggle_maximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    def add_new_tab2(self, widget, label, icon_path="default_icon.ico"):
        index = self.tab_widget.addTab(widget, "")
        self.tab_widget.setTabIcon(index, QIcon(icon_path))
        self.tab_widget.setTabText(index, label)
        self.tab_widget.setCurrentIndex(index)


    def open_accueil_window(self):
        tab_name = "Accueil"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Sinon, créez une instance unique de Nova360ProApp et ajoutez un nouvel onglet
        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
            self.nova360pro = Nova360ProApp(main_app=self)  # Créez une seule fois l'instance

        # Ajoutez l'instance existante au nouvel onglet
        self.add_custom_tab(self.nova360pro, tab_name, "nova_icon.ico")


    def open_telecommande_window (self):
        tab_name = "Telecomande"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Sinon, créez une instance unique de Nova360ProApp et ajoutez un nouvel onglet
        if not hasattr(self, 'telecommande') or self.telecommande is None:
            self.telecommande = SplitScreenView(main_app=self)  # Créez une seule fois l'instance

        # Ajoutez l'instance existante au nouvel onglet
        self.add_custom_tab(self.telecommande, tab_name, "nova_icon.ico")


    # def add_custom_tab(self, widget, title, icon_path=None):
    #     """Ajoute un nouvel onglet avec un widget personnalisé."""
    #     index = self.tab_widget.addTab(widget, title)
    #     if icon_path:
    #         self.tab_widget.setTabIcon(index, QIcon(icon_path))
    #     self.tab_widget.setCurrentIndex(index)
    def add_custom_tab(self, widget, title, icon_path=None):
        """
        Ajoute un nouvel onglet au QTabWidget avec un widget, un titre et une icône.
        """
        if not hasattr(self, "tab_widget"):
            print("Erreur : L'objet 'Browser' ne possède pas d'attribut 'tab_widget'.")
            return

        index = self.tab_widget.addTab(widget, title)

        # Ajouter une icône si fournie
        if icon_path:
            icon = QIcon(icon_path)
            self.tab_widget.setTabIcon(index, icon)

        # Afficher l'onglet nouvellement ajouté
        self.tab_widget.setCurrentIndex(index)

    def open_search_window(self):
        """Ouvre un onglet avec le contenu de la classe 'SearchWidget'."""
        widget = SearchWidget()
        self.add_custom_tab(widget, "Recherche", "search_icon.ico")

    def open_settings_window(self):
        """Ouvre un onglet avec le contenu de la classe 'SettingsWidget'."""
 
        tab_name = "Settings"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Sinon, créez une instance unique de Nova360ProApp et ajoutez un nouvel onglet
        if not hasattr(self, 'settings') or self.settings is None:
            self.settings = Nova360Ultimate(main_app=self)  # Créez une seule fois l'instance

        # Ajoutez l'instance existante au nouvel onglet
        self.add_custom_tab(self.settings, tab_name, "nova_icon.ico")


    def open_help_window(self):
        """Ouvre un onglet avec le contenu de la classe 'HelpWidget'."""
        widget = HelpWidget()
        self.add_custom_tab(widget, "Aide", "help_icon.ico")
    def open_remote_window(self):
        """Ouvre un onglet avec le contenu de la classe 'HelpWidget'."""
        widget = HelpWidget()
        self.add_custom_tab(widget, "Aide", "help_icon.ico")
    def open_upgrade_window(self):
        tab_name = "Upgrade"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Sinon, créez une instance unique de Nova360ProApp et ajoutez un nouvel onglet
        if not hasattr(self, 'upgrades') or self.upgrades is None:
            self.upgrades = SpecialOfferWindow(main_app=self)  # Créez une seule fois l'instance

        # Ajoutez l'instance existante au nouvel onglet
        self.add_custom_tab(self.upgrades, tab_name, "nova_icon.ico")
    def create_side_menu(self):
        """
        Crée un menu latéral avec des boutons de contrôle en haut,
        une barre de séparation, et un menu rétractable/extensible.
        """
        # Panneau latéral
        self.side_menu = QFrame()
        self.side_menu.setFixedWidth(60)  # Par défaut, menu réduit
        self.side_menu.setStyleSheet("""
            QFrame {
                background-color: #21252B;  /* Couleur sombre professionnelle */
                border-right: 1px solid #3C4048;
            }
        """)

        # Layout principal
        self.side_menu_layout = QVBoxLayout(self.side_menu)
        self.side_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.side_menu_layout.setSpacing(0)

        # --- Ligne supérieure : Boutons de contrôle ---
        self.control_buttons_layout = QHBoxLayout()
        self.control_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.control_buttons_layout.setSpacing(3)  # Espacement réduit entre les boutons

        # Bouton de réduction
        self.minimize_button = QPushButton("-")
        self.minimize_button.setFixedSize(20, 20)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-color: #2C2F36;
                color: #FFFFFF;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3A3D46;
            }
        """)
        self.minimize_button.clicked.connect(self.minimize_window)
        self.control_buttons_layout.addWidget(self.minimize_button)

        # Bouton d'agrandissement
        self.maximize_button = QPushButton("□")
        self.maximize_button.setFixedSize(20, 20)
        self.maximize_button.setStyleSheet("""
            QPushButton {
                background-color: #2C2F36;
                color: #FFFFFF;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3A3D46;
            }
        """)
        self.maximize_button.clicked.connect(self.maximize_window)
        self.control_buttons_layout.addWidget(self.maximize_button)

        # Bouton de fermeture
        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(20, 20)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #FF4444;
                color: #FFFFFF;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #FF2222;
            }
        """)
        self.close_button.clicked.connect(self.close_window)
        self.control_buttons_layout.addWidget(self.close_button)

        # Ajouter la ligne supérieure au layout principal
        self.side_menu_layout.addLayout(self.control_buttons_layout)

        # --- Bouton de bascule ---
        self.toggle_button = QPushButton("⇔")
        self.toggle_button.setFixedHeight(50)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #2E323A;
                color: #FFFFFF;
                border: none;
                font-size: 16px;
                padding: 0;
            }
            QPushButton:hover {
                background-color: #3A3E47;
            }
        """)
        self.toggle_button.clicked.connect(self.toggle_side_menu)
        self.side_menu_layout.addWidget(self.toggle_button)

        # --- Liste des éléments du menu principal ---
        menu_items = [
            ("🏠", "Accueil", self.open_accueil_window, []),
            ("📡", "Télécommande", self.open_telecommande_window, []),
            ("⚙️", "Paramètres", self.open_settings_window, []),
            ("🌌", "Tools", None, [
                ("ℹ️", "About", self.open_about_window),
                ("📜", "Certif", self.open_certificate),
            ]),
            # ("🛠️", "Tools", None, [
            #     ("❌", "Uninstall", self.open_uninstall_window),
            #     ("🔄", "Update", self.open_update_window),
            # ]),
            ("📁", "Instances", self.open_instances_window, []),
            ("🌍", "Langue", self.switch_language, []),
            ("⬆️", "Upgrade", self.open_upgrade_window, []),
        ]

        self.menu_buttons = []  # Stocker les boutons principaux
        self.sub_menus = {}  # Associer chaque bouton principal à ses sous-menus

        # Génération des boutons principaux et sous-menus
        for icon, text, action, sub_items in menu_items:
            # Créer le bouton principal
            button = QPushButton(f"  {icon}   {text}")
            button.setFixedHeight(50)
            button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #FFFFFF;
                    border: none;
                    font-size: 16px;
                    text-align: left;
                    padding-left: 15px;
                }
                QPushButton:hover {
                    background-color: #2E323A;
                }
            """)
            if action:
                button.clicked.connect(action)
            self.side_menu_layout.addWidget(button)
            self.menu_buttons.append((button, icon, text))

            # Ajouter les sous-menus
            if sub_items:
                sub_menu = []
                for sub_icon, sub_text, sub_action in sub_items:
                    sub_button = QPushButton(f"     {sub_icon}   {sub_text}")
                    sub_button.setFixedHeight(40)
                    sub_button.setStyleSheet("""
                        QPushButton {
                            background-color: #2A2E36;
                            color: #FFFFFF;
                            border: none;
                            font-size: 14px;
                            text-align: left;
                            padding-left: 25px;
                        }
                        QPushButton:hover {
                            background-color: #33373E;
                        }
                    """)
                    sub_button.setVisible(False)  # Cacher les sous-menus par défaut
                    sub_button.clicked.connect(sub_action)
                    self.side_menu_layout.addWidget(sub_button)
                    sub_menu.append(sub_button)

                self.sub_menus[button] = sub_menu
                button.clicked.connect(lambda _, b=button: self.toggle_sub_menu(b))

        # Ajouter le panneau au layout principal
        self.layout().addWidget(self.side_menu)
        
    def toggle_side_menu(self):
        """
        Réduit ou élargit le menu latéral.
        """
        if self.side_menu.width() == 60:  # Mode réduit
            self.side_menu.setFixedWidth(200)
            for button, icon, text in self.menu_buttons:
                button.setText(f"  {icon}   {text}")
            for sub_buttons in self.sub_menus.values():
                for sub_button in sub_buttons:
                    sub_button.setFixedWidth(200)
        else:  # Mode élargi
            self.side_menu.setFixedWidth(60)
            for button, icon, text in self.menu_buttons:
                button.setText(f"  {icon}")
            for sub_buttons in self.sub_menus.values():
                for sub_button in sub_buttons:
                    sub_button.setFixedWidth(60)

    def toggle_sub_menu(self, button):
        """
        Affiche ou masque les sous-menus associés au bouton principal.
        """
        sub_buttons = self.sub_menus.get(button, [])
        for sub_button in sub_buttons:
            sub_button.setVisible(not sub_button.isVisible())
    def open_certificate(self):
        certificate_dialog = CertificateDialog(self)
        certificate_dialog.exec_()


class AccueilWidget(QWidget):
    """Widget pour l'onglet 'Accueil'."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Bienvenue dans l'onglet Accueil")
        layout.addWidget(label)
        self.setLayout(layout)


class SearchWidget(QWidget):
    """Widget pour l'onglet 'Rechercher'."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Page de Recherche")
        layout.addWidget(label)
        self.setLayout(layout)


class SettingsWidget(QWidget):
    """Widget pour l'onglet 'Paramètres'."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Page des Paramètres")
        layout.addWidget(label)
        self.setLayout(layout)


class HelpWidget(QWidget):
    """Widget pour l'onglet 'Aide'."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Page d'Aide")
        layout.addWidget(label)
        self.setLayout(layout)


class AboutDialog(QDialog):
    """Boîte de dialogue générique pour 'À propos' de Nova360 AI."""
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialiser et charger les traductions
        # self.translator_manager = TranslatorManager()
        # self.translator_manager.load_translations()

        # Configuration de la fenêtre
        self.setWindowTitle(self.tr("À propos de Nova360 AI"))
        layout = QVBoxLayout()

        # Contenu principal
        label = QLabel(self.tr(
            """
            <div style='background-color:#F5F7FA; padding:15px; border-radius:10px;'>
                <h1 style='color:#1A5276; font-size:24px; font-weight:bold; text-align:center;'>
                    Welcome to Nova360 AI
                </h1>

                <p style='font-size:16px; color:#333333; text-align:center;'>
                    <strong>Your All-in-One AI-Powered Automation Solution</strong>
                </p><br>

                <div style='padding: 10px; border-left: 4px solid #1A5276;'>
                    <p style='font-size:14px; color:#5D6D7E; line-height:1.6; margin:0 20px;'>
                        Nova360 AI is the ultimate tool for businesses, brands, and creators looking to simplify and scale their online presence.<br>
                        Harnessing advanced AI, Nova360 AI automates social media, content creation, engagement, and growth strategies.<br>
                        Focus on what matters most while Nova360 AI handles the execution.
                    </p>
                </div><br>

                <h3 style='color:#1A5276; font-size:18px; margin-top:20px; text-align:center;'>Core Features</h3><br>

                <ul style='font-size:14px; color:#4A4A4A; padding-left: 40px;'>
                    <li style='margin-bottom:10px;'><strong>🌐 Smart Scheduling:</strong> Plan and post across multiple platforms for maximum efficiency.</li><br>
                    <li style='margin-bottom:10px;'><strong>🤖 AI-Driven Engagement:</strong> Automate replies, comments, and audience interactions seamlessly.</li><br>
                    <li><strong>📂 Integrated Management:</strong> Organize media, campaigns, and teams with ease.</li>
                </ul><br>

                <p style='font-size:14px; color:#5D6D7E; line-height:1.6; text-align:center;'>
                    Join a growing community of professionals who trust Nova360 AI to optimize their automation journey.<br>
                    Save time, grow faster, and achieve more with AI at your fingertips.
                </p><br>

                <p style='font-size:11px; color:#888888; text-align:center; margin-top:20px;'>
                    © 2024 Leopard AI | 
                    <a href='https://www.nova360pro.com' style='color:#1A5276; text-decoration:none;'>www.nova360pro.com</a>
                </p>
            </div>
            """
        ))
        layout.addWidget(label)

        # Bouton de fermeture
        close_button = QPushButton(self.tr("Fermer"))
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        # Appliquer la mise en page
        self.setLayout(layout)

        # Animation pour une transition fluide
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()
class CertificateDialog(QDialog):
    """Boîte de dialogue pour 'Certificat' (adaptée à Leopard AI)."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Certificat"))
        layout = QVBoxLayout()

        # Label avec le contenu adapté à Leopard AI
        label = QLabel(self.tr(
                "<div style='background-color:#FAF3E0; padding:15px; border-radius:8px;'>"
                "<h2 style='color:#D35400; font-size:20px; text-align:center;'>Expiration de Votre Licence</h2>"
                
                "<p style='font-size:14px; color:#4A4A4A; line-height:1.6;'>"
                "Votre licence est actuellement valide jusqu'au <strong style='color:#D35400;'>31 décembre 202x</strong>.<br>"
                "Pour continuer à profiter de toutes les fonctionnalités premium de <strong>Leopard AI</strong>, veuillez penser à renouveler votre licence avant cette date.<br>"
                "</p><br>"
                
                "<div style='padding: 10px; border-left: 4px solid #D35400; margin: 10px 0;'>"
                "<p style='font-size:13px; color:#7F8C8D; margin:0 20px;'>"
                "Après cette date, votre accès aux fonctionnalités premium sera restreint. Vous pourrez toujours accéder à votre compte mais avec des fonctionnalités limitées jusqu'au renouvellement de votre licence."
                "</p>"
                "</div><br>"
                
                "<h3 style='color:#D35400; font-size:16px;'>En Cas de Problème</h3>"
                
                "<ul style='font-size:13px; color:#4A4A4A; padding-left: 40px;'>"
                "<li style='margin-bottom:10px;'>Si votre instance ne fonctionne plus, vérifiez la connexion Internet et assurez-vous que la licence est active.</li><br>"
                "<li>Contactez notre support technique si vous rencontrez des difficultés supplémentaires.</li>"
                "</ul><br>"
                
                "<p style='font-size:12px; color:gray; text-align:center;'>"
                "Pour toute assistance, veuillez visiter <a href='https://support.leopardai.com' style='color:#D35400; text-decoration:none;'>notre centre de support</a>."
                "</p>"
                "</div>"
            ))
        layout.addWidget(label)

        # Bouton de fermeture
        close_button = QPushButton(self.tr("Fermer"))
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)

        # Animation pour rendre l'ouverture plus fluide
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
