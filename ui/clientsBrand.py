import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QScrollArea, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont, QColor, QPalette

class LogoCarousel(QWidget):
    def __init__(self, logos, logos_per_view=5):
        super().__init__()
        self.logos = logos
        self.logos_per_view = logos_per_view
        self.current_index = 0
        self.initUI()

    def initUI(self):
        self.setLayout(QHBoxLayout())
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: #ffffff; border: none; border-radius: 15px;")

        self.carousel_widget = QWidget()
        self.carousel_layout = QHBoxLayout(self.carousel_widget)
        
        # Ajouter plusieurs labels pour afficher plusieurs logos en même temps
        self.logo_labels = []
        for _ in range(self.logos_per_view):
            logo_label = QLabel()
            logo_label.setFixedSize(150, 80)  # Définir une taille fixe pour chaque logo
            self.carousel_layout.addWidget(logo_label)
            self.logo_labels.append(logo_label)
        
        self.carousel_layout.setAlignment(Qt.AlignCenter)
        self.scroll_area.setWidget(self.carousel_widget)
        self.layout().addWidget(self.scroll_area)
        
        # Timer pour changer les logos tous les 3 secondes
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_logos)
        self.timer.start(3000)

        # Afficher les logos initiaux
        self.update_logos()

    def update_logos(self):
        # Afficher un groupe de logos à partir de l'index actuel
        for i in range(self.logos_per_view):
            logo_index = (self.current_index + i) % len(self.logos)
            pixmap = QPixmap(self.logos[logo_index])
            self.logo_labels[i].setPixmap(pixmap.scaled(150, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # Passer à l'index suivant
        self.current_index = (self.current_index + self.logos_per_view) % len(self.logos)

class Nosclient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trust Carousel")
        self.setGeometry(100, 100, 800, 400)
        self.initUI()

    def initUI(self):
        # Palette de couleurs
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 248, 255))  # Alice Blue
        palette.setColor(QPalette.WindowText, QColor(50, 50, 50))  # Dark Grey
        self.setPalette(palette)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # Title layout
        title_layout = QVBoxLayout()
        title_label = QLabel(self.tr("Ils nous font confiance"))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Helvetica Neue", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")  # Dark Blue

        subtitle_label = QLabel(self.tr("Découvrez nos partenaires de confiance"))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont("Helvetica Neue", 10, QFont.Normal))
        subtitle_label.setStyleSheet("color: #34495e;")  # Subtle dark blue-grey

        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)

        # Logo carousel
        logos = [
            "resources/nosclients/1.png", "resources/nosclients/2.png",
            "resources/nosclients/3.png", "resources/nosclients/4.png",
            "resources/nosclients/5.png", "resources/nosclients/6.png",
            "resources/nosclients/7.png", "resources/nosclients/8.png",
            "resources/nosclients/9.png", "resources/nosclients/10.png",
            "resources/nosclients/11.png", "resources/nosclients/12.png",
            "resources/nosclients/13.png", "resources/nosclients/14.png"



        ]
        logo_carousel = LogoCarousel(logos, logos_per_view=7)
        
        # Footer layout
        footer_layout = QHBoxLayout()
        footer_label = QLabel(self.tr("© 2024 - Marketing Robot . Next Update 15 November 15 2024"))
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setFont(QFont("Helvetica Neue", 11))
        footer_label.setStyleSheet("color: #7f8c8d;")  # Grey

        footer_layout.addWidget(footer_label)

        # Arrange main layout
        main_layout.addLayout(title_layout)
        main_layout.addWidget(logo_carousel)
        main_layout.addLayout(footer_layout)

        # Set the main layout
        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Nosclient()
    window.show()
    sys.exit(app.exec_())
