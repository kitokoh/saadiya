from .sales_templates_model import SalesTemplatesModel
from .sales_templates_widget import SalesTemplatesWidget
from .sales_templates_controller import SalesTemplatesController

def create_sales_templates_feature():
    """
    Creates the Sales Prompts / Templates feature.

    Returns:
        A tuple containing the sales templates widget and controller.
    """
    model = SalesTemplatesModel()
    view = SalesTemplatesWidget()
    controller = SalesTemplatesController(model, view)
    return view, controller
