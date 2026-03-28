from .my_media_model import MyMediaModel
from .my_media_widget import MyMediaWidget
from .my_media_controller import MyMediaController

def create_my_media_feature():
    model = MyMediaModel()
    view = MyMediaWidget()
    controller = MyMediaController(model, view)
    return view, controller
