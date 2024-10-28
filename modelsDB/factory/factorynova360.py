import factory
from factory import Faker, SubFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from your_model_file import Base, User, Instance, License, Media, Group, FacebookUser, Alert, AuditLog, Quota, BackupLog, UserRole, EmailSession, UserSession, Contact

# Configure your database connection here
DATABASE_URL = "sqlite:///your_database.db"  # Change this to your database URL
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = session

    name = Faker('name')
    email = Faker('email')
    password = Faker('password')
    role_id = factory.LazyAttribute(lambda x: UserRoleFactory().id)  # Assuming you have a UserRoleFactory

class InstanceFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Instance
        sqlalchemy_session = session

    name = Faker('word')
    status = Faker('random_element', elements=["premium", "demo"])
    type = Faker('random_element', elements=["Facebook", "TikTok", "Instagram"])
    user_id = factory.LazyAttribute(lambda x: UserFactory().id)
    quota = Faker('random_int', min=1, max=100)

class LicenseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = License
        sqlalchemy_session = session

    label = Faker('word')
    description = Faker('text')
    duration = Faker('random_int', min=1, max=12)
    status = Faker('random_element', elements=["active", "expired"])
    instance_id = factory.LazyAttribute(lambda x: InstanceFactory().id)
    license_type = Faker('word')

class MediaFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Media
        sqlalchemy_session = session

    file_path = Faker('file_path')
    tag = Faker('word')
    label = Faker('word')
    description = Faker('text')

class GroupFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Group
        sqlalchemy_session = session

    label = Faker('word')
    description = Faker('text')
    link = Faker('url')
    category = Faker('word')
    tag = Faker('word')
    instance_id = factory.LazyAttribute(lambda x: InstanceFactory().id)

class FacebookUserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = FacebookUser
        sqlalchemy_session = session

    name = Faker('name')
    description = Faker('text')
    instance_id = factory.LazyAttribute(lambda x: InstanceFactory().id)

class AlertFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Alert
        sqlalchemy_session = session

    message = Faker('sentence')
    type = Faker('random_element', elements=["error", "info", "warning"])
    user_id = factory.LazyAttribute(lambda x: UserFactory().id)

class AuditLogFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = AuditLog
        sqlalchemy_session = session

    action = Faker('word')
    table_name = Faker('word')
    record_id = Faker('random_int', min=1, max=100)
    user_id = factory.LazyAttribute(lambda x: UserFactory().id)

class QuotaFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Quota
        sqlalchemy_session = session

    type = Faker('word')
    limit = Faker('random_int', min=1, max=100)
    current_usage = Faker('random_int', min=0, max=100)
    instance_id = factory.LazyAttribute(lambda x: InstanceFactory().id)

class BackupLogFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = BackupLog
        sqlalchemy_session = session

    instance_id = factory.LazyAttribute(lambda x: InstanceFactory().id)
    status = Faker('random_element', elements=["successful", "failed"])

class UserRoleFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserRole
        sqlalchemy_session = session

    role_name = Faker('word')
    description = Faker('text')

class EmailSessionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = EmailSession
        sqlalchemy_session = session

    email_text = Faker('text')
    subject = Faker('sentence')
    status = Faker('random_element', elements=["sent", "failed"])

class UserSessionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserSession
        sqlalchemy_session = session

    user_id = factory.LazyAttribute(lambda x: UserFactory().id)
    auth_token = Faker('md5')

class ContactFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Contact
        sqlalchemy_session = session

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    phone_number = Faker('phone_number')
    email = Faker('email')
    category = Faker('word')
    user_id = factory.LazyAttribute(lambda x: UserFactory().id)

# Example of creating instances
if __name__ == "__main__":
    Base.metadata.create_all(engine)  # Create tables if not exists
    user = UserFactory()
    instance = InstanceFactory(user_id=user.id)  # Pass user_id to InstanceFactory
    license = LicenseFactory(instance_id=instance.id)
    media = MediaFactory()
    group = GroupFactory(instance_id=instance.id)
    facebook_user = FacebookUserFactory(instance_id=instance.id)
    alert = AlertFactory(user_id=user.id)
    audit_log = AuditLogFactory(user_id=user.id)
    quota = QuotaFactory(instance_id=instance.id)
    backup_log = BackupLogFactory(instance_id=instance.id)
    role = UserRoleFactory()
    email_session = EmailSessionFactory()
    user_session = UserSessionFactory(user_id=user.id)
    contact = ContactFactory(user_id=user.id)

    session.commit()  # Save to the database
