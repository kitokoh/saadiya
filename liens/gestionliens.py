import sys
import sqlite3
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, 
                             QComboBox, QMessageBox, QFrame, QScrollArea, QSizePolicy,
                             QInputDialog, QAction, QMenu, QFileDialog, QCheckBox, QGroupBox,
                             QStackedWidget, QToolButton, QSizeGrip)
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor, QKeySequence, QPainter, QLinearGradient
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtCore import pyqtSignal
from imports import DB_PATH_links
from PyQt5.QtCore import QUrl
import webbrowser

# Database path
DB_PATH_links = DB_PATH_links

class PasswordEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEchoMode(QLineEdit.Password)
        self.toggle_password_action = self.addAction(QIcon.fromTheme("visibility"), QLineEdit.TrailingPosition)
        self.toggle_password_action.triggered.connect(self.toggle_password_visibility)
        self.password_visible = False
        self.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #d1d3e2;
                border-radius: 4px;
                background-color: #fff;
            }
            QLineEdit:focus {
                border: 1px solid #4e73df;
                outline: none;
            }
        """)

    def toggle_password_visibility(self):
        if self.password_visible:
            self.setEchoMode(QLineEdit.Password)
            self.toggle_password_action.setIcon(QIcon.fromTheme("visibility"))
            self.password_visible = False
        else:
            self.setEchoMode(QLineEdit.Normal)
            self.toggle_password_action.setIcon(QIcon.fromTheme("visibility-off"))
            self.password_visible = True
from PyQt5.QtCore import pyqtProperty, QPropertyAnimation
from PyQt5.QtGui import QPainter

class FadeButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._opacity_value = 1.0  # Variable interne pour stocker l'opacité
        self._animation = QPropertyAnimation(self, b"opacity")
        self._animation.setDuration(200)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(self._opacity_value)
        super().paintEvent(event)
        
    def get_opacity(self):
        return self._opacity_value
        
    def set_opacity(self, opacity):
        # On s'assure que l'opacité reste entre 0 et 1
        opacity = max(0.0, min(1.0, opacity))
        if self._opacity_value != opacity:
            self._opacity_value = opacity
            self.update()  # Force le repaint
            
    # Définition de la propriété Qt
    opacity = pyqtProperty(float, get_opacity, set_opacity)
    
    def enterEvent(self, event):
        self.start_animation(0.7)
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.start_animation(1.0)
        super().leaveEvent(event)
        
    def start_animation(self, target_opacity):
        self._animation.stop()
        self._animation.setStartValue(self.opacity)
        self._animation.setEndValue(target_opacity)
        self._animation.start()
class FadeButton1(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._animation = QPropertyAnimation(self, b"opacity")
        self._animation.setDuration(200)
        self._opacity = 1.0
        self.setGraphicsEffect(None)

    def setOpacity(self, opacity):
        self._opacity = opacity
        self.update()

    def opacity(self):
        return self._opacity

    def enterEvent(self, event):
        self._animation.stop()
        self._animation.setEndValue(0.7)
        self._animation.start()

    def leaveEvent(self, event):
        self._animation.stop()
        self._animation.setEndValue(1.0)
        self._animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(self._opacity)
        super().paintEvent(event)
class FadeButton2(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._opacity = 1.0
        self._animation = QPropertyAnimation(self, b"_opacity")
        self._animation.setDuration(200)
        
        # Définir la propriété opacity comme dynamique
        self.setProperty("_opacity", 1.0)
        
    def _get_opacity(self):
        return self._opacity
        
    def _set_opacity(self, opacity):
        self._opacity = opacity
        self.update()
        
    _opacity = property(_get_opacity, _set_opacity)
        
    def enterEvent(self, event):
        self._animation.stop()
        self._animation.setStartValue(self._opacity)
        self._animation.setEndValue(0.7)
        self._animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self._animation.stop()
        self._animation.setStartValue(self._opacity)
        self._animation.setEndValue(1.0)
        self._animation.start()
        super().leaveEvent(event)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(self._opacity)
        super().paintEvent(event)
class GradientLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._gradient = QLinearGradient(0, 0, 0, 1)
        self._gradient.setColorAt(0, QColor("#4e73df"))
        self._gradient.setColorAt(1, QColor("#224abe"))
        self.setFont(QFont('Arial', 16, QFont.Bold))
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(50)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        self._gradient.setFinalStop(0, self.height())
        painter.setBrush(self._gradient)
        painter.drawRect(self.rect())
        painter.setPen(QColor("#ffffff"))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH_links, check_same_thread=False)
        self.create_tables()
        self.initialize_default_data()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT DEFAULT '#4e73df'
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT DEFAULT '#858796'
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS link_tags (
                link_id INTEGER,
                tag_id INTEGER,
                PRIMARY KEY (link_id, tag_id),
                FOREIGN KEY (link_id) REFERENCES links(id),
                FOREIGN KEY (tag_id) REFERENCES tags(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                username TEXT,
                password TEXT,
                favorite BOOLEAN DEFAULT 0,
                category_id INTEGER,
                creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        ''')
        self.conn.commit()
        
    def initialize_default_data1(self):
        cursor = self.conn.cursor()
        
        # Check if database is empty
        cursor.execute('SELECT COUNT(*) FROM categories')
        if cursor.fetchone()[0] == 0:
            # Default categories
            categories = [
                ("Social Networks", "#4e73df"),
                ("Digital Marketing", "#1cc88a"),
                ("E-commerce", "#f6c23e"),
                ("Productivity Tools", "#36b9cc"),
                ("Development", "#6f42c1"),
                ("Tech News", "#e74a3b")
            ]
            
            for name, color in categories:
                self.add_category(name, color)
            
            # Default links
            default_links = [
                # Social Networks
                ("Facebook", "https://facebook.com", None, None, False, "Social Networks", ["social", "network"]),
                ("Instagram", "https://instagram.com", None, None, False, "Social Networks", ["social", "photo"]),
                ("Twitter", "https://twitter.com", None, None, False, "Social Networks", ["social", "news"]),
                ("LinkedIn", "https://linkedin.com", None, None, True, "Social Networks", ["social", "professional"]),
                
                # Digital Marketing
                ("Google Analytics", "https://analytics.google.com", None, None, True, "Digital Marketing", ["analytics", "traffic"]),
                ("Google Ads", "https://ads.google.com", None, None, False, "Digital Marketing", ["advertising", "google"]),
                ("Facebook Ads", "https://www.facebook.com/adsmanager", None, None, False, "Digital Marketing", ["advertising", "facebook"]),
                ("Mailchimp", "https://mailchimp.com", None, None, False, "Digital Marketing", ["email", "newsletter"]),
                
                # E-commerce
                ("Shopify", "https://shopify.com", None, None, False, "E-commerce", ["shop", "ecommerce"]),
                ("WooCommerce", "https://woocommerce.com", None, None, False, "E-commerce", ["wordpress", "shop"]),
                ("Amazon Seller", "https://sellercentral.amazon.com", None, None, True, "E-commerce", ["marketplace", "sales"]),
                ("Ebay", "https://www.ebay.com/sellercenter", None, None, False, "E-commerce", ["marketplace", "sales"]),
                
                # Productivity Tools
                ("Google Drive", "https://drive.google.com", None, None, True, "Productivity Tools", ["storage", "collaboration"]),
                ("Trello", "https://trello.com", None, None, False, "Productivity Tools", ["management", "project"]),
                ("Slack", "https://slack.com", None, None, False, "Productivity Tools", ["communication", "team"]),
                ("Notion", "https://www.notion.so", None, None, True, "Productivity Tools", ["organization", "notes"]),
                
                # Development
                ("GitHub", "https://github.com", None, None, True, "Development", ["code", "versioning"]),
                ("GitLab", "https://gitlab.com", None, None, False, "Development", ["code", "versioning"]),
                ("Stack Overflow", "https://stackoverflow.com", None, None, True, "Development", ["help", "programming"]),
                ("MDN Web Docs", "https://developer.mozilla.org", None, None, False, "Development", ["documentation", "web"]),
                
                # Tech News
                ("TechCrunch", "https://techcrunch.com", None, None, False, "Tech News", ["news", "technology"]),
                ("The Verge", "https://www.theverge.com", None, None, False, "Tech News", ["news", "technology"]),
                ("Wired", "https://www.wired.com", None, None, False, "Tech News", ["news", "innovation"]),
                ("Product Hunt", "https://www.producthunt.com", None, None, True, "Tech News", ["new", "products"])
            ]
            
            for title, url, username, password, favorite, category, tags in default_links:
                cursor.execute('SELECT id FROM categories WHERE name = ?', (category,))
                category_id = cursor.fetchone()[0]
                
                tag_objects = [(tag, "#858796") for tag in tags]
                
                self.add_link(
                    title=title,
                    url=url,
                    category_id=category_id,
                    username=username,
                    password=password,
                    favorite=favorite,
                    tags=tag_objects
                )
    def initialize_default_data(self):
        cursor = self.conn.cursor()

        # Check if database is empty
        cursor.execute('SELECT COUNT(*) FROM categories')
        if cursor.fetchone()[0] == 0:
            # Catégories enrichies pour un commerçant international
            categories = [
                ("Business Directories", "#4e73df"),
                ("Import/Export Tools", "#1cc88a"),
                ("Marketplaces", "#f6c23e"),
                ("Logistics & Tracking", "#36b9cc"),
                ("Market Research", "#6f42c1"),
                ("Forums & Communities", "#e74a3b"),
                ("Advertising Tools", "#fd7e14"),
                ("Payment Solutions", "#20c997"),
                ("Company Registers", "#0dcaf0"),
                ("Legal & Compliance", "#6610f2")
            ]

            for name, color in categories:
                self.add_category(name, color)

            # Liens utiles par catégorie
            default_links = [
                # Business Directories
                ("Europages", "https://www.europages.com", None, None, False, "Business Directories", ["b2b", "directory"]),
                ("Kompass", "https://www.kompass.com", None, None, False, "Business Directories", ["b2b", "directory"]),
                ("Yellow Pages", "https://www.yellowpages.com", None, None, False, "Business Directories", ["contacts", "local"]),
                ("Pages Jaunes (France)", "https://www.pagesjaunes.fr", None, None, False, "Business Directories", ["entreprises", "local"]),

                # Import/Export Tools
                ("Trademap", "https://www.trademap.org", None, None, True, "Import/Export Tools", ["data", "export"]),
                ("Alibaba", "https://www.alibaba.com", None, None, False, "Import/Export Tools", ["supplier", "china"]),
                ("Aliexpress", "https://www.aliexpress.com", None, None, False, "Import/Export Tools", ["china", "retail"]),
                ("Global Sources", "https://www.globalsources.com", None, None, False, "Import/Export Tools", ["supplier", "global"]),

                # Marketplaces
                ("Amazon Seller Central", "https://sellercentral.amazon.com", None, None, True, "Marketplaces", ["sales", "ecommerce"]),
                ("eBay Seller Center", "https://www.ebay.com/sellercenter", None, None, False, "Marketplaces", ["marketplace", "sales"]),
                ("Trendyol Partner", "https://partner.trendyol.com", None, None, False, "Marketplaces", ["turkey", "marketplace"]),
                ("Hepsiburada Business", "https://www.hepsiburada.com", None, None, False, "Marketplaces", ["turkey", "ecommerce"]),

                # Logistics & Tracking
                ("Aramex Tracking", "https://www.aramex.com/track/shipments", None, None, False, "Logistics & Tracking", ["cargo", "tracking"]),
                ("DHL Express", "https://www.dhl.com", None, None, False, "Logistics & Tracking", ["logistics", "shipment"]),
                ("FedEx", "https://www.fedex.com", None, None, False, "Logistics & Tracking", ["delivery", "tracking"]),
                ("CargoX", "https://cargox.digital", None, None, False, "Logistics & Tracking", ["blockchain", "logistics"]),

                # Market Research
                ("Market Access Map", "https://macmap.org", None, None, True, "Market Research", ["tariffs", "barriers"]),
                ("World Bank WITS", "https://wits.worldbank.org", None, None, False, "Market Research", ["data", "trade"]),
                ("OECD Trade", "https://data.oecd.org/trade.htm", None, None, False, "Market Research", ["stats", "international"]),
                ("UN Comtrade", "https://comtrade.un.org", None, None, False, "Market Research", ["data", "imports"]),

                # Forums & Communities
                ("Reddit - Exporting", "https://www.reddit.com/r/Exporting/", None, None, False, "Forums & Communities", ["forum", "discussion"]),
                ("Quora - International Trade", "https://www.quora.com/topic/International-Trade", None, None, False, "Forums & Communities", ["questions", "answers"]),
                ("Exporters India Forum", "https://www.exportersindia.com/forums/", None, None, False, "Forums & Communities", ["network", "business"]),
                ("LinkedIn Trade Groups", "https://www.linkedin.com/groups/1796788/", None, None, False, "Forums & Communities", ["professional", "network"]),

                # Advertising Tools
                ("Google Ads", "https://ads.google.com", None, None, True, "Advertising Tools", ["ads", "google"]),
                ("Meta Business Suite", "https://business.facebook.com", None, None, True, "Advertising Tools", ["facebook", "ads"]),
                ("TikTok Ads", "https://ads.tiktok.com", None, None, False, "Advertising Tools", ["tiktok", "marketing"]),
                ("LinkedIn Ads", "https://www.linkedin.com/ad/start/", None, None, False, "Advertising Tools", ["linkedin", "ads"]),

                # Payment Solutions
                ("PayPal Business", "https://www.paypal.com/business", None, None, False, "Payment Solutions", ["payment", "global"]),
                ("Wise Business", "https://wise.com/business", None, None, False, "Payment Solutions", ["bank", "transfer"]),
                ("Payoneer", "https://www.payoneer.com", None, None, False, "Payment Solutions", ["payment", "freelance"]),
                ("Stripe", "https://stripe.com", None, None, False, "Payment Solutions", ["payment", "ecommerce"]),

                # Company Registers
                ("Turkey MERSIS", "https://mersis.gtb.gov.tr", None, None, False, "Company Registers", ["turkey", "registry"]),
                ("Infogreffe (France)", "https://www.infogreffe.fr", None, None, False, "Company Registers", ["france", "legal"]),
                ("UK Companies House", "https://www.gov.uk/get-information-about-a-company", None, None, False, "Company Registers", ["uk", "registry"]),
                ("OpenCorporates", "https://opencorporates.com", None, None, False, "Company Registers", ["global", "company"]),

                # Legal & Compliance
                ("TAREKS (Turkey)", "https://uygulama.tarimorman.gov.tr/TAREKS", None, None, False, "Legal & Compliance", ["export", "control"]),
                ("EUR-Lex", "https://eur-lex.europa.eu", None, None, False, "Legal & Compliance", ["eu", "regulations"]),
                ("US Customs Info", "https://www.cbp.gov", None, None, False, "Legal & Compliance", ["usa", "customs"]),
                ("WTO", "https://www.wto.org", None, None, False, "Legal & Compliance", ["international", "trade"])
            ]

            for title, url, username, password, favorite, category, tags in default_links:
                cursor.execute('SELECT id FROM categories WHERE name = ?', (category,))
                category_id = cursor.fetchone()[0]
                tag_objects = [(tag, "#858796") for tag in tags]
                self.add_link(
                    title=title,
                    url=url,
                    category_id=category_id,
                    username=username,
                    password=password,
                    favorite=favorite,
                    tags=tag_objects
                )
        
    def add_category(self, name, color="#4e73df"):
        cursor = self.conn.cursor()
        try:
            cursor.execute('INSERT INTO categories (name, color) VALUES (?, ?)', (name, color))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return False
            
    def get_categories(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, color FROM categories ORDER BY name')
        return cursor.fetchall()
        
    def add_tag(self, name, color="#858796"):
        cursor = self.conn.cursor()
        try:
            cursor.execute('INSERT INTO tags (name, color) VALUES (?, ?)', (name, color))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            cursor.execute('SELECT id FROM tags WHERE name = ?', (name,))
            return cursor.fetchone()[0]
            
    def get_tags(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, color FROM tags ORDER BY name')
        return cursor.fetchall()
        
    def get_tags_for_link(self, link_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT t.id, t.name, t.color 
            FROM tags t
            JOIN link_tags lt ON t.id = lt.tag_id
            WHERE lt.link_id = ?
        ''', (link_id,))
        return cursor.fetchall()
        
    def update_link_tags(self, link_id, tags):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM link_tags WHERE link_id = ?', (link_id,))
        
        for tag in tags:
            if isinstance(tag, tuple):
                tag_id = self.add_tag(tag[0], tag[1])
            else:
                tag_id = self.add_tag(tag)
            cursor.execute('INSERT INTO link_tags (link_id, tag_id) VALUES (?, ?)', (link_id, tag_id))
            
        self.conn.commit()
        
    def add_link(self, title, url, category_id, username=None, password=None, favorite=False, tags=None):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO links (title, url, category_id, username, password, favorite) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, url, category_id, username, password, favorite))
        link_id = cursor.lastrowid
        
        if tags:
            self.update_link_tags(link_id, tags)
            
        self.conn.commit()
        return link_id
        
    def update_link(self, link_id, title, url, category_id, username=None, password=None, favorite=None, tags=None):
        cursor = self.conn.cursor()
        
        if favorite is not None:
            cursor.execute('''
                UPDATE links 
                SET title = ?, url = ?, category_id = ?, username = ?, password = ?, favorite = ?
                WHERE id = ?
            ''', (title, url, category_id, username, password, favorite, link_id))
        else:
            cursor.execute('''
                UPDATE links 
                SET title = ?, url = ?, category_id = ?, username = ?, password = ?
                WHERE id = ?
            ''', (title, url, category_id, username, password, link_id))
            
        if tags is not None:
            self.update_link_tags(link_id, tags)
            
        self.conn.commit()
        
    def get_links_by_category(self, category_id=None, favorite=None, search_query=None):
        cursor = self.conn.cursor()
        query = '''
            SELECT l.id, l.title, l.url, l.username, l.password, l.favorite, c.name, c.color 
            FROM links l 
            JOIN categories c ON l.category_id = c.id 
        '''
        params = []
        
        conditions = []
        if category_id:
            conditions.append("l.category_id = ?")
            params.append(category_id)
        if favorite is not None:
            conditions.append("l.favorite = ?")
            params.append(favorite)
        if search_query:
            conditions.append("(l.title LIKE ? OR l.url LIKE ? OR c.name LIKE ?)")
            params.extend([f"%{search_query}%"] * 3)
            
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        query += " ORDER BY c.name, l.title"
        cursor.execute(query, params)
            
        links = cursor.fetchall()
        
        # Get tags for each link
        result = []
        for link in links:
            tags = self.get_tags_for_link(link[0])
            result.append((*link, tags))
            
        return result
        
    def delete_link(self, link_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM link_tags WHERE link_id = ?', (link_id,))
        cursor.execute('DELETE FROM links WHERE id = ?', (link_id,))
        self.conn.commit()
        
    def delete_category(self, category_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
        cursor.execute('DELETE FROM links WHERE category_id = ?', (category_id,))
        self.conn.commit()
        
    def delete_all_data(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM link_tags')
        cursor.execute('DELETE FROM links')
        cursor.execute('DELETE FROM tags')
        cursor.execute('DELETE FROM categories')
        self.conn.commit()
        
    def export_links(self, filename):
        links = self.get_links_by_category()
        data = []
        
        for link in links:
            data.append({
                'id': link[0],
                'title': link[1],
                'url': link[2],
                'username': link[3],
                'password': link[4],
                'favorite': bool(link[5]),
                'category': link[6],
                'category_color': link[7],
                'tags': [{'name': tag[1], 'color': tag[2]} for tag in link[8]]
            })
            
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def import_links(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            
        for item in data:
            # Find or create category
            cursor = self.conn.cursor()
            cursor.execute('SELECT id FROM categories WHERE name = ?', (item['category'],))
            category = cursor.fetchone()
            
            if not category:
                self.add_category(item['category'], item.get('category_color', '#4e73df'))
                cursor.execute('SELECT id FROM categories WHERE name = ?', (item['category'],))
                category_id = cursor.fetchone()[0]
            else:
                category_id = category[0]
                
            # Check if link already exists
            cursor.execute('SELECT id FROM links WHERE title = ? AND url = ?', (item['title'], item['url']))
            existing = cursor.fetchone()
            
            if not existing:
                tags = [(tag['name'], tag.get('color', '#858796')) for tag in item.get('tags', [])]
                self.add_link(
                    title=item['title'],
                    url=item['url'],
                    category_id=category_id,
                    username=item.get('username'),
                    password=item.get('password'),
                    favorite=item.get('favorite', False),
                    tags=tags
                )

class TagWidget(QWidget):
    clicked = pyqtSignal(str)
    
    def __init__(self, tag, color="#858796", clickable=False, parent=None):
        super().__init__(parent)
        self.tag = tag
        self.color = color
        self.clickable = clickable
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(6, 2, 6, 2)
        
        self.label = QLabel(self.tag)
        self.label.setStyleSheet(f"""
            background-color: {self.color};
            border-radius: 10px;
            padding: 2px 8px;
            color: white;
            font-size: 10px;
            {'cursor: pointer;' if self.clickable else ''}
        """)
        
        if self.clickable:
            self.label.mousePressEvent = lambda e: self.clicked.emit(self.tag)
        
        layout.addWidget(self.label)
        self.setLayout(layout)

class LinkWidget(QWidget):
    edit_requested = pyqtSignal(int)
    tag_clicked = pyqtSignal(str)
    
    def __init__(self, link_id, title, url, category, category_color, 
                 username=None, password=None, favorite=False, tags=None, parent=None):
        super().__init__(parent)
        self.link_id = link_id
        self.url = url
        self.parent = parent
        self.password = password
        self.password_visible = False
        self.tags = tags or []
        self.category_color = category_color
        
        self.setup_ui(title, category, username, favorite)
        
    def setup_ui(self, title, category, username, favorite):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #ffffff;
                border-radius: 8px;
                border: 1px solid #e3e6f0;
            }}
            QPushButton {{
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
                min-width: 60px;
            }}
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)
        
        # Header with title and buttons
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title and favorite
        title_fav = QWidget()
        title_fav_layout = QHBoxLayout(title_fav)
        title_fav_layout.setContentsMargins(0, 0, 0, 0)
        
        self.fav_btn = QPushButton()
        self.fav_btn.setFixedSize(24, 24)
        self.fav_btn.setFlat(True)
        self.fav_btn.setIcon(QIcon.fromTheme("emblem-favorite" if favorite else "emblem-default"))
        self.fav_btn.setIconSize(QSize(16, 16))
        self.fav_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
            }
        """)
        self.fav_btn.clicked.connect(self.toggle_favorite)
        
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont('Arial', 10, QFont.Bold))
        self.title_label.setStyleSheet("color: #2e59d9;")
        
        title_fav_layout.addWidget(self.fav_btn)
        title_fav_layout.addWidget(self.title_label, 1)
        title_fav_layout.addStretch()
        
        header_layout.addWidget(title_fav, 1)
        
        # Action buttons
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(5)
        
        self.btn_visit = FadeButton("Visit")
        self.btn_visit.setIcon(QIcon.fromTheme("go-jump"))
        self.btn_visit.setStyleSheet("""
            QPushButton {
                background-color: #4e73df; 
                color: white;
            }
            QPushButton:hover {
                background-color: #3a5bc7;
            }
        """)
        self.btn_visit.clicked.connect(self.visit_link)
        
        self.btn_edit = QPushButton("")
        self.btn_edit.setIcon(QIcon.fromTheme("document-edit"))
        self.btn_edit.setToolTip("Edit")
        self.btn_edit.setStyleSheet("""
            QPushButton {
                background-color: #f6c23e; 
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #dda20a;
            }
        """)
        self.btn_edit.clicked.connect(lambda: self.edit_requested.emit(self.link_id))
        
        self.btn_delete = QPushButton("")
        self.btn_delete.setIcon(QIcon.fromTheme("edit-delete"))
        self.btn_delete.setToolTip("Delete")
        self.btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #e74a3b; 
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #be2617;
            }
        """)
        self.btn_delete.clicked.connect(self.delete_link)
        
        btn_layout.addWidget(self.btn_visit)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        
        header_layout.addWidget(btn_container)
        
        main_layout.addWidget(header)
        
        # Category and URL
        meta_container = QWidget()
        meta_layout = QVBoxLayout(meta_container)
        meta_layout.setContentsMargins(0, 0, 0, 0)
        meta_layout.setSpacing(4)
        
        # Category
        self.category_label = QLabel(f"<small>Category: <span style='color: {self.category_color}; font-weight: bold;'>{category}</span></small>")
        
        # URL
        self.url_label = QLabel(f"<small>URL: {self.url}</small>")
        self.url_label.setStyleSheet("color: #858796;")
        self.url_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        meta_layout.addWidget(self.category_label)
        meta_layout.addWidget(self.url_label)
        
        main_layout.addWidget(meta_container)
        
        # Username and password
        if username or self.password:
            auth_container = QWidget()
            auth_layout = QVBoxLayout(auth_container)
            auth_layout.setContentsMargins(0, 0, 0, 0)
            auth_layout.setSpacing(4)
            
            # Username
            if username:
                username_group = QWidget()
                username_layout = QHBoxLayout(username_group)
                username_layout.setContentsMargins(0, 0, 0, 0)
                
                username_title = QLabel("<small>Username:</small>")
                username_title.setStyleSheet("color: #6c757d; min-width: 70px;")
                
                self.username_value = QLabel(username)
                self.username_value.setStyleSheet("color: #5a5c69;")
                self.username_value.setTextInteractionFlags(Qt.TextSelectableByMouse)
                
                btn_copy_id = QPushButton("")
                btn_copy_id.setIcon(QIcon.fromTheme("edit-copy"))
                btn_copy_id.setToolTip("Copy")
                btn_copy_id.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #f8f9fa;
                    }
                """)
                btn_copy_id.setFixedSize(24, 24)
                btn_copy_id.clicked.connect(lambda: QApplication.clipboard().setText(username))
                
                username_layout.addWidget(username_title)
                username_layout.addWidget(self.username_value, 1)
                username_layout.addWidget(btn_copy_id)
                
                auth_layout.addWidget(username_group)
            
            # Password
            if self.password:
                password_group = QWidget()
                password_layout = QHBoxLayout(password_group)
                password_layout.setContentsMargins(0, 0, 0, 0)
                
                password_title = QLabel("<small>Password:</small>")
                password_title.setStyleSheet("color: #6c757d; min-width: 70px;")
                
                self.password_value = QLabel("••••••••")
                self.password_value.setStyleSheet("color: #5a5c69;")
                
                btn_container = QWidget()
                btn_pass_layout = QHBoxLayout(btn_container)
                btn_pass_layout.setContentsMargins(0, 0, 0, 0)
                btn_pass_layout.setSpacing(2)
                
                btn_show_pass = QPushButton("")
                btn_show_pass.setIcon(QIcon.fromTheme("visibility-off"))
                btn_show_pass.setToolTip("Show")
                btn_show_pass.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #f8f9fa;
                    }
                """)
                btn_show_pass.setFixedSize(24, 24)
                btn_show_pass.clicked.connect(self.toggle_password_visibility)
                
                btn_copy_pass = QPushButton("")
                btn_copy_pass.setIcon(QIcon.fromTheme("edit-copy"))
                btn_copy_pass.setToolTip("Copy")
                btn_copy_pass.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #f8f9fa;
                    }
                """)
                btn_copy_pass.setFixedSize(24, 24)
                btn_copy_pass.clicked.connect(lambda: QApplication.clipboard().setText(self.password))
                
                btn_pass_layout.addWidget(btn_show_pass)
                btn_pass_layout.addWidget(btn_copy_pass)
                
                password_layout.addWidget(password_title)
                password_layout.addWidget(self.password_value, 1)
                password_layout.addWidget(btn_container)
                
                auth_layout.addWidget(password_group)
            
            main_layout.addWidget(auth_container)
        
        # Tags
        if self.tags:
            tags_container = QWidget()
            tags_layout = QHBoxLayout(tags_container)
            tags_layout.setContentsMargins(0, 0, 0, 0)
            tags_layout.setSpacing(4)
            
            for tag in self.tags:
                tag_widget = TagWidget(tag[1], tag[2], True, self)
                tag_widget.clicked.connect(self.tag_clicked.emit)
                tags_layout.addWidget(tag_widget)
                
            tags_layout.addStretch()
            main_layout.addWidget(tags_container)
        
        self.setLayout(main_layout)
        
    def toggle_favorite(self):
        favorite = not ("emblem-favorite" in self.fav_btn.icon().name())
        self.parent.db.update_link(
            self.link_id, 
            favorite=favorite
        )
        self.fav_btn.setIcon(QIcon.fromTheme("emblem-favorite" if favorite else "emblem-default"))
        if self.parent.favorites_check.isChecked():
            self.setVisible(favorite)
        
    def toggle_password_visibility(self):
        if self.password_visible:
            self.password_value.setText("••••••••")
            self.sender().setIcon(QIcon.fromTheme("visibility-off"))
            self.sender().setToolTip("Show")
            self.password_visible = False
        else:
            self.password_value.setText(self.password)
            self.sender().setIcon(QIcon.fromTheme("visibility"))
            self.sender().setToolTip("Hide")
            self.password_visible = True
    def visit_link1(self):
        """Dans LinkWidget"""
        self.parent.open_link_with_choice(self.url, self.title_label.text())

    def visit_link(self):
        """Dans LinkWidget"""
        link_data = {
            'url': self.url,
            'title': self.title_label.text(),
            'username': self.username if hasattr(self, 'username') else None,
            'password': self.password if hasattr(self, 'password') else None
        }
        self.parent.open_link_with_choice(link_data)
        
    def visit_link1(self):
        self.parent.visit_link(self.url)
        
    def delete_link(self):
        reply = QMessageBox.question(
            self, 'Confirmation', 
            f"Do you really want to delete the link '{self.title_label.text()}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.parent.db.delete_link(self.link_id)
            self.parent.load_links()

class CategoryWidget(QWidget):
    def __init__(self, category_id, name, color, parent=None):
        super().__init__(parent)
        self.category_id = category_id
        self.parent = parent
        self.color = color
        
        self.setup_ui(name)
        
    def setup_ui(self, name):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #ffffff;
                border-radius: 8px;
                border: 1px solid #e3e6f0;
            }}
            QLabel {{
                color: {self.color};
                font-weight: bold;
            }}
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        
        self.name_label = QLabel(name)
        self.name_label.setFont(QFont('Arial', 12, QFont.Bold))
        
        self.btn_visit = FadeButton("Open all")
        self.btn_visit.setIcon(QIcon.fromTheme("go-jump"))
        self.btn_visit.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color};
                color: white;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(self.color)};
            }}
        """)
        self.btn_visit.clicked.connect(self.visit_all_links)
        
        self.btn_delete = FadeButton("Delete")
        self.btn_delete.setIcon(QIcon.fromTheme("edit-delete"))
        self.btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #e74a3b;
                color: white;
            }
            QPushButton:hover {
                background-color: #be2617;
            }
        """)
        self.btn_delete.clicked.connect(self.delete_category)
        
        layout.addWidget(self.name_label, 1)
        layout.addWidget(self.btn_visit)
        layout.addWidget(self.btn_delete)
        
        self.setLayout(layout)
        
    def darken_color(self, hex_color, amount=0.2):
        color = QColor(hex_color)
        return color.darker(int(100 + (amount * 100))).name()
    def visit_all_links(self):
        """Dans CategoryWidget"""
        links = self.parent.db.get_links_by_category(self.category_id)
        for i, link in enumerate(links):
            title = link[1]
            url = link[2]
            if i == 0:  # Premier lien - demander le choix
                self.parent.open_link_with_choice1(url, title)
            else:  # Les suivants - utiliser le même choix que le premier
                webbrowser.open(url)  # Ou self.parent.open_in_app() selon préférence            
            
    def visit_all_links1(self):
        links = self.parent.db.get_links_by_category(self.category_id)
        first = True
        for link in links:
            self.parent.visit_link(link[2], new_tab=not first)
            first = False
            
    def delete_category(self):
        reply = QMessageBox.question(
            self, 'Confirmation', 
            f"Do you really want to delete the category '{self.name_label.text()}' and all its links?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.parent.db.delete_category(self.category_id)
            self.parent.load_categories()
            self.parent.load_links()

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class AddCategoryDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.parent = parent

        self.setWindowTitle("➕ Add Category")
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(450, 280)  # Légèrement plus grand pour mieux respirer

        # Style moderne et cohérent
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fc;
                border-radius: 8px;
            }
            QLabel {
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                color: #5a5c69;
                font-weight: bold;
                margin-bottom: 5px;
            }
            QLineEdit, QComboBox {
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                border: 1px solid #d1d3e2;
                border-radius: 6px;
                padding: 8px;
                background-color: white;
                min-height: 36px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #4e73df;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left-width: 1px;
                border-left-color: #d1d3e2;
                border-left-style: solid;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }
            QPushButton {
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 6px;
                min-width: 100px;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
        """)

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Header avec icône
        header = QLabel("Add New Category")
        header.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #4e73df;
            qproperty-alignment: AlignCenter;
        """)
        main_layout.addWidget(header)

        # Formulaire
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # Nom de la catégorie
        name_group = QVBoxLayout()
        name_label = QLabel("Category Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Work, Personal, Projects...")
        self.name_input.setStyleSheet("padding: 8px;")
        name_group.addWidget(name_label)
        name_group.addWidget(self.name_input)
        form_layout.addLayout(name_group)

        # Couleur
        color_group = QVBoxLayout()
        color_label = QLabel("Color:")
        self.color_combo = QComboBox()
        self.color_combo.setIconSize(QSize(16, 16))
        
        # Ajout des options de couleur avec icônes colorées
        colors = [
            ("🔵 Blue", "#4e73df"),
            ("🔴 Red", "#e74a3b"),
            ("🟢 Green", "#1cc88a"),
            ("🟡 Yellow", "#f6c23e"),
            ("🟣 Purple", "#6f42c1"),
            ("🟦 Cyan", "#36b9cc")
        ]
        
        for text, color in colors:
            self.color_combo.addItem(text, color)
            # Colorer l'icône du combo box
            self.color_combo.setItemData(self.color_combo.count()-1, QColor(color), Qt.DecorationRole)
        
        color_group.addWidget(color_label)
        color_group.addWidget(self.color_combo)
        form_layout.addLayout(color_group)

        main_layout.addLayout(form_layout)

        # Boutons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        btn_layout.addStretch()

        # Bouton Annuler
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setIcon(QIcon.fromTheme("dialog-cancel"))
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #e74a3b;
                color: white;
            }
            QPushButton:hover {
                background-color: #d62c1a;
            }
        """)
        self.btn_cancel.clicked.connect(self.reject)

        # Bouton Valider
        self.btn_validate = QPushButton("Create")
        self.btn_validate.setIcon(QIcon.fromTheme("dialog-ok"))
        self.btn_validate.setStyleSheet("""
            QPushButton {
                background-color: #1cc88a;
                color: white;
            }
            QPushButton:hover {
                background-color: #18b280;
            }
        """)
        self.btn_validate.clicked.connect(self.validate)

        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_validate)
        main_layout.addLayout(btn_layout)

    def validate(self):
        name = self.name_input.text().strip()
        color = self.color_combo.currentData()

        if not name:
            QMessageBox.warning(self, "Error", "Please enter a name for the category")
            return

        success = self.db.add_category(name, color)
        if success:
            if self.parent:
                self.parent.load_categories()
            self.accept()  # Ferme le dialogue avec le statut Accepté
        else:
            QMessageBox.warning(self, "Error", "A category with this name already exists!")

from PyQt5.QtWidgets import QDialog  # Ajout de l'import
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox,
    QMessageBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class EditLinkDialog(QDialog):
    def __init__(self, db, link_id=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.link_id = link_id
        self.parent = parent

        self.setWindowTitle("Edit Link" if link_id else "Add Link")
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(500, 520)

        self.set_main_style()
        self.init_ui()

        if self.link_id:
            self.load_data()

    def set_main_style(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fc;
            }
            QLabel {
                font-family: 'Segoe UI';
                font-size: 13px;
                font-weight: 600;
                color: #4e73df;
            }
            QLineEdit, QComboBox {
                border: 1px solid #d1d3e2;
                border-radius: 6px;
                padding: 6px;
                background-color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 13px;
            }
            QCheckBox {
                font-family: 'Segoe UI';
                font-size: 13px;
                padding: 6px 0;
                color: #5a5c69;
            }
            QPushButton {
                font-family: 'Segoe UI';
                font-size: 13px;
                font-weight: bold;
                padding: 8px 18px;
                border-radius: 6px;
            }
        """)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(15)

        # Widgets
        self.category_combo = QComboBox()
        self.category_combo.setEditable(True)

        self.title_input = QLineEdit()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://")

        self.username_input = QLineEdit()
        self.password_input = PasswordEdit()

        self.favorite_check = QCheckBox("Mark as favorite")
        self.tags_input = QLineEdit()

        # Ajout des lignes
        form_layout.addRow("Category:", self.category_combo)
        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("URL:", self.url_input)
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("Tags (comma separated):", self.tags_input)
        form_layout.addRow("", self.favorite_check)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(self.setup_buttons())

        self.load_categories()

    def setup_buttons(self):
        layout = QHBoxLayout()

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setIcon(QIcon.fromTheme("dialog-cancel"))
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #e74a3b;
                color: white;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.btn_cancel.clicked.connect(self.reject)

        self.btn_validate = QPushButton("Validate")
        self.btn_validate.setIcon(QIcon.fromTheme("dialog-ok"))
        self.btn_validate.setStyleSheet("""
            QPushButton {
                background-color: #1cc88a;
                color: white;
            }
            QPushButton:hover {
                background-color: #17a673;
            }
        """)
        self.btn_validate.clicked.connect(self.validate)

        layout.addStretch()
        layout.addWidget(self.btn_cancel)
        layout.addWidget(self.btn_validate)

        return layout

    def load_categories(self):
        self.category_combo.clear()
        categories = self.db.get_categories()
        for cat_id, name, color in categories:
            self.category_combo.addItem(name, cat_id)

    def load_data(self):
        links = self.db.get_links_by_category()
        for link in links:
            if link[0] == self.link_id:
                index = self.category_combo.findData(link[6])
                if index >= 0:
                    self.category_combo.setCurrentIndex(index)
                self.title_input.setText(link[1])
                self.url_input.setText(link[2])
                self.username_input.setText(link[3] or "")
                self.password_input.setText(link[4] or "")
                self.favorite_check.setChecked(bool(link[5]))
                tag_names = [tag[1] for tag in link[8]]
                self.tags_input.setText(", ".join(tag_names))
                break

    def validate(self):
        title = self.title_input.text().strip()
        url = self.url_input.text().strip()
        
        if not title or not url:
            QMessageBox.warning(self, "Error", "Please fill at least the title and URL.")
            return

        category_index = self.category_combo.currentIndex()
        username = self.username_input.text().strip()
        password = self.password_input.text()
        favorite = int(self.favorite_check.isChecked())
        tags = [tag.strip() for tag in self.tags_input.text().split(",") if tag.strip()]
        category_id = self.category_combo.itemData(category_index)

        if self.link_id:
            self.db.update_link(self.link_id, title, url, username, password, favorite, category_id, tags)
        else:
            self.db.add_link(title, url, username, password, favorite, category_id, tags)

        if self.parent:
            self.parent.load_links()

        self.accept()

class MainWindowLink(QMainWindow):
    def __init__(self, main_app=None):
        super().__init__()
        self.main_app = main_app

        self.db = DatabaseManager()
        self.browser = None
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save)
        self.auto_save_timer.start(30000)  # Save every 30 seconds
        
        self.setWindowTitle("Useful Links Manager")
        self.setGeometry(100, 100, 1200, 800)
        
        self.setup_ui()
        self.setup_menu()
        self.load_categories()
        self.load_links()
        
    def setup_menu(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        export_action = QAction("Export links", self)
        export_action.setShortcut(QKeySequence("Ctrl+E"))
        export_action.triggered.connect(self.export_links)
        file_menu.addAction(export_action)
        
        import_action = QAction("Import links", self)
        import_action.setShortcut(QKeySequence("Ctrl+I"))
        import_action.triggered.connect(self.import_links)
        file_menu.addAction(import_action)
        
        # New delete all action
        delete_all_action = QAction("Delete All", self)
        delete_all_action.setShortcut(QKeySequence("Ctrl+D"))
        delete_all_action.triggered.connect(self.delete_all_links)
        file_menu.addAction(delete_all_action)
        
        file_menu.addSeparator()
        
        backup_action = QAction("Auto backup", self, checkable=True)
        backup_action.setChecked(True)
        backup_action.triggered.connect(self.toggle_auto_save)
        file_menu.addAction(backup_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("Quit", self)
        quit_action.setShortcut(QKeySequence.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        add_link_action = QAction("Add link", self)
        add_link_action.setShortcut(QKeySequence("Ctrl+N"))
        add_link_action.triggered.connect(self.add_link_dialog)
        edit_menu.addAction(add_link_action)
        
        add_cat_action = QAction("Add category", self)
        add_cat_action.setShortcut(QKeySequence("Ctrl+Shift+N"))
        add_cat_action.triggered.connect(self.add_category_dialog)
        edit_menu.addAction(add_cat_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        self.show_fav_action = QAction("Show only favorites", self, checkable=True)
        self.show_fav_action.setShortcut(QKeySequence("Ctrl+F"))
        self.show_fav_action.triggered.connect(self.toggle_favorites_view)
        view_menu.addAction(self.show_fav_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_ui(self):
        # Global style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fc;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #e3e6f0;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #4e73df;
                outline: none;
            }
            QGroupBox {
                border: 1px solid #e3e6f0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: bold;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QListWidget {
                border: none;
                outline: none;
                background-color: white;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e3e6f0;
            }
            QListWidget::item:hover {
                background-color: #f8f9fa;
            }
            QListWidget::item:selected {
                background-color: #4e73df;
                color: white;
                border-radius: 4px;
            }
        """)
        
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Left part - Form
        left_widget = QWidget()
        left_widget.setFixedWidth(350)
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(15)
        
        # Title with gradient
        title = GradientLabel("Links Manager")
        left_layout.addWidget(title)
        
        # Add Link button
        self.btn_add_link = FadeButton("Add Link")
        self.btn_add_link.setIcon(QIcon.fromTheme("list-add"))
        self.btn_add_link.setStyleSheet("""
            QPushButton {
                background-color: #4e73df;
                color: white;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a5bc7;
            }
        """)
        self.btn_add_link.clicked.connect(self.add_link_dialog)
        left_layout.addWidget(self.btn_add_link)
        
        # Add Category button
        self.btn_add_category = FadeButton("Add Category")
        self.btn_add_category.setIcon(QIcon.fromTheme("folder-new"))
        self.btn_add_category.setStyleSheet("""
            QPushButton {
                background-color: #36b9cc;
                color: white;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2a9faf;
            }
        """)
        self.btn_add_category.clicked.connect(self.add_category_dialog)
        left_layout.addWidget(self.btn_add_category)
        
        # Categories list
        categories_group = QGroupBox("Categories")
        categories_group.setStyleSheet("""
            QGroupBox {
                margin-top: 10px;
            }
        """)
        categories_layout = QVBoxLayout(categories_group)
        
        self.categories_list = QListWidget()
        self.categories_list.setIconSize(QSize(16, 16))
        self.categories_list.itemClicked.connect(self.filter_by_category)
        
        categories_layout.addWidget(self.categories_list)
        left_layout.addWidget(categories_group)
        
        # Filters
        filters_group = QGroupBox("Filters")
        filters_layout = QVBoxLayout(filters_group)
        
        self.favorites_check = QCheckBox("Favorites only")
        self.favorites_check.stateChanged.connect(self.filter_by_favorites)
        
        self.search_label = QLabel("Quick search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Title, URL, category...")
        self.search_input.textChanged.connect(self.filter_links)
        
        filters_layout.addWidget(self.favorites_check)
        filters_layout.addWidget(self.search_label)
        filters_layout.addWidget(self.search_input)
        left_layout.addWidget(filters_group)
        
        left_layout.addStretch()
        
        # Right part - Links list
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(15)
        
        # Toolbar
        toolbar = QWidget()
        toolbar.setStyleSheet("background-color: white; border-radius: 8px; padding: 10px;")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(5, 5, 5, 5)
        
        self.results_label = QLabel("All links")
        self.results_label.setStyleSheet("font-weight: bold; color: #4e73df;")
        
        self.btn_all = QToolButton()
        self.btn_all.setIcon(QIcon.fromTheme("view-refresh"))
        self.btn_all.setToolTip("Reset filters")
        self.btn_all.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                border: none;
                padding: 5px;
                border-radius: 4px;
            }
            QToolButton:hover {
                background-color: #f8f9fa;
            }
        """)
        self.btn_all.clicked.connect(self.load_links)
        
        toolbar_layout.addWidget(self.results_label)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.btn_all)
        right_layout.addWidget(toolbar)
        
        # Links list
        self.links_scroll = QScrollArea()
        self.links_scroll.setWidgetResizable(True)
        
        self.links_container = QWidget()
        self.links_container.setStyleSheet("background-color: transparent;")
        self.links_layout = QVBoxLayout(self.links_container)
        self.links_layout.setContentsMargins(0, 0, 5, 0)
        self.links_layout.setSpacing(10)
        self.links_layout.addStretch()
        
        self.links_scroll.setWidget(self.links_container)
        right_layout.addWidget(self.links_scroll, 1)
        
        # Add left and right parts
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)
        
        self.setCentralWidget(main_widget)
    def open_link_with_choice1(self, url, link_title):
        """Version avec mémorisation du choix"""
        # Vérifier s'il y a un choix mémorisé
        remember = hasattr(self, 'link_open_preference')
        
        if remember:
            if self.link_open_preference == "browser":
                webbrowser.open(url)
            else:
                self.open_in_app(url, link_title)
            return
            
        # Sinon demander avec option "Toujours utiliser ce choix"
        msg = QMessageBox()
        msg.setWindowTitle("Ouvrir le lien")
        msg.setText(f"Comment ouvrir {link_title}?")
        
        browser_btn = msg.addButton("Navigateur", QMessageBox.ActionRole)
        app_btn = msg.addButton("Application", QMessageBox.ActionRole)
        remember_btn = msg.addButton("Toujours dans l'application", QMessageBox.ActionRole)
        msg.addButton(QMessageBox.Cancel)
        
        msg.exec_()
        
        if msg.clickedButton() == browser_btn:
            webbrowser.open(url)
        elif msg.clickedButton() in (app_btn, remember_btn):
            self.open_in_app(url, link_title)
            if msg.clickedButton() == remember_btn:
                self.link_open_preference = "app"

    def open_link_with_choice(self, link_data):
        """Ouvre un lien avec choix et gestion des identifiants"""
        url = link_data['url']
        title = link_data['title']
        
        if hasattr(self, 'link_open_preference'):
            if self.link_open_preference == "browser":
                webbrowser.open(url)
            else:
                self.open_in_app(url, link_data)
            return
        
        msg = QMessageBox()
        msg.setWindowTitle("Ouvrir le lien")
        msg.setText(f"Comment ouvrir {title}?")
        
        browser_btn = msg.addButton("Navigateur", QMessageBox.ActionRole)
        app_btn = msg.addButton("Application (auto-login)", QMessageBox.ActionRole)
        remember_app_btn = msg.addButton("Toujours dans l'app (avec login)", QMessageBox.ActionRole)
        msg.addButton(QMessageBox.Cancel)
        
        msg.exec_()
        
        if msg.clickedButton() == browser_btn:
            webbrowser.open(url)
        elif msg.clickedButton() == app_btn:
            self.open_in_app(url, link_data)
        elif msg.clickedButton() == remember_app_btn:
            self.link_open_preference = "app"
            self.open_in_app(url, link_data)
                            
    def find_tab_by_name1(self, name):
        """Trouve l'index d'un onglet par son nom"""
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == name:
                return i
        return -1

    def find_tab_by_name(self, name):
        for i in range(self.main_app.tab_widget.count()):
            if self.main_app.tab_widget.tabText(i) == name:
                return i  # Renvoie l'index si trouvé
        return -1  # Aucun onglet trouvé
    def open_in_app(self, url, link_data):
        """Ouvre le lien dans l'application avec authentification automatique"""
        tab_name = link_data['title']
        existing_tab_index = self.find_tab_by_name(tab_name)
        
        if existing_tab_index != -1:
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return

        web_view = QWebEngineView()
        page = web_view.page()
        profile = page.profile()
        
        # Stocker les cookies avant la navigation
        cookie_store = profile.cookieStore()
        cookie_store.deleteAllCookies()  # Nettoyer les cookies existants
        
        # Injecter les identifiants si disponibles
        if link_data.get('username') and link_data.get('password'):
            self.setup_auto_login(web_view, link_data)
        
        web_view.setUrl(QUrl(url))
        self.main_app.tab_widget.addTab(web_view, tab_name)
        self.main_app.tab_widget.setCurrentIndex(self.main_app.tab_widget.count() - 1)

    def open_in_app2(self, url, tab_name):
        """Ouvre le lien dans un nouvel onglet de l'application"""
        # Vérifie si l'onglet existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return
        
        # Crée un QWebEngineView pour afficher la page
        web_view = QWebEngineView()
        web_view.setUrl(QUrl(url))
        
        # Ajoute un nouvel onglet
        self.main_app.tab_widget.addTab(web_view, tab_name)
        self.main_app.tab_widget.setCurrentIndex(self.main_app.tab_widget.count() - 1)                

    def load_categories(self):
        self.categories_list.clear()
        
        categories = self.db.get_categories()
        for cat_id, name, color in categories:
            item = QListWidgetItem(QIcon.fromTheme("folder"), name)
            item.setData(Qt.UserRole, cat_id)
            item.setData(Qt.UserRole + 1, color)
            self.categories_list.addItem(item)
    def load_links(self, category_id=None, favorite=None):
        # Clear the current layout
        while self.links_layout.count() > 1:  # Keep the stretch
            item = self.links_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
                
        if favorite is None and self.favorites_check.isChecked():
            favorite = True
            
        search_query = self.search_input.text().strip() or None
        links = self.db.get_links_by_category(category_id, favorite, search_query)
        
        # Update results label
        if category_id:
            # Find category name by iterating through the categories list
            cat_name = None
            for i in range(self.categories_list.count()):
                item = self.categories_list.item(i)
                if item.data(Qt.UserRole) == category_id:
                    cat_name = item.text()
                    break
            if cat_name:
                self.results_label.setText(f"Links in '{cat_name}'")
            else:
                self.results_label.setText(f"Links in category ID: {category_id}")
        elif favorite:
            self.results_label.setText("Favorite links")
        elif search_query:
            self.results_label.setText(f"Results for '{search_query}'")
        else:
            self.results_label.setText("All links")
            
        if not links:
            no_results = QLabel("No links found")
            no_results.setAlignment(Qt.AlignCenter)
            no_results.setStyleSheet("color: #6c757d; font-style: italic; padding: 20px;")
            self.links_layout.insertWidget(0, no_results)
            return
            
        current_category = None
        for link in links:
            link_id, title, url, username, password, favorite, category, category_color, tags = link
            
            if category != current_category and not self.favorites_check.isChecked() and not search_query:
                current_category = category
                cat_widget = CategoryWidget(
                    next(cat_id for cat_id, name, color in self.db.get_categories() if name == category),
                    category,
                    category_color,
                    self
                )
                self.links_layout.insertWidget(self.links_layout.count()-1, cat_widget)
                
            link_widget = LinkWidget(link_id, title, url, category, category_color, 
                                username, password, favorite, tags, self)
            link_widget.edit_requested.connect(self.edit_link_dialog)
            link_widget.tag_clicked.connect(self.filter_by_tag)
            self.links_layout.insertWidget(self.links_layout.count()-1, link_widget)            
    def load_links1(self, category_id=None, favorite=None):
        # Clear the current layout
        while self.links_layout.count() > 1:  # Keep the stretch
            item = self.links_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
                
        if favorite is None and self.favorites_check.isChecked():
            favorite = True
            
        search_query = self.search_input.text().strip() or None
        links = self.db.get_links_by_category(category_id, favorite, search_query)
        
        # Update results label
        if category_id:
            cat_name = next(item.text() for i in range(self.categories_list.count()) 
                         if self.categories_list.item(i).data(Qt.UserRole) == category_id)
            self.results_label.setText(f"Links in '{cat_name}'")
        elif favorite:
            self.results_label.setText("Favorite links")
        elif search_query:
            self.results_label.setText(f"Results for '{search_query}'")
        else:
            self.results_label.setText("All links")
            
        if not links:
            no_results = QLabel("No links found")
            no_results.setAlignment(Qt.AlignCenter)
            no_results.setStyleSheet("color: #6c757d; font-style: italic; padding: 20px;")
            self.links_layout.insertWidget(0, no_results)
            return
            
        current_category = None
        for link in links:
            link_id, title, url, username, password, favorite, category, category_color, tags = link
            
            if category != current_category and not self.favorites_check.isChecked() and not search_query:
                current_category = category
                cat_widget = CategoryWidget(
                    next(cat_id for cat_id, name, color in self.db.get_categories() if name == category),
                    category,
                    category_color,
                    self
                )
                self.links_layout.insertWidget(self.links_layout.count()-1, cat_widget)
                
            link_widget = LinkWidget(link_id, title, url, category, category_color, 
                                   username, password, favorite, tags, self)
            link_widget.edit_requested.connect(self.edit_link_dialog)
            link_widget.tag_clicked.connect(self.filter_by_tag)
            self.links_layout.insertWidget(self.links_layout.count()-1, link_widget)
            
    def filter_by_category(self, item):
        cat_id = item.data(Qt.UserRole)
        self.load_links(cat_id)
        
    def filter_by_tag(self, tag):
        self.search_input.setText(tag)
        self.filter_links(tag)
        
    def filter_by_favorites(self, state):
        self.load_links(favorite=state == Qt.Checked)
        
    def toggle_favorites_view(self, checked):
        self.favorites_check.setChecked(checked)
        self.filter_by_favorites(Qt.Checked if checked else Qt.Unchecked)
        
    def filter_links(self, text):
        text = text.lower()
        
        for i in range(self.links_layout.count()):
            widget = self.links_layout.itemAt(i).widget()
            if widget:
                if isinstance(widget, CategoryWidget):
                    # Hide category if no visible links below
                    has_visible = False
                    j = i + 1
                    while j < self.links_layout.count():
                        next_widget = self.links_layout.itemAt(j).widget()
                        if not next_widget or isinstance(next_widget, CategoryWidget):
                            break
                        if next_widget.isVisible():
                            has_visible = True
                            break
                        j += 1
                    widget.setVisible(has_visible)
                elif isinstance(widget, LinkWidget):
                    visible = (text in widget.title_label.text().lower() or 
                              text in widget.url_label.text().lower() or 
                              text in widget.category_label.text().lower() or
                              any(text in tag[1].lower() for tag in widget.tags))
                    widget.setVisible(visible)
                    
    def add_link_dialog(self):
        dialog = EditLinkDialog(self.db, parent=self)
        if dialog.exec_() == QDialog.Accepted:
           self.load_links()

            # dialog.show()
    def setup_auto_login(self, web_view, link_data):
        """Configure l'auto-login via JavaScript"""
        username = link_data['username']
        password = link_data['password']
        
        # Script JavaScript pour remplir le formulaire
        login_script = f"""
        function tryLogin() {{
            // Tentative de trouver les champs de connexion
            let usernameFields = [
                document.querySelector('input[type="email"]'),
                document.querySelector('input[type="text"][name*="user"]'),
                document.querySelector('input[name*="login"]'),
                document.querySelector('input[id*="user"]')
            ].filter(Boolean);
            
            let passwordFields = [
                document.querySelector('input[type="password"]'),
                document.querySelector('input[name*="pass"]'),
                document.querySelector('input[id*="pass"]')
            ].filter(Boolean);
            
            if (usernameFields.length > 0 && passwordFields.length > 0) {{
                // Remplir les champs
                usernameFields[0].value = '{username}';
                passwordFields[0].value = '{password}';
                
                // Trouver et cliquer sur le bouton de connexion
                let loginButtons = [
                    document.querySelector('button[type="submit"]'),
                    document.querySelector('input[type="submit"]'),
                    document.querySelector('button[id*="login"]')
                ].filter(Boolean);
                
                if (loginButtons.length > 0) {{
                    loginButtons[0].click();
                }}
                
                return true;
            }}
            return false;
        }}
        
        // Essai immédiat puis toutes les secondes pendant 5 secondes
        if (!tryLogin()) {{
            let attempts = 0;
            const interval = setInterval(() => {{
                if (tryLogin() || attempts >= 5) {{
                    clearInterval(interval);
                }}
                attempts++;
            }}, 1000);
        }}
        """
        
        # Exécuter le script lorsque la page est chargée
        web_view.loadFinished.connect(
            lambda: web_view.page().runJavaScript(login_script)
        )        
    def add_category_dialog(self):
        dialog = AddCategoryDialog(self.db, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            # La catégorie a été créée avec succès
            self.load_categories()        
    def edit_link_dialog(self, link_id):
        dialog = EditLinkDialog(self.db, link_id, parent=self)
        if dialog.exec_() == QDialog.Accepted:
           self.load_links()
        # dialog.show()
                
    def visit_link(self, url, new_tab=False):
        if not hasattr(self, 'browser') or not self.browser or new_tab:
            self.browser = QWebEngineView()
            self.browser.setWindowTitle("Browser - Links Manager")
            self.browser.resize(1000, 700)
            
        self.browser.load(url)
        self.browser.show()
        self.browser.activateWindow()
    def visit_link2(self, url, new_tab=False):
        if not hasattr(self, 'browser') or not self.browser or new_tab:
            self.browser = QWebEngineView()
            self.browser.setWindowTitle("Browser - Links Manager")
            self.browser.resize(1000, 700)
        
        # Convertir l'URL string en QUrl
        from PyQt5.QtCore import QUrl
        qurl = QUrl(url)
        
        # Vérifier que l'URL est valide
        if not qurl.isValid():
            qurl = QUrl("http://" + url)  # Essayer avec http:// si l'URL n'est pas valide
        
        self.browser.load(qurl)
        self.browser.show()
        self.browser.activateWindow()        
    def export_links(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export links",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if filename:
            if not filename.endswith('.json'):
                filename += '.json'
                
            try:
                self.db.export_links(filename)
                QMessageBox.information(self, "Success", "Links exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred during export:\n{str(e)}")
                
    def import_links(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Import links",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if filename:
            try:
                self.db.import_links(filename)
                self.load_categories()
                self.load_links()
                QMessageBox.information(self, "Success", "Links imported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred during import:\n{str(e)}")
                
    def delete_all_links(self):
        reply = QMessageBox.question(
            self, 'Confirmation', 
            "Are you sure you want to delete ALL links and categories? This action cannot be undone!",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Delete all data
                self.db.delete_all_data()
                
                # Restore default data
                self.db.initialize_default_data()
                
                # Reload interface
                self.load_categories()
                self.load_links()
                
                QMessageBox.information(self, "Success", "All data has been deleted and default data restored.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
                
    def auto_save(self):
        # Auto-save data
        try:
            self.db.conn.commit()
        except Exception as e:
            print(f"Error during auto-save: {e}")
            
    def toggle_auto_save(self, enabled):
        if enabled:
            self.auto_save_timer.start(30000)
        else:
            self.auto_save_timer.stop()
            
    def closeEvent(self, event):
        # Final save on close
        self.auto_save()
        event.accept()
        
    def show_about(self):
        about = QMessageBox(self)
        about.setWindowTitle("About")
        about.setIconPixmap(QIcon.fromTheme("help-about").pixmap(64, 64))
        about.setText("""
            <h2>Useful Links Manager</h2>
            <p>Version 3.0</p>
            <p>An application to organize and easily access your favorite web links.</p>
            <p><b>Features:</b></p>
            <ul>
                <li>Organization by categories and tags</li>
                <li>Secure storage of credentials</li>
                <li>Integrated browser</li>
                <li>Import/Export data</li>
                <li>Auto backup</li>
                <li>Modern and intuitive interface</li>
            </ul>
            <p>© 2023 - All rights reserved</p>
        """)
        about.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Fusion style with customization
    app.setStyle("Fusion")
    
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(248, 249, 252))
    palette.setColor(QPalette.WindowText, QColor(58, 59, 64))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(248, 249, 252))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(58, 59, 64))
    palette.setColor(QPalette.Text, QColor(58, 59, 64))
    palette.setColor(QPalette.Button, QColor(78, 115, 223))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.Highlight, QColor(78, 115, 223))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    # Default font
    font = QFont()
    font.setFamily("Segoe UI" if sys.platform == "win32" else "Arial")
    font.setPointSize(10)
    app.setFont(font)
    
    window = MainWindowLink()
    window.show()
    sys.exit(app.exec_())