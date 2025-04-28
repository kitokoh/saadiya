import os
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QMessageBox, QTableWidgetItem, QCheckBox, QDialog, QCalendarWidget, 
    QDateEdit, QGraphicsDropShadowEffect, QFileDialog, QStyledItemDelegate
)
from PyQt5.QtGui import QColor, QFont, QPainter, QPen, QLinearGradient
from PyQt5.QtCore import Qt, QRectF
import locale
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
class RoundButtonDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if index.column() == 6:  # Column with action buttons
            # Désactiver l'apparence de sélection
            option.state &= ~QtWidgets.QStyle.State_Selected
            
            button_rect = QRectF(
                option.rect.x() + (option.rect.width() - 100) / 2,
                option.rect.y() + (option.rect.height() - 30) / 2,
                100, 30
            )
            
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Dessiner le bouton rond
            gradient = QLinearGradient(button_rect.topLeft(), button_rect.bottomLeft())
            gradient.setColorAt(0, QColor(76, 175, 80))
            gradient.setColorAt(1, QColor(56, 142, 60))
            painter.setBrush(gradient)
            painter.setPen(QPen(QColor(46, 125, 50), 1))
            painter.drawRoundedRect(button_rect, 15, 15)
            
            # Texte du bouton
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(button_rect, Qt.AlignCenter, "⚙️ Action")
            painter.restore()
        else:
            QStyledItemDelegate.paint(self, painter, option, index)


class AddActivityDialog(QtWidgets.QDialog):
    def __init__(self, exe_files):
        super().__init__()
        self.setWindowTitle(self.tr("📅 Schedule an Activity"))
        self.setFixedSize(600, 650)
        self.setWindowIcon(QtGui.QIcon("resources/icons/schedule.ico"))
        
        # Style moderne avec dégradés et ombres
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f5f7fa, stop:1 #c3cfe2);
                border-radius: 15px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
                color: #2c3e50;
                font-weight: 500;
            }
            QLineEdit, QComboBox, QTimeEdit, QDateEdit {
                background-color: white;
                border: 2px solid #dfe6e9;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                min-height: 35px;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QLineEdit:focus, QComboBox:focus, QTimeEdit:focus, QDateEdit:focus {
                border: 2px solid #3498db;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left-width: 1px;
                border-left-color: #dfe6e9;
                border-left-style: solid;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #dfe6e9;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QCheckBox {
                font-size: 14px;
                color: #34495e;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                background-color: #3498db;
                border: 2px solid #2980b9;
                image: url(resources/icons/checkmark.png);
            }
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #2980b9;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: rgba(255, 255, 255, 0.7);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2c3e50);
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px 20px;
                min-width: 120px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2980b9, stop:1 #1a252f);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a5276, stop:1 #17202a);
            }
            QCalendarWidget {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
            }
            QCalendarWidget QToolButton {
                height: 30px;
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                background-color: #dfe6e9;
                border-radius: 5px;
            }
            QCalendarWidget QMenu {
                background-color: white;
                border: 1px solid #bdc3c7;
            }
            QCalendarWidget QSpinBox {
                width: 80px;
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
            }
            QCalendarWidget QWidget { 
                alternate-background-color: #e8f4fc;
            }
        """)

        # Widgets avec icônes et placeholder text
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText(self.tr("📝 Enter activity name"))
        self.name_input.setReadOnly(True)

        self.program_input = QtWidgets.QComboBox()
        self.program_input.addItems(exe_files)
        self.program_input.setCurrentIndex(-1)
        self.program_input.setPlaceholderText(self.tr("📂 Select a program"))
        self.program_input.currentIndexChanged.connect(self.update_name)

        # Style pour les jours de la semaine
        self.daily_checkbox = QtWidgets.QCheckBox(self.tr("🔄 Execute Daily"))
        self.daily_checkbox.setStyleSheet("""
            QCheckBox {
                color: #2c3e50;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        """)

        self.days_group = QtWidgets.QGroupBox(self.tr("📅 Select Specific Days"))
        self.days_layout = QtWidgets.QHBoxLayout()
        self.day_checkboxes = []
        
        day_colors = [
            ("#e74c3c", "#c0392b"),  # Monday - Red
            ("#e67e22", "#d35400"),  # Tuesday - Orange
            ("#f1c40f", "#f39c12"),  # Wednesday - Yellow
            ("#2ecc71", "#27ae60"),  # Thursday - Green
            ("#3498db", "#2980b9"),  # Friday - Blue
            ("#9b59b6", "#8e44ad"),  # Saturday - Purple
            ("#1abc9c", "#16a085")   # Sunday - Teal
        ]
        
        for i, day in enumerate([self.tr("Mon"), self.tr("Tue"), self.tr("Wed"), 
                                self.tr("Thu"), self.tr("Fri"), self.tr("Sat"), self.tr("Sun")]):
            checkbox = QtWidgets.QCheckBox(day)
            checkbox.setStyleSheet(f"""
                QCheckBox {{
                    color: {day_colors[i][1]};
                    font-weight: bold;
                }}
                QCheckBox::indicator {{
                    width: 20px;
                    height: 20px;
                    border: 2px solid {day_colors[i][0]};
                    border-radius: 4px;
                }}
                QCheckBox::indicator:checked {{
                    background-color: {day_colors[i][0]};
                    border: 2px solid {day_colors[i][1]};
                }}
            """)
            self.day_checkboxes.append(checkbox)
            self.days_layout.addWidget(checkbox)
        self.days_group.setLayout(self.days_layout)

        self.time_input = QtWidgets.QTimeEdit()
        self.time_input.setDisplayFormat("HH:mm")
        self.time_input.setTime(QtCore.QTime.currentTime())
        self.time_input.setStyleSheet("""
            QTimeEdit {
                font-size: 16px;
                font-weight: bold;
            }
            QTimeEdit::up-button, QTimeEdit::down-button {
                width: 25px;
                subcontrol-origin: border;
            }
        """)

        # Calendar widget with custom style
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumDate(QtCore.QDate.currentDate())
        self.selected_dates = set()

        # Highlight current date
        format = QtGui.QTextCharFormat()
        format.setBackground(QtGui.QColor("#3498db20"))
        format.setForeground(QtGui.QColor("#2c3e50"))
        self.calendar.setDateTextFormat(QtCore.QDate.currentDate(), format)

        self.calendar.clicked.connect(self.toggle_date_selection)

        self.specific_dates_checkbox = QtWidgets.QCheckBox(self.tr("📅 Schedule on specific dates"))
        self.specific_dates_checkbox.setStyleSheet("""
            QCheckBox {
                color: #2c3e50;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        """)
        self.specific_dates_checkbox.stateChanged.connect(self.toggle_specific_dates)

        # Save button with shadow effect
        self.save_button = QtWidgets.QPushButton(self.tr("💾 Save Schedule"))
        self.save_button.setCursor(Qt.PointingHandCursor)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(3, 3)
        self.save_button.setGraphicsEffect(shadow)

        self.save_button.clicked.connect(self.validate_and_accept)

        # Layout with spacing and margins
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(25, 25, 25, 25)

        # Form layout with proper spacing
        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add form rows with icons
        form_layout.addRow(self.create_form_row("📂 Program:", self.program_input))
        form_layout.addRow(self.create_form_row("📝 Name:", self.name_input))
        
        # Add widgets to main layout
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.daily_checkbox)
        main_layout.addWidget(self.days_group)
        main_layout.addWidget(self.create_form_row("⏰ Execution Time:", self.time_input))
        main_layout.addWidget(self.specific_dates_checkbox)
        main_layout.addWidget(self.calendar)
        
        # Button container with centered button
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addStretch()
        
        main_layout.addWidget(button_container)
        self.setLayout(main_layout)

        # Hide calendar by default
        self.calendar.setVisible(False)
        self.update_name()










    # Ajoutez cette nouvelle méthode à la classe AddActivityDialog:
    def validate_and_accept(self):
        """Validate inputs before accepting the dialog."""
        if not self.program_input.currentText():
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a program")
            return
            
        if not self.daily_checkbox.isChecked() and not any(cb.isChecked() for cb in self.day_checkboxes) and not self.specific_dates_checkbox.isChecked():
            QtWidgets.QMessageBox.warning(self, "Error", "Please select at least one schedule option (daily, weekly days, or specific dates)")
            return
            
        if self.specific_dates_checkbox.isChecked() and not self.selected_dates:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select at least one specific date")
            return
            
        self.accept()
        
    def create_form_row(self, label_text, widget):
        """Create a form row with styled label and widget."""
        container = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        label = QtWidgets.QLabel(label_text)
        label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        
        layout.addWidget(label)
        layout.addWidget(widget)
        return container

    def update_name(self):
        """Update the name field based on selected program."""
        if self.program_input.currentIndex() >= 0:
            self.name_input.setText(self.program_input.currentText())

    def toggle_specific_dates(self, state):
        """Show/hide calendar based on checkbox state."""
        self.calendar.setVisible(state == QtCore.Qt.Checked)
        if state == QtCore.Qt.Checked:
            self.daily_checkbox.setChecked(False)
            for checkbox in self.day_checkboxes:
                checkbox.setChecked(False)

    def toggle_date_selection(self, date):
        """Add or remove date from selection."""
        if date in self.selected_dates:
            self.selected_dates.remove(date)
        else:
            self.selected_dates.add(date)
        self.highlight_selected_dates()

    def highlight_selected_dates(self):
        """Highlight selected dates in calendar."""
        # Clear all formats first
        self.calendar.setDateTextFormat(QtCore.QDate(), QtGui.QTextCharFormat())
        
        # Highlight current date
        current_format = QtGui.QTextCharFormat()
        current_format.setBackground(QtGui.QColor("#3498db20"))
        current_format.setForeground(QtGui.QColor("#2c3e50"))
        self.calendar.setDateTextFormat(QtCore.QDate.currentDate(), current_format)
        
        # Highlight selected dates
        for date in self.selected_dates:
            format = QtGui.QTextCharFormat()
            format.setBackground(QtGui.QColor("#3498db"))
            format.setForeground(QtGui.QColor("#ffffff"))
            format.setFontWeight(QFont.Bold)
            self.calendar.setDateTextFormat(date, format)

    def get_activity_data(self):
        """Return user input data including specific dates if selected."""
        selected_days = [checkbox.text() for checkbox in self.day_checkboxes if checkbox.isChecked()]
        
        if self.specific_dates_checkbox.isChecked():
            selected_dates = [date.toString("MM/dd/yyyy") for date in self.selected_dates]
        else:
            selected_dates = None

        return (
            self.name_input.text(),
            self.program_input.currentText(),
            self.daily_checkbox.isChecked(),
            selected_days,
            self.time_input.time().toString("HH:mm"),
            selected_dates
        )

class Activite(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr("📅 Scheduled Activities Manager"))
        self.setStyleSheet(self._get_styles())
        self.resize(1200, 800)
        self.setWindowIcon(QtGui.QIcon("resources/icons/calendar.ico"))

        # Main title with gradient effect
        title_label = QtWidgets.QLabel(self.tr("📅 Scheduled Activities Manager"))
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setFont(QtGui.QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                padding: 10px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2c3e50);
                border-radius: 10px;
                color: white;
            }
        """)

        # Search bar with modern style
        self.search_entry = QtWidgets.QLineEdit()
        self.search_entry.setPlaceholderText(self.tr("🔍 Search activities..."))
        self.search_entry.setStyleSheet("""
            QLineEdit {
                border: 2px solid #dfe6e9;
                border-radius: 15px;
                padding: 8px 15px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)

        button_style = """
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {gradient_start}, stop:1 {gradient_end});
            color: white;
            font-size: 14px;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px 15px;
            min-width: 120px;
            border: none;
        }}
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {hover_start}, stop:1 {hover_end});
        }}
        QPushButton:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {pressed_start}, stop:1 {pressed_end});
        }}
        QPushButton:disabled {{
            background: #95a5a6;
        }}
        """.replace('\n', '').replace('    ', '')
        self.search_button = self.create_button(
            "🔍 Search", 
            button_style.format(
                gradient_start="#3498db", gradient_end="#2980b9",
                hover_start="#2980b9", hover_end="#1a5276",
                pressed_start="#1a5276", pressed_end="#154360"
            )
        )
        self.search_button.clicked.connect(self.search_activities)

        self.add_button = self.create_button(
            "➕ Add Activity", 
            button_style.format(
                gradient_start="#2ecc71", gradient_end="#27ae60",
                hover_start="#27ae60", hover_end="#219653",
                pressed_start="#219653", pressed_end="#1e8449"
            )
        )
        self.add_button.clicked.connect(self.add_activity)

        self.pause_button = self.create_button(
            "⏸️ Pause", 
            button_style.format(
                gradient_start="#f39c12", gradient_end="#e67e22",
                hover_start="#e67e22", hover_end="#d35400",
                pressed_start="#d35400", pressed_end="#ba4a00"
            )
        )
        self.pause_button.clicked.connect(self.pause_selected_activities)

        self.delete_button = self.create_button(
            "❌ Delete", 
            button_style.format(
                gradient_start="#e74c3c", gradient_end="#c0392b",
                hover_start="#c0392b", hover_end="#a93226",
                pressed_start="#a93226", pressed_end="#922b21"
            )
        )
        self.delete_button.clicked.connect(self.delete_selected_activities)

        self.refresh_button = self.create_button(
            "🔄 Refresh", 
            button_style.format(
                gradient_start="#9b59b6", gradient_end="#8e44ad",
                hover_start="#8e44ad", hover_end="#7d3c98",
                pressed_start="#7d3c98", pressed_end="#6c3483"
            )
        )
        self.refresh_button.clicked.connect(self.load_activities)

        self.export_button = self.create_button(
            "📤 Export", 
            button_style.format(
                gradient_start="#1abc9c", gradient_end="#16a085",
                hover_start="#16a085", hover_end="#138d75",
                pressed_start="#138d75", pressed_end="#117a65"
            )
        )
        self.export_button.clicked.connect(self.export_activities)

        # Dans __init__(), modifiez le bouton Export :
        self.import_export_button = QtWidgets.QPushButton("📊 Importer/Exporter")
        self.import_export_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1abc9c, stop:1 #16a085);
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #16a085, stop:1 #138d75);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #138d75, stop:1 #117a65);
            }
        """)
        self.import_export_button.clicked.connect(self.show_import_export_menu)
        # Add shadow effect to add button
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(46, 204, 113, 150))
        shadow.setOffset(0, 5)
        self.add_button.setGraphicsEffect(shadow)

        # Top bar layout with search and buttons
        top_bar_layout = QtWidgets.QHBoxLayout()
        top_bar_layout.setSpacing(15)
        top_bar_layout.addWidget(self.search_entry, 4)
        top_bar_layout.addWidget(self.search_button, 1)
        top_bar_layout.addWidget(self.add_button, 1)
        top_bar_layout.addWidget(self.pause_button, 1)
        top_bar_layout.addWidget(self.delete_button, 1)
        top_bar_layout.addWidget(self.refresh_button, 1)
        # top_bar_layout.addWidget(self.export_button, 1)
        top_bar_layout.addWidget(self.import_export_button, 1)

        # Activities table with modern style
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            self.tr("🔢 #"), self.tr("📝 Name"), self.tr("📂 Program"), 
            self.tr("📅 Days"), self.tr("⏰ Time"), self.tr("📅 Date"), self.tr("🔄 Statut"), self.tr("⚙️ Action")
        ])



    #     # Customize table appearance
    #     self.table.setStyleSheet("""
    #         QTableWidget {
    #             background-color: white;
    #             border: 2px solid #dfe6e9;
    #             border-radius: 8px;
    #             gridline-color: #dfe6e9;
    #             font-size: 14px;
    #         }
    #         QHeaderView::section {
    #             background-color: #3498db;
    #             color: white;
    #             font-weight: bold;
    #             padding: 8px;
    #             border: none;
    #             font-size: 14px;
    #         }

    #         QScrollBar:vertical {
    #             border: none;
    #             background: #f5f5f5;
    #             width: 12px;
    #             margin: 0px 0px 0px 0px;
    #         }
    #         QScrollBar::handle:vertical {
    #             background: #bdc3c7;
    #             min-height: 20px;
    #             border-radius: 6px;
    #         }
    #         QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    #             background: none;
    #         }
    #         QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    #             background: none;
    #         }
    #             QTableWidget::item:selected {
    #     background-color: transparent;
    #     color: inherit;
    # }
    # QTableWidget::item:selected:active {
    #     background-color: transparent;
    # }
    #     """)

        self.table.setStyleSheet("""
    QTableWidget::item:selected {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #3498db, stop:1 #2980b9);
        color: white;
        border: none;
    }
""")
        
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        
        # Set custom delegate for action column
        self.table.setItemDelegateForColumn(6, RoundButtonDelegate())
        
        # Main layout with proper spacing
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Add widgets to main layout
        main_layout.addWidget(title_label)
        main_layout.addLayout(top_bar_layout)
        main_layout.addWidget(self.table)
        
        self.setLayout(main_layout)

        # Load scheduled activities on startup
        QtCore.QTimer.singleShot(100, self.load_activities)

    def create_button1(self, text, style_sheet):
        """Create a styled button with hover effects."""
        button = QtWidgets.QPushButton(text)
        button.setStyleSheet(style_sheet)
        button.setCursor(Qt.PointingHandCursor)
        return button


    def create_button(self, text, style_sheet):
        """Create a styled button with hover effects."""
        button = QtWidgets.QPushButton(text)
        # Supprimez les sauts de ligne et les espaces excessifs dans le style_sheet
        style_sheet = style_sheet.replace('\n', '').replace('                ', '')
        button.setStyleSheet(style_sheet)
        button.setCursor(Qt.PointingHandCursor)
        return button


    def _get_styles(self):
        """Return CSS styles for the UI."""
        return """
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f5f7fa, stop:1 #c3cfe2);
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
                color: #2c3e50;
            }
            QLineEdit {
                border: 2px solid #dfe6e9;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
            QPushButton {
                min-width: 100px;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 5px;
                font-weight: bold;
            }
            QStatusBar {
                background-color: #2c3e50;
                color: white;
            }
        """
    def update_pause_button_text(self):
        """Change le texte du bouton Pause selon la sélection."""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            self.pause_button.setText("⏸️ Pause")
            return

        # Vérifie si au moins une tâche sélectionnée est active
        any_active = any(
            not self.is_task_disabled(self.table.item(row.row(), 1).text())
            for row in selected_rows
        )

        self.pause_button.setText("⏸️ Pause" if any_active else "▶️ Reprendre")



    def load_activities(self):
        """Load and display scheduled activities."""
        self.table.setRowCount(0)  # Reset table

        try:
            # Path to folder containing .exe files
            folder_path = os.path.expanduser("~\\AppData\\Roaming\\Saadiya\\resources\\tools")
            if not os.path.exists(folder_path):
                self.show_error_message(self.tr("Folder Not Found"), 
                                      self.tr(f"The folder {folder_path} does not exist."))
                return

            # List .exe files
            exe_files = [f for f in os.listdir(folder_path) if f.endswith(".exe")]
            if not exe_files:
                self.show_warning_message(self.tr("No Programs Found"), 
                                         self.tr("No .exe files found in the tools folder."))
                return

            # Get scheduled tasks with schtasks
            try:
                result = subprocess.check_output("schtasks /query /fo csv /nh", shell=True, 
                                                encoding="utf-8", errors="ignore")
            except subprocess.CalledProcessError as e:
                self.show_error_message(self.tr("Query Failed"), 
                                       self.tr(f"Failed to query scheduled tasks: {e}"))
                return

            lines = result.strip().splitlines()

            if not lines:
                self.show_info_message(self.tr("No Tasks Found"), 
                                     self.tr("No scheduled tasks found."))
                return

            # Parse tasks
            for i, line in enumerate(lines):
                try:
                    parts = [p.strip('"') for p in line.split(",")]
                    if len(parts) < 3:
                        continue

                    task_name = parts[0].lstrip("\\").strip()
                    task_name_with_extension = f"{task_name}.exe"

                    if task_name_with_extension.lower() in [exe_file.lower() for exe_file in exe_files]:
                        row_position = self.table.rowCount()
                        self.table.insertRow(row_position)

                        # Add columns with formatted data
                        self.table.setItem(row_position, 0, QTableWidgetItem(str(i + 1)))
                        self.table.setItem(row_position, 1, QTableWidgetItem(task_name))
                        self.table.setItem(row_position, 2, QTableWidgetItem(parts[1] if len(parts) > 1 else ""))
                        self.table.setItem(row_position, 3, QTableWidgetItem(parts[2] if len(parts) > 2 else ""))
                        self.table.setItem(row_position, 4, QTableWidgetItem(parts[3] if len(parts) > 3 else ""))
                        self.table.setItem(row_position, 5, QTableWidgetItem(parts[4] if len(parts) > 4 else ""))

                        # Add action button
                        action_button = QtWidgets.QPushButton(self.tr("⚙️ Action"))
                        action_button.setStyleSheet("""
  

                      

                            QPushButton:pressed {
                                background-color: #2471a3;
                                padding-top: 10px;
                                padding-bottom: 6px;
                            }

                            QPushButton:disabled {
                                background-color: #bdc3c7;
                                color: #ecf0f1;
                            }

                                QPushButton {
        background-color: #3498db;
        color: white;
        border-radius: 15px;
        padding: 5px 10px;
        font-weight: bold;
        min-width: 80px;
        border: none;
    }
    QPushButton:hover {
        background-color: #2980b9;
    }
                        """)


                        action_button.clicked.connect(lambda _, name=task_name: self.show_action_menu(name))
                        self.table.setCellWidget(row_position, 6, action_button)

                        # Set row colors for better readability
                        for col in range(self.table.columnCount()):
                            if self.table.item(row_position, col):
                                self.table.item(row_position, col).setTextAlignment(Qt.AlignCenter)
                                if row_position % 2 == 0:
                                    self.table.item(row_position, col).setBackground(QColor(240, 248, 255))
                except Exception as e:
                    self.show_warning_message(self.tr("Processing Error"), 
                                           self.tr(f"Error processing task: {e}"))

            # Resize columns to content
            self.table.resizeColumnsToContents()
            self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        except Exception as e:
            self.show_error_message(self.tr("Loading Error"), 
                                 self.tr(f"Error loading activities: {e}"))

    def show_action_menu(self, name):
        """Show context menu for a specific activity."""
        menu = QtWidgets.QMenu(self)
        
        # Create actions with icons
        modify_action = QtWidgets.QAction(QtGui.QIcon("resources/icons/edit.png"), "✏️ Modify", self)
        delete_action = QtWidgets.QAction(QtGui.QIcon("resources/icons/delete.png"), "❌ Delete", self)
        run_action = QtWidgets.QAction(QtGui.QIcon("resources/icons/run.png"), "▶️ Run Now", self)
        
        # Add actions to menu
        menu.addAction(modify_action)
        menu.addAction(delete_action)
        menu.addAction(run_action)
        
        # Style the menu
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 2px solid #dfe6e9;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 25px 8px 20px;
                font-size: 14px;
            }
            QMenu::item:selected {
                background-color: #3498db;
                color: white;
                border-radius: 3px;
            }
            QMenu::icon {
                padding-left: 10px;
            }
        """)
        
        # Connect actions to functions
        modify_action.triggered.connect(lambda: self.modify_activity(name))
        delete_action.triggered.connect(lambda: self.delete_activity(name))
        run_action.triggered.connect(lambda: self.run_activity_now(name))
        
        # Show menu at cursor position
        menu.exec_(QtGui.QCursor.pos())



    def add_activity(self):
        """Add a new scheduled activity."""
        folder_path = os.path.expanduser("~\\AppData\\Roaming\\Saadiya\\resources\\tools")
        exe_files = [os.path.splitext(f)[0] for f in os.listdir(folder_path) if f.endswith(".exe")]

        dialog = AddActivityDialog(exe_files)
        if dialog.exec_() == QDialog.Accepted:
            name, program, daily, days, time, specific_dates = dialog.get_activity_data()
            program_path = os.path.join(folder_path, f"{program}.exe")

            if specific_dates:
                # Schedule for specific dates
                for date in specific_dates:
                    try:
                        cmd = (
                            f'schtasks /create /tn "{name}_{date}" /tr "{program_path}" '
                            f'/SC ONCE /SD {date} /ST {time} /f'
                        )
                        subprocess.run(cmd, shell=True)
                    except Exception as e:
                        self.show_error_message(self.tr("Scheduling Error"), 
                                             self.tr(f"Error scheduling activity: {e}"))
            else:
                # Daily or weekly schedule
                schedule_type = "/SC DAILY" if daily else "/SC WEEKLY"
                date_flag = "" if daily else f" /D {','.join(days)}"

                try:
                    cmd = (
                        f'schtasks /create /tn "{name}" /tr "{program_path}" '
                        f'{schedule_type} {date_flag} /st {time} /f'
                    )
                    subprocess.run(cmd, shell=True)
                except Exception as e:
                    self.show_error_message(self.tr("Scheduling Error"), 
                                         self.tr(f"Error scheduling activity: {e}"))

            self.show_success_message(self.tr("Success"), 
                                   self.tr("Activity scheduled successfully!"))
            self.load_activities()

    def search_activities(self):
        """Filter activities based on search query."""
        query = self.search_entry.text().lower()
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount() - 1):  # Skip action column
                item = self.table.item(row, col)
                if item and query in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)

    def delete_activity(self, name):
        """Delete a scheduled activity."""
        reply = QMessageBox.question(
            self,
            self.tr("Confirmation"),
            self.tr(f"Are you sure you want to delete the activity '{name}'?"),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                subprocess.run(f'schtasks /delete /tn "{name}" /f', shell=True)
                self.show_success_message(self.tr("Success"), 
                                       self.tr(f"Activity {name} deleted successfully!"))
                self.load_activities()
            except Exception as e:
                self.show_error_message(self.tr("Deletion Error"), 
                                     self.tr(f"Error deleting activity: {e}"))

    def modify_activity(self, name):
        """Modify a scheduled activity."""
        # Get task details
        try:
            result = subprocess.check_output(f'schtasks /query /tn "{name}" /fo list', 
                                           shell=True, encoding="utf-8", errors="ignore")
            details = result.strip().splitlines()
        except subprocess.CalledProcessError as e:
            self.show_error_message(self.tr("Details Error"), 
                                 self.tr(f"Failed to retrieve task details: {e}"))
            return

        # Create modification dialog
        dialog = AddActivityDialog(self.get_exe_files())
        if dialog.exec_() == QDialog.Accepted:
            new_name, program, daily, days, time, specific_dates = dialog.get_activity_data()
            program_path = os.path.join(self.get_tools_folder(), f"{program}.exe")

            try:
                # Delete old task
                subprocess.run(f'schtasks /delete /tn "{name}" /f', shell=True)

                # Create new task
                if specific_dates:
                    for date in specific_dates:
                        cmd = (
                            f'schtasks /create /tn "{new_name}_{date}" /tr "{program_path}" '
                            f'/SC ONCE /SD {date} /ST {time} /f'
                        )
                        subprocess.run(cmd, shell=True)
                else:
                    schedule_type = "/SC DAILY" if daily else "/SC WEEKLY"
                    date_flag = "" if daily else f" /D {','.join(days)}"

                    cmd = (
                        f'schtasks /create /tn "{new_name}" /tr "{program_path}" '
                        f'{schedule_type} {date_flag} /st {time} /f'
                    )
                    subprocess.run(cmd, shell=True)

                self.show_success_message(self.tr("Success"), 
                                       self.tr("Activity modified successfully!"))
                self.load_activities()
            except Exception as e:
                self.show_error_message(self.tr("Modification Error"), 
                                     self.tr(f"Error modifying activity: {e}"))

    def export_activities(self):
        """Export scheduled activities to a CSV file."""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                self.tr("Export Activities"), 
                "", 
                "CSV Files (*.csv)"
            )
            
            if file_path:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write("Number,Name,Program,Days,Time,Date\n")
                    for row in range(self.table.rowCount()):
                        row_data = [
                            self.table.item(row, col).text() if self.table.item(row, col) else ""
                            for col in range(self.table.columnCount() - 1)  # Skip action column
                        ]
                        file.write(",".join(row_data) + "\n")
                
                self.show_success_message(self.tr("Export Success"), 
                                       self.tr("Activities exported successfully!"))
        except Exception as e:
            self.show_error_message(self.tr("Export Error"), 
                                 self.tr(f"Error exporting activities: {e}"))

    def pause_selected_activities1(self):
        """Pause selected activities."""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            self.show_warning_message(self.tr("Selection Required"), 
                                   self.tr("Please select activities to pause."))
            return

        for row in selected_rows:
            activity_name = self.table.item(row.row(), 1).text()
            try:
                subprocess.run(f'schtasks /change /tn "{activity_name}" /disable', shell=True)
            except Exception as e:
                self.show_error_message(self.tr("Pause Error"), 
                                     self.tr(f"Error pausing activity {activity_name}: {e}"))

        self.show_success_message(self.tr("Success"), 
                               self.tr("Selected activities paused successfully!"))
        self.load_activities()


    def is_task_disabled(self, task_name):
        """Vérifie si une tâche est désactivée."""
        try:
            result = subprocess.run(
                f'schtasks /query /tn "{task_name}" /fo list',
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            return "Désactivé" in result.stdout or "Disabled" in result.stdout
        except subprocess.CalledProcessError:
            return False
        
    def pause_selected_activities(self):
        """Active ou désactive les tâches sélectionnées."""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            self.show_warning_message(
                "Sélection requise",
                "Veuillez sélectionner des activités à mettre en pause/reprendre."
            )
            return

        for row in selected_rows:
            activity_name = self.table.item(row.row(), 1).text()
            is_disabled = self.is_task_disabled(activity_name)

            try:
                if is_disabled:
                    # Si la tâche est en pause, on la relance
                    subprocess.run(
                        f'schtasks /change /tn "{activity_name}" /enable',
                        shell=True,
                        check=True
                    )
                else:
                    # Si la tâche est active, on la met en pause
                    subprocess.run(
                        f'schtasks /change /tn "{activity_name}" /disable',
                        shell=True,
                        check=True
                    )
            except subprocess.CalledProcessError as e:
                self.show_error_message(
                    "Erreur",
                    f"Impossible de modifier l'état de '{activity_name}': {e}"
                )

        self.show_success_message(
            "Succès",
            "Les activités sélectionnées ont été mises à jour."
        )
        self.load_activities()  # Recharge la liste pour afficher les nouveaux états

        
    def delete_selected_activities(self):
        """Delete selected activities."""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            self.show_warning_message(self.tr("Selection Required"), 
                                   self.tr("Please select activities to delete."))
            return

        reply = QMessageBox.question(
            self,
            self.tr("Confirm Deletion"),
            self.tr(f"Are you sure you want to delete {len(selected_rows)} selected activities?"),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            for row in selected_rows:
                activity_name = self.table.item(row.row(), 1).text()
                try:
                    subprocess.run(f'schtasks /delete /tn "{activity_name}" /f', shell=True)
                except Exception as e:
                    self.show_error_message(self.tr("Deletion Error"), 
                                         self.tr(f"Error deleting activity {activity_name}: {e}"))

            self.show_success_message(self.tr("Success"), 
                                   self.tr("Selected activities deleted successfully!"))
            self.load_activities()

    def run_activity_now(self, name):
        """Run the selected activity immediately."""
        try:
            subprocess.run(f'schtasks /run /tn "{name}"', shell=True)
            self.show_success_message(self.tr("Success"), 
                                   self.tr(f"Activity '{name}' started successfully!"))
        except Exception as e:
            self.show_error_message(self.tr("Execution Error"), 
                                 self.tr(f"Error running activity: {e}"))

    def get_exe_files(self):
        """Get list of executable files from tools folder."""
        folder_path = os.path.expanduser("~\\AppData\\Roaming\\Saadiya\\resources\\tools")
        return [os.path.splitext(f)[0] for f in os.listdir(folder_path) if f.endswith(".exe")]

    def get_tools_folder(self):
        """Get path to tools folder."""
        return os.path.expanduser("~\\AppData\\Roaming\\Saadiya\\resources\\tools")

    def show_error_message(self, title, message):
        """Show styled error message."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                font-size: 14px;
            }
            QLabel {
                color: #2c3e50;
            }
        """)
        msg.exec_()

    def show_warning_message(self, title, message):
        """Show styled warning message."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                font-size: 14px;
            }
            QLabel {
                color: #2c3e50;
            }
        """)
        msg.exec_()

    def show_success_message(self, title, message):
        """Show styled success message."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                font-size: 14px;
            }
            QLabel {
                color: #2c3e50;
            }
        """)
        msg.exec_()

    def show_info_message(self, title, message):
        """Show styled information message."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                font-size: 14px;
            }
            QLabel {
                color: #2c3e50;
            }
        """)
        msg.exec_()



    def fill_table_row(self, row, task):
        """Remplit une ligne du tableau avec les données de la tâche"""
        # Colonne 0: Numéro
        self.table.setItem(row, 0, self.create_centered_item(str(row + 1)))
        
        # Colonne 1: Nom
        self.table.setItem(row, 1, self.create_centered_item(task["name"]))
        
        # Colonne 2: Programme
        self.table.setItem(row, 2, self.create_centered_item(task["program"]))
        
        # Colonne 3: Jours
        days = ", ".join(task["days"]) if task["days"] else "Quotidien"
        self.table.setItem(row, 3, self.create_centered_item(days))
        
        # Colonne 4: Heure
        self.table.setItem(row, 4, self.create_centered_item(task["time"]))
        
        # Colonne 5: Date
        self.table.setItem(row, 5, self.create_centered_item(task["date"] or "N/A"))
        
        # Colonne 6: Statut (avec couleur)
        status_item = self.create_centered_item("⏸️ Pause" if task["disabled"] else "▶️ Actif")
        status_item.setForeground(QtGui.QColor("#e74c3c" if task["disabled"] else "#2ecc71"))
        self.table.setItem(row, 6, status_item)
        
        # Colonne 7: Bouton d'action
        self.add_action_button(row, task["name"])

    def create_centered_item(self, text):
        """Crée un QTableWidgetItem centré avec le texte donné"""
        item = QtWidgets.QTableWidgetItem(text)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        return item

    def colorize_row(self, row, color):
        """Applique une couleur de fond à toute une ligne"""
        for col in range(self.table.columnCount()):
            if self.table.item(row, col):
                self.table.item(row, col).setBackground(QtGui.QColor(color))

    def add_action_button(self, row, task_name):
        """Ajoute un bouton d'action stylisé dans la dernière colonne"""
        btn = QtWidgets.QPushButton("⚙️ Actions")
        btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 4px;
                padding: 5px 10px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn.clicked.connect(lambda _, name=task_name: self.show_action_menu(name))
        self.table.setCellWidget(row, 7, btn)

    def update_action_buttons(self):
        """Met à jour les boutons en fonction de la sélection"""
        selected_rows = self.table.selectionModel().selectedRows()
        
        # Bouton Pause/Reprendre
        if selected_rows:
            any_active = any(
                self.table.item(row.row(), 6).text() == "▶️ Actif"
                for row in selected_rows
            )
            self.pause_button.setText("⏸️ Pause" if any_active else "▶️ Reprendre")
            self.pause_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        else:
            self.pause_button.setEnabled(False)
            self.delete_button.setEnabled(False)

    def get_scheduled_tasks(self):
        """Récupère les tâches planifiées avec leurs métadonnées"""
        tasks = []
        try:
            # Exemple de données (à remplacer par votre logique schtasks)
            raw_tasks = subprocess.check_output(
                'schtasks /query /fo csv /nh',
                shell=True,
                encoding='utf-8',
                errors='ignore'
            ).splitlines()
            
            for line in raw_tasks:
                parts = line.strip('"').split('","')
                if len(parts) >= 6:
                    tasks.append({
                        "name": parts[0],
                        "program": parts[1],
                        "days": self.parse_days(parts[2]),
                        "time": parts[3],
                        "date": parts[4],
                        "disabled": "Désactivé" in parts[5] or "Disabled" in parts[5]
                    })
        
        except Exception as e:
            self.show_error_message("Erreur", f"Impossible de lire les tâches : {str(e)}")
        
        return tasks

    def parse_days(self, days_str):
        """Convertit la chaîne de jours en liste"""
        if not days_str or days_str.lower() == "tous les jours":
            return []
        return [d.strip() for d in days_str.split(",")]



    def load_activities2(self):
        """Load and display scheduled activities."""
        self.table.setRowCount(0)  # Reset table

        try:
            # Path to folder containing .exe files
            folder_path = os.path.expanduser("~\\AppData\\Roaming\\Saadiya\\resources\\tools")
            if not os.path.exists(folder_path):
                self.show_error_message(self.tr("Folder Not Found"), 
                                      self.tr(f"The folder {folder_path} does not exist."))
                return

            # List .exe files
            exe_files = [f for f in os.listdir(folder_path) if f.endswith(".exe")]
            if not exe_files:
                self.show_warning_message(self.tr("No Programs Found"), 
                                         self.tr("No .exe files found in the tools folder."))
                return

            # Get scheduled tasks with schtasks
            try:
                result = subprocess.check_output("schtasks /query /fo csv /nh", shell=True, 
                                                encoding="utf-8", errors="ignore")
            except subprocess.CalledProcessError as e:
                self.show_error_message(self.tr("Query Failed"), 
                                       self.tr(f"Failed to query scheduled tasks: {e}"))
                return

            lines = result.strip().splitlines()

            if not lines:
                self.show_info_message(self.tr("No Tasks Found"), 
                                     self.tr("No scheduled tasks found."))
                return

            # Parse tasks
            for i, line in enumerate(lines):
                try:
                    parts = [p.strip('"') for p in line.split(",")]
                    if len(parts) < 3:
                        continue

                    task_name = parts[0].lstrip("\\").strip()
                    task_name_with_extension = f"{task_name}.exe"

                    if task_name_with_extension.lower() in [exe_file.lower() for exe_file in exe_files]:
                        row_position = self.table.rowCount()
                        self.table.insertRow(row_position)

                        # Add columns with formatted data
                        self.table.setItem(row_position, 0, QTableWidgetItem(str(i + 1)))
                        self.table.setItem(row_position, 1, QTableWidgetItem(task_name))
                        self.table.setItem(row_position, 2, QTableWidgetItem(parts[1] if len(parts) > 1 else ""))
                        self.table.setItem(row_position, 3, QTableWidgetItem(parts[2] if len(parts) > 2 else ""))
                        self.table.setItem(row_position, 4, QTableWidgetItem(parts[3] if len(parts) > 3 else ""))
                        self.table.setItem(row_position, 5, QTableWidgetItem(parts[4] if len(parts) > 4 else ""))

                        # Add action button
                        action_button = QtWidgets.QPushButton(self.tr("⚙️ Action"))
                        action_button.setStyleSheet("""
  

                      

                            QPushButton:pressed {
                                background-color: #2471a3;
                                padding-top: 10px;
                                padding-bottom: 6px;
                            }

                            QPushButton:disabled {
                                background-color: #bdc3c7;
                                color: #ecf0f1;
                            }

                                QPushButton {
        background-color: #3498db;
        color: white;
        border-radius: 15px;
        padding: 5px 10px;
        font-weight: bold;
        min-width: 80px;
        border: none;
    }
    QPushButton:hover {
        background-color: #2980b9;
    }
                        """)


                        action_button.clicked.connect(lambda _, name=task_name: self.show_action_menu(name))
                        self.table.setCellWidget(row_position, 6, action_button)

                        # Set row colors for better readability
                        for col in range(self.table.columnCount()):
                            if self.table.item(row_position, col):
                                self.table.item(row_position, col).setTextAlignment(Qt.AlignCenter)
                                if row_position % 2 == 0:
                                    self.table.item(row_position, col).setBackground(QColor(240, 248, 255))
                except Exception as e:
                    self.show_warning_message(self.tr("Processing Error"), 
                                           self.tr(f"Error processing task: {e}"))

            # Resize columns to content
            self.table.resizeColumnsToContents()
            self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        except Exception as e:
            self.show_error_message(self.tr("Loading Error"), 
                                 self.tr(f"Error loading activities: {e}"))

    def load_activities(self):
        """Charge et affiche les activités planifiées avec gestion améliorée des états"""
        self.table.setRowCount(0)  # Réinitialise le tableau
        self.table.setSortingEnabled(False)  # Désactive le tri pendant le chargement

        try:
            # Vérification du dossier des outils
            folder_path = os.path.expanduser("~\\AppData\\Roaming\\Saadiya\\resources\\tools")
            if not os.path.exists(folder_path):
                self.show_error_message(self.tr("Dossier introuvable"), 
                                    self.tr(f"Le dossier {folder_path} n'existe pas."))
                return

            # Liste des fichiers exe
            exe_files = [f for f in os.listdir(folder_path) if f.endswith(".exe")]
            if not exe_files:
                self.show_warning_message(self.tr("Aucun programme trouvé"), 
                                        self.tr("Aucun fichier .exe trouvé dans le dossier des outils."))
                return

            # Récupération des tâches planifiées
            try:
                result = subprocess.check_output("schtasks /query /fo csv /nh", shell=True, 
                                            encoding="utf-8", errors="ignore")
                lines = result.strip().splitlines()
            except subprocess.CalledProcessError as e:
                self.show_error_message(self.tr("Erreur de requête"), 
                                    self.tr(f"Échec de la récupération des tâches : {e}"))
                return

            if not lines:
                self.show_info_message(self.tr("Aucune tâche trouvée"), 
                                    self.tr("Aucune tâche planifiée trouvée."))
                return

            # Traitement des tâches
            for i, line in enumerate(lines):
                try:
                    parts = [p.strip('"') for p in line.split(",")]
                    if len(parts) < 3:
                        continue

                    task_name = parts[0].lstrip("\\").strip()
                    task_name_with_extension = f"{task_name}.exe"

                    if task_name_with_extension.lower() in [exe_file.lower() for exe_file in exe_files]:
                        row_position = self.table.rowCount()
                        self.table.insertRow(row_position)

                        # Détermine l'état de la tâche
                        is_disabled = "Désactivé" in parts[-1] or "Disabled" in parts[-1]

                        # Colonne 0: Numéro
                        self.table.setItem(row_position, 0, self.create_centered_item(str(i + 1)))
                        
                        # Colonne 1: Nom
                        self.table.setItem(row_position, 1, self.create_centered_item(task_name))
                        
                        # Colonne 2: Programme
                        self.table.setItem(row_position, 2, self.create_centered_item(parts[1] if len(parts) > 1 else ""))
                        
                        # Colonne 3: Jours
                        self.table.setItem(row_position, 3, self.create_centered_item(parts[2] if len(parts) > 2 else ""))
                        
                        # Colonne 4: Heure
                        self.table.setItem(row_position, 4, self.create_centered_item(parts[3] if len(parts) > 3 else ""))
                        
                        # Colonne 5: Date
                        self.table.setItem(row_position, 5, self.create_centered_item(parts[4] if len(parts) > 4 else ""))
                        
                        # Colonne 6: Statut (nouvelle colonne)
                        status_item = self.create_centered_item("⏸️ Pause" if is_disabled else "▶️ Actif")
                        status_item.setForeground(QtGui.QColor("#e74c3c" if is_disabled else "#2ecc71"))
                        self.table.setItem(row_position, 6, status_item)
                        
                        # Colonne 7: Bouton d'action
                        action_button = QtWidgets.QPushButton(self.tr("⚙️ Action"))
                        action_button.setStyleSheet("""
                            QPushButton {
                                background-color: #3498db;
                                color: white;
                                border-radius: 15px;
                                padding: 5px 10px;
                                font-weight: bold;
                                min-width: 80px;
                                border: none;
                            }
                            QPushButton:hover {
                                background-color: #2980b9;
                            }
                            QPushButton:pressed {
                                background-color: #2471a3;
                            }
                        """)
                        action_button.clicked.connect(lambda _, name=task_name: self.show_action_menu(name))
                        self.table.setCellWidget(row_position, 7, action_button)

                        # Couleur de fond alternée pour les lignes
                        for col in range(self.table.columnCount()):
                            if self.table.item(row_position, col):
                                if row_position % 2 == 0:
                                    self.table.item(row_position, col).setBackground(QColor(240, 248, 255))

                except Exception as e:
                    self.show_warning_message(self.tr("Erreur de traitement"), 
                                        self.tr(f"Erreur lors du traitement de la tâche : {e}"))

            # Configuration finale de la table
            self.table.setSortingEnabled(True)
            self.table.resizeColumnsToContents()
            self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            
            # Connexion de la sélection pour mettre à jour les boutons
            self.table.selectionModel().selectionChanged.connect(self.update_action_buttons)

        except Exception as e:
            self.show_error_message(self.tr("Erreur de chargement"), 
                                self.tr(f"Erreur lors du chargement des activités : {e}"))

    def create_centered_item(self, text):
        """Crée un QTableWidgetItem avec texte centré"""
        item = QtWidgets.QTableWidgetItem(text)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        return item

    def update_action_buttons(self):
        """Met à jour les boutons en fonction de la sélection"""
        selected_rows = self.table.selectionModel().selectedRows()
        
        if selected_rows:
            # Vérifie si au moins une tâche sélectionnée est active
            any_active = any(
                self.table.item(row.row(), 6).text() == "▶️ Actif"
                for row in selected_rows
            )
            self.pause_button.setText("⏸️ Pause" if any_active else "▶️ Reprendre")
            self.pause_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        else:
            self.pause_button.setEnabled(False)
            self.delete_button.setEnabled(False)


    def show_import_export_menu(self):
        """Affiche le menu contextuel pour l'import/export"""
        menu = QtWidgets.QMenu(self)
        
        # Actions avec icônes
        export_action = QtWidgets.QAction(QtGui.QIcon("resources/icons/export.png"), "Exporter vers CSV", self)
        import_action = QtWidgets.QAction(QtGui.QIcon("resources/icons/import.png"), "Importer depuis CSV", self)
        
        # Style du menu
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 2px solid #dfe6e9;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 25px 8px 20px;
                font-size: 14px;
            }
            QMenu::item:selected {
                background-color: #3498db;
                color: white;
                border-radius: 3px;
            }
        """)
        
        menu.addAction(export_action)
        menu.addAction(import_action)
        
        # Connexion des actions
        export_action.triggered.connect(self.export_to_csv)
        import_action.triggered.connect(self.import_from_csv)
        
        # Affichage du menu
        menu.exec_(QtGui.QCursor.pos())
    def export_to_csv(self):
        """Exporte les activités vers un fichier CSV"""
        try:
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self,
                "Exporter les activités",
                "",
                "Fichiers CSV (*.csv);;Tous les fichiers (*)"
            )
            
            if not file_path:
                return
                
            # Ajout automatique de l'extension si absent
            if not file_path.lower().endswith('.csv'):
                file_path += '.csv'
            
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                
                # En-têtes
                headers = [self.table.horizontalHeaderItem(i).text().replace("🔢 ", "").replace("📝 ", "").replace("📂 ", "")
                        for i in range(self.table.columnCount()-1)]  # Exclut la colonne Action
                writer.writerow(headers)
                
                # Données
                for row in range(self.table.rowCount()):
                    row_data = []
                    for col in range(self.table.columnCount()-1):  # Exclut la colonne Action
                        item = self.table.item(row, col)
                        row_data.append(item.text() if item else "")
                    
                    writer.writerow(row_data)
            
            self.show_success_message("Export réussi", f"Les activités ont été exportées vers:\n{file_path}")
            
        except Exception as e:
            self.show_error_message("Erreur d'export", f"Une erreur est survenue lors de l'export:\n{str(e)}")

    def import_from_csv(self):
        """Importe des activités depuis un fichier CSV"""
        try:
            file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
                self,
                "Importer des activités",
                "",
                "Fichiers CSV (*.csv);;Tous les fichiers (*)"
            )
            
            if not file_path:
                return
                
            # Vérification de confirmation
            reply = QtWidgets.QMessageBox.question(
                self,
                "Confirmation d'import",
                "Voulez-vous vraiment importer ces activités?\nCela écrasera les activités existantes.",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            
            if reply != QtWidgets.QMessageBox.Yes:
                return
            
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                headers = next(reader)  # Ligne d'en-tête
                
                # Vérification du format
                if len(headers) < 5:  # Adaptez selon vos colonnes
                    raise ValueError("Format de fichier invalide")
                
                # Nettoyage des tâches existantes
                self.clear_all_tasks()
                
                # Import des nouvelles tâches
                for row in reader:
                    if len(row) < 5:  # Vérification du nombre de colonnes
                        continue
                        
                    self.create_task_from_import(
                        name=row[0],
                        program=row[1],
                        days=row[2],
                        time=row[3],
                        date=row[4],
                        status=row[5] if len(row) > 5 else "▶️ Actif"
                    )
            
            self.show_success_message("Import réussi", "Les activités ont été importées avec succès!")
            self.load_activities()  # Recharge la table
            
        except Exception as e:
            self.show_error_message("Erreur d'import", f"Une erreur est survenue lors de l'import:\n{str(e)}")

    def clear_all_tasks(self):
        """Supprime toutes les tâches existantes"""
        try:
            # Récupère toutes les tâches
            result = subprocess.check_output("schtasks /query /fo csv /nh", shell=True, 
                                        encoding='utf-8', errors='ignore')
            lines = result.strip().splitlines()
            
            for line in lines:
                parts = [p.strip('"') for p in line.split(",")]
                if parts:  # Vérifie que la ligne n'est pas vide
                    task_name = parts[0].lstrip("\\").strip()
                    subprocess.run(f'schtasks /delete /tn "{task_name}" /f', shell=True)
                    
        except Exception as e:
            self.show_warning_message("Avertissement", 
                                    f"Certaines tâches n'ont pas pu être supprimées: {str(e)}")

    def create_task_from_import(self, name, program, days, time, date, status):
        """Crée une nouvelle tâche à partir des données importées"""
        try:
            folder_path = os.path.expanduser("~\\AppData\\Roaming\\Saadiya\\resources\\tools")
            program_path = os.path.join(folder_path, f"{program}.exe")
            
            if not os.path.exists(program_path):
                self.show_warning_message("Programme introuvable",
                                        f"Le programme {program} n'existe pas dans le dossier des outils")
                return
                
            # Construction de la commande schtasks
            if date and date.lower() not in ["n/a", "na", ""]:
                # Tâche avec date spécifique
                cmd = (f'schtasks /create /tn "{name}" /tr "{program_path}" '
                    f'/sc once /sd {date} /st {time} /f')
            else:
                # Tâche récurrente
                if days and days.lower() not in ["tous les jours", "daily"]:
                    # Hebdomadaire
                    cmd = (f'schtasks /create /tn "{name}" /tr "{program_path}" '
                        f'/sc weekly /d {days} /st {time} /f')
                else:
                    # Quotidienne
                    cmd = (f'schtasks /create /tn "{name}" /tr "{program_path}" '
                        f'/sc daily /st {time} /f')
            
            # Exécution de la commande
            subprocess.run(cmd, shell=True, check=True)
            
            # Gestion du statut (activé/désactivé)
            if "pause" in status.lower() or "⏸️" in status:
                subprocess.run(f'schtasks /change /tn "{name}" /disable', shell=True)
                
        except subprocess.CalledProcessError as e:
            self.show_warning_message("Erreur de création",
                                    f"La tâche {name} n'a pas pu être créée: {str(e)}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    # Set application style and palette
    app.setStyle("Fusion")
    
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QColor(245, 245, 245))
    palette.setColor(QtGui.QPalette.WindowText, QColor(44, 62, 80))
    palette.setColor(QtGui.QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QtGui.QPalette.AlternateBase, QColor(240, 248, 255))
    palette.setColor(QtGui.QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QtGui.QPalette.ToolTipText, QColor(44, 62, 80))
    palette.setColor(QtGui.QPalette.Text, QColor(44, 62, 80))
    palette.setColor(QtGui.QPalette.Button, QColor(52, 152, 219))
    palette.setColor(QtGui.QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QtGui.QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QtGui.QPalette.Highlight, QColor(52, 152, 219))
    palette.setColor(QtGui.QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    window = Activite()
    window.show()
    sys.exit(app.exec_())