import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, 
                            QStackedWidget, QToolBar, QStatusBar, QPushButton, 
                            QFrame, QHBoxLayout, QSizePolicy)
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QSize, QTranslator

class RibbonButton(QPushButton):
    def __init__(self, text="", icon=None, parent=None):
        super().__init__(parent)
        self.setText(self.tr(text))
        if icon:
            self.setIcon(QIcon(icon))
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(True)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 6px 12px;
                background: transparent;
                color: #333;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #e6e6e6;
                border-radius: 4px;
            }
            QPushButton:pressed {
                background: #d0d0d0;
                border-radius: 4px;
            }
            QPushButton:checked {
                background: #d0d0d0;
                border-radius: 4px;
            }
        """)

class MainWindowsales(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Marketing Management System"))
        self.setGeometry(100, 100, 1200, 800)
        
        # Dictionnaire pour stocker les instances de pages
        self.page_instances = {
            'documents': None,
            'links': None,
            'contacts': None,
            'prompts': None,
            'sav': None,
            'projects': None
        }
        
        self.setup_ui()
        
        # Setup translator
        self.translator = QTranslator()
        
        # Modern style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QToolBar {
                background: white;
                border-bottom: 1px solid #d0d0d0;
                padding: 4px;
                spacing: 4px;
            }
            QStatusBar {
                background: white;
                border-top: 1px solid #d0d0d0;
            }
        """)

    def setup_ui(self):
        self.create_ribbon()
        self.create_status_bar()
        self.create_main_content()

    def create_ribbon(self):
        # Main ribbon toolbar
        self.ribbon = QToolBar("Ribbon")
        self.ribbon.setIconSize(QSize(20, 20))
        self.addToolBar(self.ribbon)

        # Documents tab
        self.documents_btn = RibbonButton(self.tr("Documents"))
        self.documents_btn.setChecked(True)
        self.documents_btn.clicked.connect(lambda: self.show_page("documents"))
        self.ribbon.addWidget(self.documents_btn)

        # Links tab
        self.links_btn = RibbonButton(self.tr("Gestion Liens"))
        self.links_btn.clicked.connect(lambda: self.show_page("links"))
        self.ribbon.addWidget(self.links_btn)

        # Contacts tab
        self.contacts_btn = RibbonButton(self.tr("Contacts"))
        self.contacts_btn.clicked.connect(lambda: self.show_page("contacts"))
        self.ribbon.addWidget(self.contacts_btn)

        # Prompts tab
        self.prompts_btn = RibbonButton(self.tr("Prompts"))
        self.prompts_btn.clicked.connect(lambda: self.show_page("prompts"))
        self.ribbon.addWidget(self.prompts_btn)

        # SAV tab
        self.sav_btn = RibbonButton(self.tr("SAV"))
        self.sav_btn.clicked.connect(lambda: self.show_page("sav"))
        self.ribbon.addWidget(self.sav_btn)

        # Projects tab
        self.projects_btn = RibbonButton(self.tr("Projets"))
        self.projects_btn.clicked.connect(lambda: self.show_page("projects"))
        self.ribbon.addWidget(self.projects_btn)

    def create_status_bar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        # Message area
        self.status_label = QLabel(self.tr("Ready"))
        status_bar.addWidget(self.status_label, 1)

        # Status widgets
        zoom_label = QLabel("100%")
        status_bar.addPermanentWidget(zoom_label)

    def create_main_content(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Content area
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Create only the documents page initially
        self.load_documents_page()

    def load_documents_page(self):
        """Charge la page Documents seulement si elle n'existe pas déjà"""
        if self.page_instances['documents'] is None:
            from Home.homemarketing import MainWindow as DocumentsPage
            self.page_instances['documents'] = DocumentsPage()
            self.stacked_widget.addWidget(self.page_instances['documents'])
        return self.page_instances['documents']

    def load_links_page(self):
        """Charge la page Gestion Liens seulement si elle n'existe pas déjà"""
        if self.page_instances['links'] is None:
            from liens.gestionliens import MainWindowLink as LinksPage
            self.page_instances['links'] = LinksPage()
            self.stacked_widget.addWidget(self.page_instances['links'])
        return self.page_instances['links']

    def load_contacts_page(self):
        """Charge la page Contacts seulement si elle n'existe pas déjà"""
        if self.page_instances['contacts'] is None:
            from ModulesUI.whasapping.group_manager import ContactTable as ContactsPage
            self.page_instances['contacts'] = ContactsPage()
            self.stacked_widget.addWidget(self.page_instances['contacts'])
        return self.page_instances['contacts']

    def load_prompts_page(self):
        """Charge la page Prompts seulement si elle n'existe pas déjà"""
        if self.page_instances['prompts'] is None:
            from promptes.promptes import PromptManager as PromptsPage
            self.page_instances['prompts'] = PromptsPage()
            self.stacked_widget.addWidget(self.page_instances['prompts'])
        return self.page_instances['prompts']

    def load_sav_page(self):
        """Charge la page SAV seulement si elle n'existe pas déjà"""
        if self.page_instances['sav'] is None:
            # Page SAV par défaut
            class SavPage(QWidget):
                def __init__(self):
                    super().__init__()
                    layout = QVBoxLayout()
                    self.label = QLabel("Service Après-Vente")
                    self.label.setAlignment(Qt.AlignCenter)
                    self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
                    layout.addWidget(self.label)
                    
                    # Ajouter un widget de gestion des tickets SAV
                    self.info_label = QLabel("Gestion des réclamations et support client")
                    self.info_label.setAlignment(Qt.AlignCenter)
                    layout.addWidget(self.info_label)
                    
                    self.setLayout(layout)
            
            self.page_instances['sav'] = SavPage()
            self.stacked_widget.addWidget(self.page_instances['sav'])
        return self.page_instances['sav']

    def load_projects_page(self):
        """Charge la page Projets seulement si elle n'existe pas déjà"""
        if self.page_instances['projects'] is None:
            from Home.homemarketing import MainWindow as ProjectsPage
            self.page_instances['projects'] = ProjectsPage()
            self.stacked_widget.addWidget(self.page_instances['projects'])
        return self.page_instances['projects']

    def show_page(self, page_name):
        if page_name in self.page_instances:
            # Charge la page seulement quand elle est demandée
            if page_name == 'documents':
                page = self.load_documents_page()
            elif page_name == 'links':
                page = self.load_links_page()
            elif page_name == 'contacts':
                page = self.load_contacts_page()
            elif page_name == 'prompts':
                page = self.load_prompts_page()
            elif page_name == 'sav':
                page = self.load_sav_page()
            elif page_name == 'projects':
                page = self.load_projects_page()
            else:
                return

            self.stacked_widget.setCurrentWidget(page)
            self.update_button_states(page_name)
            self.status_label.setText(self.tr(f"Showing {page_name} page"))

    def update_button_states(self, active_page):
        self.documents_btn.setChecked(active_page == "documents")
        self.links_btn.setChecked(active_page == "links")
        self.contacts_btn.setChecked(active_page == "contacts")
        self.prompts_btn.setChecked(active_page == "prompts")
        self.sav_btn.setChecked(active_page == "sav")
        self.projects_btn.setChecked(active_page == "projects")

    def tr(self, text):
        """Translation method - would connect to actual translation system"""
        return text

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Modern Fusion style
    app.setStyle("Fusion")
    
    # Light color palette
    palette = app.palette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, Qt.white)
    palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.black)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())