from PyQt5 import QtWidgets, QtCore, QtGui
import sys

class SuperAdminPlatform(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SuperAdmin Platform")
        self.resize(1200, 700)
        self.setStyleSheet("background-color: #f5f5f5;")  # Fond clair et propre

        # Configurer le widget principal
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QtWidgets.QVBoxLayout(main_widget)

        # Création des sections : menu, contenu, footer
        self.create_left_menu(main_layout)
        self.create_main_content(main_layout)
        self.create_footer(main_layout)

        # Connexion des actions du menu
        self.menu_list.itemClicked.connect(self.menu_clicked)

    def create_left_menu(self, layout):
        # Container pour le menu latéral
        menu_container = QtWidgets.QWidget()
        menu_layout = QtWidgets.QVBoxLayout(menu_container)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        
        # Liste de menu flottante avec icônes modernes
        self.menu_list = QtWidgets.QListWidget()
        self.menu_list.setFixedWidth(250)
        self.menu_list.setSpacing(8)  # Plus d'espacement entre les éléments
        self.menu_list.setStyleSheet("""
            QListWidget {
                background-color: #2d3e50;  # Couleur sombre élégante
                color: #ecf0f1;  # Texte clair
                font-size: 16px;
                border-right: 2px solid #34495e;
                border-radius: 12px;
                margin-top: 20px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 12px 16px;
                border-radius: 6px;
                transition: background-color 0.3s ease;  # Transition douce
            }
            QListWidget::item:hover {
                background-color: #2980b9;
                cursor: pointer;
                color: #ffffff;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        menu_layout.addWidget(self.menu_list)
        self.populate_menu()
        layout.addWidget(menu_container)

    def create_main_content(self, layout):
        # Contenu principal avec fond blanc et ombre douce
        main_content = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout(main_content)

        # Zone de contenu avec bordures arrondies et ombre
        self.content_area = QtWidgets.QTextEdit("Bienvenue dans SuperAdmin Platform")
        self.content_area.setReadOnly(True)
        self.content_area.setStyleSheet("""
            background-color: #ffffff;  # Fond blanc pour le contenu
            color: #34495e;
            padding: 20px;
            font-size: 18px;
            font-family: 'Segoe UI', sans-serif;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);  # Ombre subtile pour l'effet de profondeur
        """)

        # Zone d'exécution avec font monospace et fond gris foncé
        self.execution_area = QtWidgets.QTextEdit("Zone d'exécution...\n")
        self.execution_area.setReadOnly(True)
        self.execution_area.setStyleSheet("""
            background-color: #2d3e50;  # Fond gris foncé
            color: #ecf0f1;
            padding: 15px;
            font-family: monospace;
            font-size: 14px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);  # Ombre subtile
        """)

        content_layout.addWidget(self.content_area)
        content_layout.addWidget(self.execution_area)
        main_content.setLayout(content_layout)

        # Disposition horizontale pour combiner menu et contenu
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(self.menu_list)
        h_layout.addWidget(main_content, stretch=2)
        layout.addLayout(h_layout)

    def create_footer(self, layout):
        # Footer stylisé
        self.footer = QtWidgets.QLabel("© 2024 SuperAdmin Platform - Tous droits réservés | Version 1.0")
        self.footer.setAlignment(QtCore.Qt.AlignCenter)
        self.footer.setStyleSheet("""
            background-color: #2d3e50;  # Fond foncé
            color: #ecf0f1;
            padding: 12px;
            font-size: 14px;
            font-family: 'Segoe UI', sans-serif;
            border-radius: 12px;
        """)
        layout.addWidget(self.footer)

    def populate_menu(self):
        # Menu dynamique avec sous-menus
        menu_sections = {
            "Compile App": ["Compile TS to QM", "Compile PY to TS", "Compile PY to QM", "Extract EXE", "EXE to EXE"],
            "Distribue App": ["To Git", "To Salesforce", "To Mega"],
            "Marketing App": ["Création de contenu", "FB Ads", "Google Ads"],
            "Manage App": ["Technique", "Finance", "Social"],
            "Manage Instances": ["Bon", "WaBon", "YTBon", "InstaBon", "PinBon", "InBon", "BrandBon", "MailBon"]
        }

        icons = {
            "Compile App": "compile_icon.png",
            "Distribue App": "distribute_icon.png",
            "Marketing App": "marketing_icon.png",
            "Manage App": "manage_icon.png",
            "Manage Instances": "instance_icon.png",
            "default": "default_icon.png"
        }

        for menu_name, submenu_items in menu_sections.items():
            main_item = self.create_menu_item(menu_name, icons)
            self.menu_list.addItem(main_item)

            for submenu_name in submenu_items:
                submenu_item = QtWidgets.QListWidgetItem(f"    - {submenu_name}")
                submenu_item.setData(QtCore.Qt.UserRole, submenu_name)
                submenu_item.setTextAlignment(QtCore.Qt.AlignLeft)
                submenu_item.setFont(QtGui.QFont("Arial", 10))
                submenu_item.setForeground(QtGui.QColor("#bdc3c7"))
                self.menu_list.addItem(submenu_item)

    def create_menu_item(self, menu_name, icons):
        # Crée et retourne un item de menu principal avec icône
        main_item = QtWidgets.QListWidgetItem(menu_name)
        icon_path = icons.get(menu_name, icons["default"])
        main_item.setIcon(QtGui.QIcon(icon_path))
        main_item.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))
        return main_item

    def menu_clicked(self, item):
        submenu_name = item.data(QtCore.Qt.UserRole)
        if submenu_name:
            self.content_area.clear()
            self.content_area.setText(f"Commande exécutée pour : {submenu_name}")
            self.execution_area.append(f"Exécution de : {submenu_name}")
            self.execute_submenu_action(submenu_name)
            self.show_notification(f"Action {submenu_name} exécutée avec succès!")

    def execute_submenu_action(self, submenu_name):
        if "Compile" in submenu_name:
            result = f"Compiling... {submenu_name} completed!"
        elif "To" in submenu_name:
            result = f"Distribution to {submenu_name.split()[-1]} initiated!"
        elif "FB Ads" in submenu_name or "Google Ads" in submenu_name:
            result = f"Launching marketing campaign on {submenu_name}!"
        else:
            result = f"Gestion de {submenu_name} initiée!"
        self.execution_area.append(result)
        self.execution_area.append("-" * 40)

    def show_notification(self, message):
        notif = QtWidgets.QLabel(message, self)
        notif.setStyleSheet("""
            QLabel {
                background-color: #16a085;
                color: white;
                padding: 12px;
                font-size: 12px;
                border-radius: 6px;
                opacity: 0;
                animation: slideIn 0.5s forwards;
            }
            @keyframes slideIn {
                0% { top: -50px; opacity: 0; }
                100% { top: 20px; opacity: 1; }
            }
        """)
        notif.setAlignment(QtCore.Qt.AlignCenter)
        notif.setGeometry(200, 10, 800, 30)
        notif.show()

app = QtWidgets.QApplication(sys.argv)
window = SuperAdminPlatform()
window.show()
sys.exit(app.exec_())
