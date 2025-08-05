from .marketing_model import MarketingModel
from .marketing_widget import MarketingWidget
from .marketing_controller import MarketingController

def create_marketing_feature():
    model = MarketingModel()
    view = MarketingWidget()
    controller = MarketingController(model, view)
    return view, controller
