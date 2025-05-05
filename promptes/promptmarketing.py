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

class ActionHandler(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
    
    @pyqtSlot(str)
    def handleAction(self, action_data):
        try:
            data = json.loads(action_data)
            self.parent.execute_action(data)
        except Exception as e:
            print(f"Error handling action: {e}")

class AnalysisThread(QThread):
    analysis_complete = pyqtSignal(str, list)
    error_occurred = pyqtSignal(str)
    progress_updated = pyqtSignal(int)

    def __init__(self, prompt_text, db_path):
        super().__init__()
        self.prompt_text = prompt_text
        self.db_path = db_path
        self._is_running = True

    def run(self):
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
            
        except Exception as e:
            self.error_occurred.emit(f"Analysis error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def generate_analysis_html(self, prompt, detected):
        html = """
        <style>
            :root {
                --primary: #4f46e5;
                --primary-hover: #4338ca;
                --background: #ffffff;
                --text: #1e293b;
                --text-secondary: #64748b;
                --card-bg: #f8fafc;
                --card-border: #e2e8f0;
                --success: #10b981;
                --error: #ef4444;
            }
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: var(--background);
                color: var(--text);
                line-height: 1.5;
                padding: 0;
                margin: 0;
            }
            
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            
            .platform-section {
                margin-bottom: 1.5rem;
                background: var(--background);
                border-radius: 12px;
                border: 1px solid var(--card-border);
                overflow: hidden;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }
            
            .platform-header {
                padding: 1rem 1.5rem;
                background: var(--card-bg);
                border-bottom: 1px solid var(--card-border);
                display: flex;
                align-items: center;
            }
            
            .platform-icon {
                font-size: 1.5rem;
                margin-right: 0.75rem;
            }
            
            .platform-title {
                font-size: 1.125rem;
                font-weight: 600;
                margin: 0;
            }
            
            .options-container {
                padding: 1rem 1.5rem;
            }
            
            .option-card {
                padding: 1rem;
                margin-bottom: 0.75rem;
                background: var(--card-bg);
                border: 1px solid var(--card-border);
                border-radius: 8px;
                transition: all 0.2s ease;
                cursor: pointer;
            }
            
            .option-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
                border-color: var(--primary);
            }
            
            .option-title {
                font-weight: 600;
                margin-bottom: 0.25rem;
            }
            
            .option-desc {
                color: var(--text-secondary);
                font-size: 0.875rem;
                margin-bottom: 0.75rem;
            }
            
            .action-btn {
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
            }
            
            .action-btn:hover {
                background: var(--primary-hover);
            }
            
            .keyword-tag {
                display: inline-block;
                background: #e0e7ff;
                color: #4f46e5;
                padding: 0.25rem 0.5rem;
                border-radius: 4px;
                font-size: 0.75rem;
                margin-right: 0.5rem;
                margin-bottom: 0.5rem;
            }
        </style>
        
        <div class="container">
            <h1 style="font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;">✨ Suggestions</h1>
            <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">Here's what I can do for you:</p>
        """
        
        if not detected:
            html += """
            <div class="platform-section">
                <div class="platform-header">
                    <div class="platform-icon">💡</div>
                    <h2 class="platform-title">General Advice</h2>
                </div>
                <div class="options-container">
                    <p style="margin-bottom: 1rem;">I didn't detect a specific request. Here are some suggestions:</p>
                    <button class="action-btn" onclick='pyHandler.handleAction(`{"type":"general_advice"}`)'>
                        Show marketing tips
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
                icon = {
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
                }.get(platform, '📌')
                
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
                        <div class="option-desc">Based on your mention: <span class="keyword-tag">{keyword}</span></div>
                        <button class="action-btn">
                            Execute this action
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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Leopardo - AI Marketing Assistant")
        self.setMinimumSize(1000, 700)
        
        # Configuration
        self.current_user = "User"
        self.settings = {
            "dark_mode": False,
            "animations": True
        }
        
        # Initialization
        self.init_db()
        self.init_ui()
        
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
        
        # Check for existing data
        cursor.execute("SELECT COUNT(*) FROM detection_rules")
        if cursor.fetchone()[0] == 0:
            # Insert complete dataset
            rules = [
                # WhatsApp
                ("whatsapp", "whatsapp", "Complete WhatsApp automation", "whatsapp_auto"),
                ("whatsapp message", "whatsapp", "Send personal WhatsApp message", "whatsapp_personal"),
                ("whatsapp group", "whatsapp", "Send message to WhatsApp group", "whatsapp_group"),
                ("whatsapp campaign", "whatsapp", "Launch WhatsApp campaign", "whatsapp_campaign"),
                ("automate whatsapp", "whatsapp", "Automate WhatsApp replies", "whatsapp_auto_reply"),
                
                # Instagram
                ("instagram", "instagram", "Create Instagram post", "instagram_post"),
                ("instagram story", "instagram", "Create Instagram story", "instagram_story"),
                ("instagram reels", "instagram", "Create Instagram Reel", "instagram_reel"),
                ("instagram campaign", "instagram", "Launch Instagram ad campaign", "instagram_ads"),
                ("instagram hashtag", "instagram", "Generate optimized hashtags", "instagram_hashtags"),
                
                # Facebook
                ("facebook", "facebook", "Create Facebook post", "facebook_post"),
                ("facebook ad", "facebook", "Launch Facebook ad", "facebook_ads"),
                ("facebook page", "facebook", "Optimize your Facebook page", "facebook_page"),
                
                # Other platforms
                ("linkedin", "linkedin", "Create LinkedIn post", "linkedin_post"),
                ("tiktok", "tiktok", "Create TikTok video", "tiktok_video"),
                ("youtube", "youtube", "Optimize YouTube video", "youtube_optimize"),
                ("email", "email", "Create email campaign", "email_campaign"),
                ("newsletter", "email", "Create newsletter", "email_newsletter"),
                
                # General
                ("strategy", "general", "Develop marketing strategy", "marketing_strategy"),
                ("analysis", "analytics", "Analyze performance", "performance_analysis"),
                ("seo", "seo", "SEO optimization", "seo_optimization"),
                ("content", "content", "Plan content", "content_planning")
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
        header = QLabel("AI Marketing Assistant")
        header.setObjectName("mainHeader")
        
        subheader = QLabel("Describe your marketing need to get customized solutions")
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
        self.prompt_input.setPlaceholderText("Ex: I want to automate my WhatsApp posts for my clothing business...")
        
        # Integrated send button
        self.send_btn = QPushButton("Analyze")
        self.send_btn.setObjectName("sendButton")
        self.send_btn.setIcon(QIcon.fromTheme("edit-find"))
        self.send_btn.clicked.connect(self.analyze_prompt)
        
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
        
        # Spacer to push content up
        self.top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        # Spacer to center content
        self.bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        # Assemble components
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
        
    def setup_prompt_suggestions(self):
        """Configure predefined prompt suggestions"""
        self.suggestions_layout = QVBoxLayout()
        self.suggestions_layout.setContentsMargins(0, 0, 0, 0)
        self.suggestions_layout.setSpacing(10)
        
        title = QLabel("💡 Example queries:")
        title.setObjectName("suggestionsTitle")
        
        suggestions_grid = QGridLayout()
        suggestions_grid.setContentsMargins(0, 0, 0, 0)
        suggestions_grid.setSpacing(10)
        
        suggestions = [
            ("📱", "Social media", "Create a strategy for Instagram and Facebook"),
            ("📈", "Analysis", "Analyze performance of my last campaign"),
            ("✉️", "Email", "Write a newsletter for my clients"),
            ("💬", "WhatsApp", "Automate WhatsApp messages for my business"),
            ("🔍", "SEO", "Optimize my website for search engines"),
            ("📊", "Report", "Generate monthly marketing report")
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
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', sans-serif;
            }
            
            QWidget#contentArea {
                background: #f8fafc;
            }
            
            QLabel#mainHeader {
                font-size: 28px;
                font-weight: bold;
                color: #1e293b;
                margin-bottom: 5px;
            }
            
            QLabel#mainSubheader {
                font-size: 16px;
                color: #64748b;
                margin-bottom: 30px;
            }
            
            QWidget#promptContainer {
                background: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                padding: 1px;
            }
            
            QTextEdit#promptInput {
                background: white;
                border: none;
                font-size: 16px;
                padding: 20px;
                border-radius: 12px;
                min-height: 120px;
                color: #1e293b;
            }
            
            QTextEdit#promptInput:focus {
                border: none;
            }
            
            QPushButton#sendButton {
                background: #4f46e5;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                margin: 10px;
                margin-top: 0;
            }
            
            QPushButton#sendButton:hover {
                background: #4338ca;
            }
            
            QPushButton#sendButton:disabled {
                background: #a5b4fc;
            }
            
            QProgressBar#progressBar {
                height: 6px;
                background: #e2e8f0;
                border-radius: 3px;
                margin: 0 10px 10px 10px;
            }
            
            QProgressBar#progressBar::chunk {
                background: #4f46e5;
                border-radius: 3px;
            }
            
            QLabel#suggestionsTitle {
                font-size: 14px;
                color: #64748b;
                margin-bottom: 5px;
            }
            
            QPushButton#suggestionButton {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                text-align: left;
                color: #1e293b;
            }
            
            QPushButton#suggestionButton:hover {
                background: #f1f5f9;
                border-color: #cbd5e1;
            }
            
            QWebEngineView#analysisDisplay {
                background: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                min-height: 300px;
            }
        """)
        
    def analyze_prompt(self):
        """Start prompt analysis"""
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            self.show_error("Please enter your request")
            return
        
        # Disable button during analysis
        self.send_btn.setEnabled(False)
        self.progress_bar.show()
        self.analysis_display.hide()
        
        # Adjust spacer to center content
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
        
        # Adjust spacers to push content up
        self.top_spacer.changeSize(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.bottom_spacer.changeSize(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        # Fade-in animation
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
                <h3 style="color: #ef4444;">❌ Error</h3>
                <p style="color: #64748b;">{message}</p>
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
            <h2 style="color: #1e293b; margin-bottom: 20px;">💬 Personal WhatsApp Message</h2>
            
            <div style="background: #f8fafc; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
                <h3 style="color: #1e293b; margin-bottom: 15px;">📋 Message Settings</h3>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; color: #64748b; margin-bottom: 8px;">Message Type:</label>
                    <select style="width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #e2e8f0;">
                        <option>Standard message</option>
                        <option>Message with image</option>
                        <option>Message with document</option>
                    </select>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; color: #64748b; margin-bottom: 8px;">Message Content:</label>
                    <textarea style="width: 100%; height: 100px; padding: 10px; border-radius: 6px; border: 1px solid #e2e8f0;"></textarea>
                </div>
            </div>
            
            <button style="background: #25D366; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-size: 16px; cursor: pointer;"
                    onclick="pyHandler.handleAction(`{{'type':'whatsapp_send','message_type':'personal'}}`)">
                Send Message
            </button>
        </div>
        """
        self.analysis_display.setHtml(html)
        
    def show_whatsapp_group_ui(self):
        """Show UI for WhatsApp group messages"""
        html = f"""
        <div style="padding: 20px; font-family: 'Segoe UI', sans-serif;">
            <h2 style="color: #1e293b; margin-bottom: 20px;">👥 WhatsApp Group Message</h2>
            
            <div style="background: #f8fafc; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
                <h3 style="color: #1e293b; margin-bottom: 15px;">📋 Group Selection</h3>
                
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 15px;">
                    <label style="display: flex; align-items: center; padding: 10px; background: white; border-radius: 6px; border: 1px solid #e2e8f0;">
                        <input type="checkbox" style="margin-right: 8px;"> Client Group
                    </label>
                    <label style="display: flex; align-items: center; padding: 10px; background: white; border-radius: 6px; border: 1px solid #e2e8f0;">
                        <input type="checkbox" style="margin-right: 8px;"> Supplier Group
                    </label>
                    <label style="display: flex; align-items: center; padding: 10px; background: white; border-radius: 6px; border: 1px solid #e2e8f0;">
                        <input type="checkbox" style="margin-right: 8px;"> Team Group
                    </label>
                    <label style="display: flex; align-items: center; padding: 10px; background: white; border-radius: 6px; border: 1px solid #e2e8f0;">
                        <input type="checkbox" style="margin-right: 8px;"> VIP Group
                    </label>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; color: #64748b; margin-bottom: 8px;">Message Content:</label>
                    <textarea style="width: 100%; height: 100px; padding: 10px; border-radius: 6px; border: 1px solid #e2e8f0;"></textarea>
                </div>
                
                <div style="display: flex; gap: 10px;">
                    <button style="flex: 1; background: white; border: 1px solid #e2e8f0; padding: 10px; border-radius: 6px; cursor: pointer;">
                        Add Attachment
                    </button>
                    <button style="flex: 1; background: white; border: 1px solid #e2e8f0; padding: 10px; border-radius: 6px; cursor: pointer;">
                        Preview
                    </button>
                </div>
            </div>
            
            <button style="background: #25D366; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-size: 16px; cursor: pointer;"
                    onclick="pyHandler.handleAction(`{{'type':'whatsapp_send','message_type':'group'}}`)">
                Send to Selected Groups
            </button>
        </div>
        """
        self.analysis_display.setHtml(html)
        
    def show_whatsapp_general_ui(self):
        """Show general WhatsApp UI"""
        html = f"""
        <div style="padding: 20px; font-family: 'Segoe UI', sans-serif;">
            <h2 style="color: #1e293b; margin-bottom: 20px;">📱 WhatsApp Automation</h2>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 20px;">
                <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 20px; cursor: pointer;"
                     onclick="pyHandler.handleAction(`{{'type':'whatsapp_action','action':'personal'}}`)">
                    <h3 style="color: #166534; margin-bottom: 10px;">💬 Personal Messages</h3>
                    <p style="color: #64748b;">Send individual messages to your contacts</p>
                </div>
                
                <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 20px; cursor: pointer;"
                     onclick="pyHandler.handleAction(`{{'type':'whatsapp_action','action':'group'}}`)">
                    <h3 style="color: #075985; margin-bottom: 10px;">👥 Group Messages</h3>
                    <p style="color: #64748b;">Send messages to multiple groups</p>
                </div>
                
                <div style="background: #f5f3ff; border: 1px solid #ddd6fe; border-radius: 8px; padding: 20px; cursor: pointer;"
                     onclick="pyHandler.handleAction(`{{'type':'whatsapp_action','action':'auto_reply'}}`)">
                    <h3 style="color: #6d28d9; margin-bottom: 10px;">🤖 Auto Replies</h3>
                    <p style="color: #64748b;">Configure automatic replies</p>
                </div>
                
                <div style="background: #fff7ed; border: 1px solid #fed7aa; border-radius: 8px; padding: 20px; cursor: pointer;"
                     onclick="pyHandler.handleAction(`{{'type':'whatsapp_action','action':'campaign'}}`)">
                    <h3 style="color: #9a3412; margin-bottom: 10px;">📢 Campaign</h3>
                    <p style="color: #64748b;">Launch WhatsApp campaign</p>
                </div>
            </div>
            
            <div style="background: #f8fafc; border-radius: 8px; padding: 20px;">
                <h3 style="color: #1e293b; margin-bottom: 15px;">📊 Recent Statistics</h3>
                
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 15px;">
                    <div style="background: white; border-radius: 6px; padding: 15px; text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: #4f46e5;">42</div>
                        <div style="color: #64748b; font-size: 14px;">Messages Sent</div>
                    </div>
                    <div style="background: white; border-radius: 6px; padding: 15px; text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: #10b981;">78%</div>
                        <div style="color: #64748b; font-size: 14px;">Read Rate</div>
                    </div>
                    <div style="background: white; border-radius: 6px; padding: 15px; text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: #ef4444;">12</div>
                        <div style="color: #64748b; font-size: 14px;">Blocked Contacts</div>
                    </div>
                </div>
                
                <button style="background: #4f46e5; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer;">
                    View Full Report
                </button>
            </div>
        </div>
        """
        self.analysis_display.setHtml(html)

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
    
    window = MarketingAIAnalyzer()
    window.show()
    
    sys.exit(app.exec_())