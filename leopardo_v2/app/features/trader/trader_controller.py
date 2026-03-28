from .trader_model import TraderModel
from .trader_widget import TraderWidget

class TraderController:
    def __init__(self, model: TraderModel, view: TraderWidget):
        self.model = model
        self.view = view
        self.connect_signals()

    def connect_signals(self):
        pass
