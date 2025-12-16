from models import Item, Recipe, RecipeItem, Message
from database.database import engine, Base
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
def on_startup():
    """Evento de inicialização do aplicativo FastAPI."""
    try:
        print("Criando tabelas no banco de dados...")
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso no banco de dados.")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")