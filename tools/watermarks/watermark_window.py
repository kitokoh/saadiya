import os
import json
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QComboBox, QSlider, QSpinBox, 
                            QColorDialog, QFileDialog, QProgressBar, QGroupBox, 
                            QCheckBox, QScrollArea, QSizePolicy, QMessageBox, 
                            QAction, QMenu, QToolBar, QStackedWidget, QTabWidget,
                            QListWidget, QListWidgetItem, QInputDialog, QDialog,
                            QDialogButtonBox, QFormLayout, QDoubleSpinBox)
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal, QPoint, QSettings, QMimeData, QUrl
from PyQt5.QtGui import (QPixmap, QColor, QImage, QIcon, QFont, QPainter, QPen, 
                        QLinearGradient, QBrush, QDragEnterEvent, QDropEvent)
from processor import MediaProcessor
from functools import partial
from PyQt5.QtCore import QObject

class WatermarkApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Watermarking Tool")
        self.setMinimumSize(1000, 700)
        self.setWindowIcon(QIcon("icon.png"))
        
        # Configuration initiale
        self.settings = QSettings("WatermarkApp", "WatermarkTool")
        self.load_settings()
        
        # Variables d'état
        self.media_files = []
        self.current_file_index = 0
        self.history = []
        self.history_index = -1
        self.presets = self.load_presets()
        
        # Initialisation de l'interface
        self.init_ui()
        self.create_menu()
        self.create_toolbar()
        self.apply_theme(self.current_theme)
        
        # Créer le dossier de sortie s'il n'existe pas
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
    
    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        
        # Panel de configuration avec onglets
        config_panel = QTabWidget()
        config_panel.setFixedWidth(350)
        
        # Onglet Watermark
        watermark_tab = QWidget()
        watermark_layout = QVBoxLayout()
        
        # Type de watermark
        self.watermark_type_combo = QComboBox()
        self.watermark_type_combo.addItems(["Texte", "Image", "Logo avec texte"])
        self.watermark_type_combo.currentIndexChanged.connect(self.update_watermark_type)
        
        # Texte du watermark
        self.watermark_text = QLineEdit()
        self.watermark_text.setPlaceholderText("Entrez votre texte de watermark")
        self.watermark_text.textChanged.connect(self.update_preview)
        
        # Police
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Arial", "Times New Roman", "Courier New", "Verdana", "Impact"])
        self.font_combo.currentIndexChanged.connect(self.update_preview)
        # Bouton pour image comme watermark
        self.image_watermark_check = QCheckBox("Utiliser une image comme watermark")
        self.image_watermark_check.stateChanged.connect(self.toggle_watermark_type)
                
        # Bouton pour image comme watermark
        self.image_watermark_btn = QPushButton("Sélectionner une image...")
        self.image_watermark_btn.clicked.connect(self.select_watermark_image)
        self.watermark_image_path = ""
        
        # Position
        self.position_combo = QComboBox()
        self.position_combo.addItems(["En bas à droite", "En bas à gauche", 
                                    "En haut à droite", "En haut à gauche", 
                                    "Centré", "Personnalisé", "Détection visage"])
        self.position_combo.currentIndexChanged.connect(self.update_preview)
        
        # Taille
        self.size_spin = QSpinBox()
        self.size_spin.setRange(10, 100)
        self.size_spin.setValue(30)
        self.size_spin.valueChanged.connect(self.update_preview)
        
        # Couleur
        self.color_btn = QPushButton("Couleur")
        self.color_btn.clicked.connect(self.select_color)
        self.selected_color = QColor(255, 255, 255)  # Blanc par défaut
        
        # Effets
        self.effect_combo = QComboBox()
        self.effect_combo.addItems(["Aucun", "Ombre", "Contour", "Dégradé"])
        self.effect_combo.currentIndexChanged.connect(self.update_preview)
        
        # Couleur effet
        self.effect_color_btn = QPushButton("Couleur effet")
        self.effect_color_btn.clicked.connect(self.select_effect_color)
        self.effect_color = QColor(0, 0, 0)  # Noir par défaut
        
        # Opacité
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(10, 100)
        self.opacity_slider.setValue(80)
        self.opacity_slider.valueChanged.connect(self.update_preview)
        
        # Rotation
        self.rotation_slider = QSlider(Qt.Horizontal)
        self.rotation_slider.setRange(0, 360)
        self.rotation_slider.setValue(0)
        self.rotation_slider.valueChanged.connect(self.update_preview)
        
        # Configuration du layout
        watermark_layout.addWidget(QLabel("Type de watermark:"))
        watermark_layout.addWidget(self.watermark_type_combo)
        watermark_layout.addSpacing(5)
        
        watermark_layout.addWidget(QLabel("Texte du watermark:"))
        watermark_layout.addWidget(self.watermark_text)
        watermark_layout.addSpacing(5)
        
        watermark_layout.addWidget(QLabel("Police:"))
        watermark_layout.addWidget(self.font_combo)
        watermark_layout.addSpacing(5)
        
        watermark_layout.addWidget(self.image_watermark_btn)
        watermark_layout.addSpacing(10)
        
        watermark_layout.addWidget(QLabel("Position:"))
        watermark_layout.addWidget(self.position_combo)
        watermark_layout.addSpacing(5)
        
        watermark_layout.addWidget(QLabel("Taille:"))
        watermark_layout.addWidget(self.size_spin)
        watermark_layout.addSpacing(5)
        
        watermark_layout.addWidget(QLabel("Couleur:"))
        watermark_layout.addWidget(self.color_btn)
        watermark_layout.addSpacing(5)
        
        watermark_layout.addWidget(QLabel("Effet:"))
        watermark_layout.addWidget(self.effect_combo)
        watermark_layout.addWidget(self.effect_color_btn)
        watermark_layout.addSpacing(5)
        
        watermark_layout.addWidget(QLabel("Opacité:"))
        watermark_layout.addWidget(self.opacity_slider)
        watermark_layout.addSpacing(5)
        
        watermark_layout.addWidget(QLabel("Rotation (degrés):"))
        watermark_layout.addWidget(self.rotation_slider)
        watermark_layout.addStretch()
        
        watermark_tab.setLayout(watermark_layout)
        
        # Onglet Sortie
        output_tab = QWidget()
        output_layout = QVBoxLayout()
        
        # Format de sortie
        self.output_format_combo = QComboBox()
        self.output_format_combo.addItems(["Original", "JPEG", "PNG", "WEBP", "BMP"])
        self.output_format_combo.currentIndexChanged.connect(self.update_quality_controls)
        
        # Qualité JPEG
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(1, 100)
        self.quality_slider.setValue(90)
        
        # Compression PNG
        self.compression_slider = QSlider(Qt.Horizontal)
        self.compression_slider.setRange(0, 9)
        self.compression_slider.setValue(3)
        
        # Dossier de sortie
        self.output_folder_btn = QPushButton("Changer le dossier de sortie")
        self.output_folder_btn.clicked.connect(self.change_output_folder)
        self.output_folder_label = QLabel(f"Dossier actuel: {self.output_folder}")
        
        # Configuration du layout
        output_layout.addWidget(QLabel("Format de sortie:"))
        output_layout.addWidget(self.output_format_combo)
        output_layout.addSpacing(10)
        
        output_layout.addWidget(QLabel("Qualité JPEG (1-100):"))
        output_layout.addWidget(self.quality_slider)
        output_layout.addSpacing(10)
        
        output_layout.addWidget(QLabel("Compression PNG (0-9):"))
        output_layout.addWidget(self.compression_slider)
        output_layout.addSpacing(10)
        
        output_layout.addWidget(self.output_folder_btn)
        output_layout.addWidget(self.output_folder_label)
        output_layout.addStretch()
        
        output_tab.setLayout(output_layout)
        
        # Onglet Presets
        presets_tab = QWidget()
        presets_layout = QVBoxLayout()
        
        self.presets_list = QListWidget()
        self.presets_list.itemClicked.connect(self.load_preset)
        
        self.save_preset_btn = QPushButton("Enregistrer le preset actuel")
        self.save_preset_btn.clicked.connect(self.save_current_preset)
        
        self.delete_preset_btn = QPushButton("Supprimer le preset sélectionné")
        self.delete_preset_btn.clicked.connect(self.delete_preset)
        
        presets_layout.addWidget(QLabel("Presets disponibles:"))
        presets_layout.addWidget(self.presets_list)
        presets_layout.addWidget(self.save_preset_btn)
        presets_layout.addWidget(self.delete_preset_btn)
        presets_layout.addStretch()
        
        presets_tab.setLayout(presets_layout)
        
        # Ajout des onglets
        config_panel.addTab(watermark_tab, "Watermark")
        config_panel.addTab(output_tab, "Sortie")
        config_panel.addTab(presets_tab, "Presets")
        
        # Panel d'affichage et actions
        display_panel = QWidget()
        display_layout = QVBoxLayout()
        
        # Boutons d'import
        import_btn = QPushButton("Importer des médias")
        import_btn.clicked.connect(self.import_media)
        
        # Zone de drop
        self.drop_label = QLabel("Glissez-déposez des fichiers ici")
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                padding: 20px;
                color: #777;
            }
        """)
        self.drop_label.setAcceptDrops(True)
        
        # Liste des fichiers
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.show_selected_file)
        
        # Prévisualisation
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.preview_label.setMinimumSize(500, 400)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        
        # Boutons de navigation
        nav_buttons = QHBoxLayout()
        self.prev_btn = QPushButton("Précédent")
        self.prev_btn.clicked.connect(self.show_previous_file)
        self.next_btn = QPushButton("Suivant")
        self.next_btn.clicked.connect(self.show_next_file)
        nav_buttons.addWidget(self.prev_btn)
        nav_buttons.addWidget(self.next_btn)
        
        # Bouton de traitement
        self.process_btn = QPushButton("Appliquer le watermark et enregistrer")
        self.process_btn.clicked.connect(self.process_files)
        self.process_btn.setEnabled(False)
        
        # Configuration du layout d'affichage
        display_layout.addWidget(import_btn)
        display_layout.addWidget(self.drop_label)
        display_layout.addWidget(self.file_list)
        display_layout.addWidget(self.preview_label)
        display_layout.addLayout(nav_buttons)
        display_layout.addWidget(self.progress_bar)
        display_layout.addWidget(self.process_btn)
        
        display_panel.setLayout(display_layout)
        
        # Ajout des panels au layout principal
        main_layout.addWidget(config_panel)
        main_layout.addWidget(display_panel)
        
        # Mise à jour initiale des contrôles
        self.update_watermark_type()
        self.update_quality_controls()
        self.update_presets_list()
    
    def create_menu(self):
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu("Fichier")
        
        import_action = file_menu.addAction("Importer des médias")
        import_action.triggered.connect(self.import_media)
        
        output_action = file_menu.addAction("Changer le dossier de sortie")
        output_action.triggered.connect(self.change_output_folder)
        
        exit_action = file_menu.addAction("Quitter")
        exit_action.triggered.connect(self.close)
        
        # Menu Edition
        edit_menu = menubar.addMenu("Édition")
        
        undo_action = edit_menu.addAction("Annuler")
        undo_action.triggered.connect(self.undo)
        undo_action.setShortcut("Ctrl+Z")
        
        redo_action = edit_menu.addAction("Rétablir")
        redo_action.triggered.connect(self.redo)
        redo_action.setShortcut("Ctrl+Y")
        
        # Menu Affichage
        view_menu = menubar.addMenu("Affichage")
        
        theme_menu = view_menu.addMenu("Thème")
        
        light_action = theme_menu.addAction("Clair")
        light_action.triggered.connect(partial(self.apply_theme, "light"))
        
        dark_action = theme_menu.addAction("Sombre")
        dark_action.triggered.connect(partial(self.apply_theme, "dark"))
        
        modern_action = theme_menu.addAction("Moderne")
        modern_action.triggered.connect(partial(self.apply_theme, "modern"))
        
        # Menu Aide
        help_menu = menubar.addMenu("Aide")
        about_action = help_menu.addAction("À propos")
        about_action.triggered.connect(self.show_about)
    
    def create_toolbar(self):
        toolbar = self.addToolBar("Outils")
        
        import_action = QAction(QIcon("icons/import.png"), "Importer", self)
        import_action.triggered.connect(self.import_media)
        toolbar.addAction(import_action)
        
        process_action = QAction(QIcon("icons/process.png"), "Traiter", self)
        process_action.triggered.connect(self.process_files)
        toolbar.addAction(process_action)
        
        toolbar.addSeparator()
        
        undo_action = QAction(QIcon("icons/undo.png"), "Annuler", self)
        undo_action.triggered.connect(self.undo)
        toolbar.addAction(undo_action)
        
        redo_action = QAction(QIcon("icons/redo.png"), "Rétablir", self)
        redo_action.triggered.connect(self.redo)
        toolbar.addAction(redo_action)
        
        toolbar.addSeparator()
        
        preset_action = QAction(QIcon("icons/preset.png"), "Enregistrer preset", self)
        preset_action.triggered.connect(self.save_current_preset)
        toolbar.addAction(preset_action)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        files = [url.toLocalFile() for url in urls if url.isLocalFile()]
        
        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.mp4', '.avi', '.mov', '.webm')
        valid_files = [f for f in files if f.lower().endswith(valid_extensions)]
        
        if valid_files:
            self.media_files = valid_files
            self.current_file_index = 0
            self.process_btn.setEnabled(True)
            self.update_file_list()
            self.show_current_file()
    
    def update_file_list(self):
        self.file_list.clear()
        for file_path in self.media_files:
            item = QListWidgetItem(os.path.basename(file_path))
            item.setData(Qt.UserRole, file_path)
            self.file_list.addItem(item)
    
    def show_selected_file(self):
        selected_items = self.file_list.selectedItems()
        if selected_items:
            self.current_file_index = self.file_list.row(selected_items[0])
            self.show_current_file()
    
    def update_watermark_type(self):
        watermark_type = self.watermark_type_combo.currentText()
        
        self.watermark_text.setEnabled(watermark_type in ["Texte", "Logo avec texte"])
        self.font_combo.setEnabled(watermark_type in ["Texte", "Logo avec texte"])
        self.image_watermark_btn.setEnabled(watermark_type in ["Image", "Logo avec texte"])
        
        self.update_preview()
    
    def update_quality_controls(self):
        output_format = self.output_format_combo.currentText()
        
        self.quality_slider.setEnabled(output_format == "JPEG")
        self.compression_slider.setEnabled(output_format == "PNG")
    
    def update_presets_list(self):
        self.presets_list.clear()
        for preset_name in self.presets.keys():
            self.presets_list.addItem(preset_name)
    
    # ... (autres méthodes restent similaires mais adaptées aux nouvelles fonctionnalités)
    # Les méthodes complètes seraient trop longues à afficher ici



    def load_settings(self):
        """Charge les paramètres depuis QSettings"""
        self.output_folder = self.settings.value("output_folder", os.path.expanduser("~/WatermarkedMedia"))
        self.current_theme = self.settings.value("theme", "light")
        
        # Charger les derniers paramètres de watermark
        self.last_watermark_params = {
            'type': self.settings.value("watermark/type", "Texte"),
            'text': self.settings.value("watermark/text", ""),
            'image_path': self.settings.value("watermark/image_path", ""),
            'position': self.settings.value("watermark/position", "En bas à droite"),
            'size': int(self.settings.value("watermark/size", 30)),
            'color': QColor(self.settings.value("watermark/color", "#ffffff")),
            'effect': self.settings.value("watermark/effect", "Aucun"),
            'effect_color': QColor(self.settings.value("watermark/effect_color", "#000000")),
            'opacity': float(self.settings.value("watermark/opacity", 0.8)),
            'rotation': int(self.settings.value("watermark/rotation", 0)),
            'font': self.settings.value("watermark/font", "Arial"),
            'output_format': self.settings.value("output/format", "Original"),
            'quality': int(self.settings.value("output/quality", 90)),
            'compression': int(self.settings.value("output/compression", 3))
        }

    def save_settings(self):
        """Enregistre les paramètres dans QSettings"""
        self.settings.setValue("output_folder", self.output_folder)
        self.settings.setValue("theme", self.current_theme)
        
        # Enregistrer les paramètres de watermark
        watermark_params = self.get_current_watermark_params()
        self.settings.setValue("watermark/type", watermark_params['type'])
        self.settings.setValue("watermark/text", watermark_params['text'])
        self.settings.setValue("watermark/image_path", watermark_params['image_path'])
        self.settings.setValue("watermark/position", watermark_params['position'])
        self.settings.setValue("watermark/size", watermark_params['size'])
        self.settings.setValue("watermark/color", watermark_params['color'].name())
        self.settings.setValue("watermark/effect", watermark_params['effect'])
        self.settings.setValue("watermark/effect_color", watermark_params['effect_color'].name())
        self.settings.setValue("watermark/opacity", watermark_params['opacity'])
        self.settings.setValue("watermark/rotation", watermark_params['rotation'])
        self.settings.setValue("watermark/font", watermark_params['font'])
        
        # Enregistrer les paramètres de sortie
        self.settings.setValue("output/format", self.output_format_combo.currentText())
        self.settings.setValue("output/quality", self.quality_slider.value())
        self.settings.setValue("output/compression", self.compression_slider.value())

    def get_current_watermark_params(self):
        """Retourne les paramètres actuels de watermark sous forme de dictionnaire"""
        return {
            'type': self.watermark_type_combo.currentText(),
            'text': self.watermark_text.text(),
            'image_path': self.watermark_image_path,
            'position': self.position_combo.currentText(),
            'size': self.size_spin.value(),
            'color': self.selected_color,
            'effect': self.effect_combo.currentText(),
            'effect_color': self.effect_color,
            'opacity': self.opacity_slider.value() / 100.0,
            'rotation': self.rotation_slider.value(),
            'font': self.font_combo.currentText(),
            'output_format': self.output_format_combo.currentText(),
            'quality': self.quality_slider.value(),
            'compression': self.compression_slider.value(),
            'output_folder': self.output_folder
        }

    def apply_theme(self, theme_name):
        """Applique un thème à l'interface"""
        self.current_theme = theme_name
        theme_file = f"styles/{theme_name}_theme.qss"
        
        if os.path.exists(theme_file):
            with open(theme_file, "r") as f:
                self.setStyleSheet(f.read())
        else:
            self.setStyleSheet("")  # Réinitialiser le style si le fichier n'existe pas

    def load_presets(self):
        """Charge les presets depuis le dossier presets"""
        presets = {}
        if not os.path.exists("presets"):
            os.makedirs("presets")
            return presets
            
        for file in os.listdir("presets"):
            if file.endswith(".json"):
                try:
                    with open(os.path.join("presets", file), "r") as f:
                        preset_data = json.load(f)
                        presets[os.path.splitext(file)[0]] = preset_data
                except Exception as e:
                    print(f"Erreur lors du chargement du preset {file}: {str(e)}")
        
        return presets

    def save_current_preset(self):
        """Enregistre la configuration actuelle comme preset"""
        name, ok = QInputDialog.getText(self, "Nouveau preset", "Nom du preset:")
        if ok and name:
            preset_data = self.get_current_watermark_params()
            
            # Convertir les QColor en chaînes hexadécimales
            preset_data['color'] = preset_data['color'].name()
            preset_data['effect_color'] = preset_data['effect_color'].name()
            
            with open(os.path.join("presets", f"{name}.json"), "w") as f:
                json.dump(preset_data, f, indent=4)
            
            # Recharger les presets
            self.presets = self.load_presets()
            self.update_presets_list()

    def load_preset(self, item):
        """Charge un preset sélectionné"""
        preset_name = item.text()
        if preset_name in self.presets:
            preset_data = self.presets[preset_name]
            
            # Convertir les couleurs hexadécimales en QColor
            color = QColor(preset_data['color'])
            effect_color = QColor(preset_data['effect_color'])
            
            # Appliquer les paramètres
            self.watermark_type_combo.setCurrentText(preset_data['type'])
            self.watermark_text.setText(preset_data['text'])
            self.watermark_image_path = preset_data['image_path']
            self.position_combo.setCurrentText(preset_data['position'])
            self.size_spin.setValue(preset_data['size'])
            self.selected_color = color
            self.effect_combo.setCurrentText(preset_data['effect'])
            self.effect_color = effect_color
            self.opacity_slider.setValue(int(preset_data['opacity'] * 100))
            self.rotation_slider.setValue(preset_data['rotation'])
            self.font_combo.setCurrentText(preset_data['font'])
            self.output_format_combo.setCurrentText(preset_data['output_format'])
            self.quality_slider.setValue(preset_data['quality'])
            self.compression_slider.setValue(preset_data['compression'])
            
            # Mettre à jour les boutons de couleur
            self.color_btn.setStyleSheet(f"background-color: {color.name()};")
            self.effect_color_btn.setStyleSheet(f"background-color: {effect_color.name()};")
            
            # Mettre à jour l'aperçu
            self.update_preview()

    def delete_preset(self):
        """Supprime le preset sélectionné"""
        selected_items = self.presets_list.selectedItems()
        if not selected_items:
            return
            
        preset_name = selected_items[0].text()
        reply = QMessageBox.question(
            self, "Confirmation", 
            f"Êtes-vous sûr de vouloir supprimer le preset '{preset_name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                os.remove(os.path.join("presets", f"{preset_name}.json"))
                self.presets = self.load_presets()
                self.update_presets_list()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de supprimer le preset: {str(e)}")

    def undo(self):
        """Annule la dernière action"""
        if self.history_index > 0:
            self.history_index -= 1
            self.apply_history_state()

    def redo(self):
        """Rétablit la dernière action annulée"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.apply_history_state()

    def add_to_history(self, state):
        """Ajoute un état à l'historique"""
        # Supprimer les états après l'index courant si on annule puis fait une nouvelle action
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        self.history.append(state)
        self.history_index = len(self.history) - 1

    def apply_history_state(self):
        """Applique l'état courant de l'historique"""
        if 0 <= self.history_index < len(self.history):
            state = self.history[self.history_index]
            # Appliquer l'état à l'interface
            # (implémentation dépendante de la structure de vos états)

    def closeEvent(self, event):
        """Sauvegarde les paramètres lors de la fermeture de l'application"""
        self.save_settings()
        event.accept()
    def select_effect_color(self):
        """Ouvre un dialogue pour sélectionner la couleur de l'effet"""
        color = QColorDialog.getColor(self.effect_color, self, "Sélectionner la couleur de l'effet")
        if color.isValid():
            self.effect_color = color
            self.effect_color_btn.setStyleSheet(f"background-color: {color.name()};")
            self.update_preview()

    def update_watermark_type1(self):
        """Met à jour l'interface en fonction du type de watermark sélectionné"""
        watermark_type = self.watermark_type_combo.currentText()
        
        # Activer/désactiver les contrôles appropriés
        self.watermark_text.setEnabled(watermark_type in ["Texte", "Logo avec texte"])
        self.font_combo.setEnabled(watermark_type in ["Texte", "Logo avec texte"])
        self.image_watermark_btn.setEnabled(watermark_type in ["Image", "Logo avec texte"])
        
        self.update_preview()

    def toggle_watermark_type(self, state):
        use_image = state == Qt.Checked
        self.watermark_text.setEnabled(not use_image)
        self.size_spin.setEnabled(not use_image)
        self.color_btn.setEnabled(not use_image)
        self.image_watermark_btn.setEnabled(use_image)
        self.update_preview()
    
    def select_watermark_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner une image de watermark", 
            "", "Images (*.png *.jpg *.jpeg *.bmp)")
        
        if file_path:
            self.watermark_image_path = file_path
            self.update_preview()
    
    def import_media(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Sélectionner des images ou vidéos", 
            "", "Médias (*.jpg *.jpeg *.png *.bmp *.mp4 *.avi *.mov *.webm)")
        
        if files:
            self.media_files = files
            self.current_file_index = 0
            self.process_btn.setEnabled(True)
            self.show_current_file()
    
    def change_output_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Sélectionner le dossier de sortie", 
            self.output_folder)
        
        if folder:
            self.output_folder = folder
    
    def show_current_file(self):
        if not self.media_files:
            return
            
        file_path = self.media_files[self.current_file_index]
        
        # Vérifier si c'est une image ou une vidéo
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            # Afficher l'image
            pixmap = QPixmap(file_path)
            self.preview_label.setPixmap(pixmap.scaled(
                self.preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            # Pour les vidéos, afficher juste le nom du fichier
            self.preview_label.setText(f"Vidéo: {os.path.basename(file_path)}")
        
        self.update_navigation_buttons()
        self.update_preview()
    
    def update_navigation_buttons(self):
        self.prev_btn.setEnabled(self.current_file_index > 0)
        self.next_btn.setEnabled(self.current_file_index < len(self.media_files) - 1)
    
    def show_previous_file(self):
        if self.current_file_index > 0:
            self.current_file_index -= 1
            self.show_current_file()
    
    def show_next_file(self):
        if self.current_file_index < len(self.media_files) - 1:
            self.current_file_index += 1
            self.show_current_file()
    
    def select_color(self):
        color = QColorDialog.getColor(self.selected_color, self)
        if color.isValid():
            self.selected_color = color
            self.update_preview()
    
    def update_preview(self):
        if not self.media_files:
            return
            
        current_file = self.media_files[self.current_file_index]
        
        # Vérifier si c'est une image (pas de prévisualisation pour les vidéos)
        if current_file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            # Créer une copie watermarquée pour prévisualisation
            processor = MediaProcessor()
            
            watermark_params = {
                'text': self.watermark_text.text(),
                'image_path': self.watermark_image_path if self.image_watermark_check.isChecked() else None,
                'position': self.position_combo.currentText(),
                'size': self.size_spin.value(),
                'color': self.selected_color,
                'opacity': self.opacity_slider.value() / 100.0
            }
            
            try:
                watermarked_img = processor.add_watermark_to_image(current_file, watermark_params, preview=True)
                
                # Convertir l'image OpenCV en QPixmap pour affichage
                height, width, channel = watermarked_img.shape
                bytes_per_line = 3 * width
                q_img = QImage(watermarked_img.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_img)
                
                self.preview_label.setPixmap(pixmap.scaled(
                    self.preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            except Exception as e:
                self.preview_label.setText(f"Erreur de prévisualisation: {str(e)}")
    
    def process_files(self):
        if not self.media_files:
            return
            
        # Créer le worker et le thread
        self.worker = MediaWorker(
            self.media_files,
            {
                'text': self.watermark_text.text(),
                'image_path': self.watermark_image_path if self.image_watermark_check.isChecked() else None,
                'position': self.position_combo.currentText(),
                'size': self.size_spin.value(),
                'color': self.selected_color,
                'opacity': self.opacity_slider.value() / 100.0,
                'output_folder': self.output_folder
            }
        )
        
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        
        # Connecter les signaux
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_processing_finished)
        self.worker.error.connect(self.on_processing_error)
        
        self.thread.started.connect(self.worker.process)
        self.thread.start()
        
        # Désactiver les boutons pendant le traitement
        self.process_btn.setEnabled(False)
        self.progress_bar.show()
        self.progress_bar.setValue(0)
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def on_processing_finished(self):
        self.thread.quit()
        self.thread.wait()
        self.progress_bar.hide()
        self.process_btn.setEnabled(True)
        
        QMessageBox.information(self, "Terminé", "Tous les fichiers ont été traités avec succès!")
    
    def on_processing_error(self, message):
        self.thread.quit()
        self.thread.wait()
        self.progress_bar.hide()
        self.process_btn.setEnabled(True)
        
        QMessageBox.critical(self, "Erreur", message)
    
    def show_about(self):
        QMessageBox.about(self, "À propos", 
            "Watermarking Tool\n\n"
            "Une application pour ajouter des watermarks aux images et vidéos.\n"
            "Développé avec PyQt5 et OpenCV.")

class MediaWorker(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, media_files, watermark_params):
        super().__init__()
        self.media_files = media_files
        self.watermark_params = watermark_params
        self.processor = MediaProcessor()
    
    def process(self):
        try:
            total_files = len(self.media_files)
            for i, file_path in enumerate(self.media_files):
                try:
                    output_path = os.path.join(
                        self.watermark_params['output_folder'],
                        f"watermarked_{os.path.basename(file_path)}"
                    )
                    
                    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                        # Traiter une image
                        self.processor.add_watermark_to_image(
                            file_path, 
                            self.watermark_params,
                            output_path=output_path
                        )
                    else:
                        # Traiter une vidéo
                        self.processor.add_watermark_to_video(
                            file_path,
                            self.watermark_params,
                            output_path=output_path,
                            progress_callback=lambda p: self.progress.emit(int((i + p) / total_files * 100)))
                    
                    self.progress.emit(int((i + 1) / total_files * 100))
                except Exception as e:
                    self.error.emit(f"Erreur lors du traitement de {file_path}: {str(e)}")
                    return
            
            self.finished.emit()
        except Exception as e:
            self.error.emit(f"Erreur générale: {str(e)}")