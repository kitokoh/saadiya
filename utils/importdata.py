import sys
import os
import zipfile
import tarfile
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox, QProgressBar, QHBoxLayout,
    QComboBox, QListWidget, QCheckBox, QLineEdit, QTabWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon

class CompressionThread(QThread):
    update_progress = pyqtSignal(int)  # Signal pour mettre à jour la barre de progression
    finished = pyqtSignal()  # Signal pour indiquer la fin de la compression

    def __init__(self, files, output_path, compression_format, compression_level, password=None):
        super().__init__()
        self.files = files
        self.output_path = output_path
        self.compression_format = compression_format
        self.compression_level = compression_level
        self.password = password

    def run(self):
        total_files = len(self.files)
        if self.compression_format == "ZIP":
            with zipfile.ZipFile(self.output_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=self.compression_level) as zipf:
                if self.password:
                    zipf.setpassword(self.password.encode())
                for i, (file_path, arcname) in enumerate(self.files):
                    zipf.write(file_path, arcname)
                    progress = int((i + 1) / total_files * 100)
                    self.update_progress.emit(progress)
        elif self.compression_format == "TAR":
            with tarfile.open(self.output_path, 'w:gz') as tarf:
                for i, (file_path, arcname) in enumerate(self.files):
                    tarf.add(file_path, arcname=arcname)
                    progress = int((i + 1) / total_files * 100)
                    self.update_progress.emit(progress)
        self.finished.emit()

class ExtractionThread(QThread):
    update_progress = pyqtSignal(int)  # Signal pour mettre à jour la barre de progression
    finished = pyqtSignal()  # Signal pour indiquer la fin de l'extraction

    def __init__(self, archive_path, output_folder, password=None):
        super().__init__()
        self.archive_path = archive_path
        self.output_folder = output_folder
        self.password = password

    def run(self):
        if self.archive_path.endswith(".zip"):
            with zipfile.ZipFile(self.archive_path, 'r') as zipf:
                if self.password:
                    zipf.setpassword(self.password.encode())
                total_files = len(zipf.infolist())
                for i, file_info in enumerate(zipf.infolist()):
                    zipf.extract(file_info, path=self.output_folder)
                    progress = int((i + 1) / total_files * 100)
                    self.update_progress.emit(progress)
        elif self.archive_path.endswith(".tar.gz"):
            with tarfile.open(self.archive_path, 'r:gz') as tarf:
                total_files = len(tarf.getmembers())
                for i, member in enumerate(tarf.getmembers()):
                    tarf.extract(member, path=self.output_folder)
                    progress = int((i + 1) / total_files * 100)
                    self.update_progress.emit(progress)
        self.finished.emit()

class DataExporterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Exportation et Importation de Données')
        self.setGeometry(100, 100, 600, 400)

        # Style CSS pour améliorer l'interface
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)

        layout = QVBoxLayout()

        # Onglets pour exporter et importer
        self.tabs = QTabWidget(self)
        self.export_tab = QWidget()
        self.import_tab = QWidget()
        self.tabs.addTab(self.export_tab, "Exporter")
        self.tabs.addTab(self.import_tab, "Importer")
        layout.addWidget(self.tabs)

        # Onglet d'exportation
        self.init_export_tab()
        # Onglet d'importation
        self.init_import_tab()

        self.setLayout(layout)

    def init_export_tab(self):
        layout = QVBoxLayout()

        # Label pour afficher les fichiers sélectionnés
        self.export_label = QLabel('Aucun fichier sélectionné.', self)
        layout.addWidget(self.export_label)

        # Bouton pour sélectionner des fichiers ou dossiers
        self.select_button = QPushButton('Sélectionner des fichiers/dossiers', self)
        self.select_button.setIcon(QIcon.fromTheme("folder-open"))
        self.select_button.clicked.connect(self.select_files)
        layout.addWidget(self.select_button)

        # Liste des fichiers sélectionnés avec des cases à cocher pour inclure/exclure
        self.file_list = QListWidget(self)
        layout.addWidget(self.file_list)

        # Options de compression
        compression_layout = QHBoxLayout()
        compression_label = QLabel('Format de compression :', self)
        self.compression_combo = QComboBox(self)
        self.compression_combo.addItem("ZIP", "ZIP")
        self.compression_combo.addItem("TAR (gzip)", "TAR")
        compression_layout.addWidget(compression_label)
        compression_layout.addWidget(self.compression_combo)

        compression_level_label = QLabel('Niveau de compression :', self)
        self.compression_level_combo = QComboBox(self)
        self.compression_level_combo.addItem("Aucune compression", 0)
        self.compression_level_combo.addItem("Faible", 1)
        self.compression_level_combo.addItem("Moyenne", 5)
        self.compression_level_combo.addItem("Élevée", 9)
        compression_layout.addWidget(compression_level_label)
        compression_layout.addWidget(self.compression_level_combo)
        layout.addLayout(compression_layout)

        # Option pour chiffrer le fichier ZIP
        self.encrypt_checkbox = QCheckBox('Chiffrer le fichier ZIP', self)
        self.encrypt_checkbox.stateChanged.connect(self.toggle_encryption)
        layout.addWidget(self.encrypt_checkbox)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Entrez un mot de passe")
        self.password_input.setEnabled(False)
        layout.addWidget(self.password_input)

        # Barre de progression
        self.export_progress_bar = QProgressBar(self)
        self.export_progress_bar.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.export_progress_bar)

        # Bouton pour exporter et zipper
        self.export_button = QPushButton('Exporter et Compresser', self)
        self.export_button.setIcon(QIcon.fromTheme("document-save"))
        self.export_button.clicked.connect(self.export_data)
        layout.addWidget(self.export_button)

        self.export_tab.setLayout(layout)

    def init_import_tab(self):
        layout = QVBoxLayout()

        # Bouton pour sélectionner un fichier compressé
        self.import_select_button = QPushButton('Sélectionner un fichier compressé', self)
        self.import_select_button.setIcon(QIcon.fromTheme("folder-open"))
        self.import_select_button.clicked.connect(self.select_archive)
        layout.addWidget(self.import_select_button)

        # Champ pour le mot de passe (si nécessaire)
        self.import_password_input = QLineEdit(self)
        self.import_password_input.setPlaceholderText("Entrez un mot de passe (si nécessaire)")
        layout.addWidget(self.import_password_input)

        # Bouton pour choisir le dossier de destination
        self.import_destination_button = QPushButton('Choisir le dossier de destination', self)
        self.import_destination_button.setIcon(QIcon.fromTheme("folder"))
        self.import_destination_button.clicked.connect(self.select_destination_folder)
        layout.addWidget(self.import_destination_button)

        # Barre de progression
        self.import_progress_bar = QProgressBar(self)
        self.import_progress_bar.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.import_progress_bar)

        # Bouton pour importer et décompresser
        self.import_button = QPushButton('Importer et Décompresser', self)
        self.import_button.setIcon(QIcon.fromTheme("document-open"))
        self.import_button.clicked.connect(self.import_data)
        layout.addWidget(self.import_button)

        self.import_tab.setLayout(layout)

    def select_files(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Sélectionner des fichiers", "", "Tous les fichiers (*)", options=options)
        folders = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier", options=options)

        self.selected_files = []
        if files:
            self.selected_files.extend([(file, os.path.basename(file)) for file in files])
        if folders:
            for root, _, files_in_folder in os.walk(folders):
                for file in files_in_folder:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.dirname(folders))
                    self.selected_files.append((file_path, arcname))

        if self.selected_files:
            self.export_label.setText(f'{len(self.selected_files)} fichier(s) sélectionné(s).')
            self.file_list.clear()
            for file_path, arcname in self.selected_files:
                item = QListWidgetItem(file_path)
                item.setCheckState(Qt.Checked)
                self.file_list.addItem(item)
        else:
            self.export_label.setText('Aucun fichier sélectionné.')

    def toggle_encryption(self):
        self.password_input.setEnabled(self.encrypt_checkbox.isChecked())

    def export_data(self):
        if not hasattr(self, 'selected_files') or not self.selected_files:
            QMessageBox.warning(self, 'Erreur', 'Veuillez d\'abord sélectionner des fichiers ou dossiers.')
            return

        # Filtrer les fichiers cochés
        files_to_compress = []
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            if item.checkState() == Qt.Checked:
                files_to_compress.append(self.selected_files[i])

        if not files_to_compress:
            QMessageBox.warning(self, 'Erreur', 'Aucun fichier sélectionné pour la compression.')
            return

        # Choisir l'emplacement du fichier de sortie
        compression_format = self.compression_combo.currentData()
        file_filter = "ZIP Files (*.zip)" if compression_format == "ZIP" else "TAR Files (*.tar.gz)"
        output_path, _ = QFileDialog.getSaveFileName(self, 'Enregistrer le fichier', '', file_filter)
        if not output_path:
            return

        # Récupérer le niveau de compression et le mot de passe
        compression_level = self.compression_level_combo.currentData()
        password = self.password_input.text() if self.encrypt_checkbox.isChecked() else None

        # Désactiver les boutons pendant la compression
        self.select_button.setEnabled(False)
        self.export_button.setEnabled(False)

        # Lancer le thread de compression
        self.compression_thread = CompressionThread(files_to_compress, output_path, compression_format, compression_level, password)
        self.compression_thread.update_progress.connect(self.export_progress_bar.setValue)
        self.compression_thread.finished.connect(self.on_compression_finished)
        self.compression_thread.start()

    def on_compression_finished(self):
        # Réactiver les boutons après la compression
        self.select_button.setEnabled(True)
        self.export_button.setEnabled(True)
        QMessageBox.information(self, 'Succès', 'Les données ont été exportées et compressées avec succès.')

    def select_archive(self):
        options = QFileDialog.Options()
        archive_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier compressé", "", "Fichiers compressés (*.zip *.tar.gz)", options=options)
        if archive_path:
            self.archive_path = archive_path
            self.import_select_button.setText(f"Fichier sélectionné : {os.path.basename(archive_path)}")

    def select_destination_folder(self):
        options = QFileDialog.Options()
        destination_folder = QFileDialog.getExistingDirectory(self, "Choisir le dossier de destination", options=options)
        if destination_folder:
            self.destination_folder = destination_folder
            self.import_destination_button.setText(f"Dossier de destination : {os.path.basename(destination_folder)}")

    def import_data(self):
        if not hasattr(self, 'archive_path') or not self.archive_path:
            QMessageBox.warning(self, 'Erreur', 'Veuillez d\'abord sélectionner un fichier compressé.')
            return

        if not hasattr(self, 'destination_folder') or not self.destination_folder:
            QMessageBox.warning(self, 'Erreur', 'Veuillez d\'abord choisir un dossier de destination.')
            return

        # Récupérer le mot de passe (si nécessaire)
        password = self.import_password_input.text() if self.import_password_input.text() else None

        # Désactiver les boutons pendant l'extraction
        self.import_select_button.setEnabled(False)
        self.import_destination_button.setEnabled(False)
        self.import_button.setEnabled(False)

        # Lancer le thread d'extraction
        self.extraction_thread = ExtractionThread(self.archive_path, self.destination_folder, password)
        self.extraction_thread.update_progress.connect(self.import_progress_bar.setValue)
        self.extraction_thread.finished.connect(self.on_extraction_finished)
        self.extraction_thread.start()

    def on_extraction_finished(self):
        # Réactiver les boutons après l'extraction
        self.import_select_button.setEnabled(True)
        self.import_destination_button.setEnabled(True)
        self.import_button.setEnabled(True)
        QMessageBox.information(self, 'Succès', 'Les données ont été importées et décompressées avec succès.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DataExporterApp()
    ex.show()
    sys.exit(app.exec_())