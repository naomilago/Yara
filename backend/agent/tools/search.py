from duckduckgo_search import DDGS
from langchain_core.tools import tool

@tool
def pesquisar_web(query: str) -> str:
  """Ferramenta poderosa de busca na internet para encontrar informações atualizadas em tempo real.
  Use esta ferramenta SEMPRE que precisar de dados específicos como:
  - Leis e direitos LGBTQIA+
  - Endereços e contatos de ambulatórios trans, CAPS ou ONGs
  - Orientações de processos hormonais ou pós-cirúrgicos
  - Notícias, eventos locais e vagas de emprego
  
  Args:
      query: O termo de busca detalhado (Ex: "ambulatórios trans SUS estado SP endereços").
  """
  try:
    with DDGS() as ddgs:
      results = list(ddgs.text(query, max_results=5))
    
    if not results:
      return "Nenhum resultado encontrado na web. Tente reformular a sua busca."
      
    info = ""
    for r in results:
      info += f"• Título: {r.get('title', '')}\n  Conteúdo: {r.get('body', '')}\n\n"
      
    return f"Resultados mais relevantes da Web:\n{info}"
  except Exception as e:
    return f"Erro ao acessar a internet: {str(e)}. Baseie-se no seu conhecimento interno."
