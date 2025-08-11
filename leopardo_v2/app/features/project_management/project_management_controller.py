from .project_management_model import ProjectManagementModel
from .project_management_widget import ProjectManagementWidget

class ProjectManagementController:
    def __init__(self, model: ProjectManagementModel, view: ProjectManagementWidget):
        self.model = model
        self.view = view
        self.connect_signals()
        self.load_projects()

    def connect_signals(self):
        self.view.add_button.clicked.connect(self.add_project)
        self.view.edit_button.clicked.connect(self.edit_project)
        self.view.delete_button.clicked.connect(self.delete_project)

    def load_projects(self):
        projects = self.model.get_projects()
        self.view.populate_table(projects)

    def add_project(self):
        project_data = self.view.show_add_edit_dialog()
        if project_data:
            name, description, status = project_data
            self.model.add_project(name, description, status)
            self.load_projects()

    def edit_project(self):
        index = self.view.get_selected_project_index()
        if index == -1:
            self.view.show_message("No selection", "Please select a project to edit.")
            return

        project = self.model.get_projects().iloc[index]
        project_data = self.view.show_add_edit_dialog(project)
        if project_data:
            name, description, status = project_data
            self.model.update_project(index, name, description, status)
            self.load_projects()

    def delete_project(self):
        index = self.view.get_selected_project_index()
        if index == -1:
            self.view.show_message("No selection", "Please select a project to delete.")
            return

        self.model.delete_project(index)
        self.load_projects()
