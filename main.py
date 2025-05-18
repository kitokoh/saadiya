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
# from licenceYonetimi.upgrade import SpecialOfferWindow
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QProgressDialog
import os
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QProgressDialog, QLabel, QApplication
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
# Simulated Nova360ProApp class for demonstration purposes
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize, QPropertyAnimation, Qt
from PyQt5.QtGui import QIcon, QColor, QLinearGradient, QPainter
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QPushButton
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QStatusBar

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

from PyQt5.QtWidgets import QLayout
from PyQt5.QtWidgets import QWidgetItem
from PyQt5.QtWidgets import QWidgetAction

class QOverlayLayout(QLayout):
    """Un layout personnalisé pour superposer des widgets (comme un badge sur une icône)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = []
        self.positions = {}  # Pour stocker les alignements
        
    def addWidget(self, widget, alignment=None):
        item = QWidgetItem(widget)
        self.addItem(item)
        if alignment is not None:
            self.positions[widget] = alignment
        return item
        
    def addItem(self, item):
        self.items.append(item)
        
    def count(self):
        return len(self.items)
    
    def itemAt(self, index):
        if 0 <= index < len(self.items):
            return self.items[index]
        return None
    
    def takeAt(self, index):
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        return None
    
    def setGeometry(self, rect):
        super().setGeometry(rect)
        
        for i in range(self.count()):
            item = self.itemAt(i)
            if item is None:
                continue
                
            widget = item.widget()
            if widget is None:
                continue
                
            # Position par défaut (remplit tout l'espace)
            widget_rect = rect
                
            # Appliquer l'alignement si spécifié
            if widget in self.positions:
                alignment = self.positions[widget]
                size = widget.sizeHint()
                
                if alignment & Qt.AlignTop:
                    widget_rect.setTop(rect.top())
                    widget_rect.setBottom(rect.top() + size.height())
                elif alignment & Qt.AlignBottom:
                    widget_rect.setTop(rect.bottom() - size.height())
                    widget_rect.setBottom(rect.bottom())
                    
                if alignment & Qt.AlignLeft:
                    widget_rect.setLeft(rect.left())
                    widget_rect.setRight(rect.left() + size.width())
                elif alignment & Qt.AlignRight:
                    widget_rect.setLeft(rect.right() - size.width())
                    widget_rect.setRight(rect.right())
                
                if alignment & Qt.AlignHCenter:
                    widget_rect.setLeft(rect.left() + (rect.width() - size.width()) // 2)
                    widget_rect.setRight(widget_rect.left() + size.width())
                elif alignment & Qt.AlignVCenter:
                    widget_rect.setTop(rect.top() + (rect.height() - size.height()) // 2)
                    widget_rect.setBottom(widget_rect.top() + size.height())
            
            widget.setGeometry(widget_rect)

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
        
        # Load saved configuration
        self.load_menu_config() 





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
        tab_name = self.tr("▶️ Run")  # Tab name (matches the label used in add_custom_tab)

        # Check if a tab with this name already exists
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # If the tab already exists, select it
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Otherwise, create a unique instance of Nova360ProApp and add a new tab
        if not hasattr(self, '▶️ Run') or self.Manu is None:
            self.Manu = DescriptionManager(parent=self)  # Create the instance only once

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



    def create_top_menu1(self):
        """
        Create a modern top menu bar with dropdown functionality
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

        # Top menu bar with sleek styling
        self.top_menu = QFrame()
        self.top_menu.setFixedHeight(50)
        # self.top_menu.setStyleSheet("""
        #     QFrame {
        #         background-color: #1A1A2E;
        #         border-bottom: 1px solid #2E2E3E;
        #     }
        # """)
        self.top_menu.setStyleSheet("""
            QFrame {
                background-color: #f0f2f5;
                border-bottom: 1px solid #d1d5db;
            }
        """)
        # Main layout with horizontal orientation
        self.top_menu_layout = QHBoxLayout(self.top_menu)
        self.top_menu_layout.setContentsMargins(5, 5, 5, 5)
        self.top_menu_layout.setSpacing(10)

        # --- App Logo/Title ---
        self.app_title = QLabel("Leopardo AI")
        # self.app_title.setStyleSheet("""
        #     QLabel {
        #         color: #7AA2F7;
        #         font-size: 18px;
        #         font-weight: bold;
        #         padding: 0 15px;
        #     }
        # """)


        self.app_title.setStyleSheet("""
        QLabel {
            color: #3b82f6;  /* Bleu vif */
            font-size: 18px;
            font-weight: bold;
            padding: 0 15px;
        }
    """)
        self.top_menu_layout.addWidget(self.app_title)

        # --- Window Controls --- (moved to right side)
        self.control_buttons_layout = QHBoxLayout()
        self.control_buttons_layout.setSpacing(5)

        # Control buttons
        self.minimize_button = QPushButton("—")
        self.minimize_button.setFixedSize(20, 20)
        self.minimize_button.setStyleSheet(self.get_button_style("minimize"))
        self.minimize_button.clicked.connect(self.minimize_window)

        self.maximize_button = QPushButton("□")
        self.maximize_button.setFixedSize(20, 20)
        self.maximize_button.setStyleSheet(self.get_button_style("maximize"))
        self.maximize_button.clicked.connect(self.maximize_window)

        self.close_button = QPushButton("✕")
        self.close_button.setFixedSize(20, 20)
        self.close_button.setStyleSheet(self.get_button_style("close"))
        self.close_button.clicked.connect(self.close_window)

        self.control_buttons_layout.addWidget(self.minimize_button)
        self.control_buttons_layout.addWidget(self.maximize_button)
        self.control_buttons_layout.addWidget(self.close_button)

        # --- Menu Items ---
        self.menu_bar = QHBoxLayout()
        self.menu_bar.setSpacing(5)
        
        # Menu items data structure
        menu_items = [
            # Home (fixed)
            ("🏠", self.tr("Home"), "home", self.open_home, self.tr("Main dashboard"), []),
            
            # Tools section (dynamic)
            ("🧰", self.tr("Tools"), "tools", None, self.tr("Document tools"), [
                ("📺", self.tr("Media"), "media", self.add_media_page, self.tr("Media Management"), []),
                ("🌍", self.tr("My Groups"), "grups", self.open_grups_window, self.tr("Group list"), []),

                ("👥", self.tr("Address book"), "contact", self.open_contacts_window, self.tr("Contact list"), []),
                ("🔗", self.tr("Links"), "links", self.open_links_window, self.tr("Manage links"), []),
                # ("⏰", self.tr("Scheduler"), "scheduler", self.open_sheduling_window, self.tr("Task scheduling"), []),
                # ("📡", self.tr("Remote"), "remote", self.open_telecommande_window, self.tr("Remote control"), []),
                # ("🛠️", self.tr("Manual"), "Manuelle", self.open_manuelle_window, self.tr("Manual tools"), []),
                 ("📝", self.tr("Desc & Prompts"), "prompts", self.open_prompts_window, self.tr("Useful prompts"), []),

                ("🧠", self.tr("Management"), "Management", self.open_management, self.tr("Management tools"), []),

            ]),
            
            # Beta Features section
            ("✨", self.tr("Plans"), "Plans", None, self.tr("Plans options"), [
                # ("✨", self.tr("AI BETA"), "features", self.open_accueil_window, self.tr("Additional features"), []),
                # ("🏛️", self.tr("Licenses"), "enterprise", self.open_upgrade_window, self.tr("Enterprise features"), []),
                ("🎯", self.tr("Marketing"), "Marketing", self.open_marketing, self.tr("Marketing tools"), []),
                ("📜", self.tr("Protocles"), "Protocoles", self.open_management, self.tr("Protocoles tools"), []),

                # ("____________", self.tr(""), "Ads", self.open_management, self.tr("Ads tools"), []),
                ("♟️", self.tr("Strategies"), "strategies", self.open_strategies_window, self.tr("Possible strategies"), []),


                ("💸", self.tr("ADS"), "Ads", self.open_management, self.tr("Ads tools"), []),
                ("⏰", self.tr("Scheduler"), "scheduler", self.open_sheduling_window, self.tr("Task scheduling"), []),

                # ("💵", self.tr("Finances"), "finances", self.open_finance, self.tr("Financial tools"), []),
                # ("🪙", self.tr("Crypto Mining"), "Management", self.open_management, self.tr("Management tools"), []),
                # ("🪙", self.tr("Tading"), "Management", self.open_management, self.tr("Management tools"), []),

            ]),
            


            # Settings section
            ("⏯️", self.tr("Run"), "Run", self.open_manuelle_window, self.tr("Run Now"), [
                # ("✨", self.tr("AI BETA"), "features", self.open_accueil_window, self.tr("Additional features"), []),
                # ("🛠️", self.tr("Manual"), "Manuelle", self.open_manuelle_window, self.tr("Manual tools"), []),

            ]),          
            
            # Settings section
            ("⚙️", self.tr("Settings"), "settings", None, self.tr("Configuration"), [
                # ("✨", self.tr("AI BETA"), "features", self.open_accueil_window, self.tr("Additional features"), []),
                ("🔌", self.tr("Add-On"), "add-on", self.add_on_page, self.tr("Add app"), []),
                ("📡", self.tr("Remote"), "remote", self.open_telecommande_window, self.tr("Remote control"), []),

                ("📦", self.tr("Installer"), "Installer", self.open_installer_window, self.tr("Add app"), []),
                # ("🔌", self.tr("Add-On"), "add-on", self.add_on_page, self.tr("Add app"), []),
                ("🌐", self.tr("Connection"), "online_connect", self.connect_via_ssh, self.tr("Remote connection settings"), []),
                ("🗂️", self.tr("Instances"), "instances", self.open_instance, self.tr("Manage instances"), []),
                ("💎", self.tr("Upgrade"), "upgrade", self.open_upgrade_window, self.tr("Upgrade options"), []),

            ]),
            # Upgrade button

            # Data section
            ("💡", self.tr("Data Banks"), "data", None, self.tr("Data management"), [
                # ("📝", self.tr("Prompts"), "prompts", self.open_prompts_window, self.tr("Useful prompts"), []),
                ("🎭", self.tr("Prospects "), "Persona", self.open_persona_window, self.tr("View statistics"), []),
                ("🌍", self.tr("Groups "), "grups", self.open_grups_window, self.tr("Group list"), []),
                
                ("📈", self.tr("Stats"), "stats", self.open_statistics_window, self.tr("View statistics"), []),
                ("📥", self.tr("Import Data"), "import", self.open_imports_window, self.tr("Import data"), []),
                ("🗃️", self.tr("ADN Backup"), "backup", self.open_imports_window, self.tr("Backup enterprise data"), []),
            ]),
            


            ("🌍", self.tr("Language"), "language", None, self.tr("Language settings"), [
                    ("🗼", self.tr("French"), "french", lambda: self.switch_language("fr"), self.tr("French language"), []),
                    ("🏰", self.tr("English"), "english", lambda: self.switch_language("en"), self.tr("English language"), []),
                    ("🕋", self.tr("Arabic"), "arabic", lambda: self.switch_language("ar"), self.tr("Arabic language"), []),
                    ("🕌", self.tr("Turkish"), "turkish", lambda: self.switch_language("tr"), self.tr("Turkish language"), []),
                    ("🏖️", self.tr("Portuguese"), "portuguese", lambda: self.switch_language("pt"), self.tr("Portuguese language"), []),
            ]),
                        # Support section
            ("🆘", self.tr("Support"), "support", None, self.tr("Support resources"), [
                ("ℹ️", self.tr("About"), "about", self.open_about_window, self.tr("About this app"), []),
                ("📜", self.tr("Documents"), "documents", self.open_certif_window, self.tr("View licenses"), []),
                ("📞", self.tr("Contact"), "contact", self.open_contact_window, self.tr("Contact us"), []),
            ]),
        ]

        self.menu_buttons = []
        self.sub_menus = {}
        self.current_open_menu = None
        self.menu_button_refs = {}  # For dynamic visibility control

        for icon, text, identifier, action, tooltip, sub_items in menu_items:
            # Create menu button
            button = QPushButton(f"{icon} {text}")
            button.setFixedHeight(36)
            # button.setStyleSheet("""
            #     QPushButton {
            #         background-color: transparent;
            #         color: #D0D0FF;
            #         border: none;
            #         font-size: 14px;
            #         padding: 5px 10px;
            #         border-radius: 4px;
            #         transition: all 0.2s ease;
            #     }
            #     QPushButton:hover {
            #         background-color: #2A2A4A;
            #         color: #FFFFFF;
            #     }
            # """)

            button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #4b5563;
                    border: none;
                    font-size: 14px;
                    padding: 5px 10px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #e5e7eb;
                    color: #1f2937;
                }
            """)


            button.setToolTip(f"<b>{text}</b><br>{tooltip}")
            
            if action:
                button.clicked.connect(action)
            
            # Store reference for dynamic visibility control
            if identifier not in ["home", "tools","data","support","upgrade","settings","beta"]:
                self.menu_button_refs[text] = button
            
            # Create dropdown menu if there are sub-items
            if sub_items:
                menu = QMenu()
                # menu.setStyleSheet("""
                #     QMenu {
                #         background-color: #252538;
                #         border: 1px solid #2E2E3E;
                #         padding: 5px;
                #     }
                #     QMenu::item {
                #         color: #C0C0FF;
                #         padding: 5px 20px;
                #         margin: 2px;
                #     }
                #     QMenu::item:selected {
                #         background-color: #3A3A5A;
                #         color: white;
                #     }
                #     QMenu::item:disabled {
                #         color: #606080;
                #     }
                # """)

                menu.setStyleSheet("""
                    QMenu {
                        background-color: #ffffff;  /* Blanc pur */
                        border: 1px solid #d1d5db;
                        padding: 5px;
                    }
                    QMenu::item {
                        color: #4b5563;
                        padding: 5px 20px;
                        margin: 2px;
                    }
                    QMenu::item:selected {
                        background-color: #f3f4f6;  /* Gris très clair */
                        color: #111827;  /* Noir profond */
                    }
                    QMenu::item:disabled {
                        color: #606080;
                    }
                """)




                for sub_icon, sub_text, sub_id, sub_action, sub_tooltip, nested_sub_items in sub_items:
                    if nested_sub_items:
                        # Create submenu for nested items
                        submenu = QMenu(sub_text)
                        submenu.setStyleSheet(menu.styleSheet())
                        
                        for nest_icon, nest_text, nest_id, nest_action, nest_tooltip, _ in nested_sub_items:
                            action = submenu.addAction(f"{nest_icon} {nest_text}")
                            action.setToolTip(nest_tooltip)
                            if nest_action:
                                action.triggered.connect(nest_action)
                        
                        menu.addMenu(submenu)
                    else:
                        # Regular menu item
                        action = menu.addAction(f"{sub_icon} {sub_text}")
                        action.setToolTip(sub_tooltip)
                        if sub_action:
                            action.triggered.connect(sub_action)
                
                button.setMenu(menu)
            
            self.menu_bar.addWidget(button)
            self.menu_buttons.append(button)

        # Add stretch before window controls

        self.top_menu_layout.addLayout(self.menu_bar)
        self.top_menu_layout.addStretch()

        self.create_notif()

        self.top_menu_layout.addStretch()

        self.top_menu_layout.addLayout(self.control_buttons_layout)


        # --- User Profile Section ---
        self.user_button = QPushButton("👤 Guest")
        self.user_button.setFixedHeight(36)
        # self.user_button.setStyleSheet("""
        #     QPushButton {
        #         background-color: #3A3F4B;
        #         color: white;
        #         border: none;
        #         font-size: 14px;
        #         padding: 5px 15px;
        #         border-radius: 4px;
        #     }
        #     QPushButton:hover {
        #         background-color: #4A4F5C;
        #     }
        # """)
        

                # User button light style
        self.user_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #4b5563;
                border: 1px solid #d1d5db;
                font-size: 14px;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f3f4f6;
            }
        """)
        # User menu
        self.user_menu = QMenu()
        self.user_menu.setStyleSheet("""
            QMenu {
                background-color: #252538;
                border: 1px solid #2E2E3E;
                padding: 5px;
            }
            QMenu::item {
                color: #C0C0FF;
                padding: 5px 20px;
                margin: 2px;
            }
            QMenu::item:selected {
                background-color: #3A3A5A;
                color: white;
            }
        """)
        
        # Add user menu actions
        self.login_action = self.user_menu.addAction("🔑 Login")
        self.logout_action = self.user_menu.addAction("🚪 Logout")
        self.user_menu.addSeparator()
        self.enterprise_action = self.user_menu.addAction("🏢 Enterprise Mode")
        self.personal_action = self.user_menu.addAction("👤 Personal Mode")
        self.user_menu.addSeparator()
        self.settings_action = self.user_menu.addAction("♻️ Update")
        self.switch_action = self.user_menu.addAction("👥 Switch Account")
        self.subscription_action = self.user_menu.addAction("🛒 Subscription")
        self.my_persona_action = self.user_menu.addAction(" 🎭 My Persona")        
        # Connect actions
        self.login_action.triggered.connect(self.user_login)
        self.logout_action.triggered.connect(self.user_logout)
        self.enterprise_action.triggered.connect(self.switch_to_enterprise)
        self.personal_action.triggered.connect(self.switch_to_personal)
        self.settings_action.triggered.connect(self.open_user_settings)
        self.switch_action.triggered.connect(self.switch_account)
        self.subscription_action.triggered.connect(self.open_subscription)
        self.my_persona_action.triggered.connect(self.open_my_persona)
        
        self.user_button.setMenu(self.user_menu)
        self.top_menu_layout.addWidget(self.user_button)

        # Update initial visibility
        self.update_user_buttons()
        self.update_menu_visibility()

        # Add to main layout (at the top)
            # self.layout().insertWidget(0, self.top_menu)
        self.main_layout.insertWidget(0, self.top_menu)

        # Mettez à jour les badges
        self.update_notification_count()
        self.update_message_count()

    def create_top_menu1(self):
        """
        Create a modern, responsive top menu bar with dropdown functionality
        with improved styling, organization and performance

                """
        # Charger l'état de connexion depuis la session
        self.load_session_state()
                

       # Initialize user state attributes
        self.is_user_logged_in = False
        self.is_enterprise_mode = False
        
        # Menu configuration with default values
        self.menu_config = {
            'visible_buttons': {
                'Tools': True,
                'Settings': True,
                'Data': True,
                'Support': True
            }
        }
        self.load_menu_config()  # Load saved configuration

        # Create top menu container
        self.top_menu = QFrame()
        self.top_menu.setFixedHeight(50)
        self.top_menu.setStyleSheet("""
            QFrame {
                background-color: #f8fafc;
                border-bottom: 1px solid #e2e8f0;
            }
        """)

        # Main layout with proper spacing and margins
        self.top_menu_layout = QHBoxLayout(self.top_menu)
        self.top_menu_layout.setContentsMargins(5, 5, 5, 5)
        self.top_menu_layout.setSpacing(10)

        # --- App Logo/Title ---
        self.app_title = QLabel("Leopardo AI")
        self.app_title.setStyleSheet("""
            QLabel {
                color: #2563eb;
                font-size: 18px;
                font-weight: bold;
                padding: 0 15px;
            }
        """)
        self.top_menu_layout.addWidget(self.app_title)

        # --- Menu Items ---
        self.menu_bar = QHBoxLayout()
        self.menu_bar.setSpacing(5)
        
        # Define menu structure in a more organized way
        menu_structure = {
            "Home": {
                "icon": "🏠",
                "action": self.open_home,
                "tooltip": "Main dashboard",
                "submenu": None
            },
            "Tools": {
                "icon": "🧰",
                "action": None,
                "tooltip": "Document tools",
                "submenu": [
                    ("📺", "Media", self.add_media_page, "Media Management"),
                    ("🌍", "My Groups", self.open_grups_window, "Group list"),
                    ("👥", "Address book", self.open_contacts_window, "Contact list"),
                    ("🔗", "Links", self.open_links_window, "Manage links"),
                    ("📝", "Desc & Prompts", self.open_prompts_window, "Useful prompts"),
                    ("🧠", "Management", self.open_management, "Management tools")
                ]
            },
            "Plans": {
                "icon": "✨",
                "action": None,
                "tooltip": "Plans options",
                "submenu": [
                    ("🎯", "Marketing", self.open_marketing, "Marketing tools"),
                    ("📜", "Protocles", self.open_management, "Protocoles tools"),
                    ("♟️", "Strategies", self.open_strategies_window, "Possible strategies"),
                    ("💸", "ADS", self.open_management, "Ads tools"),
                    ("⏰", "Scheduler", self.open_sheduling_window, "Task scheduling")
                ]
            },
            "Run": {
                "icon": "⏯️",
                "action": self.open_manuelle_window,
                "tooltip": "Run Now",
                "submenu": None
            },
            "Settings": {
                "icon": "⚙️",
                "action": None,
                "tooltip": "Configuration",
                "submenu": [
                    ("🔌", "Add-On", self.add_on_page, "Add app"),
                    ("📡", "Remote", self.open_telecommande_window, "Remote control"),
                    ("📦", "Installer", self.open_installer_window, "Add app"),
                    ("🌐", "Connection", self.connect_via_ssh, "Remote connection settings"),
                    ("🗂️", "Instances", self.open_instance, "Manage instances"),
                    ("💎", "Upgrade", self.open_upgrade_window, "Upgrade options")
                ]
            },
            "Data Banks": {
                "icon": "💡",
                "action": None,
                "tooltip": "Data management",
                "submenu": [
                    ("🎭", "Prospects", self.open_persona_window, "View statistics"),
                    ("🌍", "Groups", self.open_grups_window, "Group list"),
                    ("📈", "Stats", self.open_statistics_window, "View statistics"),
                    ("📥", "Import Data", self.open_imports_window, "Import data"),
                    ("🗃️", "ADN Backup", self.open_imports_window, "Backup enterprise data")
                ]
            },
            "Language": {
                "icon": "🌍",
                "action": None,
                "tooltip": "Language settings",
                "submenu": [
                    ("🗼", "French", lambda: self.switch_language("fr"), "French language"),
                    ("🏰", "English", lambda: self.switch_language("en"), "English language"),
                    ("🕋", "Arabic", lambda: self.switch_language("ar"), "Arabic language"),
                    ("🕌", "Turkish", lambda: self.switch_language("tr"), "Turkish language"),
                    ("🏖️", "Portuguese", lambda: self.switch_language("pt"), "Portuguese language")
                ]
            },
            "Support": {
                "icon": "🆘",
                "action": None,
                "tooltip": "Support resources",
                "submenu": [
                    ("ℹ️", "About", self.open_about_window, "About this app"),
                    ("📜", "Documents", self.open_certif_window, "View licenses"),
                    ("📞", "Contact", self.open_contact_window, "Contact us")
                ]
            }
        }

        self.menu_buttons = []
        self.sub_menus = {}
        self.current_open_menu = None
        self.menu_button_refs = {}  # For dynamic visibility control

        # Create menu items from structure
        for text, config in menu_structure.items():
            button = self._create_menu_button(
                icon=config["icon"],
                text=text,
                action=config["action"],
                tooltip=config["tooltip"]
            )
            
            # Store reference for dynamic visibility control
            if text not in ["Home"]:
                self.menu_button_refs[text] = button
            
            # Create dropdown menu if there are sub-items
            if config["submenu"]:
                menu = self._create_dropdown_menu(config["submenu"])
                button.setMenu(menu)
            
            self.menu_bar.addWidget(button)
            self.menu_buttons.append(button)

        self.top_menu_layout.addLayout(self.menu_bar)
        self.top_menu_layout.addStretch()

        # Create notification area
        self.create_notif()

        # --- Window Controls ---
        self.control_buttons_layout = QHBoxLayout()
        self.control_buttons_layout.setSpacing(5)

        # Control buttons
        control_buttons = [
            ("—", "minimize", self.minimize_window),
            ("□", "maximize", self.maximize_window),
            ("✕", "close", self.close_window)
        ]

        for text, style_type, action in control_buttons:
            btn = QPushButton(text)
            btn.setFixedSize(20, 20)
            btn.setStyleSheet(self._get_control_button_style(style_type))
            btn.clicked.connect(action)
            self.control_buttons_layout.addWidget(btn)

        self.top_menu_layout.addLayout(self.control_buttons_layout)

        # --- User Profile Section ---
        self.user_button = QPushButton("👤 Guest")
        self.user_button.setFixedHeight(36)
        self.user_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #4b5563;
                border: 1px solid #d1d5db;
                font-size: 14px;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f3f4f6;
            }
        """)

        # User menu
        self.user_menu = self._create_user_menu()
        self.user_button.setMenu(self.user_menu)
        self.top_menu_layout.addWidget(self.user_button)

        # Update initial visibility
        self.update_user_buttons()
        self.update_menu_visibility()

        # Add to main layout (at the top)
        self.main_layout.insertWidget(0, self.top_menu)

        # Update badges
        self.update_notification_count()
        self.update_message_count()

        # --- User Profile Section ---
        self.update_user_profile_section()  # Nouvelle méthode pour gérer la section utilisateur
        
        # Connecter les signaux
        if hasattr(self, 'login_module'):
            self.login_module.connection_successful.connect(self.handle_successful_login)
    def create_top_menu(self):
        """
        Crée une barre de menu supérieure moderne avec fonctionnalités déroulantes
        et gestion complète de l'authentification utilisateur.
        """
        # Initialisation de l'état utilisateur
        self.is_user_logged_in = False
        self.is_enterprise_mode = False
        self.current_username = "Guest"
        
        # Charger l'état de connexion
        self.load_session_state()

        # Configuration du menu
        self.menu_config = {
            'visible_buttons': {
                'Tools': False,
                'Settings': False,
                'Data': False,
                'Support': False
            }
        }
        self.load_menu_config()

        # Création du conteneur principal
        self.top_menu = QFrame()
        self.top_menu.setFixedHeight(50)
        self.top_menu.setStyleSheet("""
            QFrame {
                background-color: #f8fafc;
                border-bottom: 1px solid #e2e8f0;
            }
        """)

        # Layout principal
        self.top_menu_layout = QHBoxLayout(self.top_menu)
        self.top_menu_layout.setContentsMargins(5, 5, 5, 5)
        self.top_menu_layout.setSpacing(10)

        # --- Logo / Titre de l'application ---
        self.app_title = QLabel("Leopardo AI")
        self.app_title.setStyleSheet("""
            QLabel {
                color: #2563eb;
                font-size: 18px;
                font-weight: bold;
                padding: 0 15px;
            }
        """)
        self.top_menu_layout.addWidget(self.app_title)

        # --- Barre de menu ---
        self.menu_bar = QHBoxLayout()
        self.menu_bar.setSpacing(5)
        
        # Structure des éléments de menu
        menu_items = [
            ("🏠", self.tr("Home"), "home", self.open_home, self.tr("Main dashboard"), []),
            ("🧰", self.tr("Tools"), "tools", None, self.tr("Document tools"), [
                ("📺", self.tr("Media"), "media", self.add_media_page, self.tr("Media Management"), []),
                ("🌍", self.tr("My Groups"), "grups", self.open_grups_window, self.tr("Group list"), []),
                ("👥", self.tr("Address book"), "contact", self.open_contacts_window, self.tr("Contact list"), []),
                ("🔗", self.tr("Links"), "links", self.open_links_window, self.tr("Manage links"), []),
                ("📝", self.tr("Desc & Prompts"), "prompts", self.open_prompts_window, self.tr("Useful prompts"), []),
                ("🧠", self.tr("Management"), "Management", self.open_management, self.tr("Management tools"), []),
            ]),
            ("✨", self.tr("Plans"), "Plans", None, self.tr("Plans options"), [
                ("🎯", self.tr("Marketing"), "Marketing", self.open_marketing, self.tr("Marketing tools"), []),
                ("📜", self.tr("Protocles"), "Protocoles", self.open_management, self.tr("Protocoles tools"), []),
                ("♟️", self.tr("Strategies"), "strategies", self.open_strategies_window, self.tr("Possible strategies"), []),
                ("💸", self.tr("ADS"), "Ads", self.open_management, self.tr("Ads tools"), []),
                ("⏰", self.tr("Scheduler"), "scheduler", self.open_sheduling_window, self.tr("Task scheduling"), []),
            ]),
            ("⏯️", self.tr("Run"), "Run", self.open_manuelle_window, self.tr("Run Now"), []),
            ("⚙️", self.tr("Settings"), "settings", None, self.tr("Configuration"), [
                ("🔌", self.tr("Add-On"), "add-on", self.add_on_page, self.tr("Add app"), []),
                ("📡", self.tr("Remote"), "remote", self.open_telecommande_window, self.tr("Remote control"), []),
                ("📦", self.tr("Installer"), "Installer", self.open_installer_window, self.tr("Add app"), []),
                ("🌐", self.tr("Connection"), "online_connect", self.connect_via_ssh, self.tr("Remote connection settings"), []),
                ("🗂️", self.tr("Instances"), "instances", self.open_instance, self.tr("Manage instances"), []),
                ("💎", self.tr("Upgrade"), "upgrade", self.open_upgrade_window, self.tr("Upgrade options"), []),
            ]),
            ("💡", self.tr("Data Banks"), "data", None, self.tr("Data management"), [
                ("🎭", self.tr("Prospects "), "Persona", self.open_persona_window, self.tr("View statistics"), []),
                ("🌍", self.tr("Groups "), "grups", self.open_grups_window, self.tr("Group list"), []),
                ("📈", self.tr("Stats"), "stats", self.open_statistics_window, self.tr("View statistics"), []),
                ("📥", self.tr("Import Data"), "import", self.open_imports_window, self.tr("Import data"), []),
                ("🗃️", self.tr("ADN Backup"), "backup", self.open_imports_window, self.tr("Backup enterprise data"), []),
            ]),
            ("🌍", self.tr("Language"), "language", None, self.tr("Language settings"), [
                ("🗼", self.tr("French"), "french", lambda: self.switch_language("fr"), self.tr("French language"), []),
                ("🏰", self.tr("English"), "english", lambda: self.switch_language("en"), self.tr("English language"), []),
                ("🕋", self.tr("Arabic"), "arabic", lambda: self.switch_language("ar"), self.tr("Arabic language"), []),
                ("🕌", self.tr("Turkish"), "turkish", lambda: self.switch_language("tr"), self.tr("Turkish language"), []),
                ("🏖️", self.tr("Portuguese"), "portuguese", lambda: self.switch_language("pt"), self.tr("Portuguese language"), []),
            ]),
            ("🆘", self.tr("Support"), "support", None, self.tr("Support resources"), [
                ("ℹ️", self.tr("About"), "about", self.open_about_window, self.tr("About this app"), []),
                ("📜", self.tr("Documents"), "documents", self.open_certif_window, self.tr("View licenses"), []),
                ("📞", self.tr("Contact"), "contact", self.open_contact_window, self.tr("Contact us"), []),
            ]),
        ]

        # Création des boutons de menu
        self.menu_buttons = []
        self.sub_menus = {}
        self.current_open_menu = None
        self.menu_button_refs = {}

        for icon, text, identifier, action, tooltip, sub_items in menu_items:
            button = QPushButton(f"{icon} {text}")
            button.setFixedHeight(36)
            button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #4b5563;
                    border: none;
                    font-size: 14px;
                    padding: 5px 10px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #e5e7eb;
                    color: #1f2937;
                }
            """)
            button.setToolTip(f"<b>{text}</b><br>{tooltip}")
            
            if action:
                button.clicked.connect(action)
            
            if identifier not in ["home", "tools", "data", "support", "upgrade", "settings", "beta"]:
                self.menu_button_refs[text] = button
            
            if sub_items:
                menu = QMenu()
                menu.setStyleSheet("""
                    QMenu {
                        background-color: #ffffff;
                        border: 1px solid #d1d5db;
                        padding: 5px;
                    }
                    QMenu::item {
                        color: #4b5563;
                        padding: 5px 20px;
                        margin: 2px;
                    }
                    QMenu::item:selected {
                        background-color: #f3f4f6;
                        color: #111827;
                    }
                    QMenu::item:disabled {
                        color: #9ca3af;
                    }
                """)

                for sub_icon, sub_text, sub_id, sub_action, sub_tooltip, nested_sub_items in sub_items:
                    if nested_sub_items:
                        submenu = QMenu(sub_text)
                        submenu.setStyleSheet(menu.styleSheet())
                        
                        for nest_icon, nest_text, nest_id, nest_action, nest_tooltip, _ in nested_sub_items:
                            action = submenu.addAction(f"{nest_icon} {nest_text}")
                            action.setToolTip(nest_tooltip)
                            if nest_action:
                                action.triggered.connect(nest_action)
                        
                        menu.addMenu(submenu)
                    else:
                        action = menu.addAction(f"{sub_icon} {sub_text}")
                        action.setToolTip(sub_tooltip)
                        if sub_action:
                            action.triggered.connect(sub_action)
                
                button.setMenu(menu)
            
            self.menu_bar.addWidget(button)
            self.menu_buttons.append(button)

        self.top_menu_layout.addLayout(self.menu_bar)
        self.top_menu_layout.addStretch()

        # --- Section de notification ---
        self.create_notif()
        self.top_menu_layout.addStretch()

        # --- Contrôles de fenêtre ---
        self.control_buttons_layout = QHBoxLayout()
        self.control_buttons_layout.setSpacing(5)

        minimize_button = QPushButton("—")
        minimize_button.setFixedSize(20, 20)
        minimize_button.setStyleSheet(self.get_control_button_style("minimize"))
        minimize_button.clicked.connect(self.minimize_window)

        maximize_button = QPushButton("□")
        maximize_button.setFixedSize(20, 20)
        maximize_button.setStyleSheet(self.get_control_button_style("maximize"))
        maximize_button.clicked.connect(self.maximize_window)

        close_button = QPushButton("✕")
        close_button.setFixedSize(20, 20)
        close_button.setStyleSheet(self.get_control_button_style("close"))
        close_button.clicked.connect(self.close_window)

        self.control_buttons_layout.addWidget(minimize_button)
        self.control_buttons_layout.addWidget(maximize_button)
        self.control_buttons_layout.addWidget(close_button)

        # --- Section utilisateur ---
        self.user_button = QPushButton(f"👤 {self.current_username}")
        self.user_button.setFixedHeight(36)
        self.user_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #4b5563;
                border: 1px solid #d1d5db;
                font-size: 14px;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f3f4f6;
            }
        """)

        # Menu utilisateur
        self.user_menu = QMenu()
        self.user_menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff;
                border: 1px solid #d1d5db;
                padding: 5px;
            }
            QMenu::item {
                color: #4b5563;
                padding: 5px 20px;
                margin: 2px;
            }
            QMenu::item:selected {
                background-color: #f3f4f6;
                color: #111827;
            }
        """)
        
        # Actions du menu utilisateur
        self.login_action = self.user_menu.addAction("🔑 " + self.tr("Login"))
        self.logout_action = self.user_menu.addAction("🚪 " + self.tr("Logout"))
        self.user_menu.addSeparator()
        self.enterprise_action = self.user_menu.addAction("🏢 " + self.tr("Enterprise Mode"))
        self.personal_action = self.user_menu.addAction("👤 " + self.tr("Personal Mode"))
        self.user_menu.addSeparator()
        self.settings_action = self.user_menu.addAction("♻️ " + self.tr("Update"))
        self.switch_action = self.user_menu.addAction("👥 " + self.tr("Switch Account"))
        self.subscription_action = self.user_menu.addAction("🛒 " + self.tr("Subscription"))
        self.my_persona_action = self.user_menu.addAction("🎭 " + self.tr("My Persona"))
        
        # Connexions des signaux
        self.login_action.triggered.connect(self.user_login)
        self.logout_action.triggered.connect(self.user_logout)
        self.enterprise_action.triggered.connect(self.switch_to_enterprise)
        self.personal_action.triggered.connect(self.switch_to_personal)
        self.settings_action.triggered.connect(self.open_user_settings)
        self.switch_action.triggered.connect(self.switch_account)
        self.subscription_action.triggered.connect(self.open_subscription)
        self.my_persona_action.triggered.connect(self.open_my_persona)
        
        self.user_button.setMenu(self.user_menu)
        self.top_menu_layout.addWidget(self.user_button)

        # Ajouter les contrôles de fenêtre
        self.top_menu_layout.addLayout(self.control_buttons_layout)

        # Mettre à jour l'interface en fonction de l'état de connexion
        self.update_user_profile_section()
        self.update_menu_visibility()

        # Ajouter le menu top au layout principal
        self.main_layout.insertWidget(0, self.top_menu)

        # Mettre à jour les badges de notification
        self.update_notification_count()
        self.update_message_count()


    def load_session_state(self):
        """Charge l'état de connexion depuis le fichier de session"""
        session_file = os.path.join(user_data_dir, 'resources', 'data', 'session.json')
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
                self.is_user_logged_in = session_data.get('is_logged_in', False)
                self.current_username = session_data.get('username', 'Guest')
        except (FileNotFoundError, json.JSONDecodeError):
            self.is_user_logged_in = False
            self.current_username = 'Guest'

    def update_user_profile_section(self):
        """Met à jour la section utilisateur en fonction de l'état de connexion"""
        if self.is_user_logged_in:
            self.user_button.setText(f"👤 {self.current_username}")
            self.login_action.setVisible(False)
            self.logout_action.setVisible(True)
            self.switch_action.setVisible(True)
        else:
            self.user_button.setText("👤 Guest")
            self.login_action.setVisible(True)
            self.logout_action.setVisible(False)
            self.switch_action.setVisible(False)

    def handle_successful_login(self):
        """Gère une connexion réussie"""
        self.load_session_state()
        self.update_user_profile_section()
        self.update_menu_visibility()  # Si vous avez besoin de changer la visibilité des menus
        
        # Activer les fonctionnalités premium si nécessaire
        if self.is_enterprise_mode:
            self.enable_premium_features()
    def user_login(self):
        """Ouvre la fenêtre de connexion"""
        from ui.login import LoginModule

        self.login_module = LoginModule()
        self.login_module.show()

    def user_logout(self):
        """Gère la déconnexion de l'utilisateur"""
        session_file = os.path.join(user_data_dir, 'resources', 'data', 'session.json')
        if os.path.exists(session_file):
            os.remove(session_file)
        
        self.is_user_logged_in = False
        self.current_username = 'Guest'
        self.update_user_profile_section()
        
        QMessageBox.information(
            self, 
            self.tr("Déconnexion réussie"), 
            self.tr("Vous avez été déconnecté avec succès.")
        )

    def switch_account(self):
        """Permet de changer de compte"""
        self.user_logout()  # On déconnecte d'abord
        self.user_login()   # Puis on propose une nouvelle connexion
        
    def _create_menu_button(self, icon, text, action=None, tooltip=""):
        """Helper method to create consistent menu buttons"""
        button = QPushButton(f"{icon} {text}")
        button.setFixedHeight(36)
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #4b5563;
                border: none;
                font-size: 14px;
                padding: 5px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e5e7eb;
                color: #1f2937;
            }
        """)
        button.setToolTip(f"<b>{text}</b><br>{tooltip}")
        
        if action:
            button.clicked.connect(action)
        
        return button

    def _create_dropdown_menu(self, items):
        """Helper method to create consistent dropdown menus"""
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff;
                border: 1px solid #d1d5db;
                padding: 5px;
            }
            QMenu::item {
                color: #4b5563;
                padding: 5px 20px;
                margin: 2px;
            }
            QMenu::item:selected {
                background-color: #f3f4f6;
                color: #111827;
            }
            QMenu::item:disabled {
                color: #9ca3af;
            }
        """)

        for icon, text, action, tooltip in items:
            menu_action = menu.addAction(f"{icon} {text}")
            menu_action.setToolTip(tooltip)
            if action:
                menu_action.triggered.connect(action)
        
        return menu

    def _create_user_menu(self):
        """Helper method to create user menu"""
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff;
                border: 1px solid #d1d5db;
                padding: 5px;
            }
            QMenu::item {
                color: #4b5563;
                padding: 5px 20px;
                margin: 2px;
            }
            QMenu::item:selected {
                background-color: #f3f4f6;
                color: #111827;
            }
        """)
        
        # Add user menu actions
        self.login_action = menu.addAction("🔑 Login")
        self.logout_action = menu.addAction("🚪 Logout")
        menu.addSeparator()
        self.enterprise_action = menu.addAction("🏢 Enterprise Mode")
        self.personal_action = menu.addAction("👤 Personal Mode")
        menu.addSeparator()
        self.settings_action = menu.addAction("♻️ Update")
        self.switch_action = menu.addAction("👥 Switch Account")
        self.subscription_action = menu.addAction("🛒 Subscription")
        self.my_persona_action = menu.addAction("🎭 My Persona")
        
        # Connect actions
        self.login_action.triggered.connect(self.user_login)
        self.logout_action.triggered.connect(self.user_logout)
        self.enterprise_action.triggered.connect(self.switch_to_enterprise)
        self.personal_action.triggered.connect(self.switch_to_personal)
        self.settings_action.triggered.connect(self.open_user_settings)
        self.switch_action.triggered.connect(self.switch_account)
        self.subscription_action.triggered.connect(self.open_subscription)
        self.my_persona_action.triggered.connect(self.open_my_persona)
        
        return menu

    def get_control_button_style(self, button_type):
        """Return appropriate style for window control buttons"""
        styles = {
            "minimize": """
                QPushButton {
                    background-color: #f59e0b;
                    color: white;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #d97706;
                }
            """,
            "maximize": """
                QPushButton {
                    background-color: #10b981;
                    color: white;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #059669;
                }
            """,
            "close": """
                QPushButton {
                    background-color: #ef4444;
                    color: white;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #dc2626;
                }
            """
        }
        return styles.get(button_type, "")


    def add_sample_notification(self, title, content, time):
        """Ajoute une notification exemple au menu"""
        notification_action = QWidgetAction(self.notification_menu)
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold;")
        
        content_label = QLabel(content)
        content_label.setWordWrap(True)
        content_label.setStyleSheet("color: #6b7280; font-size: 12px;")
        
        time_label = QLabel(time)
        time_label.setStyleSheet("color: #9ca3af; font-size: 10px;")
        time_label.setAlignment(Qt.AlignRight)
        
        layout.addWidget(title_label)
        layout.addWidget(content_label)
        layout.addWidget(time_label)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)
        
        notification_action.setDefaultWidget(widget)
        self.notification_menu.insertAction(self.notification_menu.actions()[1], notification_action)
        
        # Mettre à jour le compteur
        current_count = int(self.notification_badge.text())
        self.notification_badge.setText(str(current_count + 1))

    def add_sample_message(self, sender, subject, preview, time):
        """Ajoute un message exemple au menu"""
        message_action = QWidgetAction(self.message_menu)
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        sender_label = QLabel(sender)
        sender_label.setStyleSheet("font-weight: bold;")
        
        subject_label = QLabel(subject)
        subject_label.setStyleSheet("color: #3b82f6;")
        
        preview_label = QLabel(preview)
        preview_label.setWordWrap(True)
        preview_label.setStyleSheet("color: #6b7280; font-size: 12px;")
        
        time_label = QLabel(time)
        time_label.setStyleSheet("color: #9ca3af; font-size: 10px;")
        time_label.setAlignment(Qt.AlignRight)
        
        layout.addWidget(sender_label)
        layout.addWidget(subject_label)
        layout.addWidget(preview_label)
        layout.addWidget(time_label)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)
        
        message_action.setDefaultWidget(widget)
        self.message_menu.insertAction(self.message_menu.actions()[1], message_action)
        
        # Mettre à jour le compteur
        current_count = int(self.message_badge.text())
        self.message_badge.setText(str(current_count + 1))

    def clear_all_notifications(self):
        """Marque toutes les notifications comme lues"""
        self.notification_badge.setText("0")
        # Ici vous pourriez aussi vider la liste des notifications
        # ou marquer les éléments comme lus dans votre système

    def open_new_message(self):
        """Ouvre la fenêtre de composition d'un nouveau message"""
        # Implémentez cette fonction selon vos besoins
        print("Ouvrir l'éditeur de message")

    def update_notification_count(self):
        """Met à jour le compteur de notifications"""
        # Implémentez la logique pour récupérer le nombre réel de notifications
        # Par exemple:
        # count = get_unread_notification_count()
        # self.notification_badge.setText(str(count))
        pass

    def update_message_count(self):
        """Met à jour le compteur de messages"""
        # Implémentez la logique pour récupérer le nombre réel de messages non lus
        # Par exemple:
        # count = get_unread_message_count()
        # self.message_badge.setText(str(count))
        pass


    # Assurez-vous que QOverlayLayout est bien défini ailleurs ou importé si c'est une classe custom

    def create_notif(self):
        def create_button_with_badge(emoji_text, badge_color):
            button = QToolButton()
            button.setText(emoji_text)
            button.setFont(QFont("Segoe UI Emoji", 10))  # Police emoji lisible
            button.setStyleSheet("""
                QToolButton {
                    background-color: transparent;
                    border: none;
                    padding: 5px;
                }
                QToolButton:hover {
                    background-color: #e5e7eb;
                    border-radius: 6px;
                }
            """)
            
            badge = QLabel("0")
            badge.setStyleSheet(f"""
                QLabel {{
                    background-color: {badge_color};
                    color: white;
                    border-radius: 8px;
                    padding: 1px 5px;
                    font-size: 10px;
                    min-width: 6px;
                    max-width: 6px;
                    min-height: 6px;
                    max-height: 6px;
                }}
            """)
            badge.setAlignment(Qt.AlignCenter)

            # Superposer badge au bouton
            overlay = QOverlayLayout(button)
            overlay.addWidget(badge, alignment=Qt.AlignTop | Qt.AlignRight)
            
            return button, badge

        # --- Notifications ---
        self.notification_button, self.notification_badge = create_button_with_badge("🔔", "#ef4444")
        self.notification_menu = QMenu()
        self.notification_menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #d1d5db;
                min-width: 100px;
                max-height: 200px;
            }
            QMenu::item {
                padding: 8px 15px;
                border-bottom: 1px solid #f3f4f6;
            }
            QMenu::item:selected {
                background-color: #f3f4f6;
            }
        """)

        notif_header = QWidgetAction(self.notification_menu)
        notif_widget = QWidget()
        notif_layout = QHBoxLayout(notif_widget)
        notif_label = QLabel("🔔 Notifications")
        notif_label.setStyleSheet("font-weight: bold;")
        clear_btn = QPushButton("Tout marquer comme lu")
        clear_btn.setStyleSheet("""
            QPushButton {
                border: none;
                color: #3b82f6;
                background: transparent;
                padding: 0;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        clear_btn.clicked.connect(self.clear_all_notifications)
        notif_layout.addWidget(notif_label)
        notif_layout.addStretch()
        notif_layout.addWidget(clear_btn)
        notif_header.setDefaultWidget(notif_widget)
        self.notification_menu.addAction(notif_header)
        self.notification_menu.addSeparator()

        self.add_sample_notification("Nouveau message", "Visite https://leopardo-ai.web.app/ ", "5 min")
        self.notification_button.setMenu(self.notification_menu)
        self.notification_button.setPopupMode(QToolButton.InstantPopup)

        # --- Messages ---
        self.message_button, self.message_badge = create_button_with_badge("💬", "#3b82f6")
        self.message_menu = QMenu()
        self.message_menu.setStyleSheet(self.notification_menu.styleSheet())

        msg_header = QWidgetAction(self.message_menu)
        msg_widget = QWidget()
        msg_layout = QHBoxLayout(msg_widget)
        msg_label = QLabel("💬 Messages")
        msg_label.setStyleSheet("font-weight: bold;")
        new_msg_btn = QPushButton("Nouveau message")
        new_msg_btn.setStyleSheet(clear_btn.styleSheet())
        new_msg_btn.clicked.connect(self.open_new_message)
        msg_layout.addWidget(msg_label)
        msg_layout.addStretch()
        msg_layout.addWidget(new_msg_btn)
        msg_header.setDefaultWidget(msg_widget)
        self.message_menu.addAction(msg_header)
        self.message_menu.addSeparator()

        self.add_sample_message("Jean Dupont", "Réunion demain", "Bonjour, nous avons une réunion demain à 10h...", "10 min")
        self.message_button.setMenu(self.message_menu)
        self.message_button.setPopupMode(QToolButton.InstantPopup)

        # --- Ajout au layout ---
        # self.top_menu_layout.addWidget(self.message_button)
        self.top_menu_layout.addWidget(self.notification_button)


    def tab_widget_style(self):
        return """
            QTabWidget::pane {
                border: 1px solid #d1d5db;
                background: #ffffff;
            }
            QTabBar::tab {
                background: #f3f4f6;
                color: #4b5563;
                padding: 8px 12px;
                border: 1px solid #d1d5db;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                color: #111827;
                border-bottom: 1px solid #ffffff;
            }
            QTabBar::tab:hover {
                background: #e5e7eb;
            }
        """


    def open_management(self):
        tab_name = self.tr("🧠 Management")

        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        if not hasattr(self, '🧠 Management') or self.management is None:
            from Home.homeManagement import MainDashboard
            self.management = MainDashboard()

        self.add_custom_tab(self.management, tab_name, "resources/icons/management.ico")
    def open_marketing(self):
        tab_name = self.tr("📣 Marketing Auto")

        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        if not hasattr(self, '📣 Marketing Auto') or self.marketingauto is None:
            from Home.home import HomePage
            self.marketingauto = HomePage(main_app=self)

        self.add_custom_tab(self.marketingauto, tab_name, "resources/icons/marketing.ico")

    def open_home(self):
        tab_name = self.tr("home")

        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        if not hasattr(self, 'home') or self.home is None:
            from promptes.promptmarketing import MarketingAIAnalyzer
            self.marketing = MarketingAIAnalyzer(parent=self)

        self.add_custom_tab(self.marketing, tab_name, "resources/icons/marketing.ico")

    def open_home(self):
        tab_name = self.tr("🏠 Home")  # Changed to include home emoji

        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        if not hasattr(self, 'home') or self.home is None:
            from promptes.promptmarketing import MarketingAIAnalyzer
            self.marketing = MarketingAIAnalyzer(parent=self)

        self.add_custom_tab(self.marketing, tab_name, "📊")  # Changed to marketing/analytics emoji
        
                    
    def open_marketing1(self):
        tab_name = self.tr("Marketing")

        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Loading UI
        loading_label = QLabel(self.tr("Loading Marketing..."))
        loading_label.setAlignment(Qt.AlignCenter)
        self.add_custom_tab(loading_label, tab_name, "resources/icons/marketing.ico")

        progress_dialog = QProgressDialog(self.tr("Loading..."), self.tr("Cancel"), 0, 0, self)
        progress_dialog.setCancelButton(None)
        progress_dialog.setWindowTitle(self.tr("Loading Marketing"))
        progress_dialog.setWindowModality(Qt.ApplicationModal)
        progress_dialog.show()

    def open_management1(self):
        tab_name = self.tr("Management")

        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        loading_label = QLabel(self.tr("Loading Management..."))
        loading_label.setAlignment(Qt.AlignCenter)
        self.add_custom_tab(loading_label, tab_name, "resources/icons/management.ico")

        progress_dialog = QProgressDialog(self.tr("Loading..."), self.tr("Cancel"), 0, 0, self)
        progress_dialog.setCancelButton(None)
        progress_dialog.setWindowTitle(self.tr("Loading Management"))
        progress_dialog.setWindowModality(Qt.ApplicationModal)
        progress_dialog.show()

        self.loader_thread = LoaderThread(main_app=self)

        def load_management():
            if not hasattr(self, 'management') or self.management is None:
                from Home.homeManagement import MainDashboard
                self.management = MainDashboard()
            self.update_tab_content(tab_name, self.management, progress_dialog)

        self.loader_thread.finished.connect(load_management)
        self.loader_thread.start()
    def open_finance(self):
        tab_name = self.tr("💵 Finance")

        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        if not hasattr(self, '💵 finance') or self.finance is None:
            from finance.finance import CryptoStrategyApp
            self.finance = CryptoStrategyApp(parent=self)

        self.add_custom_tab(self.finance, tab_name, "resources/icons/finance.ico")

    def open_finance1(self):
        tab_name = self.tr("Finance")

        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        loading_label = QLabel(self.tr("Loading Finance..."))
        loading_label.setAlignment(Qt.AlignCenter)
        self.add_custom_tab(loading_label, tab_name, "resources/icons/finance.ico")

        progress_dialog = QProgressDialog(self.tr("Loading..."), self.tr("Cancel"), 0, 0, self)
        progress_dialog.setCancelButton(None)
        progress_dialog.setWindowTitle(self.tr("Loading Finance"))
        progress_dialog.setWindowModality(Qt.ApplicationModal)
        progress_dialog.show()

        self.loader_thread = LoaderThread(main_app=self)

        def load_finance():
            if not hasattr(self, 'finance') or self.finance is None:
                from finance.finance import CryptoStrategyApp
                self.finance = CryptoStrategyApp(parent=self)
            self.update_tab_content(tab_name, self.finance, progress_dialog)

        self.loader_thread.finished.connect(load_finance)
        self.loader_thread.start()

    def get_button_style(self, button_type):
        """Return style sheet for window control buttons"""
        styles = {
            "close": """
                QPushButton {
                    background-color: #FF5C5C;
                    color: white;
                    border-radius: 10px;
                    font-size: 10px;
                }
                QPushButton:hover {
                    background-color: #FF7878;
                }
            """,
            "minimize": """
                QPushButton {
                    background-color: #FFBD4C;
                    color: white;
                    border-radius: 10px;
                    font-size: 10px;
                    padding-bottom: 3px;
                }
                QPushButton:hover {
                    background-color: #FFD37C;
                }
            """,
            "maximize": """
                QPushButton {
                    background-color: #00CA56;
                    color: white;
                    border-radius: 10px;
                    font-size: 10px;
                }
                QPushButton:hover {
                    background-color: #00E066;
                }
            """
        }
        return styles.get(button_type, "")

    def load_menu_config(self):
        """Load menu configuration from settings"""
        try:
            settings = QSettings()
            visible_buttons = settings.value("menu/visible_buttons", {})
            if visible_buttons:
                self.menu_config['visible_buttons'] = visible_buttons
        except:
            pass

    def save_menu_config(self):
        """Save menu configuration to persistent storage"""
        try:
            settings = QSettings()
            settings.setValue("menu/visible_buttons", self.menu_config['visible_buttons'])
        except:
            pass

    def toggle_menu_button(self, button_name, visible=None):
        """Toggle visibility of a menu button"""
        if button_name in self.menu_config['visible_buttons']:
            if visible is None:
                # Toggle current state
                self.menu_config['visible_buttons'][button_name] = not self.menu_config['visible_buttons'][button_name]
            else:
                # Set specific state
                self.menu_config['visible_buttons'][button_name] = visible
            
            self.save_menu_config()
            self.update_menu_visibility()
    def add_on_page(self):
        from Installsweb.installdisign import InstallerDialog
        installer = InstallerDialog(self)
        installer.exec_()

    def update_menu_visibility(self):
        """Update menu buttons visibility based on configuration"""
        for button_name, visible in self.menu_config['visible_buttons'].items():
            if button_name in self.menu_button_refs:
                button = self.menu_button_refs[button_name]
                button.setVisible(visible)
                
                # Also hide any open submenus if parent is hidden
                if not visible and button in self.sub_menus:
                    for sub_btn in self.sub_menus[button]:
                        sub_btn.setVisible(False)

    def show_menu_settings_dialog(self):
        """Show dialog to configure menu buttons visibility"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Configure Menu Buttons")
        dialog.setMinimumWidth(300)
        
        layout = QVBoxLayout(dialog)
        
        # Add checkboxes for each dynamic button
        checkboxes = {}
        for button_name in self.menu_config['visible_buttons']:
            cb = QCheckBox(button_name)
            cb.setChecked(self.menu_config['visible_buttons'][button_name])
            checkboxes[button_name] = cb
            layout.addWidget(cb)
        
        # Add save button
        btn_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(dialog.accept)
        btn_box.rejected.connect(dialog.reject)
        layout.addWidget(btn_box)
        
        if dialog.exec() == QDialog.Accepted:
            # Update configuration from checkboxes
            for button_name, cb in checkboxes.items():
                self.toggle_menu_button(button_name, cb.isChecked())
        
        dialog.deleteLater()

        
    
  


    def update_user_buttons(self):
        """Update button visibility based on user state"""
        # Login/logout toggle
        self.login_button.setVisible(not self.is_user_logged_in)
        self.logout_button.setVisible(self.is_user_logged_in)
        
        # Mode toggle
        self.enterprise_button.setVisible(self.is_user_logged_in and not self.is_enterprise_mode)
        self.personal_button.setVisible(self.is_user_logged_in and self.is_enterprise_mode)
        
        # Other buttons
        self.settings_button.setVisible(self.is_user_logged_in)
        self.switch_button.setVisible(self.is_user_logged_in)
        self.subscription_button.setVisible(self.is_user_logged_in)
        
        # Update user label
        username = "Admin" if self.is_user_logged_in else "Guest"
        self.user_button.setText(f"👤 {username}")

    # def user_login(self):
    #     """Handle user login"""
    #     self.is_user_logged_in = True
    #     self.update_user_buttons()
    #     print("User logged in")

    # def user_logout(self):
    #     """Handle user logout"""
    #     self.is_user_logged_in = False
    #     self.is_enterprise_mode = False
    #     self.update_user_buttons()
    #     print("User logged out")

    def switch_to_enterprise(self):
        """Switch to enterprise mode"""
        self.is_enterprise_mode = True
        self.update_user_buttons()
        print("Enterprise mode activated")

    def switch_to_personal(self):
        """Switch to personal mode"""
        self.is_enterprise_mode = False
        self.update_user_buttons()
        print("Personal mode activated")

    def toggle_user_menu(self):
        """Toggle user menu visibility"""
        self.user_menu.setVisible(not self.user_menu.isVisible())






    def create_menu_handler(self, button):
        """Create a handler that manages the accordion behavior"""
        def handler():
            # Close currently open menu if it's not this one
            if self.current_open_menu and self.current_open_menu != button:
                for btn in self.sub_menus[self.current_open_menu]:
                    btn.setVisible(False)
            
            # Toggle current menu
            for btn in self.sub_menus[button]:
                btn.setVisible(not btn.isVisible())
            
            # Update currently open menu
            if any(btn.isVisible() for btn in self.sub_menus[button]):
                self.current_open_menu = button
            else:
                self.current_open_menu = None
                
        return handler

    def update_user_buttons(self):
        """Update button visibility based on user state"""
        # Login/logout toggle
        self.login_button.setVisible(not self.is_user_logged_in)
        self.logout_button.setVisible(self.is_user_logged_in)
        
        # Mode toggle
        self.enterprise_button.setVisible(self.is_user_logged_in and not self.is_enterprise_mode)
        self.personal_button.setVisible(self.is_user_logged_in and self.is_enterprise_mode)
        
        # Other buttons
        self.settings_button.setVisible(self.is_user_logged_in)
        self.switch_button.setVisible(self.is_user_logged_in)
        self.subscription_button.setVisible(self.is_user_logged_in)
        
        # Update user label
        username = "Admin" if self.is_user_logged_in else "Guest"
        self.user_button.setText(f"👤 {username}")

    # def user_login(self):
    #     """Handle user login"""
    #     self.is_user_logged_in = True
    #     self.update_user_buttons()
    #     print("User logged in")






        """Toggle user menu visibility"""
        self.user_menu.setVisible(not self.user_menu.isVisible())






    def update_user_section(self):
        """Update user section based on login state"""
        # Clear existing user menu
        if hasattr(self, 'user_menu'):
            for i in reversed(range(self.user_menu_layout.count())): 
                self.user_menu_layout.itemAt(i).widget().setParent(None)
        
        # Add appropriate buttons based on state
        if self.is_user_logged_in:
            user_actions = [
                ("🚪", "Logout", self.user_logout),
                ("🏢", "Enterprise Mode", self.switch_to_enterprise) if not self.is_enterprise_mode else 
                ("👤", "Personal Mode", self.switch_to_personal),
                ("♻️", "Update", self.open_user_settings),
                ("👥", "Switch Account", self.switch_account),
                ("🛒", "Subscription", self.open_subscription),
                ("🎭", "My Persona", self.open_my_persona)

            ]
        else:
            user_actions = [
                ("🔑", "Login", self.user_login)
            ]
        
        for icon, text, action in user_actions:
            btn = QPushButton(f"  {icon}  {text}")
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
            btn.clicked.connect(action)
            self.user_menu_layout.addWidget(btn)

    def start_menu_move(self, event):
        """Start moving the menu"""
        self.drag_start_position = event.globalPos()
        self.original_menu_pos = self.central_container.sizes()[0]

    def move_menu(self, event):
        """Handle menu movement"""
        if not hasattr(self, 'drag_start_position'):
            return
            
        delta = event.globalPos() - self.drag_start_position
        new_width = max(100, min(400, self.original_menu_pos + delta.x()))
        self.central_container.setSizes([new_width, self.width() - new_width])

    def finish_menu_move(self, event):
        """Finish menu movement"""
        if hasattr(self, 'drag_start_position'):
            del self.drag_start_position

    def toggle_menu_position(self):
        """Toggle menu between left and right"""
        current_widgets = self.central_container.widgets()
        if current_widgets[0] == self.side_menu:
            # Move to right
            self.central_container.insertWidget(1, self.side_menu)
        else:
            # Move to left
            self.central_container.insertWidget(0, self.side_menu)
        self.central_container.setSizes([200, self.width() - 200])



    # def user_logout(self):
    #     """Handle user logout"""
    #     self.is_user_logged_in = False
    #     self.update_user_section()






    def open_user_settings(self):
        """Switch to personal mode"""
        from AutoUpdater.auto import UpdaterWindow
        window = UpdaterWindow(parent=self)
        window.show()




    def create_menu_handler(self, button):
        """Create a handler that manages the accordion behavior"""
        def handler():
            # Close currently open menu if it's not this one
            if self.current_open_menu and self.current_open_menu != button:
                for btn in self.sub_menus[self.current_open_menu]:
                    btn.setVisible(False)
            
            # Toggle current menu
            for btn in self.sub_menus[button]:
                btn.setVisible(not btn.isVisible())
            
            # Update currently open menu
            if any(btn.isVisible() for btn in self.sub_menus[button]):
                self.current_open_menu = button
            else:
                self.current_open_menu = None
                
        return handler

    def toggle_sub_menu(self, button):
        """Toggle submenu visibility for nested menus"""
        for btn in self.sub_menus[button]:
            btn.setVisible(not btn.isVisible())

    def toggle_user_menu(self):
        """Toggle the user menu visibility"""
        self.is_user_menu_expanded = not self.is_user_menu_expanded
        self.user_menu.setVisible(self.is_user_menu_expanded)








    def open_account_settings(self):
        """Open account settings"""
        print("Account settings opened")
    def open_subscription(self):
        """Open subscription page"""
        print("Subscription page opened")
    def open_my_persona(self):
        """Open subscription page"""
        print("Subscription page opened")

    def switch_user(self):
        """Switch user account"""
        print("Switching user")


    def create_menu_handler(self, button):
        """Create a handler that manages the accordion behavior"""
        def handler():
            # Close currently open menu if it's not this one
            if self.current_open_menu and self.current_open_menu != button:
                for btn in self.sub_menus[self.current_open_menu]:
                    btn.setVisible(False)
            
            # Toggle current menu
            for btn in self.sub_menus[button]:
                btn.setVisible(not btn.isVisible())
            
            # Update currently open menu
            if any(btn.isVisible() for btn in self.sub_menus[button]):
                self.current_open_menu = button
            else:
                self.current_open_menu = None
                
        return handler

    def toggle_sub_menu(self, button):
        """Toggle submenu visibility for nested menus"""
        for btn in self.sub_menus[button]:
            btn.setVisible(not btn.isVisible())


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







    def update_user_buttons(self):
        """Update the visibility of user-related buttons based on login state"""
        if self.is_user_logged_in:
            self.login_action.setVisible(False)
            self.logout_action.setVisible(True)
            self.switch_action.setVisible(True)
            self.user_button.setText(f"👤 {self.current_username}")
            
            if self.is_enterprise_mode:
                self.enterprise_action.setVisible(False)
                self.personal_action.setVisible(True)
            else:
                self.enterprise_action.setVisible(True)
                self.personal_action.setVisible(False)
        else:
            self.login_action.setVisible(True)
            self.logout_action.setVisible(False)
            self.switch_action.setVisible(False)
            self.enterprise_action.setVisible(False)
            self.personal_action.setVisible(False)
            self.user_button.setText("👤 Guest")



    # def user_login(self):
    #     """Handle user login"""
    #     # Votre logique de connexion existante
    #     self.is_user_logged_in = True
    #     self.current_username = "Utilisateur"  # Remplacer par le vrai nom d'utilisateur
    #     self.update_user_buttons()

    # def user_logout(self):
    #     """Handle user logout"""
    #     self.is_user_logged_in = False
    #     self.current_username = None
    #     self.update_user_buttons()



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
    """Generic dialog for 'About' Leopardo AI."""
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize and load translations
        # self.translator_manager = TranslatorManager()
        # self.translator_manager.load_translations()

        # Window configuration
        self.setWindowTitle(self.tr("About Leopardo AI"))
        layout = QVBoxLayout()

        # Main content
        label = QLabel(self.tr(
            """
            <div style='background-color:#F5F7FA; padding:15px; border-radius:10px;'>
                <h1 style='color:#1A5276; font-size:24px; font-weight:bold; text-align:center;'>
                    Welcome to Leopardo AI
                </h1>

                <p style='font-size:16px; color:#333333; text-align:center;'>
                    <strong>Your All-in-One AI-Powered Automation Solution</strong>
                </p><br>

                <div style='padding: 10px; border-left: 4px solid #1A5276;'>
                    <p style='font-size:14px; color:#5D6D7E; line-height:1.6; margin:0 20px;'>
                        Leopardo AI is the ultimate tool for businesses, brands, and creators looking to simplify and scale their online presence.<br>
                        Harnessing advanced AI, Leopardo AI automates social media, content creation, engagement, and growth strategies.<br>
                        Focus on what matters most while Leopardo AI handles the execution.
                    </p>
                </div><br>

                <h3 style='color:#1A5276; font-size:18px; margin-top:20px; text-align:center;'>Core Features</h3><br>

                <ul style='font-size:14px; color:#4A4A4A; padding-left: 40px;'>
                    <li style='margin-bottom:10px;'><strong>🌐 Smart Scheduling:</strong> Plan and post across multiple platforms for maximum efficiency.</li><br>
                    <li style='margin-bottom:10px;'><strong>🤖 AI-Driven Engagement:</strong> Automate replies, comments, and audience interactions seamlessly.</li><br>
                    <li><strong>📂 Integrated Management:</strong> Organize media, campaigns, and teams with ease.</li>
                </ul><br>

                <p style='font-size:14px; color:#5D6D7E; line-height:1.6; text-align:center;'>
                    Join a growing community of professionals who trust Leopardo AI to optimize their automation journey.<br>
                    Save time, grow faster, and achieve more with AI at your fingertips.
                </p><br>

                <p style='font-size:11px; color:#888888; text-align:center; margin-top:20px;'>
                    © 2024 Leopard AI | 
                    <a href='https://www.Leopardopro.com' style='color:#1A5276; text-decoration:none;'>www.Leopardopro.com</a>
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




import requests
from packaging import version
from PyQt5.QtWidgets import QMessageBox

VERSION_LOCAL = "1.9.0"

def check_update():
    try:
        response = requests.get("https://leopardo-ai.web.app/version.json")
        data = response.json()
        version_en_ligne = data['version']
        if version.parse(version_en_ligne) > version.parse(VERSION_LOCAL):
            msg = QMessageBox()
            msg.setWindowTitle("Nouvelle version disponible")
            msg.setText(f"Une nouvelle version {version_en_ligne} est disponible.\n\nNotes : {data.get('notes', '')}\n\nTélécharger maintenant ?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            if msg.exec_() == QMessageBox.Yes:
                import webbrowser
                webbrowser.open(data["url"])
    except Exception as e:
        print("Erreur lors de la vérification des mises à jour :", e)





import requests
import json
import os
import shutil

VERSION_ACTUELLE = "1.9"

def get_latest_version_info():
    url = "https://leopardo-ai.web.app/version.json"  # lien Firebase Hosting
    response = requests.get(url)
    return response.json()

def update_app():
    info = get_latest_version_info()
    if info["version"] != VERSION_ACTUELLE:
        print(f"📥 Nouvelle version disponible : {info['version']}")
        exe_url = info["url"]
        new_file = "leopardo_new.exe"
        
        r = requests.get(exe_url, stream=True)
        with open(new_file, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("✅ Téléchargement terminé.")
        # Facultatif : Exécuter le nouveau .exe, puis fermer l'app actuelle
        os.startfile(new_file)
        os._exit(0)  # Ferme l'ancienne version
    else:
        print("🟢 Aucune mise à jour nécessaire.")







import tkinter as tk
from tkinter import messagebox
from threading import Thread

def check_for_update():
    info = get_latest_version_info()
    if info["version"] != VERSION_ACTUELLE:
        should_update = messagebox.askyesno(
            "Mise à jour disponible",
            f"La version {info['version']} est disponible. Voulez-vous l'installer ?"
        )
        if should_update:
            download_and_execute(info["url"])

Thread(target=check_for_update).start()
