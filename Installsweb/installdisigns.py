import sys
import random
import math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QScrollArea, QCheckBox, QProgressBar, 
                            QMessageBox, QSizeGrip, QLineEdit, QSizePolicy, QSpacerItem,
                            QGraphicsDropShadowEffect, QFrame, QButtonGroup, QRadioButton,
                            QStackedWidget)
from PyQt5.QtCore import (Qt, QSize, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, 
                         pyqtProperty, QTimer, QRectF, QPoint, QPointF, QSequentialAnimationGroup)
from PyQt5.QtGui import (QFont, QIcon, QColor, QPalette, QLinearGradient, QPainter, 
                        QBrush, QPainterPath, QFontDatabase, QPixmap, QPen, QConicalGradient,
                        QRadialGradient, QImage, QPainterPath)
from PyQt5.QtSvg import QSvgWidget

class ParticleSystem(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.particles = []
        self.init_particles(50)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(20)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
    def init_particles(self, count):
        for _ in range(count):
            self.particles.append({
                'pos': QPointF(random.random() * self.width(), random.random() * self.height()),
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
            p['pos'] += QPointF(
                math.cos(p['direction']) * p['speed'],
                math.sin(p['direction']) * p['speed']
            )
            
            if p['pos'].x() < 0 or p['pos'].x() > self.width():
                p['direction'] = math.pi - p['direction']
            if p['pos'].y() < 0 or p['pos'].y() > self.height():
                p['direction'] = -p['direction']
            
            p['life'] -= 1
            if p['life'] <= 0:
                p['pos'] = QPointF(random.random() * self.width(), random.random() * self.height())
                p['life'] = p['max_life']
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        for p in self.particles:
            alpha = int(255 * (p['life'] / p['max_life']))
            color = QColor(p['color'])
            color.setAlpha(alpha)
            
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            
            glow = QRadialGradient(p['pos'], p['size'] * 2)
            glow.setColorAt(0, color)
            glow.setColorAt(1, QColor(color.red(), color.green(), color.blue(), 0))
            
            painter.setBrush(QBrush(glow))
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
        
        self.install_btn = GlassButton("Installer")
        self.install_btn.setFixedWidth(140)
        self.install_btn.setStyleSheet("""
            GlassButton {
                background: rgba(79, 172, 254, 0.2);
                border: 1px solid rgba(79, 172, 254, 0.4);
            }
        """)
        layout.addWidget(self.install_btn)
        
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

        self.install_btn.setStyleSheet(f"""
            GlassButton {{
                background: rgba({self.primary_color.red()}, {self.primary_color.green()}, {self.primary_color.blue()}, 0.25);
                border: 1px solid rgba({self.primary_color.red()}, {self.primary_color.green()}, {self.primary_color.blue()}, 0.4);
            }}
        """)

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

        self.icon_glow.setColor(QColor(self.primary_color.red(), self.primary_color.green(), self.primary_color.blue(), 150))
    
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

class ModernInstallerPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        self.setup_header(main_layout)
        self.setup_search_bar(main_layout)
        self.setup_content_area(main_layout)
        self.setup_footer(main_layout)
        
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
        
        self.title_label = QLabel("Suite Professionnelle Premium")
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                font-family: 'Segoe UI';
                color: white;
            }
        """)
        
        self.gradient_anim = QPropertyAnimation(self.title_label, b"gradientPos")
        self.gradient_anim.setDuration(3000)
        self.gradient_anim.setStartValue(0)
        self.gradient_anim.setEndValue(1)
        self.gradient_anim.setEasingCurve(QEasingCurve.InOutSine)
        self.gradient_anim.setLoopCount(-1)
        
        header_layout.addWidget(self.title_label)
        
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
        
        self.select_all_btn = GlassButton("Tout sélectionner")
        self.select_all_btn.setFixedWidth(180)
        self.select_all_btn.clicked.connect(self.toggle_select_all)
        footer_layout.addWidget(self.select_all_btn)
        
        footer_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
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
        
        confirm_dialog = QDialog(self)
        confirm_dialog.setWindowTitle("Confirmation")
        confirm_dialog.setWindowModality(Qt.ApplicationModal)
        confirm_dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        confirm_dialog.setAttribute(Qt.WA_TranslucentBackground)
        confirm_dialog.setFixedSize(400, 250)
        
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
        
        pos = QPoint(
            self.width() - notif.width() - 20,
            self.height() - notif.height() - 20
        )
        notif.move(pos)
        
        notif.show()
        
        anim = QPropertyAnimation(notif, b"windowOpacity")
        anim.setDuration(1000)
        anim.setStartValue(1)
        anim.setEndValue(0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.finished.connect(notif.deleteLater)
        
        QTimer.singleShot(2000, anim.start)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application Manager")
        self.setMinimumSize(1200, 800)
        
        # Setup main widget with particle background
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create particle system background
        self.particle_bg = ParticleSystem()
        self.particle_bg.setFixedSize(self.size())
        self.main_layout.addWidget(self.particle_bg)
        
        # Create stacked widget for pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background: transparent;")
        self.main_layout.addWidget(self.stacked_widget)
        
        # Setup navigation bar
        self.setup_navigation()
        
        # Setup installer page
        self.setup_installer_page()
        
        # Setup other pages (placeholder)
        self.setup_other_pages()
        
        # Apply styles
        self.setStyleSheet("""
            QMainWindow {
                background: #1a1e24;
            }
        """)
        
        # Start animations
        self.start_animations()
    
    def setup_navigation(self):
        # Navigation bar at top
        self.nav_bar = QWidget()
        self.nav_bar.setFixedHeight(60)
        self.nav_bar.setStyleSheet("""
            QWidget {
                background: rgba(30, 35, 45, 0.8);
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        nav_layout = QHBoxLayout(self.nav_bar)
        nav_layout.setContentsMargins(20, 0, 20, 0)
        nav_layout.setSpacing(20)
        
        # Logo/Title
        self.logo = QLabel("Suite Professionnelle")
        self.logo.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }
        """)
        nav_layout.addWidget(self.logo)
        
        # Navigation buttons
        self.nav_buttons = []
        nav_items = [
            ("Installer", ":/icons/install.svg"),
            ("Gérer", ":/icons/manage.svg"),
            ("Mises à jour", ":/icons/update.svg"),
            ("Paramètres", ":/icons/settings.svg")
        ]
        
        for text, icon in nav_items:
            btn = GlassButton(text, icon)
            btn.setCheckable(True)
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                GlassButton {
                    background: transparent;
                    border: none;
                    padding: 5px 15px;
                    font-size: 13px;
                    text-transform: none;
                }
                GlassButton:checked {
                    background: rgba(79, 172, 254, 0.2);
                }
            """)
            self.nav_buttons.append(btn)
            nav_layout.addWidget(btn)
        
        # First button checked by default
        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)
        
        # Spacer
        nav_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # User menu
        self.user_btn = GlassButton("Mon compte", ":/icons/user.svg")
        self.user_btn.setFixedHeight(40)
        self.user_btn.setStyleSheet("""
            GlassButton {
                background: transparent;
                border: none;
                padding: 5px 15px;
                font-size: 13px;
                text-transform: none;
            }
        """)
        nav_layout.addWidget(self.user_btn)
        
        self.main_layout.insertWidget(1, self.nav_bar)
    
    def setup_installer_page(self):
        self.installer_page = ModernInstallerPage()
        
        # Add sample applications
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
                "desc": "Gestionnaire d'actifs open-source pour suivre le matériel, logiciels, licences et affectations dans l'entreprise.",
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
            self.installer_page.add_application(
                app["name"],
                app["desc"],
                app["icon"],
                app["action"]
            )
        
        self.stacked_widget.addWidget(self.installer_page)
    
    def setup_other_pages(self):
        # Placeholder pages
        self.manage_page = QWidget()
        self.manage_page.setStyleSheet("background: transparent;")
        manage_layout = QVBoxLayout(self.manage_page)
        manage_layout.addWidget(QLabel("Page de gestion des applications", alignment=Qt.AlignCenter))
        self.stacked_widget.addWidget(self.manage_page)
        
        self.update_page = QWidget()
        self.update_page.setStyleSheet("background: transparent;")
        update_layout = QVBoxLayout(self.update_page)
        update_layout.addWidget(QLabel("Page des mises à jour", alignment=Qt.AlignCenter))
        self.stacked_widget.addWidget(self.update_page)
        
        self.settings_page = QWidget()
        self.settings_page.setStyleSheet("background: transparent;")
        settings_layout = QVBoxLayout(self.settings_page)
        settings_layout.addWidget(QLabel("Page des paramètres", alignment=Qt.AlignCenter))
        self.stacked_widget.addWidget(self.settings_page)
    
    def start_animations(self):
        # Start title gradient animation
        self.installer_page.gradient_anim.start()
        
        # Connect navigation buttons
        for i, btn in enumerate(self.nav_buttons):
            btn.clicked.connect(lambda _, idx=i: self.stacked_widget.setCurrentIndex(idx))
    
    def install_app(self, app_name):
        # Simulate installation
        self.installer_page.show_notification(
            "Installation réussie",
            f"{app_name} a été installé avec succès!"
        )
    
    def resizeEvent(self, event):
        self.particle_bg.setFixedSize(self.size())
        super().resizeEvent(event)

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
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())