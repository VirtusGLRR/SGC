from langchain.tools import tool
from sqlalchemy import inspect, text
from database.database import engine, SessionLocal
import json

@tool
def sql_db_schema(tables: str) -> str:
    """Use para obter o esquema (colunas e tipos) das tabelas. A entrada deve ser o nome da(s) tabela(s) separadas por vírgula. Ex: 'Item, Recipe' ou 'Recipe_Item'

    Args:
        tables: Nome das tabelas separadas por vírgula. Ex: "Item, Recipe"

    Returns:
        String com informações do esquema das tabelas
    """
    try:
        inspector = inspect(engine)
        table_list = [t.strip() for t in tables.split(',')]
        schema_info = []

        for table_name in table_list:
            columns = inspector.get_columns(table_name)
            table_schema = f"\nTabela: {table_name}\n"
            table_schema += "-" * 50 + "\n"

            for col in columns:
                col_name = col['name']
                col_type = str(col['type'])
                nullable = "NULL" if col['nullable'] else "NOT NULL"
                default = f", default={col['default']}" if col.get('default') else ""
                primary_key = "PRIMARY KEY" if col.get('primary_key', False) else ""
                table_schema += f"  • {col_name}: {col_type} {nullable}{default}{primary_key}\n"

            foreign_keys = inspector.get_foreign_keys(table_name)
            if foreign_keys:
                table_schema += "\nForeign Keys:\n"
                for fk in foreign_keys:
                    constrained_cols = ', '.join(fk['constrained_columns'])
                    referred_table = fk['referred_table']
                    referred_cols = ', '.join(fk['referred_columns'])
                    table_schema += f"    • {constrained_cols} → {referred_table}({referred_cols})\n"

            schema_info.append(table_schema)

        return "\n".join(schema_info)

    except Exception as e:
        return f"❌ Erro ao obter esquema: {str(e)}"


@tool
def sql_db_query(query: str) -> str:
    """Use esta ferramenta para executar um comando SQL de LEITURA (SELECT) contra o banco de dados. A entrada deve ser um comando SQL completo. Ex: 'SELECT COUNT(*) FROM Item' ou 'SELECT * FROM Recipe WHERE id = 1'

    Args:
        query: Comando SQL SELECT completo

    Returns:
        Resultado da query em formato JSON ou mensagem de erro
    """
    try:
        query_upper = query.strip().upper()
        if not query_upper.startswith("SELECT"):
            return "Erro: Esta ferramenta aceita apenas comandos SELECT. Use 'sql_db_write' para comandos de escrita."
        db = SessionLocal()
        try:
            result = db.execute(text(query))

            rows = []
            if result.returns_rows:
                columns = result.keys()
                for row in result:
                    rows.append(dict(zip(columns, row)))

            db.commit()

            if not rows:
                return "Query executada com sucesso. Nenhum resultado encontrado."

            return json.dumps(rows, indent=2, ensure_ascii=False, default=str)

        finally:
            db.close()

    except Exception as e:
        return f"Erro ao executar SQL (SELECT): {str(e)}"


@tool
def sql_db_write(query: str) -> str:
    """Use esta ferramenta para executar comandos SQL de ESCRITA (INSERT, UPDATE, DELETE). A entrada deve ser um comando SQL completo. USE APENAS PARA SALVAR/MODIFICAR DADOS. Ex: 'INSERT INTO Item (name, measure_unity, amount) VALUES (\"Farinha\", \"kg\", 2)'

    Args:
        query: Comando SQL de escrita completo

    Returns:
        Mensagem de sucesso ou erro
    """
    try:
        query_upper = query.strip().upper()
        allowed_commands = ['INSERT', 'UPDATE', 'DELETE']

        if not any(query_upper.startswith(cmd) for cmd in allowed_commands):
            return f"Erro: Esta ferramenta aceita apenas {', '.join(allowed_commands)}. Use 'sql_db_query' para SELECT."

        db = SessionLocal()
        try:
            result = db.execute(text(query))
            db.commit()

            rows_affected = result.rowcount if hasattr(result, 'rowcount') else 0

            return f"Comando de escrita SQL executado com sucesso. Linhas afetadas: {rows_affected}"

        except Exception as e:
            db.rollback()
            raise e

        finally:
            db.close()

    except Exception as e:
        return f"Erro ao executar SQL (WRITE): {str(e)}"



