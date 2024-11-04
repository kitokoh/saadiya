from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFrame, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class VideoAndDownloadWidget(QWidget):
    def __init__(self, video_links=None, download_links=None):
        """
        video_links : liste de deux URLs pour les vidéos YouTube
        download_links : liste de trois URLs pour les documents PDF à télécharger
        """
        super().__init__()
        self.setWindowTitle("Visionneuse de Vidéos et Téléchargement de Documents")
        self.setGeometry(200, 200, 850, 500)

        self.video_links = video_links or ["https://www.youtube.com/watch?v=abc123", "https://www.youtube.com/watch?v=def456"]
        self.download_links = download_links or ["Document1.pdf", "Document2.pdf", "Document3.pdf"]

        # Styles généraux
        self.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #1a237e;
            }
            QLineEdit, QPushButton {
                font-size: 14px;
                padding: 8px;
            }
            QPushButton {
                background-color: #3949ab;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5c6bc0;
            }
            QFrame {
                background-color: #f3f4f6;
                border-radius: 10px;
                padding: 15px;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
            }
            QWebEngineView {
                border: 2px solid #c5cae9;
                border-radius: 10px;
            }
        """)

        # Layout principal
        main_layout = QVBoxLayout()

        # Ligne 1 : deux vidéos YouTube
        video_layout = QHBoxLayout()
        
        # Vidéo 1
        video_frame_1 = self.create_video_frame("Vidéo Intéressante #1", self.video_links[0])
        video_layout.addWidget(video_frame_1)
        
        # Vidéo 2
        video_frame_2 = self.create_video_frame("Vidéo Intéressante #2", self.video_links[1])
        video_layout.addWidget(video_frame_2)

        main_layout.addLayout(video_layout)

        # Ligne 2 : trois boutons pour télécharger des documents PDF
        download_layout = QHBoxLayout()

        for i, link in enumerate(self.download_links):
            button_text = f"Télécharger Document {i + 1}"
            download_layout.addWidget(self.create_download_button(button_text, link))

        main_layout.addLayout(download_layout)
        self.setLayout(main_layout)

    def create_video_frame(self, title: str, url: str) -> QFrame:
        """
        Crée un cadre contenant un titre et un lecteur vidéo YouTube intégré.
        """
        frame = QFrame()
        frame_layout = QVBoxLayout()
        
        # Titre de la vidéo
        title_label = QLabel(title)
        frame_layout.addWidget(title_label)

        # Vue Web pour afficher la vidéo YouTube
        web_view = QWebEngineView()
        web_view.setUrl(QtCore.QUrl(url))
        web_view.setMinimumHeight(100)
        
        frame_layout.addWidget(web_view)
        frame.setLayout(frame_layout)

        return frame

    def create_download_button(self, text: str, link: str) -> QPushButton:
        """
        Crée un bouton de téléchargement avec un style.
        """
        button = QPushButton(text)
        button.clicked.connect(lambda: self.download_document(link))
        return button

    def download_document(self, link: str):
        """
        Ouvre le lien du document PDF dans le navigateur pour le téléchargement.
        """
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(link))

# Exemple d'utilisation
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    # Spécifier les liens des vidéos et des documents en paramètre
    video_urls = ["https://www.youtube.com/watch?v=xyz789", "https://www.youtube.com/watch?v=uvw123"]
    download_files = ["https://example.com/doc1.pdf", "https://example.com/doc2.pdf", "https://example.com/doc3.pdf"]

    widget = VideoAndDownloadWidget(video_links=video_urls, download_links=download_files)
    widget.show()
    app.exec_()
