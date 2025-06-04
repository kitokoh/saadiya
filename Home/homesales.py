import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, 
                            QStackedWidget, QToolBar, QStatusBar, QPushButton, 
                            QFrame, QHBoxLayout, QSizePolicy)
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QSize, QTranslator

class RibbonButton(QPushButton):
    def __init__(self, text="", icon=None, parent=None):
        super().__init__(parent)
        self.setText(text)  # Removed self.tr() since we're using English
        if icon:
            self.setIcon(QIcon(icon))
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(True)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 6px 12px;
                background: transparent;
                color: #333;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #e6e6e6;
                border-radius: 4px;
            }
            QPushButton:pressed {
                background: #d0d0d0;
                border-radius: 4px;
            }
            QPushButton:checked {
                background: #d0d0d0;
                border-radius: 4px;
            }
        """)

class MainWindowsales(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Marketing Automation Suite")
        self.setGeometry(100, 100, 1200, 800)
        
        # Dictionary to store page instances
        self.page_instances = {
            'documents': None,
            'link_manager': None,
            'contacts': None,
            'prompts': None,
            'ai_agent': None,
            'customer_support': None,
            'projects': None
        }
        
        self.setup_ui()
        
        # Setup translator (kept for potential future use)
        self.translator = QTranslator()
        
        # Modern style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QToolBar {
                background: white;
                border-bottom: 1px solid #d0d0d0;
                padding: 4px;
                spacing: 4px;
            }
            QStatusBar {
                background: white;
                border-top: 1px solid #d0d0d0;
            }
        """)

    def setup_ui(self):
        self.create_ribbon()
        self.create_status_bar()
        self.create_main_content()

    def create_ribbon(self):
        # Main ribbon toolbar
        self.ribbon = QToolBar("Ribbon")
        self.ribbon.setIconSize(QSize(20, 20))
        self.addToolBar(self.ribbon)

        # Documents tab
        self.documents_btn = RibbonButton("Documents")
        self.documents_btn.setChecked(True)
        self.documents_btn.clicked.connect(lambda: self.show_page("documents"))
        self.ribbon.addWidget(self.documents_btn)

        # Link Manager tab
        self.link_manager_btn = RibbonButton("Link Manager")
        self.link_manager_btn.clicked.connect(lambda: self.show_page("link_manager"))
        self.ribbon.addWidget(self.link_manager_btn)

        # Contacts tab
        self.contacts_btn = RibbonButton("Contacts")
        self.contacts_btn.clicked.connect(lambda: self.show_page("contacts"))
        self.ribbon.addWidget(self.contacts_btn)

        # Prompts tab
        self.prompts_btn = RibbonButton("Prompts")
        self.prompts_btn.clicked.connect(lambda: self.show_page("prompts"))
        self.ribbon.addWidget(self.prompts_btn)

        # AI Agent tab
        self.ai_agent_btn = RibbonButton("AI Agent")
        self.ai_agent_btn.clicked.connect(lambda: self.show_page("ai_agent"))
        self.ribbon.addWidget(self.ai_agent_btn)

        # Customer Support tab (formerly SAV)
        self.customer_support_btn = RibbonButton("Customer Support")
        self.customer_support_btn.clicked.connect(lambda: self.show_page("customer_support"))
        self.ribbon.addWidget(self.customer_support_btn)

        # Projects tab
        self.projects_btn = RibbonButton("Projects")
        self.projects_btn.clicked.connect(lambda: self.show_page("projects"))
        self.ribbon.addWidget(self.projects_btn)

    def create_status_bar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        # Message area
        self.status_label = QLabel("Ready")
        status_bar.addWidget(self.status_label, 1)

        # Status widgets
        zoom_label = QLabel("100%")
        status_bar.addPermanentWidget(zoom_label)

    def create_main_content(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Content area
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Create only the documents page initially
        self.load_documents_page()

    def load_documents_page(self):
        """Load Documents page only if not already loaded"""
        if self.page_instances['documents'] is None:
            from Home.homemarketing import MainWindow as DocumentsPage
            self.page_instances['documents'] = DocumentsPage()
            self.stacked_widget.addWidget(self.page_instances['documents'])
        return self.page_instances['documents']

    def load_link_manager_page(self):
        """Load Link Manager page only if not already loaded"""
        if self.page_instances['link_manager'] is None:
            from liens.gestionliens import MainWindowLink as LinkManagerPage
            self.page_instances['link_manager'] = LinkManagerPage()
            self.stacked_widget.addWidget(self.page_instances['link_manager'])
        return self.page_instances['link_manager']

    def load_contacts_page(self):
        """Load Contacts page only if not already loaded"""
        if self.page_instances['contacts'] is None:
            from ModulesUI.whasapping.group_manager import ContactTable as ContactsPage
            self.page_instances['contacts'] = ContactsPage()
            self.stacked_widget.addWidget(self.page_instances['contacts'])
        return self.page_instances['contacts']

    def load_prompts_page(self):
        """Load Prompts page only if not already loaded"""
        if self.page_instances['prompts'] is None:
            from promptes.promptes import PromptManager as PromptsPage
            self.page_instances['prompts'] = PromptsPage()
            self.stacked_widget.addWidget(self.page_instances['prompts'])
        return self.page_instances['prompts']

    def load_ai_agent_page(self):
        """Load AI Agent page only if not already loaded"""
        if self.page_instances['ai_agent'] is None:
            # Default AI Agent page with modern interface
            class AIAgentPage(QWidget):
                def __init__(self):
                    super().__init__()
                    layout = QVBoxLayout()
                    
                    # Header
                    header = QLabel("AI Agent Dashboard")
                    header.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
                    header.setAlignment(Qt.AlignCenter)
                    layout.addWidget(header)
                    
                    # AI Agent controls
                    control_frame = QFrame()
                    control_frame.setFrameShape(QFrame.StyledPanel)
                    control_layout = QHBoxLayout()
                    
                    self.start_btn = QPushButton("Start Agent")
                    self.start_btn.setStyleSheet("padding: 8px; background: #27ae60; color: white;")
                    control_layout.addWidget(self.start_btn)
                    
                    self.stop_btn = QPushButton("Stop Agent")
                    self.stop_btn.setStyleSheet("padding: 8px; background: #e74c3c; color: white;")
                    control_layout.addWidget(self.stop_btn)
                    
                    control_frame.setLayout(control_layout)
                    layout.addWidget(control_frame)
                    
                    # Status area
                    self.status_area = QLabel("Agent is currently inactive")
                    self.status_area.setStyleSheet("font-size: 14px; color: #7f8c8d;")
                    self.status_area.setAlignment(Qt.AlignCenter)
                    layout.addWidget(self.status_area)
                    
                    self.setLayout(layout)
            
            self.page_instances['ai_agent'] = AIAgentPage()
            self.stacked_widget.addWidget(self.page_instances['ai_agent'])
        return self.page_instances['ai_agent']

    def load_customer_support_page(self):
        """Load Customer Support page only if not already loaded"""
        if self.page_instances['customer_support'] is None:
            class CustomerSupportPage(QWidget):
                def __init__(self):
                    super().__init__()
                    layout = QVBoxLayout()
                    
                    header = QLabel("Customer Support Center")
                    header.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
                    header.setAlignment(Qt.AlignCenter)
                    layout.addWidget(header)
                    
                    # Ticket management section
                    ticket_frame = QFrame()
                    ticket_frame.setFrameShape(QFrame.StyledPanel)
                    ticket_layout = QVBoxLayout()
                    
                    ticket_label = QLabel("Open Support Tickets")
                    ticket_label.setStyleSheet("font-size: 14px; font-weight: bold;")
                    ticket_layout.addWidget(ticket_label)
                    
                    # Placeholder for ticket list
                    self.ticket_list = QLabel("No active tickets")
                    self.ticket_list.setStyleSheet("font-size: 12px; color: #7f8c8d;")
                    ticket_layout.addWidget(self.ticket_list)
                    
                    ticket_frame.setLayout(ticket_layout)
                    layout.addWidget(ticket_frame)
                    
                    self.setLayout(layout)
            
            self.page_instances['customer_support'] = CustomerSupportPage()
            self.stacked_widget.addWidget(self.page_instances['customer_support'])
        return self.page_instances['customer_support']

    def load_projects_page(self):
        """Load Projects page only if not already loaded"""
        if self.page_instances['projects'] is None:
            from Home.homemarketing import MainWindow as ProjectsPage
            self.page_instances['projects'] = ProjectsPage()
            self.stacked_widget.addWidget(self.page_instances['projects'])
        return self.page_instances['projects']

    def show_page(self, page_name):
        if page_name in self.page_instances:
            # Load page only when requested
            if page_name == 'documents':
                page = self.load_documents_page()
            elif page_name == 'link_manager':
                page = self.load_link_manager_page()
            elif page_name == 'contacts':
                page = self.load_contacts_page()
            elif page_name == 'prompts':
                page = self.load_prompts_page()
            elif page_name == 'ai_agent':
                page = self.load_ai_agent_page()
            elif page_name == 'customer_support':
                page = self.load_customer_support_page()
            elif page_name == 'projects':
                page = self.load_projects_page()
            else:
                return

            self.stacked_widget.setCurrentWidget(page)
            self.update_button_states(page_name)
            self.status_label.setText(f"Showing {page_name.replace('_', ' ')} page")

    def update_button_states(self, active_page):
        self.documents_btn.setChecked(active_page == "documents")
        self.link_manager_btn.setChecked(active_page == "link_manager")
        self.contacts_btn.setChecked(active_page == "contacts")
        self.prompts_btn.setChecked(active_page == "prompts")
        self.ai_agent_btn.setChecked(active_page == "ai_agent")
        self.customer_support_btn.setChecked(active_page == "customer_support")
        self.projects_btn.setChecked(active_page == "projects")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Modern Fusion style
    app.setStyle("Fusion")
    
    # Light color palette
    palette = app.palette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, Qt.white)
    palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.black)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())