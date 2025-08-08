from .tiktok_widget import TikTokWidget
from .tiktok_controller import TikTokController

def create_tiktok_feature():
    """
    Creates the tiktok feature.
    """
    tiktok_widget = TikTokWidget()
    tiktok_controller = TikTokController()
    return tiktok_widget, tiktok_controller
