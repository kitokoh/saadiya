import sqlite3
import os
from datetime import datetime
import random

class FbRobotDatabase:
    def __init__(self, db_name='nova360.db'):
        project_root = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(project_root, '../../resources/data', db_name)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.connection = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute('DROP TABLE IF EXISTS media')
            cursor.execute('DROP TABLE IF EXISTS licences')
            cursor.execute('DROP TABLE IF EXISTS instances')
            cursor.execute('DROP TABLE IF EXISTS groups')
            cursor.execute('DROP TABLE IF EXISTS facebook_users')
            cursor.execute('DROP TABLE IF EXISTS alerts')
            cursor.execute('DROP TABLE IF EXISTS audit_log')
            cursor.execute('DROP TABLE IF EXISTS quotas')
            cursor.execute('DROP TABLE IF EXISTS backup_logs')
            cursor.execute('DROP TABLE IF EXISTS user_roles')
            cursor.execute('DROP TABLE IF EXISTS email_sessions')
            cursor.execute('DROP TABLE IF EXISTS user_sessions')
            cursor.execute('DROP TABLE IF EXISTS users')
            cursor.execute('DROP TABLE IF EXISTS contacts')
            cursor.execute('DROP TABLE IF EXISTS instance_user')
            cursor.execute('DROP TABLE IF EXISTS group_user')

            # Table instances
            cursor.execute('''CREATE TABLE IF NOT EXISTS instances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                status TEXT NOT NULL,
                type TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                deleted_at DATETIME,
                quota INTEGER,
                path TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )''')

            # Table licences
            cursor.execute('''CREATE TABLE IF NOT EXISTS licences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                label TEXT NOT NULL,
                description TEXT,
                duration INTEGER NOT NULL,
                status TEXT NOT NULL,
                instance_id INTEGER NOT NULL,
                request_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                license_type TEXT NOT NULL,
                type TEXT,
                FOREIGN KEY (instance_id) REFERENCES instances(id)
            )''')

            # Table media
            cursor.execute('''CREATE TABLE IF NOT EXISTS media (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                tag TEXT NOT NULL,
                label TEXT NOT NULL,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                deleted_at DATETIME,
                instance_id INTEGER NOT NULL,
                name TEXT,
                FOREIGN KEY (instance_id) REFERENCES instances(id)
            )''')

            # Table groups
            cursor.execute('''CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                label TEXT NOT NULL,
                description TEXT,
                link TEXT NOT NULL,
                category TEXT,
                tag TEXT NOT NULL,
                instance_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                deleted_at DATETIME,
                name TEXT,
                FOREIGN KEY (instance_id) REFERENCES instances(id)
            )''')

            # Table facebook_users
            cursor.execute('''CREATE TABLE IF NOT EXISTS facebook_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                instance_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                deleted_at DATETIME,
                facebook_name TEXT,
                FOREIGN KEY (instance_id) REFERENCES instances(id)
            )''')

            # Table alerts
            cursor.execute('''CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                type TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                alert_type TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )''')

            # Table audit_log
            cursor.execute('''CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                table_name TEXT NOT NULL,
                record_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                performed_by TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )''')

            # Table quotas
            cursor.execute('''CREATE TABLE IF NOT EXISTS quotas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                quota_limit INTEGER NOT NULL,
                current_usage INTEGER DEFAULT 0,
                instance_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                media_quota INTEGER,
                FOREIGN KEY (instance_id) REFERENCES instances(id)
            )''')

            # Table backup_logs
            cursor.execute('''CREATE TABLE IF NOT EXISTS backup_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                instance_id INTEGER NOT NULL,
                backup_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT NOT NULL,
                backup_file TEXT,
                FOREIGN KEY (instance_id) REFERENCES instances(id)
            )''')

            # Table user_roles
            cursor.execute('''CREATE TABLE IF NOT EXISTS user_roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role_name TEXT NOT NULL,
                description TEXT,
                user_id INTEGER
            )''')

            # Table email_sessions
            cursor.execute('''CREATE TABLE IF NOT EXISTS email_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_text TEXT NOT NULL,
                subject TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id INTEGER
            )''')

            # Table user_sessions
            cursor.execute('''CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                auth_token TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                expires_at DATETIME,
                session_token TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )''')

            # Table users
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                role_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME,
                FOREIGN KEY (role_id) REFERENCES user_roles(id)
            )''')

            # Table contacts
            cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                email TEXT,
                category TEXT,
                tag TEXT,
                user_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )''')

            # Table d'association entre instances et utilisateurs
            cursor.execute('''CREATE TABLE IF NOT EXISTS instance_user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                instance_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (instance_id) REFERENCES instances(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )''')

            # Table d'association entre groupes et utilisateurs
            cursor.execute('''CREATE TABLE IF NOT EXISTS group_user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (group_id) REFERENCES groups(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )''')

            self.connection.commit()

            print("Base de données et tables créées avec succès.")

        except sqlite3.Error as e:
            print(f"Erreur lors de la création des tables : {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def close(self):
        self.connection.close()

    def add_user(self, name, email, password, role_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users (name, email, password, role_id) VALUES (?, ?, ?, ?)''',
                       (name, email, password, role_id))
        self.connection.commit()
        return cursor.lastrowid

    def add_instance(self, name, status, instance_type, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO instances (name, status, type, user_id) VALUES (?, ?, ?, ?)''',
                       (name, status, instance_type, user_id))
        self.connection.commit()
        return cursor.lastrowid

    def add_license(self, label, description, duration, status, instance_id, license_type, license_type_description):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO licences (label, description, duration, status, instance_id, license_type, type)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (label, description, duration, status, instance_id, license_type, license_type_description))
        self.connection.commit()
        return cursor.lastrowid

    def add_media(self, file_path, tag, label, instance_id, name):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO media (file_path, tag, label, instance_id, name) VALUES (?, ?, ?, ?, ?)''',
                       (file_path, tag, label, instance_id, name))
        self.connection.commit()
        return cursor.lastrowid

    def add_group(self, label, description, link, category, tag, instance_id, name):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO groups (label, description, link, category, tag, instance_id, name)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (label, description, link, category, tag, instance_id, name))
        self.connection.commit()
        return cursor.lastrowid

    def add_facebook_user(self, name, description, instance_id, facebook_name):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO facebook_users (name, description, instance_id, facebook_name)
                          VALUES (?, ?, ?, ?)''',
                       (name, description, instance_id, facebook_name))
        self.connection.commit()
        return cursor.lastrowid

    def add_alert(self, message, alert_type, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO alerts (message, type, user_id, alert_type)
                          VALUES (?, ?, ?, ?)''',
                       (message, alert_type, user_id, alert_type))
        self.connection.commit()
        return cursor.lastrowid

    def add_audit_log(self, action, table_name, record_id, user_id, performed_by):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO audit_log (action, table_name, record_id, user_id, performed_by)
                          VALUES (?, ?, ?, ?, ?)''',
                       (action, table_name, record_id, user_id, performed_by))
        self.connection.commit()
        return cursor.lastrowid

    def add_quota(self, quota_type, quota_limit, instance_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO quotas (type, quota_limit, instance_id)
                          VALUES (?, ?, ?)''',
                       (quota_type, quota_limit, instance_id))
        self.connection.commit()
        return cursor.lastrowid

    def add_backup_log(self, instance_id, status, backup_file):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO backup_logs (instance_id, status, backup_file)
                          VALUES (?, ?, ?)''',
                       (instance_id, status, backup_file))
        self.connection.commit()
        return cursor.lastrowid

    def add_user_role(self, role_name, description):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO user_roles (role_name, description)
                          VALUES (?, ?)''',
                       (role_name, description))
        self.connection.commit()
        return cursor.lastrowid

    def add_email_session(self, email_text, subject, status, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO email_sessions (email_text, subject, status, user_id)
                          VALUES (?, ?, ?, ?)''',
                       (email_text, subject, status, user_id))
        self.connection.commit()
        return cursor.lastrowid

    def add_user_session(self, user_id, auth_token, expires_at, session_token):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO user_sessions (user_id, auth_token, expires_at, session_token)
                          VALUES (?, ?, ?, ?)''',
                       (user_id, auth_token, expires_at, session_token))
        self.connection.commit()
        return cursor.lastrowid

    def add_contact(self, first_name, last_name, phone_number, email, category, tag, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO contacts (first_name, last_name, phone_number, email, category, tag, user_id)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (first_name, last_name, phone_number, email, category, tag, user_id))
        self.connection.commit()
        return cursor.lastrowid

    def add_instance_user(self, instance_id, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO instance_user (instance_id, user_id)
                          VALUES (?, ?)''',
                       (instance_id, user_id))
        self.connection.commit()
        return cursor.lastrowid

    def add_group_user(self, group_id, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO group_user (group_id, user_id)
                          VALUES (?, ?)''',
                       (group_id, user_id))
        self.connection.commit()
        return cursor.lastrowid

    def generate_fake_data(self):
        # Add users
        for i in range(10):
            self.add_user(f'User {i}', f'user{i}@example.com', 'password', 1)

        # Add instances
        for i in range(5):
            self.add_instance(f'Instance {i}', 'active', 'type1', random.randint(1, 10))

        # Add licenses
        for i in range(5):
            self.add_license(f'License {i}', 'Description for license', 30, 'active', random.randint(1, 5), 'type1', 'type')

        # Add media
        for i in range(5):
            self.add_media(f'/path/to/media/file{i}.jpg', f'tag{i}', f'Label {i}', random.randint(1, 5), f'Media {i}')

        # Add groups
        for i in range(5):
            self.add_group(f'Group {i}', 'Description for group', f'http://group{i}.com', 'Category', f'tag{i}', random.randint(1, 5), f'Group Name {i}')

        # Add Facebook users
        for i in range(5):
            self.add_facebook_user(f'FB User {i}', 'FB User description', random.randint(1, 5), f'fb_user_{i}')

        # Add alerts
        for i in range(5):
            self.add_alert(f'Alert message {i}', 'info', random.randint(1, 10))

        # Add audit logs
        for i in range(5):
            self.add_audit_log('insert', 'users', random.randint(1, 10), random.randint(1, 10), f'User {random.randint(1, 10)}')

        # Add quotas
        for i in range(5):
            self.add_quota('type1', random.randint(100, 500), random.randint(1, 5))

        # Add backup logs
        for i in range(5):
            self.add_backup_log(random.randint(1, 5), 'completed', f'backup_file_{i}.zip')

        # Add user roles
        for i in range(5):
            self.add_user_role(f'Role {i}', f'Description for Role {i}')

        # Add email sessions
        for i in range(5):
            self.add_email_session(f'Email body {i}', f'Subject {i}', 'sent', random.randint(1, 10))

        # Add user sessions
        for i in range(5):
            self.add_user_session(random.randint(1, 10), f'token_{i}', datetime.now(), f'session_{i}')

        # Add contacts
        for i in range(5):
            self.add_contact(f'First {i}', f'Last {i}', f'123-456-789{i}', f'contact{i}@example.com', 'friend', f'tag{i}', random.randint(1, 10))

        # Add instance-user associations
        for i in range(5):
            self.add_instance_user(random.randint(1, 5), random.randint(1, 10))

        # Add group-user associations
        for i in range(5):
            self.add_group_user(random.randint(1, 5), random.randint(1, 10))
 # Ajouter un utilisateur
    def add_user3(self, name, email, password, role_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users (name, email, password, role_id) VALUES (?, ?, ?, ?)''',
                       (name, email, password, role_id))
        self.connection.commit()
        return cursor.lastrowid

    # Ajouter une instance
    def add_instance2(self, name, status, instance_type, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO instances (name, status, type, user_id) VALUES (?, ?, ?, ?)''',
                       (name, status, instance_type, user_id))
        self.connection.commit()
        return cursor.lastrowid

    # Ajouter une licence
    def add_license1(self, label, description, duration, status, instance_id, license_type, license_type_description):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO licences (label, description, duration, status, instance_id, license_type, type)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (label, description, duration, status, instance_id, license_type, license_type_description))
        self.connection.commit()
        return cursor.lastrowid

    # Jointure Exemple 1: Lister tous les utilisateurs et leurs instances
    def get_users_and_instances(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT users.name, users.email, instances.name AS instance_name, instances.status
            FROM users
            JOIN instances ON users.id = instances.user_id
        ''')
        return cursor.fetchall()

    # Jointure Exemple 2: Obtenir les licences par instance et les informations sur les utilisateurs
    def get_instance_licenses_with_users(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT instances.name AS instance_name, licences.label, licences.status, users.name AS user_name
            FROM licences
            JOIN instances ON licences.instance_id = instances.id
            JOIN users ON instances.user_id = users.id
        ''')
        return cursor.fetchall()
if __name__ == '__main__':
    db = FbRobotDatabase()
    db.generate_fake_data()
    db.close()
