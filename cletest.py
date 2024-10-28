import os
import subprocess
import platform
import socket
import psutil
from PyQt5 import QtWidgets, QtCore


class SystemInfoApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('System Information')
        self.setGeometry(100, 100, 400, 300)

        # Create layout
        self.layout = QtWidgets.QVBoxLayout()

        # Create text area for displaying system info
        self.text_area = QtWidgets.QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.layout.addWidget(self.text_area)

        # Create a button to fetch system info and run the script
        self.button = QtWidgets.QPushButton('Get System Info and Run Script', self)
        self.button.clicked.connect(self.run_system_info_and_script)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def run_system_info_and_script(self):
        info = self.get_system_info()
        self.text_area.setPlainText(info)
        self.activate_virtualenv_and_run_script()

    def get_system_info(self):
        output = []

        output.append("Please wait... Gathering system information.\n")
        output.append("=========================")
        output.append("OPERATING SYSTEM")
        output.append(f"OS Name: {platform.system()}")
        output.append(f"OS Version: {platform.version()}")
        output.append("=========================")

        output.append("BIOS")
        output.append(f"System Type: {platform.machine()}")
        output.append("=========================")

        output.append("MEMORY")
        total_memory = psutil.virtual_memory().total / (1024 ** 2)  # Convert to MB
        output.append(f"Total Physical Memory: {total_memory:.2f} MB")
        output.append("=========================")

        output.append("CPU")
        output.append(f"CPU Name: {platform.processor()}")
        output.append("=========================")

        output.append("NETWORK ADDRESS")
        hostname = socket.gethostname()
        ip_addresses = socket.getaddrinfo(hostname, None)
        for ip in ip_addresses:
            if ip[0] == socket.AF_INET:  # IPv4
                output.append(f"IPv4 Address: {ip[4][0]}")
            elif ip[0] == socket.AF_INET6:  # IPv6
                output.append(f"IPv6 Address: {ip[4][0]}")
        output.append("=========================")

        return "\n".join(output)

    def activate_virtualenv_and_run_script(self):
        # Change to the specified directory
        os.chdir(r"D:\bons\Thefbkgrupshare\shareDoor\shareDoorEnv\Scripts")

        # Activate the virtual environment and run the script
        subprocess.call(r"activate.bat", shell=True)
        os.chdir(r"D:\bons\Thefbkgrupshare\shareDoor")
        subprocess.call(["python", "__post_in_groups__.py"])


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = SystemInfoApp()
    window.show()
    sys.exit(app.exec_())
