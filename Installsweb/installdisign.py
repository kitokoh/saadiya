import sys
import random
import math
from PyQt5.QtWidgets import (QApplication, QDialog, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QScrollArea, QCheckBox, QProgressBar, 
                            QMessageBox, QSizeGrip, QLineEdit, QSizePolicy, QSpacerItem,
                            QGraphicsDropShadowEffect, QFrame, QButtonGroup, QRadioButton)
from PyQt5.QtCore import (Qt, QSize, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, 
                         pyqtProperty, QTimer, QRectF, QPoint, QPointF, QSequentialAnimationGroup)
from PyQt5.QtGui import (QFont, QIcon, QColor, QPalette, QLinearGradient, QPainter, 
                        QBrush, QPainterPath, QFontDatabase, QPixmap, QPen, QConicalGradient,
                        QRadialGradient, QImage, QPainterPath)
from PyQt5.QtSvg import QSvgWidget

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, QPointF, Qt, QSize
from PyQt5.QtGui import QPainter, QColor, QBrush, QRadialGradient
import random
import math

class ParticleSystem(QWidget):
    def __init__(self, parent=None, particle_count=50):
        super().__init__(parent)
        self.particle_count = particle_count
        self.particles = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(20)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(100, 100)

    def resizeEvent(self, event):
        self.init_particles()
        super().resizeEvent(event)

    def init_particles(self):
        self.particles = []
        for _ in range(self.particle_count):
            self.particles.append({
                'pos': QPointF(random.uniform(0, self.width()), random.uniform(0, self.height())),
                'size': random.randint(3, 8),
                'speed': random.uniform(0.3, 1.2),
                'color': QColor(
                    random.randint(100, 200),
                    random.randint(100, 200),
                    random.randint(200, 255),
                    random.randint(30, 80)
                ),
                'direction': random.uniform(0, 2 * math.pi),
                'life': random.randint(100, 200),
                'max_life': random.randint(100, 200)
            })

    def update_particles(self):
        for p in self.particles:
            # Déplacement
            dx = math.cos(p['direction']) * p['speed']
            dy = math.sin(p['direction']) * p['speed']
            p['pos'] += QPointF(dx, dy)

            # Rebonds sur les bords
            if not (0 <= p['pos'].x() <= self.width()):
                p['direction'] = math.pi - p['direction']
            if not (0 <= p['pos'].y() <= self.height()):
                p['direction'] = -p['direction']

            # Cycle de vie
            p['life'] -= 1
            if p['life'] <= 0:
                p['pos'] = QPointF(random.uniform(0, self.width()), random.uniform(0, self.height()))
                p['life'] = p['max_life']

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for p in self.particles:
            alpha = int(255 * (p['life'] / p['max_life']))
            color = QColor(p['color'])
            color.setAlpha(alpha)

            # Glow effect
            glow = QRadialGradient(p['pos'], p['size'] * 2)
            glow.setColorAt(0, color)
            glow.setColorAt(1, QColor(color.red(), color.green(), color.blue(), 0))
            painter.setBrush(QBrush(glow))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(p['pos'], p['size'] * 2, p['size'] * 2)

            # Particle center
            painter.setBrush(QBrush(color))
            painter.drawEllipse(p['pos'], p['size'], p['size'])

class GlassButton(QPushButton):
    def __init__(self, text, icon=None, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(50)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Glass effect properties
        self._glass_opacity = 0.3
        self._glass_blur = 5
        self._light_position = 0
        self._light_color = QColor(255, 255, 255, 150)
        self._pulse_scale = 1.0
        self._ripple_alpha = 0
        self._ripple_radius = 0
        self._ripple_center = QPointF()
        
        # Advanced shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.shadow.setOffset(0, 8)
        self.setGraphicsEffect(self.shadow)
        
        # Premium style
        self.setStyleSheet("""
            GlassButton {
                color: white;
                border-radius: 15px;
                padding: 15px 30px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                background: rgba(255, 255, 255, 0.1);
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: 600;
                letter-spacing: 0.5px;
                text-transform: uppercase;
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
        
        # Setup animations
        self.setup_animations()
    
    def setup_animations(self):
        # Opacity animation
        self.opacity_anim = QPropertyAnimation(self, b"glassOpacity")
        self.opacity_anim.setDuration(400)
        self.opacity_anim.setEasingCurve(QEasingCurve.OutQuad)
        
        # Light sweep animation
        self.light_anim = QPropertyAnimation(self, b"lightPosition")
        self.light_anim.setDuration(1800)
        self.light_anim.setStartValue(0)
        self.light_anim.setEndValue(1)
        self.light_anim.setEasingCurve(QEasingCurve.InOutSine)
        self.light_anim.setLoopCount(-1)
        
        # Pulse animation
        self.pulse_anim = QPropertyAnimation(self, b"pulseScale")
        self.pulse_anim.setDuration(300)
        self.pulse_anim.setKeyValueAt(0, 1.0)
        self.pulse_anim.setKeyValueAt(0.5, 0.97)
        self.pulse_anim.setKeyValueAt(1, 1.0)
        self.pulse_anim.setEasingCurve(QEasingCurve.OutBack)
        
        # Ripple animation
        self.ripple_anim = QSequentialAnimationGroup(self)
        
        radius_anim = QPropertyAnimation(self, b"rippleRadius")
        radius_anim.setDuration(500)
        radius_anim.setStartValue(0)
        radius_anim.setEndValue(max(self.width(), self.height()) * 1.5)
        radius_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        alpha_anim = QPropertyAnimation(self, b"rippleAlpha")
        alpha_anim.setDuration(500)
        alpha_anim.setStartValue(80)
        alpha_anim.setEndValue(0)
        
        self.ripple_anim.addAnimation(radius_anim)
        self.ripple_anim.addAnimation(alpha_anim)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Apply pulse scale
        if self._pulse_scale != 1.0:
            painter.translate(self.width()/2, self.height()/2)
            painter.scale(self._pulse_scale, self._pulse_scale)
            painter.translate(-self.width()/2, -self.height()/2)
        
        rect = QRectF(self.rect()).adjusted(1, 1, -1, -1)
        path = QPainterPath()
        path.addRoundedRect(rect, 15, 15)
        
        # Frosted glass background
        bg_color = QColor(60, 70, 90, int(200 * self._glass_opacity))
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)
        
        # Light sweep effect
        if self.underMouse():
            gradient = QLinearGradient(0, 0, self.width(), 0)
            gradient.setColorAt(max(0, self._light_position - 0.3), QColor(255, 255, 255, 0))
            gradient.setColorAt(self._light_position, self._light_color)
            gradient.setColorAt(min(1, self._light_position + 0.3), QColor(255, 255, 255, 0))
            
            painter.setBrush(QBrush(gradient))
            painter.drawPath(path)
        
        # Ripple effect
        if self._ripple_alpha > 0:
            ripple_path = QPainterPath()
            ripple_path.addEllipse(self._ripple_center, self._ripple_radius, self._ripple_radius)
            
            clip_path = QPainterPath()
            clip_path.addRoundedRect(rect, 15, 15)
            painter.setClipPath(clip_path)
            
            ripple_color = QColor(255, 255, 255, self._ripple_alpha)
            painter.setBrush(QBrush(ripple_color))
            painter.setPen(Qt.NoPen)
            painter.drawPath(ripple_path)
            painter.setClipping(False)
        
        # Outer border
        painter.setBrush(Qt.NoBrush)
        border_pen = QPen(QColor(255, 255, 255, 80))
        border_pen.setWidth(1)  # Utiliser 1 au lieu de 1.5
        painter.setPen(border_pen)
        painter.drawPath(path)
        
        super().paintEvent(event)
    def enterEvent(self, event):
        self.opacity_anim.setStartValue(self._glass_opacity)
        self.opacity_anim.setEndValue(0.7)
        self.opacity_anim.start()
        self.light_anim.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.opacity_anim.setStartValue(self._glass_opacity)
        self.opacity_anim.setEndValue(0.3)
        self.opacity_anim.start()
        self.light_anim.stop()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        self._ripple_center = event.pos()
        self._ripple_alpha = 80
        self._ripple_radius = 0
        self.ripple_anim.start()
        self.pulse_anim.start()
        super().mousePressEvent(event)
    
    # Animated properties
    @pyqtProperty(float)
    def glassOpacity(self):
        return self._glass_opacity
    
    @glassOpacity.setter
    def glassOpacity(self, value):
        self._glass_opacity = value
        self.update()
    
    @pyqtProperty(float)
    def lightPosition(self):
        return self._light_position
    
    @lightPosition.setter
    def lightPosition(self, value):
        self._light_position = value
        self.update()
    
    @pyqtProperty(float)
    def pulseScale(self):
        return self._pulse_scale
    
    @pulseScale.setter
    def pulseScale(self, value):
        self._pulse_scale = value
        self.update()
    
    @pyqtProperty(int)
    def rippleAlpha(self):
        return self._ripple_alpha
    
    @rippleAlpha.setter
    def rippleAlpha(self, value):
        self._ripple_alpha = value
        self.update()
    
    @pyqtProperty(float)
    def rippleRadius(self):
        return self._ripple_radius
    
    @rippleRadius.setter
    def rippleRadius(self, value):
        self._ripple_radius = value
        self.update()

    # ... (le reste des méthodes reste inchangé)
class InstallerCard(QWidget):
    def __init__(self, app_name, description, icon_path=None, parent=None):
        super().__init__(parent)
        self._selected = True
        self._installed = False
        self._hover = False
        
        # Advanced shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(25)
        self.shadow.setColor(QColor(0, 0, 0, 100))
        self.shadow.setOffset(0, 8)
        self.setGraphicsEffect(self.shadow)
        
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(30)
        
        # Selection checkbox with custom design
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(True)
        self.checkbox.setStyleSheet("""
            QCheckBox {
                spacing: 15px;
            }
            QCheckBox::indicator {
                width: 24px;
                height: 24px;
                border: 2px solid rgba(255, 255, 255, 0.4);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.1);
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4facfe, stop:1 #00f2fe);
                border-color: rgba(255, 255, 255, 0.6);
                image: url(:/icons/check.svg);
            }
            QCheckBox::indicator:hover {
                border-color: rgba(255, 255, 255, 0.8);
            }
        """)
        layout.addWidget(self.checkbox)
        
        # App icon with glow effect
        self.icon_container = QWidget()
        self.icon_container.setFixedSize(64, 64)
        icon_layout = QVBoxLayout(self.icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
# Dans la classe InstallerCard, modifier la partie concernant l'icône SVG comme suit :

        if icon_path:
            if icon_path.endswith('.svg'):
                self.icon = QSvgWidget(icon_path)
                self.icon.setFixedSize(48, 48)
                # Créer un conteneur pour centrer l'icône SVG
                svg_container = QWidget()
                svg_layout = QVBoxLayout(svg_container)
                svg_layout.setContentsMargins(0, 0, 0, 0)
                svg_layout.addWidget(self.icon, 0, Qt.AlignCenter)
                self.icon = svg_container  # Remplacer l'icône par le conteneur
            else:
                self.icon = QLabel()
                self.icon.setPixmap(QPixmap(icon_path).scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.icon.setAlignment(Qt.AlignCenter)
        else:
            # Default icon
            self.icon = QLabel()
            self.icon.setPixmap(QPixmap(":/icons/default_app.svg").scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.icon.setAlignment(Qt.AlignCenter)

        self.icon.setFixedSize(48, 48)
        icon_layout.addWidget(self.icon, 0, Qt.AlignCenter)
        
        # Add glow effect to icon container
        self.icon_glow = QGraphicsDropShadowEffect(self.icon_container)
        self.icon_glow.setBlurRadius(20)
        self.icon_glow.setColor(QColor(79, 172, 254, 150))
        self.icon_glow.setOffset(0, 0)
        self.icon_container.setGraphicsEffect(self.icon_glow)
        
        layout.addWidget(self.icon_container)
        
        # Text content
        text_layout = QVBoxLayout()
        text_layout.setSpacing(10)
        text_layout.setContentsMargins(0, 0, 0, 0)
        
        self.name_label = QLabel(app_name)
        self.name_label.setStyleSheet("""
            color: white; 
            font-size: 18px; 
            font-weight: bold;
            font-family: 'Segoe UI';
        """)
        text_layout.addWidget(self.name_label)
        
        self.desc_label = QLabel(description)
        self.desc_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.7); 
            font-size: 14px;
            font-family: 'Segoe UI';
            line-height: 1.4;
        """)
        self.desc_label.setWordWrap(True)
        text_layout.addWidget(self.desc_label)
        
        # Add tags
        self.tags_layout = QHBoxLayout()
        self.tags_layout.setSpacing(8)
        
        for tag in ["Premium", "AI", "Cloud"]:
            tag_label = QLabel(tag)
            tag_label.setStyleSheet("""
                QLabel {
                    color: rgba(255, 255, 255, 0.9);
                    background: rgba(79, 172, 254, 0.2);
                    border-radius: 4px;
                    padding: 2px 8px;
                    font-size: 10px;
                    font-weight: bold;
                }
            """)
            self.tags_layout.addWidget(tag_label)
        
        self.tags_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        text_layout.addLayout(self.tags_layout)
        
        layout.addLayout(text_layout, 1)
        
        # Install button
        self.install_btn = GlassButton("Installer")
        self.install_btn.setFixedWidth(140)
        self.install_btn.setStyleSheet("""
            GlassButton {
                background: rgba(79, 172, 254, 0.2);
                border: 1px solid rgba(79, 172, 254, 0.4);
            }
        """)
        layout.addWidget(self.install_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(140)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                background: rgba(0, 0, 0, 0.2);
                height: 12px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4facfe, stop:1 #00f2fe);
                border-radius: 7px;
            }
        """)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        # Style and animations
        self.setup_styles()
        self.setup_animations()
        
        # Connections
        self.checkbox.stateChanged.connect(self.on_selection_changed)
    
    def setup_styles1(self):
        self.setStyleSheet("""
            InstallerCard {
                background: rgba(50, 60, 80, 0.6);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
            InstallerCard:hover {
                background: rgba(60, 70, 90, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.25);
            }
        """)







    
    def setup_styles(self):
        # Nouvelle palette de couleurs harmonieuses
        self.primary_color = QColor(94, 129, 172)  # Bleu doux
        self.secondary_color = QColor(143, 110, 164)  # Violet doux
        self.accent_color = QColor(72, 189, 170)  # Turquoise
        self.highlight_color = QColor(255, 255, 255)  # Blanc pur pour les highlights


        # Couleurs révisées pour meilleur contraste
        self.text_color = QColor(230, 230, 230)    # Blanc légèrement grisé
        self.background_color = QColor(50, 55, 65)  # Fond légèrement plus clair que le conteneur

        # Styles révisés
        # self.setStyleSheet(f"""
        #     InstallerCard {{
        #         background: rgba(40, 47, 60, 0.85);
        #         border-radius: 20px;
        #         border: 1px solid rgba({self.primary_color.red()}, {self.primary_color.green()}, {self.primary_color.blue()}, 0.3);
        #     }}
        #     InstallerCard:hover {{
        #         background: rgba(50, 58, 74, 0.9);
        #         border: 1px solid rgba({self.primary_color.red()}, {self.primary_color.green()}, {self.primary_color.blue()}, 0.5);
        #     }}
        # """)

        self.setStyleSheet(f"""
            InstallerCard {{
                background: rgba(40, 47, 60, 0.85);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.15);
            }}
            InstallerCard:hover {{
                background: rgba({self.background_color.red()+10}, {self.background_color.green()+10}, {self.background_color.blue()+10}, 0.75);
                border: 1px solid rgba({self.primary_color.red()}, {self.primary_color.green()}, {self.primary_color.blue()}, 0.5);

              }}
        """)
        # Mise à jour du style du checkbox
        self.checkbox.setStyleSheet(f"""
            QCheckBox {{
                spacing: 15px;
            }}
            QCheckBox::indicator {{
                width: 24px;
                height: 24px;
                border: 2px solid rgba({self.text_color.red()}, {self.text_color.green()}, {self.text_color.blue()}, 0.4);
                border-radius: 8px;
                background: rgba({self.text_color.red()}, {self.text_color.green()}, {self.text_color.blue()}, 0.1);
            }}
            QCheckBox::indicator:checked {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba({self.primary_color.red()}, {self.primary_color.green()}, {self.primary_color.blue()}, 255),
                    stop:1 rgba({self.accent_color.red()}, {self.accent_color.green()}, {self.accent_color.blue()}, 255));
                border-color: rgba({self.highlight_color.red()}, {self.highlight_color.green()}, {self.highlight_color.blue()}, 0.6);
            }}
            QCheckBox::indicator:hover {{
                border-color: rgba({self.highlight_color.red()}, {self.highlight_color.green()}, {self.highlight_color.blue()}, 0.8);
            }}
        """)

        # Mise à jour du texte
        self.name_label.setStyleSheet(f"""
            color: {self.text_color.name()};
            font-size: 18px;
            font-weight: bold;
            font-family: 'Segoe UI';
        """)

        self.desc_label.setStyleSheet(f"""
            color: rgba({self.text_color.red()}, {self.text_color.green()}, {self.text_color.blue()}, 0.85);
            font-size: 14px;
            font-family: 'Segoe UI';
            line-height: 1.4;
        """)

        # Mise à jour des tags
        for i in range(self.tags_layout.count()):
            widget = self.tags_layout.itemAt(i).widget()
            if isinstance(widget, QLabel):
                widget.setStyleSheet(f"""
                    QLabel {{
                        color: {self.highlight_color.name()};
                        background: rgba({self.secondary_color.red()}, {self.secondary_color.green()}, {self.secondary_color.blue()}, 0.25);
                        border-radius: 4px;
                        padding: 2px 8px;
                        font-size: 10px;
                        font-weight: bold;
                    }}
                """)

        # Mise à jour du bouton d'installation
        self.install_btn.setStyleSheet(f"""
            GlassButton {{
                background: rgba({self.primary_color.red()}, {self.primary_color.green()}, {self.primary_color.blue()}, 0.25);
                border: 1px solid rgba({self.primary_color.red()}, {self.primary_color.green()}, {self.primary_color.blue()}, 0.4);
            }}
        """)

        # Mise à jour de la barre de progression
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid rgba({self.text_color.red()}, {self.text_color.green()}, {self.text_color.blue()}, 0.2);
                border-radius: 8px;
                background: rgba(0, 0, 0, 0.2);
                height: 12px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba({self.primary_color.red()}, {self.primary_color.green()}, {self.primary_color.blue()}, 255),
                    stop:1 rgba({self.accent_color.red()}, {self.accent_color.green()}, {self.accent_color.blue()}, 255));
                border-radius: 7px;
            }}
        """)

        # Mise à jour de l'effet de glow de l'icône
        self.icon_glow.setColor(QColor(self.primary_color.red(), self.primary_color.green(), self.primary_color.blue(), 150))
    
    def setup_animations(self):
        # Selection animation
        self.selection_anim = QPropertyAnimation(self, b"selectionState")
        self.selection_anim.setDuration(400)
        self.selection_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        # Hover animation
        self.hover_anim = QPropertyAnimation(self, b"hoverState")
        self.hover_anim.setDuration(300)
        self.hover_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        # Icon glow animation
        self.glow_anim = QPropertyAnimation(self.icon_glow, b"blurRadius")
        self.glow_anim.setDuration(500)
        self.glow_anim.setEasingCurve(QEasingCurve.OutBack)
    
    def enterEvent(self, event):
        self._hover = True
        self.hover_anim.setStartValue(0)
        self.hover_anim.setEndValue(1)
        self.hover_anim.start()
        
        self.glow_anim.setStartValue(20)
        self.glow_anim.setEndValue(30)
        self.glow_anim.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self._hover = False
        self.hover_anim.setStartValue(1)
        self.hover_anim.setEndValue(0)
        self.hover_anim.start()
        
        self.glow_anim.setStartValue(30)
        self.glow_anim.setEndValue(20)
        self.glow_anim.start()
        super().leaveEvent(event)
    
    def on_selection_changed(self, state):
        self._selected = state == Qt.Checked
        self.selection_anim.setStartValue(0.5 if self._selected else 1.0)
        self.selection_anim.setEndValue(1.0 if self._selected else 0.5)
        self.selection_anim.start()
    
    def start_installation(self):
        self.install_btn.hide()
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(100)
        
        # Animate icon during installation
        self.icon_install_anim = QPropertyAnimation(self.icon, b"pos")
        self.icon_install_anim.setDuration(2000)
        self.icon_install_anim.setLoopCount(-1)
        self.icon_install_anim.setKeyValueAt(0, self.icon.pos())
        self.icon_install_anim.setKeyValueAt(0.25, self.icon.pos() + QPoint(0, -5))
        self.icon_install_anim.setKeyValueAt(0.5, self.icon.pos())
        self.icon_install_anim.setKeyValueAt(0.75, self.icon.pos() + QPoint(0, 5))
        self.icon_install_anim.setKeyValueAt(1, self.icon.pos())
        self.icon_install_anim.start()
    
    def update_progress(self):
        value = self.progress_bar.value()
        if value >= 100:
            self.progress_timer.stop()
            self.icon_install_anim.stop()
            self.progress_bar.hide()
            self._installed = True
            self.install_btn.setText("✓ Installé")
            self.install_btn.setStyleSheet("""
                GlassButton {
                    background: rgba(0, 200, 100, 0.2);
                    border: 1px solid rgba(0, 255, 100, 0.4);
                    color: rgba(255, 255, 255, 0.9);
                }
            """)
            self.install_btn.show()
            
            # Celebration effect
            self.icon_glow.setColor(QColor(0, 255, 100, 200))
            self.glow_anim.setStartValue(20)
            self.glow_anim.setEndValue(40)
            self.glow_anim.start()
            QTimer.singleShot(1000, lambda: self.glow_anim.setEndValue(20))
            return
        
        increment = random.randint(1, 10)
        self.progress_bar.setValue(min(100, value + increment))
    
    @pyqtProperty(float)
    def selectionState(self):
        return 1.0
    
    @selectionState.setter
    def selectionState(self, value):
        if self._selected:
            self.setStyleSheet(f"""
                InstallerCard {{
                    background: rgba(60, 70, 90, {0.6 + value*0.2});
                    border: 1px solid rgba(255, 255, 255, {0.15 + value*0.1});
                }}
            """)
        else:
            self.setStyleSheet(f"""
                InstallerCard {{
                    background: rgba(50, 60, 80, {0.6 - value*0.2});
                    border: 1px solid rgba(255, 255, 255, {0.15 - value*0.05});
                }}
            """)
    
    @pyqtProperty(float)
    def hoverState(self):
        return 1.0 if self._hover else 0.0
    
    @hoverState.setter
    def hoverState(self, value):
        self.setStyleSheet(f"""
            InstallerCard {{
                background: rgba(60, 70, 90, {0.6 + value*0.2});
                border: 1px solid rgba(255, 255, 255, {0.15 + value*0.1});
                transform: scale({1 + value*0.02});
            }}
        """)

class ModernInstaller(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # Header
        self.setup_header(main_layout)
        
        # Search bar
        self.setup_search_bar(main_layout)
        
        # Content area
        self.setup_content_area(main_layout)
        
        # Footer
        self.setup_footer(main_layout)
        
        # Apply styles
        self.setStyleSheet("""
            QWidget {
                background: transparent;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.1);
                width: 10px;
                margin: 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.3);
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
                background: none;
            }
        """)
    
    def setup_header(self, layout):
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(15)
        
        # Title with animated gradient
        self.title_label = QLabel("Suite Professionnelle Premium")
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                font-family: 'Segoe UI';
                color: white;
            }
        """)
        
        # Create gradient animation
        self.gradient_anim = QPropertyAnimation(self.title_label, b"gradientPos")
        self.gradient_anim.setDuration(3000)
        self.gradient_anim.setStartValue(0)
        self.gradient_anim.setEndValue(1)
        self.gradient_anim.setEasingCurve(QEasingCurve.InOutSine)
        self.gradient_anim.setLoopCount(-1)
        
        header_layout.addWidget(self.title_label)
        
        # Subtitle with separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("""
            QFrame {
                border: none;
                height: 1px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 transparent, 
                    stop:0.5 rgba(79, 172, 254, 0.5),
                    stop:1 transparent);
                margin: 10px 0;
            }
        """)
        header_layout.addWidget(separator)
        
        subtitle = QLabel("Sélectionnez les applications à installer")
        subtitle.setStyleSheet("""
            color: rgba(255, 255, 255, 0.7);
            font-size: 16px;
            font-family: 'Segoe UI';
        """)
        subtitle.setWordWrap(True)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header)
    
    def setup_search_bar(self, layout):
        search_bar = QWidget()
        search_layout = QHBoxLayout(search_bar)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(15)
        
        # Search input with icon
        search_container = QWidget()
        search_container.setStyleSheet("""
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        """)
        
        search_inner = QHBoxLayout(search_container)
        search_inner.setContentsMargins(15, 5, 15, 5)
        
        search_icon = QLabel()
        search_icon.setPixmap(QPixmap(":/icons/search.svg").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        search_inner.addWidget(search_icon)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher des applications...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                padding: 8px;
                color: white;
                font-family: 'Segoe UI';
                font-size: 14px;
                selection-background-color: rgba(79, 172, 254, 0.5);
            }
        """)
        search_inner.addWidget(self.search_input, 1)
        
        search_layout.addWidget(search_container, 1)
        
        # Filter buttons
        self.filter_group = QButtonGroup()
        filters = ["Tous", "Production", "Finance", "Bureau"]
        
        for i, text in enumerate(filters):
            btn = QRadioButton(text)
            btn.setStyleSheet("""
                QRadioButton {
                    color: white;
                    font-family: 'Segoe UI';
                    padding: 8px 15px;
                }
                QRadioButton::indicator {
                    width: 0;
                    height: 0;
                }
                QRadioButton:checked {
                    background: rgba(79, 172, 254, 0.2);
                    border-radius: 12px;
                }
            """)
            if i == 0:
                btn.setChecked(True)
            self.filter_group.addButton(btn, i)
            search_layout.addWidget(btn)
        
        layout.addWidget(search_bar)
    
    def setup_content_area(self, layout):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        # Fond du contenu défilable
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("""
            QWidget {
                background: rgba(40, 45, 55, 0.8);
                border-radius: 15px;
            }
        """)
        
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(15)
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)
        
        scroll_area.setWidget(self.scroll_content)
        layout.addWidget(scroll_area, 1)
        
    def setup_footer(self, layout):
        footer = QWidget()
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        
        # Select all button
        self.select_all_btn = GlassButton("Tout sélectionner")
        self.select_all_btn.setFixedWidth(180)
        self.select_all_btn.clicked.connect(self.toggle_select_all)
        footer_layout.addWidget(self.select_all_btn)
        
        # Spacer
        footer_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Install button
        self.install_btn = GlassButton("Installer la sélection")
        self.install_btn.setFixedWidth(200)
        self.install_btn.setStyleSheet("""
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
        self.install_btn.clicked.connect(self.install_selected)
        footer_layout.addWidget(self.install_btn)
        
        layout.addWidget(footer)
    
    def add_application(self, app_name, description, icon_path=None, install_callback=None):
        card = InstallerCard(app_name, description, icon_path)
        
        if install_callback:
            card.install_btn.clicked.connect(install_callback)
        
        self.scroll_layout.addWidget(card)
        return card
    
    def toggle_select_all(self):
        cards = self.scroll_content.findChildren(InstallerCard)
        if not cards:
            return
            
        all_selected = all(card.checkbox.isChecked() for card in cards)
        new_state = not all_selected
        
        for card in cards:
            card.checkbox.setChecked(new_state)
        
        self.select_all_btn.setText("Tout désélectionner" if new_state else "Tout sélectionner")
    
    def install_selected(self):
        cards = self.scroll_content.findChildren(InstallerCard)
        selected_cards = [card for card in cards if card.checkbox.isChecked()]
        
        if not selected_cards:
            self.show_notification("Information", "Veuillez sélectionner au moins une application.")
            return
        
        # Show confirmation dialog
        confirm_dialog = QDialog(self)
        confirm_dialog.setWindowTitle("Confirmation")
        confirm_dialog.setWindowModality(Qt.ApplicationModal)
        confirm_dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        confirm_dialog.setAttribute(Qt.WA_TranslucentBackground)
        confirm_dialog.setFixedSize(1100, 800)
        
        # Dialog background
        bg = QWidget(confirm_dialog)
        bg.setGeometry(0, 0, 400, 250)
        bg.setStyleSheet("""
            background: rgba(40, 50, 70, 0.95);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.15);
        """)
        
        shadow = QGraphicsDropShadowEffect(bg)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 10)
        bg.setGraphicsEffect(shadow)
        
        # Dialog content
        layout = QVBoxLayout(confirm_dialog)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        icon = QLabel()
        icon.setPixmap(QPixmap(":/icons/warning.svg").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)
        
        label = QLabel(f"Voulez-vous installer {len(selected_cards)} application(s) sélectionnée(s)?")
        label.setStyleSheet("""
            color: white;
            font-family: 'Segoe UI';
            font-size: 16px;
            text-align: center;
        """)
        label.setWordWrap(True)
        layout.addWidget(label)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        cancel_btn = GlassButton("Annuler")
        cancel_btn.setFixedWidth(120)
        cancel_btn.clicked.connect(confirm_dialog.reject)
        btn_layout.addWidget(cancel_btn)
        
        btn_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        install_btn = GlassButton("Installer")
        install_btn.setFixedWidth(120)
        install_btn.setStyleSheet("""
            GlassButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4facfe, stop:1 #00f2fe);
                border: none;
            }
        """)
        install_btn.clicked.connect(confirm_dialog.accept)
        btn_layout.addWidget(install_btn)
        
        layout.addLayout(btn_layout)
        
        if confirm_dialog.exec_() == QDialog.Accepted:
            for card in selected_cards:
                card.start_installation()
            
            self.show_notification("Installation", "L'installation a commencé!")
    
    def show_notification(self, title, message):
        # Simple notification effect
        notif = QLabel(message, self)
        notif.setStyleSheet("""
            QLabel {
                background: rgba(40, 50, 70, 0.9);
                color: white;
                padding: 15px 25px;
                border-radius: 10px;
                font-family: 'Segoe UI';
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        notif.setWindowFlags(Qt.FramelessWindowHint | Qt.ToolTip)
        notif.setAttribute(Qt.WA_TranslucentBackground)
        notif.adjustSize()
        
        # Position at bottom right
        pos = QPoint(
            self.width() - notif.width() - 20,
            self.height() - notif.height() - 20
        )
        notif.move(pos)
        
        notif.show()
        
        # Fade out animation
        anim = QPropertyAnimation(notif, b"windowOpacity")
        anim.setDuration(1000)
        anim.setStartValue(1)
        anim.setEndValue(0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.finished.connect(notif.deleteLater)
        
        QTimer.singleShot(2000, anim.start)

class ModernInstaller1(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # Set white background
        self.setStyleSheet("""
            QWidget {
                background-color: white;
            }
        """)
        
        # Header
        self.setup_header(main_layout)
        
        # Search bar
        self.setup_search_bar(main_layout)
        
        # Content area
        self.setup_content_area(main_layout)
        
        # Footer
        self.setup_footer(main_layout)
        
        # Apply additional styles
        self.setStyleSheet(self.styleSheet() + """
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: rgba(0, 0, 0, 0.1);
                width: 10px;
                margin: 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 0, 0, 0.3);
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
                background: none;
            }
        """)
    
    def setup_header(self, layout):
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(15)
        
        # Title with animated gradient
        self.title_label = QLabel("Suite Professionnelle Premium")
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                font-family: 'Segoe UI';
                color: #333333;
            }
        """)
        
        # Create gradient animation
        self.gradient_anim = QPropertyAnimation(self.title_label, b"gradientPos")
        self.gradient_anim.setDuration(3000)
        self.gradient_anim.setStartValue(0)
        self.gradient_anim.setEndValue(1)
        self.gradient_anim.setEasingCurve(QEasingCurve.InOutSine)
        self.gradient_anim.setLoopCount(-1)
        
        header_layout.addWidget(self.title_label)
        
        # Subtitle with separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("""
            QFrame {
                border: none;
                height: 1px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 transparent, 
                    stop:0.5 rgba(79, 172, 254, 0.5),
                    stop:1 transparent);
                margin: 10px 0;
            }
        """)
        header_layout.addWidget(separator)
        
        subtitle = QLabel("Sélectionnez les applications à installer")
        subtitle.setStyleSheet("""
            color: #666666;
            font-size: 16px;
            font-family: 'Segoe UI';
        """)
        subtitle.setWordWrap(True)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header)
    
    def setup_search_bar(self, layout):
        search_bar = QWidget()
        search_layout = QHBoxLayout(search_bar)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(15)
        
        # Search input with icon
        search_container = QWidget()
        search_container.setStyleSheet("""
            background: rgba(0, 0, 0, 0.05);
            border-radius: 12px;
            border: 1px solid rgba(0, 0, 0, 0.1);
        """)
        
        search_inner = QHBoxLayout(search_container)
        search_inner.setContentsMargins(15, 5, 15, 5)
        
        search_icon = QLabel()
        search_icon.setPixmap(QPixmap(":/icons/search.svg").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        search_inner.addWidget(search_icon)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher des applications...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                padding: 8px;
                color: #333333;
                font-family: 'Segoe UI';
                font-size: 14px;
                selection-background-color: rgba(79, 172, 254, 0.5);
            }
        """)
        search_inner.addWidget(self.search_input, 1)
        
        search_layout.addWidget(search_container, 1)
        
        # Filter buttons
        self.filter_group = QButtonGroup()
        filters = ["Tous", "Production", "Finance", "Bureau"]
        
        for i, text in enumerate(filters):
            btn = QRadioButton(text)
            btn.setStyleSheet("""
                QRadioButton {
                    color: #333333;
                    font-family: 'Segoe UI';
                    padding: 8px 15px;
                }
                QRadioButton::indicator {
                    width: 0;
                    height: 0;
                }
                QRadioButton:checked {
                    background: rgba(79, 172, 254, 0.2);
                    border-radius: 12px;
                }
            """)
            if i == 0:
                btn.setChecked(True)
            self.filter_group.addButton(btn, i)
            search_layout.addWidget(btn)
        
        layout.addWidget(search_bar)
    
    def setup_content_area(self, layout):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        # Fond du contenu défilable
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("""
            QWidget {
                background: rgba(240, 240, 240, 0.8);
                border-radius: 15px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
        """)
        
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(15)
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)
        
        scroll_area.setWidget(self.scroll_content)
        layout.addWidget(scroll_area, 1)
    
    def setup_footer(self, layout):
        footer = QWidget()
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        
        # Select all button
        self.select_all_btn = GlassButton("Tout sélectionner")
        self.select_all_btn.setFixedWidth(180)
        self.select_all_btn.clicked.connect(self.toggle_select_all)
        footer_layout.addWidget(self.select_all_btn)
        
        # Spacer
        footer_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Install button
        self.install_btn = GlassButton("Installer la sélection")
        self.install_btn.setFixedWidth(200)
        self.install_btn.setStyleSheet("""
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
        self.install_btn.clicked.connect(self.install_selected)
        footer_layout.addWidget(self.install_btn)
        
        layout.addWidget(footer)
    
    # ... (le reste des méthodes reste inchangé)




class InstallerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_applications()
    
    def setup_ui(self):
        self.setWindowTitle("Installer Premium")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(1100, 800)
        
        # Background with particle system
        self.bg = ParticleSystem(self)
        self.bg.setGeometry(0, 0, self.width(), self.height())
        
        # Main container
        self.container = QWidget(self)
        self.container.setGeometry(150, 100, 900, 700)  # Agrandir le conteneur
        self.container.setObjectName("container")
        self.container.setStyleSheet("""
            #container {
                background: rgba(30, 35, 45, 0.80);
                border-radius: 25px;
                border: 1px solid rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(10px);
            }
        """)
        
        # Container shadow
        self.container_shadow = QGraphicsDropShadowEffect(self.container)
        self.container_shadow.setBlurRadius(40)
        self.container_shadow.setColor(QColor(0, 0, 0, 200))
        self.container_shadow.setOffset(0, 15)
        self.container.setGraphicsEffect(self.container_shadow)
        
        # Installer
        self.installer = ModernInstaller(self.container)
        self.installer.setGeometry(0, 0, 800, 600)
        
        # Dans setup_ui()
        self.close_btn = QPushButton("✕", self.container)
        self.close_btn.setGeometry(750, 20, 40, 40)
        self.close_btn.setStyleSheet("""
            QPushButton {
                color: white;
                background: transparent;
                border: none;
                font-size: 20px;
                font-weight: bold;
                border-radius: 20px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
            }
        """)
        self.close_btn.clicked.connect(self.closeWithAnimation)  # Nouvelle méthode

        # Open animation
        self.open_anim = QParallelAnimationGroup(self)
        
        fade_anim = QPropertyAnimation(self, b"windowOpacity")
        fade_anim.setDuration(350)
        fade_anim.setStartValue(0)
        fade_anim.setEndValue(1)
        
        scale_anim = QPropertyAnimation(self.container, b"geometry")
        scale_anim.setDuration(500)
        scale_anim.setStartValue(QRectF(150, 150, 800, 0))
        scale_anim.setEndValue(QRectF(150, 100, 800, 600))
        scale_anim.setEasingCurve(QEasingCurve.OutBack)
        
        self.open_anim.addAnimation(fade_anim)
        self.open_anim.addAnimation(scale_anim)
        self.open_anim.start()



    # Ajouter cette méthode
    def closeWithAnimation(self):
        """Gère la fermeture avec animation"""
        if hasattr(self, 'close_anim') and self.close_anim.state() == QPropertyAnimation.Running:
            return  # Éviter les doubles clics
        
        self.close_anim = QParallelAnimationGroup(self)
        
        fade_anim = QPropertyAnimation(self, b"windowOpacity")
        fade_anim.setDuration(300)
        fade_anim.setStartValue(1)
        fade_anim.setEndValue(0)
        
        scale_anim = QPropertyAnimation(self.container, b"geometry")
        scale_anim.setDuration(400)
        scale_anim.setStartValue(QRectF(150, 100, 800, 600))
        scale_anim.setEndValue(QRectF(150, 150, 800, 0))
        scale_anim.setEasingCurve(QEasingCurve.InBack)
        
        self.close_anim.addAnimation(fade_anim)
        self.close_anim.addAnimation(scale_anim)
        self.close_anim.finished.connect(self.accept)  # Fermer le dialogue
        self.close_anim.start()
    
    def setup_applications(self):
        apps = [
            {
                "name": "Mayan EDMS",
                "desc": "Système de gestion documentaire open-source pour numériser, organiser, rechercher et sécuriser tous vos fichiers professionnels.",
                "icon": ":/icons/mayan.svg",
                "action": lambda: self.install_app("Mayan EDMS")
            },
            {
                "name": "Odoo Community",
                "desc": "ERP modulaire open-source couvrant CRM, ventes, achats, inventaire, comptabilité, RH et plus, idéal pour les PME.",
                "icon": ":/icons/odoo.svg",
                "action": lambda: self.install_app("Odoo Community")
            },
            {
                "name": "ERPNext",
                "desc": "ERP open-source robuste pour gérer compta, fabrication, RH, CRM, projets et stock dans une interface moderne.",
                "icon": ":/icons/erpnext.svg",
                "action": lambda: self.install_app("ERPNext")
            },
            {
                "name": "Crater CRM & Facturation",
                "desc": "Outil gratuit pour gérer factures, devis, paiements, clients et finances, parfait pour les freelances et petites entreprises.",
                "icon": ":/icons/crater.svg",
                "action": lambda: self.install_app("Crater")
            },
            {
                "name": "EspoCRM",
                "desc": "CRM open-source personnalisable pour suivre clients, leads, ventes et interactions, avec une interface claire et rapide.",
                "icon": ":/icons/espocrm.svg",
                "action": lambda: self.install_app("EspoCRM")
            },
            {
                "name": "OnlyOffice Workspace",
                "desc": "Suite collaborative gratuite avec traitement de texte, tableur, gestion de projets et CRM intégré pour équipes.",
                "icon": ":/icons/onlyoffice.svg",
                "action": lambda: self.install_app("OnlyOffice")
            },
            {
                "name": "Snipe-IT",
                "desc": "Gestionnaire d’actifs open-source pour suivre le matériel, logiciels, licences et affectations dans l’entreprise.",
                "icon": ":/icons/snipeit.svg",
                "action": lambda: self.install_app("Snipe-IT")
            },
            {
                "name": "Flectra ERP & CRM",
                "desc": "Alternative open-source à Odoo, Flectra offre ERP et CRM puissants dans une solution unique, légère et modulaire.",
                "icon": ":/icons/flectra.svg",
                "action": lambda: self.install_app("Flectra")
            }
        ]


        for app in apps:
            self.installer.add_application(
                app["name"],
                app["desc"],
                app["icon"],
                app["action"]
            )
    
    # def install_app(self, app_name):
    #     # Simulate installation
    #     self.installer.show_notification(
    #         "Installation réussie",
    #         f"{app_name} a été installé avec succès!"

    def install_app(self, app_name):
        from Installsweb.odoo_installer import OdooInstaller
        from Installsweb.erpnext_installer import ERPNextInstaller
        from Installsweb.flectra_installer import FlectraInstaller
        from Installsweb.tryton_installer import TrytonInstaller
        from Installsweb.axelor_installer import AxelorInstaller
        from Installsweb.dolibarr_installer import DolibarrInstaller
        from Installsweb.mayan import MayanInstaller  # Ajoutez cette ligne

        try:
            if app_name == "Odoo Community":
                OdooInstaller().install()
            elif app_name == "ERPNext":
                ERPNextInstaller().install()
            elif app_name == "Flectra":
                FlectraInstaller().install()
            elif app_name == "Tryton":
                TrytonInstaller().install()
            elif app_name == "Axelor":
                AxelorInstaller().install()
            elif app_name == "Dolibarr":
                DolibarrInstaller().install()
            elif app_name == "Mayan EDMS":  # Ajoutez cette condition
                MayanInstaller().install()
            else:
                raise ValueError("Application inconnue")

            self.installer.show_notification("Succès", f"{app_name} installé avec succès !")
        except Exception as e:
            self.installer.show_notification("Erreur", f"Erreur lors de l'installation de {app_name} : {e}")
    
        
    def closeEvent(self, event):
        # Close animation
        self.close_anim = QParallelAnimationGroup(self)
        
        fade_anim = QPropertyAnimation(self, b"windowOpacity")
        fade_anim.setDuration(300)
        fade_anim.setStartValue(1)
        fade_anim.setEndValue(0)
        
        scale_anim = QPropertyAnimation(self.container, b"geometry")
        scale_anim.setDuration(400)
        scale_anim.setStartValue(QRectF(150, 100, 800, 600))
        scale_anim.setEndValue(QRectF(150, 150, 800, 0))
        scale_anim.setEasingCurve(QEasingCurve.InBack)
        
        self.close_anim.addAnimation(fade_anim)
        self.close_anim.addAnimation(scale_anim)
        
        # Connecter le signal finished à la fermeture réelle
        self.close_anim.finished.connect(self.accept)  # Utiliser accept() pour QDialog
        
        # Démarrer l'animation
        self.close_anim.start()
        
        # Ignorer l'événement de fermeture immédiate
        event.ignore()

class InstallerPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_applications()

    def setup_ui(self):
        # Utiliser un layout principal pour s'adapter à la taille de l'écran
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Définir un fond blanc
        self.setStyleSheet("background-color: white;")

        # Background with particle system
        self.bg = ParticleSystem(self)
        self.bg.setGeometry(0, 0, self.width(), self.height())

        # Main container
        self.container = QWidget(self)
        self.container.setObjectName("container")
        self.container.setStyleSheet("""
            #container {
                background: rgba(30, 35, 45, 0.80);
                border-radius: 25px;
                border: 1px solid rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(10px);
            }
        """)

        # Container shadow
        self.container_shadow = QGraphicsDropShadowEffect(self.container)
        self.container_shadow.setBlurRadius(40)
        self.container_shadow.setColor(QColor(0, 0, 0, 200))
        self.container_shadow.setOffset(0, 15)
        self.container.setGraphicsEffect(self.container_shadow)

        # Installer
        self.installer = ModernInstaller(self.container)
        installer_layout = QVBoxLayout(self.container)
        installer_layout.addWidget(self.installer)

        # Ajouter le conteneur au layout principal
        main_layout.addWidget(self.container)

        # Ajuster la taille du conteneur lors du redimensionnement de la fenêtre
        self.resizeEvent = self.on_resize

    def on_resize(self, event):
        # Ajuster la taille du conteneur en fonction de la taille de la fenêtre
        margins = 50  # Marges autour du conteneur
        self.container.setGeometry(
            margins,
            margins,
            self.width() - 2 * margins,
            self.height() - 2 * margins
        )
        self.installer.setGeometry(0, 0, self.container.width(), self.container.height())

    def setup_applications(self):
        apps = [
            {
                "name": "Mayan EDMS",
                "desc": "Système de gestion documentaire open-source pour numériser, organiser, rechercher et sécuriser tous vos fichiers professionnels.",
                "icon": ":/icons/mayan.svg",
                "action": lambda: self.install_app("Mayan EDMS")
            },
            {
                "name": "Odoo Community",
                "desc": "ERP modulaire open-source couvrant CRM, ventes, achats, inventaire, comptabilité, RH et plus, idéal pour les PME.",
                "icon": ":/icons/odoo.svg",
                "action": lambda: self.install_app("Odoo Community")
            },
            {
                "name": "ERPNext",
                "desc": "ERP open-source robuste pour gérer compta, fabrication, RH, CRM, projets et stock dans une interface moderne.",
                "icon": ":/icons/erpnext.svg",
                "action": lambda: self.install_app("ERPNext")
            },
            {
                "name": "Crater CRM & Facturation",
                "desc": "Outil gratuit pour gérer factures, devis, paiements, clients et finances, parfait pour les freelances et petites entreprises.",
                "icon": ":/icons/crater.svg",
                "action": lambda: self.install_app("Crater")
            },
            {
                "name": "EspoCRM",
                "desc": "CRM open-source personnalisable pour suivre clients, leads, ventes et interactions, avec une interface claire et rapide.",
                "icon": ":/icons/espocrm.svg",
                "action": lambda: self.install_app("EspoCRM")
            },
            {
                "name": "OnlyOffice Workspace",
                "desc": "Suite collaborative gratuite avec traitement de texte, tableur, gestion de projets et CRM intégré pour équipes.",
                "icon": ":/icons/onlyoffice.svg",
                "action": lambda: self.install_app("OnlyOffice")
            },
            {
                "name": "Snipe-IT",
                "desc": "Gestionnaire d’actifs open-source pour suivre le matériel, logiciels, licences et affectations dans l’entreprise.",
                "icon": ":/icons/snipeit.svg",
                "action": lambda: self.install_app("Snipe-IT")
            },
            {
                "name": "Flectra ERP & CRM",
                "desc": "Alternative open-source à Odoo, Flectra offre ERP et CRM puissants dans une solution unique, légère et modulaire.",
                "icon": ":/icons/flectra.svg",
                "action": lambda: self.install_app("Flectra")
            }
        ]

        for app in apps:
            self.installer.add_application(
                app["name"],
                app["desc"],
                app["icon"],
                app["action"]
            )

    def install_app(self, app_name):
        from Installsweb.odoo_installer import OdooInstallerApp
        from Installsweb.erpnext_installer import ERPNextInstaller
        from Installsweb.flectra_installer import FlectraInstaller
        from Installsweb.tryton_installer import TrytonInstaller
        from Installsweb.axelor_installer import AxelorInstaller
        from Installsweb.dolibarr_installer import DolibarrInstaller
        from Installsweb.mayan import MayanInstallerDialog  # Ajoutez cette ligne





        try:
            if app_name == "Odoo Community":
                installer = OdooInstallerApp(self)
                installer.exec_()
            elif app_name == "ERPNext":
                installer = ERPNextInstaller(self)
                installer.exec_()
            elif app_name == "Flectra":
                installer = FlectraInstaller(self)
                installer.exec_()
            elif app_name == "Tryton":
                installer = TrytonInstaller(self)
                installer.exec_()
            elif app_name == "Axelor":
                installer = AxelorInstaller(self)
                installer.exec_()
            elif app_name == "Dolibarr":
                installer = DolibarrInstaller(self)
                installer.exec_()
            elif app_name == "Mayan EDMS":  # Ajoutez cette condition
                installer = MayanInstallerDialog(self)
                installer.exec_()
            else:
                raise ValueError("Application inconnue")

            self.installer.show_notification("Succès", f"{app_name} installé avec succès !")
        except Exception as e:
            self.installer.show_notification("Erreur", f"Erreur lors de l'installation de {app_name} : {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Load fonts
    try:
        QFontDatabase.addApplicationFont(":/fonts/SegoeUI.ttf")
        QFontDatabase.addApplicationFont(":/fonts/SegoeUI-Bold.ttf")
    except:
        pass
    
    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Create and show dialog
    dialog = InstallerDialog()
    dialog.show()
    
    sys.exit(app.exec_())