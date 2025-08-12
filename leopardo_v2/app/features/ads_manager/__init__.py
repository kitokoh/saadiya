from .ads_manager_model import AdsManagerModel
from .ads_manager_widget import AdsManagerWidget
from .ads_manager_controller import AdsManagerController

def create_ads_manager_feature():
    model = AdsManagerModel()
    view = AdsManagerWidget()
    controller = AdsManagerController(model, view)
    return view, controller
