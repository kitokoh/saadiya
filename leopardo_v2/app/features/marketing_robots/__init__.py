from .marketing_robots_model import MarketingRobotsModel
from .marketing_robots_widget import MarketingRobotsWidget
from .marketing_robots_controller import MarketingRobotsController

def create_marketing_robots_feature():
    model = MarketingRobotsModel()
    view = MarketingRobotsWidget()
    controller = MarketingRobotsController(model, view)
    return view, controller
