from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QTabWidget
from PyQt5.uic import loadUi
from database import Database

class StockApp(QMainWindow):
    def __init__(self):
        super(StockApp, self).__init__()
        loadUi('stock.ui', self)
        self.db = Database()

        # Charger les données initiales
        self.load_articles()
        self.load_categories()
        self.load_utilisateurs()
        self.load_logs()

        # Connecter les boutons
        self.addArticleButton.clicked.connect(self.add_article)
        self.addCategorieButton.clicked.connect(self.add_categorie)
        self.addUtilisateurButton.clicked.connect(self.add_utilisateur)

    # Gestion des articles
    def load_articles(self):
        self.articleTable.setRowCount(0)
        articles = self.db.get_articles()
        for row_number, article in enumerate(articles):
            self.articleTable.insertRow(row_number)
            for column_number, data in enumerate(article):
                self.articleTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_article(self):
        nom = self.nomArticleLineEdit.text()
        quantite = self.quantiteArticleLineEdit.text()
        prix = self.prixArticleLineEdit.text()
        categorie_id = self.categorieComboBox.currentData()
        if nom and quantite and prix and categorie_id:
            self.db.add_article(nom, int(quantite), float(prix), categorie_id)
            self.load_articles()
            self.clear_article_inputs()
        else:
            QMessageBox.warning(self, 'Erreur', 'Tous les champs doivent être remplis')

    # Gestion des catégories
    def load_categories(self):
        self.categorieTable.setRowCount(0)
        categories = self.db.get_categories()
        for row_number, categorie in enumerate(categories):
            self.categorieTable.insertRow(row_number)
            for column_number, data in enumerate(categorie):
                self.categorieTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_categorie(self):
        nom = self.nomCategorieLineEdit.text()
        if nom:
            self.db.add_categorie(nom)
            self.load_categories()
            self.clear_categorie_inputs()
        else:
            QMessageBox.warning(self, 'Erreur', 'Le nom de la catégorie doit être rempli')

    # Gestion des utilisateurs
    def load_utilisateurs(self):
        self.utilisateurTable.setRowCount(0)
        utilisateurs = self.db.get_utilisateurs()
        for row_number, utilisateur in enumerate(utilisateurs):
            self.utilisateurTable.insertRow(row_number)
            for column_number, data in enumerate(utilisateur):
                self.utilisateurTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_utilisateur(self):
        nom = self.nomUtilisateurLineEdit.text()
        role = self.roleComboBox.currentText()
        password = self.passwordLineEdit.text()
        if nom and role and password:
            self.db.add_utilisateur(nom, role, password)
            self.load_utilisateurs()
            self.clear_utilisateur_inputs()
        else:
            QMessageBox.warning(self, 'Erreur', 'Tous les champs doivent être remplis')

    # Gestion des logs
    def load_logs(self):
        self.logTable.setRowCount(0)
        logs = self.db.get_logs()
        for row_number, log in enumerate(logs):
            self.logTable.insertRow(row_number)
            for column_number, data in enumerate(log):
                self.logTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = StockApp()
    window.show()
    sys.exit(app.exec_())