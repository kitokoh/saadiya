import sys
import random
import math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QFrame, QTabWidget,
                             QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem,
                             QGraphicsOpacityEffect)
from PyQt5.QtGui import (QFont, QPixmap, QIcon, QColor, QLinearGradient,
                         QPainter, QBrush, QPalette, QPainterPath, QPen, QImage,
                         QRadialGradient)
from PyQt5.QtCore import (Qt, QSize, QPropertyAnimation, QEasingCurve,
                          QParallelAnimationGroup, QSequentialAnimationGroup,
                          QPoint, QTimer, QRectF, QPointF, QTime, QRect)

class AdvancedParticleSystem(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.particle_config = {
            'size_range': (3, 10),
            'speed_range': (0.5, 1.5),
            'alpha_range': (0.2, 0.6),
            'z_range': (0.3, 1.7)
        }
        self.particles = []
        self.init_particles(100)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(20)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.depth_map = None
        self.init_depth_map()

    def init_particles(self, count):
        colors = [
            QColor(255, 255, 255, 120),
            QColor(150, 220, 255, 100),
            QColor(255, 150, 220, 100)
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
                'wobble': random.uniform(0.8, 1.2)
            })

    def init_depth_map(self):
        self.depth_map = QImage(self.size(), QImage.Format_ARGB32)
        self.depth_map.fill(Qt.transparent)

        painter = QPainter(self.depth_map)
        painter.setRenderHint(QPainter.Antialiasing)

        for _ in range(8):
            center = QPointF(
                random.uniform(0, self.width()),
                random.uniform(0, self.height())
            )
            radius = random.uniform(150, 400)

            radial_grad = QRadialGradient(center, radius)
            radial_grad.setColorAt(0, QColor(255, 255, 255, 80))
            radial_grad.setColorAt(0.7, QColor(255, 255, 255, 30))
            radial_grad.setColorAt(1, Qt.transparent)

            painter.setBrush(QBrush(radial_grad))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(center, radius, radius)

        painter.end()

    def update_particles(self):
        time = QTime.currentTime().msecsSinceStartOfDay() * 0.001
        width = self.width()
        height = self.height()

        for p in self.particles:
            move_factor = p['speed'] * p['z_value'] * (0.9 + 0.2 * math.sin(time * 3))
            move_x = move_factor * math.cos(p['direction'])
            move_y = move_factor * math.sin(p['direction'])

            new_x = p['pos'].x() + move_x
            new_y = p['pos'].y() + move_y

            if new_x < 0 or new_x > width:
                p['direction'] = math.pi - p['direction'] + random.uniform(-0.3, 0.3)
                new_x = max(0, min(width, new_x))

            if new_y < 0 or new_y > height:
                p['direction'] = -p['direction'] + random.uniform(-0.3, 0.3)
                new_y = max(0, min(height, new_y))

            p['pos'].setX(new_x)
            p['pos'].setY(new_y)

            alpha_var = 0.15 * math.sin(time * 2.5 + p['pos'].x() * 0.008)
            new_alpha = max(0.15, min(0.7, p['original_alpha'] + alpha_var))
            p['color'].setAlphaF(new_alpha)

            p['current_size'] = p['size'] * (0.9 + 0.1 * math.sin(time * 2 + p['pos'].y() * 0.01))

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        paint_rect = event.rect()

        for p in sorted(self.particles, key=lambda x: -x['z_value']):
            pos = p['pos']

            if not (0 <= pos.x() < width and 0 <= pos.y() < height):
                continue

            margin = int(p['size'] * 2)
            expanded_rect = paint_rect.adjusted(-margin, -margin, margin, margin)
            if not expanded_rect.contains(pos.toPoint()):
                continue

            try:
                depth_alpha = QColor(self.depth_map.pixel(pos.toPoint())).alphaF() if self.depth_map else 0.5
            except Exception:
                depth_alpha = 0.5

            final_alpha = p['color'].alphaF() * (0.4 + 0.6 * depth_alpha)
            color = QColor(p['color'])
            color.setAlphaF(final_alpha)

            if p['z_value'] < 0.8:
                painter.setOpacity(0.6)
                size = p['current_size'] * 1.3
            else:
                painter.setOpacity(1.0)
                size = p['current_size']

            radial = QRadialGradient(pos, size)
            radial.setColorAt(0, color.lighter(150))
            radial.setColorAt(0.7, color)
            radial.setColorAt(1, Qt.transparent)

            painter.setBrush(QBrush(radial))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(pos, size, size)

        painter.end()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if not hasattr(self, 'depth_map') or self.depth_map.size() != self.size():
            self.init_depth_map()

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


class PremierepageWidget(QMainWindow):
    def __init__(self, main_app=None):
        super().__init__()
        self.main_app = main_app
        self._color_offset = 0
        self.setWindowTitle("NOVA 360° Business Suite")
        self.setMinimumSize(1200, 800)
        self.setup_ui()

    def setup_ui(self):
        self.setup_animated_background()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        content_overlay = QWidget()
        content_overlay.setStyleSheet("background: rgba(20, 40, 80, 0.3);")
        content_layout = QVBoxLayout(content_overlay)
        content_layout.setContentsMargins(80, 80, 80, 80)
        content_layout.setSpacing(10)

        self.setup_header(content_layout)

        self.setup_button_container(content_layout)
        self.setup_prompt_container(content_layout)
        self.setup_premium_footer(content_layout)

        main_layout.addWidget(content_overlay)

        self.particle_system = AdvancedParticleSystem(central_widget)
        self.particle_system.lower()

        self.init_animations()

    @property
    def color_offset(self):
        return self._color_offset

    @color_offset.setter
    def color_offset(self, offset):
        if self._color_offset != offset:
            self._color_offset = offset
            self.update_background()

    def update_background(self):
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
        super().setPalette(palette)

    def setup_animated_background(self):
        self.bg_animation = QPropertyAnimation(self, b"color_offset")
        self.bg_animation.setDuration(20000)
        self.bg_animation.setStartValue(0)
        self.bg_animation.setEndValue(1)
        self.bg_animation.setLoopCount(-1)

        QTimer.singleShot(500, self.bg_animation.start)

    def setup_header(self, layout):
        header_container = QWidget()
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(1)
        header_layout.setAlignment(Qt.AlignCenter)

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

        self.header_shadow = QGraphicsDropShadowEffect()
        self.header_shadow.setBlurRadius(20)
        self.header_shadow.setColor(QColor(100, 200, 255, 200))
        self.header_shadow.setOffset(0, 0)
        self.header.setGraphicsEffect(self.header_shadow)

        self.glow_anim = QPropertyAnimation(self.header_shadow, b"blurRadius")
        self.glow_anim.setDuration(3000)
        self.glow_anim.setEasingCurve(QEasingCurve.InOutSine)
        self.glow_anim.setStartValue(20)
        self.glow_anim.setEndValue(40)
        self.glow_anim.setLoopCount(-1)
        self.glow_anim.start()

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

    def setup_button_container(self, layout):
        button_container = QFrame()
        button_container.setFixedHeight(300)
        button_container.setStyleSheet("""
            QFrame {
                background: rgba(20, 40, 80, 0.3);
                border-radius: 30px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)

        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(40, 20, 40, 20)
        button_layout.setSpacing(40)

        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.finance_btn = PremiumButton("Finance", "#33FF57", "finance.png")
        self.finance_btn.setFixedSize(320, 170)
        button_layout.addWidget(self.finance_btn)

        self.marketing_btn = PremiumButton("Marketing", "#FF416C", "marketing.png")
        self.marketing_btn.setFixedSize(550, 230)
        button_layout.addWidget(self.marketing_btn)

        self.management_btn = PremiumButton("Management", "#4A569D", "management.png")
        self.management_btn.setFixedSize(320, 170)
        button_layout.addWidget(self.management_btn)

        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addWidget(button_container)

    def setup_prompt_container(self, layout):
        prompt_container = QFrame()
        prompt_container.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
        """)

        scroll_area = QWidget()
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

        container_layout = QVBoxLayout(prompt_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(scroll_area)

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

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

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

        settings_shadow = QGraphicsDropShadowEffect()
        settings_shadow.setBlurRadius(15)
        settings_shadow.setColor(QColor(100, 200, 255, 100))
        settings_shadow.setOffset(0, 0)
        settings_btn.setGraphicsEffect(settings_shadow)

        footer_layout.addWidget(copyright)
        footer_layout.addWidget(spacer)
        footer_layout.addWidget(settings_btn)

    def init_animations(self):
        self.enter_animation = QParallelAnimationGroup()

        title_anim = QPropertyAnimation(self.header, b"pos")
        title_anim.setDuration(1200)
        title_anim.setEasingCurve(QEasingCurve.OutElastic)
        original_pos = self.header.pos()
        title_anim.setStartValue(original_pos + QPoint(0, -200))
        title_anim.setEndValue(original_pos)

        subtitle_anim = QPropertyAnimation(self.subtitle, b"windowOpacity")
        subtitle_anim.setDuration(1500)
        subtitle_anim.setStartValue(0)
        subtitle_anim.setEndValue(1)

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

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'particle_system'):
            self.particle_system.resize(self.size())
            self.particle_system.init_depth_map()
