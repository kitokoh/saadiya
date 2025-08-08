from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QLabel
from PyQt5.QtCore import Qt

class PlaceholderWidget(QWidget):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel(name)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)

class YouTubeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)

        # Toolbar
        toolbar_layout = QHBoxLayout()
        self.dashboard_button = QPushButton("Dashboard")
        self.instances_button = QPushButton("Instances")
        self.media_button = QPushButton("Media")
        self.groups_button = QPushButton("Share")

        toolbar_layout.addWidget(self.dashboard_button)
        toolbar_layout.addWidget(self.instances_button)
        toolbar_layout.addWidget(self.media_button)
        toolbar_layout.addWidget(self.groups_button)

        main_layout.addLayout(toolbar_layout)

        # Content stack
        self.content_stack = QStackedWidget()
        self.dashboard_widget = self.create_dashboard_widget()
        self.instances_widget = self.create_instances_widget()
        self.media_widget = self.create_media_widget()
        self.groups_widget = self.create_groups_widget()

        self.content_stack.addWidget(self.dashboard_widget)
        self.content_stack.addWidget(self.instances_widget)
        self.content_stack.addWidget(self.media_widget)
        self.content_stack.addWidget(self.groups_widget)

        main_layout.addWidget(self.content_stack)

        self.setLayout(main_layout)

        # Connect signals
        self.dashboard_button.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.dashboard_widget))
        self.instances_button.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.instances_widget))
        self.media_button.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.media_widget))
        self.groups_button.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.groups_widget))

        self.content_stack.setCurrentWidget(self.dashboard_widget)

    def set_controller(self, controller):
        self.controller = controller
        self.start_robot_button.clicked.connect(self.controller.start_robot)
        self.add_instance_button.clicked.connect(self.controller.add_instance)
        self.add_media_button.clicked.connect(self.controller.add_media)
        self.add_group_button.clicked.connect(self.controller.add_group)

    def create_dashboard_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel("Dashboard")
        label.setAlignment(Qt.AlignCenter)
        self.start_robot_button = QPushButton("Start Robot")
        layout.addWidget(label)
        layout.addWidget(self.start_robot_button)
        widget.setLayout(layout)
        return widget

    def create_instances_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel("Instances Table")
        label.setAlignment(Qt.AlignCenter)
        self.add_instance_button = QPushButton("Add Instance")
        layout.addWidget(label)
        layout.addWidget(self.add_instance_button)
        widget.setLayout(layout)
        return widget

    def create_media_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel("Media Table")
        label.setAlignment(Qt.AlignCenter)
        self.add_media_button = QPushButton("Add Media")
        layout.addWidget(label)
        layout.addWidget(self.add_media_button)
        widget.setLayout(layout)
        return widget

    def create_groups_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel("Share Table")
        label.setAlignment(Qt.AlignCenter)
        self.add_group_button = QPushButton("Add Share")
        layout.addWidget(label)
        layout.addWidget(self.add_group_button)
        widget.setLayout(layout)
        return widget
