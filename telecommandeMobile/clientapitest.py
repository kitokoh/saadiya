import sys
import requests
from zeroconf import Zeroconf, ServiceBrowser
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget

class ServerDiscovery:
    """Discover Flask server using Zeroconf."""

    def __init__(self):
        self.server_ip = None
        self.zeroconf = Zeroconf()

    def discover(self):
        def on_service_state_change(zeroconf, service_type, name, state_change):
            if state_change and name.endswith("._http._tcp.local."):
                info = zeroconf.get_service_info(service_type, name)
                if info:
                    self.server_ip = socket.inet_ntoa(info.addresses[0])
                    zeroconf.close()

        browser = ServiceBrowser(self.zeroconf, "_http._tcp.local.", handlers=[on_service_state_change])

    def get_server_ip(self):
        self.discover()
        while not self.server_ip:
            pass
        return self.server_ip

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Remote Control")
        self.setGeometry(100, 100, 400, 300)

        # Server discovery
        self.server_discovery = ServerDiscovery()
        self.server_ip = self.server_discovery.get_server_ip()

        # UI elements
        layout = QVBoxLayout()
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        self.run_button = QPushButton("Run Program")
        self.run_button.clicked.connect(self.run_program)

        layout.addWidget(self.output)
        layout.addWidget(self.run_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def run_program(self):
        program_path = "/path/to/your/program.exe"  # Update this path
        url = f"http://{self.server_ip}:5000/run"
        try:
            response = requests.post(url, json={"path": program_path})
            if response.status_code == 200:
                self.output.append(f"Program started: {program_path}")
            else:
                self.output.append(f"Error: {response.json()['error']}")
        except Exception as e:
            self.output.append(f"Failed to communicate with server: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
