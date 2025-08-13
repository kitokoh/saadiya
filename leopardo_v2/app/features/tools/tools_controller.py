import subprocess
from .tools_model import ToolsModel
from .tools_widget import ToolsWidget
from .sub_pages.edit_pdf_widget import EditPDFWidget
from .sub_pages.watermark_widget import WatermarkWidget
from .sub_pages.links_widget import LinksWidget
from .sub_pages.scheduler_widget import SchedulerWidget
from .sub_pages.sign_media_widget import SignMediaWidget

class ToolsController:
    def __init__(self, model: ToolsModel, view: ToolsWidget):
        self.model = model
        self.view = view
        self.connect_signals()
        self.pdf_editor = None
        self.watermark = None
        self.link_management = None
        self.scheduler = None
        self.sign_media = None

    def connect_signals(self):
        self.view.pdf_editor_button.clicked.connect(self.launch_pdf_editor)
        self.view.watermark_button.clicked.connect(self.launch_watermark)
        self.view.link_management_button.clicked.connect(self.launch_link_management)
        self.view.scheduler_button.clicked.connect(self.launch_scheduler)
        self.view.sign_media_button.clicked.connect(self.launch_sign_media)

    def launch_pdf_editor(self):
        if not self.pdf_editor:
            self.pdf_editor = EditPDFWidget()
        self.pdf_editor.show()

    def launch_watermark(self):
        if not self.watermark:
            self.watermark = WatermarkWidget()
        self.watermark.show()

    def launch_link_management(self):
        if not self.link_management:
            self.link_management = LinksWidget()
        self.link_management.show()

    def launch_scheduler(self):
        if not self.scheduler:
            self.scheduler = SchedulerWidget()
        self.scheduler.show()

    def launch_sign_media(self):
        if not self.sign_media:
            self.sign_media = SignMediaWidget()
        self.sign_media.show()
