import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, 
                             QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem)
from PyQt5.QtGui import (QFont, QPixmap, QIcon, QColor, QLinearGradient, 
                         QPainter, QBrush, QPalette, QPainterPath, QPen)
from PyQt5.QtCore import (Qt, QSize, QPropertyAnimation, QEasingCurve, 
                          QParallelAnimationGroup, QSequentialAnimationGroup,
                          QPoint, QTimer, QRectF, QPointF)
import math
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QTime
from Home.login import Nova360ProApp
from Home.homeManagement import MainDashboard

import sys
import random
import math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QTabWidget,
                             QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem,
                             QGraphicsOpacityEffect)
from PyQt5.QtGui import (QFont, QPixmap, QIcon, QColor, QLinearGradient, 
                         QPainter, QBrush, QPalette, QPainterPath, QPen, QImage,
                         QPainter, QRadialGradient)
from PyQt5.QtCore import (Qt, QSize, QPropertyAnimation, QEasingCurve, 
                          QParallelAnimationGroup, QSequentialAnimationGroup,
                          QPoint, QTimer, QRectF, QPointF, QTime, QRect)


from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QFrame





class AdvancedParticleSystem(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

                # Configuration améliorée des particules
        self.particle_config = {
            'size_range': (3, 10),
            'speed_range': (0.5, 1.5),
            'alpha_range': (0.2, 0.6),
            'z_range': (0.3, 1.7)
        }
        self.particles = []
        self.init_particles(100)  # Augmentation du nombre de particules
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(20)  # Animation plus fluide
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        

        
        # Effet de profondeur amélioré
        self.depth_map = None
        self.init_depth_map()
        
    def init_particles(self, count):
        colors = [
            QColor(255, 255, 255, 120),  # Blanc plus visible
            QColor(150, 220, 255, 100),   # Bleu clair plus intense
            QColor(255, 150, 220, 100)    # Rose clair plus intense
        ]
        
        for _ in range(count):
            size = random.uniform(*self.particle_config['size_range'])
            x = random.uniform(0, self.width())
            y = random.uniform(0, self.height())
            speed = random.uniform(*self.particle_config['speed_range'])
            direction = random.uniform(0, 2 * math.pi)
            alpha = random.uniform(*self.particle_config['alpha_range'])
            color = random.choice(colors)
            color.setAlphaF(alpha)
            
            self.particles.append({
                'pos': QPointF(x, y),
                'size': size,
                'speed': speed,
                'direction': direction,
                'color': color,
                'original_alpha': alpha,
                'z_value': random.uniform(*self.particle_config['z_range']),
                'wobble': random.uniform(0.8, 1.2)  # Effet de tremblement
            })
    
    def init_depth_map(self):
        """Crée une carte de profondeur plus sophistiquée"""
        self.depth_map = QImage(self.size(), QImage.Format_ARGB32)
        self.depth_map.fill(Qt.transparent)
        
        painter = QPainter(self.depth_map)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Crée des zones de densité variable plus naturelles
        for _ in range(8):  # Plus de zones de densité
            center = QPointF(
                random.uniform(0, self.width()),
                random.uniform(0, self.height())
            )
            radius = random.uniform(150, 400)  # Zones plus grandes
            
            radial_grad = QRadialGradient(center, radius)
            radial_grad.setColorAt(0, QColor(255, 255, 255, 80))  # Plus opaque
            radial_grad.setColorAt(0.7, QColor(255, 255, 255, 30))
            radial_grad.setColorAt(1, Qt.transparent)
            
            painter.setBrush(QBrush(radial_grad))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(center, radius, radius)
        
        painter.end()
    
    def update_particles(self):
        """Mise à jour des particules avec mouvement plus naturel"""
        time = QTime.currentTime().msecsSinceStartOfDay() * 0.001
        width = self.width()
        height = self.height()
        
        for p in self.particles:
            # Mouvement avec effet de profondeur et tremblement
            move_factor = p['speed'] * p['z_value'] * (0.9 + 0.2 * math.sin(time * 3))
            move_x = move_factor * math.cos(p['direction'])
            move_y = move_factor * math.sin(p['direction'])
            
            new_x = p['pos'].x() + move_x
            new_y = p['pos'].y() + move_y
            
            # Rebond amélioré avec effet de fluidité
            if new_x < 0 or new_x > width:
                p['direction'] = math.pi - p['direction'] + random.uniform(-0.3, 0.3)
                new_x = max(0, min(width, new_x))
                
            if new_y < 0 or new_y > height:
                p['direction'] = -p['direction'] + random.uniform(-0.3, 0.3)
                new_y = max(0, min(height, new_y))
            
            p['pos'].setX(new_x)
            p['pos'].setY(new_y)
            
            # Animation alpha avec effet de vague plus prononcé
            alpha_var = 0.15 * math.sin(time * 2.5 + p['pos'].x() * 0.008)
            new_alpha = max(0.15, min(0.7, p['original_alpha'] + alpha_var))
            p['color'].setAlphaF(new_alpha)
            
            # Effet de pulsation pour la taille
            p['current_size'] = p['size'] * (0.9 + 0.1 * math.sin(time * 2 + p['pos'].y() * 0.01))
        
        self.update()
    
    def paintEvent(self, event):
        """Rendu optimisé des particules avec gestion de profondeur et effets"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        paint_rect = event.rect()

        # Tri des particules du fond vers l'avant (profondeur)
        for p in sorted(self.particles, key=lambda x: -x['z_value']):
            pos = p['pos']

            # Vérification des limites de l'écran
            if not (0 <= pos.x() < width and 0 <= pos.y() < height):
                continue

            # Vérification avec marge personnalisée
            margin = int(p['size'] * 2)
            expanded_rect = paint_rect.adjusted(-margin, -margin, margin, margin)
            if not expanded_rect.contains(pos.toPoint()):
                continue

            # Calcul de la transparence avec la profondeur (depth map)
            try:
                depth_alpha = QColor(self.depth_map.pixel(pos.toPoint())).alphaF() if self.depth_map else 0.5
            except Exception:
                depth_alpha = 0.5

            final_alpha = p['color'].alphaF() * (0.4 + 0.6 * depth_alpha)
            color = QColor(p['color'])
            color.setAlphaF(final_alpha)

            # Application d’un effet de flou si la particule est éloignée
            if p['z_value'] < 0.8:
                painter.setOpacity(0.6)
                size = p['current_size'] * 1.3
            else:
                painter.setOpacity(1.0)
                size = p['current_size']

            # Création du dégradé radial lumineux
            radial = QRadialGradient(pos, size)
            radial.setColorAt(0, color.lighter(150))
            radial.setColorAt(0.7, color)
            radial.setColorAt(1, Qt.transparent)

            # Dessin de la particule
            painter.setBrush(QBrush(radial))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(pos, size, size)

        painter.end()


    def resizeEvent(self, event):
        """Gestion du redimensionnement optimisée"""
        super().resizeEvent(event)
        
        # Recréation de la depth map seulement si nécessaire
        if not hasattr(self, 'depth_map') or self.depth_map.size() != self.size():
            self.init_depth_map()
            
        # Réinitialisation douce des particules
        for p in self.particles:
            if not (0 <= p['pos'].x() < self.width() and 0 <= p['pos'].y() < self.height()):
                p['pos'] = QPointF(
                    random.uniform(0, self.width()),
                    random.uniform(0, self.height())
                )


class PremiumButton(QPushButton):
    def __init__(self, text, primary_color, icon_path, parent=None):
        super().__init__(text, parent)
        self.primary_color = QColor(primary_color)
        self.icon_path = icon_path
        self.is_selected = False
        self.setup_ui()
        self.setup_animations()

    def setup_ui(self):
        self.setFixedSize(380, 280)
        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.2),
                    stop:1 rgba(255, 255, 255, 0.1)
                );
                border-radius: 20px;
                border: 2px solid rgba({self.primary_color.red()}, {self.primary_color.green()}, {self.primary_color.blue()}, 0.4);
                color: white;
                font-size: 28px;
                font-weight: bold;
                padding: 30px;
            }}
            QPushButton:hover {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.3),
                    stop:1 rgba(255, 255, 255, 0.2)
                );
                border: 2px solid rgba({self.primary_color.red()}, {self.primary_color.green()}, {self.primary_color.blue()}, 0.6);
            }}
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(self.primary_color.red(), self.primary_color.green(), self.primary_color.blue(), 150))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(25)
        layout.setAlignment(Qt.AlignCenter)

        self.icon_label = QLabel()
        pixmap = QPixmap(self.icon_path)
        if pixmap.isNull():
            self.icon_label.setText("🎯" if self.text() == "Marketing" else "🧠" if self.text() == "Finance" else "📊")
            self.icon_label.setStyleSheet("""
                QLabel {
                    font-size: 80px;
                    color: white;
                }
            """)
        else:
            self.icon_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        icon_effect = QGraphicsOpacityEffect()
        icon_effect.setOpacity(0.9)
        self.icon_label.setGraphicsEffect(icon_effect)

        layout.addWidget(self.icon_label, 0, Qt.AlignCenter)

        self.text_label = QLabel(self.text())
        self.text_label.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-size: 28px;
                font-weight: bold;
            }}
        """)

        text_shadow = QGraphicsDropShadowEffect()
        text_shadow.setBlurRadius(10)
        text_shadow.setColor(QColor(self.primary_color.red(), self.primary_color.green(), self.primary_color.blue(), 100))
        text_shadow.setOffset(2, 2)
        self.text_label.setGraphicsEffect(text_shadow)

        layout.addWidget(self.text_label, 0, Qt.AlignCenter)

        self.selection_indicator = QFrame()
        self.selection_indicator.setFixedHeight(6)
        self.selection_indicator.setStyleSheet(f"""
            QFrame {{
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 transparent,
                    stop:0.5 {self.primary_color.name()},
                    stop:1 transparent
                );
                border-radius: 3px;
            }}
        """)
        self.selection_indicator.hide()
        layout.addWidget(self.selection_indicator)

        self.indicator_anim = QPropertyAnimation(self.selection_indicator, b"maximumWidth")
        self.indicator_anim.setDuration(800)
        self.indicator_anim.setEasingCurve(QEasingCurve.OutBack)

    def setup_animations(self):
        self.hover_anim = QPropertyAnimation(self, b"geometry")
        self.hover_anim.setDuration(400)

        self.click_anim = QPropertyAnimation(self, b"geometry")
        self.click_anim.setDuration(200)

        self.shadow_anim = QPropertyAnimation(self.graphicsEffect(), b"blurRadius")
        self.shadow_anim.setDuration(400)

    def enterEvent(self, event):
        if not self.is_selected:
            self.hover_anim.stop()
            self.hover_anim.setStartValue(self.geometry())
            self.hover_anim.setEndValue(self.geometry().adjusted(-10, -10, 10, 10))
            self.hover_anim.setEasingCurve(QEasingCurve.OutBack)
            self.hover_anim.start()

            self.shadow_anim.stop()
            self.shadow_anim.setStartValue(30)
            self.shadow_anim.setEndValue(40)
            self.shadow_anim.start()

        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.is_selected:
            self.hover_anim.stop()
            self.hover_anim.setStartValue(self.geometry())
            self.hover_anim.setEndValue(self.geometry().adjusted(10, 10, -10, -10))
            self.hover_anim.setEasingCurve(QEasingCurve.OutBack)
            self.hover_anim.start()

            self.shadow_anim.stop()
            self.shadow_anim.setStartValue(40)
            self.shadow_anim.setEndValue(30)
            self.shadow_anim.start()

        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.click_anim.stop()
        self.click_anim.setStartValue(self.geometry())
        self.click_anim.setEndValue(self.geometry().adjusted(5, 5, -5, -5))
        self.click_anim.setEasingCurve(QEasingCurve.OutQuad)
        self.click_anim.start()

        self.graphicsEffect().setBlurRadius(50)
        QTimer.singleShot(200, lambda: self.graphicsEffect().setBlurRadius(30))

        super().mousePressEvent(event)

    def setSelected(self, selected):
        self.is_selected = selected
        if selected:
            self.selection_indicator.show()
            self.selection_indicator.setMaximumWidth(0)
            self.indicator_anim.stop()
            self.indicator_anim.setStartValue(0)
            self.indicator_anim.setEndValue(300)
            self.indicator_anim.start()

            self.setStyleSheet(f"""
                QPushButton {{
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 20px;
                    border: 2px solid rgba({self.primary_color.red()}, {self.primary_color.green()}, {self.primary_color.blue()}, 0.8);
                    color: white;
                    font-size: 28px;
                    font-weight: bold;
                    padding: 30px;
                }}
            """)
        else:
            self.selection_indicator.hide()
            self.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255, 255, 255, 0.2),
                        stop:1 rgba(255, 255, 255, 0.1)
                    );
                    border-radius: 20px;
                    border: 2px solid rgba({self.primary_color.red()}, {self.primary_color.green()}, {self.primary_color.blue()}, 0.4);
                    color: white;
                    font-size: 28px;
                    font-weight: bold;
                    padding: 30px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255, 255, 255, 0.3),
                        stop:1 rgba(255, 255, 255, 0.2)
                    );
                    border: 2px solid rgba({self.primary_color.red()}, {self.primary_color.green()}, {self.primary_color.blue()}, 0.6);
                }}
            """)


class MainWindow1(QMainWindow):
    def __init__(self, main_app=None):
        super().__init__()
        self.main_app = main_app
        self._color_offset = 0  # Variable privée pour stocker la valeur
        # ... reste de votre initialisation
        self.setWindowTitle("NOVA 360° Business Suite")
        self.setMinimumSize(1200, 800)
        self.setup_ui()
        
    def setup_ui(self):
        # Fond animé premium
        self.setup_animated_background()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Overlay pour le contenu
        content_overlay = QWidget()
        content_overlay.setStyleSheet("background: rgba(20, 40, 80, 0.3);")
        content_layout = QVBoxLayout(content_overlay)
        content_layout.setContentsMargins(80, 80, 80, 80)
        content_layout.setSpacing(10)
        
        # Header avec effet de lumière
        self.setup_header(content_layout)
        
        # Boutons avec conteneur premium
        self.setup_button_container(content_layout)
        self.setup_prompt_container(content_layout)        
        # Footer amélioré
        self.setup_premium_footer(content_layout)
        
        main_layout.addWidget(content_overlay)
        
        # Système de particules avancé
        self.particle_system = AdvancedParticleSystem(central_widget)
        self.particle_system.lower()
        
        # Initialiser les animations
        self.init_animations()

    @property
    def color_offset(self):
        """Getter pour color_offset"""
        return self._color_offset

    @color_offset.setter
    def color_offset(self, offset):
        """Setter pour color_offset sans récursion"""
        if self._color_offset != offset:  # Évite les mises à jour inutiles
            self._color_offset = offset
            self.update_background()  # Méthode séparée pour la mise à jour

    def update_background(self):
        """Met à jour le fond sans risque de récursion"""
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        
        pos1 = (self._color_offset) % 1.0
        pos2 = (self._color_offset + 0.3) % 1.0
        pos3 = (self._color_offset + 0.6) % 1.0
        
        gradient.setColorAt(pos1, QColor("#1a2980"))
        gradient.setColorAt(pos2, QColor("#26d0ce"))
        gradient.setColorAt(pos3, QColor("#ff416c"))
        gradient.setColorAt((pos3 + 0.3) % 1.0, QColor("#4A569D"))
        
        palette.setBrush(QPalette.Window, QBrush(gradient))
        super().setPalette(palette)  # Appel direct à la méthode parente

    def setup_animated_background(self):
        """Configuration de l'animation du fond"""
        self.bg_animation = QPropertyAnimation(self, b"color_offset")
        self.bg_animation.setDuration(20000)
        self.bg_animation.setStartValue(0)
        self.bg_animation.setEndValue(1)
        self.bg_animation.setLoopCount(-1)
        
        # Démarrer l'animation après un court délai
        QTimer.singleShot(500, self.bg_animation.start)










    def setup_animated_background1(self):
        # Fond animé avec gradient complexe
        self.bg_animation = QPropertyAnimation(self, b"color_offset")
        self.bg_animation.setDuration(20000)
        self.bg_animation.setStartValue(0)
        self.bg_animation.setEndValue(1)
        self.bg_animation.setLoopCount(-1)
        self.bg_animation.start()
        
        self.color_offset = 0
        
    def get_color_offset(self):
        return self.color_offset
    
    def set_color_offset(self, offset):
        self.color_offset = offset
        palette = self.palette()
        
        # Crée un gradient complexe animé
        gradient = QLinearGradient(0, 0, 0, self.height())
        
        # Points de couleur animés
        pos1 = (offset) % 1.0
        pos2 = (offset + 0.3) % 1.0
        pos3 = (offset + 0.6) % 1.0
        
        gradient.setColorAt(pos1, QColor("#1a2980"))
        gradient.setColorAt(pos2, QColor("#26d0ce"))
        gradient.setColorAt(pos3, QColor("#ff416c"))
        gradient.setColorAt((pos3 + 0.3) % 1.0, QColor("#4A569D"))
        
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
    
    color_offset = property(get_color_offset, set_color_offset)
    
    def setup_header(self, layout):
        header_container = QWidget()
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(1)
        header_layout.setAlignment(Qt.AlignCenter)
        
        # Titre principal avec effet néon
        self.header = QLabel("NOVA 360° Business Suite")
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 52px;
                font-weight: bold;
                margin-bottom: 5px;
            }
        """)
        
        # Effet de lueur animé
        self.header_shadow = QGraphicsDropShadowEffect()
        self.header_shadow.setBlurRadius(20)
        self.header_shadow.setColor(QColor(100, 200, 255, 200))
        self.header_shadow.setOffset(0, 0)
        self.header.setGraphicsEffect(self.header_shadow)
        
        # Animation de la lueur
        self.glow_anim = QPropertyAnimation(self.header_shadow, b"blurRadius")
        self.glow_anim.setDuration(3000)
        self.glow_anim.setEasingCurve(QEasingCurve.InOutSine)
        self.glow_anim.setStartValue(20)
        self.glow_anim.setEndValue(40)
        self.glow_anim.setLoopCount(-1)
        self.glow_anim.start()
        
        # Sous-titre avec effet de dégradé
        self.subtitle = QLabel("Plateforme Intelligente de Gestion d'Entreprise")
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet("""
            QLabel {
                color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ffffff,
                    stop:0.5 #a0d2ff,
                    stop:1 #ffffff
                );
                font-size: 24px;
                font-weight: medium;
            }
        """)
        
      #  header_layout.addWidget(self.header)
     #   header_layout.addWidget(self.subtitle)
      #  layout.addWidget(header_container, alignment=Qt.AlignTop)


   
    def setup_button_container(self, layout):
        # Conteneur principal avec effet de profondeur (hauteur réduite)
        button_container = QFrame()
        button_container.setFixedHeight(300)  # Hauteur réduite ici
        button_container.setStyleSheet("""
            QFrame {
                background: rgba(20, 40, 80, 0.3);
                border-radius: 30px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)

        # Layout horizontal avec centrage des boutons
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(40, 20, 40, 20)  # Marges ajustées
        button_layout.setSpacing(40)  # Espacement entre les boutons

        # Espaceur gauche
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Bouton Finance
        self.finance_btn = PremiumButton("Finance", "#33FF57", "finance.png")
        self.finance_btn.setFixedSize(320, 170)
        self.finance_btn.clicked.connect(self.open_finance)
        button_layout.addWidget(self.finance_btn)

        # Bouton Marketing (plus grand et central)
        self.marketing_btn = PremiumButton("Marketing", "#FF416C", "marketing.png")
        self.marketing_btn.setFixedSize(550, 230)
        self.marketing_btn.clicked.connect(self.open_marketing)
        button_layout.addWidget(self.marketing_btn)

        # Bouton Management
        self.management_btn = PremiumButton("Management", "#4A569D", "management.png")
        self.management_btn.setFixedSize(320, 170)
        self.management_btn.clicked.connect(self.open_management)
        button_layout.addWidget(self.management_btn)

        # Espaceur droit
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Ajout du container au layout principal
        layout.addWidget(button_container)


    # Assurez-vous d'avoir une méthode pour gérer le clic sur le bouton Finance

    def open_finance(self):
        self.finance_btn.setSelected(True)
        self.finance_btn.setSelected(False)
        
        tab_name = "Finance"
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return

        if not hasattr(self, 'Finance') or self.finance is None:
            from finance.finance import CryptoStrategyApp
            self.face_main = CryptoStrategyApp(parent=self.main_app)

        self.open_new_tab(tab_name, "cool.ico", self.face_main)
    
    def setup_prompt_container(self, layout):
        # Crée un conteneur principal transparent
        prompt_container = QFrame()
        prompt_container.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
        """)
        from promptes.promptmarketing import MarketingAIAnalyzer

        # # Crée une instance du widget personnalisé
        analyzer_widget = MarketingAIAnalyzer()

        # Crée une zone de défilement si le contenu déborde
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: rgba(0,0,0,0.1);
                width: 8px;
                margin: 4px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255,255,255,0.4);
                border-radius: 4px;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                background: none;
            }
        """)

        # Ajoute le widget à l'intérieur de la zone scrollable
        scroll_area.setWidget(analyzer_widget)

        # Layout pour le conteneur transparent
        container_layout = QVBoxLayout(prompt_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(scroll_area)

        # Ajoute tout dans le layout principal
        layout.addWidget(prompt_container, 1)

    def setup_premium_footer(self, layout):
        footer = QFrame()
        footer.setStyleSheet("""
            QFrame {
                background: rgba(0, 0, 0, 0.2);
                border-radius: 15px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                padding: 20px;
            }
        """)
        
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(30, 15, 30, 15)
        
        # Copyright avec effet de fondu
        copyright = QLabel("© 2023 NOVA 360° | Version Elite")
        copyright.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 14px;
                font-weight: medium;
            }
        """)
        
        fade_effect = QGraphicsOpacityEffect()
        fade_effect.setOpacity(0.8)
        copyright.setGraphicsEffect(fade_effect)
        
        # Espaceur central
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        # Bouton settings premium
        settings_btn = QPushButton()
        settings_btn.setIcon(QIcon.fromTheme("preferences-system"))
        settings_btn.setIconSize(QSize(28, 28))
        settings_btn.setFlat(True)
        settings_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                padding: 8px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.1);
            }
        """)
        
        # Effet de lueur sur le bouton settings
        settings_shadow = QGraphicsDropShadowEffect()
        settings_shadow.setBlurRadius(15)
        settings_shadow.setColor(QColor(100, 200, 255, 100))
        settings_shadow.setOffset(0, 0)
        settings_btn.setGraphicsEffect(settings_shadow)
        
        footer_layout.addWidget(copyright)
        footer_layout.addWidget(spacer)
        footer_layout.addWidget(settings_btn)
        
        #layout.addWidget(footer, 0, Qt.AlignBottom)
    
    def init_animations(self):
        # Animation d'entrée spectaculaire
        self.enter_animation = QParallelAnimationGroup()
        
        # Animation du titre (entrée depuis le haut avec rebond)
        title_anim = QPropertyAnimation(self.header, b"pos")
        title_anim.setDuration(1200)
        title_anim.setEasingCurve(QEasingCurve.OutElastic)
        original_pos = self.header.pos()
        title_anim.setStartValue(original_pos + QPoint(0, -200))
        title_anim.setEndValue(original_pos)
        
        # Animation du sous-titre (apparition progressive avec fondu)
        subtitle_anim = QPropertyAnimation(self.subtitle, b"windowOpacity")
        subtitle_anim.setDuration(1500)
        subtitle_anim.setStartValue(0)
        subtitle_anim.setEndValue(1)
        
        # Animation des boutons (entrée depuis les côtés)
        btn_group = QSequentialAnimationGroup()
        
        anim1 = QPropertyAnimation(self.marketing_btn, b"geometry")
        anim1.setDuration(1000)
        anim1.setEasingCurve(QEasingCurve.OutBack)
        start_pos1 = self.marketing_btn.geometry()
        start_pos1.moveLeft(-600)
        anim1.setStartValue(start_pos1)
        anim1.setEndValue(self.marketing_btn.geometry())
        
        anim2 = QPropertyAnimation(self.management_btn, b"geometry")
        anim2.setDuration(1000)
        anim2.setEasingCurve(QEasingCurve.OutBack)
        start_pos2 = self.management_btn.geometry()
        start_pos2.moveRight(self.width() + 600)
        anim2.setStartValue(start_pos2)
        anim2.setEndValue(self.management_btn.geometry())
        
        btn_group.addAnimation(anim1)
        btn_group.addAnimation(anim2)
        
        self.enter_animation.addAnimation(title_anim)
        self.enter_animation.addAnimation(subtitle_anim)
        self.enter_animation.addAnimation(btn_group)
        
        QTimer.singleShot(500, self.enter_animation.start)
    
    def open_marketing(self):
        self.marketing_btn.setSelected(True)
        self.management_btn.setSelected(False)
        
        tab_name = "Marketing"
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return

        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
            from Home.login import Nova360ProApp
            self.face_main = Nova360ProApp(main_app=self.main_app)

        self.open_new_tab(tab_name, "cool.ico", self.face_main)
    
    def open_management(self):
        self.marketing_btn.setSelected(False)
        self.management_btn.setSelected(True)
        
        tab_name = "Management"
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return

        if not hasattr(self, 'Management') or self.nova360pro is None:
            from Home.homeManagement import MainDashboard
            self.face_main = MainDashboard()

        self.open_new_tab(tab_name, "cool.ico", self.face_main)
        
    def open_new_tab(self, tab_name, icon_path, widget):
        if not self.main_app:
            print("Erreur : main_app n'est pas défini.")
            return

        self.main_app.add_custom_tab(widget, tab_name, icon_path)
  
    def find_tab_by_name(self, name):
        if not hasattr(self.main_app, 'tab_widget'):
            return -1
            
        for i in range(self.main_app.tab_widget.count()):
            if self.main_app.tab_widget.tabText(i) == name:
                return i
        return -1
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'particle_system'):
            self.particle_system.resize(self.size())
            self.particle_system.init_depth_map()  # Recalculer la depth map

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Configuration de police premium
    font = QFont()
    font.setFamily("Segoe UI" if sys.platform == "win32" else "Arial")
    font.setWeight(QFont.DemiBold)
    app.setFont(font)
    
    # Style global élégant
    app.setStyleSheet("""
        QToolTip {
            background-color: #1a2e45;
            color: white;
            border: 1px solid #2a4a6a;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
        }
        
        QTabWidget::pane {
            border: none;
            background: rgba(20, 40, 70, 0.9);
        }
        
        QTabBar::tab {
            background: rgba(30, 60, 90, 0.7);
            color: white;
            padding: 10px 20px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            margin-right: 2px;
            font-weight: medium;
        }
        
        QTabBar::tab:selected {
            background: rgba(50, 100, 150, 0.9);
            border-bottom: 2px solid #4a9eff;
        }
        
        QTabBar::tab:hover {
            background: rgba(70, 120, 170, 0.8);
        }
    """)
    
    window = MainWindow1()
    window.show()
    sys.exit(app.exec_())