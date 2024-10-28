# settings.py
from pydantic import BaseSettings
from translation import TranslatorManager  # Importer le gestionnaire de traductions

class Settings(BaseSettings):
    database_url: str
    app_name: str = "My Application"
    debug: bool = False

settings = Settings()
