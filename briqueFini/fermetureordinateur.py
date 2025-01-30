import sys
import subprocess
import platform
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTimeEdit, QCalendarWidget, QMessageBox, QProgressBar, QTimer
from PyQt5.QtCore import QDateTime, QTime, QDate, QTimer
from PyQt5.QtGui import QIcon


class ShutdownApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Éteindre l\'ordinateur')
        self.setGeometry(100, 100, 450, 350)
        self.setWindowIcon(QIcon('shutdown_icon.png'))  # Ajout d'une icône personnalisée

        layout = QVBoxLayout()

        # Label de titre
        self.label = QLabel('Sélectionnez une heure pour éteindre l\'ordinateur:', self)
        layout.addWidget(self.label)

        # Sélection de l'heure d'arrêt
        self.time_edit = QTimeEdit(self)
        self.time_edit.setTime(QTime.currentTime())
        layout.addWidget(self.time_edit)

        # Sélection de la date (facultatif)
        self.calendar = QCalendarWidget(self)
        layout.addWidget(self.calendar)

        # Layout horizontal pour les boutons
        h_layout = QHBoxLayout()

        # Boutons
        self.schedule_button = QPushButton('Programmer l\'arrêt', self)
        self.schedule_button.clicked.connect(self.schedule_shutdown)
        h_layout.addWidget(self.schedule_button)

        self.shutdown_button = QPushButton('Éteindre maintenant', self)
        self.shutdown_button.clicked.connect(self.shutdown_now)
        h_layout.addWidget(self.shutdown_button)

        self.cancel_button = QPushButton('Annuler l\'arrêt', self)
        self.cancel_button.clicked.connect(self.cancel_shutdown)
        self.cancel_button.setEnabled(False)  # Désactiver le bouton d'annulation au départ
        h_layout.addWidget(self.cancel_button)

        layout.addLayout(h_layout)

        # ProgressBar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

        # Timer pour vérifier si l'heure est arrivée
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_schedule)
        self.timer.start(1000)  # Vérifie toutes les secondes

        self.scheduled_shutdown = None

    def schedule_shutdown(self):
        """Programmer l'arrêt de l'ordinateur à l'heure sélectionnée"""
        selected_time = self.time_edit.time()
        selected_date = self.calendar.selectedDate()
        scheduled_datetime = QDateTime(selected_date, selected_time)

        if scheduled_datetime < QDateTime.currentDateTime():
            QMessageBox.warning(self, 'Erreur', 'L\'heure sélectionnée est déjà passée.')
            return

        self.scheduled_shutdown = scheduled_datetime
        self.label.setText(f'Arrêt programmé pour le {scheduled_datetime.toString("dd/MM/yyyy HH:mm")}')
        self.cancel_button.setEnabled(True)

    def shutdown_now(self):
        """Éteindre immédiatement l'ordinateur"""
        self.execute_shutdown()

    def cancel_shutdown(self):
        """Annuler l'arrêt programmé"""
        self.scheduled_shutdown = None
        self.label.setText('Aucun arrêt programmé.')
        self.cancel_button.setEnabled(False)

    def check_schedule(self):
        """Vérifier si l'heure programmée est arrivée"""
        if self.scheduled_shutdown:
            current_datetime = QDateTime.currentDateTime()
            if current_datetime >= self.scheduled_shutdown:
                self.execute_shutdown()
                self.scheduled_shutdown = None

    def execute_shutdown(self):
        """Exécuter la commande d'arrêt en fonction du système d'exploitation"""
        system = platform.system()
        try:
            if system == "Windows":
                subprocess.run(["shutdown", "/s", "/f", "/t", "0"])
            elif system == "Linux" or system == "Darwin":  # Darwin pour macOS
                subprocess.run(["shutdown", "-h", "now"])
            else:
                QMessageBox.warning(self, 'Erreur', 'Système d\'exploitation non pris en charge.')
                return

            # Afficher la notification avant l'arrêt
            self.show_shutdown_notification()

            QMessageBox.information(self, 'Éteindre', 'L\'ordinateur va s\'éteindre maintenant.')
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur lors de l\'arrêt: {str(e)}')

    def show_shutdown_notification(self):
        """Afficher une notification avant l'arrêt"""
        QMessageBox.information(self, 'Arrêt imminent', 'L\'ordinateur va s\'éteindre dans 10 secondes.')

        # Affichage d'un compte à rebours dans la barre de progression
        for i in range(10, -1, -1):
            self.progress_bar.setValue(i * 10)
            QTimer.singleShot(1000 * (10 - i), lambda: None)  # Met un délai de 1 seconde entre chaque mise à jour de la barre

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ShutdownApp()
    ex.show()
    sys.exit(app.exec_())
