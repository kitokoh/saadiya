from models.base_model import BaseModel

class GroupModel(BaseModel):
    def __init__(self):
        super().__init__()

    # Create
    def add_group(self, name, description, instance_id):
        query = '''
            INSERT INTO groups (name, description, instance_id) 
            VALUES (?, ?, ?)
        '''
        self.execute_query(query, (name, description, instance_id))

    # Read
    def get_groups_by_instance(self, instance_id):
        query = 'SELECT * FROM groups WHERE instance_id = ?'
        return self.fetch_all(query, (instance_id,))

    # Delete
    def delete_group(self, group_id):
        query = 'DELETE FROM groups WHERE id = ?'
        self.execute_query(query, (group_id,))
