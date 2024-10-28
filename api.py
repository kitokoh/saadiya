# api.py
from fastapi import FastAPI
import uvicorn
from translation import TranslatorManager  # Importer le gestionnaire de traductions

app = FastAPI()

@app.get("/users/")
async def read_users():
    return [{"name": "Alice"}, {"name": "Bob"}, {"name": "Charlie"}]

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
