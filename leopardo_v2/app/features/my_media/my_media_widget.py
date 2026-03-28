import json
import os
import shutil
from PyQt5.QtCore import Qt, QTimer, QLocale, QSize
from PyQt5.QtGui import QPixmap, QIcon, QColor, QFont, QPainter, QPen, QLinearGradient, QBrush, QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox,
                             QMainWindow, QTableWidget, QTableWidgetItem, QPushButton,
                             QWidget, QMessageBox, QHeaderView, QMenu,
                             QAbstractItemView, QHBoxLayout, QStackedWidget,
                             QTableWidgetSelectionRange, QComboBox, QFileDialog, QListWidget, QListWidgetItem, QInputDialog)
from PyQt5.QtCore import QObject, pyqtSignal

# from .....imports import *
# from installFBrobotPy import updatejson
# from installFBrobotPy.sendatajson import FileTransferApp
# from installFBrobotPy.sendatajson2 import FileTransferApp2
# from installFBrobotPy.sendatajson3 import FileTransferApp3
# from .....translation import TranslatorManager  # Importer le gestionnaire de traductions
# from .....ui.footer import FooterSection
# from .....ui.header import HeaderSection
# from .....ui.secondry_menu import SecondaryMenu
# from .....update_media_dialog import UpdateMediaDialog

class PreviewDialog(QDialog):
    def __init__(self, media_path, description, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Media Preview")

        layout = QVBoxLayout()

        description_label = QLabel(description)
        layout.addWidget(description_label)

        if media_path.endswith(('.png', '.jpg', '.jpeg')):
            media_label = QLabel()
            media_label.setPixmap(QPixmap(media_path))
            layout.addWidget(media_label)
        else:
            media_label = QLabel("Video preview not available.")
            layout.addWidget(media_label)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

class MyMediaWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.media_folder = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-BLOG-Robot', 'media', 'media1')
        self.json_file = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-BLOG-Robot', 'text', 'text1', 'data.json')

        self.media_list = self.load_media()
        self.page_size = 10
        self.current_page = 0

        layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()

        media_label = QLabel("Media List:", self)
        media_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #003366;")
        top_layout.addWidget(media_label)

        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText("Search...")
        self.search_field.textChanged.connect(self.filter_table)
        self.search_field.setStyleSheet("""
            QLineEdit {
                padding: 6px;
                font-size: 14px;
                border: 1px solid #007BFF;
                border-radius: 5px;
            }
        """)
        top_layout.addWidget(self.search_field)

        self.add_media_button = QPushButton('Add Media', self)
        self.add_media_button.clicked.connect(self.add_new_media)
        top_layout.addWidget(self.add_media_button)

        layout.addLayout(top_layout)

        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Name', 'Description', 'Preview', 'Action'])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #007BFF;
                border-radius: 5px;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #007BFF;
                color: white;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton('Previous', self)
        self.prev_button.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.prev_button)

        self.next_button = QPushButton('Next', self)
        self.next_button.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.next_button)

        layout.addLayout(pagination_layout)

        self.populate_table()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_table)
        self.timer.start(5000)

    def load_media(self):
        if not os.path.exists(self.media_folder):
            os.makedirs(self.media_folder, exist_ok=True)

        media_files = [f for f in os.listdir(self.media_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.mp4'))]

        if not media_files:
            return [{"nom": "No media available", "description": "", "preview_path": ""}]

        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                json_data = json.load(f)
        else:
            json_data = {'posts': []}

        media_list = []
        for media in media_files:
            media_info = {
                'nom': media,
                'description': '',
                'preview_path': os.path.join(self.media_folder, media)
            }
            for post in json_data['posts']:
                if post.get('image') == media_info['preview_path']:
                    media_info['description'] = post.get('text', '')
                    break
            media_list.append(media_info)

        return media_list

    def populate_table(self):
        self.table.setRowCount(len(self.media_list))

        for row, media in enumerate(self.media_list):
            if not isinstance(media, dict):
                continue
            nom_item = QTableWidgetItem(media.get('nom', ''))
            nom_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row, 0, nom_item)

            description_item = QTableWidgetItem(media.get('description', ''))
            description_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            description_item.setToolTip(media.get('description', ''))
            description_item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.table.setItem(row, 1, description_item)

            preview_label = QLabel()
            if media.get('nom', '').endswith(('.png', '.jpg', '.jpeg')):
                pixmap = QPixmap(media['preview_path']).scaled(150, 150, Qt.KeepAspectRatio)
                preview_label.setPixmap(pixmap)
                preview_label.setFixedHeight(150)
            elif media.get('nom', '').endswith('.mp4'):
                preview_label.setText('Video File (Click to Preview)')
                preview_label.setStyleSheet("background-color: lightgray; padding: 10px; border-radius: 5px;")
                preview_label.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(row, 2, preview_label)

            action_button = QPushButton('Action')
            action_button.setMenu(self.create_action_menu(media))
            self.table.setCellWidget(row, 3, action_button)

    def create_action_menu(self, media):
        menu = QMenu()
        edit_action = menu.addAction("Edit")
        edit_action.triggered.connect(lambda: self.update_media(media))
        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(lambda: self.delete_media(media))
        preview_action = menu.addAction("Preview")
        preview_action.triggered.connect(lambda: self.show_preview(media['preview_path']))
        return menu

    def update_media(self, media):
        dialog = UpdateMediaDialog(media, self)
        if dialog.exec_():
            self.save_description(media)
            self.populate_table()

    def save_description(self, media):
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                json_data = json.load(f)
        else:
            json_data = {'posts': []}

        found = False
        for post in json_data['posts']:
            if post.get('image') == media.get('preview_path'):
                post['text'] = media['description']
                found = True
                break

        if not found:
            json_data['posts'].append({
                'text': media['description'],
                'image': media['preview_path']
            })

        with open(self.json_file, 'w') as f:
            json.dump(json_data, f, indent=4)

    def delete_media(self, media):
        msg_box = QMessageBox.question(self, 'Confirmation', f'Are you sure you want to delete {media["nom"]} ?', QMessageBox.Yes | QMessageBox.No)
        if msg_box == QMessageBox.Yes:
            os.remove(media['preview_path'])
            self.media_list.remove(media)
            self.save_to_json()
            self.populate_table()

    def save_to_json(self):
        json_data = {'posts': []}
        for media in self.media_list:
            json_data['posts'].append({
                'text': media['description'],
                'image': media['preview_path']
            })

        with open(self.json_file, 'w') as f:
            json.dump(json_data, f, indent=4)

    def add_new_media(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select media files",
            "",
            "Images (*.png *.jpg *.jpeg);;Videos (*.mp4 *.mov)",
            options=options
        )

        if files:
            media_data = self.load_json()
            max_key = 0
            for media in media_data.get('posts', []):
                try:
                    key = int(os.path.splitext(os.path.basename(media['image']))[0])
                    if key > max_key:
                        max_key = key
                except (ValueError, KeyError):
                    continue

            for file_path in files:
                extension = os.path.splitext(file_path)[1]
                max_key += 1
                new_name = f"{max_key}{extension}"
                new_path = os.path.join(self.media_folder, new_name)
                shutil.copy(file_path, new_path)
                media_data.get('posts', []).append({
                    "text": "Media description",
                    "image": new_path
                })
            self.update_json(media_data)
            QMessageBox.information(self, "Success", "Media added successfully!")
            self.refresh_table()

    def load_json(self):
        if not os.path.exists(self.json_file):
            os.makedirs(os.path.dirname(self.json_file), exist_ok=True)
            with open(self.json_file, 'w') as f:
                json.dump({"posts": []}, f)
        with open(self.json_file, 'r') as f:
            return json.load(f)

    def update_json(self, media_data):
        with open(self.json_file, 'w') as f:
            json.dump(media_data, f)

    def filter_table(self):
        search_text = self.search_field.text().lower()
        filtered_media = [media for media in self.media_list if search_text in media.get('nom', '').lower() or search_text in media.get('description', '').lower()]
        self.table.setRowCount(len(filtered_media))
        for row, media in enumerate(filtered_media):
            self.populate_table_row(row, media)

    def populate_table_row(self, row, media):
        self.table.setItem(row, 0, QTableWidgetItem(media.get('nom', '')))
        self.table.setItem(row, 1, QTableWidgetItem(media.get('description', '')))
        preview_label = QLabel()
        if media.get('nom', '').endswith(('.png', '.jpg', '.jpeg')):
            pixmap = QPixmap(media['preview_path']).scaled(150, 150, Qt.KeepAspectRatio)
            preview_label.setPixmap(pixmap)
            preview_label.setFixedHeight(150)
        elif media.get('nom', '').endswith('.mp4'):
            preview_label.setText('Video File (Click to Preview)')
            preview_label.setStyleSheet("background-color: lightgray; padding: 10px; border-radius: 5px;")
            preview_label.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(row, 2, preview_label)
        action_button = QPushButton('Action')
        action_button.setMenu(self.create_action_menu(media))
        self.table.setCellWidget(row, 3, action_button)

    def refresh_table(self):
        self.media_list = self.load_media()
        self.populate_table()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.populate_table()

    def next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.media_list):
            self.current_page += 1
            self.populate_table()

    def show_preview(self, media_path):
        description = "Media preview"
        preview_dialog = PreviewDialog(media_path, description, self)
        preview_dialog.exec_()

class UpdateMediaDialog(QDialog):
    def __init__(self, media, parent=None):
        super().__init__(parent)
        self.media = media
        self.setWindowTitle("Update Media")
        layout = QVBoxLayout(self)
        self.label = QLabel("Description:", self)
        layout.addWidget(self.label)
        self.description_input = QLineEdit(self)
        self.description_input.setText(media['description'])
        layout.addWidget(self.description_input)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def accept(self):
        self.media['description'] = self.description_input.text()
        super().accept()
