import os
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QMessageBox, QTableWidgetItem, QCheckBox, QDialog, QCalendarWidget, QDateEdit, QGraphicsDropShadowEffect, QFileDialog
)
from PyQt5.QtGui import QColor, QFont
import locale
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


class AddActivityDialog(QtWidgets.QDialog):
    def __init__(self, exe_files):
        super().__init__()
        self.setWindowTitle(self.tr("📅 Schedule an Activity"))
        self.setFixedSize(500, 550)  # Taille ajustée pour le calendrier
        self.setWindowIcon(QtGui.QIcon("resources/icons/schedule.ico"))

        # Style général
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
                border-radius: 10px;
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
                color: #2c3e50;
            }
            QLineEdit, QComboBox, QTimeEdit, QDateEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus, QTimeEdit:focus, QDateEdit:focus {
                border: 1px solid #3498db;
            }
            QCheckBox {
                font-size: 13px;
                color: #34495e;
            }
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #2980b9;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QCalendarWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
            }
        """)

        # Widgets
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText(self.tr("📝 Program Name"))
        self.name_input.setReadOnly(True)

        self.program_input = QtWidgets.QComboBox()
        self.program_input.addItems(exe_files)
        self.program_input.currentIndexChanged.connect(self.update_name)

        self.daily_checkbox = QtWidgets.QCheckBox(self.tr("🔄 Execute Daily"))

        self.days_group = QtWidgets.QGroupBox(self.tr("📅 Select Specific Days"))
        self.days_layout = QtWidgets.QHBoxLayout()
        self.day_checkboxes = []
        for day in [self.tr("Mon"), self.tr("Tue"), self.tr("Wed"), self.tr("Thu"), self.tr("Fri"), self.tr("Sat"), self.tr("Sun")]:
            checkbox = QtWidgets.QCheckBox(day)
            self.day_checkboxes.append(checkbox)
            self.days_layout.addWidget(checkbox)
        self.days_group.setLayout(self.days_layout)

        self.time_input = QtWidgets.QTimeEdit()
        self.time_input.setDisplayFormat("HH:mm")
        self.time_input.setFont(QtGui.QFont("Arial", 12))

        # Ajouter un QCalendarWidget pour la sélection de dates spécifiques
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumDate(QtCore.QDate.currentDate())  # Empêcher la sélection de dates passées
        self.selected_dates = set()  # Pour stocker les dates sélectionnées

        # Connecter le signal de clic sur une date
        self.calendar.clicked.connect(self.toggle_date_selection)

        # Ajouter un QCheckBox pour activer/désactiver la sélection de dates spécifiques
        self.specific_dates_checkbox = QtWidgets.QCheckBox(self.tr("📅 Schedule on specific dates"))
        self.specific_dates_checkbox.stateChanged.connect(self.toggle_specific_dates)

        # Bouton de sauvegarde
        save_button = QtWidgets.QPushButton(self.tr("💾 Save"))
        save_button.clicked.connect(self.accept)

        # Layout principal
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Ajout des widgets
        main_layout.addWidget(self.create_form_group("📂 Program:", self.program_input))
        main_layout.addWidget(self.create_form_group("📝 Name:", self.name_input))
        main_layout.addWidget(self.daily_checkbox)
        main_layout.addWidget(self.days_group)
        main_layout.addWidget(self.create_form_group("⏰ Execution Time:", self.time_input))
        main_layout.addWidget(self.specific_dates_checkbox)
        main_layout.addWidget(self.calendar)
        main_layout.addWidget(save_button, alignment=QtCore.Qt.AlignRight)

        # Masquer le calendrier par défaut
        self.calendar.setVisible(False)

        self.setLayout(main_layout)

        # Mettre à jour le nom initial
        self.update_name()

    def create_form_group(self, label_text, widget):
        """Crée une ligne de formulaire avec une étiquette et un widget."""
        container = QtWidgets.QWidget()
        form_layout = QtWidgets.QHBoxLayout(container)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.addWidget(QtWidgets.QLabel(label_text))
        form_layout.addWidget(widget)
        return container

    def update_name(self):
        """Met à jour le champ du nom basé sur le fichier sélectionné."""
        self.name_input.setText(self.program_input.currentText())

    def toggle_specific_dates(self, state):
        """Afficher ou masquer le calendrier en fonction de l'état de la checkbox."""
        self.calendar.setVisible(state == QtCore.Qt.Checked)

    def toggle_date_selection(self, date):
        """Ajoute ou supprime une date de la sélection."""
        if date in self.selected_dates:
            self.selected_dates.remove(date)
        else:
            self.selected_dates.add(date)
        self.highlight_selected_dates()

    def highlight_selected_dates(self):
        """Met en évidence les dates sélectionnées dans le calendrier."""
        for date in self.selected_dates:
            format = QtGui.QTextCharFormat()
            format.setBackground(QtGui.QColor("#3498db"))
            format.setForeground(QtGui.QColor("#ffffff"))
            self.calendar.setDateTextFormat(date, format)

    def get_activity_data(self):
        """Retourne les données saisies par l'utilisateur, y compris les dates spécifiques si sélectionnées."""
        selected_days = [checkbox.text() for checkbox in self.day_checkboxes if checkbox.isChecked()]
        
        if self.specific_dates_checkbox.isChecked():
            # Convertir les dates sélectionnées en format MM/JJ/AAAA
            selected_dates = [date.toString("MM/dd/yyyy") for date in self.selected_dates]
        else:
            selected_dates = None

        return (
            self.name_input.text(),
            self.program_input.currentText(),
            self.daily_checkbox.isChecked(),
            selected_days,
            self.time_input.time().toString("HH:mm"),
            selected_dates  # Retourner les dates spécifiques au bon format
        )

class Activite(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr("📅 Scheduled Activities Manager"))
        self.setStyleSheet(self._get_styles())
        self.resize(1000, 700)

        # Titre principal
        title_label = QtWidgets.QLabel(self.tr("📅 Scheduled Activities"))
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setFont(QtGui.QFont("Arial", 20, QFont.Bold))

        # Barre de recherche
        self.search_entry = QtWidgets.QLineEdit()
        self.search_entry.setPlaceholderText(self.tr("🔍 Search an activity..."))

        # Boutons d'action
        self.search_button = QtWidgets.QPushButton(self.tr("🔍 Search"))
        self.search_button.clicked.connect(self.search_activities)

        self.add_button = QtWidgets.QPushButton(self.tr("➕ Schedule an Activity"))
        self.add_button.clicked.connect(self.add_activity)

        self.pause_button = QtWidgets.QPushButton(self.tr("⏸️ Pause"))
        self.pause_button.clicked.connect(self.pause_selected_activities)

        self.delete_button = QtWidgets.QPushButton(self.tr("❌ Delete"))
        self.delete_button.clicked.connect(self.delete_selected_activities)

        self.refresh_button = QtWidgets.QPushButton(self.tr("🔄 Load Activities"))
        self.refresh_button.clicked.connect(self.load_activities)

        self.export_button = QtWidgets.QPushButton(self.tr("📤 Export Activities"))
        self.export_button.clicked.connect(self.export_activities)

        # Ajouter une ombre lumineuse au bouton "Add"
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 212, 255))  # Bleu néon
        shadow.setOffset(0, 5)
        self.add_button.setGraphicsEffect(shadow)

        # Layout pour la barre de recherche et les boutons
        top_bar_layout = QtWidgets.QHBoxLayout()
        top_bar_layout.addWidget(self.search_entry)
        top_bar_layout.addWidget(self.search_button)
        top_bar_layout.addWidget(self.add_button)
        top_bar_layout.addWidget(self.pause_button)
        top_bar_layout.addWidget(self.delete_button)
        top_bar_layout.addWidget(self.refresh_button)
        top_bar_layout.addWidget(self.export_button)

        # Tableau des activités
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            self.tr("🔢 Number"), self.tr("📝 Name"), self.tr("📂 Program"), 
            self.tr("📅 Days"), self.tr("⏰ Time"), self.tr("📅 Date"), self.tr("⚙️ Action")
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSortingEnabled(True)

        # Layout principal
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(title_label)
        main_layout.addLayout(top_bar_layout)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

        # Charger les activités planifiées au démarrage
        QtCore.QTimer.singleShot(100, self.load_activities)

    def _get_styles(self):
        """Retourne le style CSS pour l'interface utilisateur."""
        return """
            QWidget {
                font-family: Arial;
                background-color: #f4f4f4;
            }
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #333;
            }
            QLineEdit {
                border: 1px solid #888;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border-radius: 5px;
                border: none;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
            }
            QHeaderView::section {
                background-color: #ddd;
                font-weight: bold;
                padding: 4px;
            }
        """

    def load_activities(self):
        """Charge et affiche les activités planifiées."""
        self.table.setRowCount(0)  # Réinitialiser le tableau

        try:
            # Chemin du dossier contenant les fichiers .exe
            folder_path = os.path.expanduser("~\\AppData\\Roaming\\Saadiya\\resources\\tools")
            if not os.path.exists(folder_path):
                QMessageBox.critical(self, self.tr("Error"), self.tr(f"The folder {folder_path} does not exist."))
                return

            # Lister les fichiers .exe
            exe_files = [f for f in os.listdir(folder_path) if f.endswith(".exe")]
            if not exe_files:
                QMessageBox.warning(self, self.tr("Warning"), self.tr("No .exe files found in the tools folder."))
                return

            # Récupérer les tâches planifiées avec schtasks
            try:
                result = subprocess.check_output("schtasks /query /fo csv /nh", shell=True, encoding="utf-8", errors="ignore")
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, self.tr("Error"), self.tr(f"Failed to query scheduled tasks: {e}"))
                return

            lines = result.strip().splitlines()

            if not lines:
                QMessageBox.information(self, self.tr("Info"), self.tr("No scheduled tasks found."))
                return

            # Analyser les tâches
            for i, line in enumerate(lines):
                try:
                    parts = [p.strip('"') for p in line.split(",")]
                    if len(parts) < 3:
                        continue

                    task_name = parts[0].lstrip("\\").strip()
                    task_name_with_extension = f"{task_name}.exe"

                    if task_name_with_extension.lower() in [exe_file.lower() for exe_file in exe_files]:
                        row_position = self.table.rowCount()
                        self.table.insertRow(row_position)

                        # Ajouter les colonnes
                        for j, data in enumerate([str(i + 1)] + parts[:3]):
                            self.table.setItem(row_position, j, QTableWidgetItem(data))

                        # Ajouter un bouton d'action
                        action_button = QtWidgets.QPushButton(self.tr("⚙️ Action"))
                        action_button.clicked.connect(lambda _, name=parts[0]: self.modify_or_delete_activity(name))
                        self.table.setCellWidget(row_position, 6, action_button)
                except Exception as e:
                    QMessageBox.warning(self, self.tr("Warning"), self.tr(f"Error processing task: {e}"))

        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), self.tr(f"Error loading activities: {e}"))

    def add_activity(self):
        """Ajoute une nouvelle activité planifiée."""
        folder_path = os.path.expanduser("~\\AppData\\Roaming\\Saadiya\\resources\\tools")
        exe_files = [os.path.splitext(f)[0] for f in os.listdir(folder_path) if f.endswith(".exe")]

        dialog = AddActivityDialog(exe_files)
        if dialog.exec_() == QDialog.Accepted:
            name, program, daily, days, time, specific_dates = dialog.get_activity_data()
            program_path = os.path.join(folder_path, f"{program}.exe")

            if specific_dates:
                # Si des dates spécifiques sont sélectionnées, planifier pour ces dates
                for date in specific_dates:
                    try:
                        cmd = (
                            f'schtasks /create /tn "{name}_{date}" /tr "{program_path}" '
                            f'/SC ONCE /SD {date} /ST {time} /f'
                        )
                        subprocess.run(cmd, shell=True)
                    except Exception as e:
                        QMessageBox.critical(self, self.tr("Error"), self.tr(f"Error scheduling activity: {e}"))
            else:
                # Sinon, utiliser le planning quotidien ou hebdomadaire
                schedule_type = "/SC DAILY" if daily else "/SC WEEKLY"
                date_flag = "" if daily else f" /D {','.join(days)}"

                try:
                    cmd = (
                        f'schtasks /create /tn "{name}" /tr "{program_path}" '
                        f'{schedule_type} {date_flag} /st {time} /f'
                    )
                    subprocess.run(cmd, shell=True)
                except Exception as e:
                    QMessageBox.critical(self, self.tr("Error"), self.tr(f"Error scheduling activity: {e}"))

            QMessageBox.information(self, self.tr("Success"), self.tr("Activity scheduled successfully!"))
            self.load_activities()

    def search_activities(self):
        """Filtre les activités en fonction de la recherche."""
        query = self.search_entry.text().lower()
        for row in range(self.table.rowCount()):
            match = any(query in (self.table.item(row, col).text().lower() if self.table.item(row, col) else "") 
                        for col in range(self.table.columnCount()))
            self.table.setRowHidden(row, not match)

    def modify_or_delete_activity(self, name):
        """Affiche un menu pour modifier ou supprimer une activité."""
        menu = QtWidgets.QMenu()
        modify_action = menu.addAction(self.tr("✏️ Modify"))
        delete_action = menu.addAction(self.tr("❌ Delete"))

        action = menu.exec_(QtGui.QCursor.pos())
        if action == modify_action:
            self.modify_activity(name)
        elif action == delete_action:
            self.delete_activity(name)

    def delete_activity(self, name):
        """Supprime une activité planifiée."""
        reply = QMessageBox.question(
            self,
            self.tr("Confirmation"),
            self.tr(f"Are you sure you want to delete the activity '{name}'?"),
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            try:
                subprocess.run(f'schtasks /delete /tn "{name}" /f', shell=True)
                QMessageBox.information(self, self.tr("Success"), self.tr(f"Activity {name} deleted successfully!"))
                self.load_activities()
            except Exception as e:
                QMessageBox.critical(self, self.tr("Error"), self.tr(f"Error deleting activity: {e}"))

    def modify_activity(self, name):
        """Modifie une activité planifiée."""
        # Récupérer les détails de l'activité
        try:
            result = subprocess.check_output(f'schtasks /query /tn "{name}" /fo list', shell=True, encoding="utf-8", errors="ignore")
            details = result.strip().splitlines()
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, self.tr("Error"), self.tr(f"Failed to retrieve task details: {e}"))
            return

        # Créer une boîte de dialogue pour la modification
        dialog = AddActivityDialog(self.get_exe_files())
        if dialog.exec_() == QDialog.Accepted:
            new_name, program, daily, days, time, specific_dates = dialog.get_activity_data()
            program_path = os.path.join(self.get_tools_folder(), f"{program}.exe")

            try:
                # Supprimer l'ancienne tâche
                subprocess.run(f'schtasks /delete /tn "{name}" /f', shell=True)

                # Créer la nouvelle tâche
                if specific_dates:
                    for date in specific_dates:
                        cmd = (
                            f'schtasks /create /tn "{new_name}_{date}" /tr "{program_path}" '
                            f'/SC ONCE /SD {date} /ST {time} /f'
                        )
                        subprocess.run(cmd, shell=True)
                else:
                    schedule_type = "/SC DAILY" if daily else "/SC WEEKLY"
                    date_flag = "" if daily else f" /D {','.join(days)}"

                    cmd = (
                        f'schtasks /create /tn "{new_name}" /tr "{program_path}" '
                        f'{schedule_type} {date_flag} /st {time} /f'
                    )
                    subprocess.run(cmd, shell=True)

                QMessageBox.information(self, self.tr("Success"), self.tr("Activity modified successfully!"))
                self.load_activities()
            except Exception as e:
                QMessageBox.critical(self, self.tr("Error"), self.tr(f"Error modifying activity: {e}"))

    def export_activities(self):
        """Exporte les activités planifiées dans un fichier CSV."""
        try:
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, self.tr("Export Activities"), "", "CSV Files (*.csv)")
            if file_path:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write("Number,Name,Program,Days,Time,Date\n")
                    for row in range(self.table.rowCount()):
                        row_data = [
                            self.table.item(row, col).text() if self.table.item(row, col) else ""
                            for col in range(self.table.columnCount() - 1)
                        ]
                        file.write(",".join(row_data) + "\n")
                QMessageBox.information(self, self.tr("Success"), self.tr("Activities exported successfully!"))
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), self.tr(f"Error exporting activities: {e}"))

    def pause_selected_activities(self):
        """Met en pause les activités sélectionnées."""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, self.tr("Warning"), self.tr("Please select activities to pause."))
            return

        for row in selected_rows:
            activity_name = self.table.item(row.row(), 1).text()
            try:
                subprocess.run(f'schtasks /change /tn "{activity_name}" /disable', shell=True)
            except Exception as e:
                QMessageBox.critical(self, self.tr("Error"), self.tr(f"Error pausing activity {activity_name}: {e}"))

        QMessageBox.information(self, self.tr("Success"), self.tr("Selected activities paused successfully!"))
        self.load_activities()

    def delete_selected_activities(self):
        """Supprime les activités sélectionnées."""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, self.tr("Warning"), self.tr("Please select activities to delete."))
            return

        for row in selected_rows:
            activity_name = self.table.item(row.row(), 1).text()
            try:
                subprocess.run(f'schtasks /delete /tn "{activity_name}" /f', shell=True)
            except Exception as e:
                QMessageBox.critical(self, self.tr("Error"), self.tr(f"Error deleting activity {activity_name}: {e}"))

        QMessageBox.information(self, self.tr("Success"), self.tr("Selected activities deleted successfully!"))
        self.load_activities()
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Activite()
    window.show()
    sys.exit(app.exec_())