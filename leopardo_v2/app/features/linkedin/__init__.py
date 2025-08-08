from .linkedin_widget import LinkedinWidget
from .linkedin_controller import LinkedInController

def create_linkedin_feature():
    """
    Creates the linkedin feature.
    """
    linkedin_widget = LinkedinWidget()
    linkedin_controller = LinkedInController()
    return linkedin_widget, linkedin_controller
