from models.base_model import BaseModel

class FacebookUserModel(BaseModel):
    def __init__(self):
        super().__init__()

    # Create
    def add_facebook_user(self, facebook_name, facebook_id, instance_id):
        query = '''
            INSERT INTO facebook_users (facebook_name, facebook_id, instance_id) 
            VALUES (?, ?, ?)
        '''
        self.execute_query(query, (facebook_name, facebook_id, instance_id))

    # Read
    def get_facebook_users_by_instance(self, instance_id):
        query = 'SELECT * FROM facebook_users WHERE instance_id = ?'
        return self.fetch_all(query, (instance_id,))
