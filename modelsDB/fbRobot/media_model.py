from models.base_model import BaseModel

class MediaModel(BaseModel):
    def __init__(self, db_name='nova360pro.db'):
        super().__init__(db_name)

    def create_media(self, name, file_path, media_type, instance_id):
        """Créer un nouveau média."""
        query = '''
            INSERT INTO media (name, file_path, type, instance_id) 
            VALUES (?, ?, ?, ?)
        '''
        params = (name, file_path, media_type, instance_id)
        self.execute_query(query, params)

    def get_all_media(self):
        """Récupérer tous les médias."""
        query = "SELECT * FROM media"
        return self.fetch_all(query)

    def get_media_by_id(self, media_id):
        """Récupérer un média par son ID."""
        query = "SELECT * FROM media WHERE id = ?"
        return self.fetch_one(query, (media_id,))

    def update_media(self, media_id, **kwargs):
        """Mettre à jour un média existant."""
        set_clause = ', '.join([f"{key} = ?" for key in kwargs])
        params = list(kwargs.values()) + [media_id]
        query = f"UPDATE media SET {set_clause} WHERE id = ?"
        self.execute_query(query, params)

    def delete_media(self, media_id):
        """Supprimer un média par son ID."""
        query = "DELETE FROM media WHERE id = ?"
        self.execute_query(query, (media_id,))
