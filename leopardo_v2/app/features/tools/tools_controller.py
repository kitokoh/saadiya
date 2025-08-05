from .tools_model import ToolsModel
from .tools_widget import ToolsWidget

class ToolsController:
    def __init__(self, model: ToolsModel, view: ToolsWidget):
        self.model = model
        self.view = view
        self.connect_signals()

    def connect_signals(self):
        self.view.pdf_editor_button.clicked.connect(self.launch_pdf_editor)
        self.view.watermark_button.clicked.connect(self.launch_watermark)
        self.view.link_management_button.clicked.connect(self.launch_link_management)
        self.view.scheduler_button.clicked.connect(self.launch_scheduler)

    def launch_pdf_editor(self):
        try:
            subprocess.Popen(["python", "tools/editpdf.py"])
        except FileNotFoundError:
            print("Error: Could not find 'tools/editpdf.py'")

    def launch_watermark(self):
        try:
            subprocess.Popen(["python", "tools/watermarks/watermark_window.py"])
        except FileNotFoundError:
            print("Error: Could not find 'tools/watermarks/watermark_window.py'")

    def launch_link_management(self):
        try:
            subprocess.Popen(["python", "liens/gestionliens.py"])
        except FileNotFoundError:
            print("Error: Could not find 'liens/gestionliens.py'")

    def launch_scheduler(self):
        try:
            subprocess.Popen(["python", "statistique/activiteprogramme.py"])
        except FileNotFoundError:
            print("Error: Could not find 'statistique/activiteprogramme.py'")
