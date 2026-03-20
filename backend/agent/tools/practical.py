'''
Ferramentas de Vida Prática
Transição no trabalho, empresas inclusivas, segurança digital.
'''

from duckduckgo_search import DDGS
from langchain_core.tools import tool


@tool
def transicao_no_trabalho(situacao: str = 'geral') -> str:
  """Orienta sobre como navegar a transição de gênero no ambiente de trabalho.
  Args:
      situacao: 'comunicar', 'nome_social', 'banheiro', 'discriminação' ou 'geral'.
  """
  guias = {
    'comunicar': '''💼 **Como comunicar sua transição no trabalho:**

Não há obrigação legal de comunicar antes de ter documentos alterados.
O momento ideal é quando você se sentir segura e pronta.

**Modelo de e-mail para o RH:**
---
Assunto: Atualização de informações pessoais

Gostaria de informar que estou em processo de transição de gênero.
A partir de agora, peço que me refiram como [nome] e utilizem [pronomes].

Atenciosamente, [nome]
---

**Após comunicar:** Solicite atualização do e-mail corporativo, crachá e sistemas internos.''',

    'discriminação': '''⚖️ **Discriminação no trabalho — seus direitos:**

A LGBTfobia no trabalho é crime (STF, 2019 — equiparada ao racismo).

**Se sofrer discriminação:**
1. Documente: datas, horários, testemunhas, mensagens
2. Registre reclamação no RH por escrito (guarde cópia)
3. Procure o Ministério do Trabalho (gov.br/trabalho)
4. Defensoria Pública — orientação jurídica gratuita
5. ANTRA e OABs com comissão de diversidade têm advogadas parceiras''',

    'geral': '''💼 **Transição no Trabalho — Guia Geral:**

**Seus direitos:**
• Uso do nome social em documentos internos e crachá
• Uso de banheiro conforme identidade de gênero
• Proteção contra demissão por identidade de gênero
• Ambiente livre de assédio

**Recursos:**
• MAPA TRANS (mapatrans.org.br) — empresas trans-inclusivas
• Business for Inclusive Growth (B4IG) — empresas com compromissos LGBTQIA+''',
  }

  return guias.get(situacao, guias['geral'])


@tool
def empresas_inclusivas(cidade: str = '', setor: str = '') -> str:
  """Busca empresas com políticas trans-inclusivas para oportunidades de trabalho.
  Args:
      cidade: Cidade para filtrar vagas (opcional).
      setor: 'tecnologia', 'saúde', 'varejo', 'finanças' (opcional).
  """
  try:
    with DDGS() as ddgs:
      query = f'empresas trans-inclusivas {setor} vagas {cidade} diversidade 2024 2025'.strip()
      results = list(ddgs.text(query, max_results=4))
    if results:
      info = '\n'.join([f'• {r["title"]}: {r["body"][:200]}' for r in results])
      return f'🏢 **Empresas Inclusivas{" em " + cidade if cidade else ""}:**\n\n{info}'
  except Exception:
    pass

  return '''🏢 **Empresas com políticas trans-inclusivas reconhecidas:**

Natura, Accenture, Magazine Luiza, Banco Itaú, Google Brasil, Microsoft Brasil, Ambev, Cielo

**Como buscar vagas:**
• MAPA TRANS (mapatrans.org.br) — banco de vagas trans-inclusivas
• LinkedIn: filtre empresas com "Programa de Diversidade"
• VAGAS.com.br: busque "diversidade LGBTQIA+"
• Plataforma TEAL (plataformateral.com.br) — vagas para LGBTQIA+'''


@tool
def seguranca_digital(tema: str = 'geral') -> str:
  """Dicas de segurança digital para pessoas trans, especialmente para proteger privacidade.
  Args:
      tema: 'privacidade', 'redes_sociais', 'stalker' ou 'geral'.
  """
  dicas = {
    'privacidade': '''🔒 **Privacidade Digital para Pessoas Trans:**

• Desative metadados de localização em fotos antes de postar
• Verifique se suas fotos aparecem em busca reversa (images.google.com)
• Revise e delete contas antigas com dados do deadname
• Google: solicite remoção de resultados desatualizados em myaccount.google.com''',

    'redes_sociais': '''📱 **Segurança em Redes Sociais:**

• Revise configurações de privacidade (quem pode ver seus posts?)
• Não hesite em bloquear e reportar conteúdo transfóbico
• Plataformas têm obrigação de remover conteúdo LGBTfóbico
• Habilite autenticação em dois fatores (2FA) sempre''',

    'stalker': '''🚨 **Se você está sendo assediada online:**

1. Documente tudo: screenshots com data e horário
2. Bloqueie e denuncie nas plataformas
3. Stalking digital é crime (Lei 14.132/2021) — registre BO
4. SaferNet: safernet.org.br | 0800-891-0087
5. Troque senhas e revise permissões de aplicativos''',

    'geral': '''🔒 **Segurança Digital — Essencial:**

• Use senhas fortes e únicas (gerenciador: Bitwarden)
• Ative autenticação em dois fatores (2FA) em tudo
• Revise permissões de aplicativos regularmente
• Use VPN em Wi-Fi público
• Mantenha backups de fotos e documentos importantes

Me pergunte sobre privacidade, redes sociais ou proteção contra assédio. 💙''',
  }

  return dicas.get(tema, dicas['geral'])
