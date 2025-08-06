from .finance_model import FinanceModel
from .finance_widget import FinanceWidget
from .finance_controller import FinanceController

def create_finance_feature():
    model = FinanceModel()
    view = FinanceWidget()
    controller = FinanceController(model, view)
    return view, controller
