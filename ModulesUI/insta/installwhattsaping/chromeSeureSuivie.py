# import os
# import sys
# import time
# import subprocess
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QTextEdit, QProgressBar
# )
# from PyQt5.QtCore import Qt, QTimer
# from PyQt5.QtGui import QIcon, QFont

# class FacebookLoginMonitor(QWidget):
#     def __init__(self):
#         super().__init__()
        
#         # Définir les chemins et variables
#         self.profile_number = 1
#         self.profile_path = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Profil {self.profile_number}\\Default"
#         self.log_file = "C:\\bon\\check_facebook_login_log.txt"
#         self.robot_exe_path = "C:\\chemin\\vers\\robot.exe"
#         self.cookie_file = os.path.join(self.profile_path, "Cookies")
#         self.attempts = 0
#         self.max_attempts = 60

#         # Configuration de la fenêtre principale
#         self.setWindowTitle("Surveillance de la Connexion Facebook")
#         self.setGeometry(680, 390, 600, 400)
#         self.setWindowIcon(QIcon("facebook_icon.png"))  # Icône personnalisée

#         # Mise en page principale
#         self.layout = QVBoxLayout()

#         # Ajout d'une police plus moderne et d'un titre
#         title_label = QLabel("Moniteur de Connexion Facebook", self)
#         title_label.setAlignment(Qt.AlignCenter)
#         title_label.setFont(QFont("Arial", 16, QFont.Bold))
#         self.layout.addWidget(title_label)

#         # Label d'information
#         self.info_label = QLabel(f"Vérification de la connexion Facebook pour le profil {self.profile_number}.", self)
#         self.info_label.setAlignment(Qt.AlignCenter)
#         self.layout.addWidget(self.info_label)

#         # Barre de progression pour le statut de la surveillance
#         self.progress_bar = QProgressBar(self)
#         self.progress_bar.setMaximum(self.max_attempts)
#         self.layout.addWidget(self.progress_bar)

#         # Affichage du log
#         self.log_text = QTextEdit(self)
#         self.log_text.setReadOnly(True)
#         self.layout.addWidget(self.log_text)

#         # Boutons pour démarrer et arrêter la surveillance
#         self.start_button = QPushButton("Démarrer la surveillance", self)
#         self.start_button.clicked.connect(self.start_monitoring)
#         self.layout.addWidget(self.start_button)

#         self.stop_button = QPushButton("Arrêter la surveillance", self)
#         self.stop_button.clicked.connect(self.stop_monitoring)
#         self.stop_button.setEnabled(False)  # Désactivé jusqu'au démarrage de la surveillance
#         self.layout.addWidget(self.stop_button)

#         # Appliquer la mise en page
#         self.setLayout(self.layout)

#     def write_to_log(self, message):
#         # Écrire dans la zone de texte et dans le fichier log
#         with open(self.log_file, 'a') as log:
#             log.write(message + "\n")
#         self.log_text.append(message)

#     def start_monitoring(self):
#         # Vérifier si le chemin du profil et des cookies existe avant de lancer Chrome
#         if not os.path.exists(self.profile_path):
#             self.write_to_log(f"[ERREUR] Le chemin du profil spécifié est introuvable : {self.profile_path}")
#             self.info_label.setText("Erreur : Le chemin du profil est introuvable.")
#             return

#         # Lancer Chrome avec le profil spécifié
#         chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
#         chrome_cmd = [chrome_path, f"--user-data-dir={self.profile_path}", "https://www.facebook.com"]
#         try:
#             subprocess.Popen(chrome_cmd)
#             self.write_to_log(f"[INFO] Démarrage de Google Chrome pour le profil {self.profile_number} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
#         except FileNotFoundError:
#             self.write_to_log(f"[ERREUR] Google Chrome introuvable au chemin : {chrome_path}")
#             self.info_label.setText("Erreur : Google Chrome introuvable.")
#             return

#         # Démarrer la surveillance du cookie
#         self.start_button.setEnabled(False)  # Désactiver le bouton de démarrage
#         self.stop_button.setEnabled(True)    # Activer le bouton d'arrêt
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.check_cookie)
#         self.timer.start(2000)  # Vérifier toutes les 2 secondes pour réduire la charge
#         self.progress_bar.setValue(0)

#     def check_cookie(self):
#         self.progress_bar.setValue(self.attempts)
#         if os.path.exists(self.cookie_file):
#             self.write_to_log(f"[INFO] Cookie Facebook détecté pour le profil {self.profile_number} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
#             self.info_label.setText("Cookie détecté ! Fermeture de Chrome et lancement de robot.exe.")
#             self.timer.stop()
#             self.stop_button.setEnabled(False)

#             # Fermer Chrome
#             subprocess.call(["taskkill", "/IM", "chrome.exe", "/F"])
#             self.write_to_log(f"[INFO] Fermeture de Google Chrome pour le profil {self.profile_number} - {time.strftime('%Y-%m-%d %H:%M:%S')}")

#             # Lancer robot.exe
#             try:
#                 subprocess.Popen([self.robot_exe_path])
#                 self.write_to_log(f"[INFO] Lancement de robot.exe après connexion à Facebook - {time.strftime('%Y-%m-%d %H:%M:%S')}")
#             except FileNotFoundError:
#                 self.write_to_log(f"[ERREUR] robot.exe introuvable au chemin : {self.robot_exe_path}")
#                 self.info_label.setText("Erreur : robot.exe introuvable.")

#         else:
#             self.attempts += 1
#             if self.attempts >= self.max_attempts:
#                 self.write_to_log(f"[ERREUR] Temps d'attente expiré. Le cookie n'a pas été trouvé.")
#                 self.info_label.setText("Temps d'attente expiré. Le cookie n'a pas été trouvé.")
#                 self.timer.stop()
#                 self.stop_button.setEnabled(False)

#     def stop_monitoring(self):
#         # Arrêter la surveillance et réinitialiser les états
#         self.write_to_log(f"[INFO] Surveillance arrêtée par l'utilisateur - {time.strftime('%Y-%m-%d %H:%M:%S')}")
#         self.info_label.setText("Surveillance arrêtée.")
#         self.timer.stop()
#         self.start_button.setEnabled(True)
#         self.stop_button.setEnabled(False)

# def main():
#     app = QApplication(sys.argv)

#     # Créer et afficher la fenêtre principale
#     window = FacebookLoginMonitor()
#     window.show()

#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()
import os
import time
import subprocess

def write_to_log(log_file, message):
    """Écrit les messages dans le fichier log."""
    with open(log_file, 'a') as log:
        log.write(message + "\n")
    print(message)

def check_cookie(profile_path, cookie_file, log_file, robot_exe_path, max_attempts=60):
    """Surveille la présence du fichier cookie pour vérifier la connexion Facebook."""
    attempts = 0
    while attempts < max_attempts:
        if os.path.exists(cookie_file):
            write_to_log(log_file, f"[INFO] Cookie Facebook détecté - {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Fermer Google Chrome
            subprocess.call(["taskkill", "/IM", "chrome.exe", "/F"])
            write_to_log(log_file, "[INFO] Fermeture de Google Chrome.")

            # Lancer robot.exe
            try:
                subprocess.Popen([robot_exe_path])
                write_to_log(log_file, "[INFO] Lancement de robot.exe après détection du cookie.")
            except FileNotFoundError:
                write_to_log(log_file, f"[ERREUR] robot.exe introuvable au chemin : {robot_exe_path}")
            break
        else:
            attempts += 1
            time.sleep(2)  # Pause de 2 secondes avant la prochaine vérification
    else:
        write_to_log(log_file, "[ERREUR] Temps d'attente expiré. Le cookie n'a pas été trouvé.")

def start_monitoring(profile_number=1):
    """Démarre la surveillance de la connexion Facebook."""
    user_name = os.getlogin()
    profile_path = f"C:\\Users\\{user_name}\\AppData\\Local\\Google\\Chrome\\User Data\\Profil {profile_number}\\Default"
    log_file = "C:\\bon\\check_facebook_login_log.txt"
    robot_exe_path = "C:\\chemin\\vers\\robot.exe"
    cookie_file = os.path.join(profile_path, "Cookies")

    # Vérifier si le chemin du profil existe
    if not os.path.exists(profile_path):
        write_to_log(log_file, f"[ERREUR] Le chemin du profil spécifié est introuvable : {profile_path}")
        return

    # Démarrer Chrome avec le profil spécifié
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_cmd = [chrome_path, f"--user-data-dir={profile_path}", "https://www.facebook.com"]
    try:
        subprocess.Popen(chrome_cmd)
        write_to_log(log_file, f"[INFO] Démarrage de Google Chrome pour le profil {profile_number} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
    except FileNotFoundError:
        write_to_log(log_file, f"[ERREUR] Google Chrome introuvable au chemin : {chrome_path}")
        return

    # Surveiller la présence du cookie Facebook
    check_cookie(profile_path, cookie_file, log_file, robot_exe_path)

if __name__ == "__main__":
    start_monitoring()
