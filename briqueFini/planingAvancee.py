import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QDateEdit, QPushButton, QTextEdit, QMessageBox,
    QListWidget, QHBoxLayout, QComboBox, QTabWidget, QCalendarWidget, QCheckBox, QSpinBox, QTimeEdit
)
from PyQt5.QtCore import QDate, QTimer, Qt, QTime
from PyQt5.QtGui import QIcon
from plyer import notification
import json
import os
from datetime import datetime, timedelta


class ReminderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_reminders()
        self.load_settings()

    def initUI(self):
        self.setWindowTitle('Application de Rappels Avancée')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('icon.png'))  # Ajoutez une icône si disponible

        # Layout principal avec onglets
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_reminder_tab(), "Définir un Rappel")
        self.tabs.addTab(self.create_calendar_tab(), "Calendrier")
        self.tabs.addTab(self.create_settings_tab(), "Paramètres")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        # Timer pour vérifier les rappels
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_reminders)
        self.timer.start(60000)  # Vérifie toutes les minutes

    def create_reminder_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Sélection de la date et de l'heure
        self.date_edit = QDateEdit(self)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        layout.addWidget(QLabel('Sélectionnez une date:'))
        layout.addWidget(self.date_edit)

        self.time_edit = QTimeEdit(self)
        self.time_edit.setTime(QTime.currentTime())
        layout.addWidget(QLabel('Sélectionnez une heure:'))
        layout.addWidget(self.time_edit)

        # Répétition du rappel
        self.repeat_combo = QComboBox(self)
        self.repeat_combo.addItems(["Aucune", "Quotidien", "Hebdomadaire", "Mensuel"])
        layout.addWidget(QLabel('Répétition:'))
        layout.addWidget(self.repeat_combo)

        # Texte du rappel
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText('Entrez le texte du rappel...')
        layout.addWidget(QLabel('Entrez le texte du rappel:'))
        layout.addWidget(self.text_edit)

        # Boutons pour définir, modifier et supprimer des rappels
        button_layout = QHBoxLayout()
        self.set_button = QPushButton('Définir un rappel', self)
        self.set_button.clicked.connect(self.set_reminder)
        button_layout.addWidget(self.set_button)

        self.edit_button = QPushButton('Modifier le rappel', self)
        self.edit_button.clicked.connect(self.edit_reminder)
        button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton('Supprimer le rappel', self)
        self.delete_button.clicked.connect(self.delete_reminder)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)

        # Liste des rappels
        self.reminder_list = QListWidget(self)
        layout.addWidget(QLabel('Rappels définis:'))
        layout.addWidget(self.reminder_list)

        tab.setLayout(layout)
        return tab

    def create_calendar_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Calendrier intégré
        self.calendar = QCalendarWidget(self)
        self.calendar.clicked.connect(self.on_calendar_click)
        layout.addWidget(self.calendar)

        # Liste des rappels pour la date sélectionnée
        self.calendar_reminder_list = QListWidget(self)
        layout.addWidget(QLabel('Rappels pour la date sélectionnée:'))
        layout.addWidget(self.calendar_reminder_list)

        tab.setLayout(layout)
        return tab

    def create_settings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Désactiver temporairement les rappels
        self.disable_reminders_checkbox = QCheckBox("Désactiver temporairement les rappels", self)
        layout.addWidget(self.disable_reminders_checkbox)

        # Personnalisation des notifications
        layout.addWidget(QLabel('Durée de la notification (secondes):'))
        self.notification_duration = QSpinBox(self)
        self.notification_duration.setRange(1, 60)
        self.notification_duration.setValue(5)
        layout.addWidget(self.notification_duration)

        # Sauvegarder les paramètres
        self.save_settings_button = QPushButton('Sauvegarder les paramètres', self)
        self.save_settings_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_settings_button)

        tab.setLayout(layout)
        return tab

    def set_reminder(self):
        date = self.date_edit.date().toString(Qt.ISODate)
        time = self.time_edit.time().toString(Qt.ISODate)
        text = self.text_edit.toPlainText()
        repeat = self.repeat_combo.currentText()

        if not text:
            QMessageBox.warning(self, 'Erreur', 'Le texte du rappel ne peut pas être vide.')
            return

        reminder = {
            'date': date,
            'time': time,
            'text': text,
            'repeat': repeat
        }

        self.save_reminder(reminder)
        self.update_reminder_list()
        QMessageBox.information(self, 'Rappel défini', 'Le rappel a été enregistré avec succès.')

    def edit_reminder(self):
        selected_item = self.reminder_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, 'Erreur', 'Aucun rappel sélectionné.')
            return

        index = self.reminder_list.row(selected_item)
        reminder = self.reminders[index]

        # Remplir les champs avec les données du rappel sélectionné
        self.date_edit.setDate(QDate.fromString(reminder['date'], Qt.ISODate))
        self.time_edit.setTime(QTime.fromString(reminder['time'], Qt.ISODate))
        self.text_edit.setPlainText(reminder['text'])
        self.repeat_combo.setCurrentText(reminder['repeat'])

        # Supprimer le rappel sélectionné
        self.reminders.pop(index)
        self.save_reminders()
        self.update_reminder_list()

    def delete_reminder(self):
        selected_item = self.reminder_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, 'Erreur', 'Aucun rappel sélectionné.')
            return

        index = self.reminder_list.row(selected_item)
        self.reminders.pop(index)
        self.save_reminders()
        self.update_reminder_list()
        QMessageBox.information(self, 'Rappel supprimé', 'Le rappel a été supprimé avec succès.')

    def save_reminder(self, reminder):
        reminders = []
        if os.path.exists('reminders.json'):
            with open('reminders.json', 'r') as file:
                reminders = json.load(file)

        reminders.append(reminder)

        with open('reminders.json', 'w') as file:
            json.dump(reminders, file)

    def load_reminders(self):
        if os.path.exists('reminders.json'):
            with open('reminders.json', 'r') as file:
                self.reminders = json.load(file)
        else:
            self.reminders = []

        self.update_reminder_list()

    def update_reminder_list(self):
        self.reminder_list.clear()
        for reminder in self.reminders:
            self.reminder_list.addItem(f"{reminder['date']} {reminder['time']} - {reminder['text']} ({reminder['repeat']})")

    def check_reminders(self):
        if self.disable_reminders_checkbox.isChecked():
            return

        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M')

        for reminder in self.reminders[:]:
            reminder_datetime = f"{reminder['date']} {reminder['time']}"
            if reminder_datetime <= current_datetime:
                self.show_notification(reminder['text'])
                self.handle_repeat(reminder)
                self.reminders.remove(reminder)
                self.save_reminders()

    def handle_repeat(self, reminder):
        repeat = reminder['repeat']
        if repeat == "Quotidien":
            new_date = (QDate.fromString(reminder['date'], Qt.ISODate).addDays(1)).toString(Qt.ISODate)
        elif repeat == "Hebdomadaire":
            new_date = (QDate.fromString(reminder['date'], Qt.ISODate).addDays(7)).toString(Qt.ISODate)
        elif repeat == "Mensuel":
            new_date = (QDate.fromString(reminder['date'], Qt.ISODate).addMonths(1)).toString(Qt.ISODate)
        else:
            return

        new_reminder = {
            'date': new_date,
            'time': reminder['time'],
            'text': reminder['text'],
            'repeat': reminder['repeat']
        }
        self.save_reminder(new_reminder)

    def save_reminders(self):
        with open('reminders.json', 'w') as file:
            json.dump(self.reminders, file)

    def show_notification(self, text):
        # Notification système
        notification.notify(
            title='Rappel',
            message=text,
            timeout=self.notification_duration.value(),
            app_name='Application de Rappels Avancée'
        )

        # Notification dans l'application
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Rappel')
        msg_box.setText(text)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def on_calendar_click(self, date):
        self.calendar_reminder_list.clear()
        selected_date = date.toString(Qt.ISODate)
        for reminder in self.reminders:
            if reminder['date'] == selected_date:
                self.calendar_reminder_list.addItem(f"{reminder['time']} - {reminder['text']} ({reminder['repeat']})")

    def save_settings(self):
        settings = {
            'disable_reminders': self.disable_reminders_checkbox.isChecked(),
            'notification_duration': self.notification_duration.value()
        }
        with open('settings.json', 'w') as file:
            json.dump(settings, file)
        QMessageBox.information(self, 'Paramètres sauvegardés', 'Les paramètres ont été sauvegardés avec succès.')

    def load_settings(self):
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as file:
                settings = json.load(file)
                self.disable_reminders_checkbox.setChecked(settings['disable_reminders'])
                self.notification_duration.setValue(settings['notification_duration'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReminderApp()
    ex.show()
    sys.exit(app.exec_())