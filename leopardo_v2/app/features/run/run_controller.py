from .run_model import RunModel
from .run_widget import RunWidget

class RunController:
    def __init__(self, model: RunModel, view: RunWidget):
        self.model = model
        self.view = view
        self.connect_signals()

    def connect_signals(self):
        # Connect signals from the view to the controller methods
        pass
