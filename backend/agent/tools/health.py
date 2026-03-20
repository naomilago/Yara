'''
Ferramentas de Saúde
Busca de ambulatórios SUS, informações sobre hormonização e cuidados médicos.
'''

from duckduckgo_search import DDGS
from langchain_core.tools import tool


@tool
def buscar_ambulatorio(cidade: str, estado: str = '') -> str:
  """Busca ambulatórios trans-afirmativos pelo SUS em uma cidade.
  Args:
      cidade: Nome da cidade.
      estado: Sigla do estado (ex: SP, RJ) — opcional.
  """
  query = f'ambulatório transexualizador SUS {cidade} {estado} endereço agendamento'.strip()
  try:
    with DDGS() as ddgs:
      results = list(ddgs.text(query, max_results=5))
    if results:
      info = '\n'.join([f'• **{r["title"]}**: {r["body"][:300]}' for r in results])
      return f'''🏥 **Ambulatórios Trans-Afirmativos — {cidade}:**

{info}

💡 O Processo Transexualizador do SUS (Portaria 2.803/2013) garante hormonização e acompanhamento multidisciplinar gratuitos.'''
  except Exception:
    pass

  return f'''Para encontrar ambulatórios em {cidade}:

1. Acesse sua UBS e solicite encaminhamento ao Processo Transexualizador
2. Consulte cnes.datasus.gov.br (filtre por Ambulatório)
3. ANTRA (antrabrasil.org) tem lista atualizada por região
4. Ligue 136 — Central do Ministério da Saúde'''


@tool
def info_hormonizacao(tipo: str = 'geral') -> str:
  """Informações sobre hormonização de afirmação de gênero.
  Args:
      tipo: 'feminizante', 'masculinizante', 'inicio' ou 'geral'.
  """
  bases = {
    'feminizante': '''💊 **Hormonização Feminizante — Informações Gerais**

**Medicamentos comuns (sob supervisão médica):**
• Estradiol (oral, transdérmico ou injetável)
• Antiandrogênicos: espironolactona, bicalutamida, acetato de ciproterona

**Efeitos ao longo do tempo:**
• 1–3 meses: pele mais suave, redução de oleosidade
• 3–6 meses: redistribuição de gordura, início do crescimento mamário
• 6–12 meses: mudanças mais expressivas
• 1–3 anos: maior estabilização

⚠️ Nunca inicie sem supervisão médica. Busque ambulatório SUS ou endocrinologista.''',

    'masculinizante': '''💉 **Hormonização Masculinizante — Informações Gerais**

**Medicamento principal:**
• Testosterona (injetável — cipionato ou enantato; gel transdérmico)

**Efeitos ao longo do tempo:**
• 1–3 meses: engrossamento da voz, aumento de libido
• 3–6 meses: crescimento de pelos, clitoromegalia
• 6–12 meses: redistribuição de gordura, massa muscular
• 1–3 anos: parada das menstruações (geralmente nos primeiros meses)

⚠️ Nunca inicie sem supervisão médica. Busque ambulatório SUS ou endocrinologista.''',

    'inicio': '''🌱 **Como Iniciar a Hormonização pelo SUS:**

1. Procure uma UBS e solicite encaminhamento ao Processo Transexualizador
2. Aguarde consulta com equipe multidisciplinar
3. Após avaliação, receba a prescrição e retire pelo SUS (Farmácia Popular/CONASS)

**Pelo sistema privado:** Busque endocrinologista ou ginecologista com experiência em saúde trans.

**Informed Consent:** Alguns profissionais não exigem laudos psiquiátricos — apenas sua autonomia como adulta.''',
  }

  if tipo in bases:
    return bases[tipo]

  try:
    with DDGS() as ddgs:
      results = list(ddgs.text(f'hormonização trans {tipo} saúde Brasil', max_results=3))
    if results:
      info = '\n'.join([f'• {r["title"]}: {r["body"][:250]}' for r in results])
      return f'**Hormonização — {tipo}:**\n\n{info}\n\n⚠️ Consulte sempre um profissional especializado.'
  except Exception:
    pass

  return bases.get('inicio', 'Busque um ambulatório trans-afirmativo para orientação médica personalizada.')


@tool
def preparar_consulta(tipo_consulta: str) -> str:
  """Ajuda a se preparar para uma consulta médica relacionada à transição de gênero.
  Args:
      tipo_consulta: Ex: 'primeira consulta', 'hormonização', 'cirurgia', 'psicólogo'.
  """
  dicas_gerais = '''📋 **Dicas Gerais para Consultas Médicas:**

**Antes:**
• Anote sintomas, dúvidas e histórico de saúde
• Leve: RG/CNH, Cartão SUS, comprovante de residência, exames anteriores
• Informe medicações em uso (incluindo automedicação)

**Durante:**
• Você tem direito ao uso do nome social
• Pode ser acompanhada por alguém de confiança
• Tire todas as dúvidas — anote ou grave as orientações

**Seus direitos:**
• Atendimento respeitoso e sem discriminação
• Sigilo médico
• Segunda opinião médica'''

  perguntas_hormonizacao = '''
**Perguntas para consulta de hormonização:**
• Quais são os efeitos esperados e em quanto tempo?
• Que exames precisarei fazer regularmente?
• Posso retirar a medicação pelo SUS/Farmácia Popular?
• Qual a posologia e como aplicar (se injetável)?'''

  perguntas_cirurgia = '''
**Perguntas para consulta cirúrgica:**
• O procedimento está coberto pelo Processo Transexualizador do SUS?
• Qual é o tempo de espera e os critérios de elegibilidade?
• Como é a recuperação e quais são os riscos?'''

  perguntas_psicologo = '''
**Para consulta com psicólogo:**
• Verifique antes se tem experiência com pessoas trans
• Você não precisa provar nem justificar sua identidade
• O psicólogo não pode condicionar atendimento a "cura" de identidade
• Plataformas afirmativas: TudoPsi, Psicologia Viva, Zenklub'''

  resposta = dicas_gerais
  if 'hormoniz' in tipo_consulta.lower():
    resposta += perguntas_hormonizacao
  elif 'cirurgi' in tipo_consulta.lower():
    resposta += perguntas_cirurgia
  elif 'psic' in tipo_consulta.lower():
    resposta += perguntas_psicologo

  return resposta


@tool
def cuidados_pos_cirurgia(procedimento: str) -> str:
  """Informações gerais sobre cuidados pós-cirúrgicos para procedimentos de afirmação de gênero.
  Args:
      procedimento: Nome do procedimento (ex: 'vaginoplastia', 'mastectomia').
  """
  try:
    with DDGS() as ddgs:
      results = list(ddgs.text(
        f'cuidados pós-cirurgia {procedimento} afirmação gênero trans recuperação',
        max_results=4,
      ))
    if results:
      info = '\n'.join([f'• {r["title"]}: {r["body"][:300]}' for r in results])
      return f'''🏥 **Cuidados Pós-operatórios — {procedimento}:**

{info}

⚠️ Siga SEMPRE as orientações específicas da sua equipe médica. Em caso de sangramento excessivo, febre acima de 38°C ou sinais de infecção, procure emergência.'''
  except Exception:
    pass

  return f'''Para cuidados pós-operatórios de {procedimento}:

• Siga as instruções da sua equipe cirúrgica
• Em emergência (sangramento, febre, infecção), vá ao pronto-socorro
• A ANTRA pode indicar pacientes que já passaram pelo procedimento
• Você está indo muito bem nessa jornada. 💙'''
