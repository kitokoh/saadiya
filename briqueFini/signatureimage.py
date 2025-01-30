import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit, QMessageBox,
    QComboBox, QSpinBox, QColorDialog, QHBoxLayout, QGridLayout
)
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sqlite3

class ImageSignatureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_preferences()

    def initUI(self):
        self.setWindowTitle('Image Signature App')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Image display
        self.label = QLabel('Importez une image et ajoutez une signature', self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Import image button
        self.import_button = QPushButton('Importer une image', self)
        self.import_button.clicked.connect(self.import_image)
        layout.addWidget(self.import_button)

        # Signature text input
        self.signature_text = QLineEdit(self)
        self.signature_text.setPlaceholderText('Entrez votre signature texte ici')
        layout.addWidget(self.signature_text)

        # Font customization
        font_layout = QHBoxLayout()
        self.font_combo = QComboBox(self)
        self.font_combo.addItems(["Arial", "Times New Roman", "Courier New", "Verdana"])
        self.font_combo.setCurrentText("Arial")
        font_layout.addWidget(self.font_combo)

        self.font_size = QSpinBox(self)
        self.font_size.setRange(10, 72)
        self.font_size.setValue(20)
        font_layout.addWidget(self.font_size)

        self.color_button = QPushButton('Choisir la couleur', self)
        self.color_button.clicked.connect(self.choose_color)
        font_layout.addWidget(self.color_button)

        layout.addLayout(font_layout)

        # Logo import button
        self.logo_button = QPushButton('Importer un logo (signature image)', self)
        self.logo_button.clicked.connect(self.import_logo)
        layout.addWidget(self.logo_button)

        # Signature position
        position_layout = QGridLayout()
        self.position_combo = QComboBox(self)
        self.position_combo.addItems(["En bas à gauche", "En bas à droite", "En haut à gauche", "En haut à droite"])
        self.position_combo.setCurrentIndex(0)
        position_layout.addWidget(QLabel('Position de la signature:'), 0, 0)
        position_layout.addWidget(self.position_combo, 0, 1)

        layout.addLayout(position_layout)

        # Filters
        self.filter_combo = QComboBox(self)
        self.filter_combo.addItems(["Aucun", "Flou", "Contour", "Détail", "Renforcement"])
        self.filter_combo.setCurrentIndex(0)
        layout.addWidget(QLabel('Filtre à appliquer:'))
        layout.addWidget(self.filter_combo)

        # Save button
        self.save_button = QPushButton('Sauvegarder l\'image avec signature', self)
        self.save_button.clicked.connect(self.save_image)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.image_path = None
        self.logo_path = None
        self.text_color = QColor(0, 0, 0)  # Default text color is black

        # Database for preferences
        self.db_connection = sqlite3.connect('preferences.db')
        self.create_preferences_table()

    def create_preferences_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                font TEXT,
                font_size INTEGER,
                text_color TEXT,
                position TEXT
            )
        ''')
        self.db_connection.commit()

    def load_preferences(self):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT font, font_size, text_color, position FROM preferences ORDER BY id DESC LIMIT 1')
        result = cursor.fetchone()
        if result:
            font, font_size, text_color, position = result
            self.font_combo.setCurrentText(font)
            self.font_size.setValue(font_size)
            self.text_color = QColor(text_color)
            self.position_combo.setCurrentText(position)

    def save_preferences(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            INSERT INTO preferences (font, font_size, text_color, position)
            VALUES (?, ?, ?, ?)
        ''', (
            self.font_combo.currentText(),
            self.font_size.value(),
            self.text_color.name(),
            self.position_combo.currentText()
        ))
        self.db_connection.commit()

    def import_image(self):
        options = QFileDialog.Options()
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Importer une image", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            self.label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))

    def import_logo(self):
        options = QFileDialog.Options()
        self.logo_path, _ = QFileDialog.getOpenFileName(self, "Importer un logo", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_color = color

    def apply_filter(self, image):
        filter_name = self.filter_combo.currentText()
        if filter_name == "Flou":
            return image.filter(ImageFilter.BLUR)
        elif filter_name == "Contour":
            return image.filter(ImageFilter.CONTOUR)
        elif filter_name == "Détail":
            return image.filter(ImageFilter.DETAIL)
        elif filter_name == "Renforcement":
            return image.filter(ImageFilter.EDGE_ENHANCE)
        else:
            return image

    def save_image(self):
        if not self.image_path:
            QMessageBox.warning(self, 'Erreur', 'Veuillez d\'abord importer une image.')
            return

        image = Image.open(self.image_path)
        draw = ImageDraw.Draw(image)

        # Apply filter
        image = self.apply_filter(image)

        # Add text signature
        signature_text = self.signature_text.text()
        if signature_text:
            font = ImageFont.truetype(self.font_combo.currentText(), self.font_size.value())
            position = self.position_combo.currentText()
            x, y = self.calculate_position(image, position)
            draw.text((x, y), signature_text, font=font, fill=self.text_color.name())

        # Add logo (image signature)
        if self.logo_path:
            logo = Image.open(self.logo_path)
            logo = logo.resize((100, 50))  # Resize logo if necessary
            x, y = self.calculate_position(image, position, logo=True)
            image.paste(logo, (x, y), logo)

        # Save the image
        save_folder = "saved_images"
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        save_path = os.path.join(save_folder, "signed_image.png")
        image.save(save_path)

        # Save preferences
        self.save_preferences()

        QMessageBox.information(self, 'Succès', f'Image sauvegardée sous {save_path}')

    def calculate_position(self, image, position, logo=False):
        if position == "En bas à gauche":
            return (10, image.height - 60 if logo else image.height - 30)
        elif position == "En bas à droite":
            return (image.width - 110 if logo else image.width - 200, image.height - 60 if logo else image.height - 30)
        elif position == "En haut à gauche":
            return (10, 10)
        elif position == "En haut à droite":
            return (image.width - 110 if logo else image.width - 200, 10)
        return (10, image.height - 30)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageSignatureApp()
    ex.show()
    sys.exit(app.exec_())