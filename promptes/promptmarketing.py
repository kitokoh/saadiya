import sys
import os
import sqlite3
import json
import time
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QTextEdit, QProgressBar, QScrollArea, 
                             QGroupBox, QCheckBox, QFileDialog, QMessageBox, QStackedWidget, 
                             QSizePolicy, QLineEdit, QGridLayout, QFrame, QSpacerItem)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QUrl, QSize, QRect, QPropertyAnimation, QEasingCurve, QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap, QTextCursor, QDesktopServices, QMovie, QPainter, QColor, QFont, QPalette
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QObject

class Constants:
    """Class to store application constants"""
    PRIMARY_COLOR = "#4f46e5"
    PRIMARY_HOVER = "#4338ca"
    BACKGROUND_COLOR = "#f8fafc"
    TEXT_COLOR = "#1e293b"
    TEXT_SECONDARY = "#64748b"
    SUCCESS_COLOR = "#10b981"
    ERROR_COLOR = "#ef4444"
    CARD_BG = "#f8fafc"
    CARD_BORDER = "#e2e8f0"
    WHATSAPP_GREEN = "#25D366"
    
    PLATFORM_ICONS = {
        'whatsapp': '💬',
        'instagram': '📸',
        'facebook': '👍',
        'linkedin': '💼',
        'tiktok': '🎵',
        'email': '✉️',
        'twitter': '🐦',
        'youtube': '▶️',
        'analytics': '📊',
        'seo': '🔍'
    }

class ActionHandler(QObject):
    """Handler for JavaScript to Python actions"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
    
    @pyqtSlot(str)
    def handleAction(self, action_data):
        """Handle actions sent from JavaScript"""
        try:
            data = json.loads(action_data)
            self.parent.execute_action(data)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
        except Exception as e:
            print(f"Error processing action: {e}")

class AnalysisThread(QThread):
    """Thread for asynchronous prompt analysis"""
    analysis_complete = pyqtSignal(str, list)
    error_occurred = pyqtSignal(str)
    progress_updated = pyqtSignal(int)

    def __init__(self, prompt_text, db_path):
        super().__init__()
        self.prompt_text = prompt_text
        self.db_path = db_path
        self._is_running = True

    def run(self):
        """Main execution of analysis thread"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Progress simulation
            for i in range(1, 101):
                if not self._is_running:
                    return
                time.sleep(0.02)
                self.progress_updated.emit(i)
            
            # Real analysis
            prompt_lower = self.prompt_text.lower()
            detected = []
            
            cursor.execute('SELECT keyword, platform, response_template, action_type FROM detection_rules')
            rules = cursor.fetchall()
            
            for keyword, platform, template, action_type in rules:
                if not self._is_running:
                    return
                if keyword in prompt_lower:
                    detected.append((keyword, platform, template, action_type))
            
            analysis_text = self.generate_analysis_html(prompt_lower, detected)
            self.analysis_complete.emit(analysis_text, detected)
            
        except sqlite3.Error as e:
            self.error_occurred.emit(self.tr("Database error: {}").format(str(e)))
        except Exception as e:
            self.error_occurred.emit(self.tr("Analysis error: {}").format(str(e)))
        finally:
            if conn:
                conn.close()

    def stop(self):
        """Stop the thread properly"""
        self._is_running = False
        self.wait()

    def generate_analysis_html(self, prompt, detected):
        """Generate HTML to display analysis results"""
        html = f"""
        <style>
            :root {{
                --primary: {Constants.PRIMARY_COLOR};
                --primary-hover: {Constants.PRIMARY_HOVER};
                --background: #ffffff;
                --text: {Constants.TEXT_COLOR};
                --text-secondary: {Constants.TEXT_SECONDARY};
                --card-bg: {Constants.CARD_BG};
                --card-border: {Constants.CARD_BORDER};
                --success: {Constants.SUCCESS_COLOR};
                --error: {Constants.ERROR_COLOR};
            }}
            
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: var(--background);
                color: var(--text);
                line-height: 1.5;
                padding: 0;
                margin: 0;
            }}
            
            .container {{
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            
            .platform-section {{
                margin-bottom: 1.5rem;
                background: var(--background);
                border-radius: 12px;
                border: 1px solid var(--card-border);
                overflow: hidden;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }}
            
            .platform-header {{
                padding: 1rem 1.5rem;
                background: var(--card-bg);
                border-bottom: 1px solid var(--card-border);
                display: flex;
                align-items: center;
            }}
            
            .platform-icon {{
                font-size: 1.5rem;
                margin-right: 0.75rem;
            }}
            
            .platform-title {{
                font-size: 1.125rem;
                font-weight: 600;
                margin: 0;
            }}
            
            .options-container {{
                padding: 1rem 1.5rem;
            }}
            
            .option-card {{
                padding: 1rem;
                margin-bottom: 0.75rem;
                background: var(--card-bg);
                border: 1px solid var(--card-border);
                border-radius: 8px;
                transition: all 0.2s ease;
                cursor: pointer;
            }}
            
            .option-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
                border-color: var(--primary);
            }}
            
            .option-title {{
                font-weight: 600;
                margin-bottom: 0.25rem;
            }}
            
            .option-desc {{
                color: var(--text-secondary);
                font-size: 0.875rem;
                margin-bottom: 0.75rem;
            }}
            
            .action-btn {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background: var(--primary);
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 6px;
                font-size: 0.875rem;
                font-weight: 500;
                cursor: pointer;
                transition: background 0.2s;
            }}
            
            .action-btn:hover {{
                background: var(--primary-hover);
            }}
            
            .keyword-tag {{
                display: inline-block;
                background: #e0e7ff;
                color: #4f46e5;
                padding: 0.25rem 0.5rem;
                border-radius: 4px;
                font-size: 0.75rem;
                margin-right: 0.5rem;
                margin-bottom: 0.5rem;
            }}
        </style>
        
        <div class="container">
            <h1 style="font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;">✨ {self.tr("Suggestions")}</h1>
            <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">{self.tr("Here's what I can do for you:")}</p>
        """
        
        if not detected:
            html += f"""
            <div class="platform-section">
                <div class="platform-header">
                    <div class="platform-icon">💡</div>
                    <h2 class="platform-title">{self.tr("General Advice")}</h2>
                </div>
                <div class="options-container">
                    <p style="margin-bottom: 1rem;">{self.tr("I didn't detect a specific request. Here are some suggestions:")}</p>
                    <button class="action-btn" onclick='pyHandler.handleAction(`{{"type":"general_advice"}}`)'>
                        {self.tr("Show marketing tips")}
                    </button>
                </div>
            </div>
            """
        else:
            platforms = {}
            for item in detected:
                platform = item[1]
                if platform not in platforms:
                    platforms[platform] = []
                platforms[platform].append(item)
            
            for platform, items in platforms.items():
                icon = Constants.PLATFORM_ICONS.get(platform, '📌')
                
                html += f"""
                <div class="platform-section">
                    <div class="platform-header">
                        <div class="platform-icon">{icon}</div>
                        <h2 class="platform-title">{platform.capitalize()}</h2>
                    </div>
                    <div class="options-container">
                """
                
                for idx, (keyword, platform, template, action_type) in enumerate(items):
                    html += f"""
                    <div class="option-card" onclick='pyHandler.handleAction(`{{
                        "type": "platform_action",
                        "platform": "{platform}",
                        "action": "{action_type}"
                    }}`)'>
                        <div class="option-title">{template}</div>
                        <div class="option-desc">{self.tr("Based on your mention:")} <span class="keyword-tag">{keyword}</span></div>
                        <button class="action-btn">
                            {self.tr("Execute this action")}
                        </button>
                    </div>
                    """
                
                html += """
                    </div>
                </div>
                """
        
        html += "</div>"
        return html

class MarketingAIAnalyzer(QMainWindow):
    """Main application window"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Leopardo - AI Marketing Assistant"))
        self.setMinimumSize(1000, 700)
        
        # Configuration
        self.current_user = self.tr("User")
        self.settings = {
            "dark_mode": False,
            "animations": True
        }
        
        # Initialization
        self.init_db()
        self.init_ui()
        self.setup_connections()
        
    def init_db(self):
        """Initialize database with complete dataset"""
        from imports import DB_PATH_prompt_command
        self.db_path = DB_PATH_prompt_command
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detection_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                platform TEXT NOT NULL,
                response_template TEXT NOT NULL,
                action_type TEXT NOT NULL
            )
        ''')
        
        # Check existing data
        cursor.execute("SELECT COUNT(*) FROM detection_rules")
        if cursor.fetchone()[0] == 0:
            # Insert complete dataset
            rules = [
                # WhatsApp
                ("whatsapp", "whatsapp", self.tr("Complete WhatsApp automation"), "whatsapp_auto"),
                ("whatsapp message", "whatsapp", self.tr("Send personal WhatsApp message"), "whatsapp_personal"),
                ("whatsapp group", "whatsapp", self.tr("Send message to WhatsApp group"), "whatsapp_group"),
                ("whatsapp campaign", "whatsapp", self.tr("Launch WhatsApp campaign"), "whatsapp_campaign"),
                ("automate whatsapp", "whatsapp", self.tr("Automate WhatsApp replies"), "whatsapp_auto_reply"),
                
                # Instagram
                ("instagram", "instagram", self.tr("Create Instagram post"), "instagram_post"),
                ("instagram story", "instagram", self.tr("Create Instagram story"), "instagram_story"),
                ("instagram reels", "instagram", self.tr("Create Instagram Reel"), "instagram_reel"),
                ("instagram campaign", "instagram", self.tr("Launch Instagram ad campaign"), "instagram_ads"),
                ("instagram hashtag", "instagram", self.tr("Generate optimized hashtags"), "instagram_hashtags"),
                
                # Facebook
                ("facebook", "facebook", self.tr("Create Facebook post"), "facebook_post"),
                ("facebook ad", "facebook", self.tr("Launch Facebook ad"), "facebook_ads"),
                ("facebook page", "facebook", self.tr("Optimize your Facebook page"), "facebook_page"),
                
                # Other platforms
                ("linkedin", "linkedin", self.tr("Create LinkedIn post"), "linkedin_post"),
                ("tiktok", "tiktok", self.tr("Create TikTok video"), "tiktok_video"),
                ("youtube", "youtube", self.tr("Optimize YouTube video"), "youtube_optimize"),
                ("email", "email", self.tr("Create email campaign"), "email_campaign"),
                ("newsletter", "email", self.tr("Create newsletter"), "email_newsletter"),
                
                # General
                ("strategy", "general", self.tr("Develop marketing strategy"), "marketing_strategy"),
                ("analysis", "analytics", self.tr("Analyze performance"), "performance_analysis"),
                ("seo", "seo", self.tr("SEO optimization"), "seo_optimization"),
                ("content", "content", self.tr("Plan content"), "content_planning")
            ]
            
            cursor.executemany('''
                INSERT INTO detection_rules (keyword, platform, response_template, action_type)
                VALUES (?, ?, ?, ?)
            ''', rules)
            conn.commit()
        
        conn.close()
        
    def init_ui(self):
        """Initialize user interface with modern design"""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Content area
        self.content_area = QWidget()
        self.content_area.setObjectName("contentArea")
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Stack for different views
        self.stacked_widget = QStackedWidget()
        self.content_layout.addWidget(self.stacked_widget)
        
        # Main view
        self.setup_main_view()
        
        self.main_layout.addWidget(self.content_area)
        
        # Apply global style
        self.update_styles()
        
    def setup_main_view(self):
        """Configure main view with optimized UX"""
        main_view = QWidget()
        main_view.setObjectName("mainView")
        layout = QVBoxLayout(main_view)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(0)
        
        # Center container
        center_container = QWidget()
        center_container.setMaximumWidth(800)
        center_layout = QVBoxLayout(center_container)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        
        # Header
        header = QLabel(self.tr("Hello, I'm the Leopardo assistant"))
        header.setObjectName("mainHeader")
        
        subheader = QLabel(self.tr("Describe your marketing need to get customized solutions"))
        subheader.setObjectName("mainSubheader")
        
        # Unified prompt area with button
        prompt_container = QWidget()
        prompt_container.setObjectName("promptContainer")
        prompt_layout = QVBoxLayout(prompt_container)
        prompt_layout.setContentsMargins(0, 0, 0, 0)
        prompt_layout.setSpacing(0)
        
        # Text area with styled placeholder
        self.prompt_input = QTextEdit()
        self.prompt_input.setObjectName("promptInput")
        self.prompt_input.setPlaceholderText(self.tr("Ex: I want to automate my WhatsApp posts for my clothing business..."))
        
        # Integrated send button
        self.send_btn = QPushButton(self.tr("Analyze"))
        self.send_btn.setObjectName("sendButton")
        self.send_btn.setIcon(QIcon.fromTheme("edit-find"))
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        
        # Prompt suggestions
        self.setup_prompt_suggestions()
        
        # Results area
        self.analysis_display = QWebEngineView()
        self.analysis_display.setObjectName("analysisDisplay")
        self.analysis_display.hide()
        
        # Communication channel setup
        self.channel = QWebChannel()
        self.handler = ActionHandler(self)
        self.channel.registerObject('pyHandler', self.handler)
        self.analysis_display.page().setWebChannel(self.channel)
        
        # Spacing to center content
        self.top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        # Component assembly
        prompt_layout.addWidget(self.prompt_input)
        prompt_layout.addWidget(self.send_btn, alignment=Qt.AlignRight)
        prompt_layout.addWidget(self.progress_bar)
        
        center_layout.addItem(self.top_spacer)
        center_layout.addWidget(header)
        center_layout.addWidget(subheader)
        center_layout.addSpacing(20)
        center_layout.addWidget(prompt_container)
        center_layout.addSpacing(15)
        center_layout.addLayout(self.suggestions_layout)
        center_layout.addSpacing(20)
        center_layout.addWidget(self.analysis_display)
        center_layout.addItem(self.bottom_spacer)
        
        layout.addWidget(center_container, alignment=Qt.AlignCenter)
        
        self.stacked_widget.addWidget(main_view)
        
    def setup_connections(self):
        """Configure signal and slot connections"""
        self.send_btn.clicked.connect(self.analyze_prompt)
        
    def setup_prompt_suggestions(self):
        """Configure predefined prompt suggestions"""
        self.suggestions_layout = QVBoxLayout()
        self.suggestions_layout.setContentsMargins(0, 0, 0, 0)
        self.suggestions_layout.setSpacing(10)
        
        title = QLabel("💡 " + self.tr("Example queries:"))
        title.setObjectName("suggestionsTitle")
        
        suggestions_grid = QGridLayout()
        suggestions_grid.setContentsMargins(0, 0, 0, 0)
        suggestions_grid.setSpacing(10)
        
        suggestions = [
            ("📱", self.tr("Social media"), self.tr("Create a strategy for Instagram and Facebook")),
            ("📈", self.tr("Analysis"), self.tr("Analyze performance of my last campaign")),
            ("✉️", self.tr("Email"), self.tr("Write a newsletter for my clients")),
            ("💬", self.tr("WhatsApp"), self.tr("Automate WhatsApp messages for my business")),
            ("🔍", self.tr("SEO"), self.tr("Optimize my website for search engines")),
            ("📊", self.tr("Report"), self.tr("Generate monthly marketing report"))
        ]
        
        for i, (icon, title_text, prompt_text) in enumerate(suggestions):
            btn = QPushButton(f"{icon} {title_text}")
            btn.setToolTip(prompt_text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setObjectName("suggestionButton")
            btn.clicked.connect(lambda _, text=prompt_text: self.prompt_input.setPlainText(text))
            suggestions_grid.addWidget(btn, i // 2, i % 2)
        
        self.suggestions_layout.addWidget(title)
        self.suggestions_layout.addLayout(suggestions_grid)
        
    def update_styles(self):
        """Apply CSS styles to the application"""
        self.setStyleSheet(f"""
            QWidget {{
                font-family: 'Segoe UI', sans-serif;
            }}
            
            QWidget#contentArea {{
                background: {Constants.BACKGROUND_COLOR};
            }}
            
            QLabel#mainHeader {{
                font-size: 28px;
                font-weight: bold;
                color: {Constants.TEXT_COLOR};
                margin-bottom: 5px;
            }}
            
            QLabel#mainSubheader {{
                font-size: 16px;
                color: {Constants.TEXT_SECONDARY};
                margin-bottom: 30px;
            }}
            
            QWidget#promptContainer {{
                background: white;
                border-radius: 12px;
                border: 1px solid {Constants.CARD_BORDER};
                padding: 1px;
            }}
            
            QTextEdit#promptInput {{
                background: white;
                border: none;
                font-size: 16px;
                padding: 20px;
                border-radius: 12px;
                min-height: 120px;
                color: {Constants.TEXT_COLOR};
            }}
            
            QTextEdit#promptInput:focus {{
                border: none;
            }}
            
            QPushButton#sendButton {{
                background: {Constants.PRIMARY_COLOR};
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                margin: 10px;
                margin-top: 0;
            }}
            
            QPushButton#sendButton:hover {{
                background: {Constants.PRIMARY_HOVER};
            }}
            
            QPushButton#sendButton:disabled {{
                background: #a5b4fc;
            }}
            
            QProgressBar#progressBar {{
                height: 6px;
                background: #e2e8f0;
                border-radius: 3px;
                margin: 0 10px 10px 10px;
            }}
            
            QProgressBar#progressBar::chunk {{
                background: {Constants.PRIMARY_COLOR};
                border-radius: 3px;
            }}
            
            QLabel#suggestionsTitle {{
                font-size: 14px;
                color: {Constants.TEXT_SECONDARY};
                margin-bottom: 5px;
            }}
            
            QPushButton#suggestionButton {{
                background: white;
                border: 1px solid {Constants.CARD_BORDER};
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                text-align: left;
                color: {Constants.TEXT_COLOR};
            }}
            
            QPushButton#suggestionButton:hover {{
                background: #f1f5f9;
                border-color: #cbd5e1;
            }}
            
            QWebEngineView#analysisDisplay {{
                background: white;
                border-radius: 12px;
                border: 1px solid {Constants.CARD_BORDER};
                min-height: 300px;
            }}
        """)
        
    def analyze_prompt(self):
        """Start prompt analysis"""
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            self.show_error(self.tr("Please enter your request"))
            return
        
        # Disable button during analysis
        self.send_btn.setEnabled(False)
        self.progress_bar.show()
        self.analysis_display.hide()
        
        # Adjust spacing to center content
        self.top_spacer.changeSize(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        # Loading animation
        self.loading_animation = QPropertyAnimation(self.progress_bar, b"value")
        self.loading_animation.setDuration(2000)
        self.loading_animation.setStartValue(0)
        self.loading_animation.setEndValue(100)
        self.loading_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.loading_animation.start()
        
        # Launch analysis in separate thread
        self.analysis_thread = AnalysisThread(prompt, self.db_path)
        self.analysis_thread.analysis_complete.connect(self.show_results)
        self.analysis_thread.error_occurred.connect(self.show_error)
        self.analysis_thread.progress_updated.connect(self.progress_bar.setValue)
        self.analysis_thread.start()
        
    def show_results(self, html, detected_platforms):
        """Show analysis results"""
        self.send_btn.setEnabled(True)
        self.progress_bar.hide()
        self.analysis_display.setHtml(html)
        self.analysis_display.show()
        
        # Adjust spacings
        self.top_spacer.changeSize(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.bottom_spacer.changeSize(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        # Fade animation
        fade_in = QPropertyAnimation(self.analysis_display, b"windowOpacity")
        fade_in.setDuration(300)
        fade_in.setStartValue(0)
        fade_in.setEndValue(1)
        fade_in.start()
        
    def show_error(self, message):
        """Show error message"""
        self.send_btn.setEnabled(True)
        self.progress_bar.hide()
        self.analysis_display.setHtml(f"""
            <div style="padding: 20px; font-family: 'Segoe UI', sans-serif;">
                <h3 style="color: {Constants.ERROR_COLOR};">❌ {self.tr("Error")}</h3>
                <p style="color: {Constants.TEXT_SECONDARY};">{message}</p>
            </div>
        """)
        self.analysis_display.show()
        
    def execute_action(self, action_data):
        """Execute specific action"""
        try:
            action_type = action_data.get("type")
            
            if action_type == "platform_action":
                platform = action_data.get("platform")
                action = action_data.get("action")
                
                if platform == "whatsapp":
                    self.handle_whatsapp_action(action)
                elif platform == "instagram":
                    self.handle_instagram_action(action)
                # Add other platforms here...
                
        except Exception as e:
            print(f"Execution error: {e}")
            
    def handle_whatsapp_action(self, action):
        """Handle WhatsApp actions"""
        if action == "whatsapp_personal":
            self.show_whatsapp_personal_ui()
        elif action == "whatsapp_group":
            self.show_whatsapp_group_ui()
        else:
            self.show_whatsapp_general_ui()
            
    def show_whatsapp_personal_ui(self):
        """Show UI for personal WhatsApp messages"""
        html = f"""
        <div style="padding: 20px; font-family: 'Segoe UI', sans-serif;">
            <h2 style="color: {Constants.TEXT_COLOR}; margin-bottom: 20px;">💬 {self.tr("Personal WhatsApp Message")}</h2>
            
            <div style="background: {Constants.CARD_BG}; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
                <h3 style="color: {Constants.TEXT_COLOR}; margin-bottom: 15px;">📋 {self.tr("Message Settings")}</h3>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; color: {Constants.TEXT_SECONDARY}; margin-bottom: 8px;">{self.tr("Message type:")}</label>
                    <select style="width: 100%; padding: 10px; border-radius: 6px; border: 1px solid {Constants.CARD_BORDER};">
                        <option>{self.tr("Standard message")}</option>
                        <option>{self.tr("Message with image")}</option>
                        <option>{self.tr("Message with document")}</option>
                    </select>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; color: {Constants.TEXT_SECONDARY}; margin-bottom: 8px;">{self.tr("Message content:")}</label>
                    <textarea style="width: 100%; height: 100px; padding: 10px; border-radius: 6px; border: 1px solid {Constants.CARD_BORDER};"></textarea>
                </div>
            </div>
            
            <button style="background: {Constants.WHATSAPP_GREEN}; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-size: 16px; cursor: pointer;"
                    onclick="pyHandler.handleAction(`{{'type':'whatsapp_send','message_type':'personal'}}`)">
                {self.tr("Send message")}
            </button>
        </div>
        """
        self.analysis_display.setHtml(html)
        
    def show_whatsapp_group_ui(self):
        """Show UI for WhatsApp group messages"""
        html = f"""
        <div style="padding: 20px; font-family: 'Segoe UI', sans-serif;">
            <h2 style="color: {Constants.TEXT_COLOR}; margin-bottom: 20px;">👥 {self.tr("WhatsApp Group Message")}</h2>
            
            <div style="background: {Constants.CARD_BG}; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
                <h3 style="color: {Constants.TEXT_COLOR}; margin-bottom: 15px;">📋 {self.tr("Group Selection")}</h3>
                
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 15px;">
                    <label style="display: flex; align-items: center; padding: 10px; background: white; border-radius: 6px; border: 1px solid {Constants.CARD_BORDER};">
                        <input type="checkbox" style="margin-right: 8px;"> {self.tr("Clients group")}
                    </label>
                    <label style="display: flex; align-items: center; padding: 10px; background: white; border-radius: 6px; border: 1px solid {Constants.CARD_BORDER};">
                        <input type="checkbox" style="margin-right: 8px;"> {self.tr("Suppliers group")}
                    </label>
                    <label style="display: flex; align-items: center; padding: 10px; background: white; border-radius: 6px; border: 1px solid {Constants.CARD_BORDER};">
                        <input type="checkbox" style="margin-right: 8px;"> {self.tr("Team group")}
                    </label>
                    <label style="display: flex; align-items: center; padding: 10px; background: white; border-radius: 6px; border: 1px solid {Constants.CARD_BORDER};">
                        <input type="checkbox" style="margin-right: 8px;"> {self.tr("VIP group")}
                    </label>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; color: {Constants.TEXT_SECONDARY}; margin-bottom: 8px;">{self.tr("Message content:")}</label>
                    <textarea style="width: 100%; height: 100px; padding: 10px; border-radius: 6px; border: 1px solid {Constants.CARD_BORDER};"></textarea>
                </div>
                
                <div style="display: flex; gap: 10px;">
                    <button style="flex: 1; background: white; border: 1px solid {Constants.CARD_BORDER}; padding: 10px; border-radius: 6px; cursor: pointer;">
                        {self.tr("Add attachment")}
                    </button>
                    <button style="flex: 1; background: white; border: 1px solid {Constants.CARD_BORDER}; padding: 10px; border-radius: 6px; cursor: pointer;">
                        {self.tr("Preview")}
                    </button>
                </div>
            </div>
            
            <button style="background: {Constants.WHATSAPP_GREEN}; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-size: 16px; cursor: pointer;"
                    onclick="pyHandler.handleAction(`{{'type':'whatsapp_send','message_type':'group'}}`)">
                {self.tr("Send to selected groups")}
            </button>
        </div>
        """
        self.analysis_display.setHtml(html)
        
    def show_whatsapp_general_ui(self):
        """Show general WhatsApp UI"""
        html = f"""
        <div style="padding: 20px; font-family: 'Segoe UI', sans-serif;">
            <h2 style="color: {Constants.TEXT_COLOR}; margin-bottom: 20px;">📱 {self.tr("WhatsApp Automation")}</h2>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 20px;">
                <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 20px; cursor: pointer;"
                     onclick="pyHandler.handleAction(`{{'type':'whatsapp_action','action':'personal'}}`)">
                    <h3 style="color: #166534; margin-bottom: 10px;">💬 {self.tr("Personal messages")}</h3>
                    <p style="color: {Constants.TEXT_SECONDARY};">{self.tr("Send individual messages to your contacts")}</p>
                </div>
                
                <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 20px; cursor: pointer;"
                     onclick="pyHandler.handleAction(`{{'type':'whatsapp_action','action':'group'}}`)">
                    <h3 style="color: #075985; margin-bottom: 10px;">👥 {self.tr("Group messages")}</h3>
                    <p style="color: {Constants.TEXT_SECONDARY};">{self.tr("Send messages to multiple groups")}</p>
                </div>
                
                <div style="background: #f5f3ff; border: 1px solid #ddd6fe; border-radius: 8px; padding: 20px; cursor: pointer;"
                     onclick="pyHandler.handleAction(`{{'type':'whatsapp_action','action':'auto_reply'}}`)">
                    <h3 style="color: #6d28d9; margin-bottom: 10px;">🤖 {self.tr("Auto replies")}</h3>
                    <p style="color: {Constants.TEXT_SECONDARY};">{self.tr("Configure automatic replies")}</p>
                </div>
                
                <div style="background: #fff7ed; border: 1px solid #fed7aa; border-radius: 8px; padding: 20px; cursor: pointer;"
                     onclick="pyHandler.handleAction(`{{'type':'whatsapp_action','action':'campaign'}}`)">
                    <h3 style="color: #9a3412; margin-bottom: 10px;">📢 {self.tr("Campaign")}</h3>
                    <p style="color: {Constants.TEXT_SECONDARY};">{self.tr("Launch WhatsApp campaign")}</p>
                </div>
            </div>
            
            <div style="background: {Constants.CARD_BG}; border-radius: 8px; padding: 20px;">
                <h3 style="color: {Constants.TEXT_COLOR}; margin-bottom: 15px;">📊 {self.tr("Recent statistics")}</h3>
                
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 15px;">
                    <div style="background: white; border-radius: 6px; padding: 15px; text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: {Constants.PRIMARY_COLOR};">42</div>
                        <div style="color: {Constants.TEXT_SECONDARY}; font-size: 14px;">{self.tr("Messages sent")}</div>
                    </div>
                    <div style="background: white; border-radius: 6px; padding: 15px; text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: {Constants.SUCCESS_COLOR};">78%</div>
                        <div style="color: {Constants.TEXT_SECONDARY}; font-size: 14px;">{self.tr("Read rate")}</div>
                    </div>
                    <div style="background: white; border-radius: 6px; padding: 15px; text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: {Constants.ERROR_COLOR};">12</div>
                        <div style="color: {Constants.TEXT_SECONDARY}; font-size: 14px;">{self.tr("Blocked contacts")}</div>
                    </div>
                </div>
                
                <button style="background: {Constants.PRIMARY_COLOR}; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer;">
                    {self.tr("View full report")}
                </button>
            </div>
        </div>
        """
        self.analysis_display.setHtml(html)

    def closeEvent(self, event):
        """Handle application closing"""
        if hasattr(self, 'analysis_thread') and self.analysis_thread.isRunning():
            self.analysis_thread.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Set color palette for modern look
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(248, 250, 252))
    palette.setColor(QPalette.WindowText, QColor(30, 41, 59))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(243, 244, 246))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(30, 41, 59))
    palette.setColor(QPalette.Text, QColor(30, 41, 59))
    palette.setColor(QPalette.Button, QColor(226, 232, 240))
    palette.setColor(QPalette.ButtonText, QColor(30, 41, 59))
    palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.Highlight, QColor(79, 70, 229))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    # Set default fonts
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = MarketingAIAnalyzer()
    window.show()
    
    sys.exit(app.exec_())