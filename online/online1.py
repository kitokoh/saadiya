import sys
import secrets
import sqlite3
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QTabWidget, QTextEdit, QFormLayout, 
                            QSpinBox, QLineEdit, QGroupBox, QWidget, 
                            QSystemTrayIcon, QMenu, QCheckBox, QApplication)
from PyQt5.QtCore import QThread, pyqtSignal, QObject, Qt, QTimer, QBuffer
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPainter, QImage
from flask import Flask, request, Response, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import socket
import webbrowser
import logging
from threading import Event, Lock
from datetime import datetime
import qrcode
from io import BytesIO
import base64
import platform
import subprocess
import os
import requests
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RemoteAppServer(QObject):
    server_started = pyqtSignal(str, str, str)  # local_url, network_url, qr_code
    server_stopped = pyqtSignal()
    command_received = pyqtSignal(dict)
    connection_log = pyqtSignal(str)
    ngrok_started = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, port=5000, password=None, parent_app=None):
        super().__init__()
        self.port = port
        self.password = password or secrets.token_urlsafe(12)
        self.parent_app = parent_app
        self.app = Flask(__name__)
        self.running = False
        self.shutdown_event = Event()
        self.active_connections = set()
        self.ngrok_process = None
        self.ngrok_url = None
        self.screenshot_lock = Lock()
        self.setup_routes()
        self.last_update_time = 0
        self.update_interval = 0.5  # seconds

    def setup_routes(self):
        @self.app.route('/')
        def serve_application():
            """Serve the main application interface"""
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Remote Access</title>
                <style>
                    body { margin: 0; padding: 0; overflow: hidden; }
                    #app-container { 
                        position: relative;
                        width: 100vw;
                        height: 100vh;
                    }
                    #live-view {
                        width: 100%;
                        height: 100%;
                        object-fit: contain;
                    }
                    .control-bar {
                        position: absolute;
                        bottom: 10px;
                        left: 50%;
                        transform: translateX(-50%);
                        background: rgba(0,0,0,0.7);
                        padding: 10px;
                        border-radius: 5px;
                        display: flex;
                        gap: 10px;
                    }
                    .control-btn {
                        padding: 8px 15px;
                        background: #4285f4;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                    }
                </style>
            </head>
            <body>
                <div id="app-container">
                    <img id="live-view" src="/screenshot?t=0">
                    <div class="control-bar">
                        <button class="control-btn" onclick="sendCommand('refresh')">Refresh</button>
                        <button class="control-btn" onclick="sendCommand('open')">Open</button>
                        <button class="control-btn" onclick="sendCommand('save')">Save</button>
                    </div>
                </div>
                <script>
                    let lastUpdate = 0;
                    const img = document.getElementById('live-view');
                    
                    function updateImage() {
                        const now = Date.now();
                        img.src = `/screenshot?t=${now}`;
                        lastUpdate = now;
                    }
                    
                    // Auto-refresh every 500ms
                    setInterval(updateImage, 500);
                    
                    function sendCommand(action) {
                        fetch('/command', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ action })
                        }).then(r => r.json()).then(console.log);
                    }
                    
                    // Handle clicks on the image
                    img.addEventListener('click', (e) => {
                        const rect = img.getBoundingClientRect();
                        const x = (e.clientX - rect.left) / rect.width;
                        const y = (e.clientY - rect.top) / rect.height;
                        sendCommand({
                            action: 'click',
                            x: x.toFixed(4),
                            y: y.toFixed(4)
                        });
                    });
                </script>
            </body>
            </html>
            """

        @self.app.route('/screenshot')
        def get_screenshot():
            """Capture and send application screenshot"""
            current_time = time.time()
            if current_time - self.last_update_time < self.update_interval:
                return Response(status=304)  # Not Modified
            
            try:
                with self.screenshot_lock:
                    # Grab the main window
                    pixmap = self.parent_app.grab()
                    if pixmap.isNull():
                        return Response("Failed to capture window", status=500)
                    
                    # Convert to image
                    img = pixmap.toImage()
                    buffer = QBuffer()
                    buffer.open(QBuffer.ReadWrite)
                    img.save(buffer, "JPEG", quality=80)
                    buffer.seek(0)
                    
                    self.last_update_time = current_time
                    return Response(
                        buffer.data(),
                        mimetype='image/jpeg',
                        headers={'Cache-Control': 'no-cache'}
                    )
            except Exception as e:
                logger.error(f"Screenshot error: {str(e)}")
                return Response(str(e), status=500)

        @self.app.route('/command', methods=['POST'])
        def handle_command():
            """Handle remote commands"""
            data = request.get_json()
            if data and data.get('action'):
                self.command_received.emit(data)
                return {'status': 'success', 'action': data['action']}
            return {'status': 'error', 'message': 'Invalid request'}, 400

    def run_server(self):
        if self.running:
            return

        self.running = True
        host = '0.0.0.0'
        
        local_url = f"http://localhost:{self.port}"
        network_url = f"http://{self.get_local_ip()}:{self.port}"
        
        qr_img = self.generate_qr_code(network_url)
        self.server_started.emit(local_url, network_url, qr_img)
        
        from werkzeug.serving import make_server
        self.server = make_server(host, self.port, self.app)
        
        while not self.shutdown_event.is_set():
            self.server.handle_request()
        
        self.stop_ngrok()
        self.server.server_close()
        self.running = False
        self.server_stopped.emit()

    def start_ngrok(self, auth_token):
        try:
            if platform.system() == "Windows":
                ngrok_path = os.path.join(os.getenv('APPDATA'), 'ngrok', 'ngrok.exe')
            else:
                ngrok_path = 'ngrok'
                
            self.ngrok_process = subprocess.Popen(
                [ngrok_path, 'http', str(self.port), '--authtoken', auth_token],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
            
            QTimer.singleShot(3000, self.fetch_ngrok_url)
            return True
        except Exception as e:
            logger.error(f"Ngrok error: {str(e)}")
            self.error_occurred.emit(f"Ngrok error: {str(e)}")
            return False

    def fetch_ngrok_url(self):
        try:
            resp = requests.get('http://localhost:4040/api/tunnels', timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                public_url = data['tunnels'][0]['public_url']
                self.ngrok_url = public_url
                self.ngrok_started.emit(public_url)
                logger.info(f"Ngrok tunnel started: {public_url}")
        except Exception as e:
            logger.warning(f"Failed to fetch Ngrok URL: {str(e)}")

    def stop_ngrok(self):
        if self.ngrok_process:
            try:
                self.ngrok_process.terminate()
                self.ngrok_process.wait(timeout=5)
                logger.info("Ngrok tunnel stopped")
            except subprocess.TimeoutExpired:
                self.ngrok_process.kill()
                logger.warning("Ngrok process killed forcefully")

    def shutdown_server(self):
        self.shutdown_event.set()
        try:
            requests.post(f"http://localhost:{self.port}/shutdown", timeout=1)
        except:
            pass

    def generate_qr_code(self, url):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return '127.0.0.1'

class RemoteAccessModal(QDialog):
    def __init__(self, parent_app=None):
        super().__init__(parent_app)
        self.parent_app = parent_app
        self.db = sqlite3.connect('remote_config.db')
        self.init_db()
        self.server = None
        self.server_thread = None
        self.init_ui()
        self.load_config()
        
        self.setWindowTitle("Remote Access Control Panel")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QPushButton {
                background-color: #4285f4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #3367d6;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
            }
            QLabel {
                margin: 2px;
            }
        """)

    def init_db(self):
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS config (
                id INTEGER PRIMARY KEY,
                port INTEGER DEFAULT 5000,
                password TEXT,
                enable_ngrok INTEGER DEFAULT 0,
                ngrok_token TEXT
            )
        ''')
        self.db.commit()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        
        # Create tabs
        self.tabs = QTabWidget()
        self.setup_connection_tab()
        self.setup_settings_tab()
        self.setup_log_tab()
        
        self.layout.addWidget(self.tabs)
        
        # Control buttons
        btn_layout = QHBoxLayout()
        self.toggle_btn = QPushButton("Start Remote Access")
        self.toggle_btn.clicked.connect(self.toggle_server)
        
        self.copy_url_btn = QPushButton("Copy URL")
        self.copy_url_btn.setEnabled(False)
        self.copy_url_btn.clicked.connect(self.copy_url)
        
        self.open_browser_btn = QPushButton("Open in Browser")
        self.open_browser_btn.setEnabled(False)
        self.open_browser_btn.clicked.connect(self.open_browser)
        
        btn_layout.addWidget(self.toggle_btn)
        btn_layout.addWidget(self.copy_url_btn)
        btn_layout.addWidget(self.open_browser_btn)
        
        self.layout.addLayout(btn_layout)
        
        # Preview
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumSize(400, 300)
        self.layout.addWidget(self.preview_label)
        
        # Preview update timer
        self.preview_timer = QTimer()
        self.preview_timer.timeout.connect(self.update_preview)
        self.preview_timer.start(1000)

    def setup_connection_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Connection status
        status_group = QGroupBox("Connection Status")
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("Status: Not Connected")
        self.local_url_label = QLabel("Local URL: -")
        self.network_url_label = QLabel("Network URL: -")
        self.ngrok_url_label = QLabel("Internet URL: -")
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.local_url_label)
        status_layout.addWidget(self.network_url_label)
        status_layout.addWidget(self.ngrok_url_label)
        status_group.setLayout(status_layout)
        
        # QR Code
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.setMinimumSize(200, 200)
        
        layout.addWidget(status_group)
        layout.addWidget(self.qr_label)
        layout.addStretch()
        
        self.tabs.addTab(tab, "Connection")

    def setup_settings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Server settings
        server_group = QGroupBox("Server Settings")
        server_layout = QFormLayout()
        
        self.port_input = QSpinBox()
        self.port_input.setRange(1024, 65535)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Auto-generated if empty")
        
        server_layout.addRow("Port:", self.port_input)
        server_layout.addRow("Password:", self.password_input)
        server_group.setLayout(server_layout)
        
        # Ngrok settings
        ngrok_group = QGroupBox("Internet Access (Ngrok)")
        ngrok_layout = QFormLayout()
        
        self.enable_ngrok_check = QCheckBox("Enable Ngrok")
        self.ngrok_token_input = QLineEdit()
        self.ngrok_token_input.setPlaceholderText("Your Ngrok auth token")
        
        ngrok_layout.addRow(self.enable_ngrok_check)
        ngrok_layout.addRow("Auth Token:", self.ngrok_token_input)
        ngrok_group.setLayout(ngrok_layout)
        
        layout.addWidget(server_group)
        layout.addWidget(ngrok_group)
        layout.addStretch()
        
        self.tabs.addTab(tab, "Settings")

    def setup_log_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet("""
            QTextEdit {
                font-family: 'Courier New', monospace;
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 3px;
            }
        """)
        
        # Log controls
        btn_layout = QHBoxLayout()
        clear_btn = QPushButton("Clear Log")
        clear_btn.clicked.connect(self.log_view.clear)
        
        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch()
        
        layout.addWidget(self.log_view)
        layout.addLayout(btn_layout)
        
        self.tabs.addTab(tab, "Activity Log")

    def load_config(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT port, password, enable_ngrok, ngrok_token FROM config LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            port, password, enable_ngrok, ngrok_token = result
            self.port_input.setValue(port or 5000)
            self.password_input.setText(password or "")
            self.enable_ngrok_check.setChecked(enable_ngrok == 1)
            self.ngrok_token_input.setText(ngrok_token or "")

    def save_config(self):
        port = self.port_input.value()
        password = self.password_input.text() or secrets.token_urlsafe(12)
        enable_ngrok = 1 if self.enable_ngrok_check.isChecked() else 0
        ngrok_token = self.ngrok_token_input.text()
        
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM config")
        cursor.execute(
            "INSERT INTO config (port, password, enable_ngrok, ngrok_token) VALUES (?, ?, ?, ?)",
            (port, password, enable_ngrok, ngrok_token)
        )
        self.db.commit()

    def toggle_server(self):
        if self.server and self.server.running:
            self.stop_server()
        else:
            self.start_server()

    def start_server(self):
        self.save_config()
        
        port = self.port_input.value()
        password = self.password_input.text() or secrets.token_urlsafe(12)
        
        self.server = RemoteAppServer(port, password, self.parent_app)
        self.server_thread = QThread()
        
        # Connect signals
        self.server.server_started.connect(self.on_server_started)
        self.server.server_stopped.connect(self.on_server_stopped)
        self.server.command_received.connect(self.handle_command)
        self.server.connection_log.connect(self.log_message)
        self.server.ngrok_started.connect(self.on_ngrok_started)
        self.server.error_occurred.connect(self.on_error)
        
        self.server.moveToThread(self.server_thread)
        self.server_thread.started.connect(self.server.run_server)
        self.server_thread.start()
        
        self.toggle_btn.setText("Stop Server")
        self.toggle_btn.setStyleSheet("background-color: #d32f2f;")
        self.status_label.setText("Status: Starting server...")
        
        # Start Ngrok if enabled
        if self.enable_ngrok_check.isChecked() and self.ngrok_token_input.text():
            QTimer.singleShot(2000, lambda: self.server.start_ngrok(self.ngrok_token_input.text()))

    def stop_server(self):
        if self.server:
            self.server.shutdown_server()
            self.toggle_btn.setEnabled(False)
            self.status_label.setText("Status: Stopping server...")

    def on_server_started(self, local_url, network_url, qr_code):
        self.status_label.setText("Status: Server running")
        self.local_url_label.setText(f"Local URL: {local_url}")
        self.network_url_label.setText(f"Network URL: {network_url}")
        
        # Display QR code
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(qr_code))
        self.qr_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        self.copy_url_btn.setEnabled(True)
        self.open_browser_btn.setEnabled(True)
        
        self.log_message(f"Server started on port {self.server.port}")
        self.log_message(f"Local URL: {local_url}")
        self.log_message(f"Network URL: {network_url}")

    def on_ngrok_started(self, public_url):
        self.ngrok_url_label.setText(f"Internet URL: {public_url}")
        self.log_message(f"Ngrok tunnel established: {public_url}")
        
        # Update QR code with public URL
        qr_img = self.server.generate_qr_code(public_url)
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(qr_img))
        self.qr_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def on_server_stopped(self):
        self.status_label.setText("Status: Server stopped")
        self.local_url_label.setText("Local URL: -")
        self.network_url_label.setText("Network URL: -")
        self.ngrok_url_label.setText("Internet URL: -")
        self.qr_label.clear()
        
        self.toggle_btn.setText("Start Server")
        self.toggle_btn.setStyleSheet("background-color: #4285f4;")
        self.toggle_btn.setEnabled(True)
        
        self.copy_url_btn.setEnabled(False)
        self.open_browser_btn.setEnabled(False)
        
        if self.server_thread:
            self.server_thread.quit()
            self.server_thread.wait()
            self.server_thread = None
        
        self.server = None
        self.log_message("Server stopped")

    def on_error(self, error_msg):
        QMessageBox.critical(self, "Error", error_msg)
        self.log_message(f"Error: {error_msg}", error=True)
        self.stop_server()

    def handle_command(self, command):
        action = command.get('action')
        self.log_message(f"Command received: {action}")
        
        if action == 'click':
            # Handle click coordinates
            x = float(command.get('x', 0))
            y = float(command.get('y', 0))
            self.log_message(f"Click at ({x:.2f}, {y:.2f})")
            # Here you would convert these coordinates to actual window coordinates
            # and simulate a click on your application
        else:
            # Handle other commands
            handler_name = f"handle_remote_{action}"
            if hasattr(self.parent_app, handler_name):
                getattr(self.parent_app, handler_name)()
            elif hasattr(self.parent_app, action):
                getattr(self.parent_app, action)()

    def update_preview(self):
        if hasattr(self, 'server') and self.server and self.server.running:
            try:
                response = requests.get(
                    f'http://localhost:{self.server.port}/screenshot',
                    timeout=1
                )
                if response.status_code == 200:
                    pixmap = QPixmap()
                    pixmap.loadFromData(response.content)
                    if not pixmap.isNull():
                        self.preview_label.setPixmap(
                            pixmap.scaled(
                                self.preview_label.width(),
                                self.preview_label.height(),
                                Qt.KeepAspectRatio,
                                Qt.SmoothTransformation
                            )
                        )
            except Exception as e:
                self.log_message(f"Preview error: {str(e)}", error=True)

    def copy_url(self):
        clipboard = QApplication.clipboard()
        if hasattr(self.server, 'ngrok_url') and self.server.ngrok_url:
            clipboard.setText(self.server.ngrok_url)
        else:
            clipboard.setText(self.server.get_local_ip() + f":{self.server.port}")
        self.log_message("URL copied to clipboard")

    def open_browser(self):
        if hasattr(self.server, 'ngrok_url') and self.server.ngrok_url:
            webbrowser.open(self.server.ngrok_url)
        else:
            webbrowser.open(f"http://{self.server.get_local_ip()}:{self.server.port}")
        self.log_message("Opened in browser")

    def log_message(self, message, error=False):
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = "#d32f2f" if error else "#0d47a1"
        
        self.log_view.append(f"""
            <span style="color: #757575;">[{timestamp}]</span>
            <span style="color: {color};">{message}</span>
        """)
        self.log_view.verticalScrollBar().setValue(
            self.log_view.verticalScrollBar().maximum()
        )

    def closeEvent(self, event):
        self.stop_server()
        self.db.close()
        super().closeEvent(event)