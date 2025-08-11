from .groups_model import GroupsModel
from .groups_widget import GroupsWidget
from .groups_controller import GroupsController

def create_groups_feature():
    model = GroupsModel()
    view = GroupsWidget()
    controller = GroupsController(model, view)
    return view, controller
