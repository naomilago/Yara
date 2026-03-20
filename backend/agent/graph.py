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
from agent.tools.health import (
  buscar_ambulatorio,
  info_hormonizacao,
  preparar_consulta,
  cuidados_pos_cirurgia,
)
from agent.tools.rights import (
  retificar_nome_genero,
  usar_nome_social,
  denunciar_transfobia,
  direitos_trans,
)
from agent.tools.wellbeing import (
  meditacao_guiada,
  diario_transicao,
  rastreador_humor,
  afirmacao_positiva,
)
from agent.tools.community import (
  buscar_eventos,
  grupos_apoio,
  historias_inspiradoras,
)
from agent.tools.practical import (
  transicao_no_trabalho,
  empresas_inclusivas,
  seguranca_digital,
)
from agent.tools.identity import (
  guia_pronomes,
  gerador_nomes,
  musicas_afirmativas,
)

ALL_TOOLS = [
  # Apoio em crise
  recursos_crise,
  contato_cvv,
  contato_antra,
  localizar_caps,
  # Saúde
  buscar_ambulatorio,
  info_hormonizacao,
  preparar_consulta,
  cuidados_pos_cirurgia,
  # Direitos
  retificar_nome_genero,
  usar_nome_social,
  denunciar_transfobia,
  direitos_trans,
  # Bem-estar
  meditacao_guiada,
  diario_transicao,
  rastreador_humor,
  afirmacao_positiva,
  # Comunidade
  buscar_eventos,
  grupos_apoio,
  historias_inspiradoras,
  # Vida prática
  transicao_no_trabalho,
  empresas_inclusivas,
  seguranca_digital,
  # Identidade
  guia_pronomes,
  gerador_nomes,
  musicas_afirmativas,
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
