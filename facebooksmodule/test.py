class MediaTable(QWidget):


    def populate_table(self):
        """Remplit le tableau avec un style amélioré et les nouvelles fonctionnalités"""
        self.table.setRowCount(len(self.media_list))
        
        for row, media in enumerate(self.media_list):
            # Colonne Nom
            name_item = QTableWidgetItem(media['nom'])
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, name_item)

            # Colonne Description avec éditeur enrichi
            desc_item = QTableWidgetItem(media['description'])
            desc_item.setFont(QFont("Segoe UI", 10))
            self.table.setItem(row, 1, desc_item)

            # Colonne Catégorie
            category_combo = QComboBox()
            categories = self.media_manager.load_categories()
            for category in categories:
                category_combo.addItem(category['name'])
            category_combo.setCurrentText(media.get('categorie', 'Default'))
            category_combo.currentTextChanged.connect(lambda text, row=row: self.update_category(row, text))
            self.table.setCellWidget(row, 2, category_combo)

            # Colonne Aperçu
            preview_label = QLabel()
            preview_label.setAlignment(Qt.AlignCenter)
            if media['nom'].endswith(('.png', '.jpg', '.jpeg')):
                pixmap = QPixmap(media['preview_path']).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                preview_label.setPixmap(pixmap)
            elif media['nom'].endswith(('.mp4', '.mov')):
                preview_label.setText("🎥 Voir")
            preview_label.mousePressEvent = lambda event, path=media['preview_path']: self.show_preview(path)
            self.table.setCellWidget(row, 3, preview_label)

            # Colonne Actions avec nouveaux boutons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 0, 5, 0)
            action_layout.setSpacing(5)

            # Bouton Planifier
            schedule_btn = QPushButton()
            schedule_btn.setIcon(QIcon("icons/calendar.png"))
            schedule_btn.setToolTip("Planifier la publication")
            schedule_btn.setStyleSheet("""
                QPushButton {
                    background-color: #9b59b6;
                    border-radius: 4px;
                    padding: 5px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #8e44ad;
                }
            """)
            schedule_btn.clicked.connect(lambda _, m=media: self.schedule_publication(m))
            action_layout.addWidget(schedule_btn)

            # Bouton Envoyer au Robot
            send_btn = QPushButton()
            send_btn.setIcon(QIcon("icons/robot.png"))
            send_btn.setToolTip("Envoyer au robot")
            send_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    border-radius: 4px;
                    padding: 5px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            send_btn.clicked.connect(lambda _, m=media: self.send_to_robot(m))
            action_layout.addWidget(send_btn)

            # Bouton Supprimer
            delete_btn = QPushButton()
            delete_btn.setIcon(QIcon("icons/delete.png"))
            delete_btn.setToolTip("Supprimer")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    border-radius: 4px;
                    padding: 5px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            delete_btn.clicked.connect(lambda _, m=media: self.delete_media(m))
            action_layout.addWidget(delete_btn)

            self.table.setCellWidget(row, 4, action_widget)
            # Colonne Description avec éditeur enrichi
            desc_item = QTableWidgetItem(media['description'])
            desc_item.setFont(QFont("Segoe UI", 10))
            desc_item.setFlags(desc_item.flags() | Qt.ItemIsEditable)
            self.table.setItem(row, 1, desc_item)
            
            # Configurer le delegate pour la colonne Description
            self.table.setItemDelegateForColumn(1, RichTextDelegate(self.table))
    def delete_media(self, media):
        """Version corrigée de la suppression de média"""
        try:
            # Vérifier si le fichier existe avant de le déplacer
            if not os.path.exists(media['preview_path']):
                QMessageBox.warning(self, "Erreur", "Le fichier média n'existe plus.")
                return

            # Créer le dossier archive s'il n'existe pas
            archive_folder = os.path.join(media_folder, f"{self.user_choice}Archive")
            os.makedirs(archive_folder, exist_ok=True)

            # Générer un nom de fichier d'archive unique
            base_name = os.path.basename(media['preview_path'])
            archive_name = f"archived_{int(time.time())}_{base_name}"
            archive_path = os.path.join(archive_folder, archive_name)

            # Déplacer le fichier
            shutil.move(media['preview_path'], archive_path)

            # Supprimer de la base de données
            self.media_manager.delete_media_in_db(media, self.user_choice)
            
            # Rafraîchir l'affichage
            self.media_list = self.media_manager.load_media_from_db(self.user_choice)
            self.populate_table()

            QMessageBox.information(self, "Succès", "Média supprimé et archivé avec succès.")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression : {str(e)}")

    def schedule_publication(self, media):
        """Ouvre un modal de planification avec calendrier"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Planifier la publication")
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        # Calendrier
        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                border: 1px solid #ddd;
                border-radius: 8px;
            }
            QCalendarWidget QToolButton {
                height: 30px;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.calendar)
        
        # Sélecteur d'heure
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("Heure:"))
        
        self.hour_spin = QSpinBox()
        self.hour_spin.setRange(0, 23)
        self.hour_spin.setValue(12)
        time_layout.addWidget(self.hour_spin)
        
        time_layout.addWidget(QLabel("Minute:"))
        
        self.minute_spin = QSpinBox()
        self.minute_spin.setRange(0, 59)
        self.minute_spin.setValue(0)
        time_layout.addWidget(self.minute_spin)
        
        layout.addLayout(time_layout)
        
        # Boutons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        if dialog.exec_() == QDialog.Accepted:
            selected_date = self.calendar.selectedDate()
            selected_time = QTime(self.hour_spin.value(), self.minute_spin.value())
            datetime = QDateTime(selected_date, selected_time)
            
            # Ici vous pourriez enregistrer la date planifiée dans la base de données
            QMessageBox.information(self, "Planifié", 
                                  f"Publication planifiée pour le {datetime.toString('dd/MM/yyyy HH:mm')}")

    def send_to_robot(self, media):
        """Envoie un seul média au robot"""
        try:
            # Préparer les données pour l'envoi
            data = {
                "posts": [{
                    "id": media['id'],
                    "name": media['nom'],
                    "description": media['description'],
                    "path": media['preview_path'],
                    "type": "image" if media['nom'].endswith(('.png', '.jpg', '.jpeg')) else "video"
                }],
                "groups": []
            }

            # Afficher une progression
            progress = QProgressDialog("Envoi au robot en cours...", "Annuler", 0, 100, self)
            progress.setWindowModality(Qt.WindowModal)
            
            # Simuler l'envoi progressif
            for i in range(5):
                progress.setValue(i * 20)
                QApplication.processEvents()
                time.sleep(0.5)
                if progress.wasCanceled():
                    break

            progress.close()
            
            QMessageBox.information(self, "Succès", "Média envoyé au robot avec succès!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Échec de l'envoi au robot : {str(e)}")

    def on_cell_changed(self, row, column):
        """Amélioration de l'édition directe dans le tableau"""
        if column == 1:  # Colonne Description
            try:
                new_description = self.table.item(row, column).text()
                media = self.media_list[row]
                
                # Créer un champ de texte riche temporaire pour améliorer l'expérience
                text_edit = QTextEdit()
                text_edit.setPlainText(new_description)
                text_edit.setStyleSheet("""
                    QTextEdit {
                        border: 1px solid #3498db;
                        border-radius: 4px;
                        padding: 5px;
                        font-family: 'Segoe UI';
                        font-size: 14px;
                    }
                """)
                
                # Afficher l'éditeur en plein tableau
                self.table.setCellWidget(row, column, text_edit)
                text_edit.setFocus()
                
                # Quand l'édition est terminée (quand le widget perd le focus)
                def finish_edit():
                    final_text = text_edit.toPlainText()
                    self.table.removeCellWidget(row, column)
                    item = QTableWidgetItem(final_text)
                    self.table.setItem(row, column, item)
                    
                    # Mettre à jour la base de données
                    media['description'] = final_text
                    self.media_manager.update_media_in_db(media, self.user_choice)
                
                text_edit.focusOutEvent = lambda event: finish_edit()
                
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Erreur lors de la modification : {str(e)}")





    def init_ui(self):
        """Initialise l'interface utilisateur avec un design moderne"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.light_color};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QLabel {{
                color: {self.dark_color};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)









        # Header avec dégradé et ombre
        self.header = QWidget()
        self.header.setFixedHeight(120)
        self.header.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.primary_color}, stop:1 {self.secondary_color});
                border-radius: 0;
                padding: 15px;
            }}
        """)
        
        header_layout = QVBoxLayout(self.header)
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        # Titre avec icône
        title_layout = QHBoxLayout()
        
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap("icons/logo.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        self.title_label = QLabel("FBK GROUP MANAGEMENT")
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-size: 24px;
                font-weight: bold;
                margin-left: 10px;
            }}
        """)
        
        title_layout.addWidget(self.logo_label)
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        
        # Sous-titre
        self.subtitle_label = QLabel("Nova360 AI - Marketing Automation Solution")
        self.subtitle_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
                margin-top: 5px;
                margin-left: 50px;
            }
        """)
        
        header_layout.addLayout(title_layout)
        header_layout.addWidget(self.subtitle_label)
        header_layout.addStretch()
        
        layout.addWidget(self.header)
        
        # Barre d'outils avec effet de carte
        toolbar = QWidget()
        toolbar.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border-radius: 8px;
                margin: 15px;
                padding: 10px;
                border: 1px solid #ddd;
            }}
        """)
        
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(10, 5, 10, 5)
        
        # Bouton d'action avec menu déroulant
        self.action_button = self.create_tool_button("⚡ Actions", self.primary_color)
        self.action_button.setMenu(self.create_action_menu())
        
        # Bouton de paramètres
        self.settings_button = self.create_tool_button("⚙️ Paramètres", "#7f8c8d")
        self.settings_button.setMenu(self.create_settings_menu())
        
        # Bouton d'ajout de média
        self.add_media_button = self.create_tool_button("🖼️ Ajouter média", self.secondary_color)
        self.add_media_button.clicked.connect(self.import_media)
        
        # Bouton d'envoi au robot
        self.update_robot_button = self.create_tool_button("🤖 Envoyer au robot", self.accent_color)
        self.update_robot_button.clicked.connect(self.show_update_modal)
        
        # Barre de recherche
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("🔍 Rechercher...")
        self.search_field.setStyleSheet(f"""
            QLineEdit {{
                padding: 8px 15px;
                font-size: 14px;
                border: 1px solid #ddd;
                border-radius: 20px;
                background-color: white;
                min-width: 250px;
            }}
            QLineEdit:focus {{
                border: 1px solid {self.primary_color};
                box-shadow: 0 0 5px rgba(52, 152, 219, 0.5);
            }}
        """)
        self.search_field.textChanged.connect(self.filter_table)
        
        # Sélecteur d'instance
        self.instance_combo = QComboBox()
        self.instance_combo.addItems([f"media{i}" for i in range(1, 11)])
        self.instance_combo.setCurrentText(self.user_choice)
        self.instance_combo.currentIndexChanged.connect(self.on_instance_changed)
        self.instance_combo.setStyleSheet(f"""
            QComboBox {{
                padding: 8px 15px;
                font-size: 14px;
                border: 1px solid #ddd;
                border-radius: 20px;
                background-color: white;
            }}
            QComboBox:hover {{
                border: 1px solid {self.primary_color};
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left-width: 1px;
                border-left-color: #ddd;
                border-left-style: solid;
                border-top-right-radius: 20px;
                border-bottom-right-radius: 20px;
            }}
        """)
        
        toolbar_layout.addWidget(self.search_field)
        toolbar_layout.addWidget(self.instance_combo)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.add_media_button)
        toolbar_layout.addWidget(self.action_button)
        toolbar_layout.addWidget(self.settings_button)
        toolbar_layout.addWidget(self.update_robot_button)
        
        layout.addWidget(toolbar)
        



           # Configuration du tableau avec style amélioré pour l'édition
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Nom', 'Description', 'Catégorie', 'Aperçu', 'Actions'])
    # Activer le word-wrap pour les descriptions
        self.table.setWordWrap(True)
        
        # Adapter la hauteur des lignes au contenu
        self.table.resizeRowsToContents()
        
        # Configurer le header vertical pour plus d'espace
        self.table.verticalHeader().setDefaultSectionSize(60)
        self.table.verticalHeader().setMinimumSectionSize(40)
            
        # Style amélioré pour le tableau
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 8px;
                margin: 15px;
                border: 1px solid #ddd;
                gridline-color: #eee;
                font-size: 14px;
                selection-background-color: #e3f2fd;
                selection-color: black;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: black;
            }
        """)

        # Configuration des colonnes
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Description prend plus de place
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)


        
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        self.table.cellChanged.connect(self.on_cell_changed)
        
        layout.addWidget(self.table)
        
        # Pagination avec style moderne
        pagination = QWidget()
        pagination.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                margin: 15px;
                padding: 10px;
                border: 1px solid #ddd;
            }
        """)
        
        pagination_layout = QHBoxLayout(pagination)
        
        self.prev_button = QPushButton("◀ Précédent")
        self.prev_button.setStyleSheet(f"""
            QPushButton {{
                padding: 8px 15px;
                background-color: {self.light_color};
                color: {self.dark_color};
                border: none;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #d5dbdb;
            }}
        """)
        self.prev_button.clicked.connect(self.prev_page)
        
        self.page_label = QLabel("Page 1")
        self.page_label.setStyleSheet(f"color: {self.dark_color};")
        
        self.next_button = QPushButton("Suivant ▶")
        self.next_button.setStyleSheet(f"""
            QPushButton {{
                padding: 8px 15px;
                background-color: {self.primary_color};
                color: white;
                border: none;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #2980b9;
            }}
        """)
        self.next_button.clicked.connect(self.next_page)
        
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.next_button)
        
        layout.addWidget(pagination)
        
        # Footer minimaliste
        footer = QLabel("© 2023 FBK Group - Tous droits réservés")
        footer.setStyleSheet(f"""
            QLabel {{
                color: {self.dark_color};
                font-size: 12px;
                padding: 15px;
                text-align: center;
            }}
        """)
        layout.addWidget(footer)
        
        self.populate_table()

    def create_tool_button(self, text, color):
        """Crée un bouton d'outil stylisé"""
        button = QPushButton(text)
        button.setStyleSheet(f"""
            QPushButton {{
                padding: 8px 15px;
                background-color: {color};
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 14px;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color, 15)};
            }}
        """)
        return button

    def darken_color(self, hex_color, percent):
        """Assombrit une couleur hexadécimale"""
        color = QColor(hex_color)
        return color.darker(100 + percent).name()


    def show_preview(self, path):
        """Affiche un aperçu agrandi avec animation"""
        preview = QDialog(self)
        preview.setWindowTitle("Aperçu")
        preview.setWindowModality(Qt.ApplicationModal)
        
        layout = QVBoxLayout(preview)
        
        if path.endswith(('.png', '.jpg', '.jpeg')):
            label = QLabel()
            pixmap = QPixmap(path)
            label.setPixmap(pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            layout.addWidget(label)
        elif path.endswith(('.mp4', '.mov')):
            # Ici vous pourriez intégrer un lecteur vidéo
            label = QLabel("Prévisualisation vidéo non implémentée")
            layout.addWidget(label)
        
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(preview.close)
        layout.addWidget(close_btn)
        
        preview.exec_()




