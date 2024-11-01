# import os
# import sys
# import subprocess
# from PyQt5 import QtWidgets, QtCore, QtGui

# class InstallerApp(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Facebook Robot Pro - Installation Automatique")
#         self.setGeometry(600, 300, 600, 400)
#         self.setWindowIcon(QtGui.QIcon("../resources/frpro-Open.ico"))  # Remplacez par votre icône

#         self.layout = QtWidgets.QVBoxLayout(self)

#         # Titre et sous-titre
#         self.title_label = QtWidgets.QLabel("Installation Automatique")
#         self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498db;")
#         self.layout.addWidget(self.title_label)

#         self.subtitle_label = QtWidgets.QLabel("Préparez votre environnement pour Facebook Robot Pro")
#         self.subtitle_label.setStyleSheet("font-size: 16px; color: gray;")
#         self.layout.addWidget(self.subtitle_label)

#         self.label = QtWidgets.QLabel("Cliquez sur 'Installer' pour commencer l'installation.")
#         self.layout.addWidget(self.label)

#         self.start_button = QtWidgets.QPushButton("Installer")
#         self.start_button.clicked.connect(self.start_installation)
#         self.layout.addWidget(self.start_button)

#         self.output_area = QtWidgets.QTextBrowser()  # Utilisation de QTextBrowser pour le journal
#         self.output_area.setOpenExternalLinks(True)  # Permet d'ouvrir les liens
#         self.layout.addWidget(self.output_area)

#         # Progress bar with initial style
#         self.progress_bar = QtWidgets.QProgressBar(self)
#         self.progress_bar.setRange(0, 100)
#         self.progress_bar.setStyleSheet("""
#             QProgressBar {
#                 border: 2px solid #555;
#                 border-radius: 5px;
#                 background-color: #E0E0E0;
#                 text-align: center;
#                 font-family: Arial;
#             }
#             QProgressBar::chunk {
#                 background-color: #3498db;  /* Blue for start */
#                 width: 20px;
#             }
#         """)
#         self.layout.addWidget(self.progress_bar)

#         # Adding loading animation (lazy loader)
#         self.loading_gif = QtGui.QMovie("loading.gif")
#         self.loading_label = QtWidgets.QLabel(self)
#         self.loading_label.setMovie(self.loading_gif)
#         self.loading_label.setVisible(False)  # Hidden initially
#         self.layout.addWidget(self.loading_label)

#         self.log_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "journalInstallation.txt")
#         self.create_log_file()

#         self.setStyleSheet("""
#             background-color: #f9f9f9;
#             color: #333;
#             font-family: Arial, sans-serif;
#         """)
#         self.update_install_button()


#     def create_log_file(self):
#         with open(self.log_file_path, "a") as log_file:
#             log_file.write("-- Journal d'installation --\n")
#             log_file.write(f"{QtCore.QDate.currentDate().toString()} {QtCore.QTime.currentTime().toString()}: Démarrage de l'installation\n")

#     def log(self, message):
#         with open(self.log_file_path, "a") as log_file:
#             log_file.write(message + "\n")
#         self.output_area.append(f"<b>{message}</b>")

#     def start_installation(self):
#          # Change the button text when installation starts
#         self.start_button.setText("Installation en cours...")
#         self.start_button.setEnabled(False)  # Disable the button to prevent multiple clicks

#         # Proceed with installation logic here...
#         self.output_area.clear()
#         self.log("Démarrage de l'installation...")

       

#         self.loading_label.setVisible(True)  # Show loading animation
#         self.progress_bar.setValue(0)
#         self.progress_bar.setStyleSheet("""
#             QProgressBar::chunk {
#                 background-color: #3498db;  /* Blue during GitHub clone */
#             }
#         """)

#         if not self.check_internet_connection():
#             return

#         self.log("Vérification et installation de Git...")
#         self.install_git()

#         self.progress_bar.setValue(30)  # Update progress bar after Git installation

#         self.log("Vérification et installation de Python...")
#         self.install_python()

#         self.progress_bar.setValue(50)  # Update progress bar after Python installation

#         self.handle_instance_installation()

#         self.progress_bar.setValue(100)
#         self.loading_label.setVisible(False)  # Hide loading animation
#         self.log("Installation terminée. Vous pouvez fermer la fenêtre.")
#         self.start_button.setEnabled(True)  # Re-enable the button after installation

#         QtCore.QTimer.singleShot(10000, self.close)  # Close the window automatically after 3 seconds
        
       

#     def check_internet_connection(self):
#         try:
#             subprocess.check_call(["ping", "google.com", "-n", "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             self.log("Connexion Internet vérifiée.")
#             return True
#         except subprocess.CalledProcessError:
#             self.log("Aucune connexion Internet. Veuillez vérifier votre connexion.")
#             return False

#     def install_git(self):
#         if self.run_command("git --version"):
#             git_version = self.run_command("git --version").strip()
#             self.log(f"Git déjà installé: {git_version}")
#         else:
#             self.log("Git non trouvé. Installation...")
#             if os.path.exists("Git-2.42.0-64-bit.exe"):
#                 self.run_command('start /wait "Git-2.42.0-64-bit.exe" /SILENT /VERYSILENT /NORESTART')
#                 self.log("Git installé.")
#             else:
#                 self.log("Installeur Git non trouvé.")

#     def install_python(self):
#         if self.run_command("python --version"):
#             python_version = self.run_command("python --version").strip()
#             self.log(f"Python déjà installé: {python_version}")
#         else:
#             self.log("Python non trouvé. Installation...")
#             if os.path.exists("python-3.11.5-amd64.exe"):
#                 self.run_command('start /wait "python-3.11.5-amd64.exe" /quiet InstallAllUsers=1 PrependPath=1')
#                 self.log("Python installé.")
#             else:
#                 self.log("Installeur Python non trouvé.")

  

#     def run_command(self, command):
#         try:
#             result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode().strip()
#             return result
#         except subprocess.CalledProcessError as e:
#             self.log(f"Erreur lors de l'exécution de la commande: {e.output.decode().strip()}")
#             return None
#     def handle_instance_installation(self):
#         folder_path_robot1 = "C:\\bon\\robot1"
#         folder_path_robot2 = "C:\\bon\\robot2"

#         # Si robot1 et robot2 existent déjà, demande combien d'instances l'utilisateur souhaite installer
#         if os.path.exists(folder_path_robot1) and os.path.exists(folder_path_robot2):
#             self.log("Instances 1 et 2 déjà installées.")
#             num_instances, ok = QtWidgets.QInputDialog.getInt(
#                 self, "Nombre d'instances", 
#                 "Combien d'instances souhaitez-vous installer (supérieur à 2) ?", 
#                 3, 3, 100, 1)

#             if ok and num_instances > 2:
#                 for i in range(3, num_instances + 1):
#                     self.install_instance(i)
#             else:
#                 self.log("Installation annulée. L'utilisateur n'a pas saisi de nombre valide.")
        
#         # Si seule l'instance 1 existe
#         elif os.path.exists(folder_path_robot1):
#             self.log("Instance 1 déjà installée.")
#             install_instance_2 = QtWidgets.QMessageBox.question(
#                 self, "Installer une nouvelle instance ?", 
#                 "Robot1 est déjà installé. Voulez-vous installer l'instance 2 ?", 
#                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

#             if install_instance_2 == QtWidgets.QMessageBox.Yes:
#                 self.install_instance(2)
#             else:
#                 self.log("Installation annulée par l'utilisateur.")
        
#         # Si aucune instance n'existe, installer la première instance
#         else:
#             self.log("Installation de l'instance de démo (Robot1)...")
#             self.install_instance(1)

#     def install_instance(self, instance_number):
#         folder_path = f"C:\\bon\\robot{instance_number}"
#         if not os.path.exists(folder_path):
#             os.makedirs(folder_path, exist_ok=True)
#             self.log(f"Création du dossier pour l'instance {instance_number}...")

#             # Clonage du dépôt GitHub
#             self.log(f"Clonage du dépôt GitHub pour l'instance {instance_number}...")
#             self.progress_bar.setValue(10 * instance_number)  # Mise à jour de la barre de progression
#             self.run_command(f'git clone https://github.com/kitokoh/facebook-group-bot.git {folder_path}')

#             # Création d'un environnement virtuel
#             self.log(f"Création de l'environnement virtuel pour robot{instance_number}...")
#             self.run_command(f"python -m venv {folder_path}\\env{instance_number}")
#             self.progress_bar.setValue(20 * instance_number)  # Mise à jour de la barre de progression

#             # Installation des dépendances
#             self.log(f"Installation des dépendances pour robot{instance_number}...")
#             self.run_command(f"{folder_path}\\env{instance_number}\\Scripts\\activate && pip install -r {folder_path}\\requirements.txt")
#             self.progress_bar.setValue(30 * instance_number)  # Mise à jour de la barre de progression

#             self.log(f"Installation terminée pour l'instance {instance_number}.")
#         else:
#             self.log(f"L'instance {instance_number} existe déjà. Aucune action nécessaire.")

#     def update_install_button(self):
#         folder_path_robot1 = "C:\\bon\\robot1"
#         folder_path_robot2 = "C:\\bon\\robot2"
        
#         if os.path.exists(folder_path_robot1) and os.path.exists(folder_path_robot2):
#             self.start_button.setText("Installer une autre instance")
#         elif os.path.exists(folder_path_robot1):
#             self.start_button.setText("Installer instance 2")
#         else:
#             self.start_button.setText("Installer démo")

# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     window = InstallerApp()
#     window.show()
#     sys.exit(app.exec_())


# if __name__ == "__main__":
#     main()

# import os
# import subprocess

# def log(message):
#     print(message)

# def check_internet_connection():
#     try:
#         subprocess.check_call(["ping", "google.com", "-n", "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         log("Connexion Internet vérifiée.")
#         return True
#     except subprocess.CalledProcessError:
#         log("Aucune connexion Internet. Veuillez vérifier votre connexion.")
#         return False

# def run_command(command):
#     try:
#         result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode().strip()
#         return result
#     except subprocess.CalledProcessError as e:
#         log(f"Erreur lors de l'exécution de la commande: {e.output.decode().strip()}")
#         return None

# def install_git():
#     if run_command("git --version"):
#         log("Git déjà installé.")
#     else:
#         log("Git non trouvé. Installation...")
#         if os.path.exists("Git-2.42.0-64-bit.exe"):
#             run_command('start /wait "Git-2.42.0-64-bit.exe" /SILENT /VERYSILENT /NORESTART')
#             log("Git installé.")
#         else:
#             log("Installeur Git non trouvé.")

# def install_python():
#     if run_command("python --version"):
#         log("Python déjà installé.")
#     else:
#         log("Python non trouvé. Installation...")
#         if os.path.exists("python-3.11.5-amd64.exe"):
#             run_command('start /wait "python-3.11.5-amd64.exe" /quiet InstallAllUsers=1 PrependPath=1')
#             log("Python installé.")
#         else:
#             log("Installeur Python non trouvé.")

# def handle_instance_installation():
#     folder_path_robot1 = "C:\\bon\\robot1"
#     folder_path_robot2 = "C:\\bon\\robot2"

#     if os.path.exists(folder_path_robot1) and os.path.exists(folder_path_robot2):
#         log("Instances 1 et 2 déjà installées.")
#         num_instances = int(input("Combien d'instances souhaitez-vous installer (supérieur à 2) ? "))
#         if num_instances > 2:
#             for i in range(3, num_instances + 1):
#                 install_instance(i)
#         else:
#             log("Installation annulée. L'utilisateur n'a pas saisi de nombre valide.")
        
#     elif os.path.exists(folder_path_robot1):
#         log("Instance 1 déjà installée.")
#         install_instance_2 = input("Robot1 est déjà installé. Voulez-vous installer l'instance 2 ? (o/n) ")
#         if install_instance_2.lower() == 'o':
#             install_instance(2)
#         else:
#             log("Installation annulée par l'utilisateur.")
        
#     else:
#         log("Installation de l'instance de démo (Robot1)...")
#         install_instance(1)

# def install_instance(instance_number):
#     folder_path = f"C:\\bon\\robot{instance_number}"
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path, exist_ok=True)
#         log(f"Création du dossier pour l'instance {instance_number}...")

#         log(f"Clonage du dépôt GitHub pour l'instance {instance_number}...")
#         run_command(f'git clone https://github.com/kitokoh/facebook-group-bot.git {folder_path}')

#         log(f"Création de l'environnement virtuel pour robot{instance_number}...")
#         run_command(f"python -m venv {folder_path}\\env{instance_number}")

#         log(f"Installation des dépendances pour robot{instance_number}...")
#         run_command(f"{folder_path}\\env{instance_number}\\Scripts\\activate && pip install -r {folder_path}\\requirements.txt")

#         log(f"Installation terminée pour l'instance {instance_number}.")
#     else:
#         log(f"L'instance {instance_number} existe déjà. Aucune action nécessaire.")

# def main():
#     log("Démarrage de l'installation...")
#     if not check_internet_connection():
#         return

#     install_git()
#     install_python()
#     handle_instance_installation()

#     log("Installation terminée. Vous pouvez fermer la fenêtre.")

# if __name__ == "__main__":
#     main()
import os
import subprocess
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

def log(message):
    print(message)

def check_internet_connection():
    try:
        subprocess.check_call(["ping", "google.com", "-n", "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log("Connexion Internet vérifiée.")
        return True
    except subprocess.CalledProcessError:
        log("Aucune connexion Internet. Veuillez vérifier votre connexion.")
        return False

def run_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode().strip()
        return result
    except subprocess.CalledProcessError as e:
        log(f"Erreur lors de l'exécution de la commande: {e.output.decode().strip()}")
        return None

def install_git():
    if run_command("git --version"):
        log("Git déjà installé.")
    else:
        log("Git non trouvé. Installation...")
        if os.path.exists("Git-2.42.0-64-bit.exe"):
            run_command('start /wait "Git-2.42.0-64-bit.exe" /SILENT /VERYSILENT /NORESTART')
            log("Git installé.")
        else:
            log("Installeur Git non trouvé.")

def install_python():
    if run_command("python --version"):
        log("Python déjà installé.")
    else:
        log("Python non trouvé. Installation...")
        if os.path.exists("python-3.11.5-amd64.exe"):
            run_command('start /wait "python-3.11.5-amd64.exe" /quiet InstallAllUsers=1 PrependPath=1')
            log("Python installé.")
        else:
            log("Installeur Python non trouvé.")

def handle_instance_installation():
    instance_number = 1

    # Vérifie les instances existantes
    while os.path.exists(f"C:\\wabon\\robot{instance_number}"):
        instance_number += 1  # Incrémente le numéro d'instance

    log(f"Installation de l'instance {instance_number}...")
    install_instance(instance_number)

    # Rendre tous les dossiers invisibles
    hide_directories("C:\\wabon")

def install_instance(instance_number):
    folder_path = f"C:\\wabon\\robot{instance_number}"
    os.makedirs(folder_path, exist_ok=True)
    log(f"Création du dossier pour l'instance {instance_number}...")

    log(f"Clonage du dépôt GitHub pour l'instance {instance_number}...")
    #run_command(f'git clone https://github.com/kitokoh/bondist1.git {folder_path}')
    run_command(f'git clone https://github.com/kitokoh/wabon.git {folder_path}')

    log(f"Création de l'environnement virtuel pour robot{instance_number}...")
    run_command(f"python -m venv {folder_path}\\env{instance_number}")

    log(f"Installation des dépendances pour robot{instance_number}...")
    run_command(f"{folder_path}\\env{instance_number}\\Scripts\\activate && pip install -r {folder_path}\\requirements.txt")

    log(f"Installation terminée pour l'instance {instance_number}.")

def hide_directories(parent_folder):
    log(f"Rendre tous les dossiers dans {parent_folder} invisibles...")
    run_command(f'attrib +h "{parent_folder}\\*" /S /D')

def main():
    log("Démarrage de l'installation...")
    if not check_internet_connection():
        return

    install_git()
    install_python()
    handle_instance_installation()

    log("Installation terminée. Vous pouvez fermer la fenêtre.")

if __name__ == "__main__":
    main()
