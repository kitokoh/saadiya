from .pinterest_widget import PinterestWidget
from .pinterest_controller import PinterestController

def create_pinterest_feature():
    """
    Creates the pinterest feature.
    """
    pinterest_widget = PinterestWidget()
    pinterest_controller = PinterestController()
    return pinterest_widget, pinterest_controller
