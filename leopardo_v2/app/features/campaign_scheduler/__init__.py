from .campaign_scheduler_model import CampaignSchedulerModel
from .campaign_scheduler_widget import CampaignSchedulerWidget
from .campaign_scheduler_controller import CampaignSchedulerController

def create_campaign_scheduler_feature():
    model = CampaignSchedulerModel()
    view = CampaignSchedulerWidget()
    controller = CampaignSchedulerController(model, view)
    return view, controller
