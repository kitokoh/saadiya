from .facebook_widget import FacebookWidget
from .facebook_controller import FacebookController

def create_facebook_feature():
    """
    Creates the facebook feature.
    """
    facebook_widget = FacebookWidget()
    facebook_controller = FacebookController()
    return facebook_widget, facebook_controller
