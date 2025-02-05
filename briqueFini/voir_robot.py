import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class JSONEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Editor")
        self.root.geometry("800x600")

        # Variables
        self.robot_folders = []
        self.selected_robot = tk.StringVar()
        self.selected_file = tk.StringVar()
        self.data = {}

        # UI Elements
        self.create_widgets()

        # Load robot folders
        self.load_robot_folders()

    def create_widgets(self):
        # Robot Selection
        ttk.Label(self.root, text="Select Robot:").grid(row=0, column=0, padx=10, pady=10)
        self.robot_combobox = ttk.Combobox(self.root, textvariable=self.selected_robot)
        self.robot_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.robot_combobox.bind("<<ComboboxSelected>>", self.on_robot_select)

        # File Selection
        ttk.Label(self.root, text="Select File:").grid(row=1, column=0, padx=10, pady=10)
        self.file_combobox = ttk.Combobox(self.root, textvariable=self.selected_file)
        self.file_combobox.grid(row=1, column=1, padx=10, pady=10)
        self.file_combobox.bind("<<ComboboxSelected>>", self.on_file_select)

        # Data Display
        self.data_text = tk.Text(self.root, wrap=tk.NONE)
        self.data_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Buttons
        ttk.Button(self.root, text="Add Group", command=self.add_group).grid(row=3, column=0, padx=10, pady=10)
        ttk.Button(self.root, text="Edit Group", command=self.edit_group).grid(row=3, column=1, padx=10, pady=10)
        ttk.Button(self.root, text="Delete Group", command=self.delete_group).grid(row=3, column=2, padx=10, pady=10)

        ttk.Button(self.root, text="Add Media", command=self.add_media).grid(row=4, column=0, padx=10, pady=10)
        ttk.Button(self.root, text="Edit Media", command=self.edit_media).grid(row=4, column=1, padx=10, pady=10)
        ttk.Button(self.root, text="Delete Media", command=self.delete_media).grid(row=4, column=2, padx=10, pady=10)

        # Configure grid weights
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def load_robot_folders(self):
        base_dir = "c:/bon"
        if os.path.exists(base_dir):
            self.robot_folders = [folder for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder))]
            self.robot_combobox['values'] = self.robot_folders
            if self.robot_folders:
                self.selected_robot.set(self.robot_folders[0])
                self.on_robot_select()

    def on_robot_select(self, event=None):
        robot_folder = self.selected_robot.get()
        base_dir = os.path.join("c:/bon", robot_folder)
        files = [f for f in os.listdir(base_dir) if f.endswith('.json')]
        self.file_combobox['values'] = files
        if files:
            self.selected_file.set(files[0])
            self.on_file_select()

    def on_file_select(self, event=None):
        robot_folder = self.selected_robot.get()
        file_name = self.selected_file.get()
        file_path = os.path.join("c:/bon", robot_folder, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
                self.display_data()

    def display_data(self):
        self.data_text.delete(1.0, tk.END)
        self.data_text.insert(tk.END, json.dumps(self.data, indent=4))

    def add_group(self):
        group = simpledialog.askstring("Add Group", "Enter group URL:")
        if group:
            if 'groups' not in self.data:
                self.data['groups'] = []
            self.data['groups'].append(group)
            self.save_data()
            self.display_data()

    def edit_group(self):
        selected_group = simpledialog.askstring("Edit Group", "Enter new group URL:")
        if selected_group:
            if 'groups' in self.data and self.data['groups']:
                self.data['groups'][0] = selected_group  # Example: Edit the first group
                self.save_data()
                self.display_data()

    def delete_group(self):
        if 'groups' in self.data and self.data['groups']:
            self.data['groups'].pop(0)  # Example: Delete the first group
            self.save_data()
            self.display_data()

    def add_media(self):
        media = simpledialog.askstring("Add Media", "Enter media path:")
        if media:
            if 'posts' not in self.data:
                self.data['posts'] = []
            self.data['posts'].append({"text": "New Media", "image": media})
            self.save_data()
            self.display_data()

    def edit_media(self):
        media = simpledialog.askstring("Edit Media", "Enter new media path:")
        if media:
            if 'posts' in self.data and self.data['posts']:
                self.data['posts'][0]['image'] = media  # Example: Edit the first media
                self.save_data()
                self.display_data()

    def delete_media(self):
        if 'posts' in self.data and self.data['posts']:
            self.data['posts'].pop(0)  # Example: Delete the first media
            self.save_data()
            self.display_data()

    def save_data(self):
        robot_folder = self.selected_robot.get()
        file_name = self.selected_file.get()
        file_path = os.path.join("c:/bon", robot_folder, file_name)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = JSONEditorApp(root)
    root.mainloop()