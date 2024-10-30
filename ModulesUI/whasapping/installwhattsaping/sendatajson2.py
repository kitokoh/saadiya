import os
import ctypes
import json
from PyQt5.QtWidgets import QApplication, QMessageBox, QProgressDialog
from PyQt5.QtCore import Qt
from datetime import datetime

class FileTransferApp2:
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
        if not self.confirm_submission():
            self.show_error("Processus annulé par l'utilisateur.")
            return

        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)

        progress_dialog = QProgressDialog("Copie des fichiers en cours...", "Annuler", 0, 100)
        progress_dialog.setWindowTitle("Processus de transfert")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.setValue(0)

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
            target_data1_path = os.path.join(target_folder, "data1.json")
            
            if os.path.exists(source_json_path):
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)

                if os.path.exists(target_data1_path):
                    self.rename_existing_file(target_data1_path)
                
                combined_content = self.combine_json_files(source_json_path)

                tmp_json_path = os.path.join(os.path.expanduser("~"), "Downloads", "data.tmp.json")
                with open(tmp_json_path, 'w', encoding='utf-8') as tmp_file:
                    json.dump(combined_content, tmp_file, ensure_ascii=False, indent=4)

                with open(tmp_json_path, 'r', encoding='utf-8') as tmp_file:
                    with open(target_data1_path, 'w', encoding='utf-8') as json_file:
                        json.dump(json.load(tmp_file), json_file, ensure_ascii=False, indent=4)

                os.remove(tmp_json_path)

                self.hide_file(target_folder)
            
            progress_dialog.setValue(int((idx + 1) / total_files * 100))
            
            if progress_dialog.wasCanceled():
                self.show_error("Processus annulé.")
                return
        
        progress_dialog.setValue(100)
        self.show_success("Le processus est terminé avec succès.")

    def confirm_submission(self):
        reply = QMessageBox.question(
            None,
            "Confirmation",
            "Avez-vous vérifié que tous les médias et leurs descriptions sont corrects avant de les soumettre au robot ?",
            QMessageBox.Yes | QMessageBox.No
        )
        return reply == QMessageBox.Yes
        
    def rename_existing_file(self, file_path):
        directory, old_filename = os.path.split(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"data1_backup_{timestamp}.json"
        new_file_path = os.path.join(directory, new_filename)
        os.rename(file_path, new_file_path)

    def hide_file(self, file_path):
        if os.path.exists(file_path):
            ctypes.windll.kernel32.SetFileAttributesW(file_path, 0x02 | 0x04)

    def show_error(self, message):
        QMessageBox.critical(None, "Erreur", message)

    def show_success(self, message):
        QMessageBox.information(None, "Succès", message)

    def combine_json_files(self, source_json_path):
        combined_content = {"posts": [], "images": [], "groups": []}

        try:
            with open(source_json_path, 'r', encoding='utf-8') as data_file:
                data_content = json.load(data_file)
                combined_content["posts"] = [post["text"] for post in data_content.get("posts", [])]
                combined_content["images"] = [post["image"] for post in data_content.get("posts", [])]
        except Exception as e:
            self.show_error(f"Erreur lors de la lecture de {source_json_path}: {e}")

        groups_json_path = os.path.join(self.source_dir, "text1", "groups.json")
        try:
            with open(groups_json_path, 'r', encoding='utf-8') as groups_file:
                groups_content = json.load(groups_file)
                combined_content["groups"] = [group["link"] for group in groups_content.get("groups", [])]
        except Exception as e:
            self.show_error(f"Erreur lors de la lecture de {groups_json_path}: {e}")

        return combined_content


if __name__ == "__main__":
    app = QApplication([])
    transfer_app = FileTransferApp2()
    transfer_app.start_process()
    app.exec_()
