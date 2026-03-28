from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
                             QPushButton, QHBoxLayout, QHeaderView, QLineEdit,
                             QMessageBox, QApplication)

class ShortLinksWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setWindowTitle("Short Links & Trackers")

        # Title
        self.title_label = QLabel("Create and Manage Short Links")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        # Create New Link Section
        self.create_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL to shorten...")
        self.create_button = QPushButton("Create Short Link")
        self.create_layout.addWidget(self.url_input)
        self.create_layout.addWidget(self.create_button)
        self.layout.addLayout(self.create_layout)

        # Action Buttons
        self.button_layout = QHBoxLayout()
        self.refresh_button = QPushButton("Refresh List")
        self.copy_button = QPushButton("Copy Short Link")
        self.delete_button = QPushButton("Delete Link")
        self.button_layout.addWidget(self.refresh_button)
        self.button_layout.addWidget(self.copy_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addStretch()
        self.layout.addLayout(self.button_layout)

        # Links Table
        self.links_table = QTableWidget()
        self.links_table.setColumnCount(5)
        self.links_table.setHorizontalHeaderLabels(["ID", "Original URL", "Short Link", "Clicks", "Date"])
        self.links_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.links_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)
        self.links_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.links_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.links_table)

    def get_original_url(self):
        return self.url_input.text()

    def clear_url_input(self):
        self.url_input.clear()

    def display_links(self, links):
        self.links_table.setRowCount(len(links))
        base_url = "https://leo.pard/" # A dummy base url
        for row, link_data in enumerate(links):
            # link_data is expected to be a tuple: (id, original_url, short_code, click_count, creation_date)
            self.links_table.setItem(row, 0, QTableWidgetItem(str(link_data[0])))
            self.links_table.setItem(row, 1, QTableWidgetItem(link_data[1]))
            self.links_table.setItem(row, 2, QTableWidgetItem(f"{base_url}{link_data[2]}"))
            self.links_table.setItem(row, 3, QTableWidgetItem(str(link_data[3])))
            self.links_table.setItem(row, 4, QTableWidgetItem(link_data[4]))
        self.links_table.resizeColumnToContents(2)
        self.links_table.resizeColumnToContents(3)
        self.links_table.resizeColumnToContents(4)


    def get_selected_link_info(self):
        selected_rows = self.links_table.selectionModel().selectedRows()
        if not selected_rows:
            return None, None

        selected_row = selected_rows[0].row()
        link_id = int(self.links_table.item(selected_row, 0).text())
        short_link = self.links_table.item(selected_row, 2).text()
        return link_id, short_link

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        self.show_message("Copied", f"'{text}' has been copied to the clipboard.")
