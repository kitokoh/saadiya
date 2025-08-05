from .finance_model import FinanceModel
from .finance_widget import FinanceWidget

class FinanceController:
    def __init__(self, model: FinanceModel, view: FinanceWidget):
        self.model = model
        self.view = view
        self.connect_signals()

    def connect_signals(self):
        # Connect signals from the view to the controller methods
        pass
