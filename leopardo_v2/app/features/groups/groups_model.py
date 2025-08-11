import pandas as pd

class GroupsModel:
    def __init__(self):
        self.groups = pd.DataFrame(columns=['Name', 'Description'])
        self._load_initial_data()

    def _load_initial_data(self):
        # Initial data for demonstration
        data = [
            {'Name': 'Marketing Team', 'Description': 'The marketing team'},
            {'Name': 'Sales Team', 'Description': 'The sales team'}
        ]
        self.groups = pd.DataFrame(data)

    def get_groups(self):
        return self.groups

    def add_group(self, name, description):
        new_group = pd.DataFrame([{'Name': name, 'Description': description}])
        self.groups = pd.concat([self.groups, new_group], ignore_index=True)

    def update_group(self, index, name, description):
        if 0 <= index < len(self.groups):
            self.groups.loc[index] = [name, description]

    def delete_group(self, index):
        if 0 <= index < len(self.groups):
            self.groups = self.groups.drop(index).reset_index(drop=True)
