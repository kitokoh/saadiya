import sys
import spacy
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget

# Charger le modèle NLP (utiliser "fr_core_news_sm" pour le français)
nlp = spacy.load("en_core_web_sm")

class AIAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assistant IA")
        self.setGeometry(100, 100, 600, 500)
        
        # Interface
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.layout.addWidget(self.chat_display)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Tapez une commande...")
        self.input_field.returnPressed.connect(self.process_command)
        self.layout.addWidget(self.input_field)
        
        self.send_button = QPushButton("Envoyer")
        self.send_button.clicked.connect(self.process_command)
        self.layout.addWidget(self.send_button)
        
        self.central_widget.setLayout(self.layout)
        
        # Commandes possibles
        self.commands = {
            "open settings": self.open_settings,
            "search client": self.search_client,
            "exit": self.close_app,
            "help": self.show_help
        }
    
    def process_command(self):
        user_input = self.input_field.text().strip()
        self.input_field.clear()
        
        if not user_input:
            return
        
        self.chat_display.append(f"Vous : {user_input}")
        command = self.analyze_command(user_input)
        
        if command in self.commands:
            response = self.commands[command]()
        else:
            response = "Commande non reconnue. Tapez 'help' pour voir la liste des commandes disponibles."
        
        self.chat_display.append(f"Assistant : {response}\n")
    
    def analyze_command(self, text):
        doc = nlp(text.lower())
        for token in doc:
            if "settings" in token.text:
                return "open settings"
            elif "client" in token.text:
                return "search client"
            elif "exit" in token.text or "quit" in token.text:
                return "exit"
            elif "help" in token.text:
                return "help"
        return "unknown"
    
    def open_settings(self):
        return "Ouverture des paramètres..."
    
    def search_client(self):
        return "Recherche d'un client..."
    
    def close_app(self):
        self.chat_display.append("Assistant : Fermeture de l'application...")
        QApplication.instance().quit()
        return ""
    
    def show_help(self):
        return "Commandes disponibles :\n- open settings : Ouvrir les paramètres\n- search client : Rechercher un client\n- exit : Quitter l'application\n- help : Afficher l'aide"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AIAssistant()
    window.show()
    sys.exit(app.exec())




