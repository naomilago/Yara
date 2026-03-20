from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

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


def build_graph(model_name: str = 'llama-3.1-8b-instant', session_id: str = 'default'):
  '''Constrói e retorna o grafo LangGraph compilado com todas as ferramentas da Yara.
  Args:
      model_name: Nome do modelo Groq a utilizar.
      session_id: ID da sessão para persistência de memória.
  '''
  llm = ChatGroq(model=model_name, temperature=0.0)

  checkpointer = MemorySaver()

  graph = create_react_agent(
    model=llm,
    tools=ALL_TOOLS,
    prompt=YARA_SYSTEM_PROMPT,
    checkpointer=checkpointer,
  )

  return graph
