from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, RemoveMessage

from agent.prompts import YARA_SYSTEM_PROMPT
from agent.tools.crisis_support import (
  recursos_crise,
  contato_cvv,
  contato_antra,
  localizar_caps,
)
from agent.tools.wellbeing import (
  meditacao_guiada,
  diario_transicao,
  rastreador_humor,
  afirmacao_positiva,
)
from agent.tools.search import pesquisar_web

ALL_TOOLS = [
  # Apoio em crise (MANTIDOS E ESTÁVEIS)
  recursos_crise,
  contato_cvv,
  contato_antra,
  localizar_caps,
  # Bem-estar
  meditacao_guiada,
  diario_transicao,
  rastreador_humor,
  afirmacao_positiva,
  # Buscador Dinâmico (SUBSTITUIU 15 FERRAMENTAS ESTÁTICAS)
  pesquisar_web,
]


# Checkpointer global para manter a memória enquanto o processo estiver vivo
# Nota: Em Cloud Run (serverless), isso será resetado se o container escalar para zero.
_checkpointer = MemorySaver()


def build_graph(model_name: str = 'llama-3.1-8b-instant', session_id: str = 'default'):
  '''Constrói e retorna o grafo LangGraph compilado com todas as ferramentas da Yara.
  Args:
      model_name: Nome do modelo Groq a utilizar.
      session_id: ID da sessão para persistência de memória.
  '''
  llm = ChatGroq(model=model_name, temperature=0.0)

  def state_modifier(state):
    '''Prepara as mensagens para o LLM: adiciona o prompt do sistema e mantém apenas as últimas 10 mensagens.'''
    system_msg = SystemMessage(content=YARA_SYSTEM_PROMPT)
    messages = state.get('messages', [])
    # Mantém apenas as últimas 10 mensagens de histórico
    trimmed_messages = messages[-10:] if len(messages) > 10 else messages
    return [system_msg] + trimmed_messages

  graph = create_react_agent(
    model=llm,
    tools=ALL_TOOLS,
    state_modifier=state_modifier,
    checkpointer=_checkpointer,
  )

  return graph
