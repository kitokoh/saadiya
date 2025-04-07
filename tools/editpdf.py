import sys
import os
import tempfile
import shutil
import importlib
import zipfile
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QProgressBar

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QFileDialog, QTextEdit, QLabel, QStatusBar,
                            QMessageBox, QScrollArea, QAction, QToolBar, QTabWidget,
                            QSplitter, QListWidget, QListWidgetItem, QDialog, 
                            QFormLayout, QLineEdit, QSpinBox, QColorDialog, QCheckBox,
                            QComboBox, QGroupBox, QStackedWidget, QInputDialog, QProgressDialog)
from PyQt5.QtCore import Qt, QSize, QPoint, QRectF, QThread, pyqtSignal, QTimer, QSettings
from PyQt5.QtGui import (QIcon, QTextCursor, QFont, QColor, QTextCharFormat, 
                         QTextFormat, QTextDocument, QPixmap, QImage, QPainter,
                         QDesktopServices)
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
import fitz  # PyMuPDF
from PIL import Image
import pdfrw
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import pikepdf
from pdf2image import convert_from_path
import pytesseract
#from signature import SignatureCaptureDialog  # Module personnalisé pour les signatures
from tools.signature import SignatureCaptureDialog  # Module personnalisé pour les signatures

class OCRThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, pdf_path, lang='fra'):
        super().__init__()
        self.pdf_path = pdf_path
        self.lang = lang
        self.canceled = False

    def run(self):
        try:
            # Convertir le PDF en images
            images = convert_from_path(self.pdf_path)
            total_pages = len(images)
            results = []
            
            for i, img in enumerate(images):
                if self.canceled:
                    return
                
                # Effectuer l'OCR sur chaque page
                text = pytesseract.image_to_string(img, lang=self.lang)
                results.append(text)
                
                # Émettre la progression
                self.progress.emit(int((i + 1) / total_pages * 100))
            
            self.finished.emit(results)
        
        except Exception as e:
            self.error.emit(str(e))

    def cancel(self):
        self.canceled = True

class PDFEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Éditeur PDF Professionnel")
        self.setGeometry(100, 100, 1400, 900)
        
        # Configuration et état
        self.settings = QSettings("PDFEditor", "AdvancedPDFEditor")
        self.load_settings()
        
        # Variables d'état
        self.current_file = None
        self.pdf_document = None
        self.modified = False
        self.current_page = 0
        self.zoom_factor = 1.0
        self.text_formats = {}
        self.annotations = []
        self.plugins = {}
        self.password = None
        self.temp_dir = tempfile.mkdtemp(prefix="pdf_editor_")
        self.ocr_thread = None
        
        # Initialisation de l'interface
        self.init_ui()
        self.init_advanced_features()
        self.load_plugins()
        
    def init_ui(self):
        # Widget central et layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Création des composants principaux
        self.create_toolbars()
        self.create_sidebar()
        self.create_main_content_area(main_layout)
        self.create_status_bar()
        
        # Menu
        self.create_menus()
        
        # Restaurer l'état de la fenêtre
        self.restore_state()

    # Boutons en bas
        button_layout = QHBoxLayout()
        
        # Créer et stocker le bouton Enregistrer comme attribut
        self.save_button = QPushButton("Enregistrer les modifications")
        self.save_button.setIcon(QIcon.fromTheme("document-save"))
        self.save_button.clicked.connect(self.save_changes)
        self.save_button.setEnabled(False)  # Désactivé par défaut
        
        self.export_button = QPushButton("Exporter vers un nouveau PDF")
        self.export_button.setIcon(QIcon.fromTheme("document-save-as"))
        self.export_button.clicked.connect(self.export_pdf)
        self.export_button.setEnabled(False)
        
        #button_layout.addWidget(self.save_button)
        #button_layout.addWidget(self.export_button)
        #main_layout.addLayout(button_layout)


    def save_changes(self):
        if not self.pdf_document or not self.current_file:
            return
            
        if not self.modified:
            self.status_bar.showMessage("Aucune modification à enregistrer.", 3000)
            return
            
        try:
            # Créer un nouveau document PDF avec le texte modifié
            new_doc = fitz.open()
            page = new_doc.new_page()
            
            # Ajouter le texte modifié
            modified_text = self.text_edit.toPlainText()
            rect = page.rect + (36, 36, -36, -36)  # Marges
            page.insert_textbox(rect, modified_text, fontsize=11)
            
            # Sauvegarder le fichier original
            backup_path = self.current_file.replace(".pdf", "_backup.pdf")
            self.pdf_document.save(backup_path)
                     # Sauvegarder les modifications
            new_doc.save(self.current_file)
            new_doc.close()
            
            # Recharger le document
            self.pdf_document = fitz.open(self.current_file)
            self.modified = False
            self.update_status_bar()
            self.status_bar.showMessage("Modifications enregistrées avec succès!", 3000)
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'enregistrement:\n{str(e)}")

    def export_pdf(self):
        if not self.pdf_document:
            return
            
        # Demander où sauvegarder le nouveau PDF
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Exporter le PDF", "", "Fichiers PDF (*.pdf);;Tous les fichiers (*)"
        )
        
        if file_path:
            try:
                # Créer un nouveau document PDF avec le texte modifié
                new_doc = fitz.open()
                page = new_doc.new_page()
                
                # Ajouter le texte modifié
                modified_text = self.text_edit.toPlainText()
                rect = page.rect + (36, 36, -36, -36)  # Marges
                page.insert_textbox(rect, modified_text, fontsize=11)

                                
                # Sauvegarder le nouveau fichier
                new_doc.save(file_path)
                new_doc.close()
                
                self.status_bar.showMessage(f"PDF exporté avec succès vers {file_path}", 5000)
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'exportation:\n{str(e)}")

    def save_text_changes(self):
        # Cette méthode serait plus complexe dans une vraie application
        # Pour simplifier, nous allons recréer le PDF avec le nouveau texte
        if not self.modified:
            return
            
        # Créer un nouveau PDF avec le texte modifié
        output_pdf = fitz.open()
        
        # Diviser le texte par pages (utilisant \f comme séparateur)
        pages_text = self.text_edit.toPlainText().split("\f")
        
        for page_text in pages_text:
            page = output_pdf.new_page(width=595, height=842)  # A4
            
            # Position de départ pour le texte
            rect = fitz.Rect(50, 50, 545, 792)
            
            # Insérer le texte avec une police de base
            page.insert_textbox(rect, page_text.strip(), 
                              fontsize=11, 
                              fontname="helv",
                              color=(0, 0, 0))
                    
        # Fermer l'ancien document et remplacer par le nouveau
        self.pdf_document.close()
        self.pdf_document = output_pdf
        self.modified = False
    def display_current_page(self):
        if not self.pdf_document or self.current_page >= len(self.pdf_document):
            return
            
        page = self.pdf_document.load_page(self.current_page)
        zoom_matrix = fitz.Matrix(self.zoom_factor, self.zoom_factor)
        pix = page.get_pixmap(matrix=zoom_matrix, alpha=False)
        
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        self.pdf_label.setPixmap(QPixmap.fromImage(img))
        
        # Mettre à jour la sélection dans les miniatures
        for i in range(self.page_thumbnails.count()):
            item = self.page_thumbnails.item(i)
            item.setSelected(i == self.current_page)
        
        # Mettre à jour le spinbox de page
        self.page_spin.blockSignals(True)
        self.page_spin.setValue(self.current_page + 1)
        self.page_spin.blockSignals(False)
    def update_ui_state(self):
        has_document = self.pdf_document is not None
        self.save_button.setEnabled(has_document and self.modified)
        self.export_button.setEnabled(has_document)
        self.prev_page_btn.setEnabled(has_document and self.current_page > 0)
        self.next_page_btn.setEnabled(has_document and self.current_page < len(self.pdf_document) - 1)
            
    def generate_thumbnails(self):
        self.page_thumbnails.clear()
        
        for i in range(len(self.pdf_document)):
            page = self.pdf_document.load_page(i)
            pix = page.get_pixmap(matrix=fitz.Matrix(0.2, 0.2))
            
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            icon = QIcon(QPixmap.fromImage(img))
            
            item = QListWidgetItem(icon, f"Page {i+1}")
            item.setData(Qt.UserRole, i)  # Stocker l'index de la page
            self.page_thumbnails.addItem(item)
        
        # Mettre à jour la navigation des pages
        self.page_spin.setMaximum(len(self.pdf_document))
        self.page_count_label.setText(f"/ {len(self.pdf_document)}")
    
    def save_pdf(self):
        if not self.pdf_document:
            return
            
        if not self.current_file:
            self.save_pdf_as()
            return
            
        try:
            # Sauvegarder les modifications de texte
            self.save_text_changes()
            
            # Sauvegarder les métadonnées
            self.save_document_properties()
            
            # Sauvegarder le fichier
            self.pdf_document.save(self.current_file, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
            
            self.modified = False
            self.update_status_bar()
            self.status_bar.showMessage(f"Fichier enregistré: {os.path.basename(self.current_file)}", 3000)
                        
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'enregistrement:\n{str(e)}")
    def save_document_properties(self):
        if not self.pdf_document:
            return
            
        metadata = {
            "title": self.title_edit.text(),
            "author": self.author_edit.text(),
            "subject": self.subject_edit.text(),
            "keywords": self.keywords_edit.text(),
            "creator": "Advanced PDF Editor",
            "producer": "PyMuPDF"
        }
        
        self.pdf_document.set_metadata(metadata)
        self.modified = True
        self.update_status_bar()
    def close_tab(self, index):
        if index == 0:  # Onglet d'édition de texte
            return  # Empêcher la fermeture de l'onglet principal
        
        self.tabs.removeTab(index)
    def set_modified(self):
        self.modified = True
        self.update_status_bar()
    def go_to_page(self, page_num):
        if self.pdf_document and 1 <= page_num <= len(self.pdf_document):
            self.current_page = page_num - 1
            self.display_current_page()
        
    def update_status_bar(self):
        status = ""
        if self.current_file:
            status += f"{os.path.basename(self.current_file)}"
            if self.modified:
                status += " - Modifié"
            else:
                status += " - Non modifié"
            
            status += f" | Page {self.current_page + 1}/{len(self.pdf_document) if self.pdf_document else 0}"
        else:
            status = "Prêt"
        
        self.status_bar.showMessage(status)
                
    def save_pdf_as(self):
        if not self.pdf_document:
            return
                      
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer sous", "", 
            "Fichiers PDF (*.pdf);;Tous les fichiers (*)"
        )
        
        if file_path:
            self.current_file = file_path
            self.save_pdf()
    def undo_action(self):
        if self.undo_stack:
            action = self.undo_stack.pop()
            self.redo_stack.append(action)
            # Implémenter l'annulation selon le type d'action
            self.status_bar.showMessage("Action annulée", 2000)
    def redo_action(self):
        if self.redo_stack:
            action = self.redo_stack.pop()
            self.undo_stack.append(action)
            # Implémenter le rétablissement selon le type d'action
            self.status_bar.showMessage("Action rétablie", 2000)
             
 
    def print_pdf(self):
        if not self.pdf_document:
            return
            
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        
        if dialog.exec_() == QDialog.Accepted:
            # Imprimer le document PDF
            painter = QPainter()
            painter.begin(printer)
            
            for i in range(len(self.pdf_document)):
                if i > 0:
                    printer.newPage()
                
                page = self.pdf_document.load_page(i)
                pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72), alpha=False)
                
                img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(img)

                          
                # Ajuster la taille de l'image à la page imprimée
                page_rect = printer.pageRect()
                pixmap = pixmap.scaled(page_rect.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                
                painter.drawPixmap(page_rect.topLeft(), pixmap)
            
            painter.end()
    
    def add_watermark(self):
        if not self.pdf_document:
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle("Ajouter un filigrane")
        layout = QFormLayout(dialog)
        
        text_edit = QLineEdit("Confidentiel")
        layout.addRow("Texte:", text_edit)
        
        color_btn = QPushButton("Choisir la couleur")
        color = QColor(200, 200, 200, 150)  # Gris semi-transparent par défaut
        color_btn.clicked.connect(lambda: self.choose_watermark_color(color_btn))
        layout.addRow("Couleur:", color_btn)

             
        opacity_spin = QSpinBox()
        opacity_spin.setRange(1, 100)
        opacity_spin.setValue(50)
        layout.addRow("Opacité (%):", opacity_spin)
        
        angle_spin = QSpinBox()
        angle_spin.setRange(0, 359)
        angle_spin.setValue(45)
        layout.addRow("Angle:", angle_spin)
        
        size_spin = QSpinBox()
        size_spin.setRange(10, 200)
        size_spin.setValue(72)
        layout.addRow("Taille de police:", size_spin)
        
        all_pages_check = QCheckBox("Appliquer à toutes les pages")
        all_pages_check.setChecked(True)
        layout.addRow(all_pages_check)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            try:
                watermark_text = text_edit.text()
                watermark_color = color_btn.property("color") or color
                opacity = opacity_spin.value() / 100.0
                angle = angle_spin.value()
                font_size = size_spin.value()
                all_pages = all_pages_check.isChecked()
                
                pages = range(len(self.pdf_document)) if all_pages else [self.current_page]
                
                for page_num in pages:
                    page = self.pdf_document.load_page(page_num)
                    
                    # Position centrale
                    center = fitz.Point(page.rect.width / 2, page.rect.height / 2)
                                    
                    # Créer un tampon de filigrane
                    annot = page.add_stamp_annot(
                        rect=fitz.Rect(0, 0, page.rect.width, page.rect.height),
                        stamp=0,  # Custom stamp
                        color=watermark_color.getRgb()[:3],
                        opacity=opacity
                    )
                    
                    # Ajouter du texte avec rotation
                    annot.set_text(watermark_text)
                    annot.set_rotation(angle)
                    annot.set_fontsize(font_size)
                    annot.update()
                
                self.modified = True
                self.update_status_bar()
                self.display_current_page()
                self.status_bar.showMessage("Filigrane ajouté avec succès", 3000)
                                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout du filigrane:\n{str(e)}")
    def create_menus(self):
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu("&Fichier")
        
        open_action = QAction(QIcon.fromTheme("document-open"), "&Ouvrir", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_pdf)
        file_menu.addAction(open_action)
        
        open_secure_action = QAction("Ouvrir PDF protégé", self)
        open_secure_action.setShortcut("Ctrl+Shift+O")
        open_secure_action.triggered.connect(self.open_secure_pdf)
        file_menu.addAction(open_secure_action)
        
        save_action = QAction(QIcon.fromTheme("document-save"), "&Enregistrer", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_pdf)
        file_menu.addAction(save_action)
        
        save_as_action = QAction(QIcon.fromTheme("document-save-as"), "Enregistrer &sous", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_pdf_as)
        file_menu.addAction(save_as_action)
        
        save_secure_action = QAction("Enregistrer avec mot de passe", self)
        save_secure_action.triggered.connect(self.save_secure_pdf)
        file_menu.addAction(save_secure_action)
        
        file_menu.addSeparator()
        
        print_action = QAction(QIcon.fromTheme("document-print"), "&Imprimer", self)
        print_action.setShortcut("Ctrl+P")
        print_action.triggered.connect(self.print_pdf)
        file_menu.addAction(print_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction(QIcon.fromTheme("application-exit"), "&Quitter", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Édition
        edit_menu = menubar.addMenu("&Édition")
        
        undo_action = QAction(QIcon.fromTheme("edit-undo"), "&Annuler", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.undo_action)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction(QIcon.fromTheme("edit-redo"), "&Rétablir", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.redo_action)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        format_action = QAction(QIcon.fromTheme("format-text-bold"), "&Formatage", self)
        format_action.setShortcut("Ctrl+T")
        format_action.triggered.connect(self.show_format_dialog)
        edit_menu.addAction(format_action)
        
        # Menu Affichage
        view_menu = menubar.addMenu("&Affichage")
        
        zoom_in_action = QAction(QIcon.fromTheme("zoom-in"), "Zoom &avant", self)
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction(QIcon.fromTheme("zoom-out"), "Zoom &arrière", self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)
        
        reset_zoom_action = QAction("&Réinitialiser zoom", self)
        reset_zoom_action.setShortcut("Ctrl+0")
        reset_zoom_action.triggered.connect(self.reset_zoom)
        view_menu.addAction(reset_zoom_action)
        
        view_menu.addSeparator()
        
        fullscreen_action = QAction("Plein écran", self)
        fullscreen_action.setShortcut("F11")
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        
        # Menu Outils
        tools_menu = menubar.addMenu("&Outils")
        
        ocr_action = QAction("OCR (Reconnaissance de texte)", self)
        ocr_action.setShortcut("Ctrl+R")
        ocr_action.triggered.connect(self.run_ocr)
        tools_menu.addAction(ocr_action)
        
        watermark_action = QAction("Ajouter un filigrane", self)
        watermark_action.triggered.connect(self.add_watermark)
        tools_menu.addAction(watermark_action)
        
        merge_action = QAction("Fusionner des PDF", self)
        merge_action.triggered.connect(self.merge_pdfs)
        tools_menu.addAction(merge_action)
        
        compress_action = QAction("Compresser PDF", self)
        compress_action.triggered.connect(self.compress_pdf)
        tools_menu.addAction(compress_action)
        
        sign_action = QAction("Ajouter une signature", self)
        sign_action.triggered.connect(self.add_signature)
        tools_menu.addAction(sign_action)
        
        # Menu Plugins
        self.plugins_menu = menubar.addMenu("&Plugins")
        self.update_plugins_menu()
        
        # Menu Aide
        help_menu = menubar.addMenu("&Aide")
        
        docs_action = QAction("Documentation", self)
        docs_action.triggered.connect(self.show_documentation)
        help_menu.addAction(docs_action)
        
        about_action = QAction(QIcon.fromTheme("help-about"), "&À propos", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    def change_text_color(self):
        color = QColorDialog.getColor(self.text_formats["color"], self, "Choisir la couleur du texte")
        if color.isValid():
            self.text_formats["color"] = color
            cursor = self.text_edit.textCursor()
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            cursor.mergeCharFormat(fmt)
            self.text_edit.setFocus()
 
    def show_format_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Formatage du texte")
        layout = QFormLayout(dialog)
        
        font_combo = QFontComboBox()
        font_combo.setCurrentFont(QFont(self.text_formats["font"]))
        layout.addRow("Police:", font_combo)
        
        size_spin = QSpinBox()
        size_spin.setRange(6, 72)
        size_spin.setValue(self.text_formats["size"])
        layout.addRow("Taille:", size_spin)
        
        color_btn = QPushButton()
        color_btn.setStyleSheet(f"background-color: {self.text_formats['color'].name()};")
        color_btn.clicked.connect(lambda: self.choose_text_color(color_btn))
        layout.addRow("Couleur:", color_btn)
        
        bold_check = QCheckBox("Gras")
        bold_check.setChecked(self.text_formats["bold"])
        layout.addRow(bold_check)

          
        italic_check = QCheckBox("Italique")
        italic_check.setChecked(self.text_formats["italic"])
        layout.addRow(italic_check)
        
        underline_check = QCheckBox("Souligné")
        underline_check.setChecked(self.text_formats["underline"])
        layout.addRow(underline_check)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            self.text_formats["font"] = font_combo.currentFont().family()
            self.text_formats["size"] = size_spin.value()
            self.text_formats["bold"] = bold_check.isChecked()
            self.text_formats["italic"] = italic_check.isChecked()
            self.text_formats["underline"] = underline_check.isChecked()
            
            cursor = self.text_edit.textCursor()
            fmt = QTextCharFormat()
            fmt.setFontFamily(self.text_formats["font"])
            
            fmt.setFontPointSize(self.text_formats["size"])
            fmt.setFontWeight(QFont.Bold if self.text_formats["bold"] else QFont.Normal)
            fmt.setFontItalic(self.text_formats["italic"])
            fmt.setFontUnderline(self.text_formats["underline"])
            fmt.setForeground(self.text_formats["color"])
            
            if cursor.hasSelection():
                cursor.mergeCharFormat(fmt)
            else:
                self.text_edit.setCurrentCharFormat(fmt)
            
            self.text_edit.setFocus()
    def zoom_in(self):
        self.zoom_factor *= 1.2
        self.update_zoom()
    
    def zoom_out(self):
        self.zoom_factor /= 1.2
        self.update_zoom()
    
    def reset_zoom(self):
        self.zoom_factor = 1.0
        self.update_zoom()
    
    def update_zoom(self):
        self.zoom_label.setText(f"Zoom: {int(self.zoom_factor * 100)}%")
        self.display_current_page()
            
    def prev_page(self):
        if self.pdf_document and self.current_page > 0:
            self.current_page -= 1
            self.display_current_page()
    def next_page(self):
        if self.pdf_document and self.current_page < len(self.pdf_document) - 1:
            self.current_page += 1
            self.display_current_page()
    def thumbnail_clicked(self, item):
        page_num = item.data(Qt.UserRole)
        if 0 <= page_num < len(self.pdf_document):
            self.current_page = page_num
            self.display_current_page()
 
    def merge_pdfs(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Sélectionner les PDF à fusionner", "", 
            "Fichiers PDF (*.pdf);;Tous les fichiers (*)"
        )
        
        if len(files) < 2:
            return
            
        try:
            output_pdf = fitz.open()
            
            for file in files:
                doc = fitz.open(file)
                output_pdf.insert_pdf(doc)
                doc.close()
            
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Enregistrer le PDF fusionné", "", 
                "Fichiers PDF (*.pdf);;Tous les fichiers (*)"
            )
                      
            if save_path:
                output_pdf.save(save_path)
                output_pdf.close()
                self.status_bar.showMessage("PDF fusionnés avec succès", 3000)
                
                # Ouvrir le nouveau PDF fusionné
                self.pdf_document = fitz.open(save_path)
                self.current_file = save_path
                self.current_page = 0
                self.modified = False
                self.extract_text_and_metadata()
                self.generate_thumbnails()
                self.display_current_page()
                self.update_ui_state()
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la fusion des PDF:\n{str(e)}")
    def show_about(self):
        QMessageBox.about(self, "À propos", 
                         "Éditeur PDF Professionnel\nVersion 2.0\n\n"
                         "Une application avancée pour éditer et manipuler des fichiers PDF.\n\n"
                         "Fonctionnalités:\n"
                         "- Édition de texte avancée\n"
                        "- Annotations et commentaires\n"
                        "- Fusion de PDF\n"
                        "- Ajout de filigranes\n"
                        "- Gestion des métadonnées\n\n"
                         "Technologies utilisées:\n"
                        "- PyQt5 pour l'interface\n"
                        "- PyMuPDF (fitz) pour la manipulation PDF\n"
                        "- ReportLab pour la génération PDF")

    def apply_text_format(self, format_type):
        cursor = self.text_edit.textCursor()
        
        if format_type == "bold":
            self.text_formats["bold"] = not self.text_formats["bold"]
            fmt = QTextCharFormat()
            fmt.setFontWeight(QFont.Bold if self.text_formats["bold"] else QFont.Normal)
            cursor.mergeCharFormat(fmt)
        
        elif format_type == "italic":
            self.text_formats["italic"] = not self.text_formats["italic"]
            fmt = QTextCharFormat()
            fmt.setFontItalic(self.text_formats["italic"])
            cursor.mergeCharFormat(fmt)
        
        elif format_type == "underline":
            self.text_formats["underline"] = not self.text_formats["underline"]
            fmt = QTextCharFormat()
            fmt.setFontUnderline(self.text_formats["underline"])
            cursor.mergeCharFormat(fmt)
            
    def apply_text_format(self, format_type):
        cursor = self.text_edit.textCursor()
        
        if format_type == "bold":
            self.text_formats["bold"] = not self.text_formats["bold"]
            fmt = QTextCharFormat()
            fmt.setFontWeight(QFont.Bold if self.text_formats["bold"] else QFont.Normal)
            cursor.mergeCharFormat(fmt)
        
        elif format_type == "italic":
            self.text_formats["italic"] = not self.text_formats["italic"]
            fmt = QTextCharFormat()
            fmt.setFontItalic(self.text_formats["italic"])
            cursor.mergeCharFormat(fmt)
        
        elif format_type == "underline":
            self.text_formats["underline"] = not self.text_formats["underline"]
            fmt = QTextCharFormat()
            fmt.setFontUnderline(self.text_formats["underline"])
            cursor.mergeCharFormat(fmt)  
            

    def extract_text_and_metadata(self):
        """Extrait le texte et les métadonnées du PDF chargé"""
        if not self.pdf_document:
            return

        # Extraire le texte de toutes les pages
        full_text = ""
        for page_num in range(len(self.pdf_document)):
            page = self.pdf_document.load_page(page_num)
            full_text += page.get_text("text") + "\n\f"  # \f pour les sauts de page
        
        self.text_edit.setPlainText(full_text)
        
        # Extraire les métadonnées
        metadata = self.pdf_document.metadata
        self.title_edit.setText(metadata.get("title", ""))
        self.author_edit.setText(metadata.get("author", ""))
        self.subject_edit.setText(metadata.get("subject", ""))
        self.keywords_edit.setText(metadata.get("keywords", ""))
        
        # Mettre à jour le compteur de pages
        self.page_spin.setMaximum(len(self.pdf_document))
        self.page_count_label.setText(f"/ {len(self.pdf_document)}")
        
        # Activer les boutons appropriés
        self.save_button.setEnabled(True)
        self.export_button.setEnabled(True)




    def create_toolbars(self):
        # Barre d'outils principale
        main_toolbar = self.addToolBar("Principal")
        main_toolbar.setIconSize(QSize(24, 24))
        
        # Actions principales
        open_action = QAction(QIcon.fromTheme("document-open"), "Ouvrir", self)
        open_action.triggered.connect(self.open_pdf)
        main_toolbar.addAction(open_action)
        
        save_action = QAction(QIcon.fromTheme("document-save"), "Enregistrer", self)
        save_action.triggered.connect(self.save_pdf)
        main_toolbar.addAction(save_action)
        
        print_action = QAction(QIcon.fromTheme("document-print"), "Imprimer", self)
        print_action.triggered.connect(self.print_pdf)
        main_toolbar.addAction(print_action)
        
        main_toolbar.addSeparator()
        
        # Outils d'édition
        bold_action = QAction(QIcon.fromTheme("format-text-bold"), "Gras", self)
        bold_action.triggered.connect(lambda: self.apply_text_format("bold"))
        main_toolbar.addAction(bold_action)
        
        italic_action = QAction(QIcon.fromTheme("format-text-italic"), "Italique", self)
        italic_action.triggered.connect(lambda: self.apply_text_format("italic"))
        main_toolbar.addAction(italic_action)
        
        underline_action = QAction(QIcon.fromTheme("format-text-underline"), "Souligné", self)
        underline_action.triggered.connect(lambda: self.apply_text_format("underline"))
        main_toolbar.addAction(underline_action)
        
        color_action = QAction(QIcon.fromTheme("format-text-color"), "Couleur", self)
        color_action.triggered.connect(self.change_text_color)
        main_toolbar.addAction(color_action)
        
        main_toolbar.addSeparator()
        
        # Outils OCR
        ocr_action = QAction(QIcon(":/ocr.png"), "OCR", self)
        ocr_action.triggered.connect(self.run_ocr)
        main_toolbar.addAction(ocr_action)
        
        # Outils signature
        sign_action = QAction(QIcon(":/signature.png"), "Signer", self)
        sign_action.triggered.connect(self.add_signature)
        main_toolbar.addAction(sign_action)
        
        main_toolbar.addSeparator()
        
        # Navigation
        prev_page_action = QAction(QIcon.fromTheme("go-previous"), "Page précédente", self)
        prev_page_action.triggered.connect(self.prev_page)
        main_toolbar.addAction(prev_page_action)
        
        next_page_action = QAction(QIcon.fromTheme("go-next"), "Page suivante", self)
        next_page_action.triggered.connect(self.next_page)
        main_toolbar.addAction(next_page_action)
        
        # Barre d'outils d'annotation
        annot_toolbar = QToolBar("Annotations")
        self.addToolBar(Qt.LeftToolBarArea, annot_toolbar)
        
        highlight_action = QAction(QIcon(":/highlight.png"), "Surligneur", self)
        highlight_action.triggered.connect(lambda: self.set_annotation_mode("highlight"))
        annot_toolbar.addAction(highlight_action)
        
        underline_action = QAction(QIcon(":/underline.png"), "Soulignement", self)
        underline_action.triggered.connect(lambda: self.set_annotation_mode("underline"))
        annot_toolbar.addAction(underline_action)
        
        strikeout_action = QAction(QIcon(":/strikeout.png"), "Barré", self)
        strikeout_action.triggered.connect(lambda: self.set_annotation_mode("strikeout"))
        annot_toolbar.addAction(strikeout_action)
        
        note_action = QAction(QIcon(":/note.png"), "Note", self)
        note_action.triggered.connect(lambda: self.set_annotation_mode("note"))
        annot_toolbar.addAction(note_action)
    
    def create_sidebar(self):
        # Zone latérale avec onglets
        self.sidebar = QTabWidget()
        self.sidebar.setTabPosition(QTabWidget.West)
        
        # Onglet Pages
        pages_tab = QWidget()
        pages_layout = QVBoxLayout(pages_tab)
        
        self.page_thumbnails = QListWidget()
        self.page_thumbnails.setViewMode(QListWidget.IconMode)
        self.page_thumbnails.setIconSize(QSize(100, 150))
        self.page_thumbnails.setResizeMode(QListWidget.Adjust)
        self.page_thumbnails.itemClicked.connect(self.thumbnail_clicked)
        pages_layout.addWidget(self.page_thumbnails)
        
        # Onglet Propriétés
        props_tab = QWidget()
        props_layout = QVBoxLayout(props_tab)
        
        self.doc_properties = QWidget()
        props_form = QFormLayout(self.doc_properties)
        
        self.title_edit = QLineEdit()
        self.author_edit = QLineEdit()
        self.subject_edit = QLineEdit()
        self.keywords_edit = QLineEdit()
        
        props_form.addRow("Titre:", self.title_edit)
        props_form.addRow("Auteur:", self.author_edit)
        props_form.addRow("Sujet:", self.subject_edit)
        props_form.addRow("Mots-clés:", self.keywords_edit)
        
        security_group = QGroupBox("Sécurité")
        security_layout = QFormLayout(security_group)
        
        self.encryption_check = QCheckBox("Chiffrer le document")
        self.encryption_check.stateChanged.connect(self.toggle_encryption_fields)
        security_layout.addRow(self.encryption_check)
        
        self.owner_pwd_edit = QLineEdit()
        self.owner_pwd_edit.setPlaceholderText("Mot de passe propriétaire")
        self.owner_pwd_edit.setEchoMode(QLineEdit.Password)
        security_layout.addRow("Propriétaire:", self.owner_pwd_edit)
        
        self.user_pwd_edit = QLineEdit()
        self.user_pwd_edit.setPlaceholderText("Mot de passe utilisateur")
        self.user_pwd_edit.setEchoMode(QLineEdit.Password)
        security_layout.addRow("Utilisateur:", self.user_pwd_edit)
        
        self.permissions_combo = QComboBox()
        self.permissions_combo.addItems([
            "Aucune restriction",
            "Interdire l'impression",
            "Interdire la modification",
            "Interdire la copie",
            "Interdire l'annotation"
        ])
        security_layout.addRow("Permissions:", self.permissions_combo)
        
        props_layout.addWidget(self.doc_properties)
        props_layout.addWidget(security_group)
        
        save_props_btn = QPushButton("Enregistrer les propriétés")
        save_props_btn.clicked.connect(self.save_document_properties)
        props_layout.addWidget(save_props_btn)
        
        # Onglet Plugins
        plugins_tab = QWidget()
        plugins_layout = QVBoxLayout(plugins_tab)
        
        self.plugins_list = QListWidget()
        self.plugins_list.itemClicked.connect(self.run_plugin_from_list)
        plugins_layout.addWidget(self.plugins_list)
        
        manage_btn = QPushButton("Gérer les plugins")
        manage_btn.clicked.connect(self.manage_plugins)
        plugins_layout.addWidget(manage_btn)
        
        # Ajouter les onglets à la sidebar
        self.sidebar.addTab(pages_tab, QIcon(":/pages.png"), "Pages")
        self.sidebar.addTab(props_tab, QIcon(":/properties.png"), "Propriétés")
        self.sidebar.addTab(plugins_tab, QIcon(":/plugins.png"), "Plugins")
    
    def create_main_content_area(self, main_layout):
        # Zone de contenu principal
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        # Onglets
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        # Onglet d'édition de texte
        self.text_edit_tab = QWidget()
        text_edit_layout = QVBoxLayout(self.text_edit_tab)
        
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Arial", 12))
        self.text_edit.textChanged.connect(self.set_modified)
        text_edit_layout.addWidget(self.text_edit)
        
        # Onglet d'affichage PDF
        self.pdf_view_tab = QWidget()
        pdf_view_layout = QVBoxLayout(self.pdf_view_tab)
        
        self.pdf_scroll = QScrollArea()
        self.pdf_scroll.setWidgetResizable(True)
        
        self.pdf_label = QLabel()
        self.pdf_label.setAlignment(Qt.AlignCenter)
        self.pdf_label.setBackgroundRole(QPalette.Base)
        self.pdf_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.pdf_label.setScaledContents(True)
        
        self.pdf_scroll.setWidget(self.pdf_label)
        pdf_view_layout.addWidget(self.pdf_scroll)
        
        # Onglet OCR
        self.ocr_tab = QWidget()
        ocr_layout = QVBoxLayout(self.ocr_tab)
        
        self.ocr_text = QTextEdit()
        self.ocr_text.setReadOnly(True)
        ocr_layout.addWidget(self.ocr_text)
        
        # Ajouter les onglets
        self.tabs.addTab(self.text_edit_tab, QIcon(":/edit.png"), "Édition de texte")
        self.tabs.addTab(self.pdf_view_tab, QIcon(":/preview.png"), "Aperçu PDF")
        self.tabs.addTab(self.ocr_tab, QIcon(":/ocr.png"), "Résultat OCR")
        
        content_layout.addWidget(self.tabs)
        
        # Barre de navigation des pages
        page_nav = QWidget()
        page_nav_layout = QHBoxLayout(page_nav)
        
        self.prev_page_btn = QPushButton(QIcon.fromTheme("go-previous"), "")
        self.prev_page_btn.setToolTip("Page précédente")
        self.prev_page_btn.clicked.connect(self.prev_page)
        page_nav_layout.addWidget(self.prev_page_btn)
        
        self.page_spin = QSpinBox()
        self.page_spin.setPrefix("Page ")
        self.page_spin.valueChanged.connect(self.go_to_page)
        page_nav_layout.addWidget(self.page_spin)
        
        self.page_count_label = QLabel("/ 0")
        page_nav_layout.addWidget(self.page_count_label)
        
        self.next_page_btn = QPushButton(QIcon.fromTheme("go-next"), "")
        self.next_page_btn.setToolTip("Page suivante")
        self.next_page_btn.clicked.connect(self.next_page)
        page_nav_layout.addWidget(self.next_page_btn)
        
        self.zoom_label = QLabel("Zoom: 100%")
        page_nav_layout.addWidget(self.zoom_label)
        
        content_layout.addWidget(page_nav)
        
        # Ajouter au splitter principal
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(content_widget)
        main_layout.addWidget(self.splitter)
        
        # Configurer les proportions du splitter
        self.splitter.setSizes([250, 1000])
    
    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Widget de statut personnalisé
        self.status_widget = QWidget()
        status_layout = QHBoxLayout(self.status_widget)
        status_layout.setContentsMargins(0, 0, 0, 0)
        
        self.status_label = QLabel("Prêt")
        self.status_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        status_layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setFixedWidth(200)
        self.progress_bar.setVisible(False)
        status_layout.addWidget(self.progress_bar)
        
        self.status_bar.addPermanentWidget(self.status_widget, 1)
    
    def init_advanced_features(self):
        # Initialiser les fonctionnalités avancées
        self.annotation_mode = None
        self.selected_text = ""
        self.undo_stack = []
        self.redo_stack = []
        
        # Configurer les formats de texte par défaut
        self.text_formats = {
            "bold": False,
            "italic": False,
            "underline": False,
            "color": QColor(Qt.black),
            "font": "Arial",
            "size": 12
        }
        
        # Configuration OCR
        pytesseract.pytesseract.tesseract_cmd = self.settings.value("tesseract_path", "")
        
        # Charger les plugins
        self.plugins_dir = "plugins"
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir)
    
    def load_plugins(self):
        """Charge tous les plugins valides du dossier plugins"""
        self.plugins = {}
        self.plugins_list.clear()
        
        for filename in os.listdir(self.plugins_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                plugin_name = filename[:-3]
                try:
                    spec = importlib.util.spec_from_file_location(
                        plugin_name, 
                        os.path.join(self.plugins_dir, filename)
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    if hasattr(module, "Plugin"):
                        plugin = module.Plugin(self)
                        self.plugins[plugin_name] = plugin
                        
                        item = QListWidgetItem(plugin.name)
                        item.setIcon(QIcon(plugin.icon) if hasattr(plugin, "icon") else None)
                        item.setData(Qt.UserRole, plugin_name)
                        self.plugins_list.addItem(item)
                
                except Exception as e:
                    print(f"Erreur lors du chargement du plugin {filename}: {str(e)}")
        
        self.update_plugins_menu()
    
    def update_plugins_menu(self):
        """Met à jour le menu des plugins avec les plugins disponibles"""
        self.plugins_menu.clear()
        
        for plugin_name, plugin in self.plugins.items():
            action = QAction(plugin.name, self)
            if hasattr(plugin, "icon"):
                action.setIcon(QIcon(plugin.icon))
            action.triggered.connect(lambda _, p=plugin: p.run())
            self.plugins_menu.addAction(action)
    
    def run_plugin_from_list(self, item):
        """Exécute un plugin sélectionné dans la liste"""
        plugin_name = item.data(Qt.UserRole)
        if plugin_name in self.plugins:
            self.plugins[plugin_name].run()
    
    def manage_plugins(self):
        """Ouvre le gestionnaire de plugins"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Gestionnaire de plugins")
        dialog.setMinimumSize(600, 400)
        layout = QVBoxLayout(dialog)
        
        # Liste des plugins installés
        installed_group = QGroupBox("Plugins installés")
        installed_layout = QVBoxLayout(installed_group)
        
        installed_list = QListWidget()
        for plugin_name in self.plugins:
            installed_list.addItem(plugin_name)
        installed_layout.addWidget(installed_list)
        
        # Boutons de gestion
        btn_layout = QHBoxLayout()
        install_btn = QPushButton("Installer un plugin")
        install_btn.clicked.connect(self.install_plugin)
        btn_layout.addWidget(install_btn)
        
        remove_btn = QPushButton("Supprimer le plugin sélectionné")
        remove_btn.clicked.connect(lambda: self.remove_plugin(installed_list.currentItem()))
        btn_layout.addWidget(remove_btn)
        
        installed_layout.addLayout(btn_layout)
        
        # Plugins disponibles
        available_group = QGroupBox("Plugins disponibles (en ligne)")
        available_layout = QVBoxLayout(available_group)
        
        available_list = QListWidget()
        available_list.addItems(["Plugin 1", "Plugin 2", "Plugin 3"])  # À remplacer par une vraie liste
        available_layout.addWidget(available_list)
        
        download_btn = QPushButton("Télécharger et installer")
        download_btn.clicked.connect(lambda: self.download_plugin(available_list.currentItem()))
        available_layout.addWidget(download_btn)
        
        # Ajouter les groupes au layout principal
        layout.addWidget(installed_group)
        layout.addWidget(available_group)
        
        # Boutons de dialogue
        btn_box = QDialogButtonBox(QDialogButtonBox.Close)
        btn_box.rejected.connect(dialog.reject)
        layout.addWidget(btn_box)
        
        dialog.exec_()
    
    def install_plugin(self):
        """Installe un plugin à partir d'un fichier ZIP"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner le fichier du plugin", 
            "", "Fichiers ZIP (*.zip);;Tous les fichiers (*)"
        )
        
        if file_path:
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    # Vérifier la structure du plugin
                    required_files = ['__init__.py', 'plugin.py']
                    if not all(f in zip_ref.namelist() for f in required_files):
                        raise ValueError("Le fichier ZIP ne contient pas tous les fichiers nécessaires pour un plugin")
                    
                    # Extraire dans le dossier plugins
                    plugin_name = os.path.splitext(os.path.basename(file_path))[0]
                    extract_path = os.path.join(self.plugins_dir, plugin_name)
                    zip_ref.extractall(extract_path)
                
                # Recharger les plugins
                self.load_plugins()
                QMessageBox.information(self, "Succès", "Plugin installé avec succès!")
            
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'installation du plugin:\n{str(e)}")
    
    def remove_plugin(self, item):
        """Supprime un plugin installé"""
        if not item:
            return
            
        plugin_name = item.text()
        reply = QMessageBox.question(
            self, "Confirmation", 
            f"Êtes-vous sûr de vouloir supprimer le plugin {plugin_name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                plugin_path = os.path.join(self.plugins_dir, plugin_name + ".py")
                if os.path.exists(plugin_path):
                    os.remove(plugin_path)
                
                # Recharger les plugins
                self.load_plugins()
                QMessageBox.information(self, "Succès", "Plugin supprimé avec succès!")
            
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression du plugin:\n{str(e)}")
    
    def download_plugin(self, item):
        """Télécharge et installe un plugin depuis le dépôt en ligne"""
        # Implémentation simplifiée - dans une vraie application, vous auriez
        # un système de dépôt de plugins avec une API
        QMessageBox.information(
            self, "Information", 
            "Cette fonctionnalité nécessite une connexion à un dépôt de plugins en ligne.\n" +
            "Dans une application réelle, cela téléchargerait et installerait le plugin sélectionné."
        )
    
    def open_pdf(self, file_path=None, password=None):
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Ouvrir un fichier PDF", "", 
                "Fichiers PDF (*.pdf);;Tous les fichiers (*)"
            )
        
        if file_path:
            try:
                # Fermer le document actuel s'il existe
                if self.pdf_document:
                    self.pdf_document.close()
                
                # Ouvrir le nouveau document
                if password:
                    self.pdf_document = fitz.open(file_path, password=password)
                    self.password = password
                else:
                    self.pdf_document = fitz.open(file_path)
                    self.password = None
                
                self.current_file = file_path
                self.current_page = 0
                self.modified = False
                
                # Extraire le texte et les métadonnées
                self.extract_text_and_metadata()
                
                # Générer les miniatures
                self.generate_thumbnails()
                
                # Afficher la première page
                self.display_current_page()
                
                # Mettre à jour l'interface
                self.update_ui_state()
                self.show_status_message(f"Fichier chargé: {os.path.basename(file_path)}", 3000)
                
            except Exception as e:
                if "password" in str(e).lower():
                    # Demander le mot de passe
                    self.open_secure_pdf(file_path)
                else:
                    QMessageBox.critical(self, "Erreur", f"Impossible d'ouvrir le fichier PDF:\n{str(e)}")
    
    def open_secure_pdf(self, file_path=None):
        """Ouvre un PDF protégé par mot de passe"""
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Ouvrir un PDF protégé", "", 
                "Fichiers PDF (*.pdf);;Tous les fichiers (*)"
            )
            if not file_path:
                return
        
        password, ok = QInputDialog.getText(
            self, "Mot de passe PDF", 
            "Ce PDF est protégé par mot de passe. Veuillez entrer le mot de passe:",
            QLineEdit.Password
        )
        
        if ok and password:
            try:
                self.open_pdf(file_path, password)
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Mot de passe incorrect ou erreur:\n{str(e)}")
    
    def save_secure_pdf(self):
        """Enregistre le PDF avec un mot de passe"""
        if not self.pdf_document:
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle("Enregistrer avec mot de passe")
        layout = QFormLayout(dialog)
        
        owner_pwd = QLineEdit()
        owner_pwd.setPlaceholderText("Mot de passe propriétaire (pour permissions)")
        owner_pwd.setEchoMode(QLineEdit.Password)
        layout.addRow("Propriétaire:", owner_pwd)
        
        user_pwd = QLineEdit()
        user_pwd.setPlaceholderText("Mot de passe utilisateur (pour ouvrir)")
        user_pwd.setEchoMode(QLineEdit.Password)
        layout.addRow("Utilisateur:", user_pwd)
        
        permissions = QComboBox()
        permissions.addItems([
            "Toutes permissions",
            "Interdire la modification",
            "Interdire la copie",
            "Interdire l'impression"
        ])
        layout.addRow("Permissions:", permissions)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            try:
                # Déterminer les permissions
                perm_map = {
                    0: pikepdf.Permissions.all(),
                    1: pikepdf.Permissions(modify=False),
                    2: pikepdf.Permissions(extract=False),
                    3: pikepdf.Permissions(print_lowres=False, print_highres=False)
                }
                
                perm = perm_map.get(permissions.currentIndex(), pikepdf.Permissions.all())
                
                # Enregistrer avec pikepdf pour un meilleur support du chiffrement
                with pikepdf.open(self.current_file) as pdf:
                    pdf.save(
                        self.current_file,
                        encryption=pikepdf.Encryption(
                            owner=owner_pwd.text() or None,
                            user=user_pwd.text() or None,
                            allow=perm
                        )
                    )
                
                self.modified = False
                self.update_status_bar()
                self.show_status_message("PDF enregistré avec protection par mot de passe", 3000)
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'enregistrement sécurisé:\n{str(e)}")
    
    def run_ocr(self):
        """Exécute la reconnaissance OCR sur le PDF"""
        if not self.pdf_document:
            return
            
        # Demander la langue pour l'OCR
        lang, ok = QInputDialog.getItem(
            self, "Langue OCR", 
            "Sélectionnez la langue du texte:",
            ["fra", "eng", "deu", "spa", "ita"], 0, False
        )
        
        if not ok:
            return
            
        # Configurer la boîte de dialogue de progression
        progress = QProgressDialog("OCR en cours...", "Annuler", 0, 100, self)
        progress.setWindowTitle("Reconnaissance de texte")
        progress.setWindowModality(Qt.WindowModal)
        progress.setAutoClose(True)
        
        # Créer et configurer le thread OCR
        self.ocr_thread = OCRThread(self.current_file, lang)
        
        # Connecter les signaux
        self.ocr_thread.progress.connect(progress.setValue)
        self.ocr_thread.finished.connect(self.on_ocr_finished)
        self.ocr_thread.error.connect(self.on_ocr_error)
        progress.canceled.connect(self.ocr_thread.cancel)
        
        # Démarrer le thread
        self.ocr_thread.start()
        
        # Afficher la progression
        progress.exec_()
    
    def on_ocr_finished(self, results):
        """Appelé lorsque l'OCR est terminé avec succès"""
        self.ocr_text.setPlainText("\n".join(results))
        self.tabs.setCurrentWidget(self.ocr_tab)
        self.show_status_message("OCR terminé avec succès", 3000)
        
        # Proposer d'ajouter le texte OCR au document
        reply = QMessageBox.question(
            self, "OCR Terminé", 
            "Voulez-vous ajouter le texte reconnu au document?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.text_edit.setPlainText(self.ocr_text.toPlainText())
            self.modified = True
            self.update_status_bar()

    def on_ocr_error(self, error_msg):
        """Appelé en cas d'erreur pendant l'OCR"""
        QMessageBox.critical(self, "Erreur OCR", f"Une erreur est survenue:\n{error_msg}")

    def compress_pdf(self):
        """Compresse le PDF pour réduire sa taille"""
        if not self.pdf_document:
            return
            
        options = [
            ("Haute qualité (taille réduite)", 3),
            ("Qualité moyenne (bonne compression)", 2),
            ("Faible qualité (compression maximale)", 1)
        ]
        
        option, ok = QInputDialog.getItem(
            self, "Compression PDF",
            "Niveau de compression:",
            [opt[0] for opt in options], 0, False
        )
        
        if not ok:
            return
            
        # Trouver la valeur correspondante
        level = next(opt[1] for opt in options if opt[0] == option)
        
        try:
            # Créer un fichier temporaire
            temp_file = os.path.join(self.temp_dir, "compressed.pdf")
            
            # Utiliser pikepdf pour la compression
            with pikepdf.open(self.current_file) as pdf:
                # Activer la compression
                pdf.save(temp_file, 
                        compress_streams=True, 
                        object_stream_mode=level)
            
            # Remplacer le fichier original
            os.replace(temp_file, self.current_file)
            
            # Recharger le document
            self.open_pdf(self.current_file)
            self.show_status_message("PDF compressé avec succès", 3000)
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la compression:\n{str(e)}")

    def add_signature(self):
        """Ajoute une signature électronique au PDF"""
        if not self.pdf_document:
            return
            
        # Créer une boîte de dialogue pour capturer la signature
        dialog = SignatureCaptureDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                # Obtenir la signature sous forme d'image
                signature_img = dialog.get_signature()
                
                # Demander la position sur la page
                page = self.pdf_document.load_page(self.current_page)
                rect = page.rect
                
                # Position par défaut (en bas à droite)
                img_rect = fitz.Rect(
                    rect.width - 150, rect.height - 80,
                    rect.width - 20, rect.height - 10
                )
                
                # Ajouter l'image de signature
                page.insert_image(img_rect, pixmap=fitz.Pixmap(signature_img))
                
                # Ajouter une annotation de signature
                annot = page.add_stamp_annot(img_rect, stamp=10)  # Stamp type 10 = "Approved"
                annot.set_colors(stroke=(0, 0, 1))  # Bleu
                annot.set_info(title="Signature", content="Signé électroniquement")
                annot.update()
                
                self.modified = True
                self.update_status_bar()
                self.display_current_page()
                self.show_status_message("Signature ajoutée avec succès", 3000)
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout de la signature:\n{str(e)}")

    def toggle_encryption_fields(self, state):
        """Active/désactive les champs de chiffrement"""
        enabled = state == Qt.Checked
        self.owner_pwd_edit.setEnabled(enabled)
        self.user_pwd_edit.setEnabled(enabled)
        self.permissions_combo.setEnabled(enabled)

    def load_settings(self):
        """Charge les paramètres de l'application"""
        self.settings.beginGroup("MainWindow")
        self.resize(self.settings.value("size", QSize(1200, 800)))
        self.move(self.settings.value("pos", QPoint(100, 100)))
        self.settings.endGroup()
        
        # Charger les chemins des outils externes
        self.settings.beginGroup("ExternalTools")
        self.tesseract_path = self.settings.value("tesseract_path", "")
        self.settings.endGroup()

    def save_settings(self):
        """Enregistre les paramètres de l'application"""
        self.settings.beginGroup("MainWindow")
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.settings.endGroup()

    def restore_state(self):
        """Restore window state from settings"""
        self.settings.beginGroup("MainWindow")
        if self.settings.value("maximized", False, type=bool):
            self.showMaximized()
        self.settings.endGroup()

    def show_status_message(self, message, timeout=0):
        """Affiche un message dans la barre de statut"""
        self.status_label.setText(message)
        if timeout > 0:
            QTimer.singleShot(timeout, lambda: self.status_label.setText("Prêt") if self.status_label.text() == message else None)

    def toggle_fullscreen(self):
        """Bascule en mode plein écran"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def show_documentation(self):
        """Ouvre la documentation"""
        QMessageBox.information(
            self, "Documentation",
            "Cette fonctionnalité ouvrirait normalement la documentation en ligne.\n\n" +
            "Dans une application réelle, cela pourrait ouvrir un navigateur web ou " +
            "une fenêtre d'aide intégrée."
        )

    def closeEvent(self, event):
        """Gère la fermeture de l'application"""
        if self.modified:
            reply = QMessageBox.question(
                self, "Modifications non enregistrées",
                "Vous avez des modifications non enregistrées. Voulez-vous les enregistrer avant de quitter?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Save:
                self.save_pdf()
                event.accept()
            elif reply == QMessageBox.Cancel:
                event.ignore()
                return
            else:
                event.accept()
        
        # Sauvegarder les paramètres
        self.save_settings()
        
        # Nettoyer les fichiers temporaires
        try:
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            print(f"Erreur lors du nettoyage des fichiers temporaires: {str(e)}")
        
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Configuration d'une palette de couleurs professionnelle
    palette = app.palette()
    palette.setColor(palette.Window, QColor(240, 240, 240))
    palette.setColor(palette.WindowText, Qt.black)
    palette.setColor(palette.Base, Qt.white)
    palette.setColor(palette.AlternateBase, QColor(245, 245, 245))
    palette.setColor(palette.ToolTipBase, QColor(255, 255, 220))
    palette.setColor(palette.ToolTipText, Qt.black)
    palette.setColor(palette.Text, Qt.black)
    palette.setColor(palette.Button, QColor(240, 240, 240))
    palette.setColor(palette.ButtonText, Qt.black)
    palette.setColor(palette.BrightText, Qt.red)
    palette.setColor(palette.Highlight, QColor(65, 105, 225))  # RoyalBlue
    palette.setColor(palette.HighlightedText, Qt.white)
    app.setPalette(palette)
    
    # Définir une feuille de style pour des éléments spécifiques
    app.setStyleSheet("""
        QToolBar {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #f0f0f0, stop:1 #e0e0e0);
            border-bottom: 1px solid #c0c0c0;
            spacing: 5px;
        }
        QToolButton {
            padding: 5px;
        }
        QStatusBar {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #e0e0e0, stop:1 #d0d0d0);
            border-top: 1px solid #c0c0c0;
        }
        QTabWidget::pane {
            border: 1px solid #c0c0c0;
            top: -1px;
        }
        QTabBar::tab {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #f0f0f0, stop:1 #e0e0e0);
            border: 1px solid #c0c0c0;
            padding: 5px 10px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #ffffff, stop:1 #f0f0f0);
            border-bottom-color: #ffffff;
        }
    """)
    
    window = PDFEditorApp()
    window.show()
    sys.exit(app.exec_())