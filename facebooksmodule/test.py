
    def go_to_page(self, page_num):
        """Aller à une page spécifique"""
        if 1 <= page_num <= self.total_pages:
            self.current_page = page_num
            self.update_pagination()
            self.populate_table()

    def on_page_edit_changed(self):
        """Gère le changement de page via l'édition directe"""
        try:
            page_num = int(self.page_edit.text())
            self.go_to_page(page_num)
        except ValueError:
            pass

    def update_pagination(self):
        """Met à jour l'état des boutons de pagination et les labels"""
        # Calculer le nombre total de pages
        items_per_page = int(self.items_per_page.currentText()) if self.items_per_page.currentText() != "Tous" else float('inf')
        self.total_pages = max(1, math.ceil(len(self.media_data) / items_per_page)) if items_per_page != float('inf') else 1
        
        # Mettre à jour les boutons
        self.prev_button.setEnabled(self.current_page > 1)
        self.next_button.setEnabled(self.current_page < self.total_pages)
        self.first_page_button.setEnabled(self.current_page > 1)
        self.last_page_button.setEnabled(self.current_page < self.total_pages)
        
        # Mettre à jour les labels
        self.page_edit.setText(str(self.current_page))
        self.page_label.setText(f"/ {self.total_pages}")
        self.stats_label.setText(f"Total: {len(self.media_data)} médias | Page {self.current_page}/{self.total_pages}")

    def prev_page(self):
        """Aller à la page précédente"""
        if self.current_page > 1:
            self.current_page -= 1
            self.update_pagination()
            self.populate_table()

    def next_page(self):
        """Aller à la page suivante"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_pagination()
            self.populate_table()