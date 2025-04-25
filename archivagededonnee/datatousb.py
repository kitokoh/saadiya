import sys
import os
import shutil
import win32api
import win32file
import psutil
from PyQt5 import QtGui
# ou mieux, importer juste ce dont tu as besoin :
from PyQt5.QtGui import QFont, QIcon, QPixmap  # exemple

from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, 
                            QPushButton, QComboBox, QMessageBox, QProgressBar, QCheckBox,
                            QGroupBox, QHBoxLayout, QFileDialog, QLineEdit)
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QIcon

class CopyThread(QThread):
    update_progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def __init__(self, source_paths, dest_path, parent=None):
        super().__init__(parent)
        self.source_paths = source_paths
        self.dest_path = dest_path
        self.canceled = False

    def run(self):
        try:
            total_files = 0
            # Compter le nombre total de fichiers à copier
            for src in self.source_paths:
                if os.path.isdir(src):
                    for root, _, files in os.walk(src):
                        total_files += len(files)
                elif os.path.isfile(src):
                    total_files += 1

            if total_files == 0:
                self.finished.emit(False, "Aucun fichier à copier")
                return

            copied_files = 0
            for src in self.source_paths:
                if self.canceled:
                    break

                if os.path.isdir(src):
                    dir_name = os.path.basename(src)
                    dest_dir = os.path.join(self.dest_path, dir_name)
                    os.makedirs(dest_dir, exist_ok=True)

                    for root, _, files in os.walk(src):
                        for file in files:
                            if self.canceled:
                                break
                            src_path = os.path.join(root, file)
                            rel_path = os.path.relpath(root, src)
                            dest_file_path = os.path.join(dest_dir, rel_path, file)
                            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                            shutil.copy2(src_path, dest_file_path)
                            copied_files += 1
                            progress = int((copied_files / total_files) * 100)
                            self.update_progress.emit(progress)
                elif os.path.isfile(src):
                    shutil.copy2(src, self.dest_path)
                    copied_files += 1
                    progress = int((copied_files / total_files) * 100)
                    self.update_progress.emit(progress)

            if self.canceled:
                self.finished.emit(False, "Opération annulée")
            else:
                self.finished.emit(True, "Copie terminée avec succès")

        except Exception as e:
            self.finished.emit(False, f"Erreur: {str(e)}")

class USBCheckerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionnaire USB ADN Leopardo Pro")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon("icon.ico"))  # Remplacez par votre icône
        
        # Variables de configuration
        self.config = {
            "auto_refresh": True,
            "refresh_interval": 5,  # en secondes
            "default_folders": [
                os.path.join(os.path.expanduser("~"), "Desktop", "dossier1"),
                os.path.join(os.path.expanduser("~"), "Downloads", "dossier2")
            ],
            "custom_folders": []
        }
        
        self.initUI()
        self.load_settings()
        self.check_usb_drives()
        
        # Timer pour la vérification automatique
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.check_usb_drives)
        if self.config["auto_refresh"]:
            self.refresh_timer.start(self.config["refresh_interval"] * 1000)
        
        # Thread de copie
        self.copy_thread = None

    def initUI(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Section USB
        usb_group = QGroupBox("Détection USB")
        usb_layout = QVBoxLayout()
        
        self.usb_combo = QComboBox()
        self.usb_info_label = QLabel("Aucune information disponible")
        self.refresh_button = QPushButton("Actualiser")
        self.refresh_button.clicked.connect(self.check_usb_drives)
        
        usb_layout.addWidget(QLabel("Clés USB disponibles:"))
        usb_layout.addWidget(self.usb_combo)
        usb_layout.addWidget(self.usb_info_label)
        usb_layout.addWidget(self.refresh_button)
        usb_group.setLayout(usb_layout)
        
        # Section Dossiers
        folders_group = QGroupBox("Dossiers à copier")
        folders_layout = QVBoxLayout()
        
        # Dossiers par défaut
        self.default_folder1 = QCheckBox("Dossier1 (Bureau)")
        self.default_folder1.setChecked(True)
        self.default_folder2 = QCheckBox("Dossier2 (Téléchargements)")
        self.default_folder2.setChecked(True)
        
        # Dossiers personnalisés
        self.custom_folder_label = QLabel("Dossiers supplémentaires:")
        self.custom_folder_list = QComboBox()
        self.custom_folder_list.addItems(self.config["custom_folders"])
        
        add_folder_button = QPushButton("Ajouter un dossier")
        add_folder_button.clicked.connect(self.add_custom_folder)
        remove_folder_button = QPushButton("Supprimer le dossier sélectionné")
        remove_folder_button.clicked.connect(self.remove_custom_folder)
        
        folders_layout.addWidget(self.default_folder1)
        folders_layout.addWidget(self.default_folder2)
        folders_layout.addWidget(self.custom_folder_label)
        folders_layout.addWidget(self.custom_folder_list)
        
        folder_buttons_layout = QHBoxLayout()
        folder_buttons_layout.addWidget(add_folder_button)
        folder_buttons_layout.addWidget(remove_folder_button)
        folders_layout.addLayout(folder_buttons_layout)
        
        folders_group.setLayout(folders_layout)
        
        # Section Progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_label = QLabel("Prêt")
        
        # Boutons d'action
        action_layout = QHBoxLayout()
        self.process_button = QPushButton("Exécuter")
        self.process_button.clicked.connect(self.process_usb)
        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.clicked.connect(self.cancel_operation)
        self.cancel_button.setEnabled(False)
        
        action_layout.addWidget(self.process_button)
        action_layout.addWidget(self.cancel_button)
        
        # Options
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()
        
        self.auto_refresh_check = QCheckBox("Actualisation automatique des USB")
        self.auto_refresh_check.setChecked(self.config["auto_refresh"])
        self.auto_refresh_check.stateChanged.connect(self.toggle_auto_refresh)
        
        self.interval_label = QLabel("Intervalle d'actualisation (secondes):")
        self.interval_input = QLineEdit(str(self.config["refresh_interval"]))
        self.interval_input.setValidator(QtGui.QIntValidator(1, 3600))
        self.interval_input.editingFinished.connect(self.update_refresh_interval)
        
        options_layout.addWidget(self.auto_refresh_check)
        options_layout.addWidget(self.interval_label)
        options_layout.addWidget(self.interval_input)
        options_group.setLayout(options_layout)
        
        # Assemblage de l'interface
        main_layout.addWidget(usb_group)
        main_layout.addWidget(folders_group)
        main_layout.addWidget(options_group)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.status_label)
        main_layout.addLayout(action_layout)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
    def load_settings(self):
        # Ici vous pourriez charger des paramètres depuis un fichier
        pass
        
    def save_settings(self):
        # Ici vous pourriez sauvegarder les paramètres
        pass
        
    def toggle_auto_refresh(self, state):
        self.config["auto_refresh"] = (state == Qt.Checked)
        if self.config["auto_refresh"]:
            self.refresh_timer.start(self.config["refresh_interval"] * 1000)
        else:
            self.refresh_timer.stop()
            
    def update_refresh_interval(self):
        try:
            interval = int(self.interval_input.text())
            if 1 <= interval <= 3600:
                self.config["refresh_interval"] = interval
                if self.config["auto_refresh"]:
                    self.refresh_timer.start(interval * 1000)
        except ValueError:
            pass
            
    def add_custom_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier à ajouter")
        if folder and folder not in self.config["custom_folders"]:
            self.config["custom_folders"].append(folder)
            self.custom_folder_list.addItem(folder)
            
    def remove_custom_folder(self):
        current_index = self.custom_folder_list.currentIndex()
        if current_index >= 0:
            folder = self.custom_folder_list.currentText()
            self.config["custom_folders"].remove(folder)
            self.custom_folder_list.removeItem(current_index)
            
    def check_usb_drives(self):
        """Détecte les lecteurs USB disponibles et affiche les informations"""
        self.usb_drives = []
        drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
        
        for drive in drives:
            if win32file.GetDriveType(drive) == win32file.DRIVE_REMOVABLE:
                try:
                    usage = psutil.disk_usage(drive)
                    self.usb_drives.append({
                        'letter': drive,
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free
                    })
                except:
                    continue
        
        self.usb_combo.clear()
        if self.usb_drives:
            for usb in self.usb_drives:
                display_text = f"{usb['letter']} - Libre: {self.format_size(usb['free'])} / {self.format_size(usb['total'])}"
                self.usb_combo.addItem(display_text, usb['letter'])
            
            if len(self.usb_drives) == 1:
                self.status_label.setText(f"1 clé USB détectée")
            else:
                self.status_label.setText(f"{len(self.usb_drives)} clés USB détectées")
        else:
            self.status_label.setText("Aucune clé USB détectée. Veuillez en insérer une.")
            
    def format_size(self, size_bytes):
        """Formatte la taille en octets en une chaîne lisible"""
        for unit in ['o', 'Ko', 'Mo', 'Go', 'To']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} To"
        
    def get_selected_folders(self):
        """Retourne la liste des dossiers sélectionnés pour la copie"""
        folders = []
        
        if self.default_folder1.isChecked():
            folders.append(self.config["default_folders"][0])
        if self.default_folder2.isChecked():
            folders.append(self.config["default_folders"][1])
            
        if self.custom_folder_list.count() > 0:
            folders.extend(self.config["custom_folders"])
            
        # Filtrer les dossiers qui n'existent pas
        return [f for f in folders if os.path.exists(f)]
        
    def process_usb(self):
        """Traite la clé USB sélectionnée"""
        if not self.usb_drives:
            QMessageBox.warning(self, "Aucune USB", "Veuillez insérer une clé USB d'abord.")
            return
            
        selected_index = self.usb_combo.currentIndex()
        if selected_index < 0:
            return
            
        selected_drive = self.usb_drives[selected_index]['letter']
        folders_to_copy = self.get_selected_folders()
        
        if not folders_to_copy:
            QMessageBox.warning(self, "Aucun dossier", "Aucun dossier sélectionné pour la copie.")
            return
            
        # Vérifier l'espace disponible
        total_size = 0
        for folder in folders_to_copy:
            if os.path.isdir(folder):
                total_size += sum(os.path.getsize(os.path.join(dirpath, filename)) 
                             for dirpath, _, filenames in os.walk(folder) 
                             for filename in filenames)
            elif os.path.isfile(folder):
                total_size += os.path.getsize(folder)
                
        if total_size > self.usb_drives[selected_index]['free']:
            QMessageBox.warning(self, "Espace insuffisant", 
                              f"Espace insuffisant sur la clé USB. Nécessaire: {self.format_size(total_size)}, Disponible: {self.format_size(self.usb_drives[selected_index]['free'])}")
            return
            
        # Créer/rénommer le dossier adn_leopardo
        try:
            base_dir = os.path.join(selected_drive, "adn_leopardo")
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_dir_name = f"adn_leopardo_{now}"
            
            if os.path.exists(base_dir):
                os.rename(base_dir, os.path.join(selected_drive, new_dir_name))
                base_dir = os.path.join(selected_drive, new_dir_name)
                self.status_label.setText(f"Renommage du dossier en {new_dir_name}")
            else:
                os.makedirs(base_dir)
                self.status_label.setText("Création du nouveau dossier")
                
            # Démarrer la copie dans un thread séparé
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.process_button.setEnabled(False)
            self.cancel_button.setEnabled(True)
            
            self.copy_thread = CopyThread(folders_to_copy, base_dir)
            self.copy_thread.update_progress.connect(self.update_progress)
            self.copy_thread.finished.connect(self.copy_finished)
            self.copy_thread.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {str(e)}")
            self.status_label.setText("Erreur lors de l'opération")
            
    def update_progress(self, value):
        self.progress_bar.setValue(value)
        
    def copy_finished(self, success, message):
        self.progress_bar.setVisible(False)
        self.process_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        
        if success:
            QMessageBox.information(self, "Succès", message)
            self.status_label.setText("Opération terminée avec succès")
        else:
            QMessageBox.warning(self, "Avertissement", message)
            self.status_label.setText(message)
            
    def cancel_operation(self):
        if self.copy_thread and self.copy_thread.isRunning():
            self.copy_thread.canceled = True
            self.cancel_button.setEnabled(False)
            
    def closeEvent(self, event):
        if self.copy_thread and self.copy_thread.isRunning():
            reply = QMessageBox.question(self, 'Opération en cours', 
                                       "Une opération est en cours. Voulez-vous vraiment quitter?", 
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.copy_thread.canceled = True
                self.copy_thread.wait(2000)  # Attendre 2 secondes max
                event.accept()
            else:
                event.ignore()
        else:
            self.save_settings()
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = USBCheckerApp()
    window.show()
    sys.exit(app.exec_())