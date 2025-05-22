import sys
import sqlite3
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableView, QVBoxLayout,
                            QWidget, QPushButton, QComboBox, QStyledItemDelegate,
                            QMessageBox, QHeaderView, QHBoxLayout, QLineEdit,
                            QLabel, QStatusBar, QAction, QMenu, QSystemTrayIcon,
                            QTextEdit)
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QTimer, QSize
from PyQt5.QtGui import QFont, QIcon, QColor, QTextDocument
from PyQt5.QtWidgets import QStyle

class DatabaseManager:
    def __init__(self, db_name="multilingual_text1.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
        self.insert_sample_data()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS languages_text1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                code TEXT UNIQUE NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS descriptions_text1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(language_id) REFERENCES languages_text1(id)
            )
        """)

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_desc_timestamp_text1
            AFTER UPDATE ON descriptions_text1
            FOR EACH ROW
            BEGIN
                UPDATE descriptions_text1 SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
            END;
        """)

        self.conn.commit()

    def insert_sample_data(self):
        cursor = self.conn.cursor()

        languages = [
            ("Français", "fr"),
            ("Anglais", "en"),
            ("Arabe", "ar"),
            ("Turc", "tr")
        ]

        for name, code in languages:
            try:
                cursor.execute(
                    "INSERT INTO languages_text1 (name, code) VALUES (?, ?)",
                    (name, code)
                )
            except sqlite3.IntegrityError:
                pass

        cursor.execute("SELECT COUNT(*) FROM descriptions_text1")
        if cursor.fetchone()[0] == 0:
            self.insert_fake_descriptions()

        self.conn.commit()

    def insert_fake_descriptions(self):
        cursor = self.conn.cursor()

        fake_data = {
            "Français": [
                "Promotion exceptionnelle cette semaine seulement!\nProfitez-en vite!",
                "Nouvelle collection disponible dès maintenant\nDécouvrez nos nouveautés",
                "Livraison gratuite sur toutes les commandes\nValable jusqu'au 31 décembre",
                "Réduction de 50% sur une sélection d'articles\nDans la limite des stocks disponibles",
                "Abonnez-vous à notre newsletter pour des offres exclusives\nEt recevez un cadeau de bienvenue"
            ],
            "Anglais": [
                "Special promotion this week only!\nHurry up while stocks last!",
                "New collection available now\nDiscover our latest trends",
                "Free shipping on all orders\nValid until December 31st",
                "50% off on selected items\nWhile supplies last",
                "Subscribe to our newsletter for exclusive offers\nAnd get a welcome gift"
            ],
            "Arabe": [
                "ترقية استثنائية هذا الأسبوع فقط!\nاستفد منها بسرعة!",
                "مجموعة جديدة متاحة الآن\nاكتشف أحدث الاتجاهات لدينا",
                "شحن مجاني على جميع الطلبات\nصالحة حتى 31 ديسمبر",
                "خصم 50٪ على مجموعة مختارة من العناصر\nفي حدود الكميات المتوفرة",
                "اشترك في نشرتنا الإخبارية للحصول على عروض حصرية\nواحصل على هدية ترحيبية"
            ],
            "Turc": [
                "Xop lép kép xon fon qix!\nNox jox kox!",
                "Nox kolix zop fon pix!\nLix mix jop qox!",
                "Lix mix jop qox zix!\nPox rox dox!",
                "50% kox nox jix!\nZox qox lox!",
                "Sox rox nox dox lox!\nMox pox kox!"
            ]
        }

        for lang, descriptions in fake_data.items():
            cursor.execute("SELECT id FROM languages_text1 WHERE name = ?", (lang,))
            lang_id = cursor.fetchone()[0]

            for desc in descriptions:
                cursor.execute("""
                    INSERT INTO descriptions_text1 (language_id, content)
                    VALUES (?, ?)
                """, (lang_id, desc))

    def get_languages(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, code FROM languages_text1 ORDER BY name")
        return cursor.fetchall()

    def get_descriptions(self, language):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT d.id, d.content, d.created_at, d.updated_at
            FROM descriptions_text1 d
            JOIN languages_text1 l ON d.language_id = l.id
            WHERE l.name = ?
            ORDER BY d.created_at DESC
        """, (language,))
        return cursor.fetchall()

    def add_description(self, language, content):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM languages_text1 WHERE name = ?", (language,))
        lang_id = cursor.fetchone()[0]
        cursor.execute("""
            INSERT INTO descriptions_text1 (language_id, content)
            VALUES (?, ?)
        """, (lang_id, content))
        self.conn.commit()
        return cursor.lastrowid

    def update_description(self, desc_id, new_content):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE descriptions_text1
            SET content = ?
            WHERE id = ?
        """, (new_content, desc_id))
        self.conn.commit()

    def delete_description(self, desc_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM descriptions_text1 WHERE id = ?", (desc_id,))
        self.conn.commit()

    def search_descriptions(self, language, query):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT d.id, d.content
            FROM descriptions_text1 d
            JOIN languages_text1 l ON d.language_id = l.id
            WHERE l.name = ? AND d.content LIKE ?
            ORDER BY d.updated_at DESC
        """, (language, f"%{query}%"))
        return cursor.fetchall()

    def __del__(self):
        self.conn.close()

class DescriptionModel(QAbstractTableModel):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self._current_lang = "Français"
        self._descriptions = []
        self._display_columns = ["Contenu"]
        self.load_descriptions()

    def load_descriptions(self):
        self.beginResetModel()
        self._descriptions = self.db_manager.get_descriptions(self._current_lang)
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self._descriptions)

    def columnCount(self, parent=QModelIndex()):
        return len(self._display_columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._descriptions):
            return None

        desc = self._descriptions[index.row()]

        if role == Qt.DisplayRole:
            if index.column() == 0:  # Contenu
                return desc[1]

        if role == Qt.EditRole and index.column() == 0:
            return desc[1]

        if role == Qt.FontRole and index.column() == 0:
            font = QFont()
            font.setPointSize(12)
            return font

        if role == Qt.ToolTipRole and index.column() == 0:
            return f"ID: {desc[0]}\nCrée le: {desc[2]}\nModifié le: {desc[3]}"

        if role == Qt.TextAlignmentRole:
            return Qt.AlignLeft | Qt.AlignTop

        if role == Qt.SizeHintRole:
            # Calcul dynamique de la hauteur en fonction du contenu
            doc = QTextDocument()
            doc.setPlainText(desc[1])
            doc.setDefaultFont(QFont("Arial", 12))
            return QSize(100, int(doc.size().height()) + 10)

        if role == Qt.BackgroundRole and index.column() == 0:
            return QColor(240, 248, 255)  # AliceBlue

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._display_columns[section]
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole and index.column() == 0:
            new_content = value.strip()
            if new_content:
                desc_id = self._descriptions[index.row()][0]
                self.db_manager.update_description(desc_id, new_content)
                self.load_descriptions()
                return True
        return False

    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def change_language(self, lang):
        self._current_lang = lang
        self.load_descriptions()

    def add_description(self, content):
        if content.strip():
            self.db_manager.add_description(self._current_lang, content.strip())
            self.load_descriptions()

    def remove_description(self, row):
        if 0 <= row < len(self._descriptions):
            desc_id = self._descriptions[row][0]
            self.db_manager.delete_description(desc_id)
            self.load_descriptions()

    def search(self, query):
        self.beginResetModel()
        if query:
            self._descriptions = self.db_manager.search_descriptions(self._current_lang, query)
        else:
            self._descriptions = self.db_manager.get_descriptions(self._current_lang)
        self.endResetModel()

class DescriptionDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = None

    def createEditor(self, parent, option, index):
        self.editor = QTextEdit(parent)
        self.editor.setFrameStyle(QTextEdit.NoFrame)
        self.editor.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #4a6fa5;
                padding: 5px;
            }
        """)
        return self.editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setPlainText(value)

    def setModelData(self, editor, model, index):
        value = editor.toPlainText()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect.adjusted(0, 0, 0, 0))

    def sizeHint(self, option, index):
        # Taille dynamique basée sur le contenu
        doc = QTextDocument()
        doc.setPlainText(index.data())
        doc.setDefaultFont(option.font)
        return QSize(int(doc.idealWidth()) + 20, int(doc.size().height()) + 10)

class MainWindow1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionnaire de Descriptions Multilingues Pro")
        # self.resize(1000, 700)

        self.db_manager = DatabaseManager()
        self.model = DescriptionModel(self.db_manager)

        self.setup_ui()
        self.setup_style()
        self.setup_tray_icon()

        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self.autosave)
        self.autosave_timer.start(300000)  # 5 minutes

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Barre d'outils
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(10)

        self.lang_combo = QComboBox()
        for name, code in self.db_manager.get_languages():
            self.lang_combo.addItem(self.get_lang_icon(code), name)
        self.lang_combo.setCurrentText("Français")
        self.lang_combo.currentTextChanged.connect(self.model.change_language)
        toolbar_layout.addWidget(self.lang_combo)

        self.add_button = QPushButton(self.style().standardIcon(QStyle.SP_FileDialogNewFolder), "")
        self.add_button.clicked.connect(self.add_new_description)
        toolbar_layout.addWidget(self.add_button)

        self.delete_button = QPushButton(self.style().standardIcon(QStyle.SP_TrashIcon), "")
        self.delete_button.clicked.connect(self.delete_selected)
        toolbar_layout.addWidget(self.delete_button)

        self.search_button = QPushButton(self.style().standardIcon(QStyle.SP_FileDialogContentsView), "")
        self.search_button.clicked.connect(self.toggle_search)
        toolbar_layout.addWidget(self.search_button)

        self.random_button = QPushButton(self.style().standardIcon(QStyle.SP_BrowserReload), "")
        self.random_button.clicked.connect(self.generate_random)
        self.random_button.setToolTip("Générer une description aléatoire")
        toolbar_layout.addWidget(self.random_button)

        toolbar_layout.addStretch()

        self.lang_label = QLabel("Français")
        self.lang_label.setStyleSheet("font-weight: bold; color: #4a6fa5;")
        toolbar_layout.addWidget(self.lang_label)

        main_layout.addLayout(toolbar_layout)

        # Zone de recherche
        self.search_panel = QWidget()
        search_layout = QHBoxLayout(self.search_panel)
        search_layout.setContentsMargins(0, 0, 0, 0)

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Rechercher dans les descriptions...")
        self.search_field.textChanged.connect(self.on_search)
        search_layout.addWidget(self.search_field)

        self.clear_search = QPushButton("X")
        self.clear_search.setFixedWidth(30)
        self.clear_search.clicked.connect(self.clear_search_text)
        search_layout.addWidget(self.clear_search)

        self.search_panel.setVisible(False)
        main_layout.addWidget(self.search_panel)

        # Tableau des descriptions
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setItemDelegate(DescriptionDelegate())
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.doubleClicked.connect(self.on_double_click)

        # Ajustement dynamique de la hauteur des lignes
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        main_layout.addWidget(self.table)

        # Zone de collage rapide
        self.paste_panel = QWidget()
        paste_layout = QHBoxLayout(self.paste_panel)
        paste_layout.setContentsMargins(0, 0, 0, 0)

        self.paste_label = QLabel("Collez votre texte ici:")
        paste_layout.addWidget(self.paste_label)

        self.paste_area = QLineEdit()
        self.paste_area.setPlaceholderText("Appuyez sur Entrée pour ajouter")
        self.paste_area.returnPressed.connect(self.add_from_paste)
        paste_layout.addWidget(self.paste_area)

        self.clear_paste = QPushButton("X")
        self.clear_paste.setFixedWidth(30)
        self.clear_paste.clicked.connect(self.clear_paste_text)
        paste_layout.addWidget(self.clear_paste)

        main_layout.addWidget(self.paste_panel)

        # Barre de statut
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status()
    def setup_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f8f8;
            }
            QTableView {
                border: 1px solid #e0e0e0;
                background-color: white;
                alternate-background-color: #f8f8f8;
                selection-background-color: #d0d0d0;
                selection-color: #333333;
                gridline-color: #e0e0e0;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                color: #333333;
                padding: 12px;
                font-weight: bold;
                border: none;
                border-radius: 4px;
            }
            QComboBox, QLineEdit, QPushButton {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                min-height: 36px;
            }
            QPushButton {
                background-color: #e0e0e0;
                color: #333333;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #c0c0c0;
            }
            QPushButton#clear_search, QPushButton#clear_paste {
                background-color: #a0a0a0;
            }
            QPushButton#clear_search:hover, QPushButton#clear_paste:hover {
                background-color: #909090;
            }
            QLineEdit[placeholderText="Rechercher dans les descriptions..."] {
                background-color: white;
                border-radius: 6px;
            }
            QLineEdit[placeholderText="Appuyez sur Entrée pour ajouter"] {
                background-color: #f8f8f8;
                border: 1px dashed #e0e0e0;
                border-radius: 6px;
            }
            QStatusBar {
                background-color: #f8f8f8;
                color: #333333;
                border-top: 1px solid #e0e0e0;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 10px;
            }
        """)



    def setup_tray_icon(self):
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            self.tray_icon.setIcon(QIcon.fromTheme("accessories-text-editor"))

            tray_menu = QMenu()
            show_action = tray_menu.addAction("Ouvrir")
            show_action.triggered.connect(self.show)

            exit_action = tray_menu.addAction("Quitter")
            exit_action.triggered.connect(self.close)

            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.show()

    def get_lang_icon(self, code):
        return self.style().standardIcon(QStyle.SP_DialogSaveButton)

    def add_new_description(self):
        self.model.add_description("Nouvelle description")
        last_row = self.model.rowCount() - 1
        self.table.scrollToBottom()
        self.table.edit(self.model.index(last_row, 0))
        self.update_status()

    def delete_selected(self):
        selected = self.table.selectedIndexes()
        if selected:
            row = selected[0].row()
            reply = QMessageBox.question(
                self, 'Confirmation',
                'Voulez-vous vraiment supprimer cette description?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.model.remove_description(row)
                self.update_status()

    def add_from_paste(self):
        text = self.paste_area.text().strip()
        if text:
            self.model.add_description(text)
            self.paste_area.clear()
            self.table.scrollToBottom()
            self.update_status()

    def clear_paste_text(self):
        self.paste_area.clear()

    def toggle_search(self):
        self.search_panel.setVisible(not self.search_panel.isVisible())
        if self.search_panel.isVisible():
            self.search_field.setFocus()

    def on_search(self, text):
        self.model.search(text)
        self.update_status()

    def clear_search_text(self):
        self.search_field.clear()
        self.model.search("")

    def generate_random(self):
        random_phrases = {
            "Français": [
                "Super promotion limitée dans le temps!\nProfitez-en vite!",
                "Découvrez nos nouveaux produits!\nLivraison express disponible",
                "Offre spéciale pour nos clients fidèles!\nValable jusqu'à épuisement des stocks"
            ],
            "Anglais": [
                "Limited time super sale!\nHurry up while stocks last!",
                "Discover our new products!\nExpress delivery available",
                "Special offer for loyal customers!\nWhile supplies last"
            ],
            "Arabe": [
                "تخفيضات سوبر محدودة الوقت!\nاستفد منها بسرعة!",
                "اكتشف منتجاتنا الجديدة!\nالتوصيل السريع متاح",
                "عرض خاص للعملاء المخلصين!\nفي حدود الكميات المتوفرة"
            ],
            "Turc": [
                "Xop lép kép xon fon qix!\nNox jox kox!",
                "Nox kolix zop fon pix!\nLix mix jop qox!",
                "Jix kix lix mix!\nZox qox lox!"
            ]
        }

        current_lang = self.lang_combo.currentText()
        if current_lang in random_phrases:
            phrase = random.choice(random_phrases[current_lang])
            self.model.add_description(phrase)
            self.table.scrollToBottom()
            self.update_status()

    def on_double_click(self, index):
        if index.column() == 0:
            self.table.edit(index)

    def autosave(self):
        self.status_bar.showMessage("Sauvegarde automatique effectuée", 3000)

    def update_status(self):
        lang = self.lang_combo.currentText()
        count = self.model.rowCount()
        self.lang_label.setText(f"{lang} ({count} descriptions)")
        self.status_bar.showMessage(f"Langue: {lang} | Descriptions: {count}", 5000)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Confirmation',
            'Voulez-vous vraiment quitter?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if hasattr(self, 'tray_icon'):
                self.tray_icon.hide()
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    font = QFont()
    font.setFamily("Segoe UI" if sys.platform == "win32" else "Noto Sans")
    font.setPointSize(10)
    app.setFont(font)

    palette = app.palette()
    palette.setColor(palette.Window, QColor(248, 249, 250))
    palette.setColor(palette.WindowText, QColor(33, 37, 41))
    palette.setColor(palette.Base, QColor(255, 255, 255))
    palette.setColor(palette.AlternateBase, QColor(248, 249, 250))
    palette.setColor(palette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(palette.ToolTipText, QColor(33, 37, 41))
    palette.setColor(palette.Text, QColor(33, 37, 41))
    palette.setColor(palette.Button, QColor(73, 80, 87))
    palette.setColor(palette.ButtonText, QColor(255, 255, 255))
    palette.setColor(palette.BrightText, QColor(255, 255, 255))
    palette.setColor(palette.Highlight, QColor(0, 123, 255))
    palette.setColor(palette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)

    window = MainWindow1()
    window.show()
    sys.exit(app.exec_())
