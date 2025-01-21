import sys
import os
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
    QFileDialog, QMessageBox, QLabel, QFormLayout, QListWidget, QInputDialog, QAction, QMenuBar, QStatusBar, QToolBar
)
from PyQt5.QtCore import QStandardPaths, Qt
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from googletrans import Translator
from spellchecker import SpellChecker

class MotivationLetterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.current_theme = 'light'
        self.initUI()
        self.initDB()
        self.loadTemplates()
        self.initSpellChecker()
        self.translator = Translator()
        self.statistics = {'letters_created': 0, 'letters_exported': 0}

    def initUI(self):
        self.setWindowTitle('Gestionnaire de Lettres de Motivation - Pro')
        self.setGeometry(100, 100, 1200, 900)

        # Barre de menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Fichier')
        user_menu = menubar.addMenu('Utilisateur')
        edit_menu = menubar.addMenu('Édition')
        view_menu = menubar.addMenu('Affichage')
        tools_menu = menubar.addMenu('Outils')

        # Actions du menu
        new_user_action = QAction('Nouvel Utilisateur', self)
        new_user_action.triggered.connect(self.createUser)
        user_menu.addAction(new_user_action)

        login_action = QAction('Connexion', self)
        login_action.triggered.connect(self.loginUser)
        user_menu.addAction(login_action)

        export_action = QAction('Exporter en PDF', self)
        export_action.triggered.connect(self.exportPDF)
        file_menu.addAction(export_action)

        import_action = QAction('Importer une lettre', self)
        import_action.triggered.connect(self.importLetter)
        file_menu.addAction(import_action)

        theme_action = QAction('Changer de thème', self)
        theme_action.triggered.connect(self.toggleTheme)
        view_menu.addAction(theme_action)

        stats_action = QAction('Afficher les statistiques', self)
        stats_action.triggered.connect(self.showStatistics)
        tools_menu.addAction(stats_action)

        # Barre d'outils
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        toolbar.addAction(new_user_action)
        toolbar.addAction(login_action)
        toolbar.addAction(export_action)
        toolbar.addAction(import_action)
        toolbar.addAction(theme_action)
        toolbar.addAction(stats_action)

        # Widgets
        self.jobTitleInput = QLineEdit(self)
        self.jobTitleInput.setPlaceholderText("Titre du poste")

        self.languageCombo = QComboBox(self)
        self.languageCombo.addItems(['Français', 'Anglais', 'Arabe', 'Turc'])
        self.languageCombo.currentIndexChanged.connect(self.translateLetter)

        self.templateCombo = QComboBox(self)
        self.templateCombo.currentIndexChanged.connect(self.loadTemplate)

        self.letterEdit = QTextEdit(self)
        self.letterEdit.setPlaceholderText("Rédigez votre lettre de motivation ici...")
        self.letterEdit.textChanged.connect(self.checkSpelling)

        self.saveButton = QPushButton('Enregistrer', self)
        self.saveButton.clicked.connect(self.saveLetter)

        self.exportButton = QPushButton('Exporter en PDF', self)
        self.exportButton.clicked.connect(self.exportPDF)

        self.templateList = QListWidget(self)
        self.templateList.itemClicked.connect(self.loadTemplateFromList)

        self.searchInput = QLineEdit(self)
        self.searchInput.setPlaceholderText("Rechercher une lettre...")
        self.searchInput.textChanged.connect(self.searchLetters)

        # Layout
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        form_layout.addRow("Titre du poste:", self.jobTitleInput)
        form_layout.addRow("Langue:", self.languageCombo)
        form_layout.addRow("Modèle:", self.templateCombo)
        layout.addLayout(form_layout)

        layout.addWidget(self.letterEdit)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.exportButton)
        layout.addLayout(buttonLayout)

        layout.addWidget(QLabel("Modèles disponibles:"))
        layout.addWidget(self.templateList)

        layout.addWidget(QLabel("Rechercher des lettres:"))
        layout.addWidget(self.searchInput)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Barre de statut
        self.statusBar().showMessage('Prêt')

    def initDB(self):
        app_data_path = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        db_path = os.path.join(app_data_path, 'saadiya_resources', 'letters.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                             (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS letters
                             (id INTEGER PRIMARY KEY, user_id INTEGER, job_title TEXT, language TEXT, content TEXT, date TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS templates
                             (id INTEGER PRIMARY KEY, name TEXT, content TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS statistics
                             (id INTEGER PRIMARY KEY, user_id INTEGER, letters_created INTEGER, letters_exported INTEGER)''')
        self.conn.commit()

    def initSpellChecker(self):
        self.spell = SpellChecker()
        self.spell.word_frequency.load_words(['motivation', 'emploi', 'compétences', 'expérience'])

    def checkSpelling(self):
        text = self.letterEdit.toPlainText()
        words = text.split()
        misspelled = self.spell.unknown(words)
        for word in misspelled:
            self.letterEdit.setText(self.letterEdit.toPlainText().replace(word, f'<span style="color:red">{word}</span>'))

    def createUser(self):
        username, ok = QInputDialog.getText(self, 'Nouvel Utilisateur', 'Nom d\'utilisateur:')
        if ok and username:
            password, ok = QInputDialog.getText(self, 'Nouvel Utilisateur', 'Mot de passe:', QLineEdit.Password)
            if ok and password:
                try:
                    self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                    self.conn.commit()
                    QMessageBox.information(self, 'Succès', 'Utilisateur créé avec succès!')
                except sqlite3.IntegrityError:
                    QMessageBox.warning(self, 'Erreur', 'Ce nom d\'utilisateur existe déjà.')

    def loginUser(self):
        username, ok = QInputDialog.getText(self, 'Connexion', 'Nom d\'utilisateur:')
        if ok and username:
            password, ok = QInputDialog.getText(self, 'Connexion', 'Mot de passe:', QLineEdit.Password)
            if ok and password:
                self.cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
                user = self.cursor.fetchone()
                if user:
                    self.current_user = user[0]
                    QMessageBox.information(self, 'Succès', 'Connexion réussie!')
                else:
                    QMessageBox.warning(self, 'Erreur', 'Nom d\'utilisateur ou mot de passe incorrect.')

    def loadTemplates(self):
        self.cursor.execute('SELECT name FROM templates')
        templates = self.cursor.fetchall()
        self.templateCombo.clear()
        self.templateList.clear()
        for template in templates:
            self.templateCombo.addItem(template[0])
            self.templateList.addItem(template[0])

    def loadTemplate(self):
        template_name = self.templateCombo.currentText()
        self.cursor.execute('SELECT content FROM templates WHERE name = ?', (template_name,))
        template = self.cursor.fetchone()
        if template:
            self.letterEdit.setPlainText(template[0])

    def loadTemplateFromList(self, item):
        self.cursor.execute('SELECT content FROM templates WHERE name = ?', (item.text(),))
        template = self.cursor.fetchone()
        if template:
            self.letterEdit.setPlainText(template[0])

    def saveLetter(self):
        if not self.current_user:
            QMessageBox.warning(self, 'Erreur', 'Veuillez vous connecter pour enregistrer une lettre.')
            return

        job_title = self.jobTitleInput.text()
        language = self.languageCombo.currentText()
        content = self.letterEdit.toPlainText()

        self.cursor.execute('INSERT INTO letters (user_id, job_title, language, content, date) VALUES (?, ?, ?, ?, datetime("now"))',
                            (self.current_user, job_title, language, content))
        self.conn.commit()
        self.statistics['letters_created'] += 1
        QMessageBox.information(self, 'Enregistré', 'La lettre a été enregistrée avec succès!')

    def exportPDF(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Exporter en PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if fileName:
            c = canvas.Canvas(fileName, pagesize=letter)
            text = self.letterEdit.toPlainText()
            c.setFont("Helvetica", 12)
            c.drawString(100, 750, "Lettre de Motivation")
            c.drawString(100, 730, f"Pour le poste: {self.jobTitleInput.text()}")
            c.drawString(100, 710, f"Langue: {self.languageCombo.currentText()}")
            text_lines = text.split('\n')
            y = 690
            for line in text_lines:
                c.drawString(100, y, line)
                y -= 20
            c.save()
            self.statistics['letters_exported'] += 1
            QMessageBox.information(self, 'Exporté', 'La lettre a été exportée en PDF avec succès!')

    def importLetter(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Importer une lettre", "", "Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            with open(fileName, 'r', encoding='utf-8') as file:
                content = file.read()
                self.letterEdit.setPlainText(content)
                QMessageBox.information(self, 'Importé', 'La lettre a été importée avec succès!')

    def toggleTheme(self):
        if self.current_theme == 'light':
            self.setDarkTheme()
        else:
            self.setLightTheme()

    def setDarkTheme(self):
        self.current_theme = 'dark'
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        QApplication.setPalette(dark_palette)

    def setLightTheme(self):
        self.current_theme = 'light'
        QApplication.setPalette(QApplication.style().standardPalette())

    def translateLetter(self):
        text = self.letterEdit.toPlainText()
        if text:
            lang = self.languageCombo.currentText().lower()
            translated = self.translator.translate(text, dest=lang)
            self.letterEdit.setPlainText(translated.text)

    def searchLetters(self):
        search_term = self.searchInput.text()
        if search_term:
            self.cursor.execute('SELECT job_title FROM letters WHERE job_title LIKE ?', (f'%{search_term}%',))
            results = self.cursor.fetchall()
            self.templateList.clear()
            for result in results:
                self.templateList.addItem(result[0])

    def showStatistics(self):
        stats_message = f"Lettres créées: {self.statistics['letters_created']}\nLettres exportées: {self.statistics['letters_exported']}"
        QMessageBox.information(self, 'Statistiques', stats_message)

    def closeEvent(self, event):
        self.conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MotivationLetterApp()
    mainWin.show()
    sys.exit(app.exec_())