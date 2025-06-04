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

class MainWindowattak(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Content Management System"))
        self.setGeometry(100, 100, 1200, 800)
        
        # Dictionnaire pour stocker les instances de pages
        self.page_instances = {
            'media': None,
            'groups': None,
            'content': None,
            'planning': None,
            'email': None,
            'sms': None,
            'settings': None,
            'analytics': None,
            'ads': None
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
        self.ribbon = QToolBar(self.tr("Main Menu"))
        self.ribbon.setIconSize(QSize(20, 20))
        self.addToolBar(self.ribbon)

        # Media tab
        self.media_btn = RibbonButton(self.tr("Media Library"))
        self.media_btn.setChecked(True)
        self.media_btn.clicked.connect(lambda: self.show_page("media"))
        self.ribbon.addWidget(self.media_btn)

        # Groups tab
        self.groups_btn = RibbonButton(self.tr("Audience Groups"))
        self.groups_btn.clicked.connect(lambda: self.show_page("groups"))
        self.ribbon.addWidget(self.groups_btn)

        # Content Creation tab
        self.content_btn = RibbonButton(self.tr("Content Creator"))
        self.content_btn.clicked.connect(lambda: self.show_page("content"))
        self.ribbon.addWidget(self.content_btn)

        # Planning tab (anciennement Scheduling)
        self.planning_btn = RibbonButton(self.tr("Content Calendar"))
        self.planning_btn.clicked.connect(lambda: self.show_page("planning"))
        self.ribbon.addWidget(self.planning_btn)

        # Email tab
        self.email_btn = RibbonButton(self.tr("Email Campaigns"))
        self.email_btn.clicked.connect(lambda: self.show_page("email"))
        self.ribbon.addWidget(self.email_btn)

        # SMS tab
        self.sms_btn = RibbonButton(self.tr("SMS Marketing"))
        self.sms_btn.clicked.connect(lambda: self.show_page("sms"))
        self.ribbon.addWidget(self.sms_btn)

        # Settings tab (anciennement Paramètre)
        self.settings_btn = RibbonButton(self.tr("Settings"))
        self.settings_btn.clicked.connect(lambda: self.show_page("settings"))
        self.ribbon.addWidget(self.settings_btn)

        # Analytics tab (anciennement Evaluation)
        self.analytics_btn = RibbonButton(self.tr("Performance Analytics"))
        self.analytics_btn.clicked.connect(lambda: self.show_page("analytics"))
        self.ribbon.addWidget(self.analytics_btn)

        # Ads tab
        self.ads_btn = RibbonButton(self.tr("Ad Campaigns"))
        self.ads_btn.clicked.connect(lambda: self.show_page("ads"))
        self.ribbon.addWidget(self.ads_btn)

    def create_status_bar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        # Message area
        self.status_label = QLabel(self.tr("System ready - Select a module to begin"))
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

        # Create only the media page initially
        self.load_media_page()  # Charge uniquement la page Media au démarrage

    def load_media_page(self):
        """Charge la page Media seulement si elle n'existe pas déjà"""
        if self.page_instances['media'] is None:
            from facebooksmodule.media_manager import MediaTable
            self.page_instances['media'] = MediaTable()
            self.stacked_widget.addWidget(self.page_instances['media'])
        return self.page_instances['media']

    def load_groups_page(self):
        """Charge la page Groups seulement si elle n'existe pas déjà"""
        if self.page_instances['groups'] is None:
            from facebooksmodule.group_manager import GroupTable
            self.page_instances['groups'] = GroupTable()
            self.stacked_widget.addWidget(self.page_instances['groups'])
        return self.page_instances['groups']

    def load_content_page(self):
        """Charge la page Content Creation seulement si elle n'existe pas déjà"""
        if self.page_instances['content'] is None:
            # Classe Content temporaire
            class ContentPage(QWidget):
                def __init__(self):
                    super().__init__()
                    layout = QVBoxLayout()
                    self.label = QLabel(self.tr("Content Creation Hub"))
                    self.label.setAlignment(Qt.AlignCenter)
                    self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
                    
                    # Exemple de contenu par défaut
                    self.subtitle = QLabel(self.tr("Create and manage all your marketing content here"))
                    self.subtitle.setAlignment(Qt.AlignCenter)
                    
                    layout.addWidget(self.label)
                    layout.addWidget(self.subtitle)
                    self.setLayout(layout)
            
            self.page_instances['content'] = ContentPage()
            self.stacked_widget.addWidget(self.page_instances['content'])
        return self.page_instances['content']

    def load_planning_page(self):
        """Charge la page Planning seulement si elle n'existe pas déjà"""
        if self.page_instances['planning'] is None:
            from statistique.activiteprogramme import Activite
            self.page_instances['planning'] = Activite()
            self.stacked_widget.addWidget(self.page_instances['planning'])
        return self.page_instances['planning']

    def load_email_page(self):
        """Charge la page Email seulement si elle n'existe pas déjà"""
        if self.page_instances['email'] is None:
            from mailsms.mailsysl import MainWindowMail
            self.page_instances['email'] = MainWindowMail()
            self.stacked_widget.addWidget(self.page_instances['email'])
        return self.page_instances['email']

    def load_sms_page(self):
        """Charge la page SMS seulement si elle n'existe pas déjà"""
        if self.page_instances['sms'] is None:
            # Classe SMS améliorée
            class SMSPage(QWidget):
                def __init__(self):
                    super().__init__()
                    layout = QVBoxLayout()
                    self.label = QLabel(self.tr("SMS Campaign Manager"))
                    self.label.setAlignment(Qt.AlignCenter)
                    self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
                    
                    # Contenu par défaut
                    self.features = QLabel(self.tr("""
                        <ul>
                            <li>Create SMS campaigns</li>
                            <li>Manage contact lists</li>
                            <li>Track delivery status</li>
                            <li>Analyze response rates</li>
                        </ul>
                    """))
                    self.features.setAlignment(Qt.AlignLeft)
                    
                    layout.addWidget(self.label)
                    layout.addWidget(self.features)
                    self.setLayout(layout)
            
            self.page_instances['sms'] = SMSPage()
            self.stacked_widget.addWidget(self.page_instances['sms'])
        return self.page_instances['sms']

    def load_settings_page(self):
        """Charge la page Settings seulement si elle n'existe pas déjà"""
        if self.page_instances['settings'] is None:
            from Home.home import HomePage
            self.page_instances['settings'] = HomePage()
            self.stacked_widget.addWidget(self.page_instances['settings'])
        return self.page_instances['settings']

    def load_analytics_page(self):
        """Charge la page Analytics seulement si elle n'existe pas déjà"""
        if self.page_instances['analytics'] is None:
            # Classe Analytics améliorée
            class AnalyticsPage(QWidget):
                def __init__(self):
                    super().__init__()
                    layout = QVBoxLayout()
                    self.label = QLabel(self.tr("Performance Analytics Dashboard"))
                    self.label.setAlignment(Qt.AlignCenter)
                    self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
                    
                    # Contenu par défaut
                    self.description = QLabel(self.tr("""
                        Track and analyze all your marketing campaign metrics and KPIs
                    """))
                    self.description.setAlignment(Qt.AlignCenter)
                    
                    layout.addWidget(self.label)
                    layout.addWidget(self.description)
                    self.setLayout(layout)
            
            self.page_instances['analytics'] = AnalyticsPage()
            self.stacked_widget.addWidget(self.page_instances['analytics'])
        return self.page_instances['analytics']

    def load_ads_page(self):
        """Charge la page Ads seulement si elle n'existe pas déjà"""
        if self.page_instances['ads'] is None:
            # Classe Ads améliorée
            class AdsPage(QWidget):
                def __init__(self):
                    super().__init__()
                    layout = QVBoxLayout()
                    self.label = QLabel(self.tr("Advertising Campaign Manager"))
                    self.label.setAlignment(Qt.AlignCenter)
                    self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
                    
                    # Contenu par défaut
                    self.features = QLabel(self.tr("""
                        <ul>
                            <li>Create and manage ad campaigns</li>
                            <li>Monitor ad performance</li>
                            <li>Optimize ad spending</li>
                            <li>Generate reports</li>
                        </ul>
                    """))
                    self.features.setAlignment(Qt.AlignLeft)
                    
                    layout.addWidget(self.label)
                    layout.addWidget(self.features)
                    self.setLayout(layout)
            
            self.page_instances['ads'] = AdsPage()
            self.stacked_widget.addWidget(self.page_instances['ads'])
        return self.page_instances['ads']

    def show_page(self, page_name):
        if page_name in self.page_instances:
            # Charge la page seulement quand elle est demandée
            if page_name == 'media':
                page = self.load_media_page()
            elif page_name == 'groups':
                page = self.load_groups_page()
            elif page_name == 'content':
                page = self.load_content_page()
            elif page_name == 'planning':
                page = self.load_planning_page()
            elif page_name == 'email':
                page = self.load_email_page()
            elif page_name == 'sms':
                page = self.load_sms_page()
            elif page_name == 'settings':
                page = self.load_settings_page()
            elif page_name == 'analytics':
                page = self.load_analytics_page()
            elif page_name == 'ads':
                page = self.load_ads_page()
            else:
                return

            self.stacked_widget.setCurrentWidget(page)
            self.update_button_states(page_name)
            self.status_label.setText(self.tr(f"Showing {page_name.replace('_', ' ')} module"))

    def update_button_states(self, active_page):
        self.media_btn.setChecked(active_page == "media")
        self.groups_btn.setChecked(active_page == "groups")
        self.content_btn.setChecked(active_page == "content")
        self.planning_btn.setChecked(active_page == "planning")
        self.email_btn.setChecked(active_page == "email")
        self.sms_btn.setChecked(active_page == "sms")
        self.settings_btn.setChecked(active_page == "settings")
        self.analytics_btn.setChecked(active_page == "analytics")
        self.ads_btn.setChecked(active_page == "ads")

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