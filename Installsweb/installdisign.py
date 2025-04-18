import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QFrame, QScrollArea, QSizePolicy, QSpacerItem)
from PyQt5.QtCore import (Qt, QSize, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, 
                         QSequentialAnimationGroup, pyqtProperty)
from PyQt5.QtGui import (QFont, QIcon, QColor, QPalette, QLinearGradient, QPainter, 
                        QBrush, QFontDatabase, QPixmap)
from PyQt5.QtSvg import QSvgWidget

class GlassButton(QPushButton):
    """Bouton en verre avec effets de lumière et animations premium"""
    def __init__(self, text, icon=None, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(50)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Initialisation des propriétés d'animation
        self._opacity = 0.3
        self._blur_radius = 5
        self._light_pos = 0  # Initialisation manquante
        self._light_color = QColor(255, 255, 255, 80)
        
        # Police personnalisée
        font = QFont("Segoe UI", 11, QFont.Bold)
        self.setFont(font)
        
        # Style de base
        self.setStyleSheet("""
            GlassButton {
                color: white;
                border-radius: 8px;
                padding: 12px 24px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                background: rgba(255, 255, 255, 0.1);
            }
            GlassButton:hover {
                background: rgba(255, 255, 255, 0.15);
            }
            GlassButton:pressed {
                background: rgba(255, 255, 255, 0.05);
            }
        """)
        
        if icon:
            self.setIcon(QIcon(icon))
            self.setIconSize(QSize(24, 24))
        
        # Animation de survol
        self.hover_anim = QPropertyAnimation(self, b"opacity")
        self.hover_anim.setDuration(300)
        self.hover_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        self.blur_anim = QPropertyAnimation(self, b"blurRadius")
        self.blur_anim.setDuration(400)
        self.blur_anim.setEasingCurve(QEasingCurve.OutQuad)
        
        self.anim_group = QParallelAnimationGroup()
        self.anim_group.addAnimation(self.hover_anim)
        self.anim_group.addAnimation(self.blur_anim)
        
        # Effet de lumière au survol
        self.light_effect = QPropertyAnimation(self, b"lightPosition")
        self.light_effect.setDuration(1200)
        self.light_effect.setStartValue(0)
        self.light_effect.setEndValue(1)
        self.light_effect.setEasingCurve(QEasingCurve.InOutSine)
        self.light_effect.setLoopCount(-1)  # Infinite loop
    
    def paintEvent(self, event):
        """Dessin personnalisé pour l'effet de verre"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fond semi-transparent
        bg_color = QColor(40, 50, 70, 180)
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 8, 8)
        
        # Effet de lumière animé
        if self.underMouse():
            gradient = QLinearGradient(0, 0, self.width(), 0)
            gradient.setColorAt(max(0, self._light_pos - 0.3), QColor(255, 255, 255, 0))
            gradient.setColorAt(self._light_pos, self._light_color)
            gradient.setColorAt(min(1, self._light_pos + 0.3), QColor(255, 255, 255, 0))
            
            painter.setBrush(QBrush(gradient))
            painter.drawRoundedRect(self.rect(), 8, 8)
        
        # Texte et icône
        super().paintEvent(event)
    
    def enterEvent(self, event):
        """Animation au survol"""
        self.hover_anim.setStartValue(self._opacity)
        self.hover_anim.setEndValue(0.7)
        
        self.blur_anim.setStartValue(self._blur_radius)
        self.blur_anim.setEndValue(10)
        
        self.anim_group.start()
        self.light_effect.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        """Animation à la sortie"""
        self.hover_anim.setStartValue(self._opacity)
        self.hover_anim.setEndValue(0.3)
        
        self.blur_anim.setStartValue(self._blur_radius)
        self.blur_anim.setEndValue(5)
        
        self.anim_group.start()
        self.light_effect.stop()
        super().leaveEvent(event)
    
    # Propriétés animables
    @pyqtProperty(float)
    def opacity(self):
        return self._opacity
    
    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.update()
    
    @pyqtProperty(float)
    def blurRadius(self):
        return self._blur_radius
    
    @blurRadius.setter
    def blurRadius(self, value):
        self._blur_radius = value
        self.update()
    
    @pyqtProperty(float)
    def lightPosition(self):
        return self._light_pos
    
    @lightPosition.setter
    def lightPosition(self, value):
        self._light_pos = value
        self.update()


class InstallerCard(QWidget):
    """Carte d'application avec icône, description et bouton d'installation"""
    def __init__(self, app_name, description, icon_path=None, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Layout principal
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Icône de l'application
        self.icon_label = QLabel()
        if icon_path:
            if icon_path.endswith('.svg'):
                svg_widget = QSvgWidget(icon_path)
                svg_widget.setFixedSize(48, 48)
                layout.addWidget(svg_widget)
            else:
                pixmap = QPixmap(icon_path).scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.icon_label.setPixmap(pixmap)
                layout.addWidget(self.icon_label)
        
        # Contenu textuel
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)
        
        # Nom de l'application
        self.name_label = QLabel(app_name)
        self.name_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.name_label.setStyleSheet("color: white;")
        text_layout.addWidget(self.name_label)
        
        # Description
        self.desc_label = QLabel(description)
        self.desc_label.setFont(QFont("Segoe UI", 9))
        self.desc_label.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        self.desc_label.setWordWrap(True)
        text_layout.addWidget(self.desc_label)
        
        layout.addLayout(text_layout, stretch=1)
        
        # Bouton d'installation
        self.install_btn = GlassButton("Installer")
        self.install_btn.setFixedWidth(120)
        layout.addWidget(self.install_btn)
        
        # Style de la carte
        self.setStyleSheet("""
            InstallerCard {
                background: rgba(50, 60, 80, 0.5);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            InstallerCard:hover {
                background: rgba(60, 70, 90, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
        """)


class ModernInstaller(QMainWindow):
    """Fenêtre d'installation moderne avec effets premium"""
    def __init__(self, title="Application Installer", subtitle="Sélectionnez les applications à installer"):
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(800, 600)
        
        # Configuration du fond
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(30, 35, 45))
        gradient.setColorAt(1, QColor(15, 20, 30))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)
        
        # En-tête
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(5)
        
        # Titre avec effet de dégradé
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4facfe, stop:1 #00f2fe);
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent;
            }
        """)
        header_layout.addWidget(title_label)
        
        # Sous-titre
        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("Segoe UI", 11))
        subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        subtitle_label.setWordWrap(True)
        header_layout.addWidget(subtitle_label)
        
        main_layout.addWidget(header)
        
        # Zone de contenu
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(15)
        
        # Zone scrollable pour les cartes d'applications
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.1);
                width: 8px;
                margin: 0;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.3);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)
        
        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_content)
        self.scroll_layout.setSpacing(15)
        self.scroll_layout.setContentsMargins(5, 5, 5, 5)
        
        scroll_area.setWidget(scroll_content)
        content_layout.addWidget(scroll_area)
        
        main_layout.addWidget(content, stretch=1)
        
        # Footer avec bouton d'action global
        footer = QWidget()
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        
        # Bouton d'installation globale
        self.install_all_btn = GlassButton("Tout installer")
        self.install_all_btn.setFixedWidth(180)
        self.install_all_btn.setStyleSheet("""
            GlassButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4facfe, stop:1 #00f2fe);
                border: none;
            }
            GlassButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3a9cea, stop:1 #00d8e8);
            }
        """)
        footer_layout.addWidget(self.install_all_btn)
        
        # Espaceur
        footer_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        main_layout.addWidget(footer)
    
    def add_application(self, app_name, description, icon_path=None, install_callback=None):
        """Ajoute une application à l'installateur"""
        card = InstallerCard(app_name, description, icon_path)
        
        if install_callback:
            card.install_btn.clicked.connect(install_callback)
        
        self.scroll_layout.addWidget(card)
        return card


class ProfessionalInstaller:
    """Classe de haut niveau pour gérer l'installateur"""
    def __init__(self):
        self.app = QApplication(sys.argv)
        
        # Création de la fenêtre avec un design premium
        self.window = ModernInstaller(
            title="Suite Professionnelle",
            subtitle="Sélectionnez les applications premium à installer sur votre système"
        )
        
        # Configuration des applications
        self.setup_applications()
        
        # Connecter le bouton "Tout installer"
        self.window.install_all_btn.clicked.connect(self.install_all)
    
    def setup_applications(self):
        """Configure les applications disponibles"""
        # Exemple d'applications premium
        self.window.add_application(
            "Adobe Photoshop CC 2023",
            "Édition photo professionnelle avec IA intégrée et outils avancés",
            # Remplacez par un chemin d'icône réel ou utilisez une ressource
            None,
            lambda: self.install_app("Photoshop")
        )
        
        self.window.add_application(
            "Visual Studio Code Pro",
            "Éditeur de code avec débogueur intégré, terminal et extensions premium",
            None,
            lambda: self.install_app("VS Code Pro")
        )
    
    def install_app(self, app_name):
        """Installe une application spécifique"""
        print(f"Installation premium de {app_name}...")
        # Logique d'installation réelle ici
    
    def install_all(self):
        """Installe toutes les applications"""
        print("Installation de toutes les applications premium...")
        # Logique pour tout installer
    
    def run(self):
        """Affiche la fenêtre et lance l'application"""
        self.window.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    installer = ProfessionalInstaller()
    installer.run()