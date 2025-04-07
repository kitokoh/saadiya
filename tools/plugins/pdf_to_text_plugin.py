from PyQt5.QtWidgets import QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
import os

class Plugin:
    def __init__(self, app):
        self.app = app
        self.name = "Export PDF en Texte"
        self.description = "Exporte le contenu texte d'un PDF vers un fichier .txt"
        self.author = "PDF Editor Team"
        self.version = "1.0"
        self.icon = QIcon(":/text_export.png")  # Utilise une icône de ressources
    
    def run(self):
        # Vérifier qu'un PDF est chargé
        if not self.app.pdf_document:
            QMessageBox.warning(self.app, "Erreur", "Aucun PDF chargé!")
            return
        
        # Demander où sauvegarder le fichier texte
        file_path, _ = QFileDialog.getSaveFileName(
            self.app, "Exporter en texte", 
            os.path.splitext(self.app.current_file)[0] + ".txt", 
            "Fichiers texte (*.txt);;Tous les fichiers (*)"
        )
        
        if file_path:
            try:
                # Exporter le texte
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.app.text_edit.toPlainText())
                
                # Afficher un message de confirmation
                self.app.show_status_message(f"Texte exporté vers {os.path.basename(file_path)}", 3000)
                QMessageBox.information(
                    self.app, "Succès", 
                    f"Le contenu texte a été exporté avec succès vers:\n{file_path}"
                )
            
            except Exception as e:
                QMessageBox.critical(
                    self.app, "Erreur", 
                    f"Une erreur est survenue lors de l'export:\n{str(e)}"
                )
                