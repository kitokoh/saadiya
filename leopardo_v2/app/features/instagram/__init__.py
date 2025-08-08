from .instagram_widget import InstagramWidget
from .instagram_controller import InstagramController

def create_instagram_feature():
    """
    Creates the instagram feature.
    """
    instagram_widget = InstagramWidget()
    instagram_controller = InstagramController()
    return instagram_widget, instagram_controller
