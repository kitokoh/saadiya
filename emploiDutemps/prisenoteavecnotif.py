import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                             QTextEdit, QPushButton, QLabel, QDateTimeEdit,
                             QHBoxLayout, QMessageBox)
from PyQt5.QtCore import QDateTime, QTimer, QUrl
from PyQt5.QtMultimedia import QSoundEffect
import os

class NoteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application de Notes avec Rappel")
        self.setGeometry(100, 100, 600, 400)
        
        # Initialisation de l'effet sonore
        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile(self.get_sound_path()))
        
        # Widget central et layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Zone de texte pour la note
        self.note_label = QLabel("Votre note:")
        self.note_edit = QTextEdit()
        
        # Sélecteur de date/heure
        self.datetime_label = QLabel("Programmer un rappel pour:")
        self.datetime_edit = QDateTimeEdit()
        self.datetime_edit.setDateTime(QDateTime.currentDateTime().addSecs(3600))  # 1 heure plus tard par défaut
        self.datetime_edit.setDisplayFormat("dd/MM/yyyy HH:mm:ss")
        
        # Boutons
        self.save_button = QPushButton("Enregistrer le rappel")
        self.save_button.clicked.connect(self.set_reminder)
        
        self.clear_button = QPushButton("Effacer")
        self.clear_button.clicked.connect(self.clear_note)
        
        # Layout horizontal pour les boutons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)
        
        # Ajout des widgets au layout principal
        layout.addWidget(self.note_label)
        layout.addWidget(self.note_edit)
        layout.addWidget(self.datetime_label)
        layout.addWidget(self.datetime_edit)
        layout.addLayout(button_layout)
        
        # Timer pour vérifier les rappels
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_reminders)
        self.timer.start(1000)  # Vérifie toutes les secondes
        
        # Liste des rappels
        self.reminders = []
        
    def get_sound_path(self):
        """Retourne le chemin vers un fichier sonore par défaut ou crée un fichier temporaire"""
        # Essaye de trouver un son système
        possible_paths = [
            "/usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga",
            "/usr/share/sounds/gnome/default/alerts/bark.ogg",
            "alarm.wav"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Si aucun son trouvé, crée un fichier temporaire (pour l'exemple)
        # En production, vous devriez inclure un fichier sonore avec votre application
        try:
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            temp_file.close()
            return temp_file.name
        except:
            return ""
    
    def set_reminder(self):
        """Enregistre la note avec son rappel"""
        note_text = self.note_edit.toPlainText()
        reminder_time = self.datetime_edit.dateTime()
        
        if not note_text.strip():
            QMessageBox.warning(self, "Attention", "La note ne peut pas être vide!")
            return
            
        if reminder_time <= QDateTime.currentDateTime():
            QMessageBox.warning(self, "Attention", "La date/heure du rappel doit être dans le futur!")
            return
            
        self.reminders.append({
            'text': note_text,
            'time': reminder_time,
            'triggered': False
        })
        
        QMessageBox.information(self, "Succès", 
                               f"Rappel enregistré pour {reminder_time.toString('dd/MM/yyyy HH:mm:ss')}")
        
    def check_reminders(self):
        """Vérifie si un rappel doit être déclenché"""
        current_time = QDateTime.currentDateTime()
        
        for reminder in self.reminders:
            if not reminder['triggered'] and current_time >= reminder['time']:
                self.trigger_reminder(reminder)
                reminder['triggered'] = True
    
    def trigger_reminder(self, reminder):
        """Déclenche le rappel avec notification sonore"""
        # Affiche la note
        QMessageBox.information(self, "Rappel!", reminder['text'])
        
        # Joue le son
        if self.sound_effect.source().isValid():
            self.sound_effect.play()
        
    def clear_note(self):
        """Efface la note actuelle"""
        self.note_edit.clear()
        
    def closeEvent(self, event):
        """Arrête le timer et le son lors de la fermeture"""
        self.timer.stop()
        self.sound_effect.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NoteApp()
    window.show()
    sys.exit(app.exec_())