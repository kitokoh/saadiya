import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QPushButton, QStackedWidget, QAction, QToolBar,
                            QFileDialog, QMessageBox, QStatusBar, QTabWidget, QFrame,
                            QListWidget, QListWidgetItem, QTextEdit, QComboBox, QLineEdit,
                            QFormLayout, QScrollArea, QSizePolicy, QSpacerItem)
from PyQt5.QtGui import (QIcon, QFont, QPixmap, QColor, QLinearGradient, QPainter,
                         QBrush, QPalette, QMovie)
from PyQt5.QtCore import (Qt, QSize, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup,
                          QSequentialAnimationGroup, pyqtProperty)

from PyQt5.QtWidgets import (
    QTreeWidget,
    QTreeWidgetItem,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QDoubleSpinBox,
    QSpinBox,
    QGroupBox,
    QCheckBox,
    QProgressDialog
)
import time


import time

class AnimatedButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._color = QColor(240, 240, 240)
        self.setStyleSheet("""
            QPushButton {
                border: 1px solid #8f8f91;
                border-radius: 6px;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                stop: 0 #f6f7fa, stop: 1 #dadbde);
                min-width: 80px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                stop: 0 #e0e1e4, stop: 1 #c0c1c4);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                stop: 0 #c0c1c4, stop: 1 #e0e1e4);
            }
        """)

        self.animation = QPropertyAnimation(self, b"color")
        self.animation.setDuration(300)

        self.click_animation = QPropertyAnimation(self, b"geometry")
        self.click_animation.setDuration(200)
        self.click_animation.setEasingCurve(QEasingCurve.OutQuad)

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color
        self.update()

    color = pyqtProperty(QColor, getColor, setColor)

    def enterEvent(self, event):
        self.animation.stop()
        self.animation.setEndValue(QColor(230, 230, 250))
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animation.stop()
        self.animation.setEndValue(QColor(240, 240, 240))
        self.animation.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.click_animation.stop()
        start_rect = self.geometry()
        end_rect = start_rect.adjusted(2, 2, -2, -2)
        self.click_animation.setStartValue(start_rect)
        self.click_animation.setEndValue(end_rect)

        reverse_animation = QPropertyAnimation(self, b"geometry")
        reverse_animation.setDuration(200)
        reverse_animation.setEasingCurve(QEasingCurve.OutQuad)
        reverse_animation.setStartValue(end_rect)
        reverse_animation.setEndValue(start_rect)

        seq_animation = QSequentialAnimationGroup()
        seq_animation.addAnimation(self.click_animation)
        seq_animation.addAnimation(reverse_animation)
        seq_animation.start()

        super().mousePressEvent(event)

class GradientFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(100)

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(70, 130, 180))
        gradient.setColorAt(1, QColor(30, 80, 130))

        painter.fillRect(self.rect(), gradient)

        # Ajouter un texte
        painter.setPen(Qt.white)
        font = QFont("Arial", 24, QFont.Bold)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, "Application Professionnelle")

        super().paintEvent(event)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Application Professionnelle Premium")
        self.setGeometry(100, 100, 1400, 900)

        # Configuration du style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QToolBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #f8f8f8, stop:1 #e7e7e7);
                border-bottom: 1px solid #d0d0d0;
                spacing: 5px;
                padding: 3px;
            }
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #e7e7e7, stop:1 #d0d0d0);
                border-top: 1px solid #c0c0c0;
            }
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                border-radius: 3px;
                background: white;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #f0f0f0, stop:1 #e0e0e0);
                border: 1px solid #c0c0c0;
                border-bottom-color: #c0c0c0;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 100px;
                padding: 5px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
            }
            QTabBar::tab:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #e8e8e8, stop:1 #d8d8d8);
            }
        """)

        # Création des pages
        self.pages = {
            "home": HomePage(),
            "install": InstallPage(),
            "open": OpenPage(),
            "log": LogPage(),
            "strategies": StrategiesPage(),
            "freq_ai": FreqAIPage()
        }

        self.setup_ui()

    def setup_ui(self):
        self.create_menu_bar()
        self.create_toolbar()
        self.create_status_bar()
        self.create_main_content()

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("""
            QMenuBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #f8f8f8, stop:1 #e7e7e7);
                border-bottom: 1px solid #d0d0d0;
                spacing: 5px;
            }
            QMenuBar::item {
                padding: 5px 10px;
                background: transparent;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background: #d0d0d0;
            }
            QMenuBar::item:pressed {
                background: #c0c0c0;
            }
        """)

        # Menu Fichier
        file_menu = menu_bar.addMenu("&Fichier")

        actions = [
            ("Nouveau", "new.png", self.on_new, "Ctrl+N"),
            ("Ouvrir", "open.png", self.on_open, "Ctrl+O"),
            ("Enregistrer", "save.png", self.on_save, "Ctrl+S"),
            ("Enregistrer sous...", "save_as.png", self.on_save_as, "Ctrl+Shift+S"),
            None,  # Séparateur
            ("Imprimer", "print.png", self.on_print, "Ctrl+P"),
            ("Exporter", "export.png", self.on_export, "Ctrl+E"),
            None,  # Séparateur
            ("Quitter", "exit.png", self.close, "Ctrl+Q")
        ]

        for action in actions:
            if action is None:
                file_menu.addSeparator()
            else:
                text, icon, callback, shortcut = action
                act = QAction(QIcon(f"icons/{icon}"), text, self)
                act.triggered.connect(callback)
                act.setShortcut(shortcut)
                file_menu.addAction(act)

        # Menu Édition
        edit_menu = menu_bar.addMenu("&Édition")

        actions = [
            ("Annuler", "undo.png", self.on_undo, "Ctrl+Z"),
            ("Rétablir", "redo.png", self.on_redo, "Ctrl+Y"),
            None,
            ("Couper", "cut.png", self.on_cut, "Ctrl+X"),
            ("Copier", "copy.png", self.on_copy, "Ctrl+C"),
            ("Coller", "paste.png", self.on_paste, "Ctrl+V"),
            ("Supprimer", "delete.png", self.on_delete, "Del"),
            None,
            ("Rechercher", "search.png", self.on_search, "Ctrl+F"),
            ("Remplacer", "replace.png", self.on_replace, "Ctrl+H")
        ]

        for action in actions:
            if action is None:
                edit_menu.addSeparator()
            else:
                text, icon, callback, shortcut = action
                act = QAction(QIcon(f"icons/{icon}"), text, self)
                act.triggered.connect(callback)
                act.setShortcut(shortcut)
                edit_menu.addAction(act)

        # Menu Affichage
        view_menu = menu_bar.addMenu("Affichage")

        actions = [
            ("Zoom avant", "zoom_in.png", self.on_zoom_in, "Ctrl++"),
            ("Zoom arrière", "zoom_out.png", self.on_zoom_out, "Ctrl+-"),
            ("Réinitialiser zoom", "zoom_reset.png", self.on_zoom_reset, "Ctrl+0"),
            None,
            ("Plein écran", "fullscreen.png", self.on_fullscreen, "F11")
        ]

        for action in actions:
            if action is None:
                view_menu.addSeparator()
            else:
                text, icon, callback, shortcut = action
                act = QAction(QIcon(f"icons/{icon}"), text, self)
                act.triggered.connect(callback)
                act.setShortcut(shortcut)
                view_menu.addAction(act)

        # Menu Outils
        tools_menu = menu_bar.addMenu("Outils")

        actions = [
            ("Préférences", "settings.png", self.on_preferences, None),
            ("Personnaliser", "customize.png", self.on_customize, None),
            ("Macros", "macros.png", self.on_macros, None),
            None,
            ("Analyse", "analyze.png", self.on_analyze, None),
            ("Optimisation", "optimize.png", self.on_optimize, None)
        ]

        for action in actions:
            if action is None:
                tools_menu.addSeparator()
            else:
                text, icon, callback, shortcut = action
                act = QAction(QIcon(f"icons/{icon}"), text, self)
                if shortcut:
                    act.setShortcut(shortcut)
                act.triggered.connect(callback)
                tools_menu.addAction(act)

        # Menu Aide
        help_menu = menu_bar.addMenu("Aide")

        actions = [
            ("Documentation", "help.png", self.on_help, "F1"),
            ("Vérifier les mises à jour", "update.png", self.on_update, None),
            None,
            ("À propos", "info.png", self.show_about, None)
        ]

        for action in actions:
            if action is None:
                help_menu.addSeparator()
            else:
                text, icon, callback, shortcut = action
                act = QAction(QIcon(f"icons/{icon}"), text, self)
                if shortcut:
                    act.setShortcut(shortcut)
                act.triggered.connect(callback)
                help_menu.addAction(act)

    def create_toolbar(self):
        # Barre d'outils principale
        main_toolbar = QToolBar("Barre d'outils principale")
        main_toolbar.setIconSize(QSize(32, 32))
        main_toolbar.setMovable(False)
        self.addToolBar(main_toolbar)

        # Boutons animés
        buttons = [
            ("Accueil", "home.png", "home", "Retour à la page d'accueil"),
            ("Install Bot", "install.png", "install", "Installer un nouveau bot"),
            ("Ouvrir", "open.png", "open", "Ouvrir un projet existant"),
            ("Logs", "log.png", "log", "Afficher les journaux d'activité"),
            ("Stratégies", "strategy.png", "strategies", "Gérer les stratégies"),
            ("Freq AI", "ai.png", "freq_ai", "Outils d'IA fréquentielle")
        ]

        for text, icon, page, tooltip in buttons:
            btn = AnimatedButton(QIcon(f"icons/{icon}"), " " + text)
            btn.setToolTip(tooltip)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, p=page: self.show_page(p))
            main_toolbar.addWidget(btn)

        main_toolbar.addSeparator()

        # Barre d'outils secondaire
        secondary_toolbar = QToolBar("Barre d'outils secondaire")
        secondary_toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(secondary_toolbar)

        quick_actions = [
            ("Nouveau", "new.png", self.on_new),
            ("Ouvrir", "open.png", self.on_open),
            ("Enregistrer", "save.png", self.on_save),
            ("Imprimer", "print.png", self.on_print),
            ("Couper", "cut.png", self.on_cut),
            ("Copier", "copy.png", self.on_copy),
            ("Coller", "paste.png", self.on_paste)
        ]

        for text, icon, callback in quick_actions:
            act = QAction(QIcon(f"icons/{icon}"), text, self)
            act.triggered.connect(callback)
            secondary_toolbar.addAction(act)

    def create_status_bar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        # Widgets de statut
        self.status_label = QLabel("Prêt")
        status_bar.addWidget(self.status_label, 1)

        self.progress_label = QLabel("")
        status_bar.addPermanentWidget(self.progress_label)

        version_label = QLabel("Version 2.0.0 Premium")
        status_bar.addPermanentWidget(version_label)

    def create_main_content(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Bannière avec dégradé
        banner = GradientFrame()
        banner.setFixedHeight(120)
        layout.addWidget(banner)

        # Contenu principal avec onglets
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        # Ajouter toutes les pages comme onglets
        for name, page in self.pages.items():
            self.tab_widget.addTab(page, self.get_tab_title(name))

        layout.addWidget(self.tab_widget)

        # Afficher la page d'accueil par défaut
        self.tab_widget.setCurrentIndex(0)

    def get_tab_title(self, page_name):
        titles = {
            "home": "Accueil",
            "install": "Install Bot",
            "open": "Ouvrir",
            "log": "Journaux",
            "strategies": "Stratégies",
            "freq_ai": "Freq AI"
        }
        return titles.get(page_name, page_name)

    def show_page(self, page_name):
        if page_name in self.pages:
            for i in range(self.tab_widget.count()):
                if self.tab_widget.widget(i) == self.pages[page_name]:
                    self.tab_widget.setCurrentIndex(i)
                    break

            self.status_label.setText(f"Affichage: {self.get_tab_title(page_name)}")

    def close_tab(self, index):
        if self.tab_widget.count() > 1:  # Ne pas fermer le dernier onglet
            self.tab_widget.removeTab(index)

    # Méthodes de gestion des actions
    def on_new(self):
        self.show_dialog("Nouveau fichier créé", "info")

    def on_open(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier", "", "Tous les fichiers (*)")
        if file_name:
            self.status_label.setText(f"Fichier ouvert: {file_name}")

    def on_save(self):
        self.show_dialog("Document enregistré", "info")

    def on_save_as(self):
        self.show_dialog("Document enregistré sous...", "info")

    def on_print(self):
        self.show_dialog("Impression démarrée", "info")

    def on_export(self):
        self.show_dialog("Exportation démarrée", "info")

    def on_undo(self):
        self.show_dialog("Action annulée", "info")

    def on_redo(self):
        self.show_dialog("Action rétablie", "info")

    def on_cut(self):
        self.show_dialog("Contenu coupé", "info")

    def on_copy(self):
        self.show_dialog("Contenu copié", "info")

    def on_paste(self):
        self.show_dialog("Contenu collé", "info")

    def on_delete(self):
        self.show_dialog("Contenu supprimé", "info")

    def on_search(self):
        self.show_dialog("Recherche activée", "info")

    def on_replace(self):
        self.show_dialog("Remplacement activé", "info")

    def on_zoom_in(self):
        self.show_dialog("Zoom avant", "info")

    def on_zoom_out(self):
        self.show_dialog("Zoom arrière", "info")

    def on_zoom_reset(self):
        self.show_dialog("Zoom réinitialisé", "info")

    def on_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def on_preferences(self):
        self.show_dialog("Préférences ouvertes", "info")

    def on_customize(self):
        self.show_dialog("Personnalisation activée", "info")

    def on_macros(self):
        self.show_dialog("Gestion des macros", "info")

    def on_analyze(self):
        self.show_dialog("Analyse démarrée", "info")

    def on_optimize(self):
        self.show_dialog("Optimisation démarrée", "info")

    def on_help(self):
        self.show_dialog("Documentation ouverte", "info")

    def on_update(self):
        self.show_dialog("Recherche de mises à jour...", "info")

    def show_about(self):
        about_text = """
        <h2>Application Professionnelle Premium</h2>
        <p>Version 2.0.0</p>
        <p>© 2023 Tous droits réservés</p>
        <p>Une application haut de gamme avec interface moderne, animations fluides et fonctionnalités avancées.</p>
        """
        QMessageBox.about(self, "À propos", about_text)

    def show_dialog(self, message, icon_type):
        icons = {
            "info": QMessageBox.Information,
            "warning": QMessageBox.Warning,
            "error": QMessageBox.Critical
        }
        QMessageBox(icons.get(icon_type, QMessageBox.Information),
                   "Information", message, QMessageBox.Ok, self).exec_()

class PageTemplate(QWidget):
    def __init__(self, title, icon_name=None):
        super().__init__()
        self.title = title
        self.icon_name = icon_name
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # En-tête de page
        header = QHBoxLayout()

        if self.icon_name:
            icon_label = QLabel()
            icon_label.setPixmap(QIcon(f"icons/{self.icon_name}").pixmap(48, 48))
            header.addWidget(icon_label)

        title_label = QLabel(self.title)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        header.addWidget(title_label, 1)

        header.addStretch()

        self.main_layout.addLayout(header)

        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(separator)

        # Contenu (à implémenter par les sous-classes)
        self.setup_content()

    def setup_content(self):
        # Méthode à surcharger par les sous-classes
        pass

class HomePage(PageTemplate):
    def __init__(self):
        super().__init__("Tableau de Bord", "home.png")

    def setup_content(self):
        # Layout principal avec scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Section de bienvenue
        welcome_label = QLabel("Bienvenue dans l'Application Professionnelle Premium")
        welcome_label.setFont(QFont("Arial", 14))
        welcome_label.setStyleSheet("color: #2a5caa;")
        scroll_layout.addWidget(welcome_label)

        # Widget avec animation
        animation_widget = QLabel()
        movie = QMovie("icons/welcome.gif")  # Remplacez par un vrai fichier GIF
        movie.setScaledSize(QSize(600, 200))
        animation_widget.setMovie(movie)
        movie.start()
        scroll_layout.addWidget(animation_widget, 0, Qt.AlignCenter)

        # Cartes d'information
        cards_layout = QHBoxLayout()

        cards = [
            ("Dernières Activités", "activity.png", "#4a6da7"),
            ("Statistiques", "stats.png", "#a74a6d"),
            ("Performances", "performance.png", "#6da74a")
        ]

        for title, icon, color in cards:
            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)
            card.setLineWidth(1)
            card.setFixedSize(250, 150)
            card.setStyleSheet(f"background-color: {color}; border-radius: 8px;")

            card_layout = QVBoxLayout(card)
            card_layout.setAlignment(Qt.AlignCenter)

            icon_label = QLabel()
            icon_label.setPixmap(QIcon(f"icons/{icon}").pixmap(48, 48))
            card_layout.addWidget(icon_label, 0, Qt.AlignCenter)

            title_label = QLabel(title)
            title_label.setStyleSheet("color: white; font-weight: bold;")
            card_layout.addWidget(title_label, 0, Qt.AlignCenter)

            cards_layout.addWidget(card)

        scroll_layout.addLayout(cards_layout)

        # Section récente
        recent_label = QLabel("Projets Récents")
        recent_label.setFont(QFont("Arial", 12, QFont.Bold))
        scroll_layout.addWidget(recent_label)

        recent_list = QListWidget()
        recent_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 5px;
                background: white;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e0e0e0;
            }
            QListWidget::item:hover {
                background: #f0f0f0;
            }
        """)

        for i in range(5):
            item = QListWidgetItem(f"Projet récent {i+1} - Modifié aujourd'hui")
            recent_list.addItem(item)

        scroll_layout.addWidget(recent_list)

        scroll.setWidget(scroll_content)
        self.main_layout.addWidget(scroll)

class InstallPage(PageTemplate):
    def __init__(self):
        super().__init__("Installation de Bot", "install.png")

    def setup_content(self):
        form_layout = QFormLayout()
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(15)

        # Configuration du bot
        self.bot_name = QLineEdit()
        self.bot_name.setPlaceholderText("Entrez le nom du bot")

        self.bot_type = QComboBox()
        self.bot_type.addItems(["Trading", "Analyse", "Surveillance", "Automatisation"])

        self.bot_version = QComboBox()
        self.bot_version.addItems(["Stable", "Beta", "Alpha"])

        self.install_path = QLineEdit()
        self.install_path.setPlaceholderText("Sélectionnez le dossier d'installation")
        browse_btn = QPushButton("Parcourir...")
        browse_btn.clicked.connect(self.select_install_path)

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.install_path)
        path_layout.addWidget(browse_btn)

        form_layout.addRow("Nom du bot:", self.bot_name)
        form_layout.addRow("Type de bot:", self.bot_type)
        form_layout.addRow("Version:", self.bot_version)
        form_layout.addRow("Dossier d'installation:", path_layout)

        # Options avancées
        advanced_group = QFrame()
        advanced_group.setFrameShape(QFrame.StyledPanel)
        advanced_group.setLayout(QVBoxLayout())

        advanced_label = QLabel("Options Avancées")
        advanced_label.setFont(QFont("Arial", 10, QFont.Bold))
        advanced_group.layout().addWidget(advanced_label)

        self.auto_start = QCheckBox("Démarrer automatiquement après installation")
        self.create_desktop_icon = QCheckBox("Créer un raccourci sur le bureau")
        self.log_verbose = QCheckBox("Journalisation détaillée")

        advanced_group.layout().addWidget(self.auto_start)
        advanced_group.layout().addWidget(self.create_desktop_icon)
        advanced_group.layout().addWidget(self.log_verbose)

        # Boutons d'action
        button_layout = QHBoxLayout()
        install_btn = QPushButton("Installer")
        install_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        install_btn.clicked.connect(self.start_installation)

        cancel_btn = QPushButton("Annuler")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        cancel_btn.clicked.connect(self.cancel_installation)

        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(install_btn)

        # Ajout au layout principal
        self.main_layout.addLayout(form_layout)
        self.main_layout.addWidget(advanced_group)
        self.main_layout.addStretch()
        self.main_layout.addLayout(button_layout)

    def select_install_path(self):
        path = QFileDialog.getExistingDirectory(self, "Sélectionnez le dossier d'installation")
        if path:
            self.install_path.setText(path)

    def start_installation(self):
        QMessageBox.information(self, "Installation", "L'installation du bot a commencé.")

    def cancel_installation(self):
        self.bot_name.clear()
        self.install_path.clear()
        self.bot_type.setCurrentIndex(0)
        self.bot_version.setCurrentIndex(0)
        self.auto_start.setChecked(False)
        self.create_desktop_icon.setChecked(False)
        self.log_verbose.setChecked(False)

class OpenPage(PageTemplate):
    def __init__(self):
        super().__init__("Ouvrir un Projet", "folder.png")

    def setup_content(self):
        main_splitter = QSplitter(Qt.Horizontal)

        # Panel gauche - Arborescence
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        tree_label = QLabel("Explorateur de Projets")
        tree_label.setFont(QFont("Arial", 10, QFont.Bold))
        left_layout.addWidget(tree_label)

        self.project_tree = QTreeWidget()
        self.project_tree.setHeaderHidden(True)
        self.project_tree.setStyleSheet("""
            QTreeWidget {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 5px;
                background: white;
            }
            QTreeWidget::item {
                padding: 5px;
            }
            QTreeWidget::item:hover {
                background: #f0f0f0;
            }
        """)

        # Ajouter des éléments de démonstration
        root_item = QTreeWidgetItem(self.project_tree, ["Mes Projets"])

        categories = ["Trading", "Analyse", "Automatisation", "Tests"]
        for cat in categories:
            cat_item = QTreeWidgetItem(root_item, [cat])
            for i in range(3):
                QTreeWidgetItem(cat_item, [f"Projet {i+1}"])

        self.project_tree.expandAll()
        left_layout.addWidget(self.project_tree)

        # Panel droit - Détails
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        details_label = QLabel("Détails du Projet")
        details_label.setFont(QFont("Arial", 10, QFont.Bold))
        right_layout.addWidget(details_label)

        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 10px;
                background: white;
            }
        """)
        self.details_text.setHtml("""
            <h3>Sélectionnez un projet dans l'arborescence</h3>
            <p>Les détails du projet sélectionné apparaîtront ici.</p>
        """)

        right_layout.addWidget(self.details_text)

        # Boutons d'action
        button_layout = QHBoxLayout()
        open_btn = QPushButton("Ouvrir")
        open_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)

        cancel_btn = QPushButton("Annuler")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)

        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(open_btn)

        right_layout.addLayout(button_layout)

        # Configurer le splitter
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(right_panel)
        main_splitter.setSizes([300, 500])

        self.main_layout.addWidget(main_splitter)

        # Connecter les signaux
        self.project_tree.itemClicked.connect(self.update_project_details)

    def update_project_details(self, item):
        if item.parent():  # Ne pas afficher les catégories
            self.details_text.setHtml(f"""
                <h3>{item.text(0)}</h3>
                <p><b>Chemin:</b> /projets/{item.parent().text(0).lower()}/{item.text(0).replace(' ', '_').lower()}</p>
                <p><b>Dernière modification:</b> Aujourd'hui</p>
                <p><b>Taille:</b> 2.5 MB</p>
                <p><b>Description:</b> Ceci est un projet de démonstration avec des données fictives.</p>
            """)

class LogPage(PageTemplate):
    def __init__(self):
        super().__init__("Journal des Activités", "log.png")

    def setup_content(self):
        # Contrôles de filtrage
        filter_layout = QHBoxLayout()

        self.log_type = QComboBox()
        self.log_type.addItems(["Tous", "Information", "Avertissement", "Erreur", "Debug"])

        self.date_filter = QComboBox()
        self.date_filter.addItems(["Aujourd'hui", "Cette semaine", "Ce mois", "Toutes les dates"])

        search_edit = QLineEdit()
        search_edit.setPlaceholderText("Rechercher dans les logs...")
        search_btn = QPushButton(QIcon("icons/search.png"), "")

        filter_layout.addWidget(QLabel("Type:"))
        filter_layout.addWidget(self.log_type)
        filter_layout.addWidget(QLabel("Date:"))
        filter_layout.addWidget(self.date_filter)
        filter_layout.addWidget(search_edit)
        filter_layout.addWidget(search_btn)

        # Tableau des logs
        self.log_table = QTableWidget()
        self.log_table.setColumnCount(4)
        self.log_table.setHorizontalHeaderLabels(["Date/Heure", "Type", "Source", "Message"])
        self.log_table.horizontalHeader().setStretchLastSection(True)
        self.log_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.log_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Style du tableau
        self.log_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                background: white;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: none;
            }
        """)

        # Ajouter des données de démonstration
        self.populate_logs()

        # Boutons d'action
        button_layout = QHBoxLayout()
        refresh_btn = QPushButton("Actualiser")
        export_btn = QPushButton("Exporter")
        clear_btn = QPushButton("Effacer")

        button_layout.addStretch()
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(export_btn)
        button_layout.addWidget(clear_btn)

        # Ajout au layout principal
        self.main_layout.addLayout(filter_layout)
        self.main_layout.addWidget(self.log_table)
        self.main_layout.addLayout(button_layout)

        # Connecter les signaux
        refresh_btn.clicked.connect(self.populate_logs)
        export_btn.clicked.connect(self.export_logs)
        clear_btn.clicked.connect(self.clear_logs)

    def populate_logs(self):
        self.log_table.setRowCount(0)

        log_types = ["INFO", "WARN", "ERROR", "DEBUG"]
        log_sources = ["System", "Database", "Network", "Security", "Application"]

        from random import choice, randint
        from datetime import datetime, timedelta

        for i in range(50):
            row_pos = self.log_table.rowCount()
            self.log_table.insertRow(row_pos)

            # Date aléatoire dans les 7 derniers jours
            log_time = datetime.now() - timedelta(days=randint(0, 7),
                                                 hours=randint(0, 23),
                                                 minutes=randint(0, 59))

            log_type = choice(log_types)
            log_source = choice(log_sources)
            log_msg = f"Message de log exemple {i+1} avec des données aléatoires"

            self.log_table.setItem(row_pos, 0, QTableWidgetItem(log_time.strftime("%Y-%m-%d %H:%M:%S")))
            self.log_table.setItem(row_pos, 1, QTableWidgetItem(log_type))
            self.log_table.setItem(row_pos, 2, QTableWidgetItem(log_source))
            self.log_table.setItem(row_pos, 3, QTableWidgetItem(log_msg))

            # Colorer les lignes selon le type
            if log_type == "ERROR":
                for col in range(4):
                    self.log_table.item(row_pos, col).setBackground(QColor(255, 230, 230))
            elif log_type == "WARN":
                for col in range(4):
                    self.log_table.item(row_pos, col).setBackground(QColor(255, 255, 230))
            elif log_type == "DEBUG":
                for col in range(4):
                    self.log_table.item(row_pos, col).setBackground(QColor(230, 240, 255))

    def export_logs(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Exporter les logs", "", "Fichiers CSV (*.csv)")
        if file_name:
            QMessageBox.information(self, "Export", f"Les logs ont été exportés vers {file_name}")

    def clear_logs(self):
        reply = QMessageBox.question(self, "Effacer les logs",
                                   "Voulez-vous vraiment effacer tous les logs?",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.log_table.setRowCount(0)

class StrategiesPage(PageTemplate):
    def __init__(self):
        super().__init__("Gestion des Stratégies", "strategy.png")

    def setup_content(self):
        # Layout principal avec splitter
        main_splitter = QSplitter(Qt.Horizontal)

        # Panel gauche - Liste des stratégies
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        list_label = QLabel("Stratégies Disponibles")
        list_label.setFont(QFont("Arial", 10, QFont.Bold))
        left_layout.addWidget(list_label)

        self.strategy_list = QListWidget()
        self.strategy_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 5px;
                background: white;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e0e0e0;
            }
            QListWidget::item:hover {
                background: #f0f0f0;
            }
            QListWidget::item:selected {
                background: #d0e0ff;
            }
        """)

        # Ajouter des stratégies de démonstration
        strategies = [
            "Moyenne Mobile Crossover",
            "Stratégie de Momentum",
            "Stratégie Mean Reversion",
            "Breakout Trading",
            "Scalping Algorithmique",
            "Stratégie de Suivi de Tendance",
            "Arbitrage Statistique"
        ]

        for strat in strategies:
            item = QListWidgetItem(strat)
            item.setIcon(QIcon("icons/strategy.png"))
            self.strategy_list.addItem(item)

        left_layout.addWidget(self.strategy_list)

        # Boutons de gestion
        btn_layout = QHBoxLayout()
        new_btn = QPushButton("Nouvelle")
        edit_btn = QPushButton("Modifier")
        delete_btn = QPushButton("Supprimer")

        btn_layout.addWidget(new_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)

        left_layout.addLayout(btn_layout)

        # Panel droit - Détails et configuration
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        details_label = QLabel("Configuration de la Stratégie")
        details_label.setFont(QFont("Arial", 10, QFont.Bold))
        right_layout.addWidget(details_label)

        self.details_stack = QStackedWidget()

        # Page vide initiale
        empty_page = QWidget()
        empty_layout = QVBoxLayout(empty_page)
        empty_layout.addWidget(QLabel("Sélectionnez une stratégie pour configurer"), 1, Qt.AlignCenter)
        self.details_stack.addWidget(empty_page)

        # Ajouter des pages de configuration pour chaque stratégie
        for strat in strategies:
            config_page = self.create_strategy_config_page(strat)
            self.details_stack.addWidget(config_page)

        right_layout.addWidget(self.details_stack)

        # Boutons d'action
        action_layout = QHBoxLayout()
        save_btn = QPushButton("Enregistrer")
        test_btn = QPushButton("Tester la Stratégie")
        apply_btn = QPushButton("Appliquer")

        action_layout.addWidget(save_btn)
        action_layout.addWidget(test_btn)
        action_layout.addStretch()
        action_layout.addWidget(apply_btn)

        right_layout.addLayout(action_layout)

        # Configurer le splitter
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(right_panel)
        main_splitter.setSizes([250, 550])

        self.main_layout.addWidget(main_splitter)

        # Connecter les signaux
        self.strategy_list.currentRowChanged.connect(self.details_stack.setCurrentIndex)
        new_btn.clicked.connect(self.new_strategy)
        edit_btn.clicked.connect(self.edit_strategy)
        delete_btn.clicked.connect(self.delete_strategy)

    def create_strategy_config_page(self, strategy_name):
        page = QWidget()
        layout = QVBoxLayout(page)

        # En-tête
        header = QLabel(strategy_name)
        header.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(header)

        # Séparateur
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        layout.addWidget(sep)

        # Description
        desc_label = QLabel("Description:")
        desc_label.setFont(QFont("Arial", 10))

        desc_text = QTextEdit()
        desc_text.setPlainText(f"Description de la stratégie {strategy_name}.\n\nCette stratégie est conçue pour...")
        desc_text.setMaximumHeight(80)

        layout.addWidget(desc_label)
        layout.addWidget(desc_text)

        # Paramètres
        params_label = QLabel("Paramètres:")
        params_label.setFont(QFont("Arial", 10))

        params_frame = QFrame()
        params_frame.setFrameShape(QFrame.StyledPanel)
        params_layout = QFormLayout(params_frame)

        # Ajouter des paramètres selon la stratégie
        if "Moyenne Mobile" in strategy_name:
            params_layout.addRow("Période courte:", QSpinBox())
            params_layout.addRow("Période longue:", QSpinBox())
            params_layout.addRow("Seuil d'activation:", QDoubleSpinBox())
        elif "Momentum" in strategy_name:
            params_layout.addRow("Période de lookback:", QSpinBox())
            params_layout.addRow("Seuil d'achat:", QDoubleSpinBox())
            params_layout.addRow("Seuil de vente:", QDoubleSpinBox())
        else:  # Paramètres par défaut
            params_layout.addRow("Paramètre 1:", QLineEdit())
            params_layout.addRow("Paramètre 2:", QComboBox())
            params_layout.addRow("Paramètre 3:", QDoubleSpinBox())

        layout.addWidget(params_label)
        layout.addWidget(params_frame)

        # Performances (graphique simulé)
        perf_label = QLabel("Performances Historiques:")
        perf_label.setFont(QFont("Arial", 10))

        perf_widget = QLabel()
        perf_widget.setFixedHeight(150)
        perf_widget.setStyleSheet("background-color: white; border: 1px solid #d0d0d0;")

        # Simuler un graphique avec du texte
        perf_widget.setText("""
            <center>
                <p>[Graphique de performance simulé]</p>
                <p>Rendement: +15.2%</p>
                <p>Sharpe Ratio: 1.8</p>
                <p>Max Drawdown: -8.4%</p>
            </center>
        """)
        perf_widget.setAlignment(Qt.AlignCenter)

        layout.addWidget(perf_label)
        layout.addWidget(perf_widget)

        layout.addStretch()

        return page

    def new_strategy(self):
        QMessageBox.information(self, "Nouvelle Stratégie", "Création d'une nouvelle stratégie")

    def edit_strategy(self):
        current = self.strategy_list.currentRow()
        if current >= 0:
            QMessageBox.information(self, "Modifier", f"Modification de la stratégie sélectionnée")

    def delete_strategy(self):
        current = self.strategy_list.currentRow()
        if current >= 0:
            reply = QMessageBox.question(self, "Supprimer",
                                       "Voulez-vous vraiment supprimer cette stratégie?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.strategy_list.takeItem(current)

class FreqAIPage(PageTemplate):
    def __init__(self):
        super().__init__("Freq AI - Intelligence Artificielle", "ai.png")

    def setup_content(self):
        # Layout principal avec onglets
        tab_widget = QTabWidget()

        # Onglet Analyse
        analysis_tab = QWidget()
        analysis_layout = QVBoxLayout(analysis_tab)

        analysis_desc = QLabel("""
            <h3>Analyse Fréquentielle avec IA</h3>
            <p>Cet outil utilise des algorithmes d'intelligence artificielle pour analyser les motifs fréquentiels dans vos données.</p>
        """)
        analysis_desc.setWordWrap(True)
        analysis_layout.addWidget(analysis_desc)

        # Configuration de l'analyse
        config_group = QGroupBox("Configuration de l'Analyse")
        config_layout = QFormLayout(config_group)

        self.data_source = QComboBox()
        self.data_source.addItems(["Base de données locale", "API externe", "Fichier CSV", "Flux en temps réel"])

        self.analysis_type = QComboBox()
        self.analysis_type.addItems(["Analyse spectrale", "Détection d'anomalies", "Prédiction", "Classification"])

        self.time_range = QComboBox()
        self.time_range.addItems(["Dernières 24h", "Dernière semaine", "Dernier mois", "Dernière année", "Personnalisé..."])

        config_layout.addRow("Source des données:", self.data_source)
        config_layout.addRow("Type d'analyse:", self.analysis_type)
        config_layout.addRow("Plage temporelle:", self.time_range)

        analysis_layout.addWidget(config_group)

        # Boutons d'action
        btn_layout = QHBoxLayout()
        analyze_btn = QPushButton("Lancer l'Analyse")
        analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        export_btn = QPushButton("Exporter les Résultats")

        btn_layout.addStretch()
        btn_layout.addWidget(export_btn)
        btn_layout.addWidget(analyze_btn)

        analysis_layout.addLayout(btn_layout)

        # Onglet Résultats
        results_tab = QWidget()
        results_layout = QVBoxLayout(results_tab)

        results_label = QLabel("<h3>Résultats de l'Analyse</h3>")
        results_layout.addWidget(results_label)

        # Simuler un graphique de résultats
        results_widget = QLabel()
        results_widget.setStyleSheet("background-color: white; border: 1px solid #d0d0d0;")
        results_widget.setFixedHeight(300)
        results_widget.setText("""
            <center>
                <p>[Graphique d'analyse fréquentielle simulé]</p>
                <p>Fréquences dominantes détectées: 0.25Hz, 0.5Hz, 1.0Hz</p>
                <p>Anomalies détectées: 3</p>
                <p>Confiance du modèle: 87.5%</p>
            </center>
        """)
        results_widget.setAlignment(Qt.AlignCenter)
        results_layout.addWidget(results_widget)

        # Tableau de données
        results_table = QTableWidget(5, 3)
        results_table.setHorizontalHeaderLabels(["Fréquence", "Amplitude", "Signification"])
        results_table.horizontalHeader().setStretchLastSection(True)
        results_table.verticalHeader().setVisible(False)

        # Remplir avec des données simulées
        for row in range(5):
            freq_item = QTableWidgetItem(f"{0.25 * (row + 1):.2f} Hz")
            amp_item = QTableWidgetItem(f"{100 - row * 15}%")
            sig_item = QTableWidgetItem(["Bruit", "Signal faible", "Signal moyen", "Signal fort", "Dominant"][row])

            results_table.setItem(row, 0, freq_item)
            results_table.setItem(row, 1, amp_item)
            results_table.setItem(row, 2, sig_item)

        results_layout.addWidget(results_table)

        # Ajouter les onglets
        tab_widget.addTab(analysis_tab, "Analyse")
        tab_widget.addTab(results_tab, "Résultats")

        self.main_layout.addWidget(tab_widget)

        # Connecter les signaux
        analyze_btn.clicked.connect(self.run_analysis)
        export_btn.clicked.connect(self.export_results)

    def run_analysis(self):
        # Simuler une analyse avec une barre de progression
        progress = QProgressDialog("Analyse en cours...", "Annuler", 0, 100, self)
        progress.setWindowModality(Qt.WindowModal)

        for i in range(101):
            progress.setValue(i)
            QApplication.processEvents()
            if progress.wasCanceled():
                break
            time.sleep(0.05)

        progress.close()

        if not progress.wasCanceled():
            QMessageBox.information(self, "Analyse terminée", "L'analyse fréquentielle a été complétée avec succès!")
            self.main_layout.widget().setCurrentIndex(1)  # Basculer vers l'onglet Résultats

    def export_results(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Exporter les résultats", "", "Fichiers PDF (*.pdf);;Fichiers CSV (*.csv)")
        if file_name:
            QMessageBox.information(self, "Export réussi", f"Les résultats ont été exportés vers:\n{file_name}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set application style and attributes
    app.setStyle("Fusion")
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Create and show the dialog
    dialog = MainWindow()
    dialog.show()

    sys.exit(app.exec_())
