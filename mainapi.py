from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models.base import SessionLocal, engine
from models.user import User  # Importez le modèle User
from models.user import create_user, read_user, update_user, delete_user  # Importez vos fonctions CRUD
from models.base import init_db
from translation import TranslatorManager  # Importer le gestionnaire de traductions

init_db()  # Crée les tables

# Créez l'instance de FastAPI
app = FastAPI()

# Dépendance pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=User)  # Remplacez User par votre modèle
def create_new_user(username: str, db: Session = Depends(get_db)):
    return create_user(db, username)

@app.get("/users/{user_id}", response_model=User)  # Remplacez User par votre modèle
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = read_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=User)  # Remplacez User par votre modèle
def update_existing_user(user_id: int, username: str, db: Session = Depends(get_db)):
    db_user = update_user(db, user_id, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", response_model=User)  # Remplacez User par votre modèle
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
