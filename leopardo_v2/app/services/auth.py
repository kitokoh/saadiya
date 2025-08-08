"""
Authentication service for the Leopardo V2 application.
"""

import os
import json

class AuthService:
    """
    Handles user authentication and session management.
    """
    def __init__(self):
        """
        Initializes the authentication service.
        """
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
        # In a real application, you would verify the credentials against a database
        if username == "admin" and password == "password":
            self.is_logged_in = True
            self.current_user = username
            self.is_pro = True
            self.is_enterprise = True
            self.save_session()
            return True
        elif username == "user" and password == "password":
            self.is_logged_in = True
            self.current_user = username
            self.is_pro = False
            self.is_enterprise = False
            self.save_session()
            return True
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
        if feature_level == "pro" and not self.is_pro:
            return False
        if feature_level == "enterprise" and not self.is_enterprise:
            return False
        return True
