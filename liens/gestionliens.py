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
class PasswordEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEchoMode(QLineEdit.Password)
        self.toggle_password_action = self.addAction(QIcon(":/icons/eye-off.svg"), QLineEdit.TrailingPosition)
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
            }
        """)

    def toggle_password_visibility(self):
        if self.password_visible:
            self.setEchoMode(QLineEdit.Password)
            self.toggle_password_action.setIcon(QIcon(":/icons/eye-off.svg"))
            self.password_visible = False
        else:
            self.setEchoMode(QLineEdit.Normal)
            self.toggle_password_action.setIcon(QIcon(":/icons/eye.svg"))
            self.password_visible = True

class FadeButton(QPushButton):
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

class GradientLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._gradient = QLinearGradient(0, 0, 0, 1)
        self._gradient.setColorAt(0, QColor("#4e73df"))
        self._gradient.setColorAt(1, QColor("#224abe"))

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
        
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT UNIQUE NOT NULL,
                color TEXT DEFAULT '#4e73df'
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT UNIQUE NOT NULL,
                color TEXT DEFAULT '#858796'
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lien_tags (
                lien_id INTEGER,
                tag_id INTEGER,
                PRIMARY KEY (lien_id, tag_id),
                FOREIGN KEY (lien_id) REFERENCES liens(id),
                FOREIGN KEY (tag_id) REFERENCES tags(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS liens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                url TEXT NOT NULL,
                identifiant TEXT,
                mot_de_passe TEXT,
                favori BOOLEAN DEFAULT 0,
                categorie_id INTEGER,
                date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (categorie_id) REFERENCES categories(id)
            )
        ''')
        self.conn.commit()
        
    def ajouter_categorie(self, nom, color="#4e73df"):
        cursor = self.conn.cursor()
        try:
            cursor.execute('INSERT INTO categories (nom, color) VALUES (?, ?)', (nom, color))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return False
            
    def get_categories(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, nom, color FROM categories ORDER BY nom')
        return cursor.fetchall()
        
    def ajouter_tag(self, nom, color="#858796"):
        cursor = self.conn.cursor()
        try:
            cursor.execute('INSERT INTO tags (nom, color) VALUES (?, ?)', (nom, color))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            cursor.execute('SELECT id FROM tags WHERE nom = ?', (nom,))
            return cursor.fetchone()[0]
            
    def get_tags(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, nom, color FROM tags ORDER BY nom')
        return cursor.fetchall()
        
    def get_tags_for_lien(self, lien_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT t.id, t.nom, t.color 
            FROM tags t
            JOIN lien_tags lt ON t.id = lt.tag_id
            WHERE lt.lien_id = ?
        ''', (lien_id,))
        return cursor.fetchall()
        
    def update_lien_tags(self, lien_id, tags):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM lien_tags WHERE lien_id = ?', (lien_id,))
        
        for tag in tags:
            if isinstance(tag, tuple):
                tag_id = self.ajouter_tag(tag[0], tag[1])
            else:
                tag_id = self.ajouter_tag(tag)
            cursor.execute('INSERT INTO lien_tags (lien_id, tag_id) VALUES (?, ?)', (lien_id, tag_id))
            
        self.conn.commit()
        
    def ajouter_lien(self, titre, url, categorie_id, identifiant=None, mot_de_passe=None, favori=False, tags=None):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO liens (titre, url, categorie_id, identifiant, mot_de_passe, favori) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (titre, url, categorie_id, identifiant, mot_de_passe, favori))
        lien_id = cursor.lastrowid
        
        if tags:
            self.update_lien_tags(lien_id, tags)
            
        self.conn.commit()
        return lien_id
        
    def modifier_lien(self, lien_id, titre, url, categorie_id, identifiant=None, mot_de_passe=None, favori=None, tags=None):
        cursor = self.conn.cursor()
        
        if favori is not None:
            cursor.execute('''
                UPDATE liens 
                SET titre = ?, url = ?, categorie_id = ?, identifiant = ?, mot_de_passe = ?, favori = ?
                WHERE id = ?
            ''', (titre, url, categorie_id, identifiant, mot_de_passe, favori, lien_id))
        else:
            cursor.execute('''
                UPDATE liens 
                SET titre = ?, url = ?, categorie_id = ?, identifiant = ?, mot_de_passe = ?
                WHERE id = ?
            ''', (titre, url, categorie_id, identifiant, mot_de_passe, lien_id))
            
        if tags is not None:
            self.update_lien_tags(lien_id, tags)
            
        self.conn.commit()
        
    def get_liens_par_categorie(self, categorie_id=None, favori=None, search_query=None):
        cursor = self.conn.cursor()
        query = '''
            SELECT l.id, l.titre, l.url, l.identifiant, l.mot_de_passe, l.favori, c.nom, c.color 
            FROM liens l 
            JOIN categories c ON l.categorie_id = c.id 
        '''
        params = []
        
        conditions = []
        if categorie_id:
            conditions.append("l.categorie_id = ?")
            params.append(categorie_id)
        if favori is not None:
            conditions.append("l.favori = ?")
            params.append(favori)
        if search_query:
            conditions.append("(l.titre LIKE ? OR l.url LIKE ? OR c.nom LIKE ?)")
            params.extend([f"%{search_query}%"] * 3)
            
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        query += " ORDER BY c.nom, l.titre"
        cursor.execute(query, params)
            
        liens = cursor.fetchall()
        
        # Récupérer les tags pour chaque lien
        result = []
        for lien in liens:
            tags = self.get_tags_for_lien(lien[0])
            result.append((*lien, tags))
            
        return result
        
    def supprimer_lien(self, lien_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM lien_tags WHERE lien_id = ?', (lien_id,))
        cursor.execute('DELETE FROM liens WHERE id = ?', (lien_id,))
        self.conn.commit()
        
    def supprimer_categorie(self, categorie_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM categories WHERE id = ?', (categorie_id,))
        cursor.execute('DELETE FROM liens WHERE categorie_id = ?', (categorie_id,))
        self.conn.commit()
        
    def exporter_liens(self, filename):
        liens = self.get_liens_par_categorie()
        data = []
        
        for lien in liens:
            data.append({
                'id': lien[0],
                'titre': lien[1],
                'url': lien[2],
                'identifiant': lien[3],
                'mot_de_passe': lien[4],
                'favori': bool(lien[5]),
                'categorie': lien[6],
                'categorie_color': lien[7],
                'tags': [{'nom': tag[1], 'color': tag[2]} for tag in lien[8]]
            })
            
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def importer_liens(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            
        for item in data:
            # Trouver ou créer la catégorie
            cursor = self.conn.cursor()
            cursor.execute('SELECT id FROM categories WHERE nom = ?', (item['categorie'],))
            categorie = cursor.fetchone()
            
            if not categorie:
                self.ajouter_categorie(item['categorie'], item.get('categorie_color', '#4e73df'))
                cursor.execute('SELECT id FROM categories WHERE nom = ?', (item['categorie'],))
                categorie_id = cursor.fetchone()[0]
            else:
                categorie_id = categorie[0]
                
            # Vérifier si le lien existe déjà
            cursor.execute('SELECT id FROM liens WHERE titre = ? AND url = ?', (item['titre'], item['url']))
            existing = cursor.fetchone()
            
            if not existing:
                tags = [(tag['nom'], tag.get('color', '#858796')) for tag in item.get('tags', [])]
                self.ajouter_lien(
                    titre=item['titre'],
                    url=item['url'],
                    categorie_id=categorie_id,
                    identifiant=item.get('identifiant'),
                    mot_de_passe=item.get('mot_de_passe'),
                    favori=item.get('favori', False),
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
    
    def __init__(self, lien_id, titre, url, categorie, categorie_color, 
                 identifiant=None, mot_de_passe=None, favori=False, tags=None, parent=None):
        super().__init__(parent)
        self.lien_id = lien_id
        self.url = url
        self.parent = parent
        self.mot_de_passe = mot_de_passe
        self.mot_de_passe_visible = False
        self.tags = tags or []
        self.categorie_color = categorie_color
        
        self.setup_ui(titre, categorie, identifiant, favori)
        
    def setup_ui(self, titre, categorie, identifiant, favori):
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
        
        # Header avec titre et boutons
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Titre et favori
        title_fav = QWidget()
        title_fav_layout = QHBoxLayout(title_fav)
        title_fav_layout.setContentsMargins(0, 0, 0, 0)
        
        self.fav_btn = QPushButton()
        self.fav_btn.setFixedSize(24, 24)
        self.fav_btn.setFlat(True)
        self.fav_btn.setIcon(QIcon.fromTheme("emblem-favorite" if favori else "emblem-default"))
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
        self.fav_btn.clicked.connect(self.toggle_favori)
        
        self.titre_label = QLabel(titre)
        self.titre_label.setFont(QFont('Arial', 10, QFont.Bold))
        self.titre_label.setStyleSheet("color: #2e59d9;")
        
        title_fav_layout.addWidget(self.fav_btn)
        title_fav_layout.addWidget(self.titre_label, 1)
        title_fav_layout.addStretch()
        
        header_layout.addWidget(title_fav, 1)
        
        # Boutons d'action
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(5)
        
        self.btn_visiter = FadeButton("Visiter")
        self.btn_visiter.setIcon(QIcon.fromTheme("go-jump"))
        self.btn_visiter.setStyleSheet("""
            QPushButton {
                background-color: #4e73df; 
                color: white;
            }
            QPushButton:hover {
                background-color: #3a5bc7;
            }
        """)
        self.btn_visiter.clicked.connect(self.visiter_lien)
        
        self.btn_edit = QPushButton("")
        self.btn_edit.setIcon(QIcon.fromTheme("document-edit"))
        self.btn_edit.setToolTip("Modifier")
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
        self.btn_edit.clicked.connect(lambda: self.edit_requested.emit(self.lien_id))
        
        self.btn_supprimer = QPushButton("")
        self.btn_supprimer.setIcon(QIcon.fromTheme("edit-delete"))
        self.btn_supprimer.setToolTip("Supprimer")
        self.btn_supprimer.setStyleSheet("""
            QPushButton {
                background-color: #e74a3b; 
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #be2617;
            }
        """)
        self.btn_supprimer.clicked.connect(self.supprimer_lien)
        
        btn_layout.addWidget(self.btn_visiter)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_supprimer)
        
        header_layout.addWidget(btn_container)
        
        main_layout.addWidget(header)
        
        # Catégorie et URL
        meta_container = QWidget()
        meta_layout = QVBoxLayout(meta_container)
        meta_layout.setContentsMargins(0, 0, 0, 0)
        meta_layout.setSpacing(4)
        
        # Catégorie
        self.categorie_label = QLabel(f"<small>Catégorie: <span style='color: {self.categorie_color}; font-weight: bold;'>{categorie}</span></small>")
        
        # URL
        self.url_label = QLabel(f"<small>URL: {self.url}</small>")
        self.url_label.setStyleSheet("color: #858796;")
        self.url_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        meta_layout.addWidget(self.categorie_label)
        meta_layout.addWidget(self.url_label)
        
        main_layout.addWidget(meta_container)
        
        # Identifiant et mot de passe
        if identifiant or self.mot_de_passe:
            auth_container = QWidget()
            auth_layout = QVBoxLayout(auth_container)
            auth_layout.setContentsMargins(0, 0, 0, 0)
            auth_layout.setSpacing(4)
            
            # Identifiant
            if identifiant:
                identifiant_group = QWidget()
                identifiant_layout = QHBoxLayout(identifiant_group)
                identifiant_layout.setContentsMargins(0, 0, 0, 0)
                
                identifiant_title = QLabel("<small>Identifiant:</small>")
                identifiant_title.setStyleSheet("color: #6c757d; min-width: 70px;")
                
                self.identifiant_value = QLabel(identifiant)
                self.identifiant_value.setStyleSheet("color: #5a5c69;")
                self.identifiant_value.setTextInteractionFlags(Qt.TextSelectableByMouse)
                
                btn_copy_id = QPushButton("")
                btn_copy_id.setIcon(QIcon.fromTheme("edit-copy"))
                btn_copy_id.setToolTip("Copier")
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
                btn_copy_id.clicked.connect(lambda: QApplication.clipboard().setText(identifiant))
                
                identifiant_layout.addWidget(identifiant_title)
                identifiant_layout.addWidget(self.identifiant_value, 1)
                identifiant_layout.addWidget(btn_copy_id)
                
                auth_layout.addWidget(identifiant_group)
            
            # Mot de passe
            if self.mot_de_passe:
                password_group = QWidget()
                password_layout = QHBoxLayout(password_group)
                password_layout.setContentsMargins(0, 0, 0, 0)
                
                password_title = QLabel("<small>Mot de passe:</small>")
                password_title.setStyleSheet("color: #6c757d; min-width: 70px;")
                
                self.password_value = QLabel("••••••••")
                self.password_value.setStyleSheet("color: #5a5c69;")
                
                btn_container = QWidget()
                btn_pass_layout = QHBoxLayout(btn_container)
                btn_pass_layout.setContentsMargins(0, 0, 0, 0)
                btn_pass_layout.setSpacing(2)
                
                btn_show_pass = QPushButton("")
                btn_show_pass.setIcon(QIcon.fromTheme("visibility-off"))
                btn_show_pass.setToolTip("Afficher")
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
                btn_copy_pass.setToolTip("Copier")
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
                btn_copy_pass.clicked.connect(lambda: QApplication.clipboard().setText(self.mot_de_passe))
                
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
        
    def toggle_favori(self):
        favori = not ("emblem-favorite" in self.fav_btn.icon().name())
        self.parent.db.modifier_lien(
            self.lien_id, 
            favori=favori
        )
        self.fav_btn.setIcon(QIcon.fromTheme("emblem-favorite" if favori else "emblem-default"))
        if self.parent.favoris_check.isChecked():
            self.setVisible(favori)
        
    def toggle_password_visibility(self):
        if self.mot_de_passe_visible:
            self.password_value.setText("••••••••")
            self.sender().setIcon(QIcon.fromTheme("visibility-off"))
            self.sender().setToolTip("Afficher")
            self.mot_de_passe_visible = False
        else:
            self.password_value.setText(self.mot_de_passe)
            self.sender().setIcon(QIcon.fromTheme("visibility"))
            self.sender().setToolTip("Masquer")
            self.mot_de_passe_visible = True
            
    def visiter_lien(self):
        self.parent.visiter_lien(self.url)
        
    def supprimer_lien(self):
        reply = QMessageBox.question(
            self, 'Confirmation', 
            f"Voulez-vous vraiment supprimer le lien '{self.titre_label.text()}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.parent.db.supprimer_lien(self.lien_id)
            self.parent.charger_liens()

class CategoryWidget(QWidget):
    def __init__(self, categorie_id, nom, color, parent=None):
        super().__init__(parent)
        self.categorie_id = categorie_id
        self.parent = parent
        self.color = color
        
        self.setup_ui(nom)
        
    def setup_ui(self, nom):
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
        
        self.nom_label = QLabel(nom)
        self.nom_label.setFont(QFont('Arial', 12, QFont.Bold))
        
        self.btn_visiter = FadeButton("Ouvrir tous")
        self.btn_visiter.setIcon(QIcon.fromTheme("go-jump"))
        self.btn_visiter.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color};
                color: white;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(self.color)};
            }}
        """)
        self.btn_visiter.clicked.connect(self.visiter_tous_liens)
        
        self.btn_supprimer = FadeButton("Supprimer")
        self.btn_supprimer.setIcon(QIcon.fromTheme("edit-delete"))
        self.btn_supprimer.setStyleSheet("""
            QPushButton {
                background-color: #e74a3b;
                color: white;
            }
            QPushButton:hover {
                background-color: #be2617;
            }
        """)
        self.btn_supprimer.clicked.connect(self.supprimer_categorie)
        
        layout.addWidget(self.nom_label, 1)
        layout.addWidget(self.btn_visiter)
        layout.addWidget(self.btn_supprimer)
        
        self.setLayout(layout)
        
    def darken_color(self, hex_color, amount=0.2):
        color = QColor(hex_color)
        return color.darker(int(100 + (amount * 100))).name()
        
    def visiter_tous_liens(self):
        liens = self.parent.db.get_liens_par_categorie(self.categorie_id)
        first = True
        for lien in liens:
            self.parent.visiter_lien(lien[2], new_tab=not first)
            first = False
            
    def supprimer_categorie(self):
        reply = QMessageBox.question(
            self, 'Confirmation', 
            f"Voulez-vous vraiment supprimer la catégorie '{self.nom_label.text()}' et tous ses liens?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.parent.db.supprimer_categorie(self.categorie_id)
            self.parent.charger_categories()
            self.parent.charger_liens()



class AddCategoryDialog(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.parent = parent
        
        self.setWindowTitle("➕ Ajouter une catégorie")
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(420, 240)
        self.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QLineEdit, QComboBox {
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 6px;
                background-color: #ffffff;
            }
            QLabel {
                font-weight: bold;
                color: #333;
            }
        """)
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Formulaire
        form_layout = QVBoxLayout()
        form_layout.setSpacing(12)
        
        # Nom
        nom_label = QLabel("Nom de la catégorie :")
        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Ex : Priorité, Personnel, Projet...")
        
        # Couleur
        color_label = QLabel("Couleur :")
        self.color_combo = QComboBox()
        self.color_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.color_combo.addItem("🔵 Bleu", "#4e73df")
        self.color_combo.addItem("🔴 Rouge", "#e74a3b")
        self.color_combo.addItem("🟢 Vert", "#1cc88a")
        self.color_combo.addItem("🟡 Jaune", "#f6c23e")
        self.color_combo.addItem("🟣 Violet", "#6f42c1")
        self.color_combo.addItem("🟦 Cyan", "#36b9cc")
        
        form_layout.addWidget(nom_label)
        form_layout.addWidget(self.nom_input)
        form_layout.addWidget(color_label)
        form_layout.addWidget(self.color_combo)
        
        layout.addLayout(form_layout)
        
        # Boutons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        self.btn_annuler = FadeButton("Annuler")
        self.btn_annuler.setIcon(QIcon.fromTheme("dialog-cancel"))
        self.btn_annuler.setStyleSheet("""
            QPushButton {
                background-color: #e74a3b;
                color: white;
                border-radius: 6px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.btn_annuler.clicked.connect(self.close)

        self.btn_valider = FadeButton("Valider")
        self.btn_valider.setIcon(QIcon.fromTheme("dialog-ok"))
        self.btn_valider.setStyleSheet("""
            QPushButton {
                background-color: #1cc88a;
                color: white;
                border-radius: 6px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #17a673;
            }
        """)
        self.btn_valider.clicked.connect(self.valider)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_annuler)
        btn_layout.addWidget(self.btn_valider)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
    def valider(self):
        nom = self.nom_input.text().strip()
        color = self.color_combo.currentData()
        
        if not nom:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un nom pour la catégorie")
            return
            
        success = self.db.ajouter_categorie(nom, color)
        if success:
            self.parent.charger_categories()
            self.close()
        else:
            QMessageBox.warning(self, "Erreur", "Cette catégorie existe déjà !")

class EditLinkDialog(QWidget):
    def __init__(self, db, lien_id=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.lien_id = lien_id
        self.parent = parent
        
        self.setWindowTitle("Modifier un lien" if lien_id else "Ajouter un lien")
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(500, 500)
        
        self.setup_ui()
        
        if lien_id:
            self.charger_donnees()
            
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Formulaire
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Catégorie
        categorie_label = QLabel("Catégorie:")
        self.categorie_combo = QComboBox()
        self.categorie_combo.setEditable(True)
        
        # Titre
        titre_label = QLabel("Titre:")
        self.titre_input = QLineEdit()
        
        # URL
        url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://")
        
        # Identifiant
        identifiant_label = QLabel("Identifiant:")
        self.identifiant_input = QLineEdit()
        
        # Mot de passe
        mot_de_passe_label = QLabel("Mot de passe:")
        self.mot_de_passe_input = PasswordEdit()
        
        # Favori
        self.favori_check = QCheckBox("Marquer comme favori")
        
        # Tags
        tags_label = QLabel("Tags (séparés par des virgules):")
        self.tags_input = QLineEdit()
        
        form_layout.addWidget(categorie_label)
        form_layout.addWidget(self.categorie_combo)
        form_layout.addWidget(titre_label)
        form_layout.addWidget(self.titre_input)
        form_layout.addWidget(url_label)
        form_layout.addWidget(self.url_input)
        form_layout.addWidget(identifiant_label)
        form_layout.addWidget(self.identifiant_input)
        form_layout.addWidget(mot_de_passe_label)
        form_layout.addWidget(self.mot_de_passe_input)
        form_layout.addWidget(self.favori_check)
        form_layout.addWidget(tags_label)
        form_layout.addWidget(self.tags_input)
        
        layout.addLayout(form_layout, 1)
        
        # Boutons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.btn_valider = FadeButton("Valider")
        self.btn_valider.setIcon(QIcon.fromTheme("dialog-ok"))
        self.btn_valider.setStyleSheet("background-color: #1cc88a; color: white;")
        self.btn_valider.clicked.connect(self.valider)
        
        self.btn_annuler = FadeButton("Annuler")
        self.btn_annuler.setIcon(QIcon.fromTheme("dialog-cancel"))
        self.btn_annuler.setStyleSheet("background-color: #e74a3b; color: white;")
        self.btn_annuler.clicked.connect(self.close)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_annuler)
        btn_layout.addWidget(self.btn_valider)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        # Charger les catégories
        self.charger_categories()
        
    def charger_categories(self):
        self.categorie_combo.clear()
        categories = self.db.get_categories()
        for cat_id, nom, color in categories:
            self.categorie_combo.addItem(nom, cat_id)
            
    def charger_donnees(self):
        liens = self.db.get_liens_par_categorie()
        lien = next((l for l in liens if l[0] == self.lien_id), None)
        
        if lien:
            # Trouver l'index de la catégorie
            index = self.categorie_combo.findData(lien[6])
            if index >= 0:
                self.categorie_combo.setCurrentIndex(index)
                
            self.titre_input.setText(lien[1])
            self.url_input.setText(lien[2])
            self.identifiant_input.setText(lien[3] if lien[3] else "")
            self.mot_de_passe_input.setText(lien[4] if lien[4] else "")
            self.favori_check.setChecked(bool(lien[5]))
            self.tags_input.setText(", ".join(tag[1] for tag in lien[8]))
            
    def valider(self):
        titre = self.titre_input.text().strip()
        url = self.url_input.text().strip()
        categorie_index = self.categorie_combo.currentIndex()
        identifiant = self.identifiant_input.text().strip() or None
        mot_de_passe = self.mot_de_passe_input.text().strip() or None
        favori = self.favori_check.isChecked()
        tags = [t.strip() for t in self.tags_input.text().split(",") if t.strip()]
        
        if not titre:
            QMessageBox.warning(self, 'Erreur', 'Veuillez entrer un titre pour le lien')
            return
            
        if not url:
            QMessageBox.warning(self, 'Erreur', 'Veuillez entrer une URL')
            return
            
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        if categorie_index == -1:
            # Nouvelle catégorie
            nom_categorie = self.categorie_combo.currentText().strip()
            if not nom_categorie:
                QMessageBox.warning(self, 'Erreur', 'Veuillez sélectionner ou créer une catégorie')
                return
                
            dialog = AddCategoryDialog(self.db, self.parent)
            dialog.nom_input.setText(nom_categorie)
            dialog.exec_()
            
            if dialog.result() == QDialog.Accepted:
                self.charger_categories()
                # Trouver l'ID de la nouvelle catégorie
                for i in range(self.categorie_combo.count()):
                    if self.categorie_combo.itemText(i) == nom_categorie:
                        categorie_id = self.categorie_combo.itemData(i)
                        break
            else:
                return
        else:
            categorie_id = self.categorie_combo.currentData()
            
        if self.lien_id:
            # Modification
            self.db.modifier_lien(
                self.lien_id,
                titre=titre,
                url=url,
                categorie_id=categorie_id,
                identifiant=identifiant,
                mot_de_passe=mot_de_passe,
                favori=favori,
                tags=tags
            )
        else:
            # Ajout
            self.db.ajouter_lien(
                titre=titre,
                url=url,
                categorie_id=categorie_id,
                identifiant=identifiant,
                mot_de_passe=mot_de_passe,
                favori=favori,
                tags=tags
            )
            
        self.parent.charger_liens()
        self.close()

class MainWindowLink(QMainWindow):
    def __init__(self,main_app=None):
        super().__init__()
        self.main_app = main_app

        self.db = DatabaseManager()
        self.browser = None
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save)
        self.auto_save_timer.start(30000)  # Sauvegarde toutes les 30 secondes
        
        self.setWindowTitle("Gestionnaire de Liens Utiles")
        self.setGeometry(100, 100, 1200, 800)
        
        self.setup_ui()
        self.setup_menu()
        self.charger_categories()
        self.charger_liens()
        
    def setup_menu(self):
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu("Fichier")
        
        export_action = QAction("Exporter les liens", self)
        export_action.setShortcut(QKeySequence("Ctrl+E"))
        export_action.triggered.connect(self.exporter_liens)
        file_menu.addAction(export_action)
        
        import_action = QAction("Importer des liens", self)
        import_action.setShortcut(QKeySequence("Ctrl+I"))
        import_action.triggered.connect(self.importer_liens)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        backup_action = QAction("Sauvegarde automatique", self, checkable=True)
        backup_action.setChecked(True)
        backup_action.triggered.connect(self.toggle_auto_save)
        file_menu.addAction(backup_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("Quitter", self)
        quit_action.setShortcut(QKeySequence.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Menu Edition
        edit_menu = menubar.addMenu("Edition")
        
        add_link_action = QAction("Ajouter un lien", self)
        add_link_action.setShortcut(QKeySequence("Ctrl+N"))
        add_link_action.triggered.connect(self.ajouter_lien_dialog)
        edit_menu.addAction(add_link_action)
        
        add_cat_action = QAction("Ajouter une catégorie", self)
        add_cat_action.setShortcut(QKeySequence("Ctrl+Shift+N"))
        add_cat_action.triggered.connect(self.ajouter_categorie_dialog)
        edit_menu.addAction(add_cat_action)
        
        # Menu Affichage
        view_menu = menubar.addMenu("Affichage")
        
        self.show_fav_action = QAction("Afficher seulement les favoris", self, checkable=True)
        self.show_fav_action.setShortcut(QKeySequence("Ctrl+F"))
        self.show_fav_action.triggered.connect(self.toggle_favoris_view)
        view_menu.addAction(self.show_fav_action)
        
        # Menu Aide
        help_menu = menubar.addMenu("Aide")
        
        about_action = QAction("À propos", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_ui(self):
        # Style global
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fc;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #d1d3e2;
                border-radius: 4px;
                background-color: #fff;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #4e73df;
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
            }
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
        """)
        
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Partie gauche - Formulaire
        left_widget = QWidget()
        left_widget.setFixedWidth(350)
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(15)
        
        # Titre avec gradient
        title = GradientLabel("Gestionnaire de Liens")
        title.setFont(QFont('Arial', 16, QFont.Bold))
        title.setFixedHeight(50)
        title.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title)
        
        # Bouton Ajouter
        self.btn_ajouter_lien = FadeButton("Ajouter un lien")
        self.btn_ajouter_lien.setIcon(QIcon.fromTheme("list-add"))
        self.btn_ajouter_lien.setStyleSheet("""
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
        self.btn_ajouter_lien.clicked.connect(self.ajouter_lien_dialog)
        left_layout.addWidget(self.btn_ajouter_lien)
        
        # Bouton Ajouter Catégorie
        self.btn_ajouter_categorie = FadeButton("Ajouter une catégorie")
        self.btn_ajouter_categorie.setIcon(QIcon.fromTheme("folder-new"))
        self.btn_ajouter_categorie.setStyleSheet("""
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
        self.btn_ajouter_categorie.clicked.connect(self.ajouter_categorie_dialog)
        left_layout.addWidget(self.btn_ajouter_categorie)
        
        # Liste des catégories
        categories_group = QGroupBox("Catégories")
        categories_group.setStyleSheet("""
            QGroupBox {
                margin-top: 10px;
            }
        """)
        categories_layout = QVBoxLayout(categories_group)
        
        self.categories_list = QListWidget()
        self.categories_list.setStyleSheet("""
            QListWidget {
                border: none;
                outline: none;
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
        self.categories_list.setIconSize(QSize(16, 16))
        self.categories_list.itemClicked.connect(self.filtrer_par_categorie)
        
        categories_layout.addWidget(self.categories_list)
        left_layout.addWidget(categories_group)
        
        # Filtres
        filters_group = QGroupBox("Filtres")
        filters_layout = QVBoxLayout(filters_group)
        
        self.favoris_check = QCheckBox("Favoris seulement")
        self.favoris_check.stateChanged.connect(self.filtrer_par_favoris)
        
        self.search_label = QLabel("Recherche rapide:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Titre, URL, catégorie...")
        self.search_input.textChanged.connect(self.filtrer_liens)
        
        filters_layout.addWidget(self.favoris_check)
        filters_layout.addWidget(self.search_label)
        filters_layout.addWidget(self.search_input)
        left_layout.addWidget(filters_group)
        
        left_layout.addStretch()
        
        # Partie droite - Liste des liens
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(15)
        
        # Barre d'outils
        toolbar = QWidget()
        toolbar.setStyleSheet("background-color: white; border-radius: 8px; padding: 10px;")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(5, 5, 5, 5)
        
        self.results_label = QLabel("Tous les liens")
        self.results_label.setStyleSheet("font-weight: bold; color: #4e73df;")
        
        self.btn_tous = QToolButton()
        self.btn_tous.setIcon(QIcon.fromTheme("view-refresh"))
        self.btn_tous.setToolTip("Réinitialiser les filtres")
        self.btn_tous.setStyleSheet("""
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
        self.btn_tous.clicked.connect(self.charger_liens)
        
        toolbar_layout.addWidget(self.results_label)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.btn_tous)
        right_layout.addWidget(toolbar)
        
        # Liste des liens
        self.links_scroll = QScrollArea()
        self.links_scroll.setWidgetResizable(True)
        self.links_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f8f9fc;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #d1d3e2;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        self.links_container = QWidget()
        self.links_container.setStyleSheet("background-color: transparent;")
        self.links_layout = QVBoxLayout(self.links_container)
        self.links_layout.setContentsMargins(0, 0, 5, 0)
        self.links_layout.setSpacing(10)
        self.links_layout.addStretch()
        
        self.links_scroll.setWidget(self.links_container)
        right_layout.addWidget(self.links_scroll, 1)
        
        # Ajout des parties gauche et droite
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)
        
        self.setCentralWidget(main_widget)
        
    def charger_categories(self):
        self.categories_list.clear()
        
        categories = self.db.get_categories()
        for cat_id, nom, color in categories:
            item = QListWidgetItem(QIcon.fromTheme("folder"), nom)
            item.setData(Qt.UserRole, cat_id)
            item.setData(Qt.UserRole + 1, color)
            self.categories_list.addItem(item)
            
    def charger_liens(self, categorie_id=None, favori=None):
        # Clear the current layout
        while self.links_layout.count() > 1:  # Keep the stretch
            item = self.links_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
                
        if favori is None and self.favoris_check.isChecked():
            favori = True
            
        search_query = self.search_input.text().strip() or None
        liens = self.db.get_liens_par_categorie(categorie_id, favori, search_query)
        
        # Mettre à jour le label des résultats
        if categorie_id:
            cat_name = next(item.text() for i in range(self.categories_list.count()) 
                         if self.categories_list.item(i).data(Qt.UserRole) == categorie_id)
            self.results_label.setText(f"Liens dans '{cat_name}'")
        elif favori:
            self.results_label.setText("Liens favoris")
        elif search_query:
            self.results_label.setText(f"Résultats pour '{search_query}'")
        else:
            self.results_label.setText("Tous les liens")
            
        if not liens:
            no_results = QLabel("Aucun lien trouvé")
            no_results.setAlignment(Qt.AlignCenter)
            no_results.setStyleSheet("color: #6c757d; font-style: italic; padding: 20px;")
            self.links_layout.insertWidget(0, no_results)
            return
            
        current_categorie = None
        for lien in liens:
            lien_id, titre, url, identifiant, mot_de_passe, favori, categorie, categorie_color, tags = lien
            
            if categorie != current_categorie and not self.favoris_check.isChecked() and not search_query:
                current_categorie = categorie
                cat_widget = CategoryWidget(
                    next(cat_id for cat_id, nom, color in self.db.get_categories() if nom == categorie),
                    categorie,
                    categorie_color,
                    self
                )
                self.links_layout.insertWidget(self.links_layout.count()-1, cat_widget)
                
            link_widget = LinkWidget(lien_id, titre, url, categorie, categorie_color, 
                                   identifiant, mot_de_passe, favori, tags, self)
            link_widget.edit_requested.connect(self.modifier_lien_dialog)
            link_widget.tag_clicked.connect(self.filtrer_par_tag)
            self.links_layout.insertWidget(self.links_layout.count()-1, link_widget)
            
    def filtrer_par_categorie(self, item):
        cat_id = item.data(Qt.UserRole)
        self.charger_liens(cat_id)
        
    def filtrer_par_tag(self, tag):
        self.search_input.setText(tag)
        self.filtrer_liens(tag)
        
    def filtrer_par_favoris(self, state):
        self.charger_liens(favori=state == Qt.Checked)
        
    def toggle_favoris_view(self, checked):
        self.favoris_check.setChecked(checked)
        self.filtrer_par_favoris(Qt.Checked if checked else Qt.Unchecked)
        
    def filtrer_liens(self, texte):
        texte = texte.lower()
        
        for i in range(self.links_layout.count()):
            widget = self.links_layout.itemAt(i).widget()
            if widget:
                if isinstance(widget, CategoryWidget):
                    # Masquer la catégorie si aucun lien visible en dessous
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
                    visible = (texte in widget.titre_label.text().lower() or 
                              texte in widget.url_label.text().lower() or 
                              texte in widget.categorie_label.text().lower() or
                              any(texte in tag[1].lower() for tag in widget.tags))
                    widget.setVisible(visible)
                    
    def ajouter_lien_dialog(self):
        dialog = EditLinkDialog(self.db, parent=self)
        dialog.show()
        
    def ajouter_categorie_dialog(self):
        dialog = AddCategoryDialog(self.db, parent=self)
        dialog.show()
        
    def modifier_lien_dialog(self, lien_id):
        dialog = EditLinkDialog(self.db, lien_id, parent=self)
        dialog.show()
                
    def visiter_lien(self, url, new_tab=False):
        if not hasattr(self, 'browser') or not self.browser or new_tab:
            self.browser = QWebEngineView()
            self.browser.setWindowTitle("Navigateur - Gestionnaire de Liens")
            self.browser.resize(1000, 700)
            
        self.browser.load(url)
        self.browser.show()
        self.browser.activateWindow()
        
    def exporter_liens(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter les liens",
            "",
            "Fichiers JSON (*.json);;Tous les fichiers (*)"
        )
        
        if filename:
            if not filename.endswith('.json'):
                filename += '.json'
                
            try:
                self.db.exporter_liens(filename)
                QMessageBox.information(self, "Succès", "Les liens ont été exportés avec succès!")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de l'export:\n{str(e)}")
                
    def importer_liens(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Importer des liens",
            "",
            "Fichiers JSON (*.json);;Tous les fichiers (*)"
        )
        
        if filename:
            try:
                self.db.importer_liens(filename)
                self.charger_categories()
                self.charger_liens()
                QMessageBox.information(self, "Succès", "Les liens ont été importés avec succès!")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de l'import:\n{str(e)}")
                
    def auto_save(self):
        # Sauvegarde automatique des données
        try:
            self.db.conn.commit()
        except Exception as e:
            print(f"Erreur lors de la sauvegarde automatique: {e}")
            
    def toggle_auto_save(self, enabled):
        if enabled:
            self.auto_save_timer.start(30000)
        else:
            self.auto_save_timer.stop()
            
    def closeEvent(self, event):
        # Sauvegarde finale à la fermeture
        self.auto_save()
        event.accept()
        
    def show_about(self):
        about = QMessageBox(self)
        about.setWindowTitle("À propos")
        about.setIconPixmap(QIcon.fromTheme("help-about").pixmap(64, 64))
        about.setText("""
            <h2>Gestionnaire de Liens Utiles</h2>
            <p>Version 3.0</p>
            <p>Une application pour organiser et accéder facilement à vos liens web préférés.</p>
            <p><b>Fonctionnalités:</b></p>
            <ul>
                <li>Organisation par catégories et tags</li>
                <li>Stockage sécurisé des identifiants</li>
                <li>Navigation intégrée</li>
                <li>Import/Export des données</li>
                <li>Sauvegarde automatique</li>
                <li>Interface moderne et intuitive</li>
            </ul>
            <p>© 2023 - Tous droits réservés</p>
        """)
        about.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Style fusion avec personnalisation
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
    
    # Police par défaut
    font = QFont()
    font.setFamily("Segoe UI" if sys.platform == "win32" else "Arial")
    font.setPointSize(10)
    app.setFont(font)
    
    window = MainWindowLink()
    window.show()
    sys.exit(app.exec_())