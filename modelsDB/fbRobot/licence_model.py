from models.base_model import BaseModel

class LicenceModel(BaseModel):
    def __init__(self, db_name='nova360pro.db'):
        super().__init__(db_name)

    def create_licence(self, licence_type, expiry_date, status, instance_id):
        """Créer une nouvelle licence."""
        query = '''
            INSERT INTO licences (type, expiry_date, status, instance_id) 
            VALUES (?, ?, ?, ?)
        '''
        params = (licence_type, expiry_date, status, instance_id)
        self.execute_query(query, params)

    def get_all_licences(self):
        """Récupérer toutes les licences."""
        query = "SELECT * FROM licences"
        return self.fetch_all(query)

    def get_licence_by_id(self, licence_id):
        """Récupérer une licence par son ID."""
        query = "SELECT * FROM licences WHERE id = ?"
        return self.fetch_one(query, (licence_id,))

    def update_licence(self, licence_id, **kwargs):
        """Mettre à jour une licence existante."""
        set_clause = ', '.join([f"{key} = ?" for key in kwargs])
        params = list(kwargs.values()) + [licence_id]
        query = f"UPDATE licences SET {set_clause} WHERE id = ?"
        self.execute_query(query, params)

    def delete_licence(self, licence_id):
        """Supprimer une licence par son ID."""
        query = "DELETE FROM licences WHERE id = ?"
        self.execute_query(query, (licence_id,))
