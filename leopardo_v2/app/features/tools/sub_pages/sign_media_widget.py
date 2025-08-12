import sys
import cv2
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QFileDialog, QMessageBox, QDialog)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint

class SignatureCaptureDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Capture Signature")
        self.setFixedSize(400, 200)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Sign in this area")
        self.label.setStyleSheet("background-color: white; border: 1px solid black;")

        self.image = QImage(self.label.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.drawing = False
        self.last_point = QPoint()

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_signature)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.accept)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.label.geometry().contains(event.pos()):
            self.drawing = True
            self.last_point = event.pos() - self.label.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.drawing and self.label.geometry().contains(event.pos()):
            painter = QPainter(self.image)
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))

            current_point = event.pos() - self.label.pos()
            painter.drawLine(self.last_point, current_point)
            painter.end()

            self.last_point = current_point
            self.update_preview()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def update_preview(self):
        self.label.setPixmap(QPixmap.fromImage(self.image))

    def clear_signature(self):
        self.image.fill(Qt.white)
        self.update_preview()

    def get_signature(self):
        return self.image

class SignMediaWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        self.image_label = QLabel("Please open an image file.")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.image_label)

        self.button_layout = QHBoxLayout()
        self.open_button = QPushButton("Open Image")
        self.open_button.clicked.connect(self.open_image)
        self.button_layout.addWidget(self.open_button)

        self.sign_button = QPushButton("Sign Image")
        self.sign_button.clicked.connect(self.sign_image)
        self.sign_button.setEnabled(False)
        self.button_layout.addWidget(self.sign_button)

        self.save_button = QPushButton("Save Image")
        self.save_button.clicked.connect(self.save_image)
        self.save_button.setEnabled(False)
        self.button_layout.addWidget(self.save_button)

        self.main_layout.addLayout(self.button_layout)

        self.image = None
        self.signature = None

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.image = cv2.imread(file_path)
            self.display_image(self.image)
            self.sign_button.setEnabled(True)

    def sign_image(self):
        dialog = SignatureCaptureDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.signature = dialog.get_signature()
            self.apply_signature()

    def apply_signature(self):
        if self.image is None or self.signature is None:
            return

        # Convert signature to OpenCV format
        signature_image = self.qimage_to_cvimage(self.signature)

        # Resize signature to fit the image
        h, w, _ = self.image.shape
        sh, sw, _ = signature_image.shape
        scale = min(w / sw, h / sh) * 0.2
        new_w, new_h = int(sw * scale), int(sh * scale)
        resized_signature = cv2.resize(signature_image, (new_w, new_h))

        # Position signature at the bottom right
        x_offset = w - new_w - 10
        y_offset = h - new_h - 10

        # Overlay signature
        roi = self.image[y_offset:y_offset + new_h, x_offset:x_offset + new_w]
        gray_signature = cv2.cvtColor(resized_signature, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray_signature, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        img_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        sig_fg = cv2.bitwise_and(resized_signature, resized_signature, mask=mask)
        dst = cv2.add(img_bg, sig_fg)
        self.image[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = dst

        self.display_image(self.image)
        self.save_button.setEnabled(True)

    def save_image(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            cv2.imwrite(file_path, self.image)
            QMessageBox.information(self, "Success", "Image saved successfully!")

    def display_image(self, cv_image):
        qimage = self.cvimage_to_qimage(cv_image)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def cvimage_to_qimage(self, cv_image):
        height, width, channel = cv_image.shape
        bytes_per_line = 3 * width
        return QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

    def qimage_to_cvimage(self, qimage):
        qimage = qimage.convertToFormat(QImage.Format_RGB888)
        width = qimage.width()
        height = qimage.height()
        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())
        arr = np.array(ptr).reshape(height, width, 3)
        return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
