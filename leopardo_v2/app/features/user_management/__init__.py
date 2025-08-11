from .user_management_model import UserManagementModel
from .user_management_widget import UserManagementWidget
from .user_management_controller import UserManagementController

def create_user_management_feature():
    model = UserManagementModel()
    view = UserManagementWidget()
    controller = UserManagementController(model, view)
    return view, controller
