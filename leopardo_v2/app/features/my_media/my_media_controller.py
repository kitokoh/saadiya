from .my_media_model import MyMediaModel
from .my_media_widget import MyMediaWidget

class MyMediaController:
    def __init__(self, model: MyMediaModel, view: MyMediaWidget):
        self.model = model
        self.view = view
        self.connect_signals()
        self.load_media()

    def connect_signals(self):
        self.view.add_button.clicked.connect(self.add_media)
        self.view.edit_button.clicked.connect(self.edit_media)
        self.view.delete_button.clicked.connect(self.delete_media)

    def load_media(self):
        media = self.model.get_media()
        self.view.populate_table(media)

    def add_media(self):
        media_data = self.view.show_add_edit_dialog()
        if media_data:
            title, type, path = media_data
            self.model.add_media(title, type, path)
            self.load_media()

    def edit_media(self):
        index = self.view.get_selected_media_index()
        if index == -1:
            self.view.show_message("No selection", "Please select a media file to edit.")
            return

        media = self.model.get_media().iloc[index]
        media_data = self.view.show_add_edit_dialog(media)
        if media_data:
            title, type, path = media_data
            self.model.update_media(index, title, type, path)
            self.load_media()

    def delete_media(self):
        index = self.view.get_selected_media_index()
        if index == -1:
            self.view.show_message("No selection", "Please select a media file to delete.")
            return

        self.model.delete_media(index)
        self.load_media()
