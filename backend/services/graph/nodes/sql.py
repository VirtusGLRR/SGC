from langchain_core.messages import HumanMessage, AIMessage
from ..agents import sql_agent
from ..state import AgentState

def sql_node(state : AgentState):
    response = sql_agent.invoke({
        "messages": [
            HumanMessage(content=state['user_input'])
        ]}
    )
    return {
        'sql_response': response['messages'][-1].content
    }