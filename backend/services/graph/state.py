from typing import TypedDict
from typing_extensions import Annotated
from langchain_core.messages import AnyMessage
import operator

class AgentState(TypedDict):
    user_input: str
    next_agent: str
    orchestrator_explanation: str
    sql_response: str
    final_answer: str
    messages: Annotated[list[AnyMessage], operator.add]