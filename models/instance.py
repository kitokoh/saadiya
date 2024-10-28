import sqlite3
from your_project.database import FbRobotDatabase

class InstanceModel:
    def __init__(self):
        self.db = FbRobotDatabase()

    def create_instance(self, name, status, instance_type, user_id):
        cursor = self.db.connection.cursor()
        cursor.execute('''INSERT INTO instances (name, status, type, user_id) VALUES (?, ?, ?, ?)''',
                       (name, status, instance_type, user_id))
        self.db.connection.commit()
        return cursor.lastrowid

    def read_instance(self, instance_id):
        cursor = self.db.connection.cursor()
        cursor.execute('''SELECT * FROM instances WHERE id = ?''', (instance_id,))
        instance = cursor.fetchone()
        cursor.close()
        return instance

    def update_instance(self, instance_id, name=None, status=None, instance_type=None, user_id=None):
        cursor = self.db.connection.cursor()
        updates = []
        params = []
        if name:
            updates.append('name = ?')
            params.append(name)
        if status:
            updates.append('status = ?')
            params.append(status)
        if instance_type:
            updates.append('type = ?')
            params.append(instance_type)
        if user_id:
            updates.append('user_id = ?')
            params.append(user_id)
        params.append(instance_id)
        cursor.execute(f'''UPDATE instances SET {', '.join(updates)} WHERE id = ?''', params)
        self.db.connection.commit()
        cursor.close()

    def delete_instance(self, instance_id):
        cursor = self.db.connection.cursor()
        cursor.execute('''DELETE FROM instances WHERE id = ?''', (instance_id,))
        self.db.connection.commit()
        cursor.close()
