import sys
import sqlite3
import webbrowser
import threading
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QCheckBox, QGroupBox, QPushButton, QMessageBox,
                             QListWidget, QTabWidget, QTimeEdit, QSystemTrayIcon, QMenu,
                             QGridLayout)
from PyQt5.QtCore import Qt, QTimer, QTime, QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QTextEdit

class SocialMediaPublisher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ultimate Social Publisher")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("icon.png"))

        # Configuration des paramètres
        self.settings = QSettings("SocialPublisher", "UltimatePublisher")

        # Initialisation de la base de données
        self.init_db()

        # Configuration Chrome
        self.chrome_path = self.get_chrome_path()

        # Création de l'interface
        self.init_ui()

        # Système de notifications
        self.init_notifications()

        # Charger les données
        self.load_data()

        # Vérifier les publications planifiées
        self.check_scheduled_posts()

    def get_chrome_path(self):
        """Détecte le chemin de Chrome selon l'OS"""
        import platform
        system = platform.system()

        if system == "Windows":
            return "C:/Program Files/Google/Chrome/Application/chrome.exe"
        elif system == "Darwin":
            return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        else:  # Linux et autres
            return "/usr/bin/google-chrome"

    def init_db(self):
        self.conn = sqlite3.connect('social_media.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS platform_prefs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT UNIQUE,
                selected INTEGER DEFAULT 0,
                is_favorite INTEGER DEFAULT 0
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS publication_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platforms TEXT,
                timestamp DATETIME,
                scheduled INTEGER DEFAULT 0,
                scheduled_time TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platforms TEXT,
                scheduled_time TEXT,
                executed INTEGER DEFAULT 0
            )
        ''')

        self.conn.commit()

    def init_notifications(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))

        tray_menu = QMenu()
        show_action = tray_menu.addAction("Ouvrir l'application")
        show_action.triggered.connect(self.show_normal)
        exit_action = tray_menu.addAction("Quitter")
        exit_action.triggered.connect(self.quit_app)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def show_normal(self):
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()

    def quit_app(self):
        self.conn.close()
        QApplication.quit()

    def show_notification(self, title, message):
        self.tray_icon.showMessage(title, message, QSystemTrayIcon.Information, 5000)

    def init_ui(self):
        # Style moderne avec QSS
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QGroupBox {
                border: 1px solid #dee2e6;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton {
                padding: 8px 12px;
                border-radius: 4px;
                min-width: 120px;
                font-size: 14px;
            }
            QListWidget {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 6px;
                font-size: 14px;
            }
            QCheckBox {
                font-size: 14px;
                spacing: 6px;
            }
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 4px;
                margin-top: 4px;
            }
            QTabBar::tab {
                padding: 8px 12px;
            }
            QTimeEdit {
                padding: 5px;
                font-size: 14px;
            }
        """)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Onglets principaux
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Onglet Publication
        self.create_publish_tab()

        # Onglet Historique
        self.create_history_tab()

        # Onglet Planifications
        self.create_scheduled_tab()

        # Onglet Paramètres
        self.create_settings_tab()

    def create_publish_tab(self):
        """Crée l'onglet de publication"""
        tab = QWidget()
        self.tab_widget.addTab(tab, "Publication")
        layout = QVBoxLayout(tab)

        # Section plateformes
        platforms_group = QGroupBox("Sélectionnez les plateformes")
        platforms_layout = QVBoxLayout()

        # Liste des plateformes avec leurs URLs de publication
        self.platforms_data = [
            ("Facebook", "https://www.facebook.com/", "fb"),
            ("Twitter", "https://twitter.com/compose/tweet", "tw"),
            ("LinkedIn", "https://www.linkedin.com/shareArticle?mini=true", "li"),
            ("Reddit", "https://www.reddit.com/submit", "rd"),
            ("Tumblr", "https://www.tumblr.com/new", "tb"),
            ("Instagram", "https://www.instagram.com/", "ig"),
            ("Pinterest", "https://www.pinterest.com/pin-builder/", "pn"),
            ("YouTube", "https://www.youtube.com/upload", "yt")
        ]

        # Cases à cocher pour les plateformes
        self.platform_checkboxes = []

        # Layout pour les plateformes en deux colonnes
        platforms_grid = QGridLayout()

        for index, (platform, url, short) in enumerate(self.platforms_data):
            checkbox = QCheckBox(platform)
            checkbox.setObjectName(f"platform_{short}")
            self.platform_checkboxes.append(checkbox)

            # Bouton favori
            fav_btn = QPushButton("★")
            fav_btn.setCheckable(True)
            fav_btn.setObjectName(f"fav_{short}")
            fav_btn.setFixedSize(24, 24)
            fav_btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    border: none;
                    background: transparent;
                }
                QPushButton:checked {
                    color: gold;
                }
            """)
            fav_btn.clicked.connect(lambda _, p=platform: self.toggle_favorite(p))

            # Layout pour chaque plateforme
            platform_row = QHBoxLayout()
            platform_row.addWidget(checkbox)
            platform_row.addWidget(fav_btn)
            platform_row.addStretch()

            # Ajouter à la grille
            row = index // 2
            col = index % 2
            platforms_grid.addLayout(platform_row, row, col)

        platforms_layout.addLayout(platforms_grid)
        platforms_group.setLayout(platforms_layout)
        layout.addWidget(platforms_group)

        # Options de publication
        options_group = QGroupBox("Options de publication")
        options_layout = QHBoxLayout()

        # Planification
        self.schedule_check = QCheckBox("Planifier la publication")
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime(9, 0))  # Par défaut à 9h
        self.time_edit.setEnabled(False)
        self.schedule_check.stateChanged.connect(self.toggle_schedule_ui)

        options_layout.addWidget(self.schedule_check)
        options_layout.addWidget(self.time_edit)
        options_layout.addStretch()

        options_group.setLayout(options_layout)
        layout.addWidget(options_group)

        # Boutons d'action
        btn_layout = QHBoxLayout()

        self.publish_btn = QPushButton("Publier maintenant")
        self.publish_btn.setStyleSheet("background-color: #28a745; color: white; font-weight: bold;")
        self.publish_btn.clicked.connect(self.publish_now)

        self.schedule_btn = QPushButton("Planifier")
        self.schedule_btn.setStyleSheet("background-color: #17a2b8; color: white;")
        self.schedule_btn.setEnabled(False)
        self.schedule_btn.clicked.connect(self.schedule_publication)

        btn_layout.addWidget(self.publish_btn)
        btn_layout.addWidget(self.schedule_btn)
        layout.addLayout(btn_layout)

    def create_history_tab(self):
        """Crée l'onglet d'historique"""
        tab = QWidget()
        self.tab_widget.addTab(tab, "Historique")
        layout = QVBoxLayout(tab)

        # Liste d'historique
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.show_history_item)
        layout.addWidget(self.history_list)

        # Boutons d'action
        btn_layout = QHBoxLayout()

        refresh_btn = QPushButton("Actualiser")
        refresh_btn.setStyleSheet("background-color: #6c757d; color: white;")
        refresh_btn.clicked.connect(self.load_history)

        clear_btn = QPushButton("Effacer l'historique")
        clear_btn.setStyleSheet("background-color: #dc3545; color: white;")
        clear_btn.clicked.connect(self.clear_history)

        btn_layout.addWidget(refresh_btn)
        btn_layout.addWidget(clear_btn)
        layout.addLayout(btn_layout)

    def create_scheduled_tab(self):
        """Crée l'onglet des publications planifiées"""
        tab = QWidget()
        self.tab_widget.addTab(tab, "Planifications")
        layout = QVBoxLayout(tab)

        # Liste des planifications
        self.scheduled_list = QListWidget()
        self.scheduled_list.itemDoubleClicked.connect(self.show_scheduled_item)
        layout.addWidget(self.scheduled_list)

        # Boutons d'action
        btn_layout = QHBoxLayout()

        cancel_btn = QPushButton("Annuler la sélection")
        cancel_btn.setStyleSheet("background-color: #ffc107; color: #212529;")
        cancel_btn.clicked.connect(self.cancel_scheduled)

        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def create_settings_tab(self):
        """Crée l'onglet des paramètres"""
        tab = QWidget()
        self.tab_widget.addTab(tab, "Paramètres")
        layout = QVBoxLayout(tab)

        # Groupe paramètres Chrome
        chrome_group = QGroupBox("Paramètres du navigateur")
        chrome_layout = QVBoxLayout()

        self.chrome_path_edit = QTextEdit()
        self.chrome_path_edit.setPlainText(self.chrome_path)
        self.chrome_path_edit.setMaximumHeight(60)

        test_btn = QPushButton("Tester Chrome")
        test_btn.clicked.connect(self.test_chrome)

        chrome_layout.addWidget(QLabel("Chemin de Chrome:"))
        chrome_layout.addWidget(self.chrome_path_edit)
        chrome_layout.addWidget(test_btn)
        chrome_group.setLayout(chrome_layout)
        layout.addWidget(chrome_group)

        # Bouton sauvegarde
        save_btn = QPushButton("Sauvegarder les paramètres")
        save_btn.setStyleSheet("background-color: #007bff; color: white;")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)

        layout.addStretch()

    def toggle_schedule_ui(self, state):
        """Active/désactive l'interface de planification"""
        enabled = state == Qt.Checked
        self.time_edit.setEnabled(enabled)
        self.schedule_btn.setEnabled(enabled)
        self.publish_btn.setEnabled(not enabled)

    def toggle_favorite(self, platform):
        """Marque/démarque une plateforme comme favorite"""
        for checkbox in self.platform_checkboxes:
            if checkbox.text() == platform:
                fav_btn = self.findChild(QPushButton, f"fav_{checkbox.objectName().split('_')[1]}")
                is_favorite = fav_btn.isChecked()

                self.cursor.execute(
                    "UPDATE platform_prefs SET is_favorite = ? WHERE platform = ?",
                    (1 if is_favorite else 0, platform)
                )
                self.conn.commit()
                break

    def load_data(self):
        """Charge les données sauvegardées"""
        # Charger les préférences des plateformes
        for platform, _, short in self.platforms_data:
            self.cursor.execute(
                "SELECT selected, is_favorite FROM platform_prefs WHERE platform = ?",
                (platform,)
            )
            result = self.cursor.fetchone()

            if result:
                selected, is_favorite = result

                # Cocher la case si sélectionnée précédemment
                checkbox = self.findChild(QCheckBox, f"platform_{short}")
                if checkbox:
                    checkbox.setChecked(selected == 1)

                # Marquer comme favori si applicable
                fav_btn = self.findChild(QPushButton, f"fav_{short}")
                if fav_btn:
                    fav_btn.setChecked(is_favorite == 1)
            else:
                # Ajouter une nouvelle entrée si elle n'existe pas
                self.cursor.execute(
                    "INSERT INTO platform_prefs (platform, selected, is_favorite) VALUES (?, 0, 0)",
                    (platform,)
                )

        self.conn.commit()
        self.load_history()
        self.load_scheduled()

    def publish_now(self):
        """Publie immédiatement sur les plateformes sélectionnées"""

        # Récupérer les plateformes sélectionnées
        selected_platforms = []
        for platform, url, short in self.platforms_data:
            checkbox = self.findChild(QCheckBox, f"platform_{short}")
            if checkbox and checkbox.isChecked():
                selected_platforms.append((platform, url))

                # Sauvegarder la sélection
                self.cursor.execute(
                    "UPDATE platform_prefs SET selected = 1 WHERE platform = ?",
                    (platform,))

        if not selected_platforms:
            self.show_notification("Erreur", "Aucune plateforme sélectionnée")
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner au moins une plateforme.")
            return

        self.conn.commit()

        # Exécuter la publication dans un thread séparé
        threading.Thread(
            target=self.execute_publication,
            args=(selected_platforms,),
            daemon=True
        ).start()

        # Enregistrer dans l'historique
        self.save_to_history([p[0] for p in selected_platforms])

        # Confirmation
        self.show_notification("Succès", f"Publication sur {len(selected_platforms)} plateforme(s)")
        QMessageBox.information(
            self,
            "Publication en cours",
            f"Votre publication est en cours sur: {', '.join([p[0] for p in selected_platforms])}\n\n"
            "Les onglets vont s'ouvrir dans Chrome."
        )

        # Recharger les données
        self.load_history()

    def schedule_publication(self):
        """Planifie une publication pour plus tard"""

        # Récupérer les plateformes sélectionnées
        selected_platforms = []
        for platform, url, short in self.platforms_data:
            checkbox = self.findChild(QCheckBox, f"platform_{short}")
            if checkbox and checkbox.isChecked():
                selected_platforms.append((platform, url))

                # Sauvegarder la sélection
                self.cursor.execute(
                    "UPDATE platform_prefs SET selected = 1 WHERE platform = ?",
                    (platform,))

        if not selected_platforms:
            self.show_notification("Erreur", "Aucune plateforme sélectionnée")
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner au moins une plateforme.")
            return

        self.conn.commit()

        # Heure de planification
        scheduled_time = self.time_edit.time().toString("HH:mm")

        # Enregistrer la planification
        self.cursor.execute(
            "INSERT INTO scheduled_posts (platforms, scheduled_time) VALUES (?, ?)",
            (", ".join([p[0] for p in selected_platforms]), scheduled_time)
        )
        self.conn.commit()

        # Enregistrer dans l'historique comme planifié
        self.save_to_history(
            [p[0] for p in selected_platforms],
            scheduled=True,
            scheduled_time=scheduled_time
        )

        # Confirmation
        self.show_notification("Planifié", f"Publication prévue à {scheduled_time}")
        QMessageBox.information(
            self,
            "Publication planifiée",
            f"Votre publication est prévue à {scheduled_time} sur: {', '.join([p[0] for p in selected_platforms])}"
        )

        # Recharger les données
        self.load_history()
        self.load_scheduled()

        # Réinitialiser le formulaire
        self.schedule_check.setChecked(False)

    def execute_publication(self, platforms):
        """Exécute la publication sur les plateformes sélectionnées"""
        try:
            # Configurer Chrome comme navigateur
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(self.chrome_path))

            for platform, base_url in platforms:
                # Ouvrir dans Chrome avec un nouvel onglet
                webbrowser.get('chrome').open_new_tab(base_url)

                # Petite pause entre les ouvertures pour éviter le blocage
                import time
                time.sleep(1)
        except Exception as e:
            self.show_notification("Erreur", f"Problème lors de l'ouverture: {str(e)}")

    def save_to_history(self, platforms, scheduled=False, scheduled_time=None):
        """Enregistre dans l'historique"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute(
            "INSERT INTO publication_history (platforms, timestamp, scheduled, scheduled_time) "
            "VALUES (?, ?, ?, ?)",
            (", ".join(platforms), timestamp, 1 if scheduled else 0, scheduled_time)
        )
        self.conn.commit()

    def load_history(self):
        """Charge l'historique des publications"""
        self.history_list.clear()

        self.cursor.execute("""
            SELECT id, platforms, timestamp, scheduled, scheduled_time
            FROM publication_history
            ORDER BY timestamp DESC
            LIMIT 100
        """)

        for id, platforms, timestamp, scheduled, scheduled_time in self.cursor.fetchall():
            status = "🕒 Planifié" if scheduled else "✅ Publié"
            time_info = f"à {scheduled_time}" if scheduled else ""

            item_text = f"{status} {time_info} | {timestamp}\n"
            item_text += f"Plateformes: {platforms}"

            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, id)
            self.history_list.addItem(item)

    def load_scheduled(self):
        """Charge les publications planifiées"""
        self.scheduled_list.clear()

        self.cursor.execute("""
            SELECT id, platforms, scheduled_time
            FROM scheduled_posts
            WHERE executed = 0
            ORDER BY scheduled_time
        """)

        for id, platforms, scheduled_time in self.cursor.fetchall():
            item_text = f"🕒 {scheduled_time} | Plateformes: {platforms}"

            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, id)
            self.scheduled_list.addItem(item)

    def show_history_item(self, item):
        """Affiche les détails d'un élément de l'historique"""
        item_id = item.data(Qt.UserRole)

        self.cursor.execute("""
            SELECT platforms, timestamp, scheduled, scheduled_time
            FROM publication_history
            WHERE id = ?
        """, (item_id,))

        platforms, timestamp, scheduled, scheduled_time = self.cursor.fetchone()

        details = QMessageBox(self)
        details.setWindowTitle("Détails de la publication")
        details.setIcon(QMessageBox.Information)

        text = f"<b>Date:</b> {timestamp}<br>"
        if scheduled:
            text += f"<b>Planifié pour:</b> {scheduled_time}<br>"
        text += f"<b>Plateformes:</b> {platforms}"

        details.setText(text)
        details.exec_()

    def show_scheduled_item(self, item):
        """Affiche les détails d'une publication planifiée"""
        item_id = item.data(Qt.UserRole)

        self.cursor.execute("""
            SELECT platforms, scheduled_time
            FROM scheduled_posts
            WHERE id = ?
        """, (item_id,))

        platforms, scheduled_time = self.cursor.fetchone()

        details = QMessageBox(self)
        details.setWindowTitle("Détails de la planification")
        details.setIcon(QMessageBox.Information)

        text = f"<b>Planifié pour:</b> {scheduled_time}<br>"
        text += f"<b>Plateformes:</b> {platforms}"

        details.setText(text)
        details.exec_()

    def cancel_scheduled(self):
        """Annule une publication planifiée"""
        selected_items = self.scheduled_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner une planification à annuler.")
            return

        item = selected_items[0]
        item_id = item.data(Qt.UserRole)

        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Êtes-vous sûr de vouloir annuler cette planification?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Supprimer de la table des planifications
            self.cursor.execute("DELETE FROM scheduled_posts WHERE id = ?", (item_id,))

            # Mettre à jour l'historique
            self.cursor.execute("""
                UPDATE publication_history
                SET scheduled = 0, scheduled_time = NULL
                WHERE platforms = (SELECT platforms FROM scheduled_posts WHERE id = ?)
            """, (item_id,))

            self.conn.commit()

            self.show_notification("Annulé", "Publication planifiée annulée")
            self.load_history()
            self.load_scheduled()

    def clear_history(self):
        """Efface tout l'historique"""
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Êtes-vous sûr de vouloir effacer tout l'historique?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.cursor.execute("DELETE FROM publication_history")
            self.conn.commit()
            self.history_list.clear()
            self.show_notification("Historique", "Historique effacé")

    def check_scheduled_posts(self):
        """Vérifie et exécute les publications planifiées"""
        now = datetime.now().strftime("%H:%M")

        self.cursor.execute("""
            SELECT id, platforms
            FROM scheduled_posts
            WHERE executed = 0 AND scheduled_time <= ?
        """, (now,))

        for post_id, platforms in self.cursor.fetchall():
            platform_list = [(p.strip(), "") for p in platforms.split(",")]

            # Exécuter la publication dans un thread séparé
            threading.Thread(
                target=self.execute_publication,
                args=(platform_list,),
                daemon=True
            ).start()

            # Marquer comme exécuté
            self.cursor.execute(
                "UPDATE scheduled_posts SET executed = 1 WHERE id = ?",
                (post_id,)
            )

            # Mettre à jour l'historique
            self.cursor.execute("""
                UPDATE publication_history
                SET scheduled = 0
                WHERE platforms = ? AND scheduled = 1
            """, (platforms,))

            self.conn.commit()

            self.show_notification("Publication", f"Publication effectuée sur {platforms}")

        # Planifier la prochaine vérification dans 1 minute
        QTimer.singleShot(60000, self.check_scheduled_posts)

    def test_chrome(self):
        """Teste le chemin de Chrome"""
        path = self.chrome_path_edit.toPlainText().strip()

        try:
            webbrowser.register('chrome_test', None, webbrowser.BackgroundBrowser(path))
            webbrowser.get('chrome_test').open_new_tab('https://www.google.com')
            QMessageBox.information(self, "Succès", "Chrome a été ouvert avec succès!")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'ouvrir Chrome:\n{str(e)}")

    def save_settings(self):
        """Sauvegarde les paramètres"""
        self.chrome_path = self.chrome_path_edit.toPlainText().strip()
        self.settings.setValue("chrome_path", self.chrome_path)
        QMessageBox.information(self, "Succès", "Paramètres sauvegardés!")

    def closeEvent(self, event):
        """Gère la fermeture de la fenêtre"""
        if self.tray_icon.isVisible():
            self.show_notification("Ultimate Publisher", "L'application continue de fonctionner en arrière-plan")
            self.hide()
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Vérifier la disponibilité de la barre des tâches
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "Erreur", "Impossible d'accéder à la barre des tâches.")
        sys.exit(1)

    window = SocialMediaPublisher()
    window.show()
    sys.exit(app.exec_())
