import os
import subprocess
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QProgressBar
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont


class RobotExecutionApp(QWidget):
    def __init__(self):
        super().__init__()

        # Définir le chemin des robots
        self.robot_path = "C:\\bon"
        self.robots = []
        self.current_robot = 0
        self.max_robots = 0

        # Configuration de la fenêtre principale
        self.setWindowTitle("AI FB ROBOT PRO - Système et Exécution des Robots")
        self.setGeometry(680, 390, 600, 400)
        self.setWindowIcon(QIcon("robot_icon.png"))  # Icône personnalisée

        # Mise en page principale
        self.layout = QVBoxLayout()

        # Ajout d'une police plus moderne et d'un titre stylisé
        title_label = QLabel("AI FB ROBOT PRO", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.layout.addWidget(title_label)

        # Label pour l'état du système
        self.info_label = QLabel("Collecte des informations système...", self)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.info_label)

        # Affichage du log des actions
        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)
        self.layout.addWidget(self.log_text)

        # Barre de progression pour les robots
        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        # Boutons pour démarrer et arrêter l'exécution des robots
        self.start_button = QPushButton("Démarrer l'exécution des robots", self)
        self.start_button.clicked.connect(self.start_robot_execution)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Arrêter l'exécution", self)
        self.stop_button.clicked.connect(self.stop_robot_execution)
        self.stop_button.setEnabled(False)  # Désactivé tant que l'exécution n'est pas démarrée
        self.layout.addWidget(self.stop_button)

        # Appliquer la mise en page
        self.setLayout(self.layout)

        # Initialiser le timer pour exécuter les robots
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.execute_next_robot)

    def write_to_log(self, message):
        """Écrire des messages dans le log de l'interface et dans la console"""
        self.log_text.append(message)
        print(message)

    def detect_robots(self):
        """Détecter les dossiers de robots cachés dans le répertoire spécifié"""
        self.robots = []
        for root, dirs, _ in os.walk(self.robot_path):
            for dir_name in dirs:
                if dir_name.startswith("robot") and os.path.isdir(os.path.join(root, dir_name)):
                    self.robots.append(os.path.join(root, dir_name))
        self.max_robots = len(self.robots)
        self.progress_bar.setMaximum(self.max_robots)
        self.write_to_log(f"{self.max_robots} dossiers de robots trouvés.")

    def start_robot_execution(self):
        """Démarrer l'exécution des robots"""
        self.detect_robots()
        if self.max_robots == 0:
            self.write_to_log("Aucun dossier de robot trouvé. Exécution annulée.")
            return

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.info_label.setText("Exécution des robots en cours...")
        self.current_robot = 0
        self.timer.start(1000)  # Lancer un robot toutes les 1 seconde

    def stop_robot_execution(self):
        """Arrêter l'exécution des robots"""
        self.timer.stop()
        self.write_to_log("Exécution des robots arrêtée par l'utilisateur.")
        self.info_label.setText("Exécution arrêtée.")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def execute_next_robot(self):
        """Exécuter le prochain robot trouvé dans la liste"""
        if self.current_robot < self.max_robots:
            robot_dir = self.robots[self.current_robot]
            self.write_to_log(f"Lancement du robot {self.current_robot + 1} dans {robot_dir}...")

            # Simuler l'exécution du robot dans une nouvelle fenêtre
            env_dir = os.path.join(robot_dir, "env" + str(self.current_robot + 1), "Scripts")
            robot_script = os.path.join(robot_dir, "__post_in_groups__.py")
            
            if os.path.exists(robot_script):
                # Démarrer une nouvelle fenêtre cmd pour chaque robot
                subprocess.Popen(["cmd", "/c", f"""
                TITLE Robot {self.current_robot + 1} - AI FB ROBOT PRO
                ECHO Démarrage du robot {self.current_robot + 1}...
                cd /d {env_dir}
                call activate
                cd /d {robot_dir}
                python __post_in_groups__.py
                ECHO Robot {self.current_robot + 1} terminé.
                PAUSE
                """])
            else:
                self.write_to_log(f"[ERREUR] Script introuvable pour le robot {self.current_robot + 1}")

            self.current_robot += 1
            self.progress_bar.setValue(self.current_robot)

        if self.current_robot >= self.max_robots:
            self.timer.stop()
            self.write_to_log("Tous les robots ont été exécutés.")
            self.info_label.setText("Exécution terminée.")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)


def main():
    app = QApplication(sys.argv)

    # Créer et afficher la fenêtre principale
    window = RobotExecutionApp()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
