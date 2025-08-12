from .sav_model import SavModel
from .sav_widget import SavWidget
from .sav_controller import SavController

def create_sav_feature():
    """
    Creates the SAV (After-Sales Service) feature.

    Returns:
        A tuple containing the SAV widget and controller.
    """
    model = SavModel()
    view = SavWidget()
    controller = SavController(model, view)
    return view, controller
