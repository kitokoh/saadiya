from .sales_model import SalesModel
from .sales_widget import SalesWidget
from .sales_controller import SalesController

def create_sales_feature():
    model = SalesModel()
    view = SalesWidget()
    controller = SalesController(model, view)
    return view, controller
