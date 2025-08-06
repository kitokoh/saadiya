from .sales_model import SalesModel
from .sales_widget import SalesWidget

class SalesController:
    def __init__(self, model: SalesModel, view: SalesWidget):
        self.model = model
        self.view = view
        self.connect_signals()

    def connect_signals(self):
        # Connect signals from the view to the controller methods
        pass
