from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton

class RibbonMenu(QWidget):
    def __init__(self, buttons=None):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        if buttons:
            for button_info in buttons:
                text = button_info.get("text", "")
                button = QPushButton(text)
                # Set object name for later retrieval
                button.setObjectName(f"ribbon_button_{text}")
                self.layout.addWidget(button)
