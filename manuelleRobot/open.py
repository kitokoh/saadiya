
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
            'start_env_btn': "Start Robot",
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
        # self.setFixedSize(1200, 800)

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
        # dialog.setFixedSize(400, 300)
        
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
        self.radio2 = QRadioButton("Spontane Publisher")
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
        main_layout.addWidget(right_container, 1)

        self.setLayout(main_layout)
        # self.resize(900, 700)







if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    manager = DescriptionManager()
    manager.show()
    sys.exit(app.exec_())
    












import json
import os
import subprocess
import sqlite3
import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextEdit, 
                            QPushButton, QFrame, QHBoxLayout, QScrollArea,
                            QGroupBox, QProgressBar, QSpinBox, QMessageBox,
                            QComboBox, QFileDialog, QInputDialog, QListWidget, 
                            QListWidgetItem, QCalendarWidget, QTabWidget, 
                            QDateTimeEdit, QDialog, QDialogButtonBox, 
                            QStackedWidget, QRadioButton, QCheckBox, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer, QDateTime
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QLinearGradient, QPainter

# Imports des autres modules
DB_PATH_notes = "database.db"  # À remplacer par votre chemin réel
from manuelleRobot.description import MainWindow1
from manuelleRobot.statusmanuelle import SocialMediaPublisher





import json
import os
import subprocess
import sqlite3
import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextEdit, 
                            QPushButton, QFrame, QHBoxLayout, QScrollArea,
                            QGroupBox, QProgressBar, QSpinBox, QMessageBox,
                            QComboBox, QFileDialog, QInputDialog, QListWidget, 
                            QListWidgetItem, QCalendarWidget, QTabWidget, 
                            QDateTimeEdit, QDialog, QDialogButtonBox, 
                            QStackedWidget, QRadioButton, QCheckBox, QSizePolicy,
                            QSplitter)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer, QDateTime
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QLinearGradient, QPainter

# Imports des autres modules
DB_PATH_notes = "database.db"  # À remplacer par votre chemin réel
from manuelleRobot.description import MainWindow1
from manuelleRobot.statusmanuelle import SocialMediaPublisher

class DescriptionManager(QWidget):
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
        
        self.active_tabs = {}  # Pour suivre les onglets actifs
        self.setup_database()
        self.init_ui()
        self.scan_networks_and_robots()
        self.setup_styles()
        
        # Timer pour vérifier les tâches planifiées
        self.scheduler_timer = QTimer(self)
        self.scheduler_timer.timeout.connect(self.check_scheduled_tasks)
        self.scheduler_timer.start(60000)  # Vérifie toutes les minutes
        
        # Timer pour les notifications
        self.notification_timer = QTimer(self)
        self.notification_timer.timeout.connect(self.check_notifications)
        self.notification_timer.start(30000)  # Vérifie toutes les 30 secondes

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
            
            /* Onglets */
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-top: 10px;
            }
            
            QTabBar::tab {
                padding: 8px 16px;
                background: #f1f1f1;
                border: 1px solid #ddd;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            
            QTabBar::tab:selected {
                background: #fff;
                border-bottom: 2px solid #4da6ff;
            }
            
            QTabBar::tab:hover {
                background: #e9e9e9;
            }
            
            /* Radio buttons */
            QRadioButton {
                padding: 5px;
                font-size: 14px;
            }
            
            /* Listes */
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
            
            QListWidget::item:selected {
                background-color: #e1f0fa;
                color: #333;
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
            'start_robot_btn': "Start Robot",
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
            'batch_opened': "Batch {} - {} items",
            'error_file': "File not found",
            'install_btn': "Install Robot",
            'browse_btn': "Browse",
            'visualization_placeholder': "Execution log will appear here...",
            'scheduled_tasks': "Scheduled Tasks",
            'task_scheduled': "Task scheduled for {}",
            'notification_msg': "Scheduled task will start in 10 minutes: {}",
            'task_started': "Task started: {}",
            'task_completed': "Task completed: {}",
            'select_robot_title': "Start New Robot",
            'select_network_label': "Select Network:",
            'select_robot_label': "Select Robot:",
            'select_script_label': "Select Script:",
            'current_tasks': "Current Tasks",
            'scheduled_tasks': "Scheduled Tasks",
            'task_id': "ID",
            'task_network': "Network",
            'task_robot': "Robot",
            'task_script': "Script",
            'task_scheduled_time': "Scheduled Time",
            'task_status': "Status",
            'task_actions': "Actions",
            'action_pause': "Pause",
            'action_resume': "Resume",
            'action_cancel': "Cancel",
            'action_delete': "Delete",
            'repeat_daily': "Repeat Daily",
            'repeat_weekly': "Repeat Weekly",
            'repeat_monthly': "Repeat Monthly"
        }

    def setup_database(self):
        """Initialize database connection"""
        self.conn = sqlite3.connect(DB_PATH_notes)
        self.cursor = self.conn.cursor()
        
        # Table pour les paramètres
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

        # Table pour les descriptions
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS autredescription (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                network_name TEXT NOT NULL,
                robot_name TEXT NOT NULL,
                description TEXT,
                UNIQUE(network_name, robot_name)
            )
        ''')
        
        # Table pour les tâches planifiées
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                network_name TEXT NOT NULL,
                robot_name TEXT NOT NULL,
                script_name TEXT NOT NULL,
                scheduled_time DATETIME NOT NULL,
                repeat_pattern TEXT,
                status TEXT DEFAULT 'pending',
                next_execution DATETIME,
                last_execution DATETIME,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Table pour les tâches en cours
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS active_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                network_name TEXT NOT NULL,
                robot_name TEXT NOT NULL,
                script_name TEXT NOT NULL,
                start_time DATETIME NOT NULL,
                status TEXT DEFAULT 'running',
                process_id INTEGER
            )
        ''')
        
        # Table pour les notifications
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                message TEXT NOT NULL,
                notification_time DATETIME NOT NULL,
                is_read BOOLEAN DEFAULT 0
            )
        ''')
    
        # Insérer les paramètres par défaut si la table est vide
        self.cursor.execute('SELECT COUNT(*) FROM settings')
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute('''
                INSERT INTO settings (group_size, chrome_path) 
                VALUES (10, 'C:/Program Files/Google/Chrome/Application/chrome.exe')
            ''')
            self.conn.commit()

    def init_ui(self):
        """Initialize the main UI"""
        self.setWindowTitle(self.tr['window_title'])
        self.setMinimumSize(1200, 800)
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Left panel - Description Manager
        self.left_panel = self.create_left_panel()
        
        # Right panel - Stacked widgets
        self.right_panel = self.create_right_panel()
        
        # Add panels to main layout
        main_layout.addWidget(self.left_panel, 2)  # 2/3 de l'espace
        main_layout.addWidget(self.right_panel, 1)  # 1/3 de l'espace
        
        self.setLayout(main_layout)
        
        # Charger les données initiales
        self.load_description()
        self.load_scheduled_tasks()
        
    def create_left_panel(self):
        """Create the left panel with configuration and execution tabs"""
        panel = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # Configuration group
        config_group = QGroupBox(self.tr['config_group'])
        config_layout = QVBoxLayout()
        
        # Network and robot selection
        selection_layout = QHBoxLayout()
        
        # Network selection
        network_layout = QVBoxLayout()
        network_label = QLabel(self.tr['network_select_label'])
        self.network_combo = QComboBox()
        self.network_combo.currentIndexChanged.connect(self.on_network_changed)
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
        
        selection_layout.addLayout(network_layout, 1)
        selection_layout.addLayout(robot_layout, 1)
        selection_layout.addLayout(batch_layout, 1)
        
        # Description editor
        desc_layout = QVBoxLayout()
        desc_label = QLabel(self.tr['description_label'])
        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText(self.tr['description_placeholder'])
        self.desc_edit.setMinimumHeight(150)
        self.desc_edit.textChanged.connect(self.save_description)
        
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_edit)
        
        # Add to config group
        config_layout.addLayout(selection_layout)
        config_layout.addLayout(desc_layout, 1)
        config_group.setLayout(config_layout)
        
        # Execution tabs
        self.exec_tabs = QTabWidget()
        self.exec_tabs.setTabsClosable(True)
        self.exec_tabs.tabCloseRequested.connect(self.close_execution_tab)
        
        # Add default tab
        self.add_execution_tab("Links Processing")
        
        # Control buttons
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 10, 0, 0)
        
        self.start_btn = self.create_button(self.tr['start_btn'], "#2ecc71", self.start_link_processing)
        self.schedule_btn = self.create_button(self.tr['schedule_btn'], "#3498db", self.show_schedule_dialog)
        self.start_robot_btn = self.create_button(self.tr['start_robot_btn'], "#9b59b6", self.show_start_robot_dialog)
        
        control_layout.addStretch()
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.schedule_btn)
        control_layout.addWidget(self.start_robot_btn)
        control_layout.addStretch()
        
        # Add to main layout
        layout.addWidget(config_group, 1)
        layout.addWidget(self.exec_tabs, 2)
        layout.addLayout(control_layout)
        
        panel.setLayout(layout)
        return panel
    
    def create_right_panel(self):
        """Create the right panel with stacked widgets"""
        panel = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # Radio buttons to switch between views
        self.radio_description = QRadioButton("Description Editor")
        self.radio_social = QRadioButton("Social Publisher")
        self.radio_description.setChecked(True)
        
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio_description)
        radio_layout.addWidget(self.radio_social)
        radio_layout.addStretch()
        
        # Stacked widget for right panel content
        self.stacked_widget = QStackedWidget()
        
        # Panel 1: Description Editor
        self.description_panel = MainWindow1()
        
        # Panel 2: Social Media Publisher
        self.social_panel = SocialMediaPublisher()
        
        # Add panels to stacked widget
        self.stacked_widget.addWidget(self.description_panel)
        self.stacked_widget.addWidget(self.social_panel)
        
        # Connect radio buttons to stacked widget
        self.radio_description.toggled.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.radio_social.toggled.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        # Scheduled tasks list
        tasks_group = QGroupBox(self.tr['scheduled_tasks'])
        tasks_layout = QVBoxLayout()
        
        self.scheduled_list = QListWidget()
        self.scheduled_list.itemDoubleClicked.connect(self.show_task_details)
        
        # Task control buttons
        task_btn_layout = QHBoxLayout()
        self.pause_task_btn = self.create_button(self.tr['action_pause'], "#f39c12", self.pause_scheduled_task)
        self.resume_task_btn = self.create_button(self.tr['action_resume'], "#2ecc71", self.resume_scheduled_task)
        self.cancel_task_btn = self.create_button(self.tr['action_cancel'], "#e74c3c", self.cancel_scheduled_task)
        self.delete_task_btn = self.create_button(self.tr['action_delete'], "#95a5a6", self.delete_scheduled_task)
        
        task_btn_layout.addWidget(self.pause_task_btn)
        task_btn_layout.addWidget(self.resume_task_btn)
        task_btn_layout.addWidget(self.cancel_task_btn)
        task_btn_layout.addWidget(self.delete_task_btn)
        
        tasks_layout.addWidget(self.scheduled_list, 1)
        tasks_layout.addLayout(task_btn_layout)
        tasks_group.setLayout(tasks_layout)
        
        # Add to main layout
        layout.addLayout(radio_layout)
        layout.addWidget(self.stacked_widget, 1)
        layout.addWidget(tasks_group, 1)
        
        panel.setLayout(layout)
        return panel
    
    def create_button(self, text, color, callback):
        """Create a styled button"""
        btn = QPushButton(text)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
            QPushButton:disabled {{
                background-color: #bdc3c7;
            }}
        """)
        btn.clicked.connect(callback)
        return btn
    
    def darken_color(self, hex_color, factor=0.8):
        """Darken a hex color"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        dark_rgb = tuple(int(c * factor) for c in rgb)
        return f"#{dark_rgb[0]:02x}{dark_rgb[1]:02x}{dark_rgb[2]:02x}"
    
    def add_execution_tab(self, title, content=None):
        """Add a new execution tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Status label
        status_label = QLabel(self.tr['status_ready'])
        status_label.setObjectName("status_label")
        status_label.setStyleSheet("font-weight: bold;")
        
        # Log area
        log_area = QTextEdit()
        log_area.setReadOnly(True)
        log_area.setPlaceholderText(self.tr['visualization_placeholder'])
        log_area.setObjectName("log_area")
        
        # Control buttons
        btn_layout = QHBoxLayout()
        pause_btn = self.create_button(self.tr['pause_btn'], "#f39c12", lambda: self.pause_current_task(self.exec_tabs.currentIndex()))
        stop_btn = self.create_button(self.tr['stop_btn'], "#e74c3c", lambda: self.stop_current_task(self.exec_tabs.currentIndex()))
        
        btn_layout.addStretch()
        btn_layout.addWidget(pause_btn)
        btn_layout.addWidget(stop_btn)
        btn_layout.addStretch()
        
        layout.addWidget(status_label)
        layout.addWidget(log_area, 1)
        layout.addLayout(btn_layout)
        
        tab.setLayout(layout)
        
        # Store tab info
        tab_idx = self.exec_tabs.addTab(tab, title)
        self.exec_tabs.setCurrentIndex(tab_idx)
        
        return tab_idx
    
    def close_execution_tab(self, index):
        """Close an execution tab"""
        if index == 0:  # Don't close the default tab
            return
            
        # Stop any running process for this tab
        self.stop_current_task(index)
        
        # Remove the tab
        self.exec_tabs.removeTab(index)
        
        # Update active_tabs dictionary
        tab_title = self.exec_tabs.tabText(index)
        if tab_title in self.active_tabs:
            del self.active_tabs[tab_title]
    
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
        
        robots = [d for d in os.listdir(base_path) 
                 if d.startswith('robot') and os.path.isdir(os.path.join(base_path, d))]
        
        if not robots:
            return
            
        self.robot_combo.addItems(robots)
        
        # Load last used robot for this network
        last_robot = self.load_setting('last_robot', 'robot1')
        if last_robot in robots:
            self.robot_combo.setCurrentText(last_robot)
        
        # Load description for this network/robot combination
        self.load_description_for_robot(network_name, self.robot_combo.currentText())
    
    def on_robot_changed(self, robot_name):
        """Handle robot selection change"""
        if not robot_name or not self.network_combo.currentData():
            return
            
        # Save current description before changing
        self.save_description()
        
        # Load description for new robot
        self.load_description_for_robot(self.network_combo.currentData(), robot_name)
    
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
    
    def load_setting(self, key, default=None):
        """Load setting from database"""
        self.cursor.execute(f'SELECT {key} FROM settings LIMIT 1')
        result = self.cursor.fetchone()
        return result[0] if result and result[0] is not None else default
    
    def load_description(self):
        """Load description from database"""
        last_network = self.load_setting('last_network', 'bon')
        last_robot = self.load_setting('last_robot', 'robot1')
        self.load_description_for_robot(last_network, last_robot)
    
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
    
    def start_link_processing(self):
        """Start processing links in batches"""
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
            
        # Save settings
        self.cursor.execute('''
            UPDATE settings 
            SET group_size = ?,
                last_robot = ?,
                last_network = ?
            WHERE id = 1
        ''', (
            self.batch_spin.value(),
            selected_robot,
            selected_network
        ))
        self.conn.commit()
        
        # Get the current tab
        current_tab = self.exec_tabs.currentWidget()
        status_label = current_tab.findChild(QLabel, "status_label")
        log_area = current_tab.findChild(QTextEdit, "log_area")
        
        # Initialize UI
        status_label.setText(self.tr['status_running'])
        status_label.setStyleSheet('color: #27ae60;')
        log_area.clear()
        
        # Start processing thread
        processor = LinkProcessor(
            json_path, 
            chrome_path,
            self.batch_spin.value()
        )
        
        # Connect signals
        processor.batch_processed.connect(lambda batch_num, links: self.on_batch_processed(batch_num, links, log_area, status_label))
        processor.finished.connect(lambda: self.on_processing_finished(log_area, status_label))
        processor.error_occurred.connect(lambda msg: self.on_processing_error(msg, log_area, status_label))
        
        # Store processor in active_tabs
        tab_title = self.exec_tabs.tabText(self.exec_tabs.currentIndex())
        self.active_tabs[tab_title] = {
            'processor': processor,
            'type': 'links',
            'status': 'running'
        }
        
        processor.start()
    
    def show_start_robot_dialog(self):
        """Show dialog to start a new robot"""
        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr['select_robot_title'])
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Network selection
        network_layout = QVBoxLayout()
        network_label = QLabel(self.tr['select_network_label'])
        network_combo = QComboBox()
        
        # Populate networks
        for i in range(self.network_combo.count()):
            network_combo.addItem(self.network_combo.itemText(i), self.network_combo.itemData(i))
        
        network_layout.addWidget(network_label)
        network_layout.addWidget(network_combo)
        
        # Robot selection
        robot_layout = QVBoxLayout()
        robot_label = QLabel(self.tr['select_robot_label'])
        robot_combo = QComboBox()
        
        # Populate robots based on selected network
        def update_robots(network_index):
            network_name = network_combo.currentData()
            base_path = self.base_paths.get(network_name)
            
            robot_combo.clear()
            
            if base_path and os.path.exists(base_path):
                robots = [d for d in os.listdir(base_path) 
                         if d.startswith('robot') and os.path.isdir(os.path.join(base_path, d))]
                robot_combo.addItems(robots)
        
        network_combo.currentIndexChanged.connect(update_robots)
        update_robots(0)  # Initial population
        
        robot_layout.addWidget(robot_label)
        robot_layout.addWidget(robot_combo)
        
        # Script selection
        script_layout = QVBoxLayout()
        script_label = QLabel(self.tr['select_script_label'])
        script_combo = QComboBox()
        
        # Populate scripts based on selected robot
        def update_scripts():
            network_name = network_combo.currentData()
            robot_name = robot_combo.currentText()
            
            script_combo.clear()
            
            if network_name and robot_name:
                robot_path = os.path.join(self.base_paths[network_name], robot_name)
                if os.path.exists(robot_path):
                    # List all Python files in the robot directory
                    script_files = [f for f in os.listdir(robot_path) 
                                 if f.endswith('.py') and os.path.isfile(os.path.join(robot_path, f))]
                    
                    # Add scripts with display names
                    for script in script_files:
                        display_name = self.script_display_names.get(script, script)
                        script_combo.addItem(display_name, script)
        
        robot_combo.currentTextChanged.connect(update_scripts)
        update_scripts()  # Initial population
        
        script_layout.addWidget(script_label)
        script_layout.addWidget(script_combo)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        
        # Add to layout
        layout.addLayout(network_layout)
        layout.addLayout(robot_layout)
        layout.addLayout(script_layout)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            network = network_combo.currentData()
            robot = robot_combo.currentText()
            script = script_combo.currentData()
            
            if network and robot and script:
                self.start_robot_processing(network, robot, script)
    
    def start_robot_processing(self, network, robot, script):
        """Start processing with the selected robot and script"""
        base_path = self.base_paths[network]
        robot_path = os.path.join(base_path, robot)
        script_path = os.path.join(robot_path, script)
        env_path = os.path.join(robot_path, "env1")
        
        # Check if files exist
        if not os.path.exists(env_path):
            QMessageBox.critical(self, "Error", f"Environment not found at {env_path}")
            return
            
        if not os.path.exists(script_path):
            QMessageBox.critical(self, "Error", f"Script not found at {script_path}")
            return
        
        # Create a new tab for this execution
        tab_title = f"{network} | {robot} | {self.script_display_names.get(script, script)}"
        tab_idx = self.add_execution_tab(tab_title)
        
        # Get the tab widgets
        current_tab = self.exec_tabs.widget(tab_idx)
        status_label = current_tab.findChild(QLabel, "status_label")
        log_area = current_tab.findChild(QTextEdit, "log_area")
        
        # Initialize UI
        status_label.setText(self.tr['status_running'])
        status_label.setStyleSheet('color: #9b59b6;')
        log_area.clear()
        
        # Start processing thread
        processor = EnvProcessor(
            env_path,
            script_path,
            self.batch_spin.value()
        )
        
        # Connect signals
        processor.status_updated.connect(lambda msg: self.on_env_status_updated(msg, log_area))
        processor.finished.connect(lambda: self.on_processing_finished(log_area, status_label))
        processor.error_occurred.connect(lambda msg: self.on_processing_error(msg, log_area, status_label))
        
        # Store processor in active_tabs
        self.active_tabs[tab_title] = {
            'processor': processor,
            'type': 'env',
            'status': 'running',
            'network': network,
            'robot': robot,
            'script': script
        }
        
        # Log initial info
        log_area.append(f"Starting environment for {robot} on {network}")
        log_area.append(f"• Environment: {env_path}")
        log_area.append(f"• Script: {self.script_display_names.get(script, script)}")
        
        processor.start()
        
        # Record in database
        self.cursor.execute('''
            INSERT INTO active_tasks (network_name, robot_name, script_name, start_time, status)
            VALUES (?, ?, ?, datetime('now'), 'running')
        ''', (network, robot, script))
        self.conn.commit()
    
    def show_schedule_dialog(self):
        """Show dialog to schedule a new task"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Schedule New Task")
        dialog.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        
        # Network selection
        network_layout = QVBoxLayout()
        network_label = QLabel("Network:")
        network_combo = QComboBox()
        
        # Populate networks
        for i in range(self.network_combo.count()):
            network_combo.addItem(self.network_combo.itemText(i), self.network_combo.itemData(i))
        
        network_layout.addWidget(network_label)
        network_layout.addWidget(network_combo)
        
        # Robot selection
        robot_layout = QVBoxLayout()
        robot_label = QLabel("Robot:")
        robot_combo = QComboBox()
        
        # Populate robots based on selected network
        def update_robots(network_index):
            network_name = network_combo.currentData()
            base_path = self.base_paths.get(network_name)
            
            robot_combo.clear()
            
            if base_path and os.path.exists(base_path):
                robots = [d for d in os.listdir(base_path) 
                         if d.startswith('robot') and os.path.isdir(os.path.join(base_path, d))]
                robot_combo.addItems(robots)
        
        network_combo.currentIndexChanged.connect(update_robots)
        update_robots(0)  # Initial population
        
        robot_layout.addWidget(robot_label)
        robot_layout.addWidget(robot_combo)
        
        # Script selection
        script_layout = QVBoxLayout()
        script_label = QLabel("Script:")
        script_combo = QComboBox()
        
        # Populate scripts based on selected robot
        def update_scripts():
            network_name = network_combo.currentData()
            robot_name = robot_combo.currentText()
            
            script_combo.clear()
            
            if network_name and robot_name:
                robot_path = os.path.join(self.base_paths[network_name], robot_name)
                if os.path.exists(robot_path):
                    # List all Python files in the robot directory
                    script_files = [f for f in os.listdir(robot_path) 
                                 if f.endswith('.py') and os.path.isfile(os.path.join(robot_path, f))]
                    
                    # Add scripts with display names
                    for script in script_files:
                        display_name = self.script_display_names.get(script, script)
                        script_combo.addItem(display_name, script)
        
        robot_combo.currentTextChanged.connect(update_scripts)
        update_scripts()  # Initial population
        
        script_layout.addWidget(script_label)
        script_layout.addWidget(script_combo)
        
        # Schedule time
        time_layout = QVBoxLayout()
        time_label = QLabel("Schedule Time:")
        time_edit = QDateTimeEdit()
        time_edit.setDateTime(QDateTime.currentDateTime().addSecs(3600))  # Default to 1 hour from now
        time_edit.setCalendarPopup(True)
        
        time_layout.addWidget(time_label)
        time_layout.addWidget(time_edit)
        
        # Repeat options
        repeat_group = QGroupBox("Repeat Options")
        repeat_layout = QVBoxLayout()
        
        daily_check = QCheckBox(self.tr['repeat_daily'])
        weekly_check = QCheckBox(self.tr['repeat_weekly'])
        monthly_check = QCheckBox(self.tr['repeat_monthly'])
        
        repeat_layout.addWidget(daily_check)
        repeat_layout.addWidget(weekly_check)
        repeat_layout.addWidget(monthly_check)
        repeat_group.setLayout(repeat_layout)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        
        # Add to main layout
        layout.addLayout(network_layout)
        layout.addLayout(robot_layout)
        layout.addLayout(script_layout)
        layout.addLayout(time_layout)
        layout.addWidget(repeat_group)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            network = network_combo.currentData()
            robot = robot_combo.currentText()
            script = script_combo.currentData()
            scheduled_time = time_edit.dateTime().toString("yyyy-MM-dd HH:mm:ss")
            
            # Determine repeat pattern
            repeat_pattern = ""
            if daily_check.isChecked():
                repeat_pattern = "daily"
            elif weekly_check.isChecked():
                repeat_pattern = "weekly"
            elif monthly_check.isChecked():
                repeat_pattern = "monthly"
            
            self.schedule_task(network, robot, script, scheduled_time, repeat_pattern)
    
    def schedule_task(self, network, robot, script, scheduled_time, repeat_pattern=""):
        """Schedule a new task"""
        self.cursor.execute('''
            INSERT INTO scheduled_tasks 
            (network_name, robot_name, script_name, scheduled_time, repeat_pattern, next_execution)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (network, robot, script, scheduled_time, repeat_pattern, scheduled_time))
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
            WHERE is_active = 1
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
    
    def show_task_details(self, item):
        """Show details of a scheduled task"""
        task_id = item.data(Qt.UserRole)
        
        self.cursor.execute('''
            SELECT * FROM scheduled_tasks WHERE id = ?
        ''', (task_id,))
        task = self.cursor.fetchone()
        
        if not task:
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle("Task Details")
        dialog.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        
        # Display task info
        info_layout = QFormLayout()
        
        info_layout.addRow("Network:", QLabel(task[1]))
        info_layout.addRow("Robot:", QLabel(task[2]))
        info_layout.addRow("Script:", QLabel(self.script_display_names.get(task[3], task[3])))
        info_layout.addRow("Scheduled Time:", QLabel(task[4]))
        info_layout.addRow("Repeat Pattern:", QLabel(task[5] if task[5] else "None"))
        info_layout.addRow("Status:", QLabel(task[6]))
        
        layout.addLayout(info_layout)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(dialog.reject)
        
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        dialog.exec_()
    
    def pause_scheduled_task(self):
        """Pause a scheduled task"""
        selected_items = self.scheduled_list.selectedItems()
        if not selected_items:
            return
            
        for item in selected_items:
            task_id = item.data(Qt.UserRole)
            self.cursor.execute('''
                UPDATE scheduled_tasks 
                SET status = 'paused' 
                WHERE id = ?
            ''', (task_id,))
        
        self.conn.commit()
        self.load_scheduled_tasks()
    
    def resume_scheduled_task(self):
        """Resume a paused scheduled task"""
        selected_items = self.scheduled_list.selectedItems()
        if not selected_items:
            return
            
        for item in selected_items:
            task_id = item.data(Qt.UserRole)
            self.cursor.execute('''
                UPDATE scheduled_tasks 
                SET status = 'pending' 
                WHERE id = ?
            ''', (task_id,))
        
        self.conn.commit()
        self.load_scheduled_tasks()
    
    def cancel_scheduled_task(self):
        """Cancel a scheduled task"""
        selected_items = self.scheduled_list.selectedItems()
        if not selected_items:
            return
            
        for item in selected_items:
            task_id = item.data(Qt.UserRole)
            self.cursor.execute('''
                UPDATE scheduled_tasks 
                SET status = 'cancelled' 
                WHERE id = ?
            ''', (task_id,))
        
        self.conn.commit()
        self.load_scheduled_tasks()
    
    def delete_scheduled_task(self):
        """Delete a scheduled task"""
        selected_items = self.scheduled_list.selectedItems()
        if not selected_items:
            return
            
        reply = QMessageBox.question(
            self, 'Delete Tasks',
            'Are you sure you want to delete the selected tasks?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.No:
            return
            
        for item in selected_items:
            task_id = item.data(Qt.UserRole)
            self.cursor.execute('''
                UPDATE scheduled_tasks 
                SET is_active = 0 
                WHERE id = ?
            ''', (task_id,))
        
        self.conn.commit()
        self.load_scheduled_tasks()
    
    def check_scheduled_tasks(self):
        """Check if any scheduled tasks need to be executed"""
        now = datetime.datetime.now()
        
        self.cursor.execute('''
            SELECT id, network_name, robot_name, script_name, next_execution, repeat_pattern
            FROM scheduled_tasks 
            WHERE status = 'pending' 
            AND is_active = 1
            AND next_execution <= ?
        ''', (now.strftime("%Y-%m-%d %H:%M:%S"),))
        
        tasks = self.cursor.fetchall()
        for task in tasks:
            task_id, network, robot, script, next_execution, repeat_pattern = task
            
            # Start the task
            self.start_robot_processing(network, robot, script)
            
            # Update task status and next execution
            if repeat_pattern:
                # Calculate next execution time based on repeat pattern
                next_exec_dt = datetime.datetime.strptime(next_execution, "%Y-%m-%d %H:%M:%S")
                
                if repeat_pattern == "daily":
                    next_exec_dt += datetime.timedelta(days=1)
                elif repeat_pattern == "weekly":
                    next_exec_dt += datetime.timedelta(weeks=1)
                elif repeat_pattern == "monthly":
                    # Add approximately one month
                    next_exec_dt = next_exec_dt.replace(month=next_exec_dt.month + 1)
                
                next_execution = next_exec_dt.strftime("%Y-%m-%d %H:%M:%S")
            else:
                # One-time task, mark as completed
                next_execution = None
            
            self.cursor.execute('''
                UPDATE scheduled_tasks 
                SET last_execution = ?,
                    next_execution = ?,
                    status = CASE WHEN ? IS NULL THEN 'completed' ELSE 'pending' END
                WHERE id = ?
            ''', (now.strftime("%Y-%m-%d %H:%M:%S"), next_execution, next_execution, task_id))
            
            # Add notification
            self.add_notification(task_id, self.tr['task_started'].format(f"{network} | {robot} | {script}"))
        
        self.conn.commit()
    
    def check_notifications(self):
        """Check for pending notifications"""
        self.cursor.execute('''
            SELECT id, message FROM notifications 
            WHERE is_read = 0
            ORDER BY notification_time
        ''')
        
        notifications = self.cursor.fetchall()
        for notif_id, message in notifications:
            QMessageBox.information(self, "Notification", message)
            
            # Mark as read
            self.cursor.execute('''
                UPDATE notifications 
                SET is_read = 1 
                WHERE id = ?
            ''', (notif_id,))
        
        self.conn.commit()
    
    def add_notification(self, task_id, message):
        """Add a new notification"""
        self.cursor.execute('''
            INSERT INTO notifications (task_id, message, notification_time)
            VALUES (?, ?, datetime('now'))
        ''', (task_id, message))
        self.conn.commit()
    
    def pause_current_task(self, tab_index):
        """Pause the current task in the specified tab"""
        tab_title = self.exec_tabs.tabText(tab_index)
        
        if tab_title in self.active_tabs:
            processor = self.active_tabs[tab_title]['processor']
            
            if self.active_tabs[tab_title]['status'] == 'running':
                processor.pause()
                self.active_tabs[tab_title]['status'] = 'paused'
                
                # Update UI
                current_tab = self.exec_tabs.widget(tab_index)
                status_label = current_tab.findChild(QLabel, "status_label")
                status_label.setText(self.tr['status_paused'])
                status_label.setStyleSheet('color: #f39c12;')
    
    def stop_current_task(self, tab_index):
        """Stop the current task in the specified tab"""
        tab_title = self.exec_tabs.tabText(tab_index)
        
        if tab_title in self.active_tabs:
            processor = self.active_tabs[tab_title]['processor']
            processor.stop()
            self.active_tabs[tab_title]['status'] = 'stopped'
            
            # Update UI
            current_tab = self.exec_tabs.widget(tab_index)
            status_label = current_tab.findChild(QLabel, "status_label")
            log_area = current_tab.findChild(QTextEdit, "log_area")
            
            status_label.setText(self.tr['status_stopped'])
            status_label.setStyleSheet('color: #e74c3c;')
            log_area.append("\nProcess stopped by user")
            
            # Update database if it's an environment task
            if self.active_tabs[tab_title]['type'] == 'env':
                self.cursor.execute('''
                    UPDATE active_tasks 
                    SET status = 'stopped',
                        end_time = datetime('now')
                    WHERE network_name = ? AND robot_name = ? AND script_name = ?
                    ORDER BY start_time DESC
                    LIMIT 1
                ''', (
                    self.active_tabs[tab_title]['network'],
                    self.active_tabs[tab_title]['robot'],
                    self.active_tabs[tab_title]['script']
                ))
                self.conn.commit()
    
    def on_batch_processed(self, batch_num, links, log_area, status_label):
        """Handle processed batch"""
        log_area.append(f"\n=== Batch {batch_num} ===")
        for link in links:
            log_area.append(f"• Processing link: {link}")
        
        # Auto-scroll
        scrollbar = log_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def on_env_status_updated(self, message, log_area):
        """Handle environment status updates"""
        log_area.append(f"• {message}")
        
        # Auto-scroll
        scrollbar = log_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def on_processing_finished(self, log_area, status_label):
        """Handle process completion"""
        status_label.setText(self.tr['status_complete'])
        status_label.setStyleSheet('color: #17a2b8;')
        log_area.append("\nProcess completed successfully")
    
    def on_processing_error(self, error_msg, log_area, status_label):
        """Handle processing errors"""
        status_label.setText(self.tr['status_stopped'])
        status_label.setStyleSheet('color: #e74c3c;')
        log_area.append(f"\nERROR: {error_msg}")
        
        QMessageBox.critical(self, "Processing Error", error_msg)
    
    def closeEvent(self, event):
        """Cleanup on close"""
        # Stop all running processes
        for tab_title, task_info in self.active_tabs.items():
            if task_info['status'] == 'running':
                task_info['processor'].stop()
                task_info['processor'].wait(1000)
        
        # Close database connection
        self.conn.close()
        
        super().closeEvent(event)















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
        
        self.active_tabs = {}  # Pour suivre les onglets actifs
        self.setup_database()
        self.init_ui()
        self.scan_networks_and_robots()
        self.setup_styles()
        
        # Timer pour vérifier les tâches planifiées
        self.scheduler_timer = QTimer(self)
        self.scheduler_timer.timeout.connect(self.check_scheduled_tasks)
        self.scheduler_timer.start(60000)  # Vérifie toutes les minutes
        
        # Timer pour les notifications
        self.notification_timer = QTimer(self)
        self.notification_timer.timeout.connect(self.check_notifications)
        self.notification_timer.start(30000)  # Vérifie toutes les 30 secondes

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
                margin-top: 10px;
                padding-top: 20px;
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
                padding: 8px 16px;
                font-weight: 600;
                font-size: 13px;
                min-width: 100px;
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
                padding: 8px;
                font-size: 13px;
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
                font-size: 12px;
                color: #495057;
            }
            
            /* Barre de défilement */
            QScrollBar:vertical {
                border: none;
                background: #f1f3f5;
                width: 8px;
                margin: 0px 0px 0px 0px;
            }
            
            QScrollBar::handle:vertical {
                background: #ced4da;
                min-height: 20px;
                border-radius: 4px;
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
            
            /* Boutons colorés */
            .btn-primary {
                background-color: #4da6ff;
                color: white;
            }
            
            .btn-success {
                background-color: #28a745;
                color: white;
            }
            
            .btn-warning {
                background-color: #ffc107;
                color: #212529;
            }
            
            .btn-danger {
                background-color: #dc3545;
                color: white;
            }
            
            .btn-secondary {
                background-color: #6c757d;
                color: white;
            }
            
            .btn-purple {
                background-color: #6f42c1;
                color: white;
            }
            
            /* Onglets */
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 6px;
                margin-top: 5px;
            }
            
            QTabBar::tab {
                padding: 8px 12px;
                background: #f1f1f1;
                border: 1px solid #ddd;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
                font-size: 13px;
            }
            
            QTabBar::tab:selected {
                background: #fff;
                border-bottom: 2px solid #4da6ff;
            }
            
            QTabBar::tab:hover {
                background: #e9e9e9;
            }
            
            /* Listes */
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: white;
                font-size: 13px;
            }
            
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
            
            QListWidget::item:selected {
                background-color: #e1f0fa;
                color: #333;
            }
            
            /* Séparateurs */
            QSplitter::handle {
                background: #dee2e6;
                width: 5px;
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
            'start_robot_btn': "Start Robot",
            'schedule_btn': "Schedule",
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
            'visualization_placeholder': "Execution log will appear here...",
            'scheduled_tasks': "Scheduled Tasks",
            'task_scheduled': "Task scheduled for {}",
            'notification_msg': "Scheduled task will start in 10 minutes: {}",
            'task_started': "Task started: {}",
            'task_completed': "Task completed: {}",
            'select_robot_title': "Start New Robot",
            'select_network_label': "Select Network:",
            'select_robot_label': "Select Robot:",
            'select_script_label': "Select Script:",
            'current_tasks': "Current Tasks",
            'task_id': "ID",
            'task_network': "Network",
            'task_robot': "Robot",
            'task_script': "Script",
            'task_scheduled_time': "Scheduled Time",
            'task_status': "Status",
            'task_actions': "Actions",
            'action_pause': "Pause",
            'action_resume': "Resume",
            'action_cancel': "Cancel",
            'action_delete': "Delete",
            'repeat_daily': "Repeat Daily",
            'repeat_weekly': "Repeat Weekly",
            'repeat_monthly': "Repeat Monthly",
            'execution_tab': "Execution",
            'scheduling_tab': "Scheduling"
        }

    def setup_database(self):
        """Initialize database connection"""
        self.conn = sqlite3.connect(DB_PATH_notes)
        self.cursor = self.conn.cursor()
        
        # Table pour les paramètres
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

        # Table pour les descriptions
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS autredescription (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                network_name TEXT NOT NULL,
                robot_name TEXT NOT NULL,
                description TEXT,
                UNIQUE(network_name, robot_name)
            )
        ''')
        
        # Table pour les tâches planifiées
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                network_name TEXT NOT NULL,
                robot_name TEXT NOT NULL,
                script_name TEXT NOT NULL,
                scheduled_time DATETIME NOT NULL,
                repeat_pattern TEXT,
                status TEXT DEFAULT 'pending',
                next_execution DATETIME,
                last_execution DATETIME,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Table pour les tâches en cours
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS active_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                network_name TEXT NOT NULL,
                robot_name TEXT NOT NULL,
                script_name TEXT NOT NULL,
                start_time DATETIME NOT NULL,
                status TEXT DEFAULT 'running',
                process_id INTEGER
            )
        ''')
        
        # Table pour les notifications
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                message TEXT NOT NULL,
                notification_time DATETIME NOT NULL,
                is_read BOOLEAN DEFAULT 0
            )
        ''')
    
        # Insérer les paramètres par défaut si la table est vide
        self.cursor.execute('SELECT COUNT(*) FROM settings')
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute('''
                INSERT INTO settings (group_size, chrome_path) 
                VALUES (10, 'C:/Program Files/Google/Chrome/Application/chrome.exe')
            ''')
            self.conn.commit()

    def init_ui(self):
        """Initialize the main UI"""
        self.setWindowTitle(self.tr['window_title'])
        self.setMinimumSize(1200, 800)
        
        # Main splitter for left/right panels
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Left panel (wider) - Contains configuration and execution tabs
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(5, 5, 5, 5)
        left_layout.setSpacing(10)
        
        # Tab widget for left panel
        self.left_tabs = QTabWidget()
        self.left_tabs.setObjectName("leftTabs")
        
        # Tab 1: Configuration and Execution
        config_exec_tab = QWidget()
        config_exec_layout = QVBoxLayout()
        config_exec_layout.setContentsMargins(5, 5, 5, 5)
        config_exec_layout.setSpacing(10)
        
        # Configuration group
        config_group = QGroupBox(self.tr['config_group'])
        config_layout = QVBoxLayout()
        config_layout.setContentsMargins(10, 15, 10, 10)
        
        # Network and robot selection
        selection_layout = QHBoxLayout()
        
        # Network selection
        network_layout = QVBoxLayout()
        network_label = QLabel(self.tr['network_select_label'])
        self.network_combo = QComboBox()
        self.network_combo.currentIndexChanged.connect(self.on_network_changed)
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
        
        # Schedule button
        schedule_btn = QPushButton(self.tr['schedule_btn'])
        schedule_btn.setObjectName("scheduleBtn")
        schedule_btn.setToolTip("Schedule a new task")
        schedule_btn.clicked.connect(self.show_schedule_dialog)
        schedule_btn.setFixedHeight(30)
        
        selection_layout.addLayout(network_layout, 2)
        selection_layout.addLayout(robot_layout, 2)
        selection_layout.addLayout(batch_layout, 1)
        selection_layout.addWidget(schedule_btn, 1)
        
        # Description editor
        desc_layout = QVBoxLayout()
        desc_label = QLabel(self.tr['description_label'])
        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText(self.tr['description_placeholder'])
        self.desc_edit.setMinimumHeight(150)
        self.desc_edit.textChanged.connect(self.save_description)
        
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_edit)
        
        # Add to config group
        config_layout.addLayout(selection_layout)
        config_layout.addLayout(desc_layout, 1)
        config_group.setLayout(config_layout)
        
        # Execution tabs
        self.exec_tabs = QTabWidget()
        self.exec_tabs.setObjectName("executionTabs")
        self.exec_tabs.setTabsClosable(True)
        self.exec_tabs.tabCloseRequested.connect(self.close_execution_tab)
        
        # Add default tab
        self.add_execution_tab("Links Processing")
        
        # Control buttons
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 5, 0, 5)
        
        self.start_btn = QPushButton(self.tr['start_btn'])
        self.start_btn.setObjectName("startBtn")
        self.start_robot_btn = QPushButton(self.tr['start_robot_btn'])
        self.start_robot_btn.setObjectName("startRobotBtn")
        
        self.start_btn.clicked.connect(self.start_link_processing)
        self.start_robot_btn.clicked.connect(self.show_start_robot_dialog)
        
        control_layout.addStretch()
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.start_robot_btn)
        control_layout.addStretch()
        
        # Add to config/exec tab
        config_exec_layout.addWidget(config_group, 1)
        config_exec_layout.addWidget(self.exec_tabs, 3)
        config_exec_layout.addLayout(control_layout)
        config_exec_tab.setLayout(config_exec_layout)
        
        # Tab 2: Scheduled Tasks
        scheduled_tasks_tab = QWidget()
        scheduled_layout = QVBoxLayout()
        scheduled_layout.setContentsMargins(5, 5, 5, 5)
        
        # Scheduled tasks list
        self.scheduled_list = QListWidget()
        self.scheduled_list.setObjectName("scheduledList")
        self.scheduled_list.itemDoubleClicked.connect(self.show_task_details)
        
        # Task control buttons
        task_btn_layout = QHBoxLayout()
        task_btn_layout.setContentsMargins(0, 5, 0, 5)
        
        self.pause_task_btn = QPushButton(self.tr['action_pause'])
        self.resume_task_btn = QPushButton(self.tr['action_resume'])
        self.cancel_task_btn = QPushButton(self.tr['action_cancel'])
        self.delete_task_btn = QPushButton(self.tr['action_delete'])
        
        self.pause_task_btn.setObjectName("pauseTaskBtn")
        self.resume_task_btn.setObjectName("resumeTaskBtn")
        self.cancel_task_btn.setObjectName("cancelTaskBtn")
        self.delete_task_btn.setObjectName("deleteTaskBtn")
        
        self.pause_task_btn.clicked.connect(self.pause_scheduled_task)
        self.resume_task_btn.clicked.connect(self.resume_scheduled_task)
        self.cancel_task_btn.clicked.connect(self.cancel_scheduled_task)
        self.delete_task_btn.clicked.connect(self.delete_scheduled_task)
        
        task_btn_layout.addWidget(self.pause_task_btn)
        task_btn_layout.addWidget(self.resume_task_btn)
        task_btn_layout.addWidget(self.cancel_task_btn)
        task_btn_layout.addWidget(self.delete_task_btn)
        
        scheduled_layout.addWidget(QLabel(self.tr['scheduled_tasks']))
        scheduled_layout.addWidget(self.scheduled_list, 1)
        scheduled_layout.addLayout(task_btn_layout)
        scheduled_tasks_tab.setLayout(scheduled_layout)
        
        # Add tabs to left panel
        self.left_tabs.addTab(config_exec_tab, self.tr['execution_tab'])
        self.left_tabs.addTab(scheduled_tasks_tab, self.tr['scheduling_tab'])
        
        # Add to left panel
        left_layout.addWidget(self.left_tabs)
        left_panel.setLayout(left_layout)
        
        # Right panel (narrower) - Contains description and social publisher
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(5, 5, 5, 5)
        right_layout.setSpacing(10)
        
        # Radio buttons to switch between views
        radio_layout = QHBoxLayout()
        radio_layout.setContentsMargins(0, 0, 0, 5)
        
        self.radio_description = QRadioButton("Description Editor")
        self.radio_social = QRadioButton("Social Publisher")
        self.radio_description.setChecked(True)
        
        radio_layout.addWidget(self.radio_description)
        radio_layout.addWidget(self.radio_social)
        radio_layout.addStretch()
        
        # Stacked widget for right panel content
        self.stacked_widget = QStackedWidget()
        
        # Panel 1: Description Editor
        self.description_panel = MainWindow1()
        
        # Panel 2: Social Media Publisher
        self.social_panel = SocialMediaPublisher()
        
        # Add panels to stacked widget
        self.stacked_widget.addWidget(self.description_panel)
        self.stacked_widget.addWidget(self.social_panel)
        
        # Connect radio buttons to stacked widget
        self.radio_description.toggled.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.radio_social.toggled.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        # Add to right panel
        right_layout.addLayout(radio_layout)
        right_layout.addWidget(self.stacked_widget)
        
        right_panel.setLayout(right_layout)
        
        # Add panels to splitter
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(right_panel)
        main_splitter.setStretchFactor(0, 2)  # Left panel takes 2/3 space
        main_splitter.setStretchFactor(1, 1)  # Right panel takes 1/3 space
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(main_splitter)
        self.setLayout(main_layout)
        
        # Load initial data
        self.load_description()
        self.load_scheduled_tasks()
        
        # Apply styles
        self.apply_button_styles()

    def apply_button_styles(self):
        """Apply specific styles to buttons"""
        self.start_btn.setProperty("class", "btn-success")
        self.start_robot_btn.setProperty("class", "btn-purple")
        self.findChild(QPushButton, "scheduleBtn").setProperty("class", "btn-primary")
        
        self.pause_task_btn.setProperty("class", "btn-warning")
        self.resume_task_btn.setProperty("class", "btn-success")
        self.cancel_task_btn.setProperty("class", "btn-warning")
        self.delete_task_btn.setProperty("class", "btn-danger")
        
        # Force style update
        self.start_btn.style().unpolish(self.start_btn)
        self.start_btn.style().polish(self.start_btn)
        self.start_robot_btn.style().unpolish(self.start_robot_btn)
        self.start_robot_btn.style().polish(self.start_robot_btn)

    # ... [Keep all other methods unchanged from the previous version] ...



class LinkProcessor(QThread):
    """Thread for processing links in batches"""
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
    """Thread for processing environment tasks"""
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


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    manager = DescriptionManager()
    manager.show()
    
    sys.exit(app.exec_())