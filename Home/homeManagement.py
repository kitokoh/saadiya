import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QStackedWidget, 
                            QFrame, QSizePolicy, QGraphicsOpacityEffect, 
                            QSystemTrayIcon, QMenu, QMessageBox, QSpacerItem)
from PyQt5.QtGui import (QFont, QIcon, QPalette, QColor, QLinearGradient, 
                        QBrush, QPixmap, QFontDatabase, QMovie)
from PyQt5.QtCore import (Qt, QSize, QPropertyAnimation, QEasingCurve, 
                         QTimer, QTranslator, QLocale, QEvent, QPoint)

class MainDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        # ================ INITIALIZATION ================
        self.setWindowTitle(self.tr("Executive Management Suite Pro"))
        self.setMinimumSize(1600, 950)
                # ================ STYLE CONSTANTS ================
        self.PRIMARY_COLOR = "#3498db"
        self.SECONDARY_COLOR = "#2c3e50"
        self.ACCENT_COLOR = "#e74c3c"
        self.BACKGROUND_GRADIENT = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2c3e50, stop:1 #3498db)"
        
        # ================ MAIN LAYOUT ================
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

                # ================ SIDEBAR ================
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(280)
        self.sidebar.setStyleSheet(f"""
            background-color: {self.SECONDARY_COLOR};
            border-right: 1px solid #34495e;
        """)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(10)
        # ================ UI CONFIGURATION ================
        
        self.setup_theme()
        self.setup_animations()
        self.setup_ui()
        self.setup_connections()
        
        # ================ SYSTEM INTEGRATION ================
        self.setup_system_tray()
        self.setup_notifications()
        
        # ================ DEMO CONTENT ================
        QTimer.singleShot(1500, self.show_welcome_animation)

    def setup_theme(self):
        """Configure the application theme"""
        self.theme = {
            "primary": "#4e54c8",
            "secondary": "#2b3a8a",
            "accent": "#ff7e5f",
            "background": "#f8faff",
            "text": "#2c3e50",
            "subtext": "#7f8c8d",
            "success": "#2ecc71",
            "warning": "#f39c12",
            "error": "#e74c3c"
        }
        
        # Load custom font
        QFontDatabase.addApplicationFont(":/fonts/Montserrat-Regular.ttf")
        
        # Set style
        #app.setStyle("Fusion")
        
        # Create palette
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(248, 250, 255))
        palette.setColor(QPalette.WindowText, QColor(44, 62, 80))
        palette.setColor(QPalette.Highlight, QColor(78, 84, 200))
        QApplication.setPalette(palette)

    def setup_ui(self):
        """Initialize all UI components"""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Setup components
        self.setup_sidebar()
        self.setup_content_area()
        self.setup_status_bar()
        
        # Demo modules
        self.setup_demo_modules()

    def setup_sidebar(self):
        """Create the modern glass sidebar"""
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(320)
        self.sidebar.setStyleSheet(f"""
            background: rgba(43, 58, 138, 0.92);
            border-right: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 0px 30px 30px 0px;
        """)
        
        # Sidebar layout
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(25, 50, 25, 40)
        sidebar_layout.setSpacing(20)
        
        # App logo
        self.app_logo = QLabel("💼 " + self.tr("NEO MANAGER"))
        self.app_logo.setStyleSheet("""
            color: white;
            font-size: 26px;
            font-weight: 800;
            qproperty-alignment: AlignCenter;
            margin-bottom: 40px;
            letter-spacing: 1px;
        """)
        sidebar_layout.addWidget(self.app_logo)
        
        # Navigation buttons
        self.nav_buttons = []
        modules = [
            ("📊", self.tr("Tableau de Bord"), "dashboard", "#4fc3f7"),
            ("👥", self.tr("CRM"), "crm", "#9575cd"),
            ("🌟", self.tr("Avis Clients"), "reviews", "#ffb74d"),
            ("📑", self.tr("Documents"), "documents", "#4dd0e1"),
            ("🤝", self.tr("Relations"), "relations", "#81c784"),
            ("🌐", self.tr("Réseau"), "network", "#64b5f6"),
            ("📦", self.tr("Logistique"), "logistics", "#ff8a65"),
            ("⚙️", self.tr("Paramètres"), "settings", "#90a4ae")
        ]
        
        for icon, text, module_id, color in modules:
            btn = self.create_nav_button(icon, text, module_id, color)
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)
        
        # Spacer
        sidebar_layout.addStretch()
        
        # User profile
        self.setup_user_profile(sidebar_layout)
        
        # Add to main layout
        self.main_layout.addWidget(self.sidebar)

    def create_nav_button(self, icon, text, module_id, color):
        """Create an animated navigation button"""
        btn = QPushButton(f"{icon}  {text}")
        btn.setObjectName(module_id)
        btn.setCursor(Qt.PointingHandCursor)
        
        # Base style
        btn.setStyleSheet(f"""
            QPushButton {{
                color: white;
                background: transparent;
                text-align: left;
                padding: 16px 24px;
                font-size: 15px;
                font-weight: 500;
                border-radius: 12px;
                border: none;
                margin: 2px 0;
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.08);
                padding-left: 28px;
            }}
            QPushButton#selected {{
                background: {color};
                font-weight: 600;
                padding-left: 28px;
            }}
        """)
        
        # Animation
        btn.installEventFilter(self)
        return btn

    def setup_content_area(self):
        """Setup the main content stack"""
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet(f"""
            background: {self.theme["background"]};
            border-radius: 30px 0px 0px 0px;
        """)
        
        # Add to main layout
        self.main_layout.addWidget(self.content_stack)

    def setup_demo_modules(self):
        """Create demo content for each module"""
        modules = [
            ("dashboard", "📊", self.tr("Tableau de Bord")),
            ("crm", "👥", self.tr("CRM")),
            ("reviews", "🌟", self.tr("Avis Clients")),
            ("documents", "📑", self.tr("Documents")),
            ("relations", "🤝", self.tr("Relations Clients")),
            ("network", "🌐", self.tr("Réseau Distributeurs")),
            ("logistics", "📦", self.tr("Logistique")),
            ("settings", "⚙️", self.tr("Paramètres"))
        ]
        
        for module_id, icon, title in modules:
            page = self.create_module_page(icon, title)
            self.content_stack.addWidget(page)

    def create_module_page(self, icon, title):
        """Create a beautiful module page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Header
        header = QHBoxLayout()
        
        title_label = QLabel(f"{icon}  {title}")
        title_label.setStyleSheet(f"""
            font-size: 32px;
            font-weight: 700;
            color: {self.theme["text"]};
        """)
        
        header.addWidget(title_label)
        header.addStretch()
        
        # Add animated construction widget
        construction_widget = self.create_construction_widget(title)
        
        # Add to layout
        layout.addLayout(header)
        layout.addWidget(construction_widget)
        layout.addStretch()
        
        return page

    def create_construction_widget(self, module_name):
        """Create an animated under construction widget"""
        container = QFrame()
        container.setStyleSheet(f"""
            background: white;
            border-radius: 20px;
            padding: 40px;
        """)
        
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignCenter)
        
        # Animation
        animation_label = QLabel()
        movie = QMovie(":/animations/construction.gif")
        animation_label.setMovie(movie)
        movie.start()
        
        # Title
        title = QLabel(self.tr("Module en Développement"))
        title.setStyleSheet(f"""
            font-size: 24px;
            font-weight: 600;
            color: {self.theme["text"]};
            margin-top: 30px;
            qproperty-alignment: AlignCenter;
        """)
        
        # Message
        message = QLabel(
            self.tr("L'équipe travaille activement sur le module {}.\n"
                   "Disponible dans la prochaine mise à jour!").format(module_name))
        message.setStyleSheet(f"""
            font-size: 16px;
            color: {self.theme["subtext"]};
            qproperty-alignment: AlignCenter;
            margin: 20px 0;
        """)
        message.setWordWrap(True)
        
        # Progress bar (simulated)
        progress = QLabel("🔨 🛠️ 🏗️ 🧰 🔧")
        progress.setStyleSheet("""
            font-size: 24px;
            qproperty-alignment: AlignCenter;
            margin-top: 20px;
        """)
        
        layout.addWidget(animation_label, 0, Qt.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(message)
        layout.addWidget(progress)
        
        return container

    def setup_connections(self):
        """Connect all signals and slots"""
        for btn in self.nav_buttons:
            btn.clicked.connect(self.on_nav_button_clicked)

    def on_nav_button_clicked(self):
        """Handle navigation button clicks"""
        sender = self.sender()
        
        # Update button states
        for btn in self.nav_buttons:
            btn.setProperty("selected", btn == sender)
            btn.style().polish(btn)
        
        # Get module index
        index = self.nav_buttons.index(sender)
        
        # Animate transition
        self.animate_page_transition(index)
        
        # Update status
        self.statusBar().showMessage(
            self.tr("Chargement du module: {}").format(sender.text().strip()), 
            3000)

    def animate_page_transition(self, index):
        """Animate the page transition"""
        # Fade out current
        fade_out = QGraphicsOpacityEffect(self.content_stack.currentWidget())
        self.content_stack.currentWidget().setGraphicsEffect(fade_out)
        
        anim_out = QPropertyAnimation(fade_out, b"opacity")
        anim_out.setDuration(200)
        anim_out.setStartValue(1)
        anim_out.setEndValue(0)
        
        # Change page
        anim_out.finished.connect(lambda: self.content_stack.setCurrentIndex(index))
        
        # Fade in new
        fade_in = QGraphicsOpacityEffect(self.content_stack.widget(index))
        self.content_stack.widget(index).setGraphicsEffect(fade_in)
        fade_in.setOpacity(0)
        
        anim_in = QPropertyAnimation(fade_in, b"opacity")
        anim_in.setDuration(300)
        anim_in.setStartValue(0)
        anim_in.setEndValue(1)
        
        # Start animations
        anim_out.start()
        anim_in.start()

    def show_welcome_animation(self):
        """Show welcome animation"""
        welcome = QLabel(self)
        welcome.setAlignment(Qt.AlignCenter)
        
        # Animated checkmark
        movie = QMovie(":/animations/welcome.gif")
        welcome.setMovie(movie)
        movie.start()
        
        # Center on screen
        welcome.setGeometry(
            self.width()//2 - 150, 
            self.height()//2 - 150, 
            300, 300
        )
        welcome.show()
        
        # Auto-close after animation
        QTimer.singleShot(3000, welcome.deleteLater)

    def setup_status_bar(self):
        """Configure the status bar"""
        self.statusBar().setStyleSheet(f"""
            background: {self.theme["background"]};
            color: {self.theme["text"]};
            padding: 5px;
            border-top: 1px solid #e0e0e0;
        """)

    def setup_user_profile(self, layout):
        """Create user profile section"""
        profile = QFrame()
        profile.setStyleSheet("""
            background: rgba(255, 255, 255, 0.12);
            border-radius: 18px;
        """)
        
        profile_layout = QHBoxLayout(profile)
        profile_layout.setContentsMargins(20, 15, 20, 15)
        
        # Avatar
        avatar = QLabel()
        avatar.setPixmap(QPixmap(":/icons/avatar.png").scaled(40, 40, 
                            Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # User info
        user_info = QVBoxLayout()
        
        name = QLabel(self.tr("Me"))
        name.setStyleSheet("""
            color: white;
            font-weight: 600;
            font-size: 14px;
        """)
        
        role = QLabel(self.tr("Administrateur"))
        role.setStyleSheet("""
            color: rgba(255, 255, 255, 0.7);
            font-size: 12px;
        """)
        
        user_info.addWidget(name)
        user_info.addWidget(role)
        
        # Add to layout
        profile_layout.addWidget(avatar)
        profile_layout.addLayout(user_info)
        profile_layout.addStretch()
        
        # Add to sidebar
        layout.addWidget(profile)

    def setup_animations(self):
        """Initialize animations system"""
        self.animations = {
            "page_transition": QPropertyAnimation(self, b"windowOpacity"),
            "sidebar_hover": QPropertyAnimation(self.sidebar, b"geometry")
        }
        
        for anim in self.animations.values():
            anim.setEasingCurve(QEasingCurve.OutCubic)
            anim.setDuration(350)

    def setup_system_tray(self):
        """Initialize system tray icon"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray = QSystemTrayIcon(QIcon(":/icons/app_icon.png"), self)
            
            menu = QMenu()
            menu.addAction(self.tr("Ouvrir"), self.show_normal)
            menu.addAction(self.tr("Quitter"), QApplication.quit)
            
            self.tray.setContextMenu(menu)
            self.tray.show()

    def setup_notifications(self):
        """Setup notification system"""
        self.notification_timer = QTimer()
        self.notification_timer.timeout.connect(self.check_notifications)
        self.notification_timer.start(60000)  # Check every minute

    def check_notifications(self):
        """Check for new notifications"""
        # In a real app, this would check your backend
        if hasattr(self, 'tray'):
            self.tray.showMessage(
                self.tr("Mise à jour disponible"),
                self.tr("Nouvelle version 2.5.0 disponible"),
                QSystemTrayIcon.Information, 
                3000
            )

    def show_normal(self):
        """Restore window from tray"""
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.raise_()

    def closeEvent(self, event):
        """Handle window close"""
        confirm = QMessageBox.question(
            self, 
            self.tr("Confirmation"),
            self.tr("Voulez-vous vraiment quitter l'application?"),
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = MainDashboard()
    window.show()
    
    sys.exit(app.exec_())

