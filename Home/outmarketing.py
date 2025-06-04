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

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Professional Application"))
        self.setGeometry(100, 100, 1200, 800)
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

        # Media tab
        self.media_btn = RibbonButton(self.tr("Media"))
        self.media_btn.setChecked(True)
        self.media_btn.clicked.connect(lambda: self.show_page("media"))
        self.ribbon.addWidget(self.media_btn)

        # Groups tab
        self.groups_btn = RibbonButton(self.tr("Groups"))
        self.groups_btn.clicked.connect(lambda: self.show_page("groups"))
        self.ribbon.addWidget(self.groups_btn)

        # Scheduling tab
        self.scheduling_btn = RibbonButton(self.tr("Scheduling"))
        self.scheduling_btn.clicked.connect(lambda: self.show_page("scheduling"))
        self.ribbon.addWidget(self.scheduling_btn)

        # Email tab
        self.email_btn = RibbonButton(self.tr("Email"))
        self.email_btn.clicked.connect(lambda: self.show_page("email"))
        self.ribbon.addWidget(self.email_btn)

        # SMS tab
        self.sms_btn = RibbonButton(self.tr("SMS"))
        self.sms_btn.clicked.connect(lambda: self.show_page("sms"))
        self.ribbon.addWidget(self.sms_btn)

        # Paramètre tab
        self.parametre_btn = RibbonButton(self.tr("Paramètre"))
        self.parametre_btn.clicked.connect(lambda: self.show_page("parametre"))
        self.ribbon.addWidget(self.parametre_btn)

        # Evaluation tab
        self.evaluation_btn = RibbonButton(self.tr("Evaluation"))
        self.evaluation_btn.clicked.connect(lambda: self.show_page("evaluation"))
        self.ribbon.addWidget(self.evaluation_btn)

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

        # Create only the media page initially
        self.pages = {
            "media": self.create_media_page(),
            "groups": None,
            "scheduling": None,
            "email": None,
            "sms": None,
            "parametre": None,
            "evaluation": None
        }

        self.stacked_widget.addWidget(self.pages["media"])
        self.show_page("media")

    def create_media_page(self):
        """Create the Media page"""
        # from media_module import MediaPage
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel("Media Page Content")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        return page

    def create_groups_page(self):
        """Create the Groups page when needed"""
        # from groups_module import GroupsPage
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel("Groups Page Content")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        return page

    def create_scheduling_page(self):
        """Create the Scheduling page when needed"""
        # from scheduling_module import SchedulingPage
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel("Scheduling Page Content")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        return page

    def create_email_page(self):
        """Create the Email page when needed"""
        # from email_module import EmailPage
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel("Email Page Content")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        return page

    def create_sms_page(self):
        """Create the SMS page when needed"""
        # from sms_module import SMSPage
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel("SMS Page Content")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        return page

    def create_parametre_page(self):
        """Create the Paramètre page when needed"""
        # from parametre_module import ParametrePage
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel("Paramètre Page Content")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        return page

    def create_evaluation_page(self):
        """Create the Evaluation page when needed"""
        # from evaluation_module import EvaluationPage
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel("Evaluation Page Content")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        return page

    def show_page(self, page_name):
        if page_name in self.pages:
            # Create page if it doesn't exist yet
            if self.pages[page_name] is None:
                if page_name == "groups":
                    self.pages[page_name] = self.create_groups_page()
                elif page_name == "scheduling":
                    self.pages[page_name] = self.create_scheduling_page()
                elif page_name == "email":
                    self.pages[page_name] = self.create_email_page()
                elif page_name == "sms":
                    self.pages[page_name] = self.create_sms_page()
                elif page_name == "parametre":
                    self.pages[page_name] = self.create_parametre_page()
                elif page_name == "evaluation":
                    self.pages[page_name] = self.create_evaluation_page()
                
                self.stacked_widget.addWidget(self.pages[page_name])

            self.stacked_widget.setCurrentWidget(self.pages[page_name])
            self.update_button_states(page_name)
            self.status_label.setText(self.tr(f"Showing {page_name} page"))

    def update_button_states(self, active_page):
        self.media_btn.setChecked(active_page == "media")
        self.groups_btn.setChecked(active_page == "groups")
        self.scheduling_btn.setChecked(active_page == "scheduling")
        self.email_btn.setChecked(active_page == "email")
        self.sms_btn.setChecked(active_page == "sms")
        self.parametre_btn.setChecked(active_page == "parametre")
        self.evaluation_btn.setChecked(active_page == "evaluation")

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