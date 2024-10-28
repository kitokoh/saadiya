# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import user_controller, role_controller, admin_controller, contact_controller, message_controller
from translation import TranslatorManager  # Importer le gestionnaire de traductions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_controller.router, prefix="/users")
app.include_router(role_controller.router, prefix="/roles")
app.include_router(admin_controller.router, prefix="/admins")
app.include_router(contact_controller.router, prefix="/contacts")
app.include_router(message_controller.router, prefix="/messages")

@app.get("/")
def read_root():
    return {"Hello": "World"}
