import random
from faker import Faker
from database.databasefbrobot import FbRobotDatabase

fake = Faker()

class FbRobotFactory:
    def __init__(self, db):
        self.db = db

    def create_random_instance(self):
        cursor = self.db.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO instances (name, path, status, description, config, facebook_user_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                fake.company(),
                fake.file_path(),
                random.choice(['premium', 'demo', 'dev']),
                fake.text(max_nb_chars=200),
                fake.json(),
                random.randint(1, 10)  # Exemple d'ID d'utilisateur Facebook
            ))
            self.db.connection.commit()  # Valider la transaction
        except Exception as e:
            print(f"Error creating instance: {e}")
        finally:
            cursor.close()

    def create_random_licence(self):
        cursor = self.db.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO licences (type, expiry_date, status, auto_renewal, instance_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                random.choice(['annuelle', 'mensuelle', 'demo']),
                fake.date_time_this_year(),
                random.choice(['actif', 'inactif']),
                random.choice([0, 1]),
                random.randint(1, 10)  # Exemple d'ID d'instance
            ))
            self.db.connection.commit()
        except Exception as e:
            print(f"Error creating licence: {e}")
        finally:
            cursor.close()

    def create_random_media(self):
        cursor = self.db.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO media (name, file_path, type, instance_id)
                VALUES (?, ?, ?, ?)
            ''', (
                fake.file_name(),
                fake.file_path(),
                random.choice(['image', 'vidéo']),
                random.randint(1, 10)  # Exemple d'ID d'instance
            ))
            self.db.connection.commit()
        except Exception as e:
            print(f"Error creating media: {e}")
        finally:
            cursor.close()

    def create_random_group(self):
        cursor = self.db.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO groups (name, description, instance_id)
                VALUES (?, ?, ?)
            ''', (
                fake.company(),
                fake.text(max_nb_chars=200),
                random.randint(1, 10)  # Exemple d'ID d'instance
            ))
            self.db.connection.commit()
        except Exception as e:
            print(f"Error creating group: {e}")
        finally:
            cursor.close()

    def create_random_facebook_user(self):
        cursor = self.db.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO facebook_users (facebook_name, facebook_id, instance_id)
                VALUES (?, ?, ?)
            ''', (
                fake.name(),
                fake.uuid4(),  # ID aléatoire pour simuler un ID Facebook
                random.randint(1, 10)  # Exemple d'ID d'instance
            ))
            self.db.connection.commit()
        except Exception as e:
            print(f"Error creating Facebook user: {e}")
        finally:
            cursor.close()

    def create_random_alert(self):
        cursor = self.db.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO alerts (user_id, message, alert_type)
                VALUES (?, ?, ?)
            ''', (
                random.randint(1, 10),  # Exemple d'ID d'utilisateur
                fake.sentence(),
                random.choice(['info', 'warning', 'error'])
            ))
            self.db.connection.commit()
        except Exception as e:
            print(f"Error creating alert: {e}")
        finally:
            cursor.close()

    def create_random_audit_log(self):
        cursor = self.db.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO audit_log (action, performed_by, details)
                VALUES (?, ?, ?)
            ''', (
                random.choice(['create', 'update', 'delete']),
                random.randint(1, 10),  # Exemple d'ID d'utilisateur
                fake.text(max_nb_chars=200)
            ))
            self.db.connection.commit()
        except Exception as e:
            print(f"Error creating audit log: {e}")
        finally:
            cursor.close()

    def create_random_quota(self):
        cursor = self.db.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO quotas (instance_id, media_quota, group_quota)
                VALUES (?, ?, ?)
            ''', (
                random.randint(1, 10),  # Exemple d'ID d'instance
                random.randint(50, 150),  # Quota de médias
                random.randint(10, 30)  # Quota de groupes
            ))
            self.db.connection.commit()
        except Exception as e:
            print(f"Error creating quota: {e}")
        finally:
            cursor.close()

    def create_random_backup_log(self):
        cursor = self.db.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO backup_logs (instance_id, backup_file)
                VALUES (?, ?)
            ''', (
                random.randint(1, 10),  # Exemple d'ID d'instance
                fake.file_name()
            ))
            self.db.connection.commit()
        except Exception as e:
            print(f"Error creating backup log: {e}")
        finally:
            cursor.close()

    def create_random_user_role(self):
        cursor = self.db.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO user_roles (user_id, role)
                VALUES (?, ?)
            ''', (
                random.randint(1, 10),  # Exemple d'ID d'utilisateur
                random.choice(['admin', 'user', 'viewer'])
            ))
            self.db.connection.commit()
        except Exception as e:
            print(f"Error creating user role: {e}")
        finally:
            cursor.close()

    def create_random_email_session(self):
        cursor = self.db.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO email_sessions (user_id, email, subject, content, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                random.randint(1, 10),  # Exemple d'ID d'utilisateur
                fake.email(),
                fake.sentence(),
                fake.text(max_nb_chars=500),
                random.choice(['envoyé', 'échoué'])
            ))
            self.db.connection.commit()
        except Exception as e:
            print(f"Error creating email session: {e}")
        finally:
            cursor.close()

    def create_random_user_session(self):
        cursor = self.db.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO user_sessions (user_id, session_token, expires_at)
                VALUES (?, ?, ?)
            ''', (
                random.randint(1, 10),  # Exemple d'ID d'utilisateur
                fake.uuid4(),  # Token de session aléatoire
                fake.date_time_this_year()
            ))
            self.db.connection.commit()
        except Exception as e:
            print(f"Error creating user session: {e}")
        finally:
            cursor.close()


if __name__ == "__main__":
    db = FbRobotDatabase()
    factory = FbRobotFactory(db)

    # Générer 10 instances
    for _ in range(10):
        factory.create_random_instance()
        factory.create_random_licence()
        factory.create_random_media()
        factory.create_random_group()
        factory.create_random_facebook_user()
        factory.create_random_alert()
        factory.create_random_audit_log()
        factory.create_random_quota()
        factory.create_random_backup_log()
        factory.create_random_user_role()
        factory.create_random_email_session()
        factory.create_random_user_session()

    db.close()
