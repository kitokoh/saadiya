import os
import json

class AuthService:
    def __init__(self):
        self.session_file = 'session.json'
        self.is_logged_in = False
        self.current_user = None
        self.load_session()

    def login(self, username, password):
        # In a real application, you would verify the credentials against a database
        if username == "admin" and password == "password":
            self.is_logged_in = True
            self.current_user = username
            self.save_session()
            return True
        return False

    def logout(self):
        self.is_logged_in = False
        self.current_user = None
        self.save_session()

    def save_session(self):
        session_data = {
            'is_logged_in': self.is_logged_in,
            'username': self.current_user
        }
        with open(self.session_file, 'w') as f:
            json.dump(session_data, f)

    def load_session(self):
        if os.path.exists(self.session_file):
            with open(self.session_file, 'r') as f:
                try:
                    session_data = json.load(f)
                    self.is_logged_in = session_data.get('is_logged_in', False)
                    self.current_user = session_data.get('username', None)
                except json.JSONDecodeError:
                    self.is_logged_in = False
                    self.current_user = None
