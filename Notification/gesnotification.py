import sys
import os
import sqlite3
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, 
                            QLineEdit, QTimeEdit, QPushButton, QColorDialog, QFileDialog, QListWidget,
                            QMessageBox, QFrame, QScrollArea, QComboBox, QCheckBox, QStackedWidget,
                            QSystemTrayIcon, QMenu, QStyle, QInputDialog)
from PyQt5.QtCore import QTimer, Qt, QTime, QUrl, QSize, QDateTime
from PyQt5.QtGui import QColor, QPalette, QFont, QIcon, QPixmap, QPainter, QBrush
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QListWidgetItem


class NotificationDB:
    """Classe pour gérer la base de données des notifications"""
    def __init__(self):
        self.conn = sqlite3.connect('notifications.db')
        self.create_table()
        
    def create_table(self):
        """Crée la table des notifications si elle n'existe pas"""
        query = """
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            trigger_time TEXT NOT NULL,
            color TEXT NOT NULL,
            sound_file TEXT,
            condition_text TEXT,
            repeat_mode TEXT,
            days_of_week TEXT,
            enabled INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.conn.execute(query)
        self.conn.commit()
        
    def add_notification(self, notification):
        """Ajoute une nouvelle notification à la base de données"""
        query = """
        INSERT INTO notifications 
        (message, trigger_time, color, sound_file, condition_text, repeat_mode, days_of_week)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.conn.execute(query, (
            notification['message'],
            notification['trigger_time'].toString("HH:mm"),
            notification['color'].name(),
            notification['sound_file'],
            notification['condition_text'],
            notification['repeat_mode'],
            notification['days_of_week']
        ))
        self.conn.commit()
        return self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        
    def get_all_notifications(self):
        """Récupère toutes les notifications de la base de données"""
        cursor = self.conn.execute("""
        SELECT id, message, trigger_time, color, sound_file, condition_text, 
               repeat_mode, days_of_week, enabled 
        FROM notifications
        ORDER BY trigger_time
        """)
        return cursor.fetchall()
        
    def update_notification(self, notification_id, data):
        """Met à jour une notification existante"""
        query = """
        UPDATE notifications 
        SET message=?, trigger_time=?, color=?, sound_file=?, condition_text=?,
            repeat_mode=?, days_of_week=?, enabled=?
        WHERE id=?
        """
        self.conn.execute(query, (
            data['message'],
            data['trigger_time'].toString("HH:mm"),
            data['color'].name(),
            data['sound_file'],
            data['condition_text'],
            data['repeat_mode'],
            data['days_of_week'],
            data['enabled'],
            notification_id
        ))
        self.conn.commit()
        
    def delete_notification(self, notification_id):
        """Supprime une notification"""
        self.conn.execute("DELETE FROM notifications WHERE id=?", (notification_id,))
        self.conn.commit()
        
    def close(self):
        """Ferme la connexion à la base de données"""
        self.conn.close()


class NotificationManager:
    """Classe pour gérer la logique des notifications"""
    def __init__(self, db, sound_player):
        self.db = db
        self.sound_player = sound_player
        self.active_notifications = {}
        
    def load_notifications(self):
        """Charge toutes les notifications depuis la base de données"""
        notifications = self.db.get_all_notifications()
        self.active_notifications = {}
        
        for notif in notifications:
            notif_id, message, trigger_time, color, sound_file, condition_text, \
            repeat_mode, days_of_week, enabled = notif
            
            time = QTime.fromString(trigger_time, "HH:mm")
            color_obj = QColor(color)
            
            self.active_notifications[notif_id] = {
                'id': notif_id,
                'message': message,
                'trigger_time': time,
                'color': color_obj,
                'sound_file': sound_file,
                'condition_text': condition_text,
                'repeat_mode': repeat_mode,
                'days_of_week': days_of_week,
                'enabled': enabled,
                'last_triggered': None
            }
            
    def check_notifications(self):
        """Vérifie si des notifications doivent être déclenchées"""
        current_time = QTime.currentTime()
        current_date = QDateTime.currentDateTime()
        
        for notif_id, notif in self.active_notifications.items():
            if not notif['enabled']:
                continue
                
            # Vérifier l'heure
            time_ok = (current_time.hour() == notif['trigger_time'].hour() and 
                       current_time.minute() == notif['trigger_time'].minute())
            
            if not time_ok:
                continue
                
            # Vérifier la répétition
            if notif['repeat_mode'] == 'daily':
                pass  # Tous les jours, pas de condition supplémentaire
            elif notif['repeat_mode'] == 'weekly':
                current_day = current_date.toString("dddd").lower()
                if notif['days_of_week'] and current_day not in notif['days_of_week'].split(','):
                    continue
            elif notif['last_triggered'] and notif['last_triggered'].date() == current_date.date():
                continue  # Déjà déclenchée aujourd'hui
                
            # Vérifier la condition personnalisée
            condition_ok = True
            if notif['condition_text']:
                try:
                    condition_ok = eval(notif['condition_text'])
                except Exception as e:
                    print(f"Erreur dans la condition: {e}")
                    condition_ok = False
                    
            if condition_ok:
                self.trigger_notification(notif)
                notif['last_triggered'] = current_date
                
    def trigger_notification(self, notification):
        """Déclenche une notification"""
        # Jouer le son
        if notification['sound_file'] and os.path.exists(notification['sound_file']):
            self.sound_player.play(notification['sound_file'])
            
        # Retourner les données de la notification
        return {
            'message': notification['message'],
            'color': notification['color'],
            'sound_file': notification['sound_file']
        }


class SoundPlayer:
    """Classe pour gérer la lecture des sons"""
    def __init__(self):
        self.sound_effect = QSoundEffect()
        self.sound_effect.setVolume(0.7)
        
    def play(self, sound_file):
        """Joue un fichier son"""
        self.sound_effect.setSource(QUrl.fromLocalFile(sound_file))
        self.sound_effect.play()


class NotificationToast(QFrame):
    """Widget personnalisé pour les notifications toast"""
    def __init__(self, message, color, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            NotificationToast {
                border: 1px solid #444;
                border-radius: 8px;
                background-color: rgba(40, 40, 40, 220);
            }
            QLabel {
                color: white;
                padding: 8px;
            }
        """)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Créer un widget pour la barre de couleur
        color_bar = QWidget()
        color_bar.setFixedHeight(5)
        color_bar.setStyleSheet(f"background-color: {color.name()}; border-radius: 2px;")
        layout.addWidget(color_bar)
        
        # Ajouter le message
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setFont(QFont("Arial", 10))
        layout.addWidget(message_label)
        
        # Animation de disparition
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fade_out)
        self.opacity = 1.0
        self.setWindowOpacity(self.opacity)
        
    def showEvent(self, event):
        """Démarre le timer quand la notification est affichée"""
        super().showEvent(event)
        self.timer.start(3000)  # Disparaît après 3 secondes
        
    def fade_out(self):
        """Animation de fondu pour disparaître"""
        self.opacity -= 0.05
        self.setWindowOpacity(self.opacity)
        
        if self.opacity <= 0:
            self.timer.stop()
            self.close()


class NotificationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Notification Manager")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(600, 500)
        
        # Configuration du style
        self.setup_style()
        
        # Initialiser les composants
        self.db = NotificationDB()
        self.sound_player = SoundPlayer()
        self.notification_manager = NotificationManager(self.db, self.sound_player)
        
        # Icône de la barre des tâches
        self.setup_tray_icon()
        
        # Initialiser l'interface
        self.init_ui()
        
        # Charger les notifications
        self.notification_manager.load_notifications()
        self.update_notification_list()
        
        # Timer pour vérifier les notifications
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_notifications)
        self.check_timer.start(1000)  # Vérifie toutes les secondes
        
    def setup_style(self):
        """Configure le style de l'application"""
        # Palette de couleurs moderne
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(45, 45, 48))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.AlternateBase, QColor(45, 45, 48))
        palette.setColor(QPalette.ToolTipBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(63, 63, 70))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Highlight, QColor(0, 122, 204))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        self.setPalette(palette)
        
        # Style CSS supplémentaire
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2d2d2d;
            }
            QPushButton {
                background-color: #3e3e42;
                border: 1px solid #3e3e42;
                border-radius: 4px;
                padding: 5px 10px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #4e4e52;
                border: 1px solid #4e4e52;
            }
            QPushButton:pressed {
                background-color: #2e2e32;
            }
            QPushButton:disabled {
                background-color: #2d2d30;
                color: #6d6d70;
            }
            QLineEdit, QTimeEdit, QComboBox {
                background-color: #252526;
                border: 1px solid #3e3e42;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget {
                background-color: #252526;
                border: 1px solid #3e3e42;
                border-radius: 4px;
                padding: 5px;
            }
            QLabel {
                color: #ffffff;
            }
            QFrame {
                background-color: #2d2d2d;
            }
            QTabWidget::pane {
                border: 1px solid #3e3e42;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: white;
                padding: 8px;
                border: 1px solid #3e3e42;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #1e1e1e;
                border-bottom: 1px solid #1e1e1e;
            }
        """)
        
    def setup_tray_icon(self):
        """Configure l'icône de la barre des tâches"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))
        
        tray_menu = QMenu()
        show_action = tray_menu.addAction("Ouvrir")
        show_action.triggered.connect(self.show)
        quit_action = tray_menu.addAction("Quitter")
        quit_action.triggered.connect(self.close_app)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
    def tray_icon_activated(self, reason):
        """Gère les clics sur l'icône de la barre des tâches"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            
    def close_app(self):
        """Ferme proprement l'application"""
        self.db.close()
        QApplication.quit()
        
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)
        
        # Titre de l'application
        title = QLabel("Advanced Notification Manager")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #569cd6;")
        main_layout.addWidget(title)
        
        # Onglets
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Onglet "Nouvelle notification"
        self.setup_new_notification_tab()
        
        # Onglet "Notifications programmées"
        self.setup_scheduled_notifications_tab()
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
    def setup_new_notification_tab(self):
        """Configure l'onglet pour créer de nouvelles notifications"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Message
        msg_group = QFrame()
        msg_group.setFrameShape(QFrame.StyledPanel)
        msg_layout = QVBoxLayout()
        msg_layout.setContentsMargins(10, 10, 10, 10)
        
        msg_label = QLabel("Message de notification:")
        msg_label.setFont(QFont("Segoe UI", 10))
        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Entrez le message à afficher...")
        
        msg_layout.addWidget(msg_label)
        msg_layout.addWidget(self.msg_input)
        msg_group.setLayout(msg_layout)
        layout.addWidget(msg_group)
        
        # Heure et répétition
        time_group = QFrame()
        time_group.setFrameShape(QFrame.StyledPanel)
        time_layout = QVBoxLayout()
        time_layout.setContentsMargins(10, 10, 10, 10)
        
        # Heure de déclenchement
        time_label = QLabel("Heure de déclenchement:")
        time_label.setFont(QFont("Segoe UI", 10))
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime.currentTime().addSecs(300))  # Défaut: maintenant + 5 min
        
        # Mode de répétition
        repeat_label = QLabel("Répétition:")
        repeat_label.setFont(QFont("Segoe UI", 10))
        self.repeat_combo = QComboBox()
        self.repeat_combo.addItems(["Une seule fois", "Quotidienne", "Hebdomadaire"])
        self.repeat_combo.currentIndexChanged.connect(self.update_repeat_options)
        
        # Jours de la semaine (masqué par défaut)
        self.days_group = QWidget()
        days_layout = QHBoxLayout()
        days_layout.setContentsMargins(0, 0, 0, 0)
        self.day_buttons = {}
        
        for i, day in enumerate(["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]):
            btn = QCheckBox(day)
            if i < 5:  # Sélectionner les jours de semaine par défaut
                btn.setChecked(True)
            self.day_buttons[day] = btn
            days_layout.addWidget(btn)
            
        self.days_group.setLayout(days_layout)
        self.days_group.hide()
        
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_edit)
        time_layout.addWidget(repeat_label)
        time_layout.addWidget(self.repeat_combo)
        time_layout.addWidget(self.days_group)
        time_group.setLayout(time_layout)
        layout.addWidget(time_group)
        
        # Personnalisation
        custom_group = QFrame()
        custom_group.setFrameShape(QFrame.StyledPanel)
        custom_layout = QVBoxLayout()
        custom_layout.setContentsMargins(10, 10, 10, 10)
        
        # Couleur
        color_label = QLabel("Couleur de la notification:")
        color_label.setFont(QFont("Segoe UI", 10))
        
        self.color_btn = QPushButton()
        self.current_color = QColor(0, 122, 204)  # Bleu moderne
        self.update_color_button()
        self.color_btn.clicked.connect(self.choose_color)
        
        # Son
        sound_label = QLabel("Son de notification:")
        sound_label.setFont(QFont("Segoe UI", 10))
        
        sound_btn_layout = QHBoxLayout()
        self.sound_btn = QPushButton("Choisir un son")
        self.sound_btn.clicked.connect(self.choose_sound)
        
        self.play_sound_btn = QPushButton()
        self.play_sound_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_sound_btn.setToolTip("Prévisualiser le son")
        self.play_sound_btn.setFixedSize(30, 30)
        self.play_sound_btn.clicked.connect(self.preview_sound)
        
        sound_btn_layout.addWidget(self.sound_btn)
        sound_btn_layout.addWidget(self.play_sound_btn)
        sound_btn_layout.addStretch()
        
        # Condition personnalisée
        condition_label = QLabel("Condition personnalisée (optionnel):")
        condition_label.setFont(QFont("Segoe UI", 10))
        self.condition_input = QLineEdit()
        self.condition_input.setPlaceholderText("Ex: datetime.now().weekday() < 5 # Seulement en semaine")
        
        custom_layout.addWidget(color_label)
        custom_layout.addWidget(self.color_btn)
        custom_layout.addWidget(sound_label)
        custom_layout.addLayout(sound_btn_layout)
        custom_layout.addWidget(condition_label)
        custom_layout.addWidget(self.condition_input)
        custom_group.setLayout(custom_layout)
        layout.addWidget(custom_group)
        
        # Bouton d'ajout
        self.add_btn = QPushButton("Programmer la notification")
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.add_btn.clicked.connect(self.schedule_notification)
        layout.addWidget(self.add_btn)
        
        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Nouvelle notification")
        
    def setup_scheduled_notifications_tab(self):
        """Configure l'onglet pour afficher et gérer les notifications programmées"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Liste des notifications
        self.notification_list = QListWidget()
        self.notification_list.setSelectionMode(QListWidget.SingleSelection)
        self.notification_list.itemDoubleClicked.connect(self.edit_notification)
        layout.addWidget(self.notification_list)
        
        # Boutons d'action
        btn_layout = QHBoxLayout()
        
        self.edit_btn = QPushButton("Modifier")
        self.edit_btn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        self.edit_btn.clicked.connect(self.edit_notification)
        self.edit_btn.setEnabled(False)
        
        self.toggle_btn = QPushButton("Activer/Désactiver")
        self.toggle_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogYesButton))
        self.toggle_btn.clicked.connect(self.toggle_notification)
        self.toggle_btn.setEnabled(False)
        
        self.remove_btn = QPushButton("Supprimer")
        self.remove_btn.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        self.remove_btn.clicked.connect(self.remove_notification)
        self.remove_btn.setEnabled(False)
        
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.toggle_btn)
        btn_layout.addWidget(self.remove_btn)
        layout.addLayout(btn_layout)
        
        # Connecter la sélection de la liste
        self.notification_list.itemSelectionChanged.connect(self.update_button_states)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Notifications programmées")
        
    def update_repeat_options(self):
        """Affiche ou masque les options de jours selon le mode de répétition"""
        mode = self.repeat_combo.currentText()
        if mode == "Hebdomadaire":
            self.days_group.show()
        else:
            self.days_group.hide()
            
    def update_color_button(self):
        """Met à jour l'apparence du bouton de couleur"""
        pixmap = QPixmap(32, 32)
        pixmap.fill(self.current_color)
        self.color_btn.setIcon(QIcon(pixmap))
        self.color_btn.setText(self.current_color.name())
        
    def choose_color(self):
        """Ouvre le dialogue de choix de couleur"""
        color = QColorDialog.getColor(self.current_color, self, "Choisir une couleur")
        if color.isValid():
            self.current_color = color
            self.update_color_button()
            
    def choose_sound(self):
        """Ouvre le dialogue de choix de fichier son"""
        file, _ = QFileDialog.getOpenFileName(
            self, 
            "Choisir un fichier son", 
            "", 
            "Fichiers audio (*.wav *.mp3);;Tous les fichiers (*)"
        )
        if file:
            self.sound_file = file
            self.sound_btn.setText(os.path.basename(file))
            
    def preview_sound(self):
        """Prévisualise le son sélectionné"""
        if hasattr(self, 'sound_file') and os.path.exists(self.sound_file):
            self.sound_player.play(self.sound_file)
            
    def schedule_notification(self):
        """Programme une nouvelle notification"""
        message = self.msg_input.text().strip()
        if not message:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un message pour la notification.")
            return
            
        # Préparer les données de la notification
        notification = {
            'message': message,
            'trigger_time': self.time_edit.time(),
            'color': self.current_color,
            'sound_file': getattr(self, 'sound_file', ''),
            'condition_text': self.condition_input.text().strip(),
            'repeat_mode': self.get_repeat_mode(),
            'days_of_week': self.get_selected_days(),
            'enabled': True
        }
        
        # Ajouter à la base de données
        notif_id = self.db.add_notification(notification)
        
        # Recharger les notifications
        self.notification_manager.load_notifications()
        self.update_notification_list()
        
        # Réinitialiser le formulaire
        self.msg_input.clear()
        self.time_edit.setTime(QTime.currentTime().addSecs(300))
        self.condition_input.clear()
        
        # Afficher un message de confirmation
        QMessageBox.information(
            self, 
            "Succès", 
            f"Notification programmée avec succès (ID: {notif_id})"
        )
        
    def get_repeat_mode(self):
        """Retourne le mode de répétition sous forme de chaîne"""
        mode = self.repeat_combo.currentText()
        if mode == "Une seule fois":
            return "once"
        elif mode == "Quotidienne":
            return "daily"
        elif mode == "Hebdomadaire":
            return "weekly"
        return "once"
        
    def get_selected_days(self):
        """Retourne les jours sélectionnés sous forme de chaîne séparée par des virgules"""
        if self.repeat_combo.currentText() != "Hebdomadaire":
            return ""
            
        selected_days = []
        for day, btn in self.day_buttons.items():
            if btn.isChecked():
                selected_days.append(day.lower()[:3])  # "lun", "mar", etc.
                
        return ",".join(selected_days)
        
    def update_notification_list(self):
        """Met à jour la liste des notifications programmées"""
        self.notification_list.clear()
        notifications = self.notification_manager.active_notifications.values()
        
        for notif in sorted(notifications, key=lambda x: x['trigger_time'].toString("HH:mm")):
            item_text = self.format_notification_text(notif)
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, notif['id'])
            
            # Désactiver visuellement les notifications désactivées
            if not notif['enabled']:
                item.setForeground(QColor(150, 150, 150))
                
            self.notification_list.addItem(item)
            
    def format_notification_text(self, notif):
        """Formatte le texte d'une notification pour l'affichage dans la liste"""
        time_str = notif['trigger_time'].toString("HH:mm")
        enabled_str = "✓" if notif['enabled'] else "✗"
        
        # Mode de répétition
        if notif['repeat_mode'] == 'once':
            repeat_str = "Une fois"
        elif notif['repeat_mode'] == 'daily':
            repeat_str = "Quotidienne"
        elif notif['repeat_mode'] == 'weekly':
            days = notif['days_of_week'].split(',') if notif['days_of_week'] else []
            if len(days) == 7:
                repeat_str = "Tous les jours"
            elif len(days) == 5 and all(d in days for d in ['lun', 'mar', 'mer', 'jeu', 'ven']):
                repeat_str = "Semaine (L-V)"
            else:
                repeat_str = "Hebdo (" + ",".join(days) + ")"
        else:
            repeat_str = "Inconnu"
            
        # Condition
        condition_str = " + condition" if notif['condition_text'] else ""
        
        return f"[{enabled_str}] {time_str} - {notif['message']} ({repeat_str}{condition_str})"
        
    def update_button_states(self):
        """Active ou désactive les boutons selon la sélection"""
        has_selection = len(self.notification_list.selectedItems()) > 0
        self.edit_btn.setEnabled(has_selection)
        self.toggle_btn.setEnabled(has_selection)
        self.remove_btn.setEnabled(has_selection)
        
    def edit_notification(self):
        """Ouvre l'éditeur pour la notification sélectionnée"""
        selected = self.notification_list.currentItem()
        if not selected:
            return
            
        notif_id = selected.data(Qt.UserRole)
        notif = self.notification_manager.active_notifications.get(notif_id)
        if not notif:
            return
            
        # Créer une boîte de dialogue d'édition
        dialog = QDialog(self)
        dialog.setWindowTitle("Modifier la notification")
        dialog.setMinimumWidth(400)
        layout = QVBoxLayout()
        
        # Message
        msg_label = QLabel("Message:")
        msg_edit = QLineEdit(notif['message'])
        layout.addWidget(msg_label)
        layout.addWidget(msg_edit)
        
        # Heure
        time_label = QLabel("Heure:")
        time_edit = QTimeEdit(notif['trigger_time'])
        time_edit.setDisplayFormat("HH:mm")
        layout.addWidget(time_label)
        layout.addWidget(time_edit)
        
        # Répétition
        repeat_label = QLabel("Répétition:")
        repeat_combo = QComboBox()
        repeat_combo.addItems(["Une seule fois", "Quotidienne", "Hebdomadaire"])
        
        if notif['repeat_mode'] == 'daily':
            repeat_combo.setCurrentIndex(1)
        elif notif['repeat_mode'] == 'weekly':
            repeat_combo.setCurrentIndex(2)
            
        layout.addWidget(repeat_label)
        layout.addWidget(repeat_combo)
        
        # Couleur
        color_label = QLabel("Couleur:")
        color_btn = QPushButton()
        color = notif['color']
        pixmap = QPixmap(32, 32)
        pixmap.fill(color)
        color_btn.setIcon(QIcon(pixmap))
        color_btn.setText(color.name())
        color_btn.clicked.connect(lambda: self.choose_color_for_edit(dialog, color_btn))
        layout.addWidget(color_label)
        layout.addWidget(color_btn)
        
        # Boutons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Enregistrer")
        save_btn.clicked.connect(lambda: self.save_notification_changes(
            dialog, notif_id, msg_edit.text(), time_edit.time(), 
            color, repeat_combo.currentText(), notif['condition_text']
        ))
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(dialog.reject)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()
        
    def choose_color_for_edit(self, dialog, btn):
        """Ouvre le sélecteur de couleur dans l'éditeur"""
        color = QColorDialog.getColor(QColor(btn.text()), dialog)
        if color.isValid():
            pixmap = QPixmap(32, 32)
            pixmap.fill(color)
            btn.setIcon(QIcon(pixmap))
            btn.setText(color.name())
            
    def save_notification_changes(self, dialog, notif_id, message, time, color, repeat_mode, condition):
        """Enregistre les modifications d'une notification"""
        if not message.strip():
            QMessageBox.warning(dialog, "Erreur", "Le message ne peut pas être vide.")
            return
            
        # Préparer les données mises à jour
        updated_data = {
            'message': message,
            'trigger_time': time,
            'color': color,
            'sound_file': self.notification_manager.active_notifications[notif_id]['sound_file'],
            'condition_text': condition,
            'repeat_mode': self.get_repeat_mode_from_text(repeat_mode),
            'days_of_week': self.notification_manager.active_notifications[notif_id]['days_of_week'],
            'enabled': self.notification_manager.active_notifications[notif_id]['enabled']
        }
        
        # Mettre à jour dans la base de données
        self.db.update_notification(notif_id, updated_data)
        
        # Recharger les notifications
        self.notification_manager.load_notifications()
        self.update_notification_list()
        
        dialog.accept()
        
    def get_repeat_mode_from_text(self, text):
        """Convertit le texte du combo en mode de répétition"""
        if text == "Une seule fois":
            return "once"
        elif text == "Quotidienne":
            return "daily"
        elif text == "Hebdomadaire":
            return "weekly"
        return "once"
        
    def toggle_notification(self):
        """Active ou désactive une notification"""
        selected = self.notification_list.currentItem()
        if not selected:
            return
            
        notif_id = selected.data(Qt.UserRole)
        notif = self.notification_manager.active_notifications.get(notif_id)
        if not notif:
            return
            
        # Inverser l'état
        new_state = not notif['enabled']
        
        # Mettre à jour dans la base de données
        self.db.update_notification(notif_id, {
            'message': notif['message'],
            'trigger_time': notif['trigger_time'],
            'color': notif['color'],
            'sound_file': notif['sound_file'],
            'condition_text': notif['condition_text'],
            'repeat_mode': notif['repeat_mode'],
            'days_of_week': notif['days_of_week'],
            'enabled': new_state
        })
        
        # Recharger les notifications
        self.notification_manager.load_notifications()
        self.update_notification_list()
        
    def remove_notification(self):
        """Supprime la notification sélectionnée"""
        selected = self.notification_list.currentItem()
        if not selected:
            return
            
        notif_id = selected.data(Qt.UserRole)
        
        # Confirmation
        reply = QMessageBox.question(
            self, 
            "Confirmation", 
            "Voulez-vous vraiment supprimer cette notification?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Supprimer de la base de données
            self.db.delete_notification(notif_id)
            
            # Recharger les notifications
            self.notification_manager.load_notifications()
            self.update_notification_list()
            
    def check_notifications(self):
        """Vérifie et déclenche les notifications"""
        self.notification_manager.check_notifications()
        
        # Vérifier si des notifications ont été déclenchées
        for notif_id, notif in self.notification_manager.active_notifications.items():
            if notif.get('triggered'):
                self.show_notification(notif)
                notif['triggered'] = False  # Réinitialiser pour la prochaine fois
                
    def show_notification(self, notification):
        """Affiche une notification à l'utilisateur"""
        # Afficher une notification toast
        toast = NotificationToast(
            notification['message'],
            notification['color'],
            self
        )
        
        # Positionner la notification en bas à droite
        screen_geo = QApplication.desktop().availableGeometry()
        toast.move(
            screen_geo.right() - toast.width() - 20,
            screen_geo.bottom() - toast.height() - 20
        )
        
        toast.show()
        
        # Afficher également un message système
        self.tray_icon.showMessage(
            "Notification",
            notification['message'],
            QSystemTrayIcon.Information,
            3000  # Durée en ms
        )
        
    def closeEvent(self, event):
        """Gère la fermeture de la fenêtre"""
        # Minimiser dans la barre des tâches au lieu de fermer
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Définir une police moderne par défaut
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = NotificationApp()
    window.show()
    sys.exit(app.exec_())