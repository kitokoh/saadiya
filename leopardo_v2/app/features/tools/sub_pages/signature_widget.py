from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                            QLabel, QApplication)
from PyQt5.QtGui import QPainter, QPen, QImage, QPixmap
from PyQt5.QtCore import Qt, QPoint

class SignatureCaptureDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Capture de Signature")
        self.setFixedSize(400, 200)

        # Zone de dessin
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Signez dans cette zone")
        self.label.setStyleSheet("background-color: white; border: 1px solid black;")

        # Image pour stocker la signature
        self.image = QImage(self.label.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        # Variables pour le dessin
        self.drawing = False
        self.last_point = QPoint()

        # Boutons
        self.clear_btn = QPushButton("Effacer")
        self.clear_btn.clicked.connect(self.clear_signature)

        self.save_btn = QPushButton("Enregistrer")
        self.save_btn.clicked.connect(self.accept)

        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.clicked.connect(self.reject)

        # Layout
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
        """Retourne l'image de la signature"""
        return self.image
