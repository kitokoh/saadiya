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
            dx = math.cos(p['direction']) * p['speed']
            dy = math.sin(p['direction']) * p['speed']
            p['pos'] += QPointF(dx, dy)

            if not (0 <= p['pos'].x() <= self.width()):
                p['direction'] = math.pi - p['direction']
            if not (0 <= p['pos'].y() <= self.height()):
                p['direction'] = -p['direction']

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

            glow = QRadialGradient(p['pos'], p['size'] * 2)
            glow.setColorAt(0, color)
            glow.setColorAt(1, QColor(color.red(), color.green(), color.blue(), 0))
            painter.setBrush(QBrush(glow))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(p['pos'], p['size'] * 2, p['size'] * 2)

            painter.setBrush(QBrush(color))
            painter.drawEllipse(p['pos'], p['size'], p['size'])

class GlassButton(QPushButton):
    def __init__(self, text, icon=None, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(50)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self._glass_opacity = 0.3
        self._glass_blur = 5
        self._light_position = 0
        self._light_color = QColor(255, 255, 255, 150)
        self._pulse_scale = 1.0
        self._ripple_alpha = 0
        self._ripple_radius = 0
        self._ripple_center = QPointF()

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.shadow.setOffset(0, 8)
        self.setGraphicsEffect(self.shadow)

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

        self.setup_animations()

    def setup_animations(self):
        self.opacity_anim = QPropertyAnimation(self, b"glassOpacity")
        self.opacity_anim.setDuration(400)
        self.opacity_anim.setEasingCurve(QEasingCurve.OutQuad)

        self.light_anim = QPropertyAnimation(self, b"lightPosition")
        self.light_anim.setDuration(1800)
        self.light_anim.setStartValue(0)
        self.light_anim.setEndValue(1)
        self.light_anim.setEasingCurve(QEasingCurve.InOutSine)
        self.light_anim.setLoopCount(-1)

        self.pulse_anim = QPropertyAnimation(self, b"pulseScale")
        self.pulse_anim.setDuration(300)
        self.pulse_anim.setKeyValueAt(0, 1.0)
        self.pulse_anim.setKeyValueAt(0.5, 0.97)
        self.pulse_anim.setKeyValueAt(1, 1.0)
        self.pulse_anim.setEasingCurve(QEasingCurve.OutBack)

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

        if self._pulse_scale != 1.0:
            painter.translate(self.width()/2, self.height()/2)
            painter.scale(self._pulse_scale, self._pulse_scale)
            painter.translate(-self.width()/2, -self.height()/2)

        rect = QRectF(self.rect()).adjusted(1, 1, -1, -1)
        path = QPainterPath()
        path.addRoundedRect(rect, 15, 15)

        bg_color = QColor(60, 70, 90, int(200 * self._glass_opacity))
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)

        if self.underMouse():
            gradient = QLinearGradient(0, 0, self.width(), 0)
            gradient.setColorAt(max(0, self._light_position - 0.3), QColor(255, 255, 255, 0))
            gradient.setColorAt(self._light_position, self._light_color)
            gradient.setColorAt(min(1, self._light_position + 0.3), QColor(255, 255, 255, 0))

            painter.setBrush(QBrush(gradient))
            painter.drawPath(path)

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

        painter.setBrush(Qt.NoBrush)
        border_pen = QPen(QColor(255, 255, 255, 80))
        border_pen.setWidth(1)
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

class InstallerCard(QWidget):
    def __init__(self, app_name, description, icon_path=None, parent=None):
        super().__init__(parent)
        self._selected = True
        self._installed = False
        self._hover = False

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(25)
        self.shadow.setColor(QColor(0, 0, 0, 100))
        self.shadow.setOffset(0, 8)
        self.setGraphicsEffect(self.shadow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(30)

        self.checkbox = QCheckBox()
        self.checkbox.setChecked(True)
        layout.addWidget(self.checkbox)

        self.icon_container = QWidget()
        self.icon_container.setFixedSize(64, 64)
        icon_layout = QVBoxLayout(self.icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)

        if icon_path:
            if icon_path.endswith('.svg'):
                self.icon = QSvgWidget(icon_path)
                self.icon.setFixedSize(48, 48)
                svg_container = QWidget()
                svg_layout = QVBoxLayout(svg_container)
                svg_layout.setContentsMargins(0, 0, 0, 0)
                svg_layout.addWidget(self.icon, 0, Qt.AlignCenter)
                self.icon = svg_container
            else:
                self.icon = QLabel()
                self.icon.setPixmap(QPixmap(icon_path).scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.icon.setAlignment(Qt.AlignCenter)
        else:
            self.icon = QLabel()
            self.icon.setPixmap(QPixmap(":/icons/default_app.svg").scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.icon.setAlignment(Qt.AlignCenter)

        self.icon.setFixedSize(48, 48)
        icon_layout.addWidget(self.icon, 0, Qt.AlignCenter)

        self.icon_glow = QGraphicsDropShadowEffect(self.icon_container)
        self.icon_glow.setBlurRadius(20)
        self.icon_glow.setColor(QColor(79, 172, 254, 150))
        self.icon_glow.setOffset(0, 0)
        self.icon_container.setGraphicsEffect(self.icon_glow)

        layout.addWidget(self.icon_container)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(10)
        text_layout.setContentsMargins(0, 0, 0, 0)

        self.name_label = QLabel(app_name)
        text_layout.addWidget(self.name_label)

        self.desc_label = QLabel(description)
        self.desc_label.setWordWrap(True)
        text_layout.addWidget(self.desc_label)

        self.tags_layout = QHBoxLayout()
        self.tags_layout.setSpacing(8)

        for tag in ["Premium", "AI", "Cloud"]:
            tag_label = QLabel(tag)
            self.tags_layout.addWidget(tag_label)

        self.tags_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        text_layout.addLayout(self.tags_layout)

        layout.addLayout(text_layout, 1)

        self.install_btn = GlassButton("Installer")
        self.install_btn.setFixedWidth(140)
        layout.addWidget(self.install_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(140)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        self.setup_styles()
        self.setup_animations()

        self.checkbox.stateChanged.connect(self.on_selection_changed)

    def setup_styles(self):
        self.primary_color = QColor(94, 129, 172)
        self.secondary_color = QColor(143, 110, 164)
        self.accent_color = QColor(72, 189, 170)
        self.highlight_color = QColor(255, 255, 255)
        self.text_color = QColor(230, 230, 230)
        self.background_color = QColor(50, 55, 65)

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

    def setup_animations(self):
        self.selection_anim = QPropertyAnimation(self, b"selectionState")
        self.selection_anim.setDuration(400)
        self.selection_anim.setEasingCurve(QEasingCurve.OutCubic)

        self.hover_anim = QPropertyAnimation(self, b"hoverState")
        self.hover_anim.setDuration(300)
        self.hover_anim.setEasingCurve(QEasingCurve.OutCubic)

        self.glow_anim = QPropertyAnimation(self.icon_glow, b"blurRadius")
        self.glow_anim.setDuration(500)
        self.glow_anim.setEasingCurve(QEasingCurve.OutBack)

    def enterEvent(self, event):
        self._hover = True
        self.hover_anim.start()
        self.glow_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.hover_anim.start()
        self.glow_anim.start()
        super().leaveEvent(event)

    def on_selection_changed(self, state):
        self._selected = state == Qt.Checked
        self.selection_anim.start()

    def start_installation(self):
        pass

    @pyqtProperty(float)
    def selectionState(self):
        return 1.0

    @selectionState.setter
    def selectionState(self, value):
        pass

    @pyqtProperty(float)
    def hoverState(self):
        return 1.0 if self._hover else 0.0

    @hoverState.setter
    def hoverState(self, value):
        pass

class ModernInstaller(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        self.setup_header(main_layout)
        self.setup_search_bar(main_layout)
        self.setup_content_area(main_layout)
        self.setup_footer(main_layout)

    def setup_header(self, layout):
        header = QWidget()
        header_layout = QVBoxLayout(header)
        self.title_label = QLabel("Suite Professionnelle Premium")
        header_layout.addWidget(self.title_label)
        layout.addWidget(header)

    def setup_search_bar(self, layout):
        search_bar = QWidget()
        search_layout = QHBoxLayout(search_bar)
        self.search_input = QLineEdit()
        search_layout.addWidget(self.search_input)
        layout.addWidget(search_bar)

    def setup_content_area(self, layout):
        scroll_area = QScrollArea()
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        scroll_area.setWidget(self.scroll_content)
        layout.addWidget(scroll_area, 1)

    def setup_footer(self, layout):
        footer = QWidget()
        footer_layout = QHBoxLayout(footer)
        self.select_all_btn = GlassButton("Tout sélectionner")
        footer_layout.addWidget(self.select_all_btn)
        self.install_btn = GlassButton("Installer la sélection")
        footer_layout.addWidget(self.install_btn)
        layout.addWidget(footer)

    def add_application(self, app_name, description, icon_path=None, install_callback=None):
        card = InstallerCard(app_name, description, icon_path)
        if install_callback:
            card.install_btn.clicked.connect(install_callback)
        self.scroll_layout.addWidget(card)
        return card

class PremiumInstallerWidget(QDialog):
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

        self.bg = ParticleSystem(self)
        self.bg.setGeometry(0, 0, self.width(), self.height())

        self.container = QWidget(self)
        self.container.setGeometry(150, 100, 900, 700)
        self.container.setObjectName("container")

        self.installer = ModernInstaller(self.container)
        self.installer.setGeometry(0, 0, 800, 600)

        self.close_btn = QPushButton("✕", self.container)
        self.close_btn.setGeometry(750, 20, 40, 40)
        self.close_btn.clicked.connect(self.close)

    def setup_applications(self):
        apps = [
            {"name": "Mayan EDMS", "desc": "Système de gestion documentaire open-source.", "action": lambda: self.install_app("Mayan EDMS")},
            {"name": "Odoo Community", "desc": "ERP modulaire open-source.", "action": lambda: self.install_app("Odoo Community")}
        ]
        for app in apps:
            self.installer.add_application(app["name"], app["desc"], None, app["action"])

    def install_app(self, app_name):
        QMessageBox.information(self, "Installation", f"Installation de {app_name}...")
