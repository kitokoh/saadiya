import pandas as pd

class UserManagementModel:
    def __init__(self):
        self.users = pd.DataFrame(columns=['Username', 'Email', 'Role'])
        self._load_initial_data()

    def _load_initial_data(self):
        # Initial data for demonstration
        data = [
            {'Username': 'admin', 'Email': 'admin@example.com', 'Role': 'Admin'},
            {'Username': 'user1', 'Email': 'user1@example.com', 'Role': 'User'}
        ]
        self.users = pd.DataFrame(data)

    def get_users(self):
        return self.users

    def add_user(self, username, email, role):
        new_user = pd.DataFrame([{'Username': username, 'Email': email, 'Role': role}])
        self.users = pd.concat([self.users, new_user], ignore_index=True)

    def update_user(self, index, username, email, role):
        if 0 <= index < len(self.users):
            self.users.loc[index] = [username, email, role]

    def delete_user(self, index):
        if 0 <= index < len(self.users):
            self.users = self.users.drop(index).reset_index(drop=True)
