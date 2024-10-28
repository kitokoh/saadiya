from models.base_model import BaseModel

class InstanceModel(BaseModel):
    def __init__(self, db_name='nova360.db'):
        super().__init__(db_name)

    def create_instance(self, name, path, status, description, facebook_user_id, licence_id):
        """Créer une nouvelle instance."""
        query = '''
            INSERT INTO instances (name, path, status, description, facebook_user_id, licence_id) 
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        params = (name, path, status, description, facebook_user_id, licence_id)
        self.execute_query(query, params)

    def get_all_instances(self):
        """Récupérer toutes les instances."""
        query = "SELECT * FROM instances"
        return self.fetch_all(query)

    def get_instance_by_id(self, instance_id):
        """Récupérer une instance par son ID."""
        query = "SELECT * FROM instances WHERE id = ?"
        return self.fetch_one(query, (instance_id,))

    def update_instance(self, instance_id, **kwargs):
        """Mettre à jour une instance existante."""
        set_clause = ', '.join([f"{key} = ?" for key in kwargs])
        params = list(kwargs.values()) + [instance_id]
        query = f"UPDATE instances SET {set_clause} WHERE id = ?"
        self.execute_query(query, params)

    def delete_instance(self, instance_id):
        """Supprimer une instance par son ID."""
        query = "DELETE FROM instances WHERE id = ?"
        self.execute_query(query, (instance_id,))
