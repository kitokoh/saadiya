from .my_groups_model import MyGroupsModel
from .my_groups_widget import MyGroupsWidget
from .my_groups_controller import MyGroupsController

def create_my_groups_feature():
    model = MyGroupsModel()
    view = MyGroupsWidget()
    controller = MyGroupsController(model, view)
    return view, controller
