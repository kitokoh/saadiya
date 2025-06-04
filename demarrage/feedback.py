import sys
import sqlite3
import os
from datetime import datetime
from pathlib import Path
from typing import Dict
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt, QStandardPaths
from PyQt5.QtGui import QIcon
from demarrage.baseDialog import BaseDialog
from imports import DB_PATH_demarrage
class FeedbackDialog(BaseDialog):
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Titre
        self.label = QLabel("Comment évaluez-vous votre expérience jusqu'à présent?")
        layout.addWidget(self.label)
        
        # Boutons de notation
        self.rating = 0
        self.rating_btns = []
        btn_layout = QHBoxLayout()
        
        for i in range(1, 6):
            btn = QPushButton(str(i))
            btn.setFixedSize(40, 40)
            btn.clicked.connect(lambda _, r=i: self.set_rating(r))
            self.rating_btns.append(btn)
            btn_layout.addWidget(btn)
        
        layout.addLayout(btn_layout)
        
        # Champ de commentaire
        self.feedback_input = QLineEdit()
        self.feedback_input.setPlaceholderText("Vos commentaires (optionnel)")
        layout.addWidget(self.feedback_input)
        
        # Bouton d'envoi
        self.submit_btn = QPushButton("Envoyer")
        self.submit_btn.clicked.connect(self.accept)
        layout.addWidget(self.submit_btn)
        
        self.setLayout(layout)
    
    def set_rating(self, rating: int):
        """Définir la note et mettre à jour l'apparence des boutons"""
        self.rating = rating
        for i, btn in enumerate(self.rating_btns):
            btn.setStyleSheet(
                "background-color: #4CAF50; color: white;" if i < rating else ""
            )
    
    def get_results(self) -> Dict:
        """Récupérer les résultats sous forme de dictionnaire"""
        return {
            'rating': self.rating,
            'feedback': self.feedback_input.text().strip()
        }

class FeedbackDatabase:
    def __init__(self):
        db_path = self.get_db_path()
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def get_db_path(self):
        # data_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        # Path(data_dir).mkdir(parents=True, exist_ok=True)
        # return os.path.join(data_dir, 'feedback.db')
        return DB_PATH_demarrage

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rating INTEGER,
            comment TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        self.conn.commit()

    def save_feedback(self, rating: int, comment: str):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO feedback (rating, comment)
        VALUES (?, ?)
        ''', (rating, comment))
        self.conn.commit()
        return cursor.lastrowid

    def get_all_feedback(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM feedback ORDER BY timestamp DESC')
        return cursor.fetchall()

    def __del__(self):
        self.conn.close()

class FeedbackApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Collecteur de Feedback")
        self.setMinimumSize(400, 300)
        
        self.db = FeedbackDatabase()
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
        
        # Bouton pour rafraîchir
        refresh_btn = QPushButton("Rafraîchir les statistiques")
        refresh_btn.clicked.connect(self.show_feedback_stats)
        layout.addWidget(refresh_btn)
    
    def open_feedback_dialog(self):
        dialog = FeedbackDialog(self)
        if dialog.exec_() == QWidget.Accepted:
            results = dialog.get_results()
            try:
                self.db.save_feedback(results['rating'], results['feedback'])
                QMessageBox.information(self, "Merci!", "Votre feedback a été enregistré.")
                self.show_feedback_stats()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible d'enregistrer: {str(e)}")
    
    def show_feedback_stats(self):
        feedbacks = self.db.get_all_feedback()
        
        if not feedbacks:
            self.stats_label.setText("Aucun feedback enregistré pour le moment.")
            return
        
        total = len(feedbacks)
        avg_rating = sum(f[1] for f in feedbacks) / total
        
        self.stats_label.setText(
            f"Statistiques: {total} feedbacks | Moyenne: {avg_rating:.1f}/5"
        )
