from .marketing_robots_model import MarketingRobotsModel
from .marketing_robots_widget import MarketingRobotsWidget

class MarketingRobotsController:
    def __init__(self, model: MarketingRobotsModel, view: MarketingRobotsWidget):
        self.model = model
        self.view = view
        self.connect_signals()
        self.load_robots()

    def connect_signals(self):
        self.view.add_button.clicked.connect(self.add_robot)
        self.view.start_button.clicked.connect(self.start_robot)
        self.view.stop_button.clicked.connect(self.stop_robot)
        self.view.delete_button.clicked.connect(self.delete_robot)

    def load_robots(self):
        robots = self.model.get_robots()
        self.view.populate_table(robots)

    def add_robot(self):
        robot_data = self.view.show_add_robot_dialog()
        if robot_data:
            name, platform = robot_data
            self.model.add_robot(name, platform, "Stopped")
            self.load_robots()

    def start_robot(self):
        robot_id = self.view.get_selected_robot_id()
        if robot_id is None:
            self.view.show_message("No selection", "Please select a robot to start.")
            return
        self.model.update_robot_status(robot_id, "Running")
        self.load_robots()

    def stop_robot(self):
        robot_id = self.view.get_selected_robot_id()
        if robot_id is None:
            self.view.show_message("No selection", "Please select a robot to stop.")
            return
        self.model.update_robot_status(robot_id, "Stopped")
        self.load_robots()

    def delete_robot(self):
        robot_id = self.view.get_selected_robot_id()
        if robot_id is None:
            self.view.show_message("No selection", "Please select a robot to delete.")
            return
        self.model.delete_robot(robot_id)
        self.load_robots()
