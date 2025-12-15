from langchain_core.messages import HumanMessage, AIMessage
from ..agents import structurer_agent
from ..state import AgentState

def structurer_node(state : AgentState):
    history = state['messages']
    print("Histórico da conversa para o structurer agent:", history)
    response = structurer_agent.invoke({
        "messages": [
            HumanMessage(content=f'Histórico: {history}')
        ]
    })

    sql_instruction = f"Por favor, insira estas receitas na tabela 'receitas':\n{response['structured_response']}"

    return {
        'user_input': sql_instruction,
        'messages': [sql_instruction]
    }