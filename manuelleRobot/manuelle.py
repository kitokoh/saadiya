import sys
import json
import os
import webbrowser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                            QPushButton, QLabel, QTextEdit, QHBoxLayout,
                            QGroupBox, QSpinBox, QFileDialog, QProgressBar,
                            QMessageBox, QListWidget, QTabWidget, QCheckBox)
from PyQt5.QtCore import Qt, QTimer, QSettings

class UltimateLinkOpener(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("LinkOpener", "Ultimate")
        self.load_settings()
        self.init_ui()
        self.load_last_file()
        
    def load_settings(self):
        self.json_path = self.settings.value("json_path", r"C:\bon\robot1\data.json")
        self.chrome_path = self.settings.value("chrome_path", r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        self.group_size = int(self.settings.value("group_size", 10))
        self.auto_pause = self.settings.value("auto_pause", True, type=bool)
        
    def save_settings(self):
        self.settings.setValue("json_path", self.json_path)
        self.settings.setValue("chrome_path", self.chrome_path)
        self.settings.setValue("group_size", self.group_size)
        self.settings.setValue("auto_pause", self.auto_pause)
        self.settings.setValue("last_file", self.json_path)
        
    def init_ui(self):
        self.setWindowTitle("Ultimate Link Opener")
        self.setGeometry(100, 100, 800, 600)
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Main Tab
        self.main_tab = QWidget()
        self.tabs.addTab(self.main_tab, "Contrôle")
        
        # Links Tab
        self.links_tab = QWidget()
        self.tabs.addTab(self.links_tab, "Liste des Liens")
        
        self.setup_main_tab()
        self.setup_links_tab()
        self.statusBar().showMessage("Prêt")
        
    def setup_main_tab(self):
        layout = QVBoxLayout()
        
        # Configuration Group
        config_group = QGroupBox("Configuration")
        config_layout = QVBoxLayout()
        
        # File Selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel("Fichier JSON:")
        self.file_path_label = QLabel(self.json_path)
        browse_btn = QPushButton("Parcourir...")
        browse_btn.clicked.connect(self.browse_json)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_path_label, 1)
        file_layout.addWidget(browse_btn)
        config_layout.addLayout(file_layout)
        
        # Chrome Selection
        chrome_layout = QHBoxLayout()
        chrome_label = QLabel("Chemin de Chrome:")
        self.chrome_path_label = QLabel(self.chrome_path)
        chrome_browse_btn = QPushButton("Parcourir...")
        chrome_browse_btn.clicked.connect(self.browse_chrome)
        chrome_layout.addWidget(chrome_label)
        chrome_layout.addWidget(self.chrome_path_label, 1)
        chrome_layout.addWidget(chrome_browse_btn)
        config_layout.addLayout(chrome_layout)
        
        # Settings
        settings_layout = QHBoxLayout()
        settings_layout.addWidget(QLabel("Liens par groupe:"))
        self.group_size_spin = QSpinBox()
        self.group_size_spin.setRange(1, 50)
        self.group_size_spin.setValue(self.group_size)
        settings_layout.addWidget(self.group_size_spin)
        
        self.auto_pause_check = QCheckBox("Pause auto entre groupes")
        self.auto_pause_check.setChecked(self.auto_pause)
        settings_layout.addWidget(self.auto_pause_check)
        config_layout.addLayout(settings_layout)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Control Group
        control_group = QGroupBox("Contrôle")
        control_layout = QVBoxLayout()
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.load_btn = QPushButton("Charger les liens")
        self.load_btn.clicked.connect(self.load_links)
        btn_layout.addWidget(self.load_btn)
        
        self.open_group_btn = QPushButton("Ouvrir le prochain groupe")
        self.open_group_btn.clicked.connect(self.open_next_group)
        self.open_group_btn.setEnabled(False)
        btn_layout.addWidget(self.open_group_btn)
        
        self.open_all_btn = QPushButton("Ouvrir tous les liens")
        self.open_all_btn.clicked.connect(self.open_all_links)
        self.open_all_btn.setEnabled(False)
        btn_layout.addWidget(self.open_all_btn)
        
        control_layout.addLayout(btn_layout)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        control_layout.addWidget(self.progress_bar)
        
        # Log
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        control_layout.addWidget(self.log)
        
        control_group.setLayout(control_layout)
        layout.addWidget(control_group)
        
        self.main_tab.setLayout(layout)
        
    def setup_links_tab(self):
        layout = QVBoxLayout()
        
        # Links List
        self.links_list = QListWidget()
        self.links_list.itemDoubleClicked.connect(self.open_selected_link)
        layout.addWidget(self.links_list)
        
        # Control Buttons
        btn_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("Actualiser")
        self.refresh_btn.clicked.connect(self.display_links)
        btn_layout.addWidget(self.refresh_btn)
        
        self.open_selected_btn = QPushButton("Ouvrir la sélection")
        self.open_selected_btn.clicked.connect(self.open_selected_links)
        btn_layout.addWidget(self.open_selected_btn)
        
        layout.addLayout(btn_layout)
        self.links_tab.setLayout(layout)
        
    def browse_json(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner le fichier JSON", 
            os.path.dirname(self.json_path) if self.json_path else "",
            "Fichiers JSON (*.json);;Tous les fichiers (*.*)"
        )
        
        if file:
            self.json_path = file
            self.file_path_label.setText(file)
            self.save_settings()
            self.load_links()
            
    def browse_chrome(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Localiser Chrome", 
            os.path.dirname(self.chrome_path) if self.chrome_path else "",
            "Exécutable Chrome (chrome.exe);;Tous les fichiers (*.*)"
        )
        
        if file:
            self.chrome_path = file
            self.chrome_path_label.setText(file)
            self.save_settings()
            
    def load_last_file(self):
        if os.path.exists(self.json_path):
            self.load_links()
            
    def load_links(self):
        self.links = []
        
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.links = data.get('groups', [])
                
                if not self.links:
                    self.log.append("Aucun lien trouvé dans le fichier JSON!")
                    return
                
                self.log.append(f"✅ {len(self.links)} liens chargés depuis {os.path.basename(self.json_path)}")
                self.statusBar().showMessage(f"{len(self.links)} liens prêts", 3000)
                
                self.open_group_btn.setEnabled(True)
                self.open_all_btn.setEnabled(True)
                self.progress_bar.setMaximum(len(self.links))
                self.progress_bar.setValue(0)
                
                self.display_links()
                self.save_settings()
                
        except Exception as e:
            self.log.append(f"❌ Erreur de chargement: {str(e)}")
            QMessageBox.critical(self, "Erreur", f"Impossible de charger le fichier:\n{str(e)}")
            
    def display_links(self):
        self.links_list.clear()
        for i, link in enumerate(self.links):
            display_text = link if isinstance(link, str) else link.get('url', '')
            if display_text:  # Only add if we have text to display
                self.links_list.addItem(f"{i+1}. {display_text[:200]}{'...' if len(display_text) > 200 else ''}")
            
    def open_next_group(self):
        current_pos = self.progress_bar.value()
        remaining = len(self.links) - current_pos
        
        if remaining <= 0:
            self.log.append("Tous les liens ont déjà été ouverts!")
            return
            
        group_size = min(self.group_size_spin.value(), remaining)
        end_pos = current_pos + group_size
        
        self.log.append(f"\n🔷 Ouverture du groupe (liens {current_pos+1}-{end_pos}):")
        
        for i in range(current_pos, end_pos):
            if i >= len(self.links):  # Safety check
                break
                
            link = self.links[i]
            url = link if isinstance(link, str) else link.get('url', '')
            
            if not url:  # Skip if no URL
                continue
                
            try:
                if self.chrome_path and os.path.exists(self.chrome_path):
                    os.startfile(self.chrome_path, url)
                else:
                    webbrowser.open(url)
                    
                self.log.append(f"   ✓ {i+1}. {url[:80]}...")
                item = self.links_list.item(i)
                if item:
                    item.setBackground(Qt.green)
            except Exception as e:
                self.log.append(f"   ✗ {i+1}. ERREUR: {str(e)}")
                item = self.links_list.item(i)
                if item:
                    item.setBackground(Qt.red)
            
            self.progress_bar.setValue(i + 1)
            QApplication.processEvents()
            
        if self.auto_pause_check.isChecked() and end_pos < len(self.links):
            self.log.append("\n⏸ Pause entre les groupes...")
            QMessageBox.information(
                self, "Pause", 
                f"Groupe terminé. Prêt pour le prochain groupe?", 
                QMessageBox.Ok
            )
                
    def open_all_links(self):
        remaining = len(self.links) - self.progress_bar.value()
        if remaining <= 0:
            self.log.append("Tous les liens ont déjà été ouverts!")
            return
            
        reply = QMessageBox.question(
            self, "Confirmation",
            f"Ouvrir les {remaining} liens restants?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            while self.progress_bar.value() < len(self.links):
                self.open_next_group()
                QApplication.processEvents()
                
    def open_selected_link(self, item):
        index = self.links_list.row(item)
        if index >= len(self.links):
            return
            
        link = self.links[index]
        url = link if isinstance(link, str) else link.get('url', '')
        
        try:
            if self.chrome_path and os.path.exists(self.chrome_path):
                os.startfile(self.chrome_path, url)
            else:
                webbrowser.open(url)
                
            self.log.append(f"✓ Lien sélectionné ouvert: {url[:80]}...")
            item.setBackground(Qt.green)
        except Exception as e:
            self.log.append(f"✗ ERREUR avec le lien sélectionné: {str(e)}")
            item.setBackground(Qt.red)
            
    def open_selected_links(self):
        selected = self.links_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Avertissement", "Aucun lien sélectionné!")
            return
            
        self.log.append(f"\n🔹 Ouverture de {len(selected)} liens sélectionnés:")
        
        for item in selected:
            self.open_selected_link(item)
            
    def closeEvent(self, event):
        self.group_size = self.group_size_spin.value()
        self.auto_pause = self.auto_pause_check.isChecked()
        self.save_settings()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UltimateLinkOpener()
    window.show()
    sys.exit(app.exec_())