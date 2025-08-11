from .sales_assistant_model import SalesAssistantModel
from .sales_assistant_widget import SalesAssistantWidget

class SalesAssistantController:
    def __init__(self, model: SalesAssistantModel, view: SalesAssistantWidget):
        self.model = model
        self.view = view
        self.connect_signals()

    def connect_signals(self):
        pass
