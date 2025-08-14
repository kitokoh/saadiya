"""
Authentication service for the Leopardo V2 application.
"""

import os
import json
import sqlite3
import hashlib

class AuthService:
    """
    Handles user authentication and session management.
    """
    def __init__(self):
        """
        Initializes the authentication service.
        """
        self.db_path = "nova360.db"
        self.session_file = 'session.json'
        self.is_logged_in = False
        self.current_user = None
        self.is_pro = False
        self.is_enterprise = False
        self.load_session()

    def login(self, username, password):
        """
        Logs in a user.

        Args:
            username: The username of the user.
            password: The password of the user.

        Returns:
            True if the login is successful, False otherwise.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
            user = cursor.fetchone()

            conn.close()

            if user:
                self.is_logged_in = True
                self.current_user = user[1] # username
                # Assuming role is in the 4th column
                role = user[4]
                if role == 'admin' or role == 'enterprise':
                    self.is_pro = True
                    self.is_enterprise = True
                elif role == 'pro':
                    self.is_pro = True
                    self.is_enterprise = False
                else:
                    self.is_pro = False
                    self.is_enterprise = False

                self.save_session()
                return True
            return False
        except Exception as e:
            print(f"Error during login: {e}")
            return False

    def logout(self):
        """
        Logs out the current user.
        """
        self.is_logged_in = False
        self.current_user = None
        self.is_pro = False
        self.is_enterprise = False
        self.save_session()

    def save_session(self):
        """
        Saves the current session to a file.
        """
        session_data = {
            'is_logged_in': self.is_logged_in,
            'username': self.current_user,
            'is_pro': self.is_pro,
            'is_enterprise': self.is_enterprise
        }
        with open(self.session_file, 'w') as f:
            json.dump(session_data, f)

    def load_session(self):
        """
        Loads the session from a file.
        """
        if os.path.exists(self.session_file):
            with open(self.session_file, 'r') as f:
                try:
                    session_data = json.load(f)
                    self.is_logged_in = session_data.get('is_logged_in', False)
                    self.current_user = session_data.get('username', None)
                    self.is_pro = session_data.get('is_pro', False)
                    self.is_enterprise = session_data.get('is_enterprise', False)
                except json.JSONDecodeError:
                    self.is_logged_in = False
                    self.current_user = None
                    self.is_pro = False
                    self.is_enterprise = False

    def has_access(self, feature_level):
        """
        Checks if the current user has access to a feature.

        Args:
            feature_level: The level of the feature (e.g., "pro", "enterprise").

        Returns:
            True if the user has access, False otherwise.
        """
        if not self.is_logged_in:
            return False
        if feature_level == "pro" and not (self.is_pro or self.is_enterprise):
            return False
        if feature_level == "enterprise" and not self.is_enterprise:
            return False
        return True
