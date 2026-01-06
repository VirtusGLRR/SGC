from langchain_core.messages import HumanMessage, AIMessage
from ..agents import structurer_item_agent
from ..state import AgentState

def structurer_item_node(state : AgentState):
    # Pegar apenas a última mensagem do usuário
    history = state['messages']
    user_messages = [msg for msg in history if isinstance(msg, HumanMessage)]

    if not user_messages:
        current_request = state.get('user_input', 'Nenhuma solicitação encontrada.')
    else:
        current_request = user_messages[-1].content

    response = structurer_item_agent.invoke({
        "messages": [
            HumanMessage(content=f'Solicitação atual do usuário:\n\n{current_request}\n\nExtraia e estruture APENAS os itens mencionados NESTA solicitação específica. Ignore qualquer item mencionado anteriormente.')
        ]
    })

    structured_response = response['structured_response']

    # structured_response é um objeto Pydantic ItemStructuredOutputList
    # Acessar o atributo 'items' diretamente, não usar .get()
    items = structured_response.items if hasattr(structured_response, 'items') else []

    # Cada item é um ItemStructuredOutput com atributos item_data e transaction_data
    items_data = [item.item_data for item in items]
    transactions_data = [item.transaction_data for item in items]

    return {
        'sql_item_instruction': items_data,
        'sql_transaction_instruction': transactions_data
    }