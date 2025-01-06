from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QCheckBox, QDialog
import subprocess
import os

class AddActivityDialog(QtWidgets.QDialog):
    def __init__(self, exe_files):
        super().__init__()
        self.setWindowTitle("Programmer une Activité")
        self.setFixedSize(400, 300)
        self.setLayout(QtWidgets.QVBoxLayout())

        # Widgets
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Nom du programme")
        self.name_input.setReadOnly(True)  # Nom basé sur le fichier sélectionné

        self.program_input = QtWidgets.QComboBox()
        self.program_input.addItems(exe_files)
        self.program_input.currentIndexChanged.connect(self.update_name)

        self.daily_checkbox = QtWidgets.QCheckBox("Exécution quotidienne")
        self.days_group = QtWidgets.QGroupBox("Jours spécifiques")
        self.days_layout = QtWidgets.QHBoxLayout()
        self.day_checkboxes = []
        for day in ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]:
            checkbox = QCheckBox(day)
            self.day_checkboxes.append(checkbox)
            self.days_layout.addWidget(checkbox)
        self.days_group.setLayout(self.days_layout)

        self.time_input = QtWidgets.QTimeEdit()
        self.time_input.setDisplayFormat("HH:mm")

        save_button = QtWidgets.QPushButton("Sauvegarder")
        save_button.clicked.connect(self.accept)

        # Layout
        layout = self.layout()
        layout.addWidget(QtWidgets.QLabel("Programme :"))
        layout.addWidget(self.program_input)
        layout.addWidget(QtWidgets.QLabel("Nom :"))
        layout.addWidget(self.name_input)
        layout.addWidget(self.daily_checkbox)
        layout.addWidget(self.days_group)
        layout.addWidget(QtWidgets.QLabel("Heure d'exécution :"))
        layout.addWidget(self.time_input)
        layout.addWidget(save_button)

        self.update_name()

    def update_name(self):
        self.name_input.setText(self.program_input.currentText())

    def get_activity_data(self):
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
        self.setWindowTitle("Gestionnaire d'Activités Programmées")
        self.setStyleSheet(self._get_styles())
        self.resize(1000, 700)

        # Titre principal
        title_label = QtWidgets.QLabel("Activités Programmées")
        title_label.setAlignment(QtCore.Qt.AlignCenter)

        # Barre de recherche et boutons
        self.search_entry = QtWidgets.QLineEdit()
        self.search_entry.setPlaceholderText("Rechercher une activité...")
        
        search_button = QtWidgets.QPushButton("Rechercher")
        search_button.clicked.connect(self.search_activities)

        add_button = QtWidgets.QPushButton("Programmer une Activité")
        add_button.clicked.connect(self.add_activity)

        pause_button = QtWidgets.QPushButton("Mettre en Pause")
        pause_button.clicked.connect(self.pause_selected_activities)

        delete_button = QtWidgets.QPushButton("Supprimer")
        delete_button.clicked.connect(self.delete_selected_activities)

        refresh_button = QtWidgets.QPushButton("Charger les Activités")
        refresh_button.clicked.connect(self.load_activities)

        # Layout pour la barre de recherche et les boutons
        top_bar_layout = QtWidgets.QHBoxLayout()
        top_bar_layout.addWidget(self.search_entry)
        top_bar_layout.addWidget(search_button)
        top_bar_layout.addWidget(add_button)
        top_bar_layout.addWidget(pause_button)
        top_bar_layout.addWidget(delete_button)
        top_bar_layout.addWidget(refresh_button)

        # Tableau des activités
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Numéro", "Nom", "Programme", "Jours", "Heure", "Action"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSortingEnabled(True)

        # Disposition principale
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(title_label)
        main_layout.addLayout(top_bar_layout)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

        # Charger les activités programmées au démarrage
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
        Charge et affiche les activités programmées dont le programme correspond
        à un fichier .exe présent dans le dossier tools.
        """
        print("Début de load_activities")
        self.table.setRowCount(0)  # Réinitialiser la table

        try:
            # Obtenir le chemin du dossier contenant les fichiers .exe
            folder_path = os.path.expanduser("~\\AppData\\Roaming\\Saadiya\\resources\\tools")
            print(f"Chemin du dossier tools : {folder_path}")

            if not os.path.exists(folder_path):
                print(f"Erreur : Le dossier {folder_path} n'existe pas.")
                QMessageBox.critical(self, "Erreur", f"Le dossier {folder_path} n'existe pas.")
                return

            # Lister les fichiers .exe dans le dossier
            exe_files = [f for f in os.listdir(folder_path) if f.endswith(".exe")]
            print(f"Fichiers .exe trouvés : {exe_files}")

            if not exe_files:
                QMessageBox.warning(self, "Avertissement", "Aucun fichier .exe trouvé dans le dossier tools.")
                print("Aucun fichier .exe trouvé dans le dossier tools.")
                return

            # Exécuter la commande pour récupérer les tâches programmées
            print("Exécution de la commande schtasks pour récupérer les tâches programmées...")
            try:
                result = subprocess.check_output("schtasks /query /fo csv /nh", shell=True, text=True)
            except subprocess.CalledProcessError as e:
                print(f"Erreur lors de l'exécution de schtasks : {e}")
                QMessageBox.critical(self, "Erreur", "Impossible d'exécuter la commande schtasks.")
                return

            lines = result.strip().splitlines()
            print(f"Nombre de tâches récupérées : {len(lines)}")

            if not lines:
                print("Aucune tâche trouvée.")
                QMessageBox.information(self, "Info", "Aucune tâche planifiée trouvée.")
                return

            # Analyse des lignes retournées
            for i, line in enumerate(lines):
                print(f"Analyse de la tâche {i + 1}: {line}")

                # Diviser les données CSV en colonnes
                parts = [p.strip('"') for p in line.split(",")]
                print(f"Colonnes extraites : {parts}")

                # Vérifier qu'il y a au moins 3 colonnes (nom, date/heure, état)
                if len(parts) < 3:
                    print(f"Tâche {i + 1} ignorée : format incorrect (moins de 3 colonnes).")
                    continue

                # Nettoyer la première colonne (nom de la tâche)
                task_name = parts[0].lstrip("\\").strip()  # Supprimer le préfixe '\\'
                print(f"Nom de la tâche nettoyé : {task_name}")

                # Ajouter l'extension .exe pour la comparaison
                task_name_with_extension = f"{task_name}.exe"
                print(f"Nom de la tâche avec extension : {task_name_with_extension}")

                # Vérifier si le nom de la tâche avec .exe correspond à un fichier .exe
                if task_name_with_extension.lower() in [exe_file.lower() for exe_file in exe_files]:
                    print(f"Tâche correspondante trouvée : {task_name_with_extension}")

                    # Ajouter une nouvelle ligne au tableau pour cette tâche
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)

                    # Ajouter les colonnes dans la ligne (au moins les 3 premières colonnes disponibles)
                    for j, data in enumerate([str(i + 1)] + parts[:3]):  # Numéro + colonnes disponibles
                        print(f"Ajout de la donnée dans la table : {data}")
                        self.table.setItem(row_position, j, QTableWidgetItem(data))

                    # Ajouter un bouton d'action
                    action_button = QtWidgets.QPushButton("Action")
                    action_button.clicked.connect(lambda _, name=parts[0]: self.modify_or_delete_activity(name))
                    self.table.setCellWidget(row_position, 5, action_button)
                else:
                    print(f"Tâche ignorée (ne correspond pas à un fichier .exe) : {task_name}")

        except Exception as e:
            print(f"Erreur inattendue : {e}")
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement des activités : {e}")

        print("Fin de load_activities")


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
                QMessageBox.information(self, "Succès", "Activité programmée avec succès !")
                self.load_activities()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la programmation : {e}")

    def search_activities(self):
        query = self.search_entry.text().lower()
        for row in range(self.table.rowCount()):
            match = any(query in (self.table.item(row, col).text().lower() if self.table.item(row, col) else "") for col in range(self.table.columnCount()))
            self.table.setRowHidden(row, not match)

    def modify_or_delete_activity(self, name):
        menu = QtWidgets.QMenu()
        modify_action = menu.addAction("Modifier")
        delete_action = menu.addAction("Supprimer")

        action = menu.exec_(QtGui.QCursor.pos())
        if action == modify_action:
            QMessageBox.information(self, "Modification", f"Modifier l'activité {name}")
        elif action == delete_action:
            self.delete_activity(name)

    def delete_activity(self, name):
        try:
            subprocess.run(f'schtasks /delete /tn "{name}" /f', shell=True)
            QMessageBox.information(self, "Succès", f"Activité {name} supprimée avec succès !")
            self.load_activities()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression de l'activité : {e}")








    def modify_activity(self, name):
        QMessageBox.information(self, "Modification", f"Modifier l'activité {name}")


    def pause_selected_activities(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Avertissement", "Veuillez sélectionner des activités à mettre en pause.")
            return

        for row in selected_rows:
            activity_name = self.table.item(row.row(), 1).text()
            try:
                subprocess.run(f'schtasks /change /tn "{activity_name}" /disable', shell=True)
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la mise en pause de l'activité {activity_name} : {e}")

        QMessageBox.information(self, "Succès", "Les activités sélectionnées ont été mises en pause avec succès !")
        self.load_activities()

    def delete_selected_activities(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Avertissement", "Veuillez sélectionner des activités à supprimer.")
            return

        for row in selected_rows:
            activity_name = self.table.item(row.row(), 1).text()
            try:
                subprocess.run(f'schtasks /delete /tn "{activity_name}" /f', shell=True)
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression de l'activité {activity_name} : {e}")

        QMessageBox.information(self, "Succès", "Les activités sélectionnées ont été supprimées avec succès !")
        self.load_activities()





    def get_exe_files(self):
        folder_path = os.path.expanduser("~\\AppData\\Roaming\\Saadiya\\resources\\tools")
        exe_files = [f for f in os.listdir(folder_path) if f.endswith(".exe")]
        return {exe: os.path.splitext(exe)[0].capitalize() for exe in exe_files}


    def show_action_menu(self, row):
        activity_name = self.table.item(row, 2).text()
        menu = QtWidgets.QMenu()
        modify_action = menu.addAction("Modifier")
        delete_action = menu.addAction("Supprimer")

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
