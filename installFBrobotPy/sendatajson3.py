import os
import ctypes
import json
from PyQt5.QtWidgets import QApplication, QMessageBox, QProgressDialog
from PyQt5.QtCore import Qt
from datetime import datetime

class FileTransferApp3:
    def __init__(self):
        # Dossier source et cible
        self.source_dir = self.get_downloads_folder()
        self.target_dir = "C:\\Bon"
        
    def get_downloads_folder(self):
        """Récupère le chemin du dossier Téléchargements de l'utilisateur."""
        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads", "AI-FB-Robot", "text")
        if not os.path.exists(downloads_dir):
            self.show_error("Le dossier 'AI-FB-Robot/text' dans Téléchargements n'existe pas.")
        return downloads_dir

    def start_process(self):
        # Demander une confirmation avant de continuer
        if not self.confirm_submission():
            self.show_error("Processus annulé par l'utilisateur.")
            return

        # Vérification du dossier cible
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)

        # Créer une boîte de dialogue de progression
        progress_dialog = QProgressDialog("Copie des fichiers en cours...", "Annuler", 0, 100)
        progress_dialog.setWindowTitle("Processus de transfert")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.setValue(0)
        
        # Vérifier l'existence des dossiers source
        if not os.path.exists(self.source_dir):
            self.show_error("Le dossier source n'existe pas.")
            return
        
        subfolders = [f for f in os.listdir(self.source_dir) if f.startswith("text")]
        total_files = len(subfolders)
        
        if total_files == 0:
            self.show_error("Aucun fichier 'data.json' trouvé.")
            return
        
        for idx, folder_name in enumerate(subfolders):
            folder_num = folder_name.replace("text", "")
            source_json_path = os.path.join(self.source_dir, folder_name, "data.json")
            target_folder = os.path.join(self.target_dir, f"robot{folder_num}")
            target_json_path = os.path.join(target_folder, "data.json")
            
            if os.path.exists(source_json_path):
                # Vérifier si le fichier data.json existe déjà dans robotx
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)

                if os.path.exists(target_json_path):
                    # Renommer l'ancien fichier data.json dans robotx
                    self.rename_existing_file(target_json_path)
                
                # Combiner les fichiers JSON avant de copier
                combined_content = self.combine_json_files(source_json_path)

                # Créer le fichier data.tmp.json dans le dossier Téléchargements
                tmp_json_path = os.path.join(os.path.expanduser("~"), "Downloads", "data.tmp.json")
                with open(tmp_json_path, 'w', encoding='utf-8') as tmp_file:
                    json.dump(combined_content, tmp_file, ensure_ascii=False, indent=4)

                # Copier le contenu de data.tmp.json dans le nouveau data.json
                with open(tmp_json_path, 'r', encoding='utf-8') as tmp_file:
                    with open(target_json_path, 'w', encoding='utf-8') as json_file:
                        json.dump(json.load(tmp_file), json_file, ensure_ascii=False, indent=4)

                # Supprimer le fichier temporaire
                os.remove(tmp_json_path)

                # Cacher le dossier cible
                self.hide_file(target_folder)
            
            # Mise à jour de la progression
            progress_dialog.setValue(int((idx + 1) / total_files * 100))
            
            # En cas d'annulation
            if progress_dialog.wasCanceled():
                self.show_error("Processus annulé.")
                return
        
        # Finalisation du processus
        progress_dialog.setValue(100)
        self.show_success("Le processus est terminé avec succès.")

    def confirm_submission(self):
        """Demande à l'utilisateur de confirmer la soumission.""" 
        reply = QMessageBox.question(
            None,
            "Confirmation",
            "Avez-vous vérifié que tous les médias et leurs descriptions sont corrects avant de les soumettre au robot ?",
            QMessageBox.Yes | QMessageBox.No
        )
        return reply == QMessageBox.Yes
        
    def rename_existing_file(self, file_path):
        """Renomme le fichier data.json existant dans robotx.""" 
        directory, old_filename = os.path.split(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"data_backup_{timestamp}.json"
        new_file_path = os.path.join(directory, new_filename)
        os.rename(file_path, new_file_path)

    def hide_file(self, file_path):
        """Cache un fichier ou un dossier avec les attributs 'hidden' et 'system'.""" 
        if os.path.exists(file_path):
            ctypes.windll.kernel32.SetFileAttributesW(file_path, 0x02 | 0x04)

    def show_error(self, message):
        """Affiche une boîte de dialogue d'erreur.""" 
        QMessageBox.critical(None, "Erreur", message)

    def show_success(self, message):
        """Affiche une boîte de dialogue de succès.""" 
        QMessageBox.information(None, "Succès", message)

    def combine_json_files(self, source_json_path):
        """Combine les données de data.json et groups.json avec des images vides et en extrayant uniquement les liens des groupes."""
        combined_content = {}

        # Lire le fichier data.json source
        try:
            with open(source_json_path, 'r', encoding='utf-8') as data_file:
                data_content = json.load(data_file)
                # Ajouter les posts avec des chemins d'images vides
                combined_content["posts"] = [
                    {"text": post.get("text", ""), "image": ""} for post in data_content.get("posts", [])
                ]
        except Exception as e:
            self.show_error(f"Erreur lors de la lecture de {source_json_path}: {e}")

        # Lire le fichier groups.json source
        groups_json_path = os.path.join(self.source_dir, "text1", "groups.json")
        try:
            with open(groups_json_path, 'r', encoding='utf-8') as groups_file:
                groups_content = json.load(groups_file)
                # Extraire uniquement les liens des groupes
                combined_content["groups"] = [group["link"] for group in groups_content.get("groups", [])]
        except Exception as e:
            self.show_error(f"Erreur lors de la lecture de {groups_json_path}: {e}")

        return combined_content


# Lancement de l'application PyQt
if __name__ == "__main__":
    app = QApplication([])
    transfer_app = FileTransferApp3()
    transfer_app.start_process()
    app.exec_()
