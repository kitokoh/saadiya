from .settings_model import SettingsModel
from .settings_widget import SettingsWidget
from .settings_controller import SettingsController

def create_settings_feature():
    model = SettingsModel()
    view = SettingsWidget()
    controller = SettingsController(model, view)
    return view, controller
