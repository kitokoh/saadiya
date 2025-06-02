import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QSystemTrayIcon, QMenu, 
                             QVBoxLayout, QLabel, QTextEdit, QPushButton, 
                             QHBoxLayout, QMessageBox)
from PyQt5.QtGui import QIcon, QPixmap, QCursor, QColor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QSize, QPoint, QTimer, QPropertyAnimation, pyqtProperty
from PyQt5.QtWebEngineWidgets import QWebEngineView  # Pour intégrer Dialogflow (optionnel)
from imports import DB_PATH_Home
# --- CONSTANTES ---
WHATSAPP_NUMBER = "+123456789"  # Remplacez par votre numéro
SUPPORT_EMAIL = "support@example.com"
APP_NAME = "Virtual Assistant"

# --- BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect(DB_PATH_Home)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_text TEXT,
            bot_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# --- BULLE FLOTTANTE PERSONNALISÉE ---
class FloatingBubble(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(60, 60)
        
        # Position initiale (coin inférieur droit)
        screen_geometry = QApplication.desktop().screenGeometry()
        self.move(screen_geometry.width() - 70, screen_geometry.height() - 70)
        
        # Animation de pulsation
        self.pulse_animation = QPropertyAnimation(self, b"size")
        self.pulse_animation.setDuration(1000)
        self.pulse_animation.setLoopCount(-1)
        self.pulse_animation.setKeyValueAt(0, QSize(60, 60))
        self.pulse_animation.setKeyValueAt(0.5, QSize(65, 65))
        self.pulse_animation.setKeyValueAt(1, QSize(60, 60))
        self.pulse_animation.start()
        
        self.drag_pos = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Cercle avec dégradé
        gradient = QBrush(QColor(110, 72, 170))  # Violet
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())
        
        # Icône chatbot
        icon = QIcon.fromTheme("help-contents").pixmap(30, 30)
        painter.drawPixmap(15, 15, icon)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.drag_pos:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None

# --- FENÊTRE DE CHAT ---
class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assistant Virtuel")
        self.setFixedSize(350, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F7FA;
                font-family: 'Arial';
            }
            QTextEdit {
                border: 1px solid #E2E8F0;
                border-radius: 10px;
                padding: 8px;
                background-color: white;
            }
            QPushButton {
                background-color: #6E48AA;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #8A63C7;
            }
        """)
        
        self.init_ui()
        self.load_chat_history()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # En-tête
        header = QHBoxLayout()
        self.bot_icon = QLabel()
        self.bot_icon.setPixmap(QPixmap("bot_icon.png").scaled(40, 40))  # Remplacez par votre icône
        header.addWidget(self.bot_icon)
        
        self.bot_name = QLabel("Helper AI • En ligne")
        self.bot_name.setStyleSheet("font-weight: bold; color: #2D3748;")
        header.addWidget(self.bot_name)
        header.addStretch()
        
        layout.addLayout(header)
        
        # Zone de chat
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)
        
        # Champ de saisie
        self.user_input = QTextEdit()
        self.user_input.setMaximumHeight(60)
        self.user_input.setPlaceholderText("Tapez votre message...")
        layout.addWidget(self.user_input)
        
        # Boutons
        button_layout = QHBoxLayout()
        self.send_button = QPushButton("Envoyer")
        self.send_button.clicked.connect(self.send_message)
        button_layout.addWidget(self.send_button)
        
        self.quick_reply = QPushButton("Options rapides")
        self.quick_reply.clicked.connect(self.show_quick_replies)
        button_layout.addWidget(self.quick_reply)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def send_message(self):
        user_text = self.user_input.toPlainText().strip()
        if user_text:
            self.display_message(user_text, is_user=True)
            self.user_input.clear()
            
            # Simuler une réponse du bot (remplacez par Dialogflow/Rasa)
            QTimer.singleShot(1000, lambda: self.bot_response(user_text))
    
    def bot_response(self, user_text):
        # Réponses pré-définies (à remplacer par une API IA)
        responses = {
            "bonjour": "Bonjour ! Comment puis-je vous aider aujourd'hui ?",
            "aide": "Je peux vous aider avec:\n1. Problèmes techniques\n2. Questions de facturation\n3. Guide d'utilisation",
            "merci": "Avec plaisir ! 😊"
        }
        
        reply = responses.get(user_text.lower(), 
                            "Désolé, je n'ai pas compris. Tapez 'aide' pour les options.")
        
        self.display_message(reply, is_user=False)
        self.save_to_db(user_text, reply)
    
    def display_message(self, text, is_user):
        alignment = "right" if is_user else "left"
        color = "#6E48AA" if is_user else "#E2E8F0"
        
        self.chat_display.append(f"""
        <div style='text-align: {alignment}; margin: 5px;'>
            <div style='background: {color}; 
                        color: {'white' if is_user else 'black'};
                        border-radius: 10px; 
                        padding: 8px; 
                        display: inline-block;
                        max-width: 80%;'>
                {text}
            </div>
        </div>
        """)
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum())
    
    def show_quick_replies(self):
        menu = QMenu()
        options = [
            ("Problème technique", "Mon compte ne fonctionne pas"),
            ("Question facturation", "Où trouver ma facture ?"),
            ("Guide", "Comment utiliser l'application ?")
        ]
        
        for text, reply in options:
            action = menu.addAction(text)
            action.triggered.connect(lambda _, r=reply: self.user_input.setPlainText(r))
        
        menu.exec_(QCursor.pos())
    
    def save_to_db(self, user_text, bot_reply):
        conn = sqlite3.connect(DB_PATH_Home)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chats (user_text, bot_response) VALUES (?, ?)", 
                      (user_text, bot_reply))
        conn.commit()
        conn.close()
    
    def load_chat_history(self):
        conn = sqlite3.connect(DB_PATH_Home)
        cursor = conn.cursor()
        cursor.execute("SELECT user_text, bot_response FROM chats ORDER BY timestamp LIMIT 50")
        chats = cursor.fetchall()
        conn.close()
        
        for user_text, bot_reply in chats:
            self.display_message(user_text, is_user=True)
            self.display_message(bot_reply, is_user=False)

# --- APPLICATION PRINCIPALE ---
class VirtualAssistantApp(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.setQuitOnLastWindowClosed(False)
        init_db()
        
        # Bulle flottante
        self.bubble = FloatingBubble()
        self.bubble.show()
        
        # Fenêtre de chat (cachée au départ)
        self.chat_window = ChatWindow()
        
        # Menu contextuel
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(QIcon("icon.png"))  # Remplacez par votre icône
        
        self.context_menu = QMenu()
        self.setup_context_menu()
        
        # Premier démarrage
        if self.is_first_run():
            self.show_welcome_message()
    
    def setup_context_menu(self):
        # Actions
        chat_action = self.context_menu.addAction("Discuter avec l'assistant")
        chat_action.triggered.connect(self.chat_window.show)
        
        whatsapp_action = self.context_menu.addAction("Contacter via WhatsApp")
        whatsapp_action.triggered.connect(self.open_whatsapp)
        
        email_action = self.context_menu.addAction("Envoyer un Email")
        email_action.triggered.connect(self.send_email)
        
        quit_action = self.context_menu.addAction("Quitter")
        quit_action.triggered.connect(self.quit)
        
        # Associer le menu à la bulle
        self.bubble.setContextMenuPolicy(Qt.CustomContextMenu)
        self.bubble.customContextMenuRequested.connect(self.show_context_menu)
    
    def show_context_menu(self):
        self.context_menu.exec_(QCursor.pos())
    
    def open_whatsapp(self):
        import webbrowser
        webbrowser.open(f"https://wa.me/{WHATSAPP_NUMBER}?text=Bonjour,%20j'ai%20besoin%20d'aide%20sur%20{APP_NAME}")
    
    def send_email(self):
        import webbrowser
        subject = f"Support {APP_NAME}"
        body = "Bonjour,\n\nJe contacte à propos de : [Décrivez ici votre demande].\n\nCordialement,"
        webbrowser.open(f"mailto:{SUPPORT_EMAIL}?subject={subject}&body={body}")
    
    def is_first_run(self):
        conn = sqlite3.connect(DB_PATH_Home)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM chats")
        count = cursor.fetchone()[0]
        conn.close()
        return count == 0
    
    def show_welcome_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Bienvenue !")
        msg.setText("Avez-vous besoin d'aide pour commencer ?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        if msg.exec_() == QMessageBox.Yes:
            self.chat_window.show()
            self.chat_window.display_message(
                "Bienvenue ! Posez-moi vos questions ou tapez 'aide' pour les options.", 
                is_user=False)

# --- LANCEMENT ---
if __name__ == "__main__":
    app = VirtualAssistantApp(sys.argv)
    sys.exit(app.exec_())