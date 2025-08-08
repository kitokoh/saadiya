from .youtube_widget import YouTubeWidget
from .youtube_controller import YouTubeController

def create_youtube_feature():
    """
    Creates the youtube feature.
    """
    youtube_widget = YouTubeWidget()
    youtube_controller = YouTubeController()
    return youtube_widget, youtube_controller
