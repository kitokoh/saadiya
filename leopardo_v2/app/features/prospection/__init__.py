from .prospection_model import ProspectionModel
from .prospection_widget import ProspectionWidget
from .prospection_controller import ProspectionController

def create_prospection_feature():
    """
    Creates the Prospection & Relances feature.

    Returns:
        A tuple containing the prospection widget and controller.
    """
    model = ProspectionModel()
    view = ProspectionWidget()
    controller = ProspectionController(model, view)
    return view, controller
