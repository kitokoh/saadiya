from .user_management_model import UserManagementModel
from .user_management_widget import UserManagementWidget

class UserManagementController:
    def __init__(self, model: UserManagementModel, view: UserManagementWidget):
        self.model = model
        self.view = view
        self.connect_signals()
        self.load_users()

    def connect_signals(self):
        self.view.add_button.clicked.connect(self.add_user)
        self.view.edit_button.clicked.connect(self.edit_user)
        self.view.delete_button.clicked.connect(self.delete_user)

    def load_users(self):
        users = self.model.get_users()
        self.view.populate_table(users)

    def add_user(self):
        user_data = self.view.show_add_edit_dialog()
        if user_data:
            username, email, role = user_data
            self.model.add_user(username, email, role)
            self.load_users()

    def edit_user(self):
        index = self.view.get_selected_user_index()
        if index == -1:
            self.view.show_message("No selection", "Please select a user to edit.")
            return

        user = self.model.get_users().iloc[index]
        user_data = self.view.show_add_edit_dialog(user)
        if user_data:
            username, email, role = user_data
            self.model.update_user(index, username, email, role)
            self.load_users()

    def delete_user(self):
        index = self.view.get_selected_user_index()
        if index == -1:
            self.view.show_message("No selection", "Please select a user to delete.")
            return

        self.model.delete_user(index)
        self.load_users()
