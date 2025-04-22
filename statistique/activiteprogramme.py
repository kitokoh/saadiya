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
            button = QtWidgets.QPushButton("⚙️ Action")
            button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 15px;
                    padding: 5px 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            
            # Calculate button position
            button_rect = QRectF(
                option.rect.x() + (option.rect.width() - 100) / 2,
                option.rect.y() + (option.rect.height() - 30) / 2,
                100, 30
            )
            
            # Draw button
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing)
            
            if option.state & QtWidgets.QStyle.State_Selected:
                gradient = QLinearGradient(button_rect.topLeft(), button_rect.bottomLeft())
                gradient.setColorAt(0, QColor(76, 175, 80))
                gradient.setColorAt(1, QColor(56, 142, 60))
                painter.setBrush(gradient)
            else:
                painter.setBrush(QColor(76, 175, 80))
            
            painter.setPen(QPen(QColor(46, 125, 50), 1))
            painter.drawRoundedRect(button_rect, 15, 15)
            
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
        save_button = QtWidgets.QPushButton(self.tr("💾 Save Schedule"))
        save_button.setCursor(Qt.PointingHandCursor)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(3, 3)
        save_button.setGraphicsEffect(shadow)

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
        button_layout.addWidget(save_button)
        button_layout.addStretch()
        
        main_layout.addWidget(button_container)
        self.setLayout(main_layout)

        # Hide calendar by default
        self.calendar.setVisible(False)
        self.update_name()

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
        top_bar_layout.addWidget(self.export_button, 1)

        # Activities table with modern style
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            self.tr("🔢 #"), self.tr("📝 Name"), self.tr("📂 Program"), 
            self.tr("📅 Days"), self.tr("⏰ Time"), self.tr("📅 Date"), self.tr("⚙️ Action")
        ])
        
        # Customize table appearance
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #dfe6e9;
                border-radius: 8px;
                gridline-color: #dfe6e9;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 8px;
                border: none;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QScrollBar:vertical {
                border: none;
                background: #f5f5f5;
                width: 12px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #bdc3c7;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
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
                            QPushButton {
                                background-color: #3498db;
                                color: white;
                                border-radius: 15px;
                                padding: 5px 10px;
                                font-weight: bold;
                                min-width: 80px;
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

    def pause_selected_activities(self):
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