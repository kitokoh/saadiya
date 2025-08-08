from .twitter_widget import TwitterWidget
from .twitter_controller import TwitterController

def create_twitter_feature():
    """
    Creates the twitter feature.
    """
    twitter_widget = TwitterWidget()
    twitter_controller = TwitterController()
    return twitter_widget, twitter_controller
