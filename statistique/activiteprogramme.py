import os
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QCheckBox, QDialog

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QPushButton, QMenu, QAction, QGraphicsDropShadowEffect

from PyQt5.QtGui import QColor, QFont


class AddActivityDialog(QtWidgets.QDialog):
    def __init__(self, exe_files):
        super().__init__()
        self.setWindowTitle(self.tr("Schedule an Activity"))
        self.setFixedSize(450, 350)
        self.setWindowIcon(QtGui.QIcon("resources/icons/schedule.ico"))  # Ajoutez une icône personnalisée si nécessaire

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
            QLineEdit, QComboBox, QTimeEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus, QTimeEdit:focus {
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
        """)

        # Widgets
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText(self.tr("Program Name"))
        self.name_input.setReadOnly(True)

        self.program_input = QtWidgets.QComboBox()
        self.program_input.addItems(exe_files)
        self.program_input.currentIndexChanged.connect(self.update_name)

        self.daily_checkbox = QtWidgets.QCheckBox(self.tr("Execute Daily"))

        self.days_group = QtWidgets.QGroupBox(self.tr("Select Specific Days"))
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

        save_button = QtWidgets.QPushButton(self.tr("Save"))
        save_button.clicked.connect(self.accept)

        # Layout principal
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)

                # Ajout des widgets
        main_layout.addWidget(self.create_form_group("Program:", self.program_input))
        main_layout.addWidget(self.create_form_group("Name:", self.name_input))
        main_layout.addWidget(self.daily_checkbox)
        main_layout.addWidget(self.days_group)
        main_layout.addWidget(self.create_form_group("Execution Time:", self.time_input))

        main_layout.addWidget(save_button, alignment=QtCore.Qt.AlignRight)

        self.setLayout(main_layout)

        # Mettre à jour le nom initial
        self.update_name()

    # def create_form_group(self, label_text, widget):
    #     """Crée une ligne de formulaire avec une étiquette et un widget."""
    #     form_layout = QtWidgets.QHBoxLayout()
    #     form_layout.addWidget(QtWidgets.QLabel(label_text))
    #     form_layout.addWidget(widget)
    #     return form_layout
    def create_form_group(self, label_text, widget):
        """Crée une ligne de formulaire avec une étiquette et un widget dans un QWidget."""
        container = QtWidgets.QWidget()
        form_layout = QtWidgets.QHBoxLayout(container)
        form_layout.setContentsMargins(0, 0, 0, 0)  # Enlever les marges internes
        form_layout.addWidget(QtWidgets.QLabel(label_text))
        form_layout.addWidget(widget)
        return container

    def update_name(self):
        """Met à jour le champ du nom basé sur le fichier sélectionné."""
        self.name_input.setText(self.program_input.currentText())

    def get_activity_data(self):
        """Retourne les données saisies par l'utilisateur."""
        selected_days = [checkbox.text() for checkbox in self.day_checkboxes if checkbox.isChecked()]
        return (
            self.name_input.text(),
            self.program_input.currentText(),
            self.daily_checkbox.isChecked(),
            selected_days,
            self.time_input.time().toString("HH:mm")
        )

class Activite(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr("Scheduled Activities Manager"))
        self.setStyleSheet(self._get_styles())
        self.resize(1000, 700)

        # Main title
        title_label = QtWidgets.QLabel(self.tr("Scheduled Activities"))
        title_label.setAlignment(QtCore.Qt.AlignCenter)


        # Search bar and buttons
        self.search_entry = QtWidgets.QLineEdit()
        self.search_entry.setPlaceholderText(self.tr("Search an activity..."))

        search_button = QtWidgets.QPushButton(self.tr("Search"))
        search_button.clicked.connect(self.search_activities)

        add_button = QtWidgets.QPushButton(self.tr("Schedule an Activity"))
        add_button.clicked.connect(self.add_activity)
        # Add a glowing shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 212, 255))  # Neon blue
        shadow.setOffset(0, 5)
        add_button.setGraphicsEffect(shadow)

        pause_button = QtWidgets.QPushButton(self.tr("Pause"))
        pause_button.clicked.connect(self.pause_selected_activities)

        delete_button = QtWidgets.QPushButton(self.tr("Delete"))
        delete_button.clicked.connect(self.delete_selected_activities)

        refresh_button = QtWidgets.QPushButton(self.tr("Load Activities"))
        refresh_button.clicked.connect(self.load_activities)

        # Layout for the search bar and buttons
        top_bar_layout = QtWidgets.QHBoxLayout()
        top_bar_layout.addWidget(self.search_entry)
        top_bar_layout.addWidget(search_button)
        top_bar_layout.addWidget(add_button)
        top_bar_layout.addWidget(pause_button)
        top_bar_layout.addWidget(delete_button)
        top_bar_layout.addWidget(refresh_button)

        # Activities table
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            self.tr("Number"), self.tr("Name"), self.tr("Program"), self.tr("Days"), self.tr("Time"), self.tr("Action")
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSortingEnabled(True)

        # Main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(title_label)
        main_layout.addLayout(top_bar_layout)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

        # Load scheduled activities on startup
        QtCore.QTimer.singleShot(100, self.load_activities)

    def _get_styles(self):
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
        """
        Load and display scheduled activities whose program matches
        an .exe file in the tools folder.
        """
        print("Starting load_activities")
        self.table.setRowCount(0)  # Reset the table

        try:
            # Get the path to the folder containing the .exe files
            folder_path = os.path.expanduser("~\\AppData\\Roaming\\Saadiya\\resources\\tools")
            print(f"Tools folder path: {folder_path}")

            if not os.path.exists(folder_path):
                print(f"Error: The folder {folder_path} does not exist.")
                QMessageBox.critical(self, self.tr("Error"), self.tr(f"The folder {folder_path} does not exist."))
                return

            # List .exe files in the folder
            exe_files = [f for f in os.listdir(folder_path) if f.endswith(".exe")]
            print(f".exe files found: {exe_files}")

            if not exe_files:
                QMessageBox.warning(self, self.tr("Warning"), self.tr("No .exe files found in the tools folder."))
                print("No .exe files found in the tools folder.")
                return

            # Execute the command to retrieve scheduled tasks
            print("Executing schtasks command to retrieve scheduled tasks...")
            try:
                result = subprocess.check_output("schtasks /query /fo csv /nh", shell=True, text=True)
            except subprocess.CalledProcessError as e:
                print(f"Error executing schtasks: {e}")
                QMessageBox.critical(self, self.tr("Error"), self.tr("Failed to execute schtasks command."))
                return

            lines = result.strip().splitlines()
            print(f"Number of tasks retrieved: {len(lines)}")

            if not lines:
                print("No tasks found.")
                QMessageBox.information(self, self.tr("Info"), self.tr("No scheduled tasks found."))
                return

            # Analyze the returned lines
            for i, line in enumerate(lines):
                print(f"Analyzing task {i + 1}: {line}")

                # Split CSV data into columns
                parts = [p.strip('"') for p in line.split(",")]
                print(f"Extracted columns: {parts}")

                # Ensure there are at least 3 columns (name, date/time, status)
                if len(parts) < 3:
                    print(f"Task {i + 1} ignored: incorrect format (less than 3 columns).")
                    continue

                # Clean the first column (task name)
                task_name = parts[0].lstrip("\\").strip()  # Remove the '\\' prefix
                print(f"Cleaned task name: {task_name}")

                # Add .exe extension for comparison
                task_name_with_extension = f"{task_name}.exe"
                print(f"Task name with extension: {task_name_with_extension}")

                # Check if the task name with .exe matches an .exe file
                if task_name_with_extension.lower() in [exe_file.lower() for exe_file in exe_files]:
                    print(f"Matching task found: {task_name_with_extension}")

                    # Add a new row to the table for this task
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)

                    # Add columns to the row (at least the first 3 available columns)
                    for j, data in enumerate([str(i + 1)] + parts[:3]):  # Number + available columns
                        print(f"Adding data to table: {data}")
                        self.table.setItem(row_position, j, QTableWidgetItem(data))

                    # Add an action button
                    action_button = QtWidgets.QPushButton(self.tr("Action"))
                    action_button.clicked.connect(lambda _, name=parts[0]: self.modify_or_delete_activity(name))
                    self.table.setCellWidget(row_position, 5, action_button)
                else:
                    print(f"Task ignored (does not match an .exe file): {task_name}")

        except Exception as e:
            print(f"Unexpected error: {e}")
            QMessageBox.critical(self, self.tr("Error"), self.tr(f"Error loading activities: {e}"))

        print("End of load_activities")

    def add_activity(self):
        folder_path = os.path.expanduser("~\\AppData\\Roaming\\Saadiya\\resources\\tools")
        exe_files = [os.path.splitext(f)[0] for f in os.listdir(folder_path) if f.endswith(".exe")]

        dialog = AddActivityDialog(exe_files)
        if dialog.exec_() == QDialog.Accepted:
            name, program, daily, days, time = dialog.get_activity_data()
            program_path = os.path.join(folder_path, f"{program}.exe")

            schedule_type = "/SC DAILY" if daily else "/SC WEEKLY"
            days_flag = "" if daily else f" /D {','.join(days)}"

            try:
                cmd = (
                    f'schtasks /create /tn "{name}" /tr "{program_path}" '
                    f'{schedule_type} {days_flag} /st {time} /f'
                )
                subprocess.run(cmd, shell=True)
                QMessageBox.information(self, self.tr("Success"), self.tr("Activity scheduled successfully!"))
                self.load_activities()
            except Exception as e:
                QMessageBox.critical(self, self.tr("Error"), self.tr(f"Error scheduling activity: {e}"))

    def search_activities(self):
        query = self.search_entry.text().lower()
        for row in range(self.table.rowCount()):
            match = any(query in (self.table.item(row, col).text().lower() if self.table.item(row, col) else "") for col in range(self.table.columnCount()))
            self.table.setRowHidden(row, not match)

    def modify_or_delete_activity(self, name):
        menu = QtWidgets.QMenu()
        modify_action = menu.addAction(self.tr("Modify"))
        delete_action = menu.addAction(self.tr("Delete"))

        action = menu.exec_(QtGui.QCursor.pos())
        if action == modify_action:
            QMessageBox.information(self, self.tr("Modify"), self.tr(f"Modify activity {name}"))
        elif action == delete_action:
            self.delete_activity(name)

    def delete_activity(self, name):
        try:
            subprocess.run(f'schtasks /delete /tn "{name}" /f', shell=True)
            QMessageBox.information(self, self.tr("Success"), self.tr(f"Activity {name} deleted successfully!"))
            self.load_activities()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), self.tr(f"Error deleting activity: {e}"))

    def modify_activity(self, name):
        QMessageBox.information(self, self.tr("Modify"), self.tr(f"Modify activity {name}"))

    def pause_selected_activities(self):
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

    def get_exe_files(self):
        folder_path = os.path.expanduser("~\\AppData\\Roaming\\Saadiya\\resources\\tools")
        exe_files = [f for f in os.listdir(folder_path) if f.endswith(".exe")]
        return {exe: os.path.splitext(exe)[0].capitalize() for exe in exe_files}

    def show_action_menu(self, row):
        activity_name = self.table.item(row, 2).text()
        menu = QtWidgets.QMenu()
        modify_action = menu.addAction(self.tr("Modify"))
        delete_action = menu.addAction(self.tr("Delete"))

        action = menu.exec_(QtGui.QCursor.pos())
        if action == modify_action:
            self.modify_activity(activity_name)
        elif action == delete_action:
            self.delete_activity(activity_name)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Activite()
    window.show()
    sys.exit(app.exec_())