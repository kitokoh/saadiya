import sys
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt, QTranslator, QLocale, QLibraryInfo, QPropertyAnimation
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTabWidget, QTabBar, QFrame, QLabel, QWidget,
    QSplitter, QStackedWidget
)
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QLabel, QHeaderView, QAbstractItemView, QComboBox,
                             QDialog, QDialogButtonBox, QFormLayout, QMenu, QMessageBox)

from Home.giris import SplitScreenView
from Home.login import Nova360ProApp
from Home.parametre import Nova360Ultimate
from upgrade import SpecialOfferWindow
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QProgressDialog
import os
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QProgressDialog, QLabel, QApplication
import sys
import time
from imports import *
from PyQt5.QtWidgets import QMessageBox, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QSplashScreen
from statistique.activiteprogramme import Activite
from PyQt5.QtGui import QFont

# Simulated Nova360ProApp class for demonstration purposes
class LoaderThreadTelecommande(QThread):
    finished = pyqtSignal(object)  # Signal to emit the SplitScreenView instance

    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

    def run(self):
        # Instantiate SplitScreenView in the background
        telecommande_instance = SplitScreenView(main_app=self.main_app)
        self.finished.emit(telecommande_instance)  # Emit the instance once done

class LoaderThread(QThread):
    finished = pyqtSignal(object)  # Signal to emit the Nova360ProApp instance

    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

    def run(self):
        # Instantiate Nova360ProApp in the background
        app_instance = Nova360ProApp(main_app=self.main_app)
        self.finished.emit(app_instance)  # Emit the instance once done

class LoadingScreen(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
                border-radius: 10px;
            }
            QLabel {
                color: white;
                font-size: 16px;
            }
        """)

        layout = QVBoxLayout()
        self.label = QLabel("Loading in progress, please wait...")

        layout.addWidget(self.label)
        self.setLayout(layout)
        self.resize(300, 100)

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        # Afficher le splash screen
        self.show_splash_screen()

        self.translator = QTranslator()
        self.init_language()
        self.setWindowTitle(self.tr("Modern Browser"))
        self.setWindowIcon(QIcon("browser_icon.png"))
       #self.setGeometry(0, 60, 1200, 800)
        self.setGeometry(220, 80,1200, 800)

        # Enable settings for customization
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        # Simuler une initialisation longue (remplacez cela par votre logique réelle)
        self.initUI()


        time.sleep(3)  # Simule un chargement de 3 secondes
        


        # Fermer le splash screen une fois l'initialisation terminée
        self.splash.finish(self)

    # def show_splash_screen(self):
    #     """Affiche un écran de chargement."""
    #     self.splash_pix = QPixmap("resources/images/splashScreer.png")  # Remplacez par le chemin de votre image
    #     self.splash = QSplashScreen(self.splash_pix, Qt.WindowStaysOnTopHint)
    #     self.splash.show()

    #     # Ajouter du texte au splash screen
    #     self.splash.showMessage("Chargement en cours...", Qt.AlignBottom | Qt.AlignCenter, Qt.white)
 
    def show_splash_screen(self):
        """Affiche un écran de chargement."""
        self.splash_pix = QPixmap("resources/images/splashScreer.png")  # Remplacez par le chemin de votre image
        if self.splash_pix.isNull():
                    print("Error: Splash screen image not found.")
                    return
  
  
        self.splash = QSplashScreen(self.splash_pix, Qt.WindowStaysOnTopHint)
        self.splash.setStyleSheet("background-color: #2E7D32;")  # Optional: Change background color
        self.splash.setFont(QFont("Arial", 12))

        self.splash.show()

        # Ajouter du texte au splash screen
        # Display a loading message
        loading_message = "Loading, please wait..."  # English message
        self.splash.showMessage(
            loading_message,
            Qt.AlignBottom | Qt.AlignCenter,
            Qt.white  # Text color
        )

        
    def initUI(self):
        # Main container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout with a splitter
        self.main_layout = QVBoxLayout(central_widget)  # Switch to QVBoxLayout to include the top bar
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Create the top bar with buttons
        # self.create_top_bar(self.main_layout)

        # Create the main container with a splitter
        self.central_container = QSplitter(Qt.Horizontal)
        self.central_container.setChildrenCollapsible(False)

        # Create the side menu
        self.create_side_menu()

        # Main browser container
        self.browser_container = QWidget()
        self.browser_layout = QVBoxLayout(self.browser_container)
        self.browser_layout.setContentsMargins(0, 0, 0, 0)

        # Add tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.update_search_bar_visibility)
        self.tab_widget.setStyleSheet(self.tab_widget_style())

        self.browser_layout.addWidget(self.tab_widget)

        # Add the search bar
        self.create_search_bar(self.browser_layout)

        # Add the side menu and browser container to the splitter
        self.central_container.addWidget(self.side_menu)
        self.central_container.addWidget(self.browser_container)

        # Adjust the initial size
        self.central_container.setSizes([200, 1000])
        self.main_layout.addWidget(self.central_container, stretch=1)

        # Add a first tab with a web page
        self.open_accueil_window()
        #self.add_new_tab(QUrl("https://www.nova360.turknovatech.com"), "Nova360", "resources/icons/multi_fb.ico")

    def open_instance(self):
       # self.setCentralWidget(InstanceTable(self))
       pass

    def open_about_window(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

    def find_tab_by_name(self, name):
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == name:
                return i  # Return the index if found
        return -1  # No tab found

    def open_accueil_window1(self):
        tab_name = self.tr("Accueil")  # Tab name
        existing_tab_index = self.find_tab_by_name(tab_name)
        
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
        else:
            # Otherwise, create a new tab
            accueil_widget = QLabel(self.tr("Accueil - Content here"))  # Replace with the actual widget
            self.add_new_tab(accueil_widget, tab_name, "resources/icons/multi_fb.ico")

    def open_update_window1(self):
        QMessageBox.information(self, self.tr("Upgrade"), self.tr("Upgrade your plan."))

    def open_accueil_window1(self):
        tab_name = self.tr("Accueil")

        # Check if the tab already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Show a loading message in the tab
        loading_label = QLabel(self.tr("Loading... Please wait."))
        loading_label.setAlignment(Qt.AlignCenter)
        self.add_custom_tab(loading_label, tab_name, "resources/icons/multi_fb.ico")

        # Create a progress dialog
        self.progress_dialog = QProgressDialog(self.tr("Loading Nova360Pro..."), self.tr("Cancel"), 0, 0, self)
        self.progress_dialog.setWindowTitle(self.tr("Loading"))
        self.progress_dialog.setWindowModality(Qt.ApplicationModal)
        self.progress_dialog.setCancelButton(None)  # Disable the Cancel button
        self.progress_dialog.show()

        # Start the loading thread
        self.loader_thread = LoaderThread(main_app=self)
        self.loader_thread.finished.connect(self.on_loader_finished)
        self.loader_thread.start()

    def on_loader_finished(self, app_instance):
        """
        Callback called when loading is complete.
        """
        # Close the progress dialog
        self.progress_dialog.close()

        # Update the tab with the Nova360ProApp instance
        tab_name = self.tr("Accueil")
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.removeTab(existing_tab_index)  # Remove the loading tab
            self.add_custom_tab(app_instance, tab_name, "resources/icons/multi_fb.ico")  # Add the Nova360ProApp instance
            self.nova360pro = app_instance  # Store the instance for later use

    def open_certif_window1(self):
        QMessageBox.information(self, self.tr("Nova360 - Certif"), self.tr("Certification for Nova360."))
    def open_dashboard(self):
        """
        Cette méthode affiche un écran de chargement puis initialise et retourne le widget du tableau de bord.
        """
        # Créer et afficher l'écran de chargement
        loading_screen = LoadingScreen(self)
        loading_screen.show()

        # Utiliser QTimer pour simuler un temps de chargement
        QTimer.singleShot(1000, lambda: self.finish_loading(loading_screen))

    def open_statistics_window(self):
        """
        Ouvre un nouvel onglet avec un écran de chargement,
        puis charge le tableau de bord dans cet onglet une fois prêt.
        """
        tab_name = self.tr("statistiques")

        # Vérifier si l'onglet existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Créer un widget contenant l'écran de chargement
        loading_screen = LoadingScreen(self)
        loading_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(loading_screen)
        loading_widget.setLayout(layout)

        # Ajouter un nouvel onglet avec l'écran de chargement
        new_tab_index = self.add_custom_ta(loading_widget, tab_name, "resources/icons/multi_fb.ico")
        if new_tab_index is None:
            raise RuntimeError("Failed to add a new tab. add_custom_tab returned None.")

        self.tab_widget.setCurrentIndex(new_tab_index)

        # Charger les données en arrière-plan
        QTimer.singleShot(1000, lambda: self.load_statistics_content(new_tab_index))


    def load_statistics_content(self, tab_index):
        """
        Charge le tableau de bord et remplace l'écran de chargement par le contenu dans l'onglet.
        """
        if tab_index < 0 or tab_index >= self.tab_widget.count():
            print(f"Invalid tab index: {tab_index}")
            return

        try:
            # Charger les données pour le tableau de bord
            license_checker = LicenseChecker(license_dir="C:\\bon")
            file_path = 'C:\\bon\\robot1\\data.json'
            group_counter = GroupCounter(file_path)
            Nombregroup = group_counter.count_groups()

            # Créer le widget du tableau de bord
            dash = Dashboard(
                title="wa+ CRM",
                subtitle="Analytics Overview",
                validiter=license_checker.is_license_valid(),
                Nombregroupes=Nombregroup,
                totalshare="Total partagé",
                nexttimeshare="Aucune"
            )

            # Remplacer l'écran de chargement par le tableau de bord
            self.tab_widget.removeTab(tab_index)
            self.add_custom_ta(dash, self.tr("statistiques"), "resources/icons/multi_fb.ico")
        except Exception as e:
            print(f"Erreur lors du chargement des statistiques : {e}")

    def add_custom_ta(self, widget, tab_name, icon_path):
        """
        Ajoute un nouvel onglet à la tab_widget.
        Retourne l'index de l'onglet ajouté.
        """
        icon = QIcon(icon_path) if icon_path else QIcon()
        new_tab_index = self.tab_widget.addTab(widget, icon, tab_name)
        return new_tab_index


    def open_statistics_windw(self):
        tab_name = self.tr("statistiques")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, 'statistiques')or self.statistique is None:
            self.statistique =self.open_dashboard()
        # Add the existing instance to the new tab
        self.add_custom_tab(self.statistique, tab_name, "resources/icons/multi_fb.ico")



    def open_panel_action(self):
        """
        Action associated with the 'Open Panel' button.
        """
        QMessageBox.information(self, self.tr("Action"), self.tr("Open Panel action triggered."))

    def start_robots_action(self):
        """
        Action associated with the 'Start Robots' button.
        """
        QMessageBox.information(self, self.tr("Action"), self.tr("Start Robots action triggered."))

    def choice_module_action(self):
        """
        Action associated with the 'Choice Module' button.
        """
        QMessageBox.information(self, self.tr("Action"), self.tr("Choice Module action triggered."))

    def open_uninstall_window(self):
        """
        Open the uninstall window.
        """
        QMessageBox.warning(self, self.tr("Tools - Uninstall"), self.tr("Uninstall tool triggered."))

    def open_instances_window(self):
        """
        Open the 'Instances' window.
        """
        QMessageBox.information(self, self.tr("Instances"), self.tr("Instance management."))

    def switch_language(self):
        """
        Switch between different languages.
        """
        QMessageBox.information(self, self.tr("Language"), self.tr("Change language feature triggered."))

    def open_upgrade_window(self):
        """
        Open the 'Upgrade' window.
        """
        # QMessageBox.information(self, "Upgrade", "Upgrade your plan.")
        self.add_new_tab(QUrl("https://www.nova360.turknovatech.com/pricing"), self.tr("Upgrade"), "resources/icons/tok.ico")

    # Add methods for the buttons
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

        # Navigation buttons
        self.back_button = QPushButton("<")
        self.forward_button = QPushButton(">")
        self.refresh_button = QPushButton("⟳")
        self.home_button = QPushButton("🏠")

        for btn in [self.back_button, self.forward_button, self.refresh_button, self.home_button]:
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(self.button_style())
            search_bar_layout.addWidget(btn)

        # Search bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText(self.tr("Search or enter URL"))
        self.url_bar.setStyleSheet(self.url_bar_style())
        search_bar_layout.addWidget(self.url_bar, stretch=1)

        # Connect buttons
        self.back_button.clicked.connect(self.navigate_back)
        self.forward_button.clicked.connect(self.navigate_forward)
        self.refresh_button.clicked.connect(self.refresh_page)
        self.home_button.clicked.connect(self.open_accueil_window)
       
       # self.home_button.clicked.connect(self.navigate_home)
        self.url_bar.returnPressed.connect(self.load_url)

        layout.addWidget(search_bar_frame)

        # Button to add a new tab
        self.new_tab_button = QPushButton("+")
        self.new_tab_button.setFixedSize(30, 30)
        self.new_tab_button.setStyleSheet(self.button_style())
        self.new_tab_button.clicked.connect(self.open_new_tab)
        search_bar_layout.addWidget(self.new_tab_button)

    def add_new_tab(self, content, label, icon_path="resources/icons/tok.ico"):
        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(label)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Create the tab content based on the type of `content`
        if isinstance(content, QUrl):  # If the content is a URL
            browser = QWebEngineView()
            browser.setUrl(content)
            browser.setStyleSheet("""
                QWebEngineView {
                    background-color: white;
                    color: black;
                }
            """)  # Apply a white background and black text
            widget_to_add = browser
        elif isinstance(content, QWidget):  # If the content is a custom widget
            content.setStyleSheet("""
                QWidget {
                    background-color: white;
                    color: black;
                }
            """)  # Apply a white background and black text
            widget_to_add = content
        else:
            raise TypeError(f"Unsupported type for 'content': {type(content)}")

        # Add the tab
        index = self.tab_widget.addTab(widget_to_add, "")
        self.tab_widget.setTabIcon(index, QIcon(icon_path))
        self.tab_widget.setTabText(index, label)
        self.tab_widget.setCurrentIndex(index)

        # Connect signals if necessary
        if isinstance(content, QUrl):  # Only for QWebEngineView
            widget_to_add.urlChanged.connect(self.update_url)

        # Add a general style for the tab
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

    def add_new_tab1(self, url, label, icon_path="resources/icons/tok.ico"):
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

    def open_new_tab(self, tab_name="Dashboard", icon_path="resources/icons/tok.ico"):
        self.add_new_tab(QUrl("https://www.nova360.turknovatech.com"), self.tr("Nova360"), "resources/icons/tok.ico")

    def create_top_bar(self, layout):
        self.top_bar_frame = QFrame()
        self.top_bar_frame.setStyleSheet("background-color: #282828;")
        self.top_bar_frame.setFixedHeight(40)

        top_bar_layout = QHBoxLayout(self.top_bar_frame)
        top_bar_layout.setContentsMargins(5, 5, 5, 5)

        # Native buttons
        self.minimize_button = QPushButton("─")
        self.maximize_button = QPushButton("❐")
        self.close_button = QPushButton("✖")
        self.new_tab_button = QPushButton("+")  # Button for new tab

        for btn in [self.new_tab_button, self.minimize_button, self.maximize_button, self.close_button]:
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(self.button_style())
            top_bar_layout.addWidget(btn, alignment=Qt.AlignRight)

        # Add tabs to the top bar
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

        # Connect native buttons
        self.minimize_button.clicked.connect(self.showMinimized)
        self.maximize_button.clicked.connect(self.toggle_maximized)
        self.close_button.clicked.connect(self.close)
        self.new_tab_button.clicked.connect(lambda: self.add_new_tab(QUrl("https://www.nova360.turknovatech.com"), self.tr("Nova360")))

    def toggle_maximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def add_new_tab2(self, widget, label, icon_path="resources/icons/tok.ico"):
        index = self.tab_widget.addTab(widget, "")
        self.tab_widget.setTabIcon(index, QIcon(icon_path))
        self.tab_widget.setTabText(index, label)
        self.tab_widget.setCurrentIndex(index)

    def open_accueil_window(self):
        tab_name = self.tr("Accueil")

        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Show loading message
        loading_label = QLabel(self.tr("Loading..."))
        loading_label.setAlignment(Qt.AlignCenter)
        self.add_custom_tab(loading_label, tab_name, "resources/icons/tok.ico")

        # Show progress dialog
        progress_dialog = QProgressDialog(self.tr("Loading..."), self.tr("Cancel"), 0, 0, self)
        progress_dialog.setCancelButton(None)
        progress_dialog.setWindowTitle(self.tr("Loading"))
        progress_dialog.setWindowModality(Qt.ApplicationModal)
        progress_dialog.show()

        # Start loading thread
        self.loader_thread = LoaderThread(main_app=self)
        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
            self.nova360pro = Nova360ProApp(main_app=self)  # Create the instance only once

            self.loader_thread.finished.connect(lambda app: self.update_tab_content(tab_name, self.nova360pro, progress_dialog))
        self.loader_thread.start()

    def update_tab_content(self, tab_name, app_instance, dialog):
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.removeTab(existing_tab_index)
            self.add_custom_tab(app_instance, tab_name, "resources/icons/tok.ico")
            self.nova360pro = app_instance  # Set the instance here
        dialog.close()

    # ... (rest of the code)
    def open_accueil_window2(self):
        tab_name = self.tr("Accueil")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
            self.nova360pro = Nova360ProApp(main_app=self)  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.nova360pro, tab_name, "resources/icons/tok.ico")

    def open_telecommande_window1(self):
        tab_name = self.tr("Remote Control")  # Tab name

        # Check if the tab already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Show a loading message in the tab
        loading_label = QLabel(self.tr("Loading remote control... Please wait."))
        loading_label.setAlignment(Qt.AlignCenter)
        self.add_custom_tab(loading_label, tab_name, "resources/icons/tok.ico")

        # Create a progress dialog
        self.progress_dialog = QProgressDialog(self.tr("Loading remote control..."), self.tr("Cancel"), 0, 0, self)
        self.progress_dialog.setWindowTitle(self.tr("Loading"))
        self.progress_dialog.setWindowModality(Qt.ApplicationModal)
        self.progress_dialog.setCancelButton(None)  # Disable the Cancel button
        self.progress_dialog.show()

        # Start the loading thread
        self.telecommande_loader_thread = LoaderThreadTelecommande(main_app=self)
        self.telecommande_loader_thread.finished.connect(self.on_telecommande_loader_finished)
        self.telecommande_loader_thread.start()

    def on_telecommande_loader_finished(self, telecommande_instance):
        """
        Callback called when the remote control loading is complete.
        """
        # Close the progress dialog
        self.progress_dialog.close()

        # Update the tab with the SplitScreenView instance
        tab_name = self.tr("Remote Control")
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.removeTab(existing_tab_index)  # Remove the loading tab
            self.add_custom_tab(telecommande_instance, tab_name, "resources/icons/tok.ico")  # Add the SplitScreenView instance
            self.telecommande = telecommande_instance  # Store the instance for later use
    def open_statistics_wind(self):
        tab_name = self.tr("statistiques")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, 'telecommande') or self.telecommande is None:
            self.telecommande =self.open_dashboard()
        # Add the existing instance to the new tab
        self.add_custom_tab(self.telecommande, tab_name, "resources/icons/multi_fb.ico")

    def open_telecommande_window(self):
        tab_name = self.tr("Remote Control")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, 'telecommande') or self.telecommande is None:
            self.telecommande = SplitScreenView(main_app=self)  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.telecommande, tab_name, "resources/icons/multi_fb.ico")
    def open_sheduling_window(self):
        tab_name = self.tr("shedulings")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, 'sheduling') or self.telecommande is None:
            self.sheduling = Activite()  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.sheduling, tab_name, "resources/icons/multi_fb.ico")

    def add_custom_tab(self, widget, title, icon_path=None):
        """
        Add a new tab to the QTabWidget with a widget, title, and icon.
        """
        if not hasattr(self, "tab_widget"):
            print("Error: The 'Browser' object does not have a 'tab_widget' attribute.")
            return

        index = self.tab_widget.addTab(widget, title)

        # Add an icon if provided
        if icon_path:
            icon = QIcon(icon_path)
            self.tab_widget.setTabIcon(index, icon)

        # Show the newly added tab
        self.tab_widget.setCurrentIndex(index)

    def open_search_window(self):
        """Open a tab with the content of the 'SearchWidget' class."""
        widget = SearchWidget()
        self.add_custom_tab(widget, self.tr("Search"), "resources/icons/multi_fb.ico")

    def open_settings_window(self):
        """Open a tab with the content of the 'SettingsWidget' class."""
        tab_name = self.tr("Settings")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, 'settings') or self.settings is None:
            self.settings = Nova360Ultimate(main_app=self)  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.settings, tab_name, "resources/icons/multi_fb.ico")

    def open_help_window(self):
        """Open a tab with the content of the 'HelpWidget' class."""
        widget = HelpWidget()
        self.add_custom_tab(widget, self.tr("Help"), "resources/icons/multi_fb.ico")

    def open_remote_window(self):
        """Open a tab with the content of the 'HelpWidget' class."""
        widget = HelpWidget()
        self.add_custom_tab(widget, self.tr("Help"), "resources/icons/multi_fb.ico")

    def open_upgrade_window1(self):
        tab_name = self.tr("Upgrade")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, 'upgrades') or self.upgrades is None:
            self.upgrades = SpecialOfferWindow(main_app=self)  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.upgrades, tab_name, "resources/icons/multi_fb.ico")


                                     
    
                                        
    def create_side_menu(self):
        """
        Create a side menu with control buttons at the top,
        a separator bar, and a collapsible/expandable menu.
        """
        # Side panel
        self.side_menu = QFrame()
        self.side_menu.setFixedWidth(60)  # Default, reduced menu width
        self.side_menu.setStyleSheet("""
            QFrame {
                background-color: #2F343F;  /* Background similar to ChatGPT's menu */
                border-right: 1px solid #3C4048;
            }
        """)

        # Main layout
        self.side_menu_layout = QVBoxLayout(self.side_menu)
        self.side_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.side_menu_layout.setSpacing(0)

        # --- Top row: Control buttons ---
        self.control_buttons_layout = QHBoxLayout()
        self.control_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.control_buttons_layout.setSpacing(3)  # Reduced spacing between buttons

        # Minimize button
        self.minimize_button = QPushButton("-")
        self.minimize_button.setFixedSize(20, 20)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-color: #3A3F4B;
                color: #FFFFFF;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4A4F5C;
            }
        """)
        self.minimize_button.clicked.connect(self.minimize_window)
        self.control_buttons_layout.addWidget(self.minimize_button)

        # Maximize button
        self.maximize_button = QPushButton("□")
        self.maximize_button.setFixedSize(20, 20)
        self.maximize_button.setStyleSheet("""
            QPushButton {
                background-color: #3A3F4B;
                color: #FFFFFF;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4A4F5C;
            }
        """)
        self.maximize_button.clicked.connect(self.maximize_window)
        self.control_buttons_layout.addWidget(self.maximize_button)

        # Close button
        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(20, 20)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #FF5F57;
                color: #FFFFFF;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #FF4343;
            }
        """)
        self.close_button.clicked.connect(self.close_window)
        self.control_buttons_layout.addWidget(self.close_button)

        # Add the top row to the main layout
        self.side_menu_layout.addLayout(self.control_buttons_layout)

        # --- Toggle button ---
        self.toggle_button = QPushButton("⇔")
        self.toggle_button.setFixedHeight(50)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #3A3F4B;
                color: #FFFFFF;
                border: none;
                font-size: 16px;
                padding: 0;
            }
            QPushButton:hover {
                background-color: #4A4F5C;
            }
        """)
        self.toggle_button.clicked.connect(self.toggle_side_menu)
        self.side_menu_layout.addWidget(self.toggle_button)

# --- List of main menu items ---
        menu_items = [
            # Home menu
            ("🏠", self.tr("Home"), self.open_accueil_window, []),

            # Remote control and scheduling
            ("📡", self.tr("Remote Control"), self.open_telecommande_window, []),
            ("📅", self.tr("Schedule"), self.open_sheduling_window, []),  # Changed icon to 📅 for "Schedule"

            # Settings menu with submenus
            ("⚙️", self.tr("Settings"), None, [
                ("❌", self.tr("Uninstall"), self.open_uninstall_window),
                ("🔄", self.tr("Update"), self.open_update_window),
                ("📊", self.tr("Statistics"), self.open_statistics_window),
                ("📁", self.tr("Instances"), self.open_certif_window),
                ("🛠️", self.tr("Management"), self.open_settings_window),
            ]),

            # Language selection menu
            ("🌍", self.tr("Language"), None, [
                ("🇫🇷", self.tr("French"), lambda: self.switch_language("fr")),
                ("🇬🇧", self.tr("English"), lambda: self.switch_language("en")),
                ("🇦🇪", self.tr("Arabic"), lambda: self.switch_language("ar")),
                ("🇹🇷", self.tr("Turkish"), lambda: self.switch_language("tr")),
                ("🇵🇹", self.tr("Portuguese"), lambda: self.switch_language("pt")),
            ]),

            # Support menu with submenus
            ("❓", self.tr("Support"), None, [
                ("ℹ️", self.tr("About"), self.open_about_window),
                ("📜", self.tr("Certificates"), self.open_certif_window),
                ("📞", self.tr("Contact"), self.open_contact_window),
            ]),

            # Upgrade option
            ("⬆️", self.tr("Upgrade"), self.open_upgrade_window, []),
        ]

        self.menu_buttons = []  # Store the main buttons
        self.sub_menus = {}  # Associate each main button with its submenus

        # Generate main buttons and submenus
        for icon, text, action, sub_items in menu_items:
            # Create the main button
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
                    background-color: #4A4F5C;
                }
            """)
            if action:
                button.clicked.connect(action)
            self.side_menu_layout.addWidget(button)
            self.menu_buttons.append((button, icon, text))

            # Add submenus
            if sub_items:
                sub_menu = []
                for sub_icon, sub_text, sub_action in sub_items:
                    sub_button = QPushButton(f"     {sub_icon}   {sub_text}")
                    sub_button.setFixedHeight(40)
                    sub_button.setStyleSheet("""
                        QPushButton {
                            background-color: #3A3F4B;
                            color: #FFFFFF;
                            border: none;
                            font-size: 14px;
                            text-align: left;
                            padding-left: 25px;
                        }
                        QPushButton:hover {
                            background-color: #4A4F5C;
                        }
                    """)
                    sub_button.setVisible(False)  # Hide submenus by default
                    sub_button.clicked.connect(sub_action)
                    self.side_menu_layout.addWidget(sub_button)
                    sub_menu.append(sub_button)

                self.sub_menus[button] = sub_menu
                button.clicked.connect(lambda _, b=button: self.toggle_sub_menu(b))

        # Add the panel to the main layout
        self.layout().addWidget(self.side_menu)


    def set_language_french(self):
        """Set the application language to French."""
        self.switch_language("fr")

    def set_language_english(self):
        """Set the application language to English."""
        self.switch_language("en")

    def open_contact_window(self):
        """Open the contact window."""
        self.add_new_tab(QUrl("https://script.google.com/macros/s/AKfycbzjBEtoeGcosEFv7yULAxa4RdPdTWUb7Tovtlr6Ym4EkDdttIYz2SU1s5HUHmqSaIDk1Q/exec"), self.tr("Contact"), "resources/icons/multi_fb.ico")

    def switch_language(self, language):
        """Switch the application language."""
        translator_path = os.path.join(user_data_dir, 'resources', 'lang', language, 'modules', 'main_fb_robot_translated.qm')
        
        if os.path.exists(translator_path):
            self.translator.load(translator_path)
        else:
            self.translator.load("")
        
        QApplication.instance().installTranslator(self.translator)
        self.save_language_choice(language)
        self.retranslateUi()

        # Show a green popup
        self.show_success_message(self.tr("Language changed successfully!"))

    def show_success_message(self, message):
        """Show a floating label to display the message."""
        label = QLabel(message, self)
        label.setStyleSheet("""
            QLabel {
                background-color: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        label.setAlignment(Qt.AlignCenter)
        label.setWindowFlags(Qt.FramelessWindowHint | Qt.ToolTip)
        label.adjustSize()

        # Position the label in the center of the main window
        label.move(
            (self.width() - label.width()) // 2,
            (self.height() - label.height()) // 2
        )
        label.show()

        # Automatically disappear after 3 seconds
        QTimer.singleShot(3000, label.close)

    def save_language_choice(self, language):
        """Save the selected language to the settings file."""
        preferences = {'language': language}
        with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'w') as f:
            json.dump(preferences, f)

    def retranslateUi(self):
        """Retranslate the UI elements."""
        self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        # Example of retranslating other UI elements if needed
        # self.home_action.setText(self.tr('Home'))
        # self.instance_action.setText(self.tr('Instance'))
        # self.media_action.setText(self.tr('Media'))
        # self.group_action.setText(self.tr('Groups'))
        # self.about_action.setText(self.tr('About'))
        # self.certificate_action.setText(self.tr('Certif'))
        # self.settings_menu.setTitle(self.tr('Settings'))
        # self.dark_mode_action.setText(self.tr('Enable Dark Mode'))
        # self.theme_action.setText(self.tr('Customize Theme'))
        # self.instance_install.setText(self.tr('Install'))
        # self.language_menu.setTitle(self.tr('Language'))
        # self.tools_menu.setTitle(self.tr("Tools"))
        # self.tools_menu.actions()[0].setText(self.tr("Scheduling"))
        # self.tools_menu.actions()[1].setText(self.tr("Uninstall Instances"))
        # self.tools_menu.actions()[2].setText(self.tr("Update Robot"))
        # self.tools_menu.actions()[3].setText(self.tr("Update Instance"))

    def init_language(self):
        """Initialize the application language based on user preferences or system locale."""
        if os.path.exists(os.path.join(user_data_dir, 'resources', 'settings.json')):
            with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'r') as f:
                preferences = json.load(f)
                selected_language = preferences.get('language', 'en')
        else:
            system_locale = QLocale.system().name()[:2]
            language_map = {'en': 'en', 'fr': 'fr', 'tr': 'tr', 'ar': 'ar'}
            selected_language = language_map.get(system_locale, 'en')
        self.switch_language(selected_language)

    def toggle_side_menu(self):
        """Collapse or expand the side menu."""
        if self.side_menu.width() == 60:  # Collapsed mode
            self.side_menu.setFixedWidth(200)
            for button, icon, text in self.menu_buttons:
                button.setText(f"  {icon}   {text}")
            for sub_buttons in self.sub_menus.values():
                for sub_button in sub_buttons:
                    sub_button.setFixedWidth(200)
        else:  # Expanded mode
            self.side_menu.setFixedWidth(60)
            for button, icon, text in self.menu_buttons:
                button.setText(f"  {icon}")
            for sub_buttons in self.sub_menus.values():
                for sub_button in sub_buttons:
                    sub_button.setFixedWidth(60)

    def toggle_sub_menu(self, button):
        """Show or hide the submenus associated with the main button."""
        sub_buttons = self.sub_menus.get(button, [])
        for sub_button in sub_buttons:
            sub_button.setVisible(not sub_button.isVisible())

    def open_certif_window(self):
        """Open the certificate dialog."""
        certificate_dialog = CertificateDialog(self)
        certificate_dialog.exec_()

    def open_contact_window1(self):
        """Open the contact window."""
        pass

    def open_update_window(self):
        """Open the update window."""
        pass




class AccueilWidget(QWidget):
    """Widget for the 'Accueil' tab."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(self.tr("Welcome to the Accueil tab"))
        layout.addWidget(label)
        self.setLayout(layout)


class SearchWidget(QWidget):
    """Widget for the 'Search' tab."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(self.tr("Search Page"))
        layout.addWidget(label)
        self.setLayout(layout)


class SettingsWidget(QWidget):
    """Widget for the 'Settings' tab."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(self.tr("Settings Page"))
        layout.addWidget(label)
        self.setLayout(layout)


class HelpWidget(QWidget):
    """Widget for the 'Help' tab."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(self.tr("Help Page"))
        layout.addWidget(label)
        self.setLayout(layout)


class AboutDialog(QDialog):
    """Generic dialog for 'About' Nova360 AI."""
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize and load translations
        # self.translator_manager = TranslatorManager()
        # self.translator_manager.load_translations()

        # Window configuration
        self.setWindowTitle(self.tr("About Nova360 AI"))
        layout = QVBoxLayout()

        # Main content
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

        # Close button
        close_button = QPushButton(self.tr("Close"))
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        # Apply the layout
        self.setLayout(layout)

        # Animation for smooth transition
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()


class CertificateDialog(QDialog):
    """Dialog for 'Certificate' (adapted for Leopard AI)."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Certificate"))
        layout = QVBoxLayout()

        # Label with content adapted for Leopard AI
        label = QLabel(self.tr(
                "<div style='background-color:#FAF3E0; padding:15px; border-radius:8px;'>"
                "<h2 style='color:#D35400; font-size:20px; text-align:center;'>Your License Expiration</h2>"
                
                "<p style='font-size:14px; color:#4A4A4A; line-height:1.6;'>"
                "Your license is currently valid until <strong style='color:#D35400;'>December 31, 202x</strong>.<br>"
                "To continue enjoying all the premium features of <strong>Leopardo I</strong>, please consider renewing your license before this date.<br>"
                "</p><br>"
                
                "<div style='padding: 10px; border-left: 4px solid #D35400; margin: 10px 0;'>"
                "<p style='font-size:13px; color:#7F8C8D; margin:0 20px;'>"
                "After this date, your access to premium features will be restricted. You will still be able to access your account but with limited features until your license is renewed."
                "</p>"
                "</div><br>"
                
                "<h3 style='color:#D35400; font-size:16px;'>In Case of Issues</h3>"
                
                "<ul style='font-size:13px; color:#4A4A4A; padding-left: 40px;'>"
                "<li style='margin-bottom:10px;'>If your instance stops working, check the internet connection and ensure the license is active.</li><br>"
                "<li>Contact our technical support if you encounter additional difficulties.</li>"
                "</ul><br>"
                
                "<p style='font-size:12px; color:gray; text-align:center;'>"
                "For any assistance, please visit <a href='https://support.leopardai.com' style='color:#D35400; text-decoration:none;'>our support center</a>."
                "</p>"
                "</div>"
            ))
        layout.addWidget(label)

        # Close button
        close_button = QPushButton(self.tr("Close"))
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)

        # Animation for smooth opening
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()

if __name__ == "__main__":
    # Créer l'application
    app = QApplication(sys.argv)

    # Créer et afficher la fenêtre principale
    window = Browser()
    window.show()

    # Exécuter l'application
    sys.exit(app.exec_())
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = Browser()
#     window.show()
#     sys.exit(app.exec_())