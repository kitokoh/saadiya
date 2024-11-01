import os
import ctypes

class IconHider:
    def __init__(self):
        self.desktop_path = self.get_desktop_path()

    def get_desktop_path(self):
        """Retourne le chemin du bureau de l'utilisateur."""
        return os.path.join(os.path.expanduser("~"), "Desktop")

    def hide_icon(self, icon_path):
        """Cache un fichier en le rendant invisible."""
        # Utilisation de l'API Windows pour cacher le fichier
        ctypes.windll.kernel32.SetFileAttributesW(icon_path, 2)  # 2 = FILE_ATTRIBUTE_HIDDEN

    def hide_icons_containing_robot(self):
        """Cache toutes les icônes sur le bureau contenant 'robot' dans le nom."""
        for filename in os.listdir(self.desktop_path):
            if 'robot' in filename.lower():  # Vérifie si 'robot' est dans le nom
                icon_path = os.path.join(self.desktop_path, filename)
                if os.path.isfile(icon_path):  # Vérifie si c'est un fichier
                    self.hide_icon(icon_path)
                    print(f"Fichier caché : {icon_path}")

if __name__ == "__main__":
    hider = IconHider()
    hider.hide_icons_containing_robot()  # Cache les icônes contenant 'robot'
