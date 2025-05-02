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
class DescriptionManager(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tr = self.init_translations()
        self.base_path = "C:/bon"
        self.setup_database()
        self.init_ui()
        self.scan_robots()
        self.link_opener = None
        self.setup_styles()



    def init_translations(self):
        """Initialize professional translations"""
        return {
            'window_title': "Sales Robot Manager",
            'no_robot_title': "No Robot Installed",
            'no_robot_msg': "No sales robot detected. Please install at least one robot in the C:/bon directory.",
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
                chrome_path TEXT
            )
        ''')


        # Nouvelle table pour les descriptions des autres robots
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS autredescription (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                robot_name TEXT NOT NULL,
                description TEXT,
                UNIQUE(robot_name)
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
        self.cursor.execute('''
            UPDATE settings 
            SET last_description = ?
            WHERE id = 1
        ''', (description,))
        self.conn.commit()
        
    def save_settings(self):
        """Sauvegarde les paramètres (sauf description déjà sauvegardée automatiquement)"""
        self.cursor.execute('''
            UPDATE settings 
            SET group_size = ?,
                last_robot = ?
            WHERE id = 1
        ''', (
            self.batch_spin.value(),
            self.robot_combo.currentText()
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
        description = self.load_setting('last_description')
        if description:
            self.desc_edit.setPlainText(description)


    def init_ui(self):
        """Initialize professional UI"""
        self.setWindowTitle(self.tr['window_title'])
        self.setFixedSize(1000, 800)
        
        # Professional styling
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
            QSpinBox, QComboBox {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                min-height: 30px;
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
        
        # First row - Robot selection and Batch size
        top_row_layout = QHBoxLayout()
        
        # Robot selection
        robot_layout = QVBoxLayout()
        robot_label = QLabel(self.tr['robot_select_label'])
        self.robot_combo = QComboBox()
        self.robot_combo.setStyleSheet('min-width: 200px;')
        robot_layout.addWidget(robot_label)
        robot_layout.addWidget(self.robot_combo)
        
        # Batch size setting
        batch_layout = QVBoxLayout()
        batch_label = QLabel(self.tr['group_size_label'])
        self.batch_spin = QSpinBox()
        self.batch_spin.setRange(1, 50)
        self.batch_spin.setValue(self.load_setting('group_size', 10))
        batch_layout.addWidget(batch_label)
        batch_layout.addWidget(self.batch_spin)
        
        # Add to top row with stretchable space
        top_row_layout.addLayout(robot_layout, 2)
        top_row_layout.addSpacing(30)  # Space between elements
        top_row_layout.addLayout(batch_layout, 1)
        top_row_layout.addStretch()
        
        # Product description (second row)
        desc_layout = QVBoxLayout()
        desc_label = QLabel(self.tr['description_label'])
        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText(self.tr['description_placeholder'])
        self.desc_edit.setStyleSheet('''
            QTextEdit {
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 15px;
                font-size: 14px;
                background-color: #ffffff;
                min-height: 150px;
            }
            QTextEdit:focus {
                border: 2px solid #3498db;
            }
        ''')


        # Dans init_ui, après avoir créé desc_edit:
        self.desc_edit.setPlaceholderText(self.tr['description_placeholder'])
        self.desc_edit.setMinimumHeight(120)
        self.desc_edit.textChanged.connect(self.save_description)  # Connection du signal
        self.load_description()  # Chargement initial


        
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_edit)
        
        # Add to config group
        config_layout.addLayout(top_row_layout)
        config_layout.addSpacing(15)  # Space between rows
        config_layout.addLayout(desc_layout, 1)  # Takes remaining space
        config_group.setLayout(config_layout)
        
        # Execution group (unchanged)
        exec_group = QGroupBox(self.tr['exec_group'])
        exec_layout = QVBoxLayout()
        




        # Control buttons
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
        
        # Status display
        self.status_label = QLabel(self.tr['status_ready'])
        self.status_label.setStyleSheet('font-weight: bold; color: #7f8c8d; font-size: 14px;')
        
        # Batch info
        self.batch_label = QLabel()
        self.batch_label.setStyleSheet('color: #95a5a6; font-size: 13px;')
        
        # Visualization area
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
        
        exec_layout.addLayout(control_layout)
        exec_layout.addWidget(self.status_label)
        exec_layout.addWidget(self.batch_label)
        exec_layout.addWidget(self.visualization, 1)
        exec_group.setLayout(exec_layout)
        






        # Assemble main layout
        main_layout.addWidget(config_group, 1)
        main_layout.addWidget(exec_group, 2)
        self.setLayout(main_layout)


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

    def scan_robots(self):
        """Scan for available sales robots"""
        self.robot_combo.clear()
        
        if not os.path.exists(self.base_path):
            self.show_no_robot_modal()
            return
            
        robots = [d for d in os.listdir(self.base_path) 
                 if d.startswith('robot') and os.path.isdir(os.path.join(self.base_path, d))]
        
        if not robots:
            self.show_no_robot_modal()
            return
            
        self.robot_combo.addItems(robots)
        
        # Load last used robot
        last_robot = self.load_setting('last_robot')
        if last_robot and last_robot in robots:
            self.robot_combo.setCurrentText(last_robot)

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
        QMessageBox.information(self, "Installation", "Please create robot directories in C:/bon (robot1, robot2, etc.)")

    def browse_for_robot(self):
        """Let user browse for robot location"""
        path = QFileDialog.getExistingDirectory(self, "Select Robot Directory", "C:/")
        if path:
            self.base_path = path
            self.scan_robots()

    def load_setting(self, key, default=None):
        """Load setting from database"""
        self.cursor.execute(f'SELECT {key} FROM settings LIMIT 1')
        result = self.cursor.fetchone()
        return result[0] if result and result[0] is not None else default


    def save_settings(self):
        """Save current settings to database"""
        self.cursor.execute('''
            UPDATE settings 
            SET group_size = ?, 
                last_description = ?,
                last_robot = ?
            WHERE id = 1
        ''', (
            self.batch_spin.value(),
            self.desc_edit.toPlainText(),
            self.robot_combo.currentText()
        ))
        self.conn.commit()

    def start_processing(self):
        """Start link processing"""
        selected_robot = self.robot_combo.currentText()
        if not selected_robot:
            QMessageBox.warning(self, "Selection Required", "Please select a sales robot")
            return
            
        json_path = os.path.join(self.base_path, selected_robot, "data.json")
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
            self.tr['group_opened'].format(batch_num, len(links))
        )
        
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

    def closeEvent(self, event):
        """Cleanup on close"""
        if self.link_opener and self.link_opener.isRunning():
            self.link_opener.stop()
            self.link_opener.wait(1000)
        
        self.save_settings()
        self.conn.close()
        super().closeEvent(event)






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
        """Initialize professional translations"""
        return {
            'window_title': "Sales Robot Manager - Professional Edition",
            'no_robot_title': "No Robot Installed",
            'no_robot_msg': "No sales robot detected. Please install at least one robot in the C:/bon directory.",
            'config_group': "Configuration Settings",
            'group_size_label': "Links per batch:",
            'description_label': "Product Description:",
            'description_placeholder': "Enter your professional product description here...",
            'exec_group': "Execution Control",
            'start_btn': "Start Processing",
            'continue_btn': "Continue",
            'stop_btn': "Stop Process",
            'status_ready': "Ready to start processing",
            'status_running': "Processing links...",
            'status_paused': "Waiting for confirmation...",
            'status_complete': "Process completed successfully",
            'status_stopped': "Process stopped by user",
            'robot_select_label': "Select Sales Robot:",
            'group_opened': "Batch {} opened - {} links processed",
            'error_json': "Error: JSON file not found",
            'error_chrome': "Error: Chrome path incorrect",
            'install_btn': "Install Robot",
            'browse_btn': "Browse Directory",
            'visualization_placeholder': "Execution details will appear here...\n\nStatus messages, processed links and other information will be displayed in this area."
        }

    def init_ui(self):
        """Initialize modern UI"""
        self.setWindowTitle(self.tr['window_title'])
        self.setWindowIcon(QIcon("robot_icon.png"))  # Ajoutez une icône appropriée
        self.setMinimumSize(1000, 800)
        
        # Main layout with modern spacing
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)
        
        # Configuration group - modern card style
        config_group = QGroupBox(self.tr['config_group'])
        config_group.setObjectName("configGroup")
        config_layout = QVBoxLayout()
        config_layout.setSpacing(15)
        config_layout.setContentsMargins(20, 20, 20, 20)
        
        # Top row - responsive layout
        top_row = QHBoxLayout()
        top_row.setSpacing(30)
        
        # Robot selection - modern combo box
        robot_layout = QVBoxLayout()
        robot_layout.setSpacing(8)
        robot_label = QLabel(self.tr['robot_select_label'])
        self.robot_combo = QComboBox()
        self.robot_combo.setMinimumHeight(35)
        robot_layout.addWidget(robot_label)
        robot_layout.addWidget(self.robot_combo)
        
        # Batch size - modern spin box
        batch_layout = QVBoxLayout()
        batch_layout.setSpacing(8)
        batch_label = QLabel(self.tr['group_size_label'])
        self.batch_spin = QSpinBox()
        self.batch_spin.setRange(1, 50)
        self.batch_spin.setValue(self.load_setting('group_size', 10))
        self.batch_spin.setMinimumHeight(35)
        batch_layout.addWidget(batch_label)
        batch_layout.addWidget(self.batch_spin)
        
        # Add to top row with proper spacing
        top_row.addLayout(robot_layout, 2)
        top_row.addLayout(batch_layout, 1)
        top_row.addStretch()
        
        # Description area - modern text edit
        desc_layout = QVBoxLayout()
        desc_layout.setSpacing(8)
        desc_label = QLabel(self.tr['description_label'])
        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText(self.tr['description_placeholder'])
        self.desc_edit.setMinimumHeight(150)
        self.desc_edit.textChanged.connect(self.save_description)
        
        # Add shadow effect to description area
        desc_frame = QFrame()
        desc_frame.setLayout(desc_layout)
        desc_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 6px;
                border: 1px solid #e9ecef;
            }
        """)
        
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_edit)
        
        # Add to config group
        config_layout.addLayout(top_row)
        config_layout.addWidget(desc_frame, 1)
        config_group.setLayout(config_layout)
        
        # Execution group - modern card style
        exec_group = QGroupBox(self.tr['exec_group'])
        exec_group.setObjectName("execGroup")
        exec_layout = QVBoxLayout()
        exec_layout.setSpacing(15)
        exec_layout.setContentsMargins(20, 20, 20, 20)
        
        # Control buttons - modern button group
        control_layout = QHBoxLayout()
        control_layout.setSpacing(15)
        
        self.start_btn = QPushButton(self.tr['start_btn'])
        self.start_btn.setObjectName("start_btn")
        self.start_btn.clicked.connect(self.start_processing)
        
        self.continue_btn = QPushButton(self.tr['continue_btn'])
        self.continue_btn.setObjectName("continue_btn")
        self.continue_btn.clicked.connect(self.continue_processing)
        self.continue_btn.setEnabled(False)
        
        self.stop_btn = QPushButton(self.tr['stop_btn'])
        self.stop_btn.setObjectName("stop_btn")
        self.stop_btn.clicked.connect(self.stop_processing)
        self.stop_btn.setEnabled(False)
        
        # Add buttons with proper spacing
        control_layout.addStretch()
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.continue_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addStretch()
        
        # Status display - modern label
        self.status_label = QLabel(self.tr['status_ready'])
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 600;
                padding: 10px;
                border-radius: 6px;
                background-color: #f1f3f5;
            }
        """)
        
        # Batch info - subtle label
        self.batch_label = QLabel()
        self.batch_label.setAlignment(Qt.AlignCenter)
        self.batch_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 13px;
                font-style: italic;
            }
        """)
        
        # Visualization area - modern console-like appearance
        self.visualization = QTextEdit()
        self.visualization.setObjectName("visualization")
        self.visualization.setReadOnly(True)
        self.visualization.setPlaceholderText(self.tr['visualization_placeholder'])
        
        # Add shadow effect to visualization area
        viz_frame = QFrame()
        viz_frame.setLayout(QVBoxLayout())
        viz_frame.layout().addWidget(self.visualization)
        viz_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 6px;
                border: 1px solid #e9ecef;
            }
        """)
        
        # Add to exec group
        exec_layout.addLayout(control_layout)
        exec_layout.addWidget(self.status_label)
        exec_layout.addWidget(self.batch_label)
        exec_layout.addWidget(viz_frame, 1)
        exec_group.setLayout(exec_layout)
        
        # Assemble main layout
        main_layout.addWidget(config_group, 1)
        main_layout.addWidget(exec_group, 2)
        self.setLayout(main_layout)
        
        # Load initial data
        self.load_description()
        
        # Add subtle animation to buttons on hover
        self.setup_button_animations()

    def setup_button_animations(self):
        """Configure des animations subtiles pour les boutons"""
        for btn in [self.start_btn, self.continue_btn, self.stop_btn]:
            btn.setGraphicsEffect(None)
            
    def update_status_style(self, status_type):
        """Met à jour le style du label de statut"""
        self.status_label.setProperty("class", f"status-{status_type}")
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
































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

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    manager = DescriptionManager()
    manager.show()
    sys.exit(app.exec_())