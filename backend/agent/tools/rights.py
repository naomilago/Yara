'''
Ferramentas de Direitos
Retificação de nome e gênero, nome social, denúncias.
'''

from duckduckgo_search import DDGS
from langchain_core.tools import tool


@tool
def retificar_nome_genero(estado: str = '', duvida: str = '') -> str:
  """Informa sobre retificação de nome e gênero nos documentos brasileiros sem laudo ou cirurgia.
  Args:
      estado: Sigla do estado para buscar cartórios ou informações locais (opcional).
      duvida: Dúvida específica sobre o processo (opcional).
  """
  info_base = '''📄 **Retificação de Nome e Gênero — Brasil**

✅ **Não precisa de cirurgia**
✅ **Não precisa de laudo psiquiátrico**
✅ **Não precisa de processo judicial**
✅ **Pode ser feito no cartório de registro civil**

**Base legal:** Decisão STF (ADI 4275/2018) + Provimento CNJ nº 73/2018

**Como fazer (via extrajudicial — mais rápido):**
1. Procure um cartório de registro civil (qualquer um)
2. Apresente: documento com foto, CPF, certidão de nascimento
3. Preencha o formulário de retificação
4. Aguarde o prazo (geralmente 5 dias úteis)

**Custos:** Gratuito com declaração de pobreza (LOAS). Custos cartoriais para quem pode pagar.

**Dúvidas comuns:**
• Posso retificar com menos de 18 anos? Sim, com autorização dos responsáveis
• E o histórico escolar? Atualize apresentando a certidão retificada'''

  if duvida:
    try:
      with DDGS() as ddgs:
        results = list(ddgs.text(
          f'retificação nome gênero trans Brasil {duvida}',
          max_results=3,
        ))
      if results:
        extra = '\n'.join([f'• {r["title"]}: {r["body"][:200]}' for r in results])
        return f'{info_base}\n\n**Sobre "{duvida}":**\n{extra}'
    except Exception:
      pass

  return info_base


@tool
def usar_nome_social(contexto: str = 'geral') -> str:
  """Informa sobre o direito ao nome social em diferentes contextos.
  Args:
      contexto: 'saúde', 'escola', 'trabalho', 'banco' ou 'geral'.
  """
  contextos = {
    'saúde': '''🏥 **Nome Social na Saúde**

**Base legal:** Portaria 1.820/2009 (MS) e Carta dos Direitos dos Usuários do SUS

✅ Ser chamada pelo nome social em todas as unidades (públicas e privadas)
✅ Prontuário com nome social visível
✅ Respeito à identidade de gênero em internações

**Se não respeitarem:**
1. Solicite falar com a ouvidoria da unidade
2. Registre no Disque 136 (Central do SUS)
3. Protocole no CRM ou COREN''',

    'escola': '''🎓 **Nome Social na Escola e Universidade**

**Base legal:** Resolução CNE/CP nº 1/2018

✅ Nome social em chamadas e documentos internos
✅ Acesso a banheiros conforme identidade de gênero
✅ Proteção contra bullying por identidade de gênero

**Como usar:** Registre o nome social na secretaria.
Em universidades federais, o SIGAA já suporta nome social.
No ENEM: há campo específico para nome social na inscrição.

**Se houver problemas:** Acione a Ouvidoria do MEC (0800 616161)''',

    'trabalho': '''💼 **Nome Social no Trabalho**

**Base legal:** Portaria MTE nº 1.083/2021

✅ Nome social em crachá, e-mail e documentos internos
✅ Proteção contra demissão por identidade de gênero
✅ Uso de banheiro conforme identidade de gênero

**Como implementar:**
1. Solicite formalmente ao RH por escrito
2. Informe TI para atualização em sistemas

**Se houver discriminação:** Procure o Ministério do Trabalho ou advogado trabalhista.''',

    'banco': '''🏦 **Nome Social em Bancos**

**Base legal:** Resolução BACEN nº 4.860/2020

✅ Nome social em todos os produtos e canais após solicitação

**Como fazer:** Vá a uma agência com documento oficial ou use o app/internet banking.
A maioria dos grandes bancos já suporta pelo app.''',
  }

  return contextos.get(contexto, '''📋 **Direito ao Nome Social no Brasil**

Onde é garantido por lei:
• ✅ Saúde (SUS e rede privada)
• ✅ Educação (escolas e universidades)
• ✅ Serviço público federal, estadual e municipal
• ✅ Bancos (Resolução BACEN)
• ✅ ENEM e vestibulares

Você não precisa de nenhum documento especial — é um direito seu.
Simplesmente diga: *"Meu nome social é [nome]. Por favor, me chame assim."*''')


@tool
def denunciar_transfobia(tipo: str = 'geral', estado: str = '') -> str:
  """Orienta sobre como denunciar discriminação e violência transfóbica.
  Args:
      tipo: 'violência', 'discriminação', 'trabalho', 'saúde' ou 'geral'.
      estado: Estado onde ocorreu (opcional).
  """
  info_base = '''⚖️ **Como Denunciar Transfobia — Guia Prático**

**🔴 Emergências / Violência:**
• 190 — Polícia Militar
• 180 — Central da Mulher
• 100 — Disque Direitos Humanos (crimes de ódio)

**🟡 Discriminação:**
• Disque 100 — Direitos Humanos Federal
• ANTRA: antrabrasil.org
• Defensoria Pública do Estado (gratuita)

**🟢 Online / Redes Sociais:**
• Documente (screenshot) ANTES de denunciar
• Protocole no SENACON (consumidor.gov.br)

**Como documentar:**
1. Guarde screenshots, gravações, datas/horários e nomes de testemunhas
2. Registre Boletim de Ocorrência — você tem direito mesmo que a polícia resista

**A LGBTfobia é crime no Brasil** (STF 2019, equiparada ao racismo). 💙'''

  if estado:
    try:
      with DDGS() as ddgs:
        results = list(ddgs.text(
          f'denúncia transfobia LGBTfobia {estado} delegacia órgão',
          max_results=3,
        ))
      if results:
        extra = '\n'.join([f'• {r["title"]}: {r["body"][:200]}' for r in results])
        return f'{info_base}\n\n**Órgãos locais em {estado}:**\n{extra}'
    except Exception:
      pass

  return info_base


@tool
def direitos_trans(tema: str) -> str:
  """Explica os direitos legais das pessoas trans no Brasil sobre um tema.
  Args:
      tema: Ex: 'banheiro', 'adoção', 'prisão', 'casamento', 'herança'.
  """
  try:
    with DDGS() as ddgs:
      results = list(ddgs.text(
        f'direitos pessoas trans Brasil {tema} lei jurisprudência 2024',
        max_results=4,
      ))
    if results:
      info = '\n'.join([f'• {r["title"]}: {r["body"][:300]}' for r in results])
      return f'''⚖️ **Direitos Trans — {tema.title()}:**

{info}

📌 **Recursos jurídicos gratuitos:**
• Defensoria Pública do Estado
• ANTRA (antrabrasil.org)
• OAB — Comissão de Diversidade Sexual e de Gênero'''
  except Exception:
    pass

  return f'''Para informações jurídicas sobre {tema}:

• Defensoria Pública oferece orientação gratuita
• ANTRA tem advogadas trans e aliadas
• JusBrasil (jusbrasil.com.br) para consultar jurisprudência

Você tem direitos. A lei está do seu lado. 💙'''
