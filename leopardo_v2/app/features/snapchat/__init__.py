from .snapchat_widget import SnapchatWidget
from .snapchat_controller import SnapchatController

def create_snapchat_feature():
    """
    Creates the snapchat feature.
    """
    snapchat_widget = SnapchatWidget()
    snapchat_controller = SnapchatController()
    return snapchat_widget, snapchat_controller
