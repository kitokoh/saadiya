from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox

class ContentGeneratorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setWindowTitle("Content Generator")

        self.topic_label = QLabel("Topic:")
        self.topic_input = QLineEdit()
        self.layout.addWidget(self.topic_label)
        self.layout.addWidget(self.topic_input)

        self.type_label = QLabel("Content Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Blog Post", "Tweet", "Email", "Product Description"])
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_combo)

        self.generate_button = QPushButton("Generate Content")
        self.layout.addWidget(self.generate_button)

        self.result_label = QLabel("Generated Content:")
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.layout.addWidget(self.result_label)
        self.layout.addWidget(self.result_text)

        self.history_label = QLabel("Generation History:")
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        self.layout.addWidget(self.history_label)
        self.layout.addWidget(self.history_text)

    def get_topic(self):
        return self.topic_input.text()

    def get_content_type(self):
        return self.type_combo.currentText()

    def set_generated_content(self, text):
        self.result_text.setText(text)

    def set_history(self, history_df):
        self.history_text.setText(history_df.to_string())

    def clear_inputs(self):
        self.topic_input.clear()
