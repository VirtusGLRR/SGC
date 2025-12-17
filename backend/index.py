from models import Item, Recipe, RecipeItem, Bot
from database.database import engine, Base
from routes import bot_routes, recipe_routes, item_routes
from fastapi import FastAPI

app = FastAPI(
    title="Minha API",
    version="1.0.0"
)

app.include_router(item_routes, tags=["Item"])
app.include_router(recipe_routes, tags=["Recipe"])
app.include_router(bot_routes, tags=["Bot"])

@app.on_event("startup")
def on_startup():
    """Evento de inicialização do aplicativo FastAPI."""
    try:
        print("Criando tabelas no banco de dados...")
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso no banco de dados.")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "index:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
