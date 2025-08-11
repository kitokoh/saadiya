import pandas as pd

class ProjectManagementModel:
    def __init__(self):
        self.projects = pd.DataFrame(columns=['Name', 'Description', 'Status'])
        self._load_initial_data()

    def _load_initial_data(self):
        # Initial data for demonstration
        data = [
            {'Name': 'Project Alpha', 'Description': 'The first project', 'Status': 'In Progress'},
            {'Name': 'Project Beta', 'Description': 'The second project', 'Status': 'Completed'}
        ]
        self.projects = pd.DataFrame(data)

    def get_projects(self):
        return self.projects

    def add_project(self, name, description, status):
        new_project = pd.DataFrame([{'Name': name, 'Description': description, 'Status': status}])
        self.projects = pd.concat([self.projects, new_project], ignore_index=True)

    def update_project(self, index, name, description, status):
        if 0 <= index < len(self.projects):
            self.projects.loc[index] = [name, description, status]

    def delete_project(self, index):
        if 0 <= index < len(self.projects):
            self.projects = self.projects.drop(index).reset_index(drop=True)
