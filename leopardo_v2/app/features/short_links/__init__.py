from .short_links_model import ShortLinksModel
from .short_links_widget import ShortLinksWidget
from .short_links_controller import ShortLinksController

def create_short_links_feature():
    """
    Creates the Short Links & Trackers feature.

    Returns:
        A tuple containing the short links widget and controller.
    """
    model = ShortLinksModel()
    view = ShortLinksWidget()
    controller = ShortLinksController(model, view)
    return view, controller
