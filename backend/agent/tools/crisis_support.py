'''
Ferramentas de Apoio em Crise
Acionadas com prioridade quando há sofrimento intenso.
'''

from duckduckgo_search import DDGS
from langchain_core.tools import tool


@tool
def recursos_crise() -> str:
  '''
  Retorna recursos de apoio em crise para pessoas trans em sofrimento intenso.
  USE IMEDIATAMENTE ao detectar sofrimento intenso, automutilação ou pensamentos suicidas.
  '''
  return '''🆘 RECURSOS DE CRISE — APOIO IMEDIATO

**CVV — Centro de Valorização da Vida**
📞 188 (24 horas, gratuito, inclusive de celular)
💬 Chat: cvv.org.br

**ANTRA — Associação Nacional de Travestis e Transexuais**
🌐 antrabrasil.org | @antrabrasil

**CAPS — Centro de Atenção Psicossocial**
Atendimento gratuito em saúde mental pelo SUS.

**Ligue 180** — Canal da Mulher (violência e encaminhamento)
**SAMU — 192** — Emergências médicas

**Você não está sozinha. Estou aqui com você agora. 💙**'''


@tool
def contato_cvv(cidade: str = '') -> str:
  """Busca informações sobre o CVV e postos de apoio presenciais.
  Args:
      cidade: Nome da cidade para buscar posto CVV presencial (opcional).
  """
  if cidade:
    try:
      with DDGS() as ddgs:
        results = list(ddgs.text(
          f'CVV posto presencial {cidade} endereço horário',
          max_results=3,
        ))
      if results:
        info = '\n'.join([f'• {r["title"]}: {r["body"][:200]}' for r in results])
        return f'📍 CVV em {cidade}:\n{info}\n\n☎️ Lembre: o 188 está disponível 24h de qualquer cidade.'
    except Exception:
      pass
  return '''**CVV — Centro de Valorização da Vida**
☎️ 188 — ligação gratuita, 24 horas por dia
💬 Chat: cvv.org.br
📧 atendimento@cvv.org.br

Qualquer sofrimento é válido para ligar. Você não precisa estar em crise aguda.'''


@tool
def contato_antra() -> str:
  """Retorna informações de contato e serviços da ANTRA."""
  return '''🏳️‍⚧️ **ANTRA — Associação Nacional de Travestis e Transexuais**

🌐 antrabrasil.org
📸 @antrabrasil (Instagram)

**O que a ANTRA oferece:**
• Apoio jurídico para pessoas trans em vulnerabilidade
• Encaminhamento para saúde e assistência social
• Rede de organizações LGBTQIA+ em todo o Brasil
• Relatório anual sobre assassinatos de pessoas trans

Para denúncias urgentes: antrabrasil.org/contato'''


@tool
def localizar_caps(cidade: str) -> str:
  """Localiza CAPS (Centro de Atenção Psicossocial) para atendimento em saúde mental gratuito.
  Args:
      cidade: Nome da cidade onde buscar o CAPS.
  """
  try:
    with DDGS() as ddgs:
      results = list(ddgs.text(
        f'CAPS Centro Atenção Psicossocial {cidade} endereço telefone horário',
        max_results=4,
      ))
    if results:
      info = '\n'.join([f'• {r["title"]}: {r["body"][:250]}' for r in results])
      return f'🏥 **CAPS em {cidade}:**\n\n{info}\n\n💡 Atendimento gratuito pelo SUS, sem encaminhamento em crise.'
  except Exception:
    pass

  return f'''Para encontrar o CAPS em {cidade}:

1. Ligue para **0800 644 4300** (Central Nacional de Regulação)
2. Acesse cnes.datasus.gov.br e filtre por CAPS
3. Vá ao posto de saúde mais próximo e solicite encaminhamento'''
