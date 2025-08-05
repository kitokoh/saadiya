from .home_model import HomeModel
from .home_widget import HomeWidget
from .home_controller import HomeController

def create_home_feature():
    model = HomeModel()
    view = HomeWidget()
    controller = HomeController(model, view)
    return view, controller
