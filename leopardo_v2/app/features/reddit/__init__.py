from .reddit_widget import RedditWidget
from .reddit_controller import RedditController

def create_reddit_feature():
    """
    Creates the reddit feature.
    """
    reddit_widget = RedditWidget()
    reddit_controller = RedditController()
    return reddit_widget, reddit_controller
