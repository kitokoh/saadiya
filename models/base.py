# import sqlite3
# import os
# from datetime import datetime

# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# class BaseDatabase:
#     def __init__(self, db_name='nova360.db'):
#         project_root = os.path.dirname(os.path.abspath(__file__))
#         db_path = os.path.join(project_root, '../../resources/data', db_name)
#         os.makedirs(os.path.dirname(db_path), exist_ok=True)
#         self.connection = sqlite3.connect(db_path)
#         self.create_tables()

#     def create_tables(self):
#         cursor = self.connection.cursor()
#         # Code to create tables (omitted for brevity)
#         self.connection.commit()

#     def close(self):
#         self.connection.close()


# DATABASE_URL = "sqlite:///./test.db"  # deux fois le meme coe Changez cela pour votre base de données

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # Créer les tables
# def init_db():
#     Base.metadata.create_all(bind=engine)
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
