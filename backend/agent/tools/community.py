'''
Ferramentas de Comunidade
Eventos, grupos de apoio e histórias inspiradoras.
'''

from duckduckgo_search import DDGS
from langchain_core.tools import tool


@tool
def buscar_eventos(cidade: str, tipo: str = 'lgbtqia+') -> str:
  """Busca eventos LGBTQIA+ em uma cidade.
  Args:
      cidade: Nome da cidade.
      tipo: Tipo de evento: 'lgbtqia+', 'trans', 'parada', 'cultural'.
  """
  try:
    with DDGS() as ddgs:
      results = list(ddgs.text(
        f'eventos {tipo} LGBT trans {cidade} 2025 2026',
        max_results=5,
      ))
    if results:
      info = '\n'.join([f'• **{r["title"]}**: {r["body"][:200]}' for r in results])
      return f'🎉 **Eventos {tipo.upper()} em {cidade}:**\n\n{info}\n\n💡 Siga perfis LGBTQIA+ locais no Instagram para atualizações.'
  except Exception:
    pass

  return f'''Para encontrar eventos em {cidade}:
• Facebook/Instagram: pesquise "LGBT {cidade}" ou "Trans {cidade}"
• Sympla: sympla.com.br | Eventbrite: eventbrite.com.br

📅 Datas marcantes: Dia da Visibilidade Trans (31/03), Dia contra a Transfobia (17/05), Paradas do Orgulho.'''


@tool
def grupos_apoio(cidade: str = '', online: str = 'false') -> str:
  '''Encontra grupos de apoio para pessoas trans.
  Args:
      cidade: Nome da cidade para presencial (opcional).
      online: Se 'true', foca em grupos online.
  '''
  base_online = '''🌐 **Grupos Online:**
• @antrabrasil (Instagram) — maior rede trans do Brasil
• @ibte_br (Instituto Brasileiro de Transmasculinidades)
• Reddit: r/transbr
• Discord: servidores "Trans Brasil"
• TudoPsi / Psicologia Viva — psicólogos LGBTQIA+ afirmativos'''

  if cidade and str(online).lower() != 'true':
    try:
      with DDGS() as ddgs:
        results = list(ddgs.text(
          f'grupos apoio trans LGBT {cidade} organização coletivo',
          max_results=4,
        ))
      if results:
        info = '\n'.join([f'• {r["title"]}: {r["body"][:200]}' for r in results])
        return f'🤝 **Grupos em {cidade}:**\n\n{info}\n\n---\n{base_online}'
    except Exception:
      pass

  return f'Pesquise "grupo trans {cidade}" no Facebook ou contate a ANTRA (antrabrasil.org).\n\n{base_online}'


@tool
def historias_inspiradoras(tema: str = 'geral') -> str:
  """Compartilha histórias de pessoas trans brasileiras inspiradoras.
  Args:
      tema: 'arte', 'política', 'ativismo' ou 'geral'.
  """
  historias = {
    'arte': '''🎭 **Trans Brasileiras na Arte:**
• **Liniker** — cantora soul/MPB, Grammy Latino 2023 🎵
• **Linn da Quebrada** — performer e compositora, álbum "Pajubá" (2017)
• **Indianara Siqueira** — documentarista e ativista''',

    'política': '''🏛️ **Trans na Política:**
• **Erika Hilton** — deputada federal SP (PSOL), pioneira no maior estado do Brasil
• **Dani Balbi** — deputada estadual SC
• **Linda Brasil** — vereadora em Aracaju (SE)''',

    'ativismo': '''✊ **Ativistas Trans que Mudaram o Brasil:**
• **Keila Simpson** — ex-presidente da ANTRA, décadas de luta pelos direitos trans
• **Indianara Siqueira** — pioneira no ativismo de trabalhadoras sexuais trans
• **Jaqueline Gomes de Jesus** — psicóloga, maior referência em identidade de gênero no Brasil''',

    'geral': '''✨ **Brasileiras Trans que Inspiram:**
🎵 **Liniker** — cantora, Grammy Latino 2023
🏛️ **Erika Hilton** — deputada federal pioneira
🎭 **Linn da Quebrada** — performer revolucionária
📚 **Jaqueline Gomes de Jesus** — referência em identidade de gênero
✊ **Keila Simpson** — ativista histórica da ANTRA

Pessoas trans são líderes, artistas, cientistas, políticas.
Há espaço para você brilhar também. 🌟 Qual área te inspira mais?''',
  }

  return historias.get(tema, historias['geral'])
