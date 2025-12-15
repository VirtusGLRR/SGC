import sys
from pathlib import Path

# Adicionar o backend ao path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from database.database import engine, Base
from models import Recipe, Item, RecipeItem

print("Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")

# Verificar tabelas criadas
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"\nTabelas no banco de dados: {tables}")

for table in tables:
    columns = inspector.get_columns(table)
    print(f"\nTabela: {table}")
    for column in columns:
        print(f"  - {column['name']} ({column['type']})")

