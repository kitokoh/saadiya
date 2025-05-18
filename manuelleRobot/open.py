
import json
import os
import subprocess
import sqlite3
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextEdit, 
                            QPushButton, QFrame, QHBoxLayout, QScrollArea,
                            QGroupBox, QProgressBar, QSpinBox, QMessageBox,
                            QComboBox, QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QLinearGradient, QPainter
from imports import DB_PATH_notes



from manuelleRobot.description import MainWindow1




from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QRadioButton

from manuelleRobot.statusmanuelle import SocialMediaPublisher
class DescriptionManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Partie gauche
        self.left_panel = DescriptionManager1()

        # Créer le QStackedWidget avec les deux panneaux
        self.stacked_right_panel = QStackedWidget()
        self.right_panel1 = MainWindow1()
        self.right_panel2 = SocialMediaPublisher()
        self.stacked_right_panel.addWidget(self.right_panel1)
        self.stacked_right_panel.addWidget(self.right_panel2)
        self.stacked_right_panel.setCurrentIndex(0)

        # Boutons radio (affichés en horizontal pour meilleur rendu)
        self.radio1 = QRadioButton("Description")
        self.radio2 = QRadioButton("Status Publisher")
        self.radio1.setChecked(True)

        self.radio1.toggled.connect(lambda: self.stacked_right_panel.setCurrentIndex(0))
        self.radio2.toggled.connect(lambda: self.stacked_right_panel.setCurrentIndex(1))

        # Layout horizontal pour les boutons radio
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio1)
        radio_layout.addWidget(self.radio2)
        radio_layout.addStretch()  # pousse les boutons à gauche

        # Conteneur pour les boutons
        radio_container = QWidget()
        radio_container.setLayout(radio_layout)

        # Layout principal de droite (radio en haut + widget en dessous)
        right_layout = QVBoxLayout()
        right_layout.addWidget(radio_container)
        right_layout.addWidget(self.stacked_right_panel)
        right_layout.setStretch(1, 1)  # donne tout l'espace dispo au stacked panel

        right_container = QWidget()
        right_container.setLayout(right_layout)

        # Layout global
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.left_panel, 2)
        main_layout.addWidget(right_container, 3)  # un peu plus large

        self.setLayout(main_layout)
        self.resize(1200, 700)









import json
import os
import subprocess
import sqlite3
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextEdit, 
                            QPushButton, QFrame, QHBoxLayout, QScrollArea,
                            QGroupBox, QProgressBar, QSpinBox, QMessageBox,
                            QComboBox, QFileDialog, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QLinearGradient, QPainter
from imports import DB_PATH_notes

class DescriptionManager1(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tr = self.init_translations()
        self.base_paths = {
            "bon": "C:/bon",
            "wabon": "C:/wabon",
            "instabon": "C:/instabon",
            "inbon": "C:/inbon",
            "ytbon": "C:/ytbon"
        }
        self.setup_database()
        self.init_ui()
        self.scan_networks_and_robots()
        self.link_opener = None
        self.setup_styles()
        self.current_robot = None
        self.current_network = None

    def init_translations(self):
        """Initialize professional translations"""
        return {
            'window_title': "Sales Robot Manager",
            'no_robot_title': "No Robot Installed",
            'no_robot_msg': "No sales robot detected. Please install at least one robot in the network directories.",
            'config_group': "Configuration",
            'group_size_label': "Links per batch:",
            'description_label': "Product Description:",
            'description_placeholder': "Enter your professional product description here...",
            'exec_group': "Execution",
            'start_btn': "Start",
            'continue_btn': "Continue",
            'stop_btn': "Stop",
            'status_ready': "Ready to start",
            'status_running': "Processing...",
            'status_paused': "Waiting for confirmation...",
            'status_complete': "Process completed",
            'status_stopped': "Process stopped",
            'network_select_label': "Select Social Network:",
            'robot_select_label': "Select Sales Robot:",
            'group_opened': "Batch {} opened - {} links",
            'error_json': "Error: JSON file not found",
            'error_chrome': "Error: Chrome path incorrect",
            'install_btn': "Install Robot",
            'browse_btn': "Browse",
            'visualization_placeholder': "Execution details will appear here..."
        }

    def setup_database(self):
        """Initialize database connection"""
        self.conn = sqlite3.connect(DB_PATH_notes)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_size INTEGER DEFAULT 10,
                last_description TEXT,
                last_robot TEXT,
                last_network TEXT,
                chrome_path TEXT
            )
        ''')

        # Nouvelle table pour les descriptions des autres robots
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS autredescription (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                network_name TEXT NOT NULL,
                robot_name TEXT NOT NULL,
                description TEXT,
                UNIQUE(network_name, robot_name)
            )
        ''')
    
        # Insert default settings if needed
        self.cursor.execute('SELECT COUNT(*) FROM settings')
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute('''
                INSERT INTO settings (group_size, chrome_path) 
                VALUES (10, 'C:/Program Files/Google/Chrome/Application/chrome.exe')
            ''')
            self.conn.commit()

    def save_description(self):
        """Sauvegarde automatiquement la description dans la base de données"""
        description = self.desc_edit.toPlainText()
        robot_name = self.robot_combo.currentText()
        network_name = self.network_combo.currentText()
        
        if robot_name == "robot1" and network_name == "bon":
            # Sauvegarde dans la table settings pour robot1 sur bon
            self.cursor.execute('''
                UPDATE settings 
                SET last_description = ?
                WHERE id = 1
            ''', (description,))
        else:
            # Sauvegarde dans la table autredescription pour les autres robots
            self.cursor.execute('''
                INSERT OR REPLACE INTO autredescription (network_name, robot_name, description)
                VALUES (?, ?, ?)
            ''', (network_name, robot_name, description))
        
        self.conn.commit()

    def load_description_for_robot(self, network_name, robot_name):
        """Charge la description appropriée selon le robot sélectionné"""
        if robot_name == "robot1" and network_name == "bon":
            # Charge depuis la table settings pour robot1 sur bon
            self.cursor.execute('SELECT last_description FROM settings LIMIT 1')
            result = self.cursor.fetchone()
            description = result[0] if result and result[0] is not None else ""
        else:
            # Charge depuis la table autredescription pour les autres robots
            self.cursor.execute('''
                SELECT description FROM autredescription 
                WHERE network_name = ? AND robot_name = ?
            ''', (network_name, robot_name))
            result = self.cursor.fetchone()
            description = result[0] if result else ""
        
        self.desc_edit.setPlainText(description)

    def save_settings(self):
        """Sauvegarde les paramètres (sauf description déjà sauvegardée automatiquement)"""
        self.cursor.execute('''
            UPDATE settings 
            SET group_size = ?,
                last_robot = ?,
                last_network = ?
            WHERE id = 1
        ''', (
            self.batch_spin.value(),
            self.robot_combo.currentText(),
            self.network_combo.currentText()
        ))
        self.conn.commit()

    def closeEvent(self, event):
        """Ferme proprement les ressources"""
        if self.link_opener and self.link_opener.isRunning():
            self.link_opener.stop()
            self.link_opener.wait(1000)
        
        self.conn.close()
        super().closeEvent(event)

    def load_description(self):
        """Charge la description depuis la base de données"""
        last_network = self.load_setting('last_network', 'bon')
        last_robot = self.load_setting('last_robot', 'robot1')
        self.load_description_for_robot(last_network, last_robot)


    def init_ui(self):
        """Initialize professional UI"""
        self.setWindowTitle(self.tr['window_title'])
        self.setFixedSize(1000, 800)

        # Style général
        self.setStyleSheet('''
            QWidget {
                font-family: "Segoe UI", Arial, sans-serif;
                background-color: #f5f7fa;
            }
            QGroupBox {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 20px;
                font-weight: bold;
                color: #2c3e50;
                background-color: white;
                font-size: 14px;
            }
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 12px;
                font-size: 14px;
                background-color: #ffffff;
            }
            QComboBox, QSpinBox {
                border: 2px solid #00ffff;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 14px;
                min-width: 150px;
                background-color: #ffffff;
            }
            QComboBox:focus, QSpinBox:focus {
                border: 2px solid #00ffcc;
                background-color: #e8fdfd;
            }
            QLabel {
                color: #34495e;
                font-size: 13px;
            }
        ''')

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Groupe de configuration
        config_group = QGroupBox(self.tr['config_group'])
        config_layout = QVBoxLayout()

        # Ligne des trois sélections côte à côte
        selection_line = QHBoxLayout()

        # --- Choix réseau ---
        network_layout = QVBoxLayout()
        network_label = QLabel(self.tr['network_select_label'])
        self.network_combo = QComboBox()
        self.network_combo.currentTextChanged.connect(self.on_network_changed)
        network_layout.addWidget(network_label)
        network_layout.addWidget(self.network_combo)

        # --- Choix robot ---
        robot_layout = QVBoxLayout()
        robot_label = QLabel(self.tr['robot_select_label'])
        self.robot_combo = QComboBox()
        self.robot_combo.currentTextChanged.connect(self.on_robot_changed)
        robot_layout.addWidget(robot_label)
        robot_layout.addWidget(self.robot_combo)

        # --- Taille du groupe ---
        batch_layout = QVBoxLayout()
        batch_label = QLabel(self.tr['group_size_label'])
        self.batch_spin = QSpinBox()
        self.batch_spin.setRange(1, 50)
        self.batch_spin.setValue(self.load_setting('group_size', 10))
        batch_layout.addWidget(batch_label)
        batch_layout.addWidget(self.batch_spin)

        # Ajout dans la ligne
        selection_line.addLayout(network_layout)
        selection_line.addSpacing(20)
        selection_line.addLayout(robot_layout)
        selection_line.addSpacing(20)
        selection_line.addLayout(batch_layout)
        selection_line.addStretch()

        # --- Description du produit ---
        desc_layout = QVBoxLayout()
        desc_label = QLabel(self.tr['description_label'])
        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText(self.tr['description_placeholder'])
        self.desc_edit.setMinimumHeight(120)
        self.desc_edit.textChanged.connect(self.save_description)
        self.load_description()

        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_edit)

        # Assemblage du groupe config
        config_layout.addLayout(selection_line)
        config_layout.addSpacing(15)
        config_layout.addLayout(desc_layout, 1)
        config_group.setLayout(config_layout)

        # Groupe exécution
        exec_group = QGroupBox(self.tr['exec_group'])
        exec_layout = QVBoxLayout()

        # Boutons de contrôle
        control_layout = QHBoxLayout()
        self.start_btn = self.create_button(self.tr['start_btn'], "#2ecc71", self.start_processing)
        self.continue_btn = self.create_button(self.tr['continue_btn'], "#3498db", self.continue_processing)
        self.continue_btn.setEnabled(False)
        self.stop_btn = self.create_button(self.tr['stop_btn'], "#e74c3c", self.stop_processing)
        self.stop_btn.setEnabled(False)

        control_layout.addStretch()
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.continue_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addStretch()

        # Affichage du statut et batch
        self.status_label = QLabel(self.tr['status_ready'])
        self.status_label.setStyleSheet('font-weight: bold; color: #7f8c8d; font-size: 14px;')

        self.batch_label = QLabel()
        self.batch_label.setStyleSheet('color: #95a5a6; font-size: 13px;')

        # Zone de visualisation
        self.visualization = QTextEdit()
        self.visualization.setReadOnly(True)
        self.visualization.setStyleSheet('''
            QTextEdit {
                background-color: #f9f9f9;
                border: 2px dashed #ddd;
                border-radius: 8px;
                color: #555;
                font-size: 13px;
                min-height: 200px;
                padding: 15px;
            }
        ''')
        self.visualization.setPlaceholderText(self.tr['visualization_placeholder'])

        # Ajout au layout exécution
        exec_layout.addLayout(control_layout)
        exec_layout.addWidget(self.status_label)
        exec_layout.addWidget(self.batch_label)
        exec_layout.addWidget(self.visualization, 1)
        exec_group.setLayout(exec_layout)

        # Ajout final au layout principal
        main_layout.addWidget(config_group, 1)
        main_layout.addWidget(exec_group, 2)
        self.setLayout(main_layout)

    def scan_networks_and_robots(self):
        """Scan for available social networks and their robots"""
        self.network_combo.clear()
        self.robot_combo.clear()
        
        available_networks = []
        
        for network_name, base_path in self.base_paths.items():
            if os.path.exists(base_path):
                robots = [d for d in os.listdir(base_path) 
                         if d.startswith('robot') and os.path.isdir(os.path.join(base_path, d))]
                
                if robots:
                    display_name = {
                        'bon': 'Facebook',
                        'wabon': 'WhatsApp',
                        'instabon': 'Instagram',
                        'inbon': 'LinkedIn',
                        'ytbon': 'YouTube'
                    }.get(network_name, network_name)
                    
                    available_networks.append((network_name, display_name, robots))
        
        if not available_networks:
            self.show_no_robot_modal()
            return
            
        # Add networks to combo box
        for network_name, display_name, robots in available_networks:
            self.network_combo.addItem(display_name, network_name)
        
        # Load last used network
        last_network = self.load_setting('last_network', 'bon')
        last_network_index = max(0, self.network_combo.findData(last_network))
        self.network_combo.setCurrentIndex(last_network_index)
        
        # This will trigger on_network_changed to populate robots
        self.on_network_changed(last_network_index)

    def on_network_changed(self, index):
        """Called when network selection changes"""
        if index < 0:
            return
            
        network_name = self.network_combo.itemData(index)
        base_path = self.base_paths.get(network_name)
        
        if not base_path or not os.path.exists(base_path):
            return
            
        self.robot_combo.clear()
        
        robots = [d for d in os.listdir(base_path) 
                 if d.startswith('robot') and os.path.isdir(os.path.join(base_path, d))]
        
        if not robots:
            return
            
        self.robot_combo.addItems(robots)
        
        # Load last used robot for this network
        last_robot = self.load_setting('last_robot', 'robot1')
        if last_robot in robots:
            self.robot_combo.setCurrentText(last_robot)
        
        # Update current network and robot
        self.current_network = network_name
        self.current_robot = self.robot_combo.currentText()
        
        # Load description for this network/robot combination
        self.load_description_for_robot(network_name, self.current_robot)

    def on_robot_changed(self, robot_name):
        """Called when robot selection changes"""
        if not robot_name or not self.current_network:
            return
            
        self.current_robot = robot_name
        
        # Save current description before changing
        self.save_description()
        
        # Load description for new robot
        self.load_description_for_robot(self.current_network, robot_name)

    def create_button(self, text, color, callback):
        """Create professional button"""
        btn = QPushButton(text)
        btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                min-width: 120px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
            QPushButton:disabled {{
                background-color: #bdc3c7;
            }}
        ''')
        btn.clicked.connect(callback)
        return btn

    def darken_color(self, hex_color, factor=0.8):
        """Darken hex color"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        dark_rgb = tuple(int(c * factor) for c in rgb)
        return f"#{dark_rgb[0]:02x}{dark_rgb[1]:02x}{dark_rgb[2]:02x}"

    def show_no_robot_modal(self):
        """Show professional installation modal"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(self.tr['no_robot_title'])
        msg.setText(self.tr['no_robot_msg'])
        msg.setStandardButtons(QMessageBox.Ok)
        
        # Add custom buttons
        install_btn = msg.addButton(self.tr['install_btn'], QMessageBox.ActionRole)
        browse_btn = msg.addButton(self.tr['browse_btn'], QMessageBox.ActionRole)
        msg.setDefaultButton(QMessageBox.Ok)
        
        install_btn.clicked.connect(self.install_robot)
        browse_btn.clicked.connect(self.browse_for_robot)
        
        msg.exec_()

    def install_robot(self):
        """Guide user to install robot"""
        QMessageBox.information(self, "Installation", 
            "Please create robot directories in one of the network folders:\n"
            "C:/bon (Facebook)\n"
            "C:/wabon (WhatsApp)\n"
            "C:/instabon (Instagram)\n"
            "C:/inbon (LinkedIn)\n"
            "C:/ytbon (YouTube)")

    def browse_for_robot(self):
        """Let user browse for robot location"""
        path = QFileDialog.getExistingDirectory(self, "Select Robot Directory", "C:/")
        if path:
            # Determine which network this path belongs to
            for network_name, base_path in self.base_paths.items():
                if path.startswith(base_path):
                    # Update the base path and rescan
                    self.base_paths[network_name] = os.path.dirname(path)
                    self.scan_networks_and_robots()
                    return
            
            # If not in standard network paths, ask user to select network
            networks = list(self.base_paths.keys())
            network, ok = QInputDialog.getItem(
                self, "Select Network", 
                "Which network does this robot belong to?", 
                networks, 0, False)
            
            if ok and network:
                self.base_paths[network] = path
                self.scan_networks_and_robots()

    def load_setting(self, key, default=None):
        """Load setting from database"""
        self.cursor.execute(f'SELECT {key} FROM settings LIMIT 1')
        result = self.cursor.fetchone()
        return result[0] if result and result[0] is not None else default

    def start_processing(self):
        """Start link processing"""
        selected_network = self.network_combo.currentData()
        selected_robot = self.robot_combo.currentText()
        
        if not selected_network or not selected_robot:
            QMessageBox.warning(self, "Selection Required", "Please select both a network and a robot")
            return
            
        json_path = os.path.join(self.base_paths[selected_network], selected_robot, "data.json")
        if not os.path.exists(json_path):
            QMessageBox.critical(self, self.tr['error_json'], f"JSON file not found in {json_path}")
            return
            
        chrome_path = self.load_setting('chrome_path', 'C:/Program Files/Google/Chrome/Application/chrome.exe')
        if not os.path.exists(chrome_path):
            QMessageBox.critical(self, self.tr['error_chrome'], f"Chrome not found at {chrome_path}")
            return
            
        self.save_settings()
        
        # Initialize UI
        self.start_btn.setEnabled(False)
        self.continue_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.visualization.clear()
        self.status_label.setText(self.tr['status_running'])
        self.status_label.setStyleSheet('color: #27ae60;')
        
        # Start processing thread
        self.link_opener = LinkProcessor(
            json_path, 
            chrome_path,
            self.batch_spin.value()
        )
        self.link_opener.batch_processed.connect(self.on_batch_processed)
        self.link_opener.finished.connect(self.on_processing_finished)
        self.link_opener.error_occurred.connect(self.on_processing_error)
        self.link_opener.start()

    def continue_processing(self):
        """Continue with next batch"""
        if self.link_opener:
            self.continue_btn.setEnabled(False)
            self.status_label.setText(self.tr['status_running'])
            self.status_label.setStyleSheet('color: #27ae60;')
            self.link_opener.resume()

    def stop_processing(self):
        """Stop the processing"""
        if self.link_opener:
            self.link_opener.stop()
            self.status_label.setText(self.tr['status_stopped'])
            self.status_label.setStyleSheet('color: #e74c3c;')
            self.visualization.append("\nProcess stopped by user")

    def on_batch_processed(self, batch_num, links):
        """Handle processed batch"""
        self.continue_btn.setEnabled(True)
        self.status_label.setText(self.tr['status_paused'])
        self.status_label.setStyleSheet('color: #f39c12;')
        
        # Update batch info
        self.batch_label.setText(
            self.tr['group_opened'].format(batch_num, len(links)))
        
        # Add to visualization
        self.visualization.append(f"\n=== Batch {batch_num} ===")
        for link in links:
            self.visualization.append(f"• {link[:80]}...")
        self.visualization.append("\nClick 'Continue' for next batch")
        
        # Auto-scroll
        scrollbar = self.visualization.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def on_processing_finished(self):
        """Handle process completion"""
        self.start_btn.setEnabled(True)
        self.continue_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.status_label.setText(self.tr['status_complete'])
        self.status_label.setStyleSheet('color: #27ae60;')
        self.visualization.append("\nAll batches processed successfully")

    def on_processing_error(self, error_msg):
        """Handle processing errors"""
        QMessageBox.critical(self, "Processing Error", error_msg)
        self.on_processing_finished()

    def setup_styles(self):
        """Configure les styles modernes pour l'application"""
        self.setStyleSheet("""
            /* Style général */
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: #f8f9fa;
                color: #333;
            }
            
            /* Titres */
            QLabel {
                color: #495057;
                font-size: 14px;
            }
            
            /* Groupes */
            QGroupBox {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                margin-top: 20px;
                padding-top: 25px;
                background-color: white;
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
            
            /* Boutons */
            QPushButton {
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 14px;
                min-width: 120px;
                transition: all 0.3s;
            }
            
            QPushButton:hover {
                transform: translateY(-1px);
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            
            QPushButton:pressed {
                transform: translateY(1px);
            }
            
            /* Champs de texte */
            QTextEdit, QSpinBox, QComboBox {
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                background-color: white;
                selection-background-color: #4da6ff;
            }
            
            QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
                border: 1px solid #4da6ff;
                box-shadow: 0 0 0 2px rgba(77, 166, 255, 0.2);
            }
            
            /* Zone de visualisation */
            #visualization {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
                color: #495057;
            }
            
            /* Barre de défilement */
            QScrollBar:vertical {
                border: none;
                background: #f1f3f5;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            
            QScrollBar::handle:vertical {
                background: #ced4da;
                min-height: 20px;
                border-radius: 5px;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            /* Status labels */
            .status-ready { color: #6c757d; }
            .status-running { color: #28a745; }
            .status-paused { color: #ffc107; }
            .status-complete { color: #17a2b8; }
            .status-stopped { color: #dc3545; }
            
            /* Boutons spécifiques */
            #start_btn {
                background-color: #28a745;
                color: white;
            }
            
            #start_btn:hover {
                background-color: #218838;
            }
            
            #continue_btn {
                background-color: #17a2b8;
                color: white;
            }
            
            #continue_btn:hover {
                background-color: #138496;
            }
            
            #stop_btn {
                background-color: #dc3545;
                color: white;
            }
            
            #stop_btn:hover {
                background-color: #c82333;
            }
        """)


    def on_network_changed(self, index):
        """Called when network selection changes"""
        # Handle case where signal sends text instead of index
        if isinstance(index, str):
            if index == "":
                return
            index = self.network_combo.findData(index)
            if index < 0:
                return
        
        if index < 0:
            return
            
        network_name = self.network_combo.itemData(index)
        base_path = self.base_paths.get(network_name)
        
        if not base_path or not os.path.exists(base_path):
            return
            
        self.robot_combo.clear()
        
        robots = [d for d in os.listdir(base_path) 
                if d.startswith('robot') and os.path.isdir(os.path.join(base_path, d))]
        
        if not robots:
            return
            
        self.robot_combo.addItems(robots)
        
        # Load last used robot for this network
        last_robot = self.load_setting('last_robot', 'robot1')
        if last_robot in robots:
            self.robot_combo.setCurrentText(last_robot)
        
        # Initialize current_network if not already done
        if not hasattr(self, 'current_network'):
            self.current_network = network_name
        
        # Update current network and robot
        self.current_network = network_name
        self.current_robot = self.robot_combo.currentText()
        
        # Load description for this network/robot combination
        self.load_description_for_robot(network_name, self.current_robot)

    def on_robot_changed(self, robot_name):
        """Called when robot selection changes"""
        # Ensure current_network is initialized
        if not hasattr(self, 'current_network'):
            self.current_network = self.network_combo.currentData()
            
        if not robot_name or not self.current_network:
            return
            
        self.current_robot = robot_name
        
        # Save current description before changing
        self.save_description()
        
        # Load description for new robot
        self.load_description_for_robot(self.current_network, robot_name)


class LinkProcessor(QThread):
    """Professional link processing thread"""
    batch_processed = pyqtSignal(int, list)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, json_path, chrome_path, batch_size):
        super().__init__()
        self.json_path = json_path
        self.chrome_path = chrome_path
        self.batch_size = batch_size
        self._is_paused = False
        self._should_stop = False

    def run(self):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            links = data.get("groups", [])
            total_links = len(links)
            num_batches = (total_links + self.batch_size - 1) // self.batch_size

            for batch_num in range(num_batches):
                if self._should_stop:
                    break

                # Wait if paused
                while self._is_paused:
                    if self._should_stop:
                        break
                    self.msleep(100)

                start_idx = batch_num * self.batch_size
                end_idx = min(start_idx + self.batch_size, total_links)
                current_batch = links[start_idx:end_idx]

                # Open links in batch
                for link in current_batch:
                    subprocess.Popen([self.chrome_path, link], shell=True)

                # Emit signal
                self.batch_processed.emit(batch_num + 1, current_batch)

                # Pause between batches (except last)
                if batch_num < num_batches - 1 and not self._should_stop:
                    self._is_paused = True

        except Exception as e:
            self.error_occurred.emit(f"Processing error: {str(e)}")
        finally:
            self.finished.emit()

    def pause(self):
        """Pause the processing"""
        self._is_paused = True

    def resume(self):
        """Resume processing"""
        self._is_paused = False

    def stop(self):
        """Stop processing"""
        self._should_stop = True
        self._is_paused = False















import json
import os
import subprocess
import sqlite3
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextEdit, 
                            QPushButton, QFrame, QHBoxLayout, QScrollArea,
                            QGroupBox, QProgressBar, QSpinBox, QMessageBox,
                            QComboBox, QFileDialog, QInputDialog)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QLinearGradient, QPainter
from imports import DB_PATH_notes

class DescriptionManager1(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tr = self.init_translations()
        self.base_paths = {
            "bon": "C:/bon",
            "wabon": "C:/wabon",
            "instabon": "C:/instabon",
            "inbon": "C:/inbon",
            "ytbon": "C:/ytbon"
        }
        self.setup_database()
        self.init_ui()
        self.scan_networks_and_robots()
        self.link_opener = None
        self.env_processor = None
        self.setup_styles()
        self.current_robot = None
        self.current_network = None
        self.current_mode = None  # 'links' ou 'env'

    def setup_styles(self):
        """Configure les styles modernes pour l'application"""
        self.setStyleSheet("""
            /* Style général */
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: #f8f9fa;
                color: #333;
            }
            
            /* Titres */
            QLabel {
                color: #495057;
                font-size: 14px;
            }
            
            /* Groupes */
            QGroupBox {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                margin-top: 20px;
                padding-top: 25px;
                background-color: white;
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
            
            /* Boutons */
            QPushButton {
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 14px;
                min-width: 120px;
                transition: all 0.3s;
            }
            
            QPushButton:hover {
                transform: translateY(-1px);
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            
            QPushButton:pressed {
                transform: translateY(1px);
            }
            
            /* Champs de texte */
            QTextEdit, QSpinBox, QComboBox {
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                background-color: white;
                selection-background-color: #4da6ff;
            }
            
            QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
                border: 1px solid #4da6ff;
                box-shadow: 0 0 0 2px rgba(77, 166, 255, 0.2);
            }
            
            /* Zone de visualisation */
            #visualization {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
                color: #495057;
            }
            
            /* Barre de défilement */
            QScrollBar:vertical {
                border: none;
                background: #f1f3f5;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            
            QScrollBar::handle:vertical {
                background: #ced4da;
                min-height: 20px;
                border-radius: 5px;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            /* Status labels */
            .status-ready { color: #6c757d; }
            .status-running { color: #28a745; }
            .status-paused { color: #ffc107; }
            .status-complete { color: #17a2b8; }
            .status-stopped { color: #dc3545; }
            
            /* Boutons spécifiques */
            #start_btn {
                background-color: #28a745;
                color: white;
            }
            
            #start_btn:hover {
                background-color: #218838;
            }
            
            #continue_btn {
                background-color: #17a2b8;
                color: white;
            }
            
            #continue_btn:hover {
                background-color: #138496;
            }
            
            #stop_btn {
                background-color: #dc3545;
                color: white;
            }
            
            #stop_btn:hover {
                background-color: #c82333;
            }
        """)


    def init_translations(self):
        """Initialize translations"""
        return {
            'window_title': "Robot Manager Pro",
            'no_robot_title': "No Robot Installed",
            'no_robot_msg': "No robot detected. Please install at least one robot.",
            'config_group': "Configuration",
            'group_size_label': "Batch size:",
            'description_label': "Content:",
            'description_placeholder': "Enter your content here...",
            'exec_group': "Execution",
            'start_btn': "Start Links",
            'start_env_btn': "Start Env",
            'continue_btn': "Continue",
            'pause_btn': "Pause",
            'stop_btn': "Stop",
            'status_ready': "Ready",
            'status_running': "Running...",
            'status_paused': "Paused",
            'status_complete': "Completed",
            'status_stopped': "Stopped",
            'network_select_label': "Network:",
            'robot_select_label': "Robot:",
            'batch_opened': "Batch {} - {} items",
            'error_file': "File not found",
            'install_btn': "Install Robot",
            'browse_btn': "Browse",
            'visualization_placeholder': "Execution log will appear here..."
        }

    def setup_database(self):
        """Initialize database connection"""
        self.conn = sqlite3.connect(DB_PATH_notes)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_size INTEGER DEFAULT 10,
                last_description TEXT,
                last_robot TEXT,
                last_network TEXT,
                chrome_path TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS autredescription (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                network_name TEXT NOT NULL,
                robot_name TEXT NOT NULL,
                description TEXT,
                UNIQUE(network_name, robot_name)
            )
        ''')
    
        self.cursor.execute('SELECT COUNT(*) FROM settings')
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute('''
                INSERT INTO settings (group_size, chrome_path) 
                VALUES (10, 'C:/Program Files/Google/Chrome/Application/chrome.exe')
            ''')
            self.conn.commit()

    def save_description(self):
        """Save description automatically"""
        description = self.desc_edit.toPlainText()
        robot_name = self.robot_combo.currentText()
        network_name = self.network_combo.currentData()
        
        if robot_name == "robot1" and network_name == "bon":
            self.cursor.execute('UPDATE settings SET last_description = ? WHERE id = 1', (description,))
        else:
            self.cursor.execute('''
                INSERT OR REPLACE INTO autredescription (network_name, robot_name, description)
                VALUES (?, ?, ?)
            ''', (network_name, robot_name, description))
        
        self.conn.commit()
    
    def save_description(self):
        """Sauvegarde automatiquement la description dans la base de données"""
        description = self.desc_edit.toPlainText()
        robot_name = self.robot_combo.currentText()
        network_name = self.network_combo.currentData()  # Use currentData() instead of currentText()
        
        if not network_name:  # Add validation
            return
            
        if robot_name == "robot1" and network_name == "bon":
            # Sauvegarde dans la table settings pour robot1 sur bon
            self.cursor.execute('''
                UPDATE settings 
                SET last_description = ?
                WHERE id = 1
            ''', (description,))
        else:
            # Sauvegarde dans la table autredescription pour les autres robots
            self.cursor.execute('''
                INSERT OR REPLACE INTO autredescription (network_name, robot_name, description)
                VALUES (?, ?, ?)
            ''', (network_name, robot_name, description))
        
        self.conn.commit()
        
    def load_description_for_robot(self, network_name, robot_name):
        """Load description for selected robot"""
        if robot_name == "robot1" and network_name == "bon":
            self.cursor.execute('SELECT last_description FROM settings LIMIT 1')
            result = self.cursor.fetchone()
            description = result[0] if result and result[0] is not None else ""
        else:
            self.cursor.execute('''
                SELECT description FROM autredescription 
                WHERE network_name = ? AND robot_name = ?
            ''', (network_name, robot_name))
            result = self.cursor.fetchone()
            description = result[0] if result else ""
        
        self.desc_edit.setPlainText(description)

    def save_settings(self):
        """Save settings"""
        self.cursor.execute('''
            UPDATE settings 
            SET group_size = ?,
                last_robot = ?,
                last_network = ?
            WHERE id = 1
        ''', (
            self.batch_spin.value(),
            self.robot_combo.currentText(),
            self.network_combo.currentData()
        ))
        self.conn.commit()

    def closeEvent(self, event):
        """Cleanup on close"""
        if self.link_opener and self.link_opener.isRunning():
            self.link_opener.stop()
            self.link_opener.wait(1000)
        
        if self.env_processor and self.env_processor.isRunning():
            self.env_processor.stop()
            self.env_processor.wait(1000)
        
        self.conn.close()
        super().closeEvent(event)

    def load_description(self):
        """Load description from database"""
        last_network = self.load_setting('last_network', 'bon')
        last_robot = self.load_setting('last_robot', 'robot1')
        self.load_description_for_robot(last_network, last_robot)

    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle(self.tr['window_title'])
        self.setFixedSize(1000, 800)

        # Main styling
        self.setStyleSheet('''
            QWidget {
                font-family: "Segoe UI", Arial, sans-serif;
                background-color: #f5f7fa;
            }
            QGroupBox {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 20px;
                font-weight: bold;
                color: #2c3e50;
                background-color: white;
                font-size: 14px;
            }
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 12px;
                font-size: 14px;
                background-color: #ffffff;
            }
            QComboBox, QSpinBox {
                border: 2px solid #00ffff;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 14px;
                min-width: 150px;
                background-color: #ffffff;
            }
            QLabel {
                color: #34495e;
                font-size: 13px;
            }
        ''')

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Configuration group
        config_group = QGroupBox(self.tr['config_group'])
        config_layout = QVBoxLayout()

        # Network and robot selection
        selection_line = QHBoxLayout()

        # Network selection
        network_layout = QVBoxLayout()
        network_label = QLabel(self.tr['network_select_label'])
        self.network_combo = QComboBox()
        self.network_combo.currentTextChanged.connect(self.on_network_changed)
        network_layout.addWidget(network_label)
        network_layout.addWidget(self.network_combo)

        # Robot selection
        robot_layout = QVBoxLayout()
        robot_label = QLabel(self.tr['robot_select_label'])
        self.robot_combo = QComboBox()
        self.robot_combo.currentTextChanged.connect(self.on_robot_changed)
        robot_layout.addWidget(robot_label)
        robot_layout.addWidget(self.robot_combo)

        # Batch size
        batch_layout = QVBoxLayout()
        batch_label = QLabel(self.tr['group_size_label'])
        self.batch_spin = QSpinBox()
        self.batch_spin.setRange(1, 50)
        self.batch_spin.setValue(self.load_setting('group_size', 10))
        batch_layout.addWidget(batch_label)
        batch_layout.addWidget(self.batch_spin)

        selection_line.addLayout(network_layout)
        selection_line.addSpacing(20)
        selection_line.addLayout(robot_layout)
        selection_line.addSpacing(20)
        selection_line.addLayout(batch_layout)
        selection_line.addStretch()

        # Content editor
        desc_layout = QVBoxLayout()
        desc_label = QLabel(self.tr['description_label'])
        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText(self.tr['description_placeholder'])
        self.desc_edit.setMinimumHeight(120)
        self.desc_edit.textChanged.connect(self.save_description)
        self.load_description()

        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_edit)

        # Add to config group
        config_layout.addLayout(selection_line)
        config_layout.addSpacing(15)
        config_layout.addLayout(desc_layout, 1)
        config_group.setLayout(config_layout)

        # Execution group
        exec_group = QGroupBox(self.tr['exec_group'])
        exec_layout = QVBoxLayout()

        # Control buttons
        control_layout = QHBoxLayout()
        self.start_btn = self.create_button(self.tr['start_btn'], "#2ecc71", self.start_link_processing)
        self.start_env_btn = self.create_button(self.tr['start_env_btn'], "#9b59b6", self.start_env_processing)
        self.pause_btn = self.create_button(self.tr['pause_btn'], "#f39c12", self.toggle_pause)
        self.stop_btn = self.create_button(self.tr['stop_btn'], "#e74c3c", self.stop_processing)

        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)

        control_layout.addStretch()
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.start_env_btn)
        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addStretch()

        # Status display
        self.status_label = QLabel(self.tr['status_ready'])
        self.status_label.setStyleSheet('font-weight: bold; color: #7f8c8d; font-size: 14px;')

        self.batch_label = QLabel()
        self.batch_label.setStyleSheet('color: #95a5a6; font-size: 13px;')

        # Log area
        self.visualization = QTextEdit()
        self.visualization.setReadOnly(True)
        self.visualization.setStyleSheet('''
            QTextEdit {
                background-color: #f9f9f9;
                border: 2px dashed #ddd;
                border-radius: 8px;
                color: #555;
                font-size: 13px;
                min-height: 200px;
                padding: 15px;
            }
        ''')
        self.visualization.setPlaceholderText(self.tr['visualization_placeholder'])

        # Add to execution group
        exec_layout.addLayout(control_layout)
        exec_layout.addWidget(self.status_label)
        exec_layout.addWidget(self.batch_label)
        exec_layout.addWidget(self.visualization, 1)
        exec_group.setLayout(exec_layout)
        
        self.network_combo.addItem(display_name, network_name)  # display_name is what's shown, network_name is the actual value
       # Assemble main layout
        main_layout.addWidget(config_group, 1)
        main_layout.addWidget(exec_group, 2)
        self.setLayout(main_layout)
    def on_network_changed(self, index):
        """Called when network selection changes"""
        # Handle case where signal sends text instead of index
        if isinstance(index, str):
            if index == "":
                return
            index = self.network_combo.findData(index)
            if index < 0:
                return
        
        if index < 0:
            return
            
        network_name = self.network_combo.itemData(index)
        base_path = self.base_paths.get(network_name)
        
        if not base_path or not os.path.exists(base_path):
            return
            
        self.robot_combo.clear()
        
        robots = [d for d in os.listdir(base_path) 
                if d.startswith('robot') and os.path.isdir(os.path.join(base_path, d))]
        
        if not robots:
            return
            
        self.robot_combo.addItems(robots)
        
        # Load last used robot for this network
        last_robot = self.load_setting('last_robot', 'robot1')
        if last_robot in robots:
            self.robot_combo.setCurrentText(last_robot)
        
        # Initialize current_network if not already done
        if not hasattr(self, 'current_network'):
            self.current_network = network_name
        
        # Update current network and robot
        self.current_network = network_name
        self.current_robot = self.robot_combo.currentText()
        
        # Load description for this network/robot combination
        self.load_description_for_robot(network_name, self.current_robot)

    def on_robot_changed(self, robot_name):
        """Called when robot selection changes"""
        # Ensure current_network is initialized
        if not hasattr(self, 'current_network'):
            self.current_network = self.network_combo.currentData()
            
        if not robot_name or not self.current_network:
            return
            
        self.current_robot = robot_name
        
        # Save current description before changing
        self.save_description()
        
        # Load description for new robot
        self.load_description_for_robot(self.current_network, robot_name)

    def scan_networks_and_robots(self):
        """Scan for available networks and robots"""
        self.network_combo.clear()
        self.robot_combo.clear()
        
        available_networks = []
        
        for network_name, base_path in self.base_paths.items():
            if os.path.exists(base_path):
                robots = [d for d in os.listdir(base_path) 
                         if d.startswith('robot') and os.path.isdir(os.path.join(base_path, d))]
                
                if robots:
                    display_name = {
                        'bon': 'Facebook',
                        'wabon': 'WhatsApp',
                        'instabon': 'Instagram',
                        'inbon': 'LinkedIn',
                        'ytbon': 'YouTube'
                    }.get(network_name, network_name)
                    
                    available_networks.append((network_name, display_name, robots))
        
        if not available_networks:
            self.show_no_robot_modal()
            return
            
        # Add networks to combo box
        for network_name, display_name, robots in available_networks:
            self.network_combo.addItem(display_name, network_name)
        
        # Load last used network
        last_network = self.load_setting('last_network', 'bon')
        last_network_index = max(0, self.network_combo.findData(last_network))
        self.network_combo.setCurrentIndex(last_network_index)
        
        # This will trigger on_network_changed to populate robots
        self.on_network_changed(last_network_index)

    def on_network_changed(self, index):
        """Handle network selection change"""
        if index < 0:
            return
            
        network_name = self.network_combo.itemData(index)
        base_path = self.base_paths.get(network_name)
        
        if not base_path or not os.path.exists(base_path):
            return
            
        self.robot_combo.clear()
        
        robots = [d for d in os.listdir(base_path) 
                 if d.startswith('robot') and os.path.isdir(os.path.join(base_path, d))]
        
        if not robots:
            return
            
        self.robot_combo.addItems(robots)
        
        # Load last used robot for this network
        last_robot = self.load_setting('last_robot', 'robot1')
        if last_robot in robots:
            self.robot_combo.setCurrentText(last_robot)
        
        # Update current network and robot
        self.current_network = network_name
        self.current_robot = self.robot_combo.currentText()
        
        # Load description for this network/robot combination
        self.load_description_for_robot(network_name, self.current_robot)

    def on_robot_changed(self, robot_name):
        """Handle robot selection change"""
        if not robot_name or not self.current_network:
            return
            
        self.current_robot = robot_name
        
        # Save current description before changing
        self.save_description()
        
        # Load description for new robot
        self.load_description_for_robot(self.current_network, robot_name)

    def create_button(self, text, color, callback):
        """Create styled button"""
        btn = QPushButton(text)
        btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                min-width: 120px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
            QPushButton:disabled {{
                background-color: #bdc3c7;
            }}
        ''')
        btn.clicked.connect(callback)
        return btn

    def darken_color(self, hex_color, factor=0.8):
        """Darken color"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        dark_rgb = tuple(int(c * factor) for c in rgb)
        return f"#{dark_rgb[0]:02x}{dark_rgb[1]:02x}{dark_rgb[2]:02x}"

    def show_no_robot_modal(self):
        """Show installation modal"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(self.tr['no_robot_title'])
        msg.setText(self.tr['no_robot_msg'])
        msg.setStandardButtons(QMessageBox.Ok)
        
        install_btn = msg.addButton(self.tr['install_btn'], QMessageBox.ActionRole)
        browse_btn = msg.addButton(self.tr['browse_btn'], QMessageBox.ActionRole)
        msg.setDefaultButton(QMessageBox.Ok)
        
        install_btn.clicked.connect(self.install_robot)
        browse_btn.clicked.connect(self.browse_for_robot)
        
        msg.exec_()

    def install_robot(self):
        """Guide user to install robot"""
        QMessageBox.information(self, "Installation", 
            "Please create robot directories in one of the network folders:\n"
            "C:/bon (Facebook)\n"
            "C:/wabon (WhatsApp)\n"
            "C:/instabon (Instagram)\n"
            "C:/inbon (LinkedIn)\n"
            "C:/ytbon (YouTube)")

    def browse_for_robot(self):
        """Let user browse for robot location"""
        path = QFileDialog.getExistingDirectory(self, "Select Robot Directory", "C:/")
        if path:
            for network_name, base_path in self.base_paths.items():
                if path.startswith(base_path):
                    self.base_paths[network_name] = os.path.dirname(path)
                    self.scan_networks_and_robots()
                    return
            
            networks = list(self.base_paths.keys())
            network, ok = QInputDialog.getItem(
                self, "Select Network", 
                "Which network does this robot belong to?", 
                networks, 0, False)
            
            if ok and network:
                self.base_paths[network] = path
                self.scan_networks_and_robots()

    def load_setting(self, key, default=None):
        """Load setting from database"""
        self.cursor.execute(f'SELECT {key} FROM settings LIMIT 1')
        result = self.cursor.fetchone()
        return result[0] if result and result[0] is not None else default

    def start_link_processing(self):
        """Start processing links"""
        self.current_mode = 'links'
        selected_network = self.network_combo.currentData()
        selected_robot = self.robot_combo.currentText()
        
        if not selected_network or not selected_robot:
            QMessageBox.warning(self, "Selection Required", "Please select both a network and a robot")
            return
            
        json_path = os.path.join(self.base_paths[selected_network], selected_robot, "data.json")
        if not os.path.exists(json_path):
            QMessageBox.critical(self, self.tr['error_file'], f"JSON file not found in {json_path}")
            return
            
        chrome_path = self.load_setting('chrome_path', 'C:/Program Files/Google/Chrome/Application/chrome.exe')
        if not os.path.exists(chrome_path):
            QMessageBox.critical(self, self.tr['error_file'], f"Chrome not found at {chrome_path}")
            return
            
        self.save_settings()
        
        # Initialize UI
        self.start_btn.setEnabled(False)
        self.start_env_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        self.visualization.clear()
        self.status_label.setText(self.tr['status_running'])
        self.status_label.setStyleSheet('color: #27ae60;')
        
        # Start processing thread
        self.link_opener = LinkProcessor(
            json_path, 
            chrome_path,
            self.batch_spin.value()
        )
        self.link_opener.batch_processed.connect(self.on_batch_processed)
        self.link_opener.finished.connect(self.on_processing_finished)
        self.link_opener.error_occurred.connect(self.on_processing_error)
        self.link_opener.start()

    def start_env_processing(self):
        """Start environment processing"""
        self.current_mode = 'env'
        selected_network = self.network_combo.currentData()
        selected_robot = self.robot_combo.currentText()
        
        if not selected_network or not selected_robot:
            QMessageBox.warning(self, "Selection Required", "Please select both a network and a robot")
            return
            
        base_path = self.base_paths[selected_network]
        robot_path = os.path.join(base_path, selected_robot)
        
        # Determine script name based on network
        script_mapping = {
            "bon": "__post_in_groups__.py",
            "wabon": "__post_in_whatsapp__.py",
            "instabon": "__post_in_instagram__.py",
            "inbon": "__post_in_linkedin__.py",
            "ytbon": "__post_in_youtube__.py"
        }
        
        script_name = script_mapping.get(selected_network, "__post_in_groups__.py")
        env_path = os.path.join(robot_path, "env1")
        script_path = os.path.join(robot_path, script_name)
        
        # Check if files exist
        if not os.path.exists(env_path):
            QMessageBox.critical(self, "Error", f"Environment not found at {env_path}")
            return
            
        if not os.path.exists(script_path):
            QMessageBox.critical(self, "Error", f"Script not found at {script_path}")
            return
        
        self.save_settings()
        
        # Initialize UI
        self.start_btn.setEnabled(False)
        self.start_env_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        self.visualization.clear()
        self.status_label.setText(self.tr['status_running'])
        self.status_label.setStyleSheet('color: #9b59b6;')
        
        # Start processing thread
        self.env_processor = EnvProcessor(
            env_path,
            script_path,
            self.batch_spin.value()
        )
        self.env_processor.status_updated.connect(self.on_env_status_updated)
        self.env_processor.finished.connect(self.on_processing_finished)
        self.env_processor.error_occurred.connect(self.on_processing_error)
        self.env_processor.start()
        
        # Initial log
        self.visualization.append(f"Starting environment for {selected_robot} on {selected_network}")
        self.visualization.append(f"• Environment: {env_path}")
        self.visualization.append(f"• Script: {script_name}")

    def toggle_pause(self):
        """Toggle pause/resume for current process"""
        if self.current_mode == 'links' and self.link_opener:
            if self.link_opener.is_paused():
                self.link_opener.resume()
                self.pause_btn.setText(self.tr['pause_btn'])
                self.status_label.setText(self.tr['status_running'])
                self.status_label.setStyleSheet('color: #27ae60;' if self.current_mode == 'links' else 'color: #9b59b6;')
            else:
                self.link_opener.pause()
                self.pause_btn.setText(self.tr['continue_btn'])
                self.status_label.setText(self.tr['status_paused'])
                self.status_label.setStyleSheet('color: #f39c12;')
        
        elif self.current_mode == 'env' and self.env_processor:
            if self.env_processor.is_paused():
                self.env_processor.resume()
                self.pause_btn.setText(self.tr['pause_btn'])
                self.status_label.setText(self.tr['status_running'])
                self.status_label.setStyleSheet('color: #9b59b6;')
            else:
                self.env_processor.pause()
                self.pause_btn.setText(self.tr['continue_btn'])
                self.status_label.setText(self.tr['status_paused'])
                self.status_label.setStyleSheet('color: #f39c12;')

    def stop_processing(self):
        """Stop current processing"""
        if self.current_mode == 'links' and self.link_opener:
            self.link_opener.stop()
            self.status_label.setText(self.tr['status_stopped'])
            self.status_label.setStyleSheet('color: #e74c3c;')
            self.visualization.append("\nProcess stopped by user")
        
        elif self.current_mode == 'env' and self.env_processor:
            self.env_processor.stop()
            self.status_label.setText(self.tr['status_stopped'])
            self.status_label.setStyleSheet('color: #e74c3c;')
            self.visualization.append("\nEnvironment stopped by user")

    def on_batch_processed(self, batch_num, links):
        """Handle processed batch"""
        self.pause_btn.setText(self.tr['continue_btn'])
        self.pause_btn.setEnabled(True)
        self.status_label.setText(self.tr['status_paused'])
        self.status_label.setStyleSheet('color: #f39c12;')
        
        self.batch_label.setText(
            self.tr['batch_opened'].format(batch_num, len(links)))
        
        self.visualization.append(f"\n=== Batch {batch_num} ===")
        for link in links:
            self.visualization.append(f"• Processing link...")
        
        scrollbar = self.visualization.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def on_env_status_updated(self, message):
        """Handle environment status updates"""
        self.visualization.append(f"• {message}")
        scrollbar = self.visualization.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def on_processing_finished(self):
        """Handle process completion"""
        self.start_btn.setEnabled(True)
        self.start_env_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.status_label.setText(self.tr['status_complete'])
        self.status_label.setStyleSheet('color: #27ae60;' if self.current_mode == 'links' else 'color: #9b59b6;')
        self.visualization.append("\nProcess completed successfully")

    def on_processing_error(self, error_msg):
        """Handle processing errors"""
        QMessageBox.critical(self, "Processing Error", error_msg)
        self.on_processing_finished()


class LinkProcessor(QThread):
    """Thread for processing links"""
    batch_processed = pyqtSignal(int, list)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, json_path, chrome_path, batch_size):
        super().__init__()
        self.json_path = json_path
        self.chrome_path = chrome_path
        self.batch_size = batch_size
        self._is_paused = False
        self._should_stop = False

    def run(self):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            links = data.get("groups", [])
            total_links = len(links)
            num_batches = (total_links + self.batch_size - 1) // self.batch_size

            for batch_num in range(num_batches):
                if self._should_stop:
                    break

                while self._is_paused:
                    if self._should_stop:
                        break
                    self.msleep(100)

                start_idx = batch_num * self.batch_size
                end_idx = min(start_idx + self.batch_size, total_links)
                current_batch = links[start_idx:end_idx]

                for link in current_batch:
                    subprocess.Popen([self.chrome_path, link], shell=True)

                self.batch_processed.emit(batch_num + 1, current_batch)

                if batch_num < num_batches - 1 and not self._should_stop:
                    self._is_paused = True

        except Exception as e:
            self.error_occurred.emit(f"Processing error: {str(e)}")
        finally:
            self.finished.emit()

    def pause(self):
        self._is_paused = True

    def resume(self):
        self._is_paused = False

    def stop(self):
        self._should_stop = True
        self._is_paused = False

    def is_paused(self):
        return self._is_paused


class EnvProcessor(QThread):
    """Thread for processing environment"""
    status_updated = pyqtSignal(str)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, env_path, script_path, batch_size):
        super().__init__()
        self.env_path = env_path
        self.script_path = script_path
        self.batch_size = batch_size
        self._is_paused = False
        self._should_stop = False
        self.process = None

    def run(self):
        try:
            activate_script = os.path.join(self.env_path, "Scripts", "activate")
            command = f'cmd.exe /k "cd /d {os.path.dirname(activate_script)} && activate && cd /d {os.path.dirname(self.script_path)} && python {self.script_path}"'
            
            self.process = subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.status_updated.emit("Environment started successfully")
            
            while True:
                if self._should_stop:
                    break
                
                while self._is_paused:
                    if self._should_stop:
                        break
                    self.msleep(100)
                
                self.msleep(500)

        except Exception as e:
            self.error_occurred.emit(f"Environment error: {str(e)}")
        finally:
            if self.process:
                self.process.terminate()
            self.finished.emit()

    def pause(self):
        self._is_paused = True
        self.status_updated.emit("Environment paused")

    def resume(self):
        self._is_paused = False
        self.status_updated.emit("Environment resumed")

    def stop(self):
        self._should_stop = True
        self._is_paused = False
        self.status_updated.emit("Stopping environment...")

    def is_paused(self):
        return self._is_paused


class DescriptionManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Left panel
        self.left_panel = DescriptionManager1()

        # Right stacked panel
        self.stacked_right_panel = QStackedWidget()
        self.right_panel1 = MainWindow1()
        self.right_panel2 = SocialMediaPublisher()
        self.stacked_right_panel.addWidget(self.right_panel1)
        self.stacked_right_panel.addWidget(self.right_panel2)
        self.stacked_right_panel.setCurrentIndex(0)

        # Radio buttons
        self.radio1 = QRadioButton("Description")
        self.radio2 = QRadioButton("Status Publisher")
        self.radio1.setChecked(True)

        self.radio1.toggled.connect(lambda: self.stacked_right_panel.setCurrentIndex(0))
        self.radio2.toggled.connect(lambda: self.stacked_right_panel.setCurrentIndex(1))

        # Radio button layout
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio1)
        radio_layout.addWidget(self.radio2)
        radio_layout.addStretch()

        radio_container = QWidget()
        radio_container.setLayout(radio_layout)

        # Right layout
        right_layout = QVBoxLayout()
        right_layout.addWidget(radio_container)
        right_layout.addWidget(self.stacked_right_panel)
        right_layout.setStretch(1, 1)

        right_container = QWidget()
        right_container.setLayout(right_layout)

        # Main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.left_panel, 2)
        main_layout.addWidget(right_container, 3)

        self.setLayout(main_layout)
        self.resize(1200, 700)



import json
import os
import subprocess
import sqlite3
import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextEdit, 
                            QPushButton, QFrame, QHBoxLayout, QScrollArea,
                            QGroupBox, QProgressBar, QSpinBox, QMessageBox,
                            QComboBox, QFileDialog, QInputDialog, QListWidget, 
                            QListWidgetItem, QCalendarWidget, QTabWidget, QDateTimeEdit)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer, QDateTime
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QLinearGradient, QPainter
from imports import DB_PATH_notes
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox

class DescriptionManager1(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tr = self.init_translations()
        self.base_paths = {
            "bon": "C:/bon",
            "wabon": "C:/wabon", 
            "instabon": "C:/instabon",
            "inbon": "C:/inbon",
            "ytbon": "C:/ytbon"
        }
        self.script_display_names = {
            "__post_in_groups__.py": "Post in Groups",
            "__post_in_groupsx__.py": "Multiple Groups",
            "__post_in_comment__.py": "Post Comments",
            "__post_in_whatsapp__.py": "WhatsApp Messages",
            "__post_in_instagram__.py": "Instagram Posts",
            "__post_in_linkedin__.py": "LinkedIn Posts",
            "__post_in_youtube__.py": "YouTube Videos"
        }
        
        # Initialiser le timer avant init_ui()
        self.notification_timer = QTimer()
        
        self.setup_database()
        self.init_ui()
        self.scan_networks_and_robots()
        self.link_opener = None
        self.env_processor = None
        self.setup_styles()
        self.current_robot = None
        self.current_network = None
        self.current_mode = None
        self.scheduled_tasks = []
        
        # Connecter le timer après l'initialisation
        self.notification_timer.timeout.connect(self.check_scheduled_tasks)
        self.notification_timer.start(60000)  # Vérifier toutes les 
        
    def setup_styles(self):
        """Configure les styles modernes pour l'application"""
        self.setStyleSheet("""
            /* Style général */
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: #f8f9fa;
                color: #333;
            }
            
            /* Titres */
            QLabel {
                color: #495057;
                font-size: 14px;
            }
            
            /* Groupes */
            QGroupBox {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                margin-top: 20px;
                padding-top: 25px;
                background-color: white;
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
            
            /* Boutons */
            QPushButton {
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 14px;
                min-width: 120px;
                transition: all 0.3s;
            }
            
            QPushButton:hover {
                transform: translateY(-1px);
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            
            QPushButton:pressed {
                transform: translateY(1px);
            }
            
            /* Champs de texte */
            QTextEdit, QSpinBox, QComboBox {
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                background-color: white;
                selection-background-color: #4da6ff;
            }
            
            QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
                border: 1px solid #4da6ff;
                box-shadow: 0 0 0 2px rgba(77, 166, 255, 0.2);
            }
            
            /* Zone de visualisation */
            #visualization {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
                color: #495057;
            }
            
            /* Barre de défilement */
            QScrollBar:vertical {
                border: none;
                background: #f1f3f5;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            
            QScrollBar::handle:vertical {
                background: #ced4da;
                min-height: 20px;
                border-radius: 5px;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            /* Status labels */
            .status-ready { color: #6c757d; }
            .status-running { color: #28a745; }
            .status-paused { color: #ffc107; }
            .status-complete { color: #17a2b8; }
            .status-stopped { color: #dc3545; }
            
            /* Boutons spécifiques */
            #start_btn {
                background-color: #28a745;
                color: white;
            }
            
            #start_btn:hover {
                background-color: #218838;
            }
            
            #continue_btn {
                background-color: #17a2b8;
                color: white;
            }
            
            #continue_btn:hover {
                background-color: #138496;
            }
            
            #stop_btn {
                background-color: #dc3545;
                color: white;
            }
            
            #stop_btn:hover {
                background-color: #c82333;
            }
        """)


    def init_translations(self):
        """Initialize translations"""
        return {
            'window_title': "Advanced Robot Manager",
            'no_robot_title': "No Robot Installed",
            'no_robot_msg': "No robot detected. Please install at least one robot.",
            'config_group': "Configuration",
            'group_size_label': "Batch size:",
            'description_label': "Content:",
            'description_placeholder': "Enter your content here...",
            'exec_group': "Execution",
            'start_btn': "Start Links",
            'start_env_btn': "Start Env",
            'schedule_btn': "Schedule Task",
            'continue_btn': "Continue",
            'pause_btn': "Pause",
            'stop_btn': "Stop",
            'status_ready': "Ready",
            'status_running': "Running...",
            'status_paused': "Paused",
            'status_complete': "Completed",
            'status_stopped': "Stopped",
            'network_select_label': "Network:",
            'robot_select_label': "Robot:",
            'script_select_label': "Script:",
            'batch_opened': "Batch {} - {} items",
            'error_file': "File not found",
            'install_btn': "Install Robot",
            'browse_btn': "Browse",
            'visualization_placeholder': "Execution log will appear here...",
            'scheduled_tasks': "Scheduled Tasks",
            'task_scheduled': "Task scheduled for {}",
            'notification_msg': "Scheduled task will start in 10 minutes: {}"
        }

    def setup_database(self):
        """Initialize database connection"""
        self.conn = sqlite3.connect(DB_PATH_notes)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_size INTEGER DEFAULT 10,
                last_description TEXT,
                last_robot TEXT,
                last_network TEXT,
                chrome_path TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS autredescription (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                network_name TEXT NOT NULL,
                robot_name TEXT NOT NULL,
                description TEXT,
                UNIQUE(network_name, robot_name)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                network_name TEXT NOT NULL,
                robot_name TEXT NOT NULL,
                script_name TEXT NOT NULL,
                scheduled_time DATETIME NOT NULL,
                status TEXT DEFAULT 'pending'
            )
        ''')
    
        self.cursor.execute('SELECT COUNT(*) FROM settings')
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute('''
                INSERT INTO settings (group_size, chrome_path) 
                VALUES (10, 'C:/Program Files/Google/Chrome/Application/chrome.exe')
            ''')
            self.conn.commit()

    def save_description(self):
        """Save description automatically"""
        description = self.desc_edit.toPlainText()
        robot_name = self.robot_combo.currentText()
        network_name = self.network_combo.currentData()
        
        if not network_name or not robot_name:
            return
            
        if robot_name == "robot1" and network_name == "bon":
            self.cursor.execute('UPDATE settings SET last_description = ? WHERE id = 1', (description,))
        else:
            self.cursor.execute('''
                INSERT OR REPLACE INTO autredescription (network_name, robot_name, description)
                VALUES (?, ?, ?)
            ''', (network_name, robot_name, description))
        
        self.conn.commit()

    def load_description_for_robot(self, network_name, robot_name):
        """Load description for selected robot"""
        if not network_name or not robot_name:
            return
            
        if robot_name == "robot1" and network_name == "bon":
            self.cursor.execute('SELECT last_description FROM settings LIMIT 1')
            result = self.cursor.fetchone()
            description = result[0] if result and result[0] is not None else ""
        else:
            self.cursor.execute('''
                SELECT description FROM autredescription 
                WHERE network_name = ? AND robot_name = ?
            ''', (network_name, robot_name))
            result = self.cursor.fetchone()
            description = result[0] if result else ""
        
        self.desc_edit.setPlainText(description)

    def save_settings(self):
        """Save settings"""
        self.cursor.execute('''
            UPDATE settings 
            SET group_size = ?,
                last_robot = ?,
                last_network = ?
            WHERE id = 1
        ''', (
            self.batch_spin.value(),
            self.robot_combo.currentText(),
            self.network_combo.currentData()
        ))
        self.conn.commit()

    def closeEvent(self, event):
        """Cleanup on close"""
        if self.link_opener and self.link_opener.isRunning():
            self.link_opener.stop()
            self.link_opener.wait(1000)
        
        if self.env_processor and self.env_processor.isRunning():
            self.env_processor.stop()
            self.env_processor.wait(1000)
        
        self.conn.close()
        super().closeEvent(event)

    def load_description(self):
        """Load description from database"""
        last_network = self.load_setting('last_network', 'bon')
        last_robot = self.load_setting('last_robot', 'robot1')
        self.load_description_for_robot(last_network, last_robot)

    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle(self.tr['window_title'])
        self.setFixedSize(1200, 800)

        # Main styling
        self.setStyleSheet('''
            QWidget {
                font-family: "Segoe UI", Arial, sans-serif;
                background-color: #f5f7fa;
            }
            QGroupBox {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 20px;
                font-weight: bold;
                color: #2c3e50;
                background-color: white;
                font-size: 14px;
            }
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 12px;
                font-size: 14px;
                background-color: #ffffff;
            }
            QComboBox, QSpinBox, QDateTimeEdit {
                border: 2px solid #00ffff;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 14px;
                min-width: 150px;
                background-color: #ffffff;
            }
            QLabel {
                color: #34495e;
                font-size: 13px;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QTabBar::tab {
                padding: 8px 16px;
                background: #f1f1f1;
                border: 1px solid #ddd;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #fff;
                border-bottom: 2px solid #4da6ff;
            }
        ''')

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Configuration group
        config_group = QGroupBox(self.tr['config_group'])
        config_layout = QVBoxLayout()

        # Network, robot and script selection
        selection_line = QHBoxLayout()

        # Network selection
        network_layout = QVBoxLayout()
        network_label = QLabel(self.tr['network_select_label'])
        self.network_combo = QComboBox()
        self.network_combo.currentTextChanged.connect(self.on_network_changed)
        network_layout.addWidget(network_label)
        network_layout.addWidget(self.network_combo)

        # Robot selection
        robot_layout = QVBoxLayout()
        robot_label = QLabel(self.tr['robot_select_label'])
        self.robot_combo = QComboBox()
        self.robot_combo.currentTextChanged.connect(self.on_robot_changed)
        robot_layout.addWidget(robot_label)
        robot_layout.addWidget(self.robot_combo)

        # Script selection
        script_layout = QVBoxLayout()
        script_label = QLabel(self.tr['script_select_label'])
        self.script_combo = QComboBox()
        script_layout.addWidget(script_label)
        script_layout.addWidget(self.script_combo)

        # Batch size
        batch_layout = QVBoxLayout()
        batch_label = QLabel(self.tr['group_size_label'])
        self.batch_spin = QSpinBox()
        self.batch_spin.setRange(1, 50)
        self.batch_spin.setValue(self.load_setting('group_size', 10))
        batch_layout.addWidget(batch_label)
        batch_layout.addWidget(self.batch_spin)

        selection_line.addLayout(network_layout)
        selection_line.addSpacing(10)
        selection_line.addLayout(robot_layout)
        selection_line.addSpacing(10)
        selection_line.addLayout(script_layout)
        selection_line.addSpacing(10)
        selection_line.addLayout(batch_layout)
        selection_line.addStretch()

        # Content editor
        desc_layout = QVBoxLayout()
        desc_label = QLabel(self.tr['description_label'])
        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText(self.tr['description_placeholder'])
        self.desc_edit.setMinimumHeight(120)
        self.desc_edit.textChanged.connect(self.save_description)
        self.load_description()

        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_edit)

        # Add to config group
        config_layout.addLayout(selection_line)
        config_layout.addSpacing(15)
        config_layout.addLayout(desc_layout, 1)
        config_group.setLayout(config_layout)

        # Execution group with tabs
        exec_group = QGroupBox(self.tr['exec_group'])
        exec_layout = QVBoxLayout()

        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Current execution tab
        current_tab = QWidget()
        current_layout = QVBoxLayout()
        
        # Control buttons
        control_layout = QHBoxLayout()
        self.start_btn = self.create_button(self.tr['start_btn'], "#2ecc71", self.start_link_processing)
        self.start_env_btn = self.create_button(self.tr['start_env_btn'], "#9b59b6", self.start_env_processing)
        self.schedule_btn = self.create_button(self.tr['schedule_btn'], "#3498db", self.show_schedule_dialog)
        self.pause_btn = self.create_button(self.tr['pause_btn'], "#f39c12", self.toggle_pause)
        self.stop_btn = self.create_button(self.tr['stop_btn'], "#e74c3c", self.stop_processing)

        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)

        control_layout.addStretch()
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.start_env_btn)
        control_layout.addWidget(self.schedule_btn)
        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addStretch()

        # Status display
        self.status_label = QLabel(self.tr['status_ready'])
        self.status_label.setStyleSheet('font-weight: bold; color: #7f8c8d; font-size: 14px;')

        self.batch_label = QLabel()
        self.batch_label.setStyleSheet('color: #95a5a6; font-size: 13px;')

        # Log area
        self.visualization = QTextEdit()
        self.visualization.setReadOnly(True)
        self.visualization.setStyleSheet('''
            QTextEdit {
                background-color: #f9f9f9;
                border: 2px dashed #ddd;
                border-radius: 8px;
                color: #555;
                font-size: 13px;
                min-height: 200px;
                padding: 15px;
            }
        ''')
        self.visualization.setPlaceholderText(self.tr['visualization_placeholder'])

        current_layout.addLayout(control_layout)
        current_layout.addWidget(self.status_label)
        current_layout.addWidget(self.batch_label)
        current_layout.addWidget(self.visualization, 1)
        current_tab.setLayout(current_layout)
        
        # Scheduled tasks tab
        scheduled_tab = QWidget()
        scheduled_layout = QVBoxLayout()
        
        self.scheduled_list = QListWidget()
        self.scheduled_list.setStyleSheet('''
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
        ''')
        
        self.load_scheduled_tasks()
        
        scheduled_layout.addWidget(QLabel(self.tr['scheduled_tasks']))
        scheduled_layout.addWidget(self.scheduled_list, 1)
        scheduled_tab.setLayout(scheduled_layout)
        
        # Add tabs to tab widget
        self.tab_widget.addTab(current_tab, "Current Execution")
        self.tab_widget.addTab(scheduled_tab, "Scheduled Tasks")
        
        # Add tab widget to execution group
        exec_layout.addWidget(self.tab_widget)
        exec_group.setLayout(exec_layout)

        # Assemble main layout
        main_layout.addWidget(config_group, 1)
        main_layout.addWidget(exec_group, 2)
        self.setLayout(main_layout)
        
        # Start notification timer
        self.notification_timer.start(60000)  # Check every minute

    def create_button(self, text, color, callback):
        """Create styled button"""
        btn = QPushButton(text)
        btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                min-width: 120px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
            QPushButton:disabled {{
                background-color: #bdc3c7;
            }}
        ''')
        btn.clicked.connect(callback)
        return btn

    def darken_color(self, hex_color, factor=0.8):
        """Darken color"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        dark_rgb = tuple(int(c * factor) for c in rgb)
        return f"#{dark_rgb[0]:02x}{dark_rgb[1]:02x}{dark_rgb[2]:02x}"

    def scan_networks_and_robots(self):
        """Scan for available networks and robots"""
        self.network_combo.clear()
        self.robot_combo.clear()
        
        available_networks = []
        
        for network_name, base_path in self.base_paths.items():
            if os.path.exists(base_path):
                robots = [d for d in os.listdir(base_path) 
                         if d.startswith('robot') and os.path.isdir(os.path.join(base_path, d))]
                
                if robots:
                    display_name = {
                        'bon': 'Facebook',
                        'wabon': 'WhatsApp',
                        'instabon': 'Instagram',
                        'inbon': 'LinkedIn',
                        'ytbon': 'YouTube'
                    }.get(network_name, network_name)
                    
                    available_networks.append((network_name, display_name, robots))
        
        if not available_networks:
            self.show_no_robot_modal()
            return
            
        # Add networks to combo box
        for network_name, display_name, robots in available_networks:
            self.network_combo.addItem(display_name, network_name)
        
        # Load last used network
        last_network = self.load_setting('last_network', 'bon')
        last_network_index = max(0, self.network_combo.findData(last_network))
        self.network_combo.setCurrentIndex(last_network_index)
        
        # This will trigger on_network_changed to populate robots
        self.on_network_changed(last_network_index)

    def on_network_changed(self, index):
        """Handle network selection change"""
        if index < 0:
            return
            
        network_name = self.network_combo.currentData()
        base_path = self.base_paths.get(network_name)
        
        if not base_path or not os.path.exists(base_path):
            return
            
        self.robot_combo.clear()
        self.script_combo.clear()
        
        robots = [d for d in os.listdir(base_path) 
                 if d.startswith('robot') and os.path.isdir(os.path.join(base_path, d))]
        
        if not robots:
            return
            
        self.robot_combo.addItems(robots)
        
        # Load last used robot for this network
        last_robot = self.load_setting('last_robot', 'robot1')
        if last_robot in robots:
            self.robot_combo.setCurrentText(last_robot)
        
        # Update current network and robot
        self.current_network = network_name
        self.current_robot = self.robot_combo.currentText()
        
        # Load scripts for the selected robot
        self.load_scripts_for_robot()
        
        # Load description for this network/robot combination
        self.load_description_for_robot(network_name, self.current_robot)

    def load_scripts_for_robot(self):
        """Load available scripts for the selected robot"""
        if not self.current_network or not self.current_robot:
            return
            
        robot_path = os.path.join(self.base_paths[self.current_network], self.current_robot)
        if not os.path.exists(robot_path):
            return
            
        self.script_combo.clear()
        
        # List all Python files in the robot directory
        script_files = [f for f in os.listdir(robot_path) 
                       if f.endswith('.py') and os.path.isfile(os.path.join(robot_path, f))]
        
        # Add scripts with display names
        for script in script_files:
            display_name = self.script_display_names.get(script, script)
            self.script_combo.addItem(display_name, script)

    def on_robot_changed(self, robot_name):
        """Handle robot selection change"""
        if not robot_name or not self.current_network:
            return
            
        self.current_robot = robot_name
        
        # Save current description before changing
        self.save_description()
        
        # Load scripts for the new robot
        self.load_scripts_for_robot()
        
        # Load description for new robot
        self.load_description_for_robot(self.current_network, robot_name)

    def show_no_robot_modal(self):
        """Show installation modal"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(self.tr['no_robot_title'])
        msg.setText(self.tr['no_robot_msg'])
        msg.setStandardButtons(QMessageBox.Ok)
        
        install_btn = msg.addButton(self.tr['install_btn'], QMessageBox.ActionRole)
        browse_btn = msg.addButton(self.tr['browse_btn'], QMessageBox.ActionRole)
        msg.setDefaultButton(QMessageBox.Ok)
        
        install_btn.clicked.connect(self.install_robot)
        browse_btn.clicked.connect(self.browse_for_robot)
        
        msg.exec_()

    def install_robot(self):
        """Guide user to install robot"""
        QMessageBox.information(self, "Installation", 
            "Please create robot directories in one of the network folders:\n"
            "C:/bon (Facebook)\n"
            "C:/wabon (WhatsApp)\n"
            "C:/instabon (Instagram)\n"
            "C:/inbon (LinkedIn)\n"
            "C:/ytbon (YouTube)")

    def browse_for_robot(self):
        """Let user browse for robot location"""
        path = QFileDialog.getExistingDirectory(self, "Select Robot Directory", "C:/")
        if path:
            for network_name, base_path in self.base_paths.items():
                if path.startswith(base_path):
                    self.base_paths[network_name] = os.path.dirname(path)
                    self.scan_networks_and_robots()
                    return
            
            networks = list(self.base_paths.keys())
            network, ok = QInputDialog.getItem(
                self, "Select Network", 
                "Which network does this robot belong to?", 
                networks, 0, False)
            
            if ok and network:
                self.base_paths[network] = path
                self.scan_networks_and_robots()

    def load_setting(self, key, default=None):
        """Load setting from database"""
        self.cursor.execute(f'SELECT {key} FROM settings LIMIT 1')
        result = self.cursor.fetchone()
        return result[0] if result and result[0] is not None else default

    def start_link_processing(self):
        """Start processing links"""
        self.current_mode = 'links'
        selected_network = self.network_combo.currentData()
        selected_robot = self.robot_combo.currentText()
        
        if not selected_network or not selected_robot:
            QMessageBox.warning(self, "Selection Required", "Please select both a network and a robot")
            return
            
        json_path = os.path.join(self.base_paths[selected_network], selected_robot, "data.json")
        if not os.path.exists(json_path):
            QMessageBox.critical(self, self.tr['error_file'], f"JSON file not found in {json_path}")
            return
            
        chrome_path = self.load_setting('chrome_path', 'C:/Program Files/Google/Chrome/Application/chrome.exe')
        if not os.path.exists(chrome_path):
            QMessageBox.critical(self, self.tr['error_file'], f"Chrome not found at {chrome_path}")
            return
            
        self.save_settings()
        
        # Initialize UI
        self.start_btn.setEnabled(False)
        self.start_env_btn.setEnabled(False)
        self.schedule_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        self.visualization.clear()
        self.status_label.setText(self.tr['status_running'])
        self.status_label.setStyleSheet('color: #27ae60;')
        
        # Start processing thread
        self.link_opener = LinkProcessor(
            json_path, 
            chrome_path,
            self.batch_spin.value()
        )
        self.link_opener.batch_processed.connect(self.on_batch_processed)
        self.link_opener.finished.connect(self.on_processing_finished)
        self.link_opener.error_occurred.connect(self.on_processing_error)
        self.link_opener.start()

    def start_env_processing(self):
        """Start environment processing"""
        self.current_mode = 'env'
        selected_network = self.network_combo.currentData()
        selected_robot = self.robot_combo.currentText()
        selected_script = self.script_combo.currentData()
        
        if not selected_network or not selected_robot or not selected_script:
            QMessageBox.warning(self, "Selection Required", "Please select network, robot and script")
            return
            
        base_path = self.base_paths[selected_network]
        robot_path = os.path.join(base_path, selected_robot)
        script_path = os.path.join(robot_path, selected_script)
        env_path = os.path.join(robot_path, "env1")
        
        # Check if files exist
        if not os.path.exists(env_path):
            QMessageBox.critical(self, "Error", f"Environment not found at {env_path}")
            return
            
        if not os.path.exists(script_path):
            QMessageBox.critical(self, "Error", f"Script not found at {script_path}")
            return
        
        self.save_settings()
        
        # Initialize UI
        self.start_btn.setEnabled(False)
        self.start_env_btn.setEnabled(False)
        self.schedule_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        self.visualization.clear()
        self.status_label.setText(self.tr['status_running'])
        self.status_label.setStyleSheet('color: #9b59b6;')
        
        # Start processing thread
        self.env_processor = EnvProcessor(
            env_path,
            script_path,
            self.batch_spin.value()
        )
        self.env_processor.status_updated.connect(self.on_env_status_updated)
        self.env_processor.finished.connect(self.on_processing_finished)
        self.env_processor.error_occurred.connect(self.on_processing_error)
        self.env_processor.start()
        
        # Initial log
        self.visualization.append(f"Starting environment for {selected_robot} on {selected_network}")
        self.visualization.append(f"• Environment: {env_path}")
        self.visualization.append(f"• Script: {self.script_combo.currentText()}")

    def show_schedule_dialog(self):
        """Show dialog to schedule a task"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Schedule Task")
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        # Network, robot and script selection
        network_label = QLabel("Network:")
        network_combo = QComboBox()
        for i in range(self.network_combo.count()):
            network_combo.addItem(self.network_combo.itemText(i), self.network_combo.itemData(i))
        
        robot_label = QLabel("Robot:")
        robot_combo = QComboBox()
        robot_combo.addItems([self.robot_combo.itemText(i) for i in range(self.robot_combo.count())])
        
        script_label = QLabel("Script:")
        script_combo = QComboBox()
        for i in range(self.script_combo.count()):
            script_combo.addItem(self.script_combo.itemText(i), self.script_combo.itemData(i))
        
        # Date and time selection
        datetime_label = QLabel("Schedule Date & Time:")
        datetime_edit = QDateTimeEdit()
        datetime_edit.setDateTime(QDateTime.currentDateTime().addSecs(3600))  # Default to 1 hour from now
        datetime_edit.setCalendarPopup(True)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        
        # Add widgets to layout
        layout.addWidget(network_label)
        layout.addWidget(network_combo)
        layout.addWidget(robot_label)
        layout.addWidget(robot_combo)
        layout.addWidget(script_label)
        layout.addWidget(script_combo)
        layout.addWidget(datetime_label)
        layout.addWidget(datetime_edit)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            network = network_combo.currentData()
            robot = robot_combo.currentText()
            script = script_combo.currentData()
            scheduled_time = datetime_edit.dateTime().toString("yyyy-MM-dd HH:mm:ss")
            
            self.schedule_task(network, robot, script, scheduled_time)

    def schedule_task(self, network, robot, script, scheduled_time):
        """Schedule a new task"""
        self.cursor.execute('''
            INSERT INTO scheduled_tasks (network_name, robot_name, script_name, scheduled_time)
            VALUES (?, ?, ?, ?)
        ''', (network, robot, script, scheduled_time))
        self.conn.commit()
        
        # Update UI
        self.load_scheduled_tasks()
        
        # Show confirmation
        QMessageBox.information(self, "Task Scheduled", 
            self.tr['task_scheduled'].format(scheduled_time))

    def load_scheduled_tasks(self):
        """Load scheduled tasks from database"""
        self.scheduled_list.clear()
        self.cursor.execute('''
            SELECT id, network_name, robot_name, script_name, scheduled_time, status 
            FROM scheduled_tasks 
            ORDER BY scheduled_time
        ''')
        
        tasks = self.cursor.fetchall()
        for task in tasks:
            task_id, network, robot, script, scheduled_time, status = task
            display_name = self.script_display_names.get(script, script)
            item_text = f"{network} | {robot} | {display_name} | {scheduled_time} | {status}"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, task_id)
            self.scheduled_list.addItem(item)

    def check_scheduled_tasks(self):
        """Check if any scheduled tasks need to be executed"""
        now = datetime.datetime.now()
        ten_minutes_later = now + datetime.timedelta(minutes=10)
        
        self.cursor.execute('''
            SELECT id, network_name, robot_name, script_name, scheduled_time 
            FROM scheduled_tasks 
            WHERE status = 'pending' 
            AND scheduled_time BETWEEN ? AND ?
        ''', (now.strftime("%Y-%m-%d %H:%M:%S"), ten_minutes_later.strftime("%Y-%m-%d %H:%M:%S")))
        
        tasks = self.cursor.fetchall()
        for task in tasks:
            task_id, network, robot, script, scheduled_time = task
            display_name = self.script_display_names.get(script, script)
            
            # Send notification
            QMessageBox.information(self, "Scheduled Task Notification", 
                self.tr['notification_msg'].format(f"{network} | {robot} | {display_name}"))
            
            # Mark as notified
            self.cursor.execute('''
                UPDATE scheduled_tasks 
                SET status = 'notified' 
                WHERE id = ?
            ''', (task_id,))
            self.conn.commit()
            
            # Reload tasks
            self.load_scheduled_tasks()

    def toggle_pause(self):
        """Toggle pause/resume for current process"""
        if self.current_mode == 'links' and self.link_opener:
            if self.link_opener.is_paused():
                self.link_opener.resume()
                self.pause_btn.setText(self.tr['pause_btn'])
                self.status_label.setText(self.tr['status_running'])
                self.status_label.setStyleSheet('color: #27ae60;' if self.current_mode == 'links' else 'color: #9b59b6;')
            else:
                self.link_opener.pause()
                self.pause_btn.setText(self.tr['continue_btn'])
                self.status_label.setText(self.tr['status_paused'])
                self.status_label.setStyleSheet('color: #f39c12;')
        
        elif self.current_mode == 'env' and self.env_processor:
            if self.env_processor.is_paused():
                self.env_processor.resume()
                self.pause_btn.setText(self.tr['pause_btn'])
                self.status_label.setText(self.tr['status_running'])
                self.status_label.setStyleSheet('color: #9b59b6;')
            else:
                self.env_processor.pause()
                self.pause_btn.setText(self.tr['continue_btn'])
                self.status_label.setText(self.tr['status_paused'])
                self.status_label.setStyleSheet('color: #f39c12;')

    def stop_processing(self):
        """Stop current processing"""
        if self.current_mode == 'links' and self.link_opener:
            self.link_opener.stop()
            self.status_label.setText(self.tr['status_stopped'])
            self.status_label.setStyleSheet('color: #e74c3c;')
            self.visualization.append("\nProcess stopped by user")
        
        elif self.current_mode == 'env' and self.env_processor:
            self.env_processor.stop()
            self.status_label.setText(self.tr['status_stopped'])
            self.status_label.setStyleSheet('color: #e74c3c;')
            self.visualization.append("\nEnvironment stopped by user")

    def on_batch_processed(self, batch_num, links):
        """Handle processed batch"""
        self.pause_btn.setText(self.tr['continue_btn'])
        self.pause_btn.setEnabled(True)
        self.status_label.setText(self.tr['status_paused'])
        self.status_label.setStyleSheet('color: #f39c12;')
        
        self.batch_label.setText(
            self.tr['batch_opened'].format(batch_num, len(links)))
        
        self.visualization.append(f"\n=== Batch {batch_num} ===")
        for link in links:
            self.visualization.append(f"• Processing link...")
        
        scrollbar = self.visualization.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def on_env_status_updated(self, message):
        """Handle environment status updates"""
        self.visualization.append(f"• {message}")
        scrollbar = self.visualization.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def on_processing_finished(self):
        """Handle process completion"""
        self.start_btn.setEnabled(True)
        self.start_env_btn.setEnabled(True)
        self.schedule_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.status_label.setText(self.tr['status_complete'])
        self.status_label.setStyleSheet('color: #27ae60;' if self.current_mode == 'links' else 'color: #9b59b6;')
        self.visualization.append("\nProcess completed successfully")

    def on_processing_error(self, error_msg):
        """Handle processing errors"""
        QMessageBox.critical(self, "Processing Error", error_msg)
        self.on_processing_finished()
    

class LinkProcessor(QThread):
    """Thread for processing links"""
    batch_processed = pyqtSignal(int, list)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, json_path, chrome_path, batch_size):
        super().__init__()
        self.json_path = json_path
        self.chrome_path = chrome_path
        self.batch_size = batch_size
        self._is_paused = False
        self._should_stop = False

    def run(self):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            links = data.get("groups", [])
            total_links = len(links)
            num_batches = (total_links + self.batch_size - 1) // self.batch_size

            for batch_num in range(num_batches):
                if self._should_stop:
                    break

                while self._is_paused:
                    if self._should_stop:
                        break
                    self.msleep(100)

                start_idx = batch_num * self.batch_size
                end_idx = min(start_idx + self.batch_size, total_links)
                current_batch = links[start_idx:end_idx]

                for link in current_batch:
                    subprocess.Popen([self.chrome_path, link], shell=True)

                self.batch_processed.emit(batch_num + 1, current_batch)

                if batch_num < num_batches - 1 and not self._should_stop:
                    self._is_paused = True

        except Exception as e:
            self.error_occurred.emit(f"Processing error: {str(e)}")
        finally:
            self.finished.emit()

    def pause(self):
        self._is_paused = True

    def resume(self):
        self._is_paused = False

    def stop(self):
        self._should_stop = True
        self._is_paused = False

    def is_paused(self):
        return self._is_paused


class EnvProcessor(QThread):
    """Thread for processing environment"""
    status_updated = pyqtSignal(str)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, env_path, script_path, batch_size):
        super().__init__()
        self.env_path = env_path
        self.script_path = script_path
        self.batch_size = batch_size
        self._is_paused = False
        self._should_stop = False
        self.process = None

    def run(self):
        try:
            activate_script = os.path.join(self.env_path, "Scripts", "activate")
            command = f'cmd.exe /k "cd /d {os.path.dirname(activate_script)} && activate && cd /d {os.path.dirname(self.script_path)} && python {self.script_path}"'
            
            self.process = subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.status_updated.emit("Environment started successfully")
            
            while True:
                if self._should_stop:
                    break
                
                while self._is_paused:
                    if self._should_stop:
                        break
                    self.msleep(100)
                
                self.msleep(500)

        except Exception as e:
            self.error_occurred.emit(f"Environment error: {str(e)}")
        finally:
            if self.process:
                self.process.terminate()
            self.finished.emit()

    def pause(self):
        self._is_paused = True
        self.status_updated.emit("Environment paused")

    def resume(self):
        self._is_paused = False
        self.status_updated.emit("Environment resumed")

    def stop(self):
        self._should_stop = True
        self._is_paused = False
        self.status_updated.emit("Stopping environment...")

    def is_paused(self):
        return self._is_paused


class DescriptionManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Left panel
        self.left_panel = DescriptionManager1()

        # Right stacked panel
        self.stacked_right_panel = QStackedWidget()
        self.right_panel1 = MainWindow1()
        self.right_panel2 = SocialMediaPublisher()
        self.stacked_right_panel.addWidget(self.right_panel1)
        self.stacked_right_panel.addWidget(self.right_panel2)
        self.stacked_right_panel.setCurrentIndex(0)

        # Radio buttons
        self.radio1 = QRadioButton("Description")
        self.radio2 = QRadioButton("Status Publisher")
        self.radio1.setChecked(True)

        self.radio1.toggled.connect(lambda: self.stacked_right_panel.setCurrentIndex(0))
        self.radio2.toggled.connect(lambda: self.stacked_right_panel.setCurrentIndex(1))

        # Radio button layout
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio1)
        radio_layout.addWidget(self.radio2)
        radio_layout.addStretch()

        radio_container = QWidget()
        radio_container.setLayout(radio_layout)

        # Right layout
        right_layout = QVBoxLayout()
        right_layout.addWidget(radio_container)
        right_layout.addWidget(self.stacked_right_panel)
        right_layout.setStretch(1, 1)

        right_container = QWidget()
        right_container.setLayout(right_layout)

        # Main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.left_panel, 2)
        main_layout.addWidget(right_container, 3)

        self.setLayout(main_layout)
        self.resize(1200, 700)







if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    manager = DescriptionManager()
    manager.show()
    sys.exit(app.exec_())
    









