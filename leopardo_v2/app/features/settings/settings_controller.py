from .settings_model import SettingsModel
from .settings_widget import SettingsWidget

class SettingsController:
    def __init__(self, model: SettingsModel, view: SettingsWidget):
        self.model = model
        self.view = view
        self.connect_signals()

    def connect_signals(self):
        # Connect signals from the view to the controller methods
        pass
