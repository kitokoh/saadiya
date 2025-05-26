import os
import sys
import shutil
import requests
import zipfile
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                            QVBoxLayout, QWidget, QMessageBox, QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sqlite3

class DownloadThread(QThread):
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, github_url, target_dir):
        super().__init__()
        self.github_url = github_url
        self.target_dir = target_dir
        self.db_file = "copy_log.db"
        
    def run(self):
        try:
            # Vérifier/Créer le dossier cible
            if not os.path.exists(self.target_dir):
                try:
                    os.makedirs(self.target_dir)
                except PermissionError:
                    self.finished.emit(False, "Permission denied to create target directory")
                    return
            
            # Télécharger la release depuis GitHub
            self.progress_updated.emit(10)
            
            # Ici vous devriez utiliser l'API GitHub pour récupérer la dernière release
            # Pour cet exemple, je suppose qu'il y a un zip avec le dossier sourccode
            release_url = f"{self.github_url}/releases/latest/download/sourccode.zip"
            
            temp_zip = os.path.join(self.target_dir, "temp_release.zip")
            
            try:
                response = requests.get(release_url, stream=True)
                response.raise_for_status()
                
                with open(temp_zip, 'wb') as f:
                    total_length = int(response.headers.get('content-length', 0))
                    if total_length == 0:
                        f.write(response.content)
                    else:
                        downloaded = 0
                        for data in response.iter_content(chunk_size=4096):
                            downloaded += len(data)
                            f.write(data)
                            progress = 10 + int((downloaded / total_length) * 80)
                            self.progress_updated.emit(progress)
            except Exception as e:
                self.finished.emit(False, f"Download failed: {str(e)}")
                return
            
            self.progress_updated.emit(90)
            
            # Extraire le zip
            try:
                with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
                    zip_ref.extractall(self.target_dir)
            except Exception as e:
                self.finished.emit(False, f"Extraction failed: {str(e)}")
                return
            
            # Supprimer le zip temporaire
            try:
                os.remove(temp_zip)
            except:
                pass
            
            self.progress_updated.emit(95)
            
            # Enregistrer dans la base de données
            self.log_execution(success=True)
            
            self.progress_updated.emit(100)
            self.finished.emit(True, "Operation completed successfully")
            
        except Exception as e:
            self.log_execution(success=False, error_msg=str(e))
            self.finished.emit(False, f"An error occurred: {str(e)}")
    
    def log_execution(self, success, error_msg=""):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Créer la table si elle n'existe pas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS copy_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            execution_date TEXT NOT NULL,
            success INTEGER NOT NULL,
            error_msg TEXT,
            source_url TEXT NOT NULL,
            target_dir TEXT NOT NULL
        )
        ''')
        
        # Insérer le log
        cursor.execute('''
        INSERT INTO copy_log (execution_date, success, error_msg, source_url, target_dir)
        VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), int(success), error_msg, self.github_url, self.target_dir))
        
        conn.commit()
        conn.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.github_url = "https://github.com/kitokoh/mining"
        self.target_dir = r"C:\eneim"
        
        self.initUI()
        self.init_db()
        
    def initUI(self):
        self.setWindowTitle("GitHub Release Copier")
        self.setGeometry(100, 100, 400, 200)
        
        layout = QVBoxLayout()
        
        self.info_label = QLabel(
            f"Cette application va copier le dossier 'sourccode' depuis\n"
            f"les releases de {self.github_url}\n"
            f"vers {self.target_dir}"
        )
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        self.start_button = QPushButton("Commencer la copie")
        self.start_button.clicked.connect(self.start_copy)
        layout.addWidget(self.start_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    def init_db(self):
        db_file = "copy_log.db"
        if not os.path.exists(db_file):
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS copy_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                execution_date TEXT NOT NULL,
                success INTEGER NOT NULL,
                error_msg TEXT,
                source_url TEXT NOT NULL,
                target_dir TEXT NOT NULL
            )
            ''')
            conn.commit()
            conn.close()
    
    def start_copy(self):
        self.start_button.setEnabled(False)
        self.progress_bar.setValue(0)
        
        self.thread = DownloadThread(self.github_url, self.target_dir)
        self.thread.progress_updated.connect(self.update_progress)
        self.thread.finished.connect(self.operation_finished)
        self.thread.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def operation_finished(self, success, message):
        self.start_button.setEnabled(True)
        
        msg = QMessageBox(self)
        if success:
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Succès")
        else:
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Erreur")
        
        msg.setText(message)
        msg.exec_()
        
        if not success and "Permission" in message:
            self.request_admin_rights()
    
    def request_admin_rights(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Permissions requises")
        msg.setText("L'application a besoin de permissions élevées pour effectuer cette opération. Voulez-vous redémarrer avec des permissions administrateur?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        if msg.exec_() == QMessageBox.Yes:
            # Essayez de redémarrer avec les droits admin
            try:
                import ctypes
                if not ctypes.windll.shell32.IsUserAnAdmin():
                    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                    sys.exit()
            except:
                QMessageBox.warning(self, "Erreur", "Impossible d'obtenir les droits administrateur")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Vérifier si le programme a les droits nécessaires
    try:
        test_dir = r"C:\eneim"
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
    except PermissionError:
        # Demander les droits admin
        try:
            import ctypes
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()
        except:
            pass
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())