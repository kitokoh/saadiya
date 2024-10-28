import sqlite3
from your_project.database import FbRobotDatabase

class LicenseModel:
    def __init__(self):
        self.db = FbRobotDatabase()

    def create_license(self, label, description, duration, status, instance_id, license_type, license_type_description):
        cursor = self.db.connection.cursor()
        cursor.execute('''INSERT INTO licences (label, description, duration, status, instance_id, license_type, type)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (label, description, duration, status, instance_id, license_type, license_type_description))
        self.db.connection.commit()
        return cursor.lastrowid

    def read_license(self, license_id):
        cursor = self.db.connection.cursor()
        cursor.execute('''SELECT * FROM licences WHERE id = ?''', (license_id,))
        license_record = cursor.fetchone()
        cursor.close()
        return license_record

    def update_license(self, license_id, label=None, description=None, duration=None, status=None, instance_id=None, license_type=None):
        cursor = self.db.connection.cursor()
        updates = []
        params = []
        if label:
            updates.append('label = ?')
            params.append(label)
        if description:
            updates.append('description = ?')
            params.append(description)
        if duration:
            updates.append('duration = ?')
            params.append(duration)
        if status:
            updates.append('status = ?')
            params.append(status)
        if instance_id:
            updates.append('instance_id = ?')
            params.append(instance_id)
        if license_type:
            updates.append('license_type = ?')
            params.append(license_type)
        params.append(license_id)
        cursor.execute(f'''UPDATE licences SET {', '.join(updates)} WHERE id = ?''', params)
        self.db.connection.commit()
        cursor.close()

    def delete_license(self, license_id):
        cursor = self.db.connection.cursor()
        cursor.execute('''DELETE FROM licences WHERE id = ?''', (license_id,))
        self.db.connection.commit()
        cursor.close()
