    def init_ui(self):
        """Initialise l'interface utilisateur avec QTableView pour une meilleure performance"""
        # Appliquer le style global
        self.setStyleSheet(f"""
            /* Styles de base */
            QWidget {{
                background-color: {self.light_color};
                font-family: 'Segoe UI', Arial, sans-serif;
                color: {self.dark_color};
            }}
            
            /* Styles pour les éléments désactivés */
            QWidget:disabled {{
                color: #95a5a6;
            }}
            
            /* Effets de transition pour les interactions */
            QPushButton, QComboBox, QLineEdit {{
                transition: all 0.3s ease;
            }}
        """)

        # Layout principal avec espacement optimisé
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # ----------------------------
        # Header amélioré (identique pour conserver l'identité visuelle)
        # ----------------------------
        self.header = QWidget()
        self.header.setFixedHeight(70)
        self.header.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.primary_color}, stop:1 {self.secondary_color});
                border-bottom: 2px solid {self.dark_color};
            }}
        """)
        
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(15, 5, 15, 5)
        header_layout.setSpacing(10)
        
        title_container = QWidget()
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(10)
        
        self.logo_label = QLabel()
        logo_pixmap = QPixmap("icons/logo.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignVCenter)
        
        self.title_label = QLabel("FBK GROUP MANAGEMENT")
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-size: 18px;
                font-weight: bold;
                margin: 0;
            }}
        """)
        self.title_label.setAlignment(Qt.AlignVCenter)
        
        title_layout.addWidget(self.logo_label)
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        
        header_layout.addWidget(title_container)
        header_layout.addStretch()
        
        layout.addWidget(self.header)

        # ----------------------------
        # Barre d'outils améliorée (identique)
        # ----------------------------
        toolbar = QWidget()
        toolbar.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border-radius: 0;
                padding: 10px 15px;
                border-bottom: 1px solid #ddd;
            }}
        """)
        
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(5, 5, 5, 5)
        toolbar_layout.setSpacing(10)
        
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("🔍 Rechercher...")
        self.search_field.setClearButtonEnabled(True)
        self.search_field.setStyleSheet(f"""
            QLineEdit {{
                padding: 8px 15px;
                font-size: 14px;
                border: 1px solid #ddd;
                border-radius: 20px;
                background-color: white;
                min-width: 250px;
            }}
            QLineEdit:hover {{
                border: 1px solid {self.primary_color};
            }}
            QLineEdit:focus {{
                border: 2px solid {self.primary_color};
                padding: 7px 14px;
            }}
        """)
        self.search_field.textChanged.connect(self.filter_table)
        
        self.instance_combo = QComboBox()
        self.instance_combo.addItems([f"media{i}" for i in range(1, 11)])
        self.instance_combo.setCurrentText(self.user_choice)
        self.instance_combo.setCurrentIndex(0)
        self.instance_combo.currentIndexChanged.connect(self.on_instance_changed)
        self.instance_combo.setStyleSheet(f"""
            QComboBox {{
                padding: 8px 15px 8px 10px;
                font-size: 14px;
                border: 1px solid #ddd;
                border-radius: 20px;
                background-color: white;
            }}
            QComboBox:hover {{
                border: 1px solid {self.primary_color};
            }}
            QComboBox:focus {{
                border: 2px solid {self.primary_color};
                padding: 7px 14px 7px 9px;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left-width: 1px;
                border-left-color: #ddd;
                border-left-style: solid;
                border-top-right-radius: 20px;
                border-bottom-right-radius: 20px;
            }}
            QComboBox::down-arrow {{
                image: url(icons/down-arrow.png);
                width: 12px;
                height: 12px;
            }}
        """)
        
        button_style = """
            QPushButton {{
                padding: 8px 15px;
                font-size: 14px;
                border-radius: 20px;
                border: none;
                color: white;
                background-color: {0};
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {1};
                transform: translateY(-1px);
            }}
            QPushButton:pressed {{
                transform: translateY(1px);
            }}
        """
        
        self.add_media_button = QPushButton("➕ Ajouter média")
        self.add_media_button.setStyleSheet(button_style.format(
            self.secondary_color, 
            QColor(self.secondary_color).darker(110).name()
        ))
        self.add_media_button.clicked.connect(self.import_media)
        
        self.action_button = QPushButton("📋 Actions")
        self.action_button.setStyleSheet(button_style.format(
            self.primary_color,
            QColor(self.primary_color).darker(110).name()
        ))
        self.action_button.setMenu(self.create_action_menu())
        
        self.settings_button = QPushButton("⚙️ Paramètres")
        self.settings_button.setStyleSheet(button_style.format(
            "#7f8c8d",
            QColor("#7f8c8d").darker(110).name()
        ))
        self.settings_button.setMenu(self.create_settings_menu())
        
        self.update_robot_button = QPushButton("🤖 Envoyer au robot")
        self.update_robot_button.setStyleSheet(button_style.format(
            self.accent_color,
            QColor(self.accent_color).darker(110).name()
        ))
        self.update_robot_button.clicked.connect(self.show_update_modal)
        
        toolbar_layout.addWidget(self.search_field)
        toolbar_layout.addWidget(self.instance_combo)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.add_media_button)
        toolbar_layout.addWidget(self.action_button)
        toolbar_layout.addWidget(self.settings_button)
        toolbar_layout.addWidget(self.update_robot_button)
        
        layout.addWidget(toolbar)

        # ----------------------------
        # Nouvelle implémentation avec QTableView
        # ----------------------------
        self.table_view = QTableView()
        
        # Création du modèle de données
        self.model = MediaTableModel()
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.table_view.setModel(self.proxy_model)
        
        # Configuration avancée de la vue
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setSelectionMode(QTableView.ExtendedSelection)
        self.table_view.setSortingEnabled(True)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setShowGrid(False)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.verticalHeader().setDefaultSectionSize(40)
        
        # Configuration des colonnes
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        
        # Style amélioré pour la vue
        self.table_view.setStyleSheet(f"""
            QTableView {{
                background-color: white;
                border-radius: 0;
                margin: 0;
                border: none;
                alternate-background-color: #f9f9f9;
                selection-background-color: {self.primary_color}20;
                selection-color: {self.dark_color};
            }}
            QHeaderView::section {{
                background-color: {self.primary_color};
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 12px;
            }}
            QTableView::item {{
                padding: 8px;
                border-bottom: 1px solid #eee;
            }}
            QTableView::item:selected {{
                background-color: {self.primary_color}40;
            }}
            QScrollBar:vertical {{
                width: 12px;
                margin: 0;
                background: transparent;
            }}
            QScrollBar::handle:vertical {{
                background: {self.primary_color};
                min-height: 20px;
                border-radius: 6px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
                background: none;
            }}
        """)
        
        # Ajout des boutons d'action dans la dernière colonne
        self.table_view.setItemDelegateForColumn(4, ActionItemDelegate(self))
        
        # Activer l'édition avec double-clic
        self.table_view.setEditTriggers(QTableView.DoubleClicked | QTableView.EditKeyPressed)
        
        layout.addWidget(self.table_view, 1)
        
        # ----------------------------
        # Pagination améliorée avec prise en charge du proxy
        # ----------------------------
        pagination = QWidget()
        pagination.setStyleSheet("""
            QWidget {
                background-color: white;
                border-top: 1px solid #ddd;
                padding: 10px 15px;
            }
        """)
        
        pagination_layout = QHBoxLayout(pagination)
        pagination_layout.setContentsMargins(0, 0, 0, 0)
        
        self.prev_button = QPushButton("◀ Précédent")
        self.prev_button.setCursor(Qt.PointingHandCursor)
        self.prev_button.setStyleSheet(f"""
            QPushButton {{
                padding: 8px 15px;
                background-color: {self.light_color};
                color: {self.dark_color};
                border: 1px solid #ddd;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #e0e0e0;
            }}
            QPushButton:disabled {{
                background-color: #f5f5f5;
                color: #bdbdbd;
            }}
        """)
        self.prev_button.clicked.connect(self.prev_page)
        
        self.page_label = QLabel("Page 1")
        self.page_label.setStyleSheet(f"""
            QLabel {{
                color: {self.dark_color};
                font-weight: bold;
            }}
        """)
        self.page_label.setAlignment(Qt.AlignCenter)
        
        self.next_button = QPushButton("Suivant ▶")
        self.next_button.setCursor(Qt.PointingHandCursor)
        self.next_button.setStyleSheet(f"""
            QPushButton {{
                padding: 8px 15px;
                background-color: {self.primary_color};
                color: white;
                border: none;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {QColor(self.primary_color).darker(110).name()};
            }}
            QPushButton:disabled {{
                background-color: #b0bec5;
            }}
        """)
        self.next_button.clicked.connect(self.next_page)
        
        self.items_per_page = QComboBox()
        self.items_per_page.addItems(["10", "25", "50", "100", "Tous"])
        self.items_per_page.setCurrentText("25")
        self.items_per_page.currentTextChanged.connect(self.update_pagination)
        self.items_per_page.setStyleSheet(f"""
            QComboBox {{
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                min-width: 60px;
            }}
        """)
        
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addStretch()
        pagination_layout.addWidget(QLabel("Éléments par page:"))
        pagination_layout.addWidget(self.items_per_page)
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.next_button)
        
        layout.addWidget(pagination)
        
        # Configuration finale
        self.setMinimumSize(1000, 700)
        self.load_data()  # Nouvelle méthode pour charger les données dans le modèle

class MediaTableModel(QAbstractTableModel):
    """Modèle personnalisé pour gérer les données des médias"""
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self._data = data or []
        self._headers = ['Nom', 'Description', 'Catégorie', 'Aperçu', 'Actions']
        
    def rowCount(self, parent=None):
        return len(self._data)
    
    def columnCount(self, parent=None):
        return len(self._headers)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
            
        row = index.row()
        col = index.column()
        
        if role == Qt.DisplayRole:
            if col == 4:  # Colonne Actions - affichage spécial
                return None
            return self._data[row][col]
            
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignLeft | Qt.AlignVCenter
            
        elif role == Qt.BackgroundRole and row % 2 == 0:
            return QColor('#f9f9f9')
            
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return None
    
    def flags(self, index):
        flags = super().flags(index)
        if index.column() != 4:  # Toutes les colonnes sauf Actions sont éditables
            flags |= Qt.ItemIsEditable
        return flags
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False
    
    def add_media(self, media_data):
        self.beginInsertRows(QModelIndex(), len(self._data), len(self._data))
        self._data.append(media_data)
        self.endInsertRows()
    
    def remove_media(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self._data[row]
        self.endRemoveRows()

class ActionItemDelegate(QStyledItemDelegate):
    """Délégué pour afficher les boutons d'action dans la dernière colonne"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
    def paint(self, painter, option, index):
        if not index.isValid():
            return
            
        # Dessiner le fond
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, QColor(self.parent.primary_color).lighter(160))
        elif index.row() % 2 == 0:
            painter.fillRect(option.rect, QColor('#f9f9f9'))
        else:
            painter.fillRect(option.rect, Qt.white)
            
        # Créer les boutons
        btn_width = option.rect.width() // 3 - 2
        btn_height = option.rect.height() - 4
        
        # Bouton Éditer
        edit_rect = QRect(option.rect.left() + 2, option.rect.top() + 2, btn_width, btn_height)
        edit_option = QStyleOptionButton()
        edit_option.rect = edit_rect
        edit_option.text = "✏️"
        edit_option.state = QStyle.State_Enabled
        
        # Bouton Supprimer
        delete_rect = QRect(edit_rect.right() + 2, option.rect.top() + 2, btn_width, btn_height)
        delete_option = QStyleOptionButton()
        delete_option.rect = delete_rect
        delete_option.text = "🗑️"
        delete_option.state = QStyle.State_Enabled
        
        # Dessiner les boutons
        QApplication.style().drawControl(QStyle.CE_PushButton, edit_option, painter)
        QApplication.style().drawControl(QStyle.CE_PushButton, delete_option, painter)
        
    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonRelease:
            btn_width = option.rect.width() // 3 - 2
            btn_height = option.rect.height() - 4
            
            # Vérifier quel bouton a été cliqué
            edit_rect = QRect(option.rect.left() + 2, option.rect.top() + 2, btn_width, btn_height)
            delete_rect = QRect(edit_rect.right() + 2, option.rect.top() + 2, btn_width, btn_height)
            
            if edit_rect.contains(event.pos()):
                self.parent.edit_media(index.row())
                return True
            elif delete_rect.contains(event.pos()):
                self.parent.delete_media(index.row())
                return True
                
        return super().editorEvent(event, model, option, index)
    
    def sizeHint(self, option, index):
        return QSize(150, 40)  # Taille fixe pour la colonne Actions