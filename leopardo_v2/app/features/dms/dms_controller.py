from .dms_model import DmsModel
from .dms_widget import DmsWidget

class DmsController:
    def __init__(self, model: DmsModel, view: DmsWidget):
        self.model = model
        self.view = view
        self.connect_signals()
        self.load_documents()

    def connect_signals(self):
        self.view.add_button.clicked.connect(self.add_document)
        self.view.edit_button.clicked.connect(self.edit_document)
        self.view.delete_button.clicked.connect(self.delete_document)

    def load_documents(self):
        documents = self.model.get_documents()
        self.view.populate_table(documents)

    def add_document(self):
        document_data = self.view.show_add_edit_dialog()
        if document_data:
            title, type, path = document_data
            self.model.add_document(title, type, path)
            self.load_documents()

    def edit_document(self):
        index = self.view.get_selected_document_index()
        if index == -1:
            self.view.show_message("No selection", "Please select a document to edit.")
            return

        document = self.model.get_documents().iloc[index]
        document_data = self.view.show_add_edit_dialog(document)
        if document_data:
            title, type, path = document_data
            self.model.update_document(index, title, type, path)
            self.load_documents()

    def delete_document(self):
        index = self.view.get_selected_document_index()
        if index == -1:
            self.view.show_message("No selection", "Please select a document to delete.")
            return

        self.model.delete_document(index)
        self.load_documents()
