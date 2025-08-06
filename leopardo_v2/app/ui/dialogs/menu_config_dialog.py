from PyQt5.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QDialogButtonBox

class MenuConfigDialog(QDialog):
    def __init__(self, menu_config, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure Menu Buttons")
        self.layout = QVBoxLayout(self)

        self.checkboxes = {}
        for button_name, visible in menu_config.items():
            checkbox = QCheckBox(button_name)
            checkbox.setChecked(visible)
            self.checkboxes[button_name] = checkbox
            self.layout.addWidget(checkbox)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def get_menu_config(self):
        config = {}
        for button_name, checkbox in self.checkboxes.items():
            config[button_name] = checkbox.isChecked()
        return config
