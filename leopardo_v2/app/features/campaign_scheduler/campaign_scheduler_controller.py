from .campaign_scheduler_model import CampaignSchedulerModel
from .campaign_scheduler_widget import CampaignSchedulerWidget

class CampaignSchedulerController:
    def __init__(self, model: CampaignSchedulerModel, view: CampaignSchedulerWidget):
        self.model = model
        self.view = view
        self.connect_signals()
        self.load_campaigns()

    def connect_signals(self):
        self.view.add_button.clicked.connect(self.add_campaign)
        self.view.edit_button.clicked.connect(self.edit_campaign)
        self.view.delete_button.clicked.connect(self.delete_campaign)

    def load_campaigns(self):
        campaigns = self.model.get_campaigns()
        self.view.populate_table(campaigns)

    def add_campaign(self):
        campaign_data = self.view.show_add_edit_dialog()
        if campaign_data:
            name, platform, schedule, status = campaign_data
            self.model.add_campaign(name, platform, schedule, status)
            self.load_campaigns()

    def edit_campaign(self):
        campaign_data = self.view.get_selected_campaign_data()
        if campaign_data is None:
            self.view.show_message("No selection", "Please select a campaign to edit.")
            return

        new_campaign_data = self.view.show_add_edit_dialog(campaign_data)
        if new_campaign_data:
            name, platform, schedule, status = new_campaign_data
            self.model.update_campaign(campaign_data['id'], name, platform, schedule, status)
            self.load_campaigns()

    def delete_campaign(self):
        campaign_id = self.view.get_selected_campaign_id()
        if campaign_id is None:
            self.view.show_message("No selection", "Please select a campaign to delete.")
            return
        self.model.delete_campaign(campaign_id)
        self.load_campaigns()
