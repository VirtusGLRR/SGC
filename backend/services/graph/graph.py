from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, END
from .state import AgentState
from pathlib import Path
from .nodes import (
    orchestrator_node,
    structurer_node,
    trivial_node,
    sql_node,
    revisor_node,
    web_node
)
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent.parent
db_path = BASE_DIR / "database" / "checkpoints.db"
conn = sqlite3.connect(str(db_path), check_same_thread=False)
memory = SqliteSaver(conn)

builder = StateGraph(AgentState)

builder.add_node("orchestrator", orchestrator_node)
builder.add_node("structurer", structurer_node)
builder.add_node("trivial", trivial_node)
builder.add_node("sql", sql_node)
builder.add_node("revisor", revisor_node)
builder.add_node("web", web_node)
builder.set_entry_point("orchestrator")

builder.add_conditional_edges(
    "orchestrator",
    lambda state: state['next_agent'],
    {
        "TRIVIAL": "trivial",
        "SQL": "sql",
        "WEB": "web",
        "SAVE_RECIPE": "structurer"
    }
)

builder.add_edge("structurer", "sql")
builder.add_edge("sql", "revisor")

builder.add_conditional_edges(
    "revisor",
    lambda state: state['next_agent'],
    {
        "FINALIZAR": END,
        "WEB": "web"
    }
)

builder.add_edge("web", END)
builder.add_edge("trivial", END)

graph = builder.compile(checkpointer=memory)

assets_dir = BASE_DIR / "assets"

image_path = assets_dir / "graph.png"
image_data = graph.get_graph().draw_mermaid_png()

with open(image_path, "wb") as f:
    f.write(image_data)


