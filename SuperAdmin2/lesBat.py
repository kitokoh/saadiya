import os
import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox, QSplitter, QTextBrowser, QMenuBar, QMenu, QAction
)
from PyQt5.QtCore import Qt, QProcess


class TerminalWidget(QWidget):
    """Widget pour afficher un terminal intégré."""
    def __init__(self, script_name, script_path, parent=None):
        super().__init__(parent)
        self.script_name = script_name
        self.script_path = script_path
        self.log_file = f"logs/{script_name}.log"

        # Crée le dossier logs s'il n'existe pas
        os.makedirs("logs", exist_ok=True)

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Affichage de sortie du terminal
        self.output_display = QTextBrowser()
        self.output_display.setReadOnly(True)
        self.output_display.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 5px;")
        self.layout.addWidget(self.output_display)

        # Processus pour exécuter le script
        self.process = QProcess()
        self.process.setProgram("cmd.exe")
        self.process.setArguments(["/C", script_path])
        self.process.readyReadStandardOutput.connect(self.display_output)
        self.process.readyReadStandardError.connect(self.display_output)
        self.process.finished.connect(self.execution_finished)

        # Lancer le script
        self.process.start()

    def display_output(self):
        """Afficher et enregistrer la sortie du processus."""
        output = self.process.readAllStandardOutput().data().decode()
        error = self.process.readAllStandardError().data().decode()
        self.output_display.append(output + error)
        with open(self.log_file, "a") as f:
            f.write(output + error)

    def execution_finished(self):
        """Message d'exécution terminée."""
        self.output_display.append("<br><b>--- Exécution terminée ---</b>")


class BatLauncherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lanceur de Scripts .bat avec HTML pour les Descriptions")
        self.setGeometry(100, 100, 900, 800)
        self.scripts_data = self.load_scripts()

        # Style global
        self.setStyleSheet("""
        QWidget { background-color: #f9f9f9; font-family: 'Arial'; font-size: 14px; }
        QTabWidget::pane { border: 1px solid #ccc; background: #fff; }
        QTabBar::tab { background: #d3d3d3; color: #333; padding: 10px; margin: 3px; border-radius: 5px; }
        QTabBar::tab:selected { background: #007acc; color: white; font-weight: bold; }
        QPushButton { background-color: #007acc; color: white; border: 2px solid #005999; border-radius: 10px; padding: 10px; }
        QPushButton:hover { background-color: #005999; }
        QPushButton:pressed { background-color: #003d66; border-color: #003d66; }
        QTextBrowser { font-size: 15px; color: #333; border: 1px solid #ddd; border-radius: 10px; padding: 15px; }
        """)

        # Barre de menu
        self.create_menu_bar()

        # Splitter principal
        self.splitter = QSplitter(Qt.Vertical)
        self.setCentralWidget(self.splitter)

        # Section des boutons
        self.button_tabs = QTabWidget()
        self.splitter.addWidget(self.button_tabs)

        # Section des terminaux
        self.terminal_tabs = QTabWidget()
        self.terminal_tabs.setTabsClosable(True)
        self.terminal_tabs.tabCloseRequested.connect(self.close_terminal_tab)
        self.splitter.addWidget(self.terminal_tabs)

        # Charger les onglets des boutons
        for category, data in self.scripts_data.items():
            self.add_button_tab(category, data["scripts"], data["description"])

    def load_scripts(self):
        """Charger les données des scripts depuis un fichier JSON."""
        try:
            with open("scripts.json", "r") as file:
                data = json.load(file)
                # Vérifie que le format attendu est respecté
                if not isinstance(data, dict):
                    raise ValueError("Le fichier JSON doit contenir un objet à la racine.")
                return data
        except FileNotFoundError:
            QMessageBox.critical(self, "Erreur", "Le fichier 'scripts.json' est introuvable.")
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de parsing du fichier JSON : {e}")
        except ValueError as e:
            QMessageBox.critical(self, "Erreur", str(e))
        return {}

    def add_button_tab(self, category, scripts, description):
        """Ajouter un onglet de boutons pour une catégorie avec une section explicative HTML."""
        tab = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(40)
        layout.setContentsMargins(30, 30, 30, 30)

        # Section des boutons
        button_layout = QVBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setContentsMargins(10, 0, 10, 0)

        for script in scripts:
            btn = QPushButton(script["name"])
            btn.setFixedHeight(70)
            btn.setFixedWidth(280)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #005A9E; 
                    color: white; 
                    font-size: 18px; 
                    font-weight: bold; 
                    border-radius: 15px; 
                    border: 2px solid #0078D7;
                    padding: 10px;
                    text-align: center;
                }
                QPushButton:hover {
                    background-color: #0078D7; 
                }
                QPushButton:pressed {
                    background-color: #004C8C; 
                    border-color: #003E73; 
                }
            """)
            btn.clicked.connect(lambda _, s=script: self.open_terminal(s))
            button_layout.addWidget(btn)

        layout.addLayout(button_layout)

        # Section explicative (HTML)
        description_box = QTextBrowser()
        description_box.setHtml(description)
        description_box.setStyleSheet("""
            QTextBrowser {
                background: #F9F9F9; 
                border: 1px solid #D1D1D1; 
                border-radius: 15px; 
                padding: 25px; 
                font-family: 'Roboto', sans-serif; 
                font-size: 16px; 
                color: #444444; 
                line-height: 1.8;
                max-height: 400px; 
            }
            QTextBrowser h2 {
                font-size: 22px; 
                color: #005A9E; 
                margin-bottom: 15px;
                font-weight: bold;
            }
            QTextBrowser p {
                font-size: 16px; 
                margin-bottom: 15px;
            }
            QTextBrowser a {
                color: #005A9E; 
                text-decoration: none;
            }
            QTextBrowser a:hover {
                text-decoration: underline;
            }
        """)
        description_box.setFixedWidth(1000)
        description_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Ajouter la barre de défilement verticale
        layout.addWidget(description_box)

        # Appliquer le layout
        tab.setLayout(layout)

        # Styliser les onglets
        self.button_tabs.addTab(tab, category)
        self.button_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #D1D1D1;
                background: #FAFAFA;
                border-radius: 15px;
                padding: 10px;
            }
            QTabBar::tab {
                background-color: #005A9E;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 15px 25px;
                border-radius: 12px;
                margin: 0 8px;
                white-space: nowrap;  /* Empêche le texte de se couper */
                min-width: 150px;  /* Largeur minimale pour garantir la lisibilité */
            }
            QTabBar::tab:hover {
                background-color: #0078D7;
            }
            QTabBar::tab:selected {
                background-color: #003E73;
                color: white;
                border-radius: 12px;
                font-weight: bold;
                border: 3px solid #003E73;
            }
            QTabWidget::tab-bar {
                alignment: left;  /* Alignement des onglets à gauche */
            }
        """)

        # Application des animations et de la couleur dynamique pour un onglet sélectionné
        self.button_tabs.setTabBarAutoHide(True)

    def open_terminal(self, script):
        """Ouvrir un terminal intégré dans un nouvel onglet."""
        if not os.path.exists(script["path"]):
            QMessageBox.critical(self, "Erreur", f"Le fichier '{script['path']}' est introuvable.")
            return

        terminal_widget = TerminalWidget(script["name"], script["path"])
        self.terminal_tabs.addTab(terminal_widget, script["name"])
        self.terminal_tabs.setCurrentWidget(terminal_widget)

    def close_terminal_tab(self, index):
        """Fermer un onglet de terminal."""
        widget = self.terminal_tabs.widget(index)
        if widget:
            widget.process.terminate()
            self.terminal_tabs.removeTab(index)

    def create_menu_bar(self):
        """Créer une barre de menu pour ajouter des outils supplémentaires."""
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Fichier")
        help_menu = menu_bar.addMenu("Aide")

        # Option de recharger les scripts
        reload_action = file_menu.addAction("Recharger les scripts")
        reload_action.triggered.connect(self.reload_scripts)

        # Option d'exporter les logs
        export_action = file_menu.addAction("Exporter les logs")
        export_action.triggered.connect(self.export_logs)

        # Option à propos
        about_action = help_menu.addAction("À propos")
        about_action.triggered.connect(self.show_about_dialog)

    def reload_scripts(self):
        """Recharger les scripts depuis le fichier JSON."""
        self.scripts_data = self.load_scripts()
        self.button_tabs.clear()
        for category, data in self.scripts_data.items():
            self.add_button_tab(category, data["scripts"], data["description"])

    def export_logs(self):
        """Exporter les logs dans un fichier .txt."""
        logs_dir = "logs"
        export_dir = "exports"
        os.makedirs(export_dir, exist_ok=True)
        for log_file in os.listdir(logs_dir):
            if log_file.endswith(".log"):
                log_path = os.path.join(logs_dir, log_file)
                export_path = os.path.join(export_dir, log_file.replace(".log", ".txt"))
                with open(log_path, "r") as src, open(export_path, "w") as dest:
                    dest.write(src.read())
        QMessageBox.information(self, "Exportation", "Les logs ont été exportés avec succès.")

    def show_about_dialog(self):
        """Afficher une boîte de dialogue 'À propos'."""
        QMessageBox.information(self, "À propos", "Lanceur de Scripts .bat v1.0\n© 2024 VotreEntreprise")

    def closeEvent(self, event):
        """S'assurer que tous les processus sont arrêtés à la fermeture."""
        for i in range(self.terminal_tabs.count()):
            widget = self.terminal_tabs.widget(i)
            if widget and widget.process.state() != QProcess.NotRunning:
                widget.process.terminate()
                widget.process.waitForFinished()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BatLauncherApp()
    window.show()
    sys.exit(app.exec_())

