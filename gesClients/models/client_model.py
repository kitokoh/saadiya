from PyQt5.QtCore import QObject, pyqtSignal
from datetime import datetime

class Client(QObject):
    def __init__(self, id=None, company_name="", contact_name="", phone="", email="", address="", notes=""):
        super().__init__()
        self.id = id
        self.company_name = company_name
        self.contact_name = contact_name
        self.phone = phone
        self.email = email
        self.address = address
        self.notes = notes
        self.last_contact_date = None
        self.next_contact_date = None
        self.projects = []
    
    def to_dict(self):
        return {
            "id": self.id,
            "company_name": self.company_name,
            "contact_name": self.contact_name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "notes": self.notes,
            "last_contact_date": self.last_contact_date.strftime("%Y-%m-%d") if self.last_contact_date else None,
            "next_contact_date": self.next_contact_date.strftime("%Y-%m-%d") if self.next_contact_date else None
        }
    
    def update_contact_date(self, contact_date=None):
        if contact_date is None:
            contact_date = datetime.now()
        self.last_contact_date = contact_date
        # Par défaut, on propose 2 semaines plus tard pour le prochain contact
        self.next_contact_date = contact_date + timedelta(days=14)
    
    def add_project(self, project):
        self.projects.append(project)
    
    def get_projects(self):
        return self.projects