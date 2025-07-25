from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QFont
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
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QProgressDialog
import os
import sys
import time
from imports import *
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QMessageBox, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QSplashScreen
from statistique.activiteprogramme import Activite
from PyQt5.QtGui import QFont
from Home.instances import InstanceTable
from Home.premierepage import MainWindow1
from tools.editpdf import PDFEditorApp
from tools.watermarks.watermark_window import WatermarkApp
from liens.gestionliens import MainWindowLink
from promptes.promptes import PromptManager
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize, QPropertyAnimation, Qt
from PyQt5.QtGui import QIcon, QColor, QLinearGradient, QPainter
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QPushButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QStatusBar
from ui.threads import LoaderThread, LoaderThreadTelecommande
from ui.loading_screen import LoadingScreen
from ui.overlay_layout import QOverlayLayout
from PyQt5.QtWidgets import QWidgetAction
from PyQt5.QtWidgets import QListWidget, QListWidgetItem

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        # Afficher le splash screen
        self.splash = None  # Initialize the attribute

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
    # Add menu configuration storage
        self.menu_config = {
            'visible_buttons': {
                'Tools': True,
                'Settings': True,
                'Data': True,
                'Support': True
            }
        }
        # self.control_application()
        # Load saved configuration
        self.load_menu_config()






        # controller.ex
    def control_application(self):
        from demarrage.demarage import FlowManager, DatabaseManager

        db = DatabaseManager()
        flow_manager = FlowManager(db)
        flow = flow_manager.start_session()  # Détecte automatiquement le flux nécessaire

        # Exécuter les dialogues du flux (sans bloquer l'interface principale)
        for dialog_class, title in flow['dialogs']:
            dialog = dialog_class(title)
            dialog.exec_()  # Bloque jusqu'à la fermeture, mais garde la fenêtre principale visible
            # OU dialog.show() pour un affichage non bloquant (si les dialogues sont indépendants)

        flow_manager.end_session()
        db.close()

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
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Create the main container with a splitter
        self.central_container = QSplitter(Qt.Horizontal)
        self.central_container.setChildrenCollapsible(False)
        self.central_container.setHandleWidth(10)
        self.central_container.setStyleSheet("""
            QSplitter::handle {
                background: #333333;
                width: 5px;
            }
            QSplitter::handle:hover {
                background: #444444;
            }
        """)

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

        # Add widgets to splitter with drag and drop support
        self.central_container.addWidget(self.side_menu)
        self.central_container.addWidget(self.browser_container)

        # Make the splitter movable and remember position
        self.central_container.setSizes([200, 1000])
        self.main_layout.addWidget(self.central_container, stretch=1)

        # Add drag handle for side menu
        self.menu_drag_handle = QLabel("☰")
        self.menu_drag_handle.setAlignment(Qt.AlignCenter)
        self.menu_drag_handle.setStyleSheet("""
            QLabel {
                background-color: #3A3F4B;
                color: white;
                font-size: 16px;
                qproperty-alignment: AlignCenter;
            }
            QLabel:hover {
                background-color: #4A4F5C;
                cursor: move;
            }
        """)
        self.menu_drag_handle.mousePressEvent = self.start_menu_move
        self.menu_drag_handle.mouseMoveEvent = self.move_menu
        self.menu_drag_handle.mouseReleaseEvent = self.finish_menu_move

        # Add drag handle to menu
       # self.side_menu.layout().insertWidget(0, self.menu_drag_handle)

        # Add first tab
        self.open_home()
        # self.open_accueil_window()




    def initUI(self):
        # Main container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout with vertical orientation
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Create and add the top menu bar
        self.create_top_menu()
        self.main_layout.addWidget(self.top_menu, stretch=0)

        # Create the main container with a splitter
        self.central_container = QSplitter(Qt.Horizontal)
        self.central_container.setChildrenCollapsible(False)
        self.central_container.setHandleWidth(10)
        self.central_container.setStyleSheet("""
            QSplitter::handle {
                background: #333333;
                width: 5px;
            }
            QSplitter::handle:hover {
                background: #444444;
            }
        """)

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

        # Add widgets to splitter
        self.central_container.addWidget(self.browser_container)

        # Add central container to main layout
        self.main_layout.addWidget(self.central_container, stretch=1)

        # Status bar (optional)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Add first tab
        self.open_home()
        # self.control_application()
        QTimer.singleShot(200, self.control_application)  # Lance le flux après un court délai



    def control_application(self):
        from demarrage.demarage import FlowManager, DatabaseManager

        self.db = DatabaseManager()  # Conservez la connexion ouverte si nécessaire
        self.flow_manager = FlowManager( self.db)
        self.current_flow = self.flow_manager.start_session()
        self.current_step = 0

        self.run_next_dialog()

    def run_next_dialog(self):
        if self.current_step < len(self.current_flow['dialogs']):
            dialog_class, title = self.current_flow['dialogs'][self.current_step]
            self.dialog = dialog_class(title)
            self.dialog.finished.connect(self.on_dialog_finished)
            self.dialog.show()  # Affiche le dialogue sans bloquer l'interface
        else:
            self.flow_manager.end_session()  # Ferme la session si tous les dialogues sont terminés

    def on_dialog_finished(self, result):
        if result == QDialog.Accepted:
            self.current_step += 1
            self.run_next_dialog()
        else:
            # L'utilisateur a annulé, on arrête le flux
            self.flow_manager.end_session()




    def create_minimal_side_panel(self):
        """Create a minimal side panel for quick access items"""
        self.side_panel = QFrame()
        self.side_panel.setFixedWidth(150)
        self.side_panel.setStyleSheet("""
            QFrame {
                background-color: #252538;
                border-right: 1px solid #2E2E3E;
            }
        """)

        side_layout = QVBoxLayout(self.side_panel)
        side_layout.setContentsMargins(5, 10, 5, 10)
        side_layout.setSpacing(10)

        # Add quick access buttons
        quick_actions = [
            ("🏠", "Home", self.open_home),
            ("🔍", "Search", self.focus_search_bar),
            ("📁", "Files", self.open_file_manager),
            ("⚙️", "Settings", self.open_settings)
        ]

        for icon, text, callback in quick_actions:
            btn = QPushButton(f"{icon} {text}")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3A3F4B;
                    color: white;
                    border: none;
                    padding: 8px;
                    text-align: left;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #4A4F5C;
                }
            """)
            btn.clicked.connect(callback)
            side_layout.addWidget(btn)

        # Add stretch to push buttons to top
        side_layout.addStretch()

        # Optional: Add a collapse/expand button
        toggle_btn = QPushButton("◀")
        toggle_btn.setFixedHeight(20)
        toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #3A3F4B;
                color: white;
                border: none;
                padding: 0;
            }
            QPushButton:hover {
                background-color: #4A4F5C;
            }
        """)
        toggle_btn.clicked.connect(self.toggle_side_panel)
        side_layout.addWidget(toggle_btn, alignment=Qt.AlignCenter)















    def open_instance(self):

        tab_name = self.tr("Instances")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, 'Instances') or self.instances is None:
            self.instances =InstanceTable(self)
        # Add the existing instance to the new tab
        self.add_custom_tab(self.instances, tab_name, "resources/icons/multi_fb.ico")
        # self.setCentralWidget(InstanceTable(self))



    def open_about_window(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

    def find_tab_by_name(self, name):
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == name:
                return i  # Return the index if found
        return -1  # No tab found


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
        QMessageBox.information(self, self.tr("Leopardo - Certif"), self.tr("Certification for Leopardo."))
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

    def open_persona_window(self):
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

    def open_accueil_window(self):
        from Installsweb.installdisign import InstallerPage
        tab_name = self.tr("Home")

        # Vérifie si l’onglet existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Crée l’interface de l’installeur
        installer_page = MainWindow1(main_app=self)

        # Ajoute l’onglet
        new_tab_index = self.add_custom_ta(installer_page, tab_name, "resources/icons/installer.ico")
        if new_tab_index is None:
            raise RuntimeError("Failed to add a new tab.")

        self.tab_widget.setCurrentIndex(new_tab_index)


    def open_accueil_window1(self):
        from Installsweb.installdisign import InstallerPage
        tab_name = self.tr("Installer Premium")

        # Vérifie si l’onglet existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Crée l’interface de l’installeur
        installer_page = InstallerPage(self)

        # Ajoute l’onglet
        new_tab_index = self.add_custom_ta(installer_page, tab_name, "resources/icons/installer.ico")
        if new_tab_index is None:
            raise RuntimeError("Failed to add a new tab.")

        self.tab_widget.setCurrentIndex(new_tab_index)

    def open_installer_window(self):
        from Installsweb.installdisign import InstallerPage
        tab_name = self.tr("Installer Premium")

        # Vérifie si l’onglet existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Crée l’interface de l’installeur
        installer_page = InstallerPage(self)

        # Ajoute l’onglet
        new_tab_index = self.add_custom_ta(installer_page, tab_name, "resources/icons/installer.ico")
        if new_tab_index is None:
            raise RuntimeError("Failed to add a new tab.")

        self.tab_widget.setCurrentIndex(new_tab_index)

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
        self.add_new_tab(QUrl("https://www.nova360.turknovatech.com/pricing"), self.tr("🚀 Upgrade"), "resources/icons/tok.ico")
    def open_upgrade_window(self):
        """
        Ouvre la page d'abonnement + affiche une fenêtre spéciale d'offre.
        """
        # Nom de l'onglet
        tab_name = self.tr("🚀 Upgrade")

        # Ouvre le lien pricing dans un nouvel onglet
        self.add_new_tab(QUrl("https://www.nova360.turknovatech.com/pricing"), tab_name, "resources/icons/tokk.ico")
        from Upgrade.upgrade import ContactDialog # Import ici si besoin
        self.upgrades = ContactDialog()
        self.upgrades.show()
        # Ajoute aussi le module SpecialOfferWindow dans un onglet si non déjà ouvert
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        if not hasattr(self, 'upgrades') or self.upgrades is None:
            from Upgrade.upgrade import ContactDialog # Import ici si besoin
            self.upgrades = ContactDialog(parent=self)
            self.upgrades.show()
        self.add_custom_tab(self.upgrades, tab_name, "resources/icons/multi_fb.ico")

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
        self.add_new_tab(QUrl("https://leopardo-ai.web.app/"), self.tr("Leopardo"), "resources/icons/tok.ico")

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

    def open_accueil_window1(self):
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
           # self.nova360pro = Nova360ProApp(main_app=self)  # Create the instance only once
            self.nova360pro = MainWindow1(main_app=self)  # Create the instance only once

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

    def open_manuelle_window(self):
        from manuelleRobot.open import DescriptionManager
        from Home.homerun import MainWindow
        tab_name = self.tr("🚀 Run")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, ' 🚀 Run') or self.Manu is None:
            self.Manu = MainWindow(parent=self)  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.Manu, tab_name, "resources/icons/multi_sfb.ico")

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
        tab_name = self.tr("⏰ shedulings")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, '⏰ shedulings') or self.sheduling is None:
            self.sheduling = Activite()  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.sheduling, tab_name, "resources/icons/multi_fbb.ico")



    def open_editpdf_window(self):
        tab_name = self.tr("editpdf")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, 'editpdf') or self.editpdf is None:
            self.editpdf = PDFEditorApp()  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.editpdf, tab_name, "resources/icons/multi_fb.ico")
    def open_removebg_window(self):
        tab_name = self.tr("Remove Background")  # Nom de l'onglet affiché

        # Vérifie si l'onglet est déjà ouvert
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Crée un QWebEngineView pour afficher le site
        web_view = QWebEngineView()
        web_view.setUrl(QUrl("https://www.remove.bg/"))

        # Ajoute le web_view dans un nouvel onglet
        self.add_custom_tab(web_view, tab_name, "resources/icons/multi_fb.ico")




    def open_removebg_window2  (self):
        tab_name = self.tr("watermarks")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, 'watermarks') or self.telecommande is None:
            self.watermarks = WatermarkApp()  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.watermarks, tab_name, "resources/icons/multi_fb.ico")


    def open_export_window  (self):
        tab_name = self.tr("watermarks")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, 'watermarks') or self.telecommande is None:
            self.watermarks = WatermarkApp()  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.watermarks, tab_name, "resources/icons/multi_fb.ico")


    def open_import_window  (self):
        tab_name = self.tr("watermarks")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, 'watermarks') or self.telecommande is None:
            self.watermarks = WatermarkApp()  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.watermarks, tab_name, "resources/icons/multi_fb.ico")


    def open_archives_window  (self):
        tab_name = self.tr("watermarks")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, 'watermarks') or self.telecommande is None:
            self.watermarks = WatermarkApp()  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.watermarks, tab_name, "resources/icons/multi_fb.ico")





    def open_watermark_window  (self):
        tab_name = self.tr("watermarks")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, 'watermarks') or self.telecommande is None:
            self.watermarks = WatermarkApp()  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.watermarks, tab_name, "resources/icons/multi_fb.ico")




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

    def open_links_window(self):
        """Open a tab with the content of the 'SettingsWidget' class."""
        tab_name = self.tr("🔗 links")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists :


        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, '🔗 links') or self.links is None:
            self.links = MainWindowLink(main_app=self)  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.links, tab_name, "resources/icons/multi_fbb.ico")
    def open_exports_window(self):
        """Open a tab with the content of the 'SettingsWidget' class."""
        tab_name = self.tr("exports")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, 'exports') or self.settings is None:
            self.settings = Nova360Ultimate(main_app=self)  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.settings, tab_name, "resources/icons/multi_fb.ico")

    def open_imports_window(self):
        """Open a tab with the content of the 'SettingsWidget' class."""
        tab_name = self.tr("imports")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, 'imports') or self.settings is None:
            self.settings = Nova360Ultimate(main_app=self)  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.settings, tab_name, "resources/icons/multi_fb.ico")
    def open_strategies_window(self):
        """Open a tab with the content of the 'SettingsWidget' class."""
        tab_name = self.tr("strategies")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, 'strategies') or self.settings is None:
            self.settings = Nova360Ultimate(main_app=self)  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.settings, tab_name, "resources/icons/multi_fb.ico")

    def open_prompts_window(self):
        """Open a tab with the content of the 'SettingsWidget' class."""
        tab_name = self.tr("⚡prompts")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, '⚡ prompts') or self.prompts is None:
            self.prompts = PromptManager(main_app=self)  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.prompts, tab_name, "resources/icons/multi_fbc.ico")

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

    def open_contacts_window(self):
        from ModulesUI.whasapping.group_manager import ContactTable

        """Open a tab with the content of the 'SettingsWidget' class."""
        tab_name = self.tr("👥 contacts")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, '👥 contacts') or self.contacts is None:
            self.contacts = ContactTable(parent=self)  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.contacts, tab_name, "resources/icons/multi_fbb.ico")

    def open_grups_window(self):
        from facebooksmodule.group_manager import GroupTable


        """Open a tab with the content of the 'SettingsWidget' class."""
        tab_name = self.tr("👥 groups")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, '👥 groups') or self.groups is None:
            self.groups = GroupTable(parent=self)  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.groups, tab_name, "resources/icons/multi_fbb.ico")


    def add_media_page(self):
        from facebooksmodule.media_manager import MediaTable

        """Open a tab with the content of the 'SettingsWidget' class."""
        tab_name = self.tr("📺 Medias")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, '📺 Medias') or self.medias is None:
            self.medias = MediaTable(parent=self)  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.medias, tab_name, "resources/icons/multi_fbb.ico")

    def open_help_window(self):
        """Open a tab with the content of the 'HelpWidget' class."""
        widget = HelpWidget()
        self.add_custom_tab(widget, self.tr("🆘 Help"), "resources/icons/multi_fb.ico")

    def open_remote_window(self):
        """Open a tab with the content of the 'HelpWidget' class."""
        widget = HelpWidget()
        self.add_custom_tab(widget, self.tr("🆘 Help"), "resources/icons/multi_fb.ico")

    def open_upgrade_window1(self):
        tab_name = self.tr("🚀 Upgrade")  # ajoute aussi le module licene.upgrade

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, '🚀 Upgrade') or self.upgrades is None:
            self.upgrades = SpecialOfferWindow(main_app=self)  # Create the instance only once

        # Add the existing instance to the new tab
        self.add_custom_tab(self.upgrades, tab_name, "resources/icons/multi_fb.ico")

    def connect_via_ssh(self):
        import atexit

        from online.online1 import RemoteAccessModal  # Import local pour éviter les dépendances circulaires
        modal = RemoteAccessModal(self)
        modal.exec_()
        # Configuration pour fermer proprement
        atexit.register(self.cleanup)        # Ajoute ici ton vrai code de connexion
    def cleanup(self):
        """Nettoyage à la fermeture de l'application"""
        if hasattr(self, 'remote_manager') and self.remote_manager.server:
            self.remote_manager.stop_server()

    def connect_via_ftp(self):
        print("Connecting to FTP server...")

    def connect_via_api(self):
        print("Connecting to external API...")

    def connect_remote_desktop(self):
        print("Launching remote desktop session...")

    def connect_via_vpn(self):
        print("Connecting through VPN...")

    def connect_ai_service(self):
        print("Connecting to AI service...")


    def archive_to_zip(self):
        print("Archiving locally as ZIP...")

    def archive_to_gdrive(self):
        print("Uploading to Google Drive...")

    def archive_to_dropbox(self):
        print("Uploading to Dropbox...")

    def archive_to_ftp(self):
        print("Uploading via FTP...")

    def archive_to_sftp(self):
        print("Uploading via secure SFTP...")

    def archive_to_external_disk(self):
        print("Copying archive to external disk...")

    def schedule_backup(self):
        print("Opening backup scheduler...")


    def create_side_menu(self):
        """
        Create an ultra-modern side menu with dynamic button management
        """
        # Initialize user state attributes
        self.is_user_logged_in = False
        self.is_enterprise_mode = False

        # Menu configuration (default values)
        self.menu_config = {
            'visible_buttons': {
                'Tools': False,
                'Settings': False,
                'Data': False,
                'Support': False
            }
        }
        self.load_menu_config()  # Load saved configuration

        # Side panel with sleek styling
        self.side_menu = QFrame()
        self.side_menu.setFixedWidth(200)
        self.side_menu.setStyleSheet("""
            QFrame {
                background-color: #1A1A2E;
                border-right: 1px solid #2E2E3E;
            }
        """)

        # Main layout with perfect spacing
        self.side_menu_layout = QVBoxLayout(self.side_menu)
        self.side_menu_layout.setContentsMargins(0, 5, 0, 10)
        self.side_menu_layout.setSpacing(6)

        # --- Window Controls ---
        self.control_buttons_layout = QHBoxLayout()
        self.control_buttons_layout.setContentsMargins(8, 8, 8, 15)
        self.control_buttons_layout.setSpacing(6)

        # Control buttons
        self.close_button = QPushButton("✕")
        self.close_button.setFixedSize(20, 20)
        self.close_button.setStyleSheet(self.get_button_style("close"))
        self.close_button.clicked.connect(self.close_window)

        self.minimize_button = QPushButton("—")
        self.minimize_button.setFixedSize(20, 20)
        self.minimize_button.setStyleSheet(self.get_button_style("minimize"))
        self.minimize_button.clicked.connect(self.minimize_window)

        self.maximize_button = QPushButton("□")
        self.maximize_button.setFixedSize(20, 20)
        self.maximize_button.setStyleSheet(self.get_button_style("maximize"))
        self.maximize_button.clicked.connect(self.maximize_window)

        self.control_buttons_layout.addWidget(self.close_button)
        self.control_buttons_layout.addWidget(self.minimize_button)
        self.control_buttons_layout.addWidget(self.maximize_button)
        self.side_menu_layout.addLayout(self.control_buttons_layout)

        # --- Toggle Button ---
        self.toggle_button = QPushButton("⇄")
        self.toggle_button.setFixedHeight(32)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #2A2A3A;
                color: #7AA2F7;
                border: 1px solid #444466;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3A3A4A;
                color: #9DB4FF;
            }
        """)
        self.toggle_button.clicked.connect(self.toggle_side_menu)
        self.side_menu_layout.addWidget(self.toggle_button)

        # --- Menu Items ---
        menu_items = [
            # Home (fixed)
            ("🏠", self.tr("Home"), "home", self.open_home, self.tr("Main dashboard"), []),
            # ("🏠", self.tr("Home"), "home", self.open_accueil_window, self.tr("Main dashboard"), []),

            # Tools section (dynamic)
            ("🧰", self.tr("Tools"), "tools", None, self.tr("Document tools"), [
                ("📺", self.tr("Media"), "media", self.add_media_page, self.tr("Media Management"), []),
                ("👥", self.tr("Mes Contacts"), "contact", self.open_contacts_window, self.tr("liste de mes contacts"), []),
                ("🔗", self.tr("Links"), "links", self.open_links_window, self.tr("Manage links"), []),

                ("⏰", self.tr("Scheduler"), "scheduler", self.open_sheduling_window, self.tr("Task scheduling"), []),
                 ("🌍", self.tr("Grups"), "grups", self.open_grups_window, self.tr("liste de mes grops"), []),
                ("📡", self.tr("Remote"), "remote", self.open_telecommande_window, self.tr("Remote control"), []),

                ("🛠️", self.tr("Manuelle"), "Manuelle", self.open_manuelle_window, self.tr("Remote control"), []),
                # ("📝", self.tr("Edit PDF"), "edit_pdf", self.open_editpdf_window, self.tr("Modify PDF documents"), []),
                # ("💧", self.tr("Watermarks"), "watermarks", self.open_watermark_window, self.tr("Add/remove watermarks"), []),
                # ("📝", self.tr("Remove BG"), "remove_bg", self.open_removebg_window, self.tr("Remove Background"), []),
                # ("📦", self.tr("Add-On"), "add-on", self.add_on_page, self.tr("add app"), []),
                # ("📦", self.tr("Add-On"), "add-on", self.add_on_page, self.tr("add app"), []),
                # ("🕸️", self.tr("Interconnexion"), "connect", self.add_on_page, self.tr("interconnect Management"), []),


            ]),


            # Upgrade section (fixed)
            ("✨", self.tr("Beta Feature"), "beta", None, self.tr("Beata options"), [
                ("✨", self.tr("IA BETA"), "features", self.open_accueil_window, self.tr("Additional features"), []),
                ("🏛️", self.tr("Licences"), "enterprise", self.open_upgrade_window, self.tr("Enterprise features"), []),
                ("🎯", self.tr("Marketing"), "Marketing", self.open_marketing, self.tr("liste de mes contacts"), []),
                 ("🧠", self.tr("Management"), "Management", self.open_management, self.tr("liste de mes grops"), []),
                 ("💵", self.tr("Finances"), "finances", self.open_finance, self.tr("liste de mes grops"), []),

            ]),
            # Data section (dynamic)
            ("💡", self.tr("Data"), "data", None, self.tr("Data management"), [
                ("📝", self.tr("Prompts"), "prompts", self.open_prompts_window, self.tr("les promptes utiles"), []),

                ("📈", self.tr("Stats"), "stats", self.open_statistics_window, self.tr("View statistics"), []),
                ("📜", self.tr("Strategies"), "strategies", self.open_strategies_window, self.tr("les stategies possible"), []),

                # ("📤", self.tr("Export"), "export", self.open_exports_window, self.tr("Export data"), []),
                ("📥", self.tr("Import Data"), "import", self.open_imports_window, self.tr("Import data"), []),
                ("🗃️", self.tr("ADN Backup"), "backup", self.open_imports_window, self.tr("Bakup the adn  data of your entreprise"), []),

                # ("🗃️", self.tr("Backup"), "backup", None, self.tr("Backup and archive options"), [
                #     ("📁", self.tr("Local ZIP Archive"), "local_zip", self.archive_to_zip, self.tr("Compress and save locally"), []),
                #     ("☁️", self.tr("Google Drive"), "gdrive", self.archive_to_gdrive, self.tr("Upload archive to Google Drive"), []),
                #     ("📦", self.tr("Dropbox"), "dropbox", self.archive_to_dropbox, self.tr("Save archive to Dropbox"), []),
                #     ("🌐", self.tr("FTP Server"), "ftp_backup", self.archive_to_ftp, self.tr("Upload archive via FTP"), []),
                #     ("🔐", self.tr("SFTP Secure"), "sftp", self.archive_to_sftp, self.tr("Secure archive via SFTP"), []),
                #     ("🗄️", self.tr("External Disk"), "external_disk", self.archive_to_external_disk, self.tr("Save to external device"), []),
                #     ("🔁", self.tr("Schedule Backup"), "schedule_backup", self.schedule_backup, self.tr("Plan automatic backups"), []),
                # ]),

            ]),

            # Support section (dynamic)
            ("🆘", self.tr("Support"), "support", None, self.tr("Support resources"), [
                ("ℹ️", self.tr("About"), "about", self.open_about_window, self.tr("About this app"), []),
                ("📜", self.tr("Documents"), "documents", self.open_certif_window, self.tr("View licenses"), []),
                ("📞", self.tr("Contact"), "contact", self.open_contact_window, self.tr("Contact us"), []),

            ]),
            ("💎", self.tr("Upgrade"), "upgrade", self.open_upgrade_window, self.tr("Upgrade options"), [ ]),

            # Settings section (dynamic)
            ("⚙️", self.tr("Settings"), "settings", None, self.tr("Configuration"), [
                # ("📅", self.tr("Schedule"), "schedule", self.open_sheduling_window, self.tr("Configure schedules"), []),
                ("📦", self.tr("Installer"), "Installer", self.open_installer_window, self.tr("add app"), []),
                ("📦", self.tr("Add-On"), "add-on", self.add_on_page, self.tr("add app"), []),
                ("📞", self.tr("Vision"), "contact", self.open_contact_window, self.tr("vision global"), []),
                ("📞", self.tr("Com Interne"), "contact", self.open_contact_window, self.tr("vision global"), []),
                ("📞", self.tr("Com Externe"), "contact", self.open_contact_window, self.tr("vision global"), []),

                 ("🌐", self.tr("Connection"), "online_connect", self.connect_via_ssh, self.tr("Remote connection settings"), []),
                ("🗂️", self.tr("Instances"), "instances", self.open_instance, self.tr("Manage instances"), []),

                ("🌍", self.tr("Language"), "language", None, self.tr("Language settings"), [
                    ("🗼", self.tr("French"), "french", lambda: self.switch_language("fr"), self.tr("French language"), []),
                    ("🏰", self.tr("English"), "english", lambda: self.switch_language("en"), self.tr("English language"), []),
                    ("🕋", self.tr("Arabic"), "arabic", lambda: self.switch_language("ar"), self.tr("Arabic language"), []),
                    ("🕌", self.tr("Turkish"), "turkish", lambda: self.switch_language("tr"), self.tr("Turkish language"), []),
                    ("🏖️", self.tr("Portuguese"), "portuguese", lambda: self.switch_language("pt"), self.tr("Portuguese language"), []),
                ]),
                # ("🌐", self.tr("Connection"), "online_connect", None, self.tr("Remote connection settings"), [
                #     ("🖥️", self.tr("SSH Connect"), "ssh", self.connect_via_ssh, self.tr("Connect securely via SSH"), []),
                #     # ("📂", self.tr("FTP Server"), "ftp", self.connect_via_ftp, self.tr("Access files via FTP"), []),
                #     # ("🔗", self.tr("API Link"), "api", self.connect_via_api, self.tr("Connect to external APIs"), []),
                #     # ("🛰️", self.tr("Remote Desktop"), "remote_desktop", self.connect_remote_desktop, self.tr("Access remote desktop sessions"), []),
                #     # ("🔒", self.tr("VPN Connect"), "vpn", self.connect_via_vpn, self.tr("Connect securely using VPN"), []),
                #     # ("🧠", self.tr("AI Service"), "ai_service", self.connect_ai_service, self.tr("Connect to external AI platforms"), []),

                # ])
            ]),


        ]

        self.menu_buttons = []
        self.sub_menus = {}
        self.current_open_menu = None
        self.menu_button_refs = {}  # For dynamic visibility control

        for icon, text, identifier, action, tooltip, sub_items in menu_items:
            # Main menu button
            button = QPushButton(f"  {icon}  {text}")
            button.setFixedHeight(40)
            button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #D0D0FF;
                    border: none;
                    font-size: 14px;
                    text-align: left;
                    padding-left: 12px;
                    border-radius: 5px;
                    transition: all 0.2s ease;
                }
                QPushButton:hover {
                    background-color: #2A2A4A;
                    color: #FFFFFF;
                }
            """)
            button.setToolTip(f"<b>{text}</b><br>{tooltip}")

            if action:
                button.clicked.connect(action)

            self.side_menu_layout.addWidget(button)
            self.menu_buttons.append((button, icon, text))

            # Store reference for dynamic visibility control (except fixed buttons)
            if identifier not in ["home", "tools"]:
                self.menu_button_refs[text] = button

            # Create submenus if they exist
            if sub_items:
                sub_menu = []
                for sub_icon, sub_text, sub_id, sub_action, sub_tooltip, nested_sub_items in sub_items:
                    sub_btn = QPushButton(f"    {sub_icon}  {sub_text}")
                    sub_btn.setFixedHeight(36)
                    sub_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #252538;
                            color: #C0C0FF;
                            border: none;
                            font-size: 13px;
                            text-align: left;
                            padding-left: 24px;
                            border-radius: 5px;
                            transition: all 0.2s ease;
                        }
                        QPushButton:hover {
                            background-color: #303048;
                            color: #FFFFFF;
                        }
                    """)
                    sub_btn.setToolTip(f"<b>{sub_text}</b><br>{sub_tooltip}")
                    sub_btn.setVisible(False)

                    if sub_action:
                        sub_btn.clicked.connect(sub_action)

                    self.side_menu_layout.addWidget(sub_btn)
                    sub_menu.append(sub_btn)

                    # Handle nested submenus
                    if nested_sub_items:
                        nested_menu = []
                        for nest_icon, nest_text, nest_id, nest_action, nest_tooltip, _ in nested_sub_items:
                            nest_btn = QPushButton(f"      {nest_icon}  {nest_text}")
                            nest_btn.setFixedHeight(34)
                            nest_btn.setStyleSheet("""
                                QPushButton {
                                    background-color: #202034;
                                    color: #B0B0FF;
                                    border: none;
                                    font-size: 12px;
                                    text-align: left;
                                    padding-left: 36px;
                                    border-radius: 5px;
                                    transition: all 0.2s ease;
                                }
                                QPushButton:hover {
                                    background-color: #282842;
                                    color: #FFFFFF;
                                }
                            """)
                            nest_btn.setToolTip(f"<b>{nest_text}</b><br>{nest_tooltip}")
                            nest_btn.setVisible(False)

                            if nest_action:
                                nest_btn.clicked.connect(nest_action)

                            self.side_menu_layout.addWidget(nest_btn)
                            nested_menu.append(nest_btn)

                        self.sub_menus[sub_btn] = nested_menu
                        sub_btn.clicked.connect(lambda _, b=sub_btn: self.toggle_sub_menu(b))

                self.sub_menus[button] = sub_menu
                button.clicked.connect(self.create_menu_handler(button))

        # Add stretch
        self.side_menu_layout.addStretch()


        class ShinyButton(QPushButton):
            def paintEvent(self, event):
                painter = QPainter(self)
                painter.setRenderHint(QPainter.Antialiasing)

                # Fond avec dégradé
                gradient = QLinearGradient(0, 0, self.width(), 0)
                gradient.setColorAt(0, QColor(100, 130, 255))
                gradient.setColorAt(0.5, QColor(160, 90, 255))
                gradient.setColorAt(1, QColor(255, 70, 150))

                painter.setBrush(gradient)
                painter.setPen(Qt.NoPen)
                painter.drawRoundedRect(self.rect(), 8, 8)

                # Texte et icône
                painter.setPen(QColor(255, 255, 255))
                painter.drawText(self.rect(), Qt.AlignCenter, self.text())

        # --- Menu Configuration Button ---
        self.menu_config_button = ShinyButton("⚙️ MENU")
        self.menu_config_button.setFixedHeight(48)
        self.menu_config_button.setFixedWidth(180)
        self.menu_config_button.setIcon(QIcon.fromTheme("preferences-system"))
        self.menu_config_button.setIconSize(QSize(24, 24))
        self.menu_config_button.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
                padding-left: 10px;
                border: none;
                margin: 10px 5px;
            }
        """)

        # Effet de brillance animée
        self.glow_animation = QPropertyAnimation(self.menu_config_button, b"iconSize")
        self.glow_animation.setDuration(1500)
        self.glow_animation.setLoopCount(-1)  # Infinite loop
        self.glow_animation.setKeyValueAt(0, QSize(24, 24))
        self.glow_animation.setKeyValueAt(0.5, QSize(28, 28))
        self.glow_animation.setKeyValueAt(1, QSize(24, 24))
        self.glow_animation.start()

        # Ombre portée intense
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(100, 130, 255, 150))
        self.menu_config_button.setGraphicsEffect(shadow)

        # Animation au survol
        self.hover_animation = QPropertyAnimation(self.menu_config_button, b"geometry")
        self.hover_animation.setDuration(200)

        def animate_hover(enter):
            if enter:
                self.hover_animation.setEndValue(self.menu_config_button.geometry().adjusted(-5, -2, 5, 2))
            else:
                self.hover_animation.setEndValue(self.menu_config_button.geometry().adjusted(5, 2, -5, -2))
            self.hover_animation.start()

        self.menu_config_button.enterEvent = lambda e: animate_hover(True)
        self.menu_config_button.leaveEvent = lambda e: animate_hover(False)

        self.menu_config_button.clicked.connect(self.show_menu_settings_dialog)
        self.side_menu_layout.addWidget(self.menu_config_button)

        # --- User Section ---
        self.user_frame = QFrame()
        self.user_frame.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-top: 1px solid #333333;
            }
        """)
        self.user_layout = QVBoxLayout(self.user_frame)
        self.user_layout.setContentsMargins(5, 10, 5, 10)
        self.user_layout.setSpacing(8)

        # User profile button
        self.user_button = QPushButton("👤 Guest")
        self.user_button.setFixedHeight(40)
        self.user_button.setStyleSheet("""
            QPushButton {
                background-color: #3A3F4B;
                color: white;
                border: none;
                font-size: 14px;
                text-align: left;
                padding-left: 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4A4F5C;
            }
        """)
        self.user_button.clicked.connect(self.toggle_user_menu)
        self.user_layout.addWidget(self.user_button)

        # User menu container
        self.user_menu = QFrame()
        self.user_menu.setVisible(False)
        self.user_menu.setStyleSheet("""
            QFrame {
                background-color: #2A2A2A;
                border-radius: 5px;
            }
        """)
        self.user_menu_layout = QVBoxLayout(self.user_menu)
        self.user_menu_layout.setContentsMargins(0, 5, 0, 5)
        self.user_menu_layout.setSpacing(3)

        # User menu buttons
        self.login_button = QPushButton("🔑 Login")
        self.logout_button = QPushButton("🚪 Logout")
        self.enterprise_button = QPushButton("🏢 Enterprise Mode")
        self.personal_button = QPushButton("👤 Personal Mode")
        self.settings_button = QPushButton("⚙️ Settings")
        self.switch_button = QPushButton("👥 Switch Account")
        self.subscription_button = QPushButton("🛒 Subscription")

        for btn in [self.login_button, self.logout_button, self.enterprise_button,
                    self.personal_button, self.settings_button, self.switch_button,
                    self.subscription_button]:
            btn.setFixedHeight(36)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3A3F4B;
                    color: white;
                    border: none;
                    font-size: 13px;
                    text-align: left;
                    padding-left: 20px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #4A4F5C;
                }
            """)

        # Connect buttons
        self.login_button.clicked.connect(self.user_login)
        self.logout_button.clicked.connect(self.user_logout)
        self.enterprise_button.clicked.connect(self.switch_to_enterprise)
        self.personal_button.clicked.connect(self.switch_to_personal)
        self.settings_button.clicked.connect(self.open_user_settings)
        self.switch_button.clicked.connect(self.switch_account)
        self.subscription_button.clicked.connect(self.open_subscription)

        # Add buttons to layout
        self.user_menu_layout.addWidget(self.login_button)
        self.user_menu_layout.addWidget(self.logout_button)
        self.user_menu_layout.addWidget(self.enterprise_button)
        self.user_menu_layout.addWidget(self.personal_button)
        self.user_menu_layout.addWidget(self.settings_button)
        self.user_menu_layout.addWidget(self.switch_button)
        self.user_menu_layout.addWidget(self.subscription_button)

        self.user_layout.addWidget(self.user_menu)
        self.side_menu_layout.addWidget(self.user_frame)

        # Update initial visibility
        self.update_user_buttons()
        self.update_menu_visibility()

        # Add to main layout
        self.layout().addWidget(self.side_menu)
        self.is_menu_expanded = False
        self.is_user_menu_expanded = False
=======
from ui.browser import Browser
>>>>>>> REPLACE
