import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTabWidget, QTabBar, QFrame, QLabel, QWidget,
    QSplitter, QStackedWidget
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from login import Nova360ProApp

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
        self.add_new_tab(QUrl("https://www.nova360.turknovatech.com"), "Leopard", "new_tab_icon.ico")

    def find_tab_by_name(self, name):
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == name:
                return i  # Renvoie l'index si trouvé
        return -1  # Aucun onglet trouvé

    def open_accueil_window(self):
        tab_name = "Accueil"  # Nom de l'onglet
        existing_tab_index = self.find_tab_by_name(tab_name)
        
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.tab_widget.setCurrentIndex(existing_tab_index)
        else:
            # Sinon, créez un nouvel onglet
            accueil_widget = QLabel("Accueil - Contenu ici")  # Remplacez par le widget réel
            self.add_new_tab(accueil_widget, tab_name, "accueil_icon.ico")

    def create_side_menu(self):
        # Panneau latéral
        self.side_menu = QFrame()
        self.side_menu.setFixedWidth(150)
        self.side_menu.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #2C2C2C, stop:1 #1E1E1E);
                border-right: 1px solid #444;
            }
        """)

        # Layout principal
        self.side_menu_layout = QVBoxLayout(self.side_menu)
        self.side_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.side_menu_layout.setSpacing(10)

        # Bouton pour masquer/afficher le menu
        self.toggle_button = QPushButton("⇔")
        self.toggle_button.setFixedSize(30, 30)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #3A3A3A;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        self.toggle_button.clicked.connect(self.toggle_side_menu)

        # Ajout du bouton au menu et en dehors pour qu'il reste toujours visible
        self.side_menu_layout.addWidget(self.toggle_button, alignment=Qt.AlignRight)

        # Ajouter des options avec icônes
        menu_items = [
            ("🏠", "Accueil", self.open_accueil_window),
            ("🔍", "Rechercher", self.open_search_window),
            ("⚙️", "Paramètres", self.open_settings_window),
            ("❓", "Aide", self.open_help_window),
        ]

        for icon, text, action in menu_items:
            button = QPushButton(f"{icon}  {text}")
            button.setFixedHeight(40)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2C2C2C;
                    color: #FFFFFF;
                    border: none;
                    text-align: left;
                    padding-left: 10px;
                }
                QPushButton:hover {
                    background-color: #3A3A3A;
                }
            """)
            button.clicked.connect(action)
            self.side_menu_layout.addWidget(button)

        # Ajout d'un séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #444;")
        self.side_menu_layout.addWidget(separator)

        # Espacer les options restantes
        self.side_menu_layout.addStretch()

    # # Méthodes pour ouvrir les fenêtres
    # def open_accueil_window(self):
    #     self.accueil_window = Nova360ProApp()
    #     self.accueil_window.show()





    def toggle_side_menu(self):
        # Animation fluide pour afficher/masquer le menu
        new_width = 30 if self.side_menu.width() > 100 else 150
        self.side_menu.setFixedWidth(new_width)
        # Met à jour la position du bouton si nécessaire
        self.toggle_button.setText("⇔" if new_width == 150 else "⇐")




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
            url = QUrl("https://www.google.com")
            self.add_new_tab(url, "Google", "google_icon.ico")

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
            widget_to_add = browser
        elif isinstance(content, QWidget):  # Si le contenu est un widget personnalisé
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
            current_browser.setUrl(QUrl("https://www.google.com"))

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
        self.add_new_tab(QUrl("https://www.google.com"), "Google", "new_tab_icon.ico")


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
        self.new_tab_button.clicked.connect(lambda: self.add_new_tab(QUrl("https://www.google.com"), "Nouvel onglet"))


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

    def open_accueil_window1(self):
        """Ouvre un onglet avec le contenu de la classe 'AccueilWidget'."""

            # Créer une instance de Nova360Pro et transmettre self comme main_app
        self.nova360pro = Nova360ProApp(main_app=self)
        self.add_custom_tab(self.nova360pro, "Nova360", "nova_icon.ico")
    def open_accueil_window(self):
        tab_name = "Nova360"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

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
        widget = SettingsWidget()
        self.add_custom_tab(widget, "Paramètres", "settings_icon.ico")

    def open_help_window(self):
        """Ouvre un onglet avec le contenu de la classe 'HelpWidget'."""
        widget = HelpWidget()
        self.add_custom_tab(widget, "Aide", "help_icon.ico")


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




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
