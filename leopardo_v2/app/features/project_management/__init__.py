from .project_management_model import ProjectManagementModel
from .project_management_widget import ProjectManagementWidget
from .project_management_controller import ProjectManagementController

def create_project_management_feature():
    model = ProjectManagementModel()
    view = ProjectManagementWidget()
    controller = ProjectManagementController(model, view)
    return view, controller
