from .short_links_model import ShortLinksModel
from .short_links_widget import ShortLinksWidget

class ShortLinksController:
    def __init__(self, model: ShortLinksModel, view: ShortLinksWidget):
        self.model = model
        self.view = view
        self.connect_signals()
        self.load_links()

    def connect_signals(self):
        self.view.create_button.clicked.connect(self.create_short_link)
        self.view.refresh_button.clicked.connect(self.load_links)
        self.view.copy_button.clicked.connect(self.copy_short_link)
        self.view.delete_button.clicked.connect(self.delete_short_link)

    def load_links(self):
        try:
            links = self.model.get_all_links()
            self.view.display_links(links)
        except Exception as e:
            self.view.show_message("Error", f"Failed to load links: {e}")

    def create_short_link(self):
        original_url = self.view.get_original_url()
        if not original_url.startswith(('http://', 'https://')):
            self.view.show_message("Validation Error", "Please enter a valid URL (starting with http:// or https://).")
            return

        try:
            self.model.create_short_link(original_url)
            self.view.clear_url_input()
            self.load_links()
            self.view.show_message("Success", "Short link created successfully.")
        except Exception as e:
            self.view.show_message("Error", f"Failed to create short link: {e}")

    def copy_short_link(self):
        link_id, short_link_text = self.view.get_selected_link_info()
        if link_id is None:
            self.view.show_message("Info", "Please select a link from the table to copy.")
            return
        self.view.copy_to_clipboard(short_link_text)

    def delete_short_link(self):
        link_id, _ = self.view.get_selected_link_info()
        if link_id is None:
            self.view.show_message("Info", "Please select a link from the table to delete.")
            return

        try:
            self.model.delete_link(link_id)
            self.load_links()
            self.view.show_message("Success", f"Link ID {link_id} deleted successfully.")
        except Exception as e:
            self.view.show_message("Error", f"Failed to delete link: {e}")

    def get_view(self):
        return self.view
