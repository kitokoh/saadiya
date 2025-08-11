from .groups_model import GroupsModel
from .groups_widget import GroupsWidget

class GroupsController:
    def __init__(self, model: GroupsModel, view: GroupsWidget):
        self.model = model
        self.view = view
        self.connect_signals()
        self.load_groups()

    def connect_signals(self):
        self.view.add_button.clicked.connect(self.add_group)
        self.view.edit_button.clicked.connect(self.edit_group)
        self.view.delete_button.clicked.connect(self.delete_group)

    def load_groups(self):
        groups = self.model.get_groups()
        self.view.populate_table(groups)

    def add_group(self):
        group_data = self.view.show_add_edit_dialog()
        if group_data:
            name, description = group_data
            self.model.add_group(name, description)
            self.load_groups()

    def edit_group(self):
        index = self.view.get_selected_group_index()
        if index == -1:
            self.view.show_message("No selection", "Please select a group to edit.")
            return

        group = self.model.get_groups().iloc[index]
        group_data = self.view.show_add_edit_dialog(group)
        if group_data:
            name, description = group_data
            self.model.update_group(index, name, description)
            self.load_groups()

    def delete_group(self):
        index = self.view.get_selected_group_index()
        if index == -1:
            self.view.show_message("No selection", "Please select a group to delete.")
            return

        self.model.delete_group(index)
        self.load_groups()
