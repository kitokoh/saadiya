from .auto_responder_model import AutoResponderModel
from .auto_responder_widget import AutoResponderWidget

class AutoResponderController:
    def __init__(self, model: AutoResponderModel, view: AutoResponderWidget):
        self.model = model
        self.view = view
        self.connect_signals()
        self.load_responses()

    def connect_signals(self):
        self.view.add_button.clicked.connect(self.add_response)
        self.view.edit_button.clicked.connect(self.edit_response)
        self.view.delete_button.clicked.connect(self.delete_response)

    def load_responses(self):
        responses = self.model.responses
        self.view.populate_table(responses)

    def add_response(self):
        response_data = self.view.show_add_edit_dialog()
        if response_data:
            keyword, response = response_data
            self.model.add_response(keyword, response)
            self.load_responses()

    def edit_response(self):
        keyword = self.view.get_selected_response_keyword()
        if keyword is None:
            self.view.show_message("No selection", "Please select a response to edit.")
            return

        response = self.model.get_response(keyword)
        response_data = self.view.show_add_edit_dialog({'keyword': keyword, 'response': response})
        if response_data:
            new_keyword, new_response = response_data
            if new_keyword != keyword:
                del self.model.responses[keyword]
            self.model.add_response(new_keyword, new_response)
            self.load_responses()

    def delete_response(self):
        keyword = self.view.get_selected_response_keyword()
        if keyword is None:
            self.view.show_message("No selection", "Please select a response to delete.")
            return

        del self.model.responses[keyword]
        self.load_responses()
