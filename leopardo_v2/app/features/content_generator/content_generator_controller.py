from .content_generator_model import ContentGeneratorModel
from .content_generator_widget import ContentGeneratorWidget

class ContentGeneratorController:
    def __init__(self, model: ContentGeneratorModel, view: ContentGeneratorWidget):
        self.model = model
        self.view = view
        self.connect_signals()

    def connect_signals(self):
        self.view.generate_button.clicked.connect(self.generate_content)

    def generate_content(self):
        topic = self.view.get_topic()
        content_type = self.view.get_content_type()
        if topic:
            generated_content = self.model.generate_content(topic, content_type)
            self.view.set_generated_content(generated_content)
            self.update_history()
            self.view.clear_inputs()
        else:
            self.view.set_generated_content("Please enter a topic.")

    def update_history(self):
        history = self.model.get_all_contents()
        self.view.set_history(history)

    def get_view(self):
        return self.view
