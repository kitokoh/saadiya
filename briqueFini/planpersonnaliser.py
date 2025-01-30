import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QCalendarWidget, QTimeEdit, QFileDialog, QMessageBox, QListWidget, QComboBox, QProgressBar
from PyQt5.QtCore import QDateTime, QTimer, QDate, QTime, QThread, pyqtSignal
import subprocess
import csv


class SchedulerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.db_init()

    def initUI(self):
        self.setWindowTitle('Planificateur d\'exécution')
        self.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout()

        self.calendar = QCalendarWidget(self)
        layout.addWidget(self.calendar)

        self.time_edit = QTimeEdit(self)
        self.time_edit.setTime(QDateTime.currentDateTime().time())
        layout.addWidget(self.time_edit)

        self.label = QLabel('Sélectionnez une date et une heure, puis cliquez sur "Planifier"', self)
        layout.addWidget(self.label)

        self.schedule_button = QPushButton('Planifier', self)
        self.schedule_button.clicked.connect(self.schedule_task)
        layout.addWidget(self.schedule_button)

        self.import_button = QPushButton('Importer des dates', self)
        self.import_button.clicked.connect(self.import_dates)
        layout.addWidget(self.import_button)

        self.export_button = QPushButton('Exporter les tâches en CSV', self)
        self.export_button.clicked.connect(self.export_to_csv)
        layout.addWidget(self.export_button)

        self.delete_button = QPushButton('Supprimer une tâche', self)
        self.delete_button.clicked.connect(self.delete_task)
        layout.addWidget(self.delete_button)

        self.modify_button = QPushButton('Modifier une tâche', self)
        self.modify_button.clicked.connect(self.modify_task)
        layout.addWidget(self.modify_button)

        self.file_button = QPushButton('Sélectionner le fichier .exe', self)
        self.file_button.clicked.connect(self.select_exe_file)
        layout.addWidget(self.file_button)

        self.scheduled_tasks_list = QListWidget(self)
        layout.addWidget(self.scheduled_tasks_list)

        self.priority_combo = QComboBox(self)
        self.priority_combo.addItems(["Haute", "Moyenne", "Basse"])
        layout.addWidget(self.priority_combo)

        self.recurrence_combo = QComboBox(self)
        self.recurrence_combo.addItems(["Aucune", "Quotidienne", "Hebdomadaire", "Mensuelle"])
        layout.addWidget(self.recurrence_combo)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_schedule)
        self.timer.start(1000)  # Vérifie toutes les secondes

        self.scheduled_tasks = []
        self.exe_path = ""

    def db_init(self):
        """Initialiser la base de données SQLite pour stocker les tâches"""
        self.conn = sqlite3.connect('tasks.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                datetime TEXT,
                                priority TEXT,
                                recurrence TEXT,
                                exe_path TEXT)''')
        self.conn.commit()

    def db_save_task(self, scheduled_datetime, priority, recurrence):
        """Sauvegarder la tâche dans la base de données"""
        self.cursor.execute("INSERT INTO tasks (datetime, priority, recurrence, exe_path) VALUES (?, ?, ?, ?)",
                            (scheduled_datetime.toString("yyyy-MM-dd HH:mm"), priority, recurrence, self.exe_path))
        self.conn.commit()

    def schedule_task(self):
        selected_date = self.calendar.selectedDate()
        selected_time = self.time_edit.time()
        scheduled_datetime = QDateTime(selected_date, selected_time)

        if scheduled_datetime < QDateTime.currentDateTime():
            QMessageBox.warning(self, 'Erreur', 'La date et l\'heure sélectionnées sont déjà passées.')
            return

        priority = self.priority_combo.currentText()
        recurrence = self.recurrence_combo.currentText()

        self.scheduled_tasks.append({'datetime': scheduled_datetime, 'priority': priority, 'recurrence': recurrence})
        self.scheduled_tasks_list.addItem(f'Tâche planifiée pour le {scheduled_datetime.toString("dd/MM/yyyy HH:mm")} - Priorité: {priority} - Répétition: {recurrence}')
        self.db_save_task(scheduled_datetime, priority, recurrence)

        self.label.setText(f'Tâche planifiée pour le {scheduled_datetime.toString("dd/MM/yyyy HH:mm")}')

    def import_dates(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Importer des dates", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            with open(file_name, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    date_str = row[0]
                    date = QDate.fromString(date_str, "dd/MM/yyyy")
                    if date.isValid():
                        scheduled_datetime = QDateTime(date, self.time_edit.time())
                        self.scheduled_tasks.append({'datetime': scheduled_datetime, 'priority': 'Moyenne', 'recurrence': 'Aucune'})
                        self.scheduled_tasks_list.addItem(f'Tâche importée pour le {scheduled_datetime.toString("dd/MM/yyyy HH:mm")}')
                    else:
                        QMessageBox.warning(self, 'Erreur', f'Date invalide dans le fichier CSV: {date_str}')

    def export_to_csv(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Exporter les tâches en CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Date et Heure', 'Priorité', 'Répétition', 'Exécutable'])
                for task in self.scheduled_tasks:
                    writer.writerow([task['datetime'].toString("dd/MM/yyyy HH:mm"), task['priority'], task['recurrence'], self.exe_path])
            QMessageBox.information(self, 'Exportation', 'Tâches exportées avec succès.')

    def select_exe_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier .exe", "", "Executable Files (*.exe);;All Files (*)", options=options)
        if file_name:
            self.exe_path = file_name
            QMessageBox.information(self, 'Fichier sélectionné', f'Fichier .exe sélectionné: {file_name}')

    def delete_task(self):
        selected_item = self.scheduled_tasks_list.currentItem()
        if selected_item:
            task_index = self.scheduled_tasks_list.row(selected_item)
            self.scheduled_tasks.pop(task_index)
            self.scheduled_tasks_list.takeItem(task_index)
            QMessageBox.information(self, 'Suppression', 'Tâche supprimée avec succès.')
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez sélectionner une tâche à supprimer.')

    def modify_task(self):
        selected_item = self.scheduled_tasks_list.currentItem()
        if selected_item:
            task_index = self.scheduled_tasks_list.row(selected_item)
            selected_datetime_str = selected_item.text().split(' pour le ')[1]
            scheduled_datetime = QDateTime.fromString(selected_datetime_str, "dd/MM/yyyy HH:mm")

            new_date, new_time = self.get_new_datetime(scheduled_datetime)
            if new_date and new_time:
                new_scheduled_datetime = QDateTime(new_date, new_time)
                self.scheduled_tasks[task_index]['datetime'] = new_scheduled_datetime
                self.scheduled_tasks_list.item(task_index).setText(f'Tâche modifiée pour le {new_scheduled_datetime.toString("dd/MM/yyyy HH:mm")}')
                QMessageBox.information(self, 'Modification', 'Tâche modifiée avec succès.')
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez sélectionner une tâche à modifier.')

    def get_new_datetime(self, current_datetime):
        """Méthode pour obtenir une nouvelle date et heure modifiées"""
        selected_date = self.calendar.selectedDate()
        selected_time = self.time_edit.time()
        if selected_date != current_datetime.date() or selected_time != current_datetime.time():
            return selected_date, selected_time
        return None, None

    def check_schedule(self):
        current_datetime = QDateTime.currentDateTime()
        for task in self.scheduled_tasks:
            task_time = task['datetime']
            if current_datetime >= task_time:
                self.execute_exe(task)
                self.scheduled_tasks.remove(task)

    def execute_exe(self, task):
        if not self.exe_path:
            QMessageBox.warning(self, 'Erreur', 'Aucun fichier .exe sélectionné.')
            return

        reply = QMessageBox.question(self, 'Confirmation', f'Voulez-vous exécuter le programme à {task["datetime"].toString("dd/MM/yyyy HH:mm")} ?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                process_thread = ProcessExecutionThread(self.exe_path, self.progress_bar)
                process_thread.start()
                process_thread.finished.connect(lambda: QMessageBox.information(self, 'Exécution', 'Le programme a été exécuté avec succès.'))
            except Exception as e:
                QMessageBox.critical(self, 'Erreur', f'Erreur lors de l\'exécution du programme: {str(e)}')


class ProcessExecutionThread(QThread):
    finished = pyqtSignal()

    def __init__(self, exe_path, progress_bar):
        super().__init__()
        self.exe_path = exe_path
        self.progress_bar = progress_bar

    def run(self):
        # Simuler une exécution de programme avec progression
        for i in range(101):
            self.sleep(1)  # Simuler le temps d'exécution
            self.progress_bar.setValue(i)
        subprocess.Popen(self.exe_path)
        self.finished.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SchedulerApp()
    ex.show()
    sys.exit(app.exec_())
