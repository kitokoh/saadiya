import sys
import sqlite3
import os
from datetime import datetime
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QTextEdit, QPushButton, QSlider, QCheckBox, 
                            QMessageBox, QDialog, QDialogButtonBox)
from PyQt5.QtCore import Qt, QStandardPaths, QSize
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import tempfile
from textblob import TextBlob

class StarRatingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 50)
        self._rating = 0
        self._max_rating = 5
        self._star_size = QSize(30, 30)
        self._star_color = QColor(255, 215, 0)  # Gold color
        
    def setRating(self, rating):
        self._rating = rating
        self.update()
        
    def rating(self):
        return self._rating
        
    def sizeHint(self):
        return QSize(self._max_rating * self._star_size.width(), self._star_size.height())
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        for i in range(self._max_rating):
            if i < self._rating:
                painter.setBrush(self._star_color)
                painter.setPen(self._star_color)
            else:
                painter.setBrush(Qt.NoBrush)
                painter.setPen(QColor(200, 200, 200))
                
            star_points = [
                QPointF(10 + i * 30 + 15, 5),
                QPointF(10 + i * 30 + 20, 20),
                QPointF(10 + i * 30 + 35, 20),
                QPointF(10 + i * 30 + 22, 30),
                QPointF(10 + i * 30 + 28, 45),
                QPointF(10 + i * 30 + 15, 35),
                QPointF(10 + i * 30 + 2, 45),
                QPointF(10 + i * 30 + 8, 30),
                QPointF(10 + i * 30 - 5, 20),
                QPointF(10 + i * 30 + 10, 20)
            ]
            painter.drawPolygon(star_points)
            
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.pos().x()
            new_rating = min(self._max_rating, max(1, (x // self._star_size.width()) + 1))
            self.setRating(new_rating)
            self.ratingChanged.emit(new_rating)

class FeedbackDatabase:
    def __init__(self):
        db_path = self.get_db_path()
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def get_db_path(self):
        data_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        Path(data_dir).mkdir(parents=True, exist_ok=True)
        return os.path.join(data_dir, 'feedback.db')

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rating INTEGER,
            comment TEXT,
            screenshot_path TEXT,
            sentiment REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        self.conn.commit()

    def save_feedback(self, rating, comment, screenshot_path=None):
        sentiment = TextBlob(comment).sentiment.polarity if comment else 0.0
        
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO feedback (rating, comment, screenshot_path, sentiment)
        VALUES (?, ?, ?, ?)
        ''', (rating, comment, screenshot_path, sentiment))
        self.conn.commit()
        return cursor.lastrowid

    def get_all_feedback(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM feedback ORDER BY timestamp DESC')
        return cursor.fetchall()

    def __del__(self):
        self.conn.close()

class FeedbackDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Envoyer un Feedback")
        self.setMinimumSize(500, 400)
        self.db = FeedbackDatabase()
        self._screenshot_path = None
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Titre
        title_label = QLabel("Partagez votre expérience avec nous")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Note
        layout.addWidget(QLabel("Notez votre expérience:"))
        
        self.rating_slider = QSlider(Qt.Horizontal)
        self.rating_slider.setMinimum(1)
        self.rating_slider.setMaximum(5)
        self.rating_slider.setValue(3)
        self.rating_slider.setTickPosition(QSlider.TicksBelow)
        self.rating_slider.setTickInterval(1)
        layout.addWidget(self.rating_slider)
        
        # Widget d'étoiles
        self.star_rating = StarRatingWidget()
        self.star_rating.setRating(3)
        self.rating_slider.valueChanged.connect(self.star_rating.setRating)
        layout.addWidget(self.star_rating, 0, Qt.AlignHCenter)
        
        # Commentaire
        layout.addWidget(QLabel("Vos commentaires:"))
        self.comment_edit = QTextEdit()
        self.comment_edit.setPlaceholderText("Dites-nous ce que vous avez aimé ou ce qui pourrait être amélioré...")
        layout.addWidget(self.comment_edit)
        
        # Options
        options_layout = QHBoxLayout()
        
        self.screenshot_btn = QPushButton("Ajouter une capture d'écran")
        self.screenshot_btn.setIcon(QIcon.fromTheme("camera-photo"))
        self.screenshot_btn.clicked.connect(self.capture_screenshot)
        options_layout.addWidget(self.screenshot_btn)
        
        self.email_check = QCheckBox("Envoyer par email")
        options_layout.addWidget(self.email_check)
        
        layout.addLayout(options_layout)
        
        # Boutons
        btn_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        submit_btn = QPushButton("Envoyer")
        submit_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        submit_btn.clicked.connect(self.submit_feedback)
        btn_layout.addWidget(submit_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def capture_screenshot(self):
        # En production, vous implémenteriez la capture d'écran ici
        # Pour cet exemple, nous allons simplement utiliser une image de test
        reply = QMessageBox.question(
            self, 
            "Capture d'écran", 
            "Voulez-vous capturer une partie de votre écran maintenant?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Simuler la capture d'écran
                temp_dir = tempfile.gettempdir()
                self._screenshot_path = os.path.join(temp_dir, "feedback_screenshot.png")
                
                # Créer une image de test
                pixmap = QPixmap(400, 300)
                pixmap.fill(Qt.white)
                painter = QPainter(pixmap)
                painter.drawText(100, 150, "Exemple de capture d'écran")
                painter.end()
                pixmap.save(self._screenshot_path)
                
                QMessageBox.information(
                    self, 
                    "Capture réussie", 
                    f"Capture enregistrée dans: {self._screenshot_path}"
                )
            except Exception as e:
                QMessageBox.warning(
                    self, 
                    "Erreur", 
                    f"Impossible de capturer l'écran: {str(e)}"
                )
    
    def submit_feedback(self):
        rating = self.rating_slider.value()
        comment = self.comment_edit.toPlainText()
        
        if not comment.strip():
            QMessageBox.warning(self, "Commentaire vide", "Veuillez saisir un commentaire avant de soumettre.")
            return
        
        try:
            # Sauvegarder dans la base de données
            feedback_id = self.db.save_feedback(rating, comment, self._screenshot_path)
            
            # Envoyer par email si demandé
            if self.email_check.isChecked():
                self.send_email(rating, comment, feedback_id)
            
            QMessageBox.information(
                self, 
                "Merci!", 
                "Votre feedback a été enregistré avec succès. Merci pour votre contribution!"
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Erreur", 
                f"Une erreur est survenue lors de l'enregistrement: {str(e)}"
            )
    
    def send_email(self, rating, comment, feedback_id):
        try:
            # Configuration email (à remplacer par vos paramètres)
            smtp_server = "smtp.example.com"
            smtp_port = 587
            username = "your_email@example.com"
            password = "yourpassword"
            recipient = "feedback@example.com"
            
            msg = MIMEMultipart()
            msg['From'] = username
            msg['To'] = recipient
            msg['Subject'] = f"Nouveau feedback (#{feedback_id}) - Note: {rating}/5"
            
            body = f"""
            Nouveau feedback reçu:
            
            Note: {rating}/5
            Commentaire: {comment}
            
            Feedback ID: {feedback_id}
            Date: {datetime.now()}
            """
            msg.attach(MIMEText(body, 'plain'))
            
            if self._screenshot_path and os.path.exists(self._screenshot_path):
                with open(self._screenshot_path, 'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-Disposition', 'attachment', filename='screenshot.png')
                    msg.attach(img)
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
                
        except Exception as e:
            QMessageBox.warning(
                self, 
                "Email non envoyé", 
                f"Le feedback a été enregistré mais l'email n'a pas pu être envoyé: {str(e)}"
            )

class FeedbackApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Collecteur de Feedback")
        self.setMinimumSize(600, 500)
        
        self.setup_ui()
        self.show_feedback_stats()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Bouton pour ouvrir le dialogue de feedback
        self.feedback_btn = QPushButton("Donner votre feedback")
        self.feedback_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.feedback_btn.clicked.connect(self.open_feedback_dialog)
        layout.addWidget(self.feedback_btn, 0, Qt.AlignCenter)
        
        # Statistiques
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.stats_label)
        
        # Liste des feedbacks
        self.feedback_list = QTextEdit()
        self.feedback_list.setReadOnly(True)
        layout.addWidget(self.feedback_list)
        
        # Bouton pour rafraîchir
        refresh_btn = QPushButton("Rafraîchir")
        refresh_btn.clicked.connect(self.show_feedback_stats)
        layout.addWidget(refresh_btn)
    
    def open_feedback_dialog(self):
        dialog = FeedbackDialog(self)
        dialog.exec_()
        self.show_feedback_stats()
    
    def show_feedback_stats(self):
        db = FeedbackDatabase()
        feedbacks = db.get_all_feedback()
        
        if not feedbacks:
            self.stats_label.setText("Aucun feedback enregistré pour le moment.")
            self.feedback_list.clear()
            return
        
        total = len(feedbacks)
        avg_rating = sum(f[1] for f in feedbacks) / total
        positive = sum(1 for f in feedbacks if f[4] > 0.2)
        neutral = sum(1 for f in feedbacks if -0.2 <= f[4] <= 0.2)
        negative = sum(1 for f in feedbacks if  -0.2 < f[4] )



        self.stats_label.setText(
            f"Statistiques: {total} feedbacks | Moyenne: {avg_rating:.1f}/5 | "
            f"Positifs: {positive} | Neutres: {neutral} | Négatifs: {negative}"
        )
        
        # Afficher les derniers feedbacks
        self.feedback_list.clear()
        self.feedback_list.append("Derniers feedbacks reçus:\n")
        
        for fb in feedbacks[:10]:  # Afficher les 10 derniers
            stars = "★" * fb[1] + "☆" * (5 - fb[1])
            sentiment = "😊 Positif" if fb[4] > 0.2 else "😐 Neutre" if fb[4] >= -0.2 else "😞 Négatif"
            self.feedback_list.append(
                f"[{fb[5]}] {stars}\n"
                f"Commentaire: {fb[2]}\n"
                f"Sentiment: {sentiment}\n"
                f"{'-'*40}\n"
            )

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Feedback Collector")
    app.setOrganizationName("MyCompany")
    app.setStyle("Fusion")  # Style moderne
    
    # Palette de couleurs pour un look moderne
    palette = app.palette()
    palette.setColor(palette.Window, QColor(240, 240, 240))
    palette.setColor(palette.WindowText, QColor(50, 50, 50))
    palette.setColor(palette.Highlight, QColor(100, 149, 237))  # Cornflower blue
    palette.setColor(palette.HighlightedText, Qt.white)
    app.setPalette(palette)
    
    window = FeedbackApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
