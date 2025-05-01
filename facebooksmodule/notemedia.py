import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QTableWidget, QTableWidgetItem, QTextEdit, QHeaderView, 
                            QLabel, QFrame, QPushButton, QGraphicsDropShadowEffect, 
                            QSizeGrip, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import (Qt, QSettings, QPropertyAnimation, QEasingCurve, 
                         QPoint, QTimer, QRectF, QSequentialAnimationGroup, 
                         QParallelAnimationGroup, QCoreApplication)
from PyQt5.QtGui import (QFont, QColor, QPainter, QLinearGradient, QBrush, 
                        QPainterPath, QPalette, QRegion, QIcon)


class PremiumModal(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._init_translations()
        self.setup_ui()
        self.load_settings()
        
        # Configuration premium du modal
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        # Effets visuels premium
        self.setup_visual_effects()
        
        # Animation et persistance
        self.setup_animations()
        self.setup_persistence()
        
        # Applique le style initial
        self.set_styles()
        
        # Masque pour les coins arrondis
        self.setMask(QRegion(self.rect(), QRegion.Rectangle))
        self.update_mask()

    def _init_translations(self):
        """Initialise les textes traduisibles"""
        self.tr_close = QCoreApplication.translate("PremiumModal", "Fermer")
        self.tr_media = QCoreApplication.translate("PremiumModal", "Média")
        self.tr_description = QCoreApplication.translate("PremiumModal", "Description")
        self.tr_title = QCoreApplication.translate("PremiumModal", "ÉDITEUR CRÉATIF PREMIUM")
        self.tr_prompt = QCoreApplication.translate("PremiumModal", "PROMPT INSPIRANT")
        self.tr_placeholder = QCoreApplication.translate("PremiumModal", "Exprimez votre créativité ici...")
        self.tr_media_item = QCoreApplication.translate("PremiumModal", "Média {}")
        self.tr_desc_placeholder = QCoreApplication.translate("PremiumModal", "Cliquez pour éditer la description {}")

    def update_mask(self):
        """Met à jour le masque pour les coins arrondis lors du redimensionnement"""
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 15, 15)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def set_styles(self):
        """Applique les styles CSS personnalisés"""
        self.setStyleSheet("""
            PremiumModal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f8f8);
                border-radius: 15px;
                border: 1px solid rgba(0, 0, 0, 0.08);
            }
            QTableWidget {
                border: none;
                background: transparent;
                alternate-background-color: rgba(240, 240, 240, 0.5);
                selection-background-color: #e0f7fa;
                selection-color: #007bff;
            }
            QHeaderView::section {
                background-color: rgba(240, 240, 240, 0.8);
                padding: 12px 8px;
                border: none;
                font-weight: 600;
                color: #555;
                border-bottom: 1px solid #e0e0e0;
            }
            QTextEdit {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 12px;
                background: white;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 1px solid #4da6ff;
            }
            QLabel {
                font-weight: 600;
                color: #555;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            #headerLabel {
                font-size: 18px;
                font-weight: 700;
                color: #2d3748;
                background: transparent;
                border-bottom: 1px solid rgba(0, 0, 0, 0.05);
                padding-bottom: 10px;
            }
            #closeButton {
                background: transparent;
                border: none;
                padding: 5px;
                qproperty-icon: url(:/icons/close.svg);
                qproperty-iconSize: 16px;
            }
            #closeButton:hover {
                background: rgba(0, 0, 0, 0.05);
                border-radius: 4px;
            }
            #footerButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f56565, stop:1 #e53e3e);
                color: white;
                font-weight: 600;
                font-size: 14px;
                border-radius: 8px;
                padding: 8px 16px;
                min-width: 100px;
            }
            #footerButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e53e3e, stop:1 #c53030);
            }
        """)

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.main_layout.setSpacing(20)

        # En-tête avec bouton de fermeture
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.header = QLabel(self.tr_title)
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFixedHeight(40)
        
        # Bouton de fermeture en haut à droite
        self.close_button = QPushButton()
        self.close_button.setObjectName("closeButton")
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.close)
        
        header_layout.addWidget(self.header)
        header_layout.addWidget(self.close_button, 0, Qt.AlignRight)
        
        # Tableau des médias
        self.table = QTableWidget(10, 2)
        self.table.setHorizontalHeaderLabels([self.tr_media, self.tr_description])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.CurrentChanged | QTableWidget.DoubleClicked | 
                                 QTableWidget.EditKeyPressed | QTableWidget.AnyKeyPressed)
        
        # Configuration typographique
        font = QFont()
        font.setFamily("Segoe UI Variable" if sys.platform == "win32" else "SF Pro Display")
        font.setWeight(QFont.Medium)
        font.setPixelSize(14)
        self.table.setFont(font)
        
        # Remplissage avec style
        for i in range(10):
            media_item = QTableWidgetItem(self.tr_media_item.format(i+1))
            media_item.setFlags(media_item.flags() & ~Qt.ItemIsEditable)
            media_item.setForeground(QColor("#2d3748"))
            self.table.setItem(i, 0, media_item)
            
            desc_item = QTableWidgetItem(self.tr_desc_placeholder.format(i+1))
            desc_item.setForeground(QColor("#4a5568"))
            self.table.setItem(i, 1, desc_item)
        
        # Zone de prompt
        self.setup_prompt_section()
        
        # Bouton de fermeture en bas
        self.footer_button = QPushButton(self.tr_close)
        self.footer_button.setObjectName("footerButton")
        self.footer_button.setCursor(Qt.PointingHandCursor)
        self.footer_button.clicked.connect(self.close)
        
        # Ajout des éléments au layout
        self.main_layout.addLayout(header_layout)
        self.main_layout.addWidget(self.table, 1)
        self.main_layout.addWidget(self.prompt_frame)
        
        # Espacement et bouton footer
        self.main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.main_layout.addWidget(self.footer_button, 0, Qt.AlignCenter)
        
        self.setLayout(self.main_layout)
        self.resize(700, 600)
        
        # Poignée de redimensionnement
        self.size_grip = QSizeGrip(self)
        self.size_grip.setFixedSize(20, 20)

    def setup_prompt_section(self):
        self.prompt_frame = QFrame()
        self.prompt_frame.setFrameShape(QFrame.NoFrame)
        prompt_layout = QVBoxLayout()
        self.prompt_frame.setLayout(prompt_layout)
        
        self.prompt_label = QLabel(self.tr_prompt)
        self.prompt_label.setAlignment(Qt.AlignCenter)
        
        self.prompt_edit = QTextEdit()
        self.prompt_edit.setPlaceholderText(self.tr_placeholder)
        self.prompt_edit.setMinimumHeight(120)
        
        prompt_layout.addWidget(self.prompt_label)
        prompt_layout.addWidget(self.prompt_edit)
        prompt_layout.setSpacing(10)
        prompt_layout.setContentsMargins(0, 0, 0, 0)

    def setup_visual_effects(self):
        # Ombre portée dynamique
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.shadow.setOffset(0, 10)
        self.setGraphicsEffect(self.shadow)
        
        # Effet de bordure personnalisé
        self.border_color = QColor("#4da6ff")

    def setup_animations(self):
        # Groupe d'animations pour l'ouverture/fermeture
        self.animation_group = QParallelAnimationGroup()
        
        # Animation de géométrie
        self.geom_animation = QPropertyAnimation(self, b"geometry")
        self.geom_animation.setDuration(400)
        self.geom_animation.setEasingCurve(QEasingCurve.OutQuint)
        
        # Animation d'opacité
        self.opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_animation.setDuration(300)
        
        self.animation_group.addAnimation(self.geom_animation)
        self.animation_group.addAnimation(self.opacity_animation)

    def setup_persistence(self):
        # Timer pour sauvegarde automatique
        self.save_timer = QTimer()
        self.save_timer.setInterval(500)  # 500ms
        self.save_timer.timeout.connect(self.save_settings)
        self.save_timer.start()
        
        # Connexions pour sauvegarde immédiate
        self.table.cellChanged.connect(self.trigger_save)
        self.prompt_edit.textChanged.connect(self.trigger_save)

    def trigger_save(self):
        # Déclenche une sauvegarde immédiate
        self.save_settings()

    def showEvent(self, event):
        if self.parent and hasattr(self.parent, 'trigger_button'):
            btn = self.parent.trigger_button
            global_pos = btn.mapToGlobal(QPoint(0, 0))
            
            # Animation d'ouverture "Origami"
            start_rect = QRectF(global_pos.x(), global_pos.y(), 
                               btn.width(), btn.height()).toRect()
            end_rect = QRectF(global_pos.x() - (self.width() - btn.width()) // 2,
                             global_pos.y() + btn.height() + 10,
                             self.width(), self.height()).toRect()
            
            self.setGeometry(start_rect)
            
            self.geom_animation.setStartValue(start_rect)
            self.geom_animation.setEndValue(end_rect)
            
            self.opacity_animation.setStartValue(0)
            self.opacity_animation.setEndValue(1)
            
            self.animation_group.start()
        
        super().showEvent(event)

    def closeEvent(self, event):
        # Animation de fermeture inversée
        if self.parent and hasattr(self.parent, 'trigger_button'):
            btn = self.parent.trigger_button
            global_pos = btn.mapToGlobal(QPoint(0, 0))
            
            self.geom_animation.setDirection(QPropertyAnimation.Backward)
            self.opacity_animation.setDirection(QPropertyAnimation.Backward)
            
            self.animation_group.finished.connect(self.deleteLater)
            self.animation_group.start()
            event.ignore()
        else:
            event.accept()

    def save_settings(self):
        settings = QSettings("PremiumModal", "CreativeSuitePro")
        settings.beginGroup("MediaData")
        
        for i in range(self.table.rowCount()):
            description = self.table.item(i, 1).text()
            settings.setValue(f"media_{i}_desc", description)
        
        settings.endGroup()
        
        settings.beginGroup("PromptData")
        settings.setValue("content", self.prompt_edit.toPlainText())
        settings.setValue("last_modified", self.parent.get_current_time())
        settings.endGroup()

    def load_settings(self):
        settings = QSettings("PremiumModal", "CreativeSuitePro")
        settings.beginGroup("MediaData")
        
        for i in range(self.table.rowCount()):
            description = settings.value(f"media_{i}_desc", "")
            if description:
                self.table.item(i, 1).setText(description)
        
        settings.endGroup()
        
        settings.beginGroup("PromptData")
        prompt = settings.value("content", "")
        if prompt:
            self.prompt_edit.setPlainText(prompt)
        settings.endGroup()

    def paintEvent(self, event):
        # Dessin personnalisé pour un look ultra premium
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        
        # Fond avec dégradé complexe
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 15, 15)
        
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(250, 250, 252))
        gradient.setColorAt(1, QColor(240, 242, 245))
        
        painter.fillPath(path, QBrush(gradient))
        
        # Bordure élégante
        painter.setPen(QColor("#e2e8f0"))
        painter.drawPath(path)
        
        # Overlay de luminosité
        highlight = QLinearGradient(0, 0, 0, 50)
        highlight.setColorAt(0, QColor(255, 255, 255, 80))
        highlight.setColorAt(1, QColor(255, 255, 255, 0))
        painter.fillRect(0, 0, self.width(), 50, highlight)
        
        # Positionnement de la poignée
        self.size_grip.move(self.width() - 25, self.height() - 25)

    def resizeEvent(self, event):
        self.update_mask()
        super().resizeEvent(event)


class PremiumMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._init_translations()
        self.setup_window()
        self.setup_ui()
        self.setup_styles()
        
        # Référence au modal
        self.modal = None

    def _init_translations(self):
        """Initialise les textes traduisibles"""
        self.tr_open = QCoreApplication.translate("PremiumMainWindow", "OUVRIR L'ÉDITEUR")
        self.tr_close = QCoreApplication.translate("PremiumMainWindow", "FERMER L'ÉDITEUR")
        self.tr_title = QCoreApplication.translate("PremiumMainWindow", "Suite Créative Premium")

    def setup_window(self):
        self.setWindowTitle(self.tr_title)
        self.setGeometry(100, 100, 900, 700)
        
        # Fond animé
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#f7fafc"))
        gradient.setColorAt(1, QColor("#edf2f7"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Bouton premium
        self.setup_trigger_button()
        
        layout.addStretch(1)
        layout.addWidget(self.trigger_button, 0, Qt.AlignCenter)
        layout.addStretch(1)

    def setup_trigger_button(self):
        self.trigger_button = QPushButton(self.tr_open)
        self.trigger_button.setFixedSize(240, 60)
        self.trigger_button.setCursor(Qt.PointingHandCursor)
        
        # Effet 3D au survol
        self.btn_shadow = QGraphicsDropShadowEffect()
        self.btn_shadow.setBlurRadius(20)
        self.btn_shadow.setColor(QColor(0, 123, 255, 150))
        self.btn_shadow.setOffset(0, 5)
        self.trigger_button.setGraphicsEffect(self.btn_shadow)
        
        self.trigger_button.clicked.connect(self.toggle_modal)

    def update_button_state(self, modal_visible):
        if modal_visible:
            self.trigger_button.setText(self.tr_close)
            self.trigger_button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #e53e3e, stop:1 #c53030);
                    color: white;
                    font-weight: 600;
                    font-size: 15px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #f56565, stop:1 #e53e3e);
                }
            """)
        else:
            self.trigger_button.setText(self.tr_open)
            self.trigger_button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #4299e1, stop:1 #3182ce);
                    color: white;
                    font-weight: 600;
                    font-size: 15px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #63b3ed, stop:1 #4299e1);
                }
            """)

    def toggle_modal(self):
        if self.modal and self.modal.isVisible():
            self.modal.close()
            self.modal = None
            self.update_button_state(False)
        else:
            self.modal = PremiumModal(self)
            self.modal.show()
            self.update_button_state(True)

    def get_current_time(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def setup_styles(self):
        # Style global premium
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f7fafc, stop:1 #edf2f7);
            }
            QLabel {
                font-weight: 600;
                color: #2d3748;
            }
        """)


    def toggle_modal(self):
        # Vérifie si le modal existe ET n'a pas été supprimé
        if hasattr(self, 'modal') and self.modal is not None:
            try:
                if self.modal.isVisible():
                    self.modal.close()
                    self.modal = None  # Important: réinitialiser la référence
                    self.update_button_state(False)
                    return
            except RuntimeError:
                # L'objet a été supprimé mais la référence existe encore
                self.modal = None
                self.update_button_state(False)
                return
        
        # Créer un nouveau modal si nécessaire
        self.modal = PremiumModal(self)
        self.modal.destroyed.connect(self.on_modal_destroyed)  # Nouvelle connexion
        self.modal.show()
        self.update_button_state(True)

    def on_modal_destroyed(self):
        """Callback quand le modal est détruit"""
        self.modal = None
        self.update_button_state(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Configuration typographique ultra premium
    font = QFont()
    font.setFamily("Segoe UI Variable" if sys.platform == "win32" else "SF Pro Display")
    font.setWeight(QFont.Medium)
    font.setPixelSize(13)
    font.setStyleStrategy(QFont.PreferAntialias)
    app.setFont(font)
    
    # Style des tooltips premium
    app.setStyleSheet("""
        QToolTip {
            background-color: #2d3748;
            color: #f7fafc;
            border: 1px solid #4a5568;
            border-radius: 6px;
            padding: 5px 10px;
            font-size: 13px;
            opacity: 240;
        }
    """)
    
    window = PremiumMainWindow()
    window.show()
    sys.exit(app.exec_())