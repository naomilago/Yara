'''
Ferramentas de Bem-estar
Meditações, diário de transição, rastreador de humor, afirmações.
'''

import random
from datetime import datetime

from langchain_core.tools import tool

# Persistência simples em memória (por session_id)
_diarios: dict[str, list] = {}
_humores: dict[str, list] = {}


@tool
def meditacao_guiada(duracao_minutos: int = 5, foco: str = 'calma') -> str:
  """Oferece uma meditação guiada trans-afirmativa.
  Args:
      duracao_minutos: Duração desejada em minutos (3, 5 ou 10).
      foco: 'calma', 'autoestima', 'corpo' ou 'ansiedade'.
  """
  meditacoes = {
    'calma': f'''🌊 **Meditação de Calma — {duracao_minutos} minutos**

Encontre uma posição confortável. Pode fechar os olhos ou suavizar o olhar.

**Respire comigo:**
Inspire pelo nariz... 1... 2... 3... 4...
Segure... 1... 2...
Expire pela boca... 1... 2... 3... 4... 5... 6...

Repita 3 vezes.

**Visualize:** Um lugar onde você se sente completamente segura e aceita.

**Afirmação:**
*"Eu sou quem eu sou. Minha identidade é real e válida."*
*"Este momento é meu. Estou aqui. Estou bem."*

Quando estiver pronta, abra os olhos lentamente. 💙''',

    'autoestima': f'''✨ **Meditação de Autoestima — {duracao_minutos} minutos**

Coloque uma mão no peito. Sinta o calor da sua própria mão.

**Afirmações — diga mentalmente:**

*"Meu corpo é meu lar."*
*"Eu mereço amor — especialmente o meu próprio."*
*"Minha existência é um ato de coragem."*
*"Eu sou suficiente exatamente como sou hoje."*

Cada pensamento negativo é uma nuvem que passa. Deixe passar. Você é extraordinária. 🌺''',

    'corpo': f'''🌸 **Meditação de Conexão com o Corpo — {duracao_minutos} minutos**

Comece pelos pés. Sinta-os. Agradeça por carregarem você.
Suba pelas pernas, quadris, barriga, peito, ombros, pescoço, rosto.

Em cada parte, diga mentalmente: *"Estou aprendendo a me amar aqui também."*

Não há pressa. Seu corpo está em transição — e isso exige paciência e compaixão.
Sua identidade é válida independente de qualquer procedimento. Você já é você. 💙''',

    'ansiedade': f'''🫁 **Meditação para Ansiedade — {duracao_minutos} minutos**

**Técnica 5-4-3-2-1 (grounding):**

• 5 coisas que você pode VER
• 4 coisas que você pode TOCAR
• 3 coisas que você pode OUVIR
• 2 coisas que você pode CHEIRAR
• 1 coisa que você pode PROVAR

**Agora respire (box breathing):**
Inspire 4... Segure 4... Expire 4... Segure 4.
Repita 4 vezes.

A ansiedade passa. Você está segura agora. 🌊''',
  }

  return meditacoes.get(foco, meditacoes['calma'])


@tool
def diario_transicao(session_id: str, acao: str = 'ler', entrada: str = '') -> str:
  """Diário de transição pessoal — registra e recupera marcos e sentimentos.
  Args:
      session_id: ID da sessão/usuário para persistência.
      acao: 'escrever' para adicionar entrada, 'ler' para ver histórico.
      entrada: Texto da entrada do diário (quando acao='escrever').
  """
  if session_id not in _diarios:
    _diarios[session_id] = []

  if acao == 'escrever' and entrada:
    registro = {
      'data': datetime.now().strftime('%d/%m/%Y às %H:%M'),
      'texto': entrada,
    }
    _diarios[session_id].append(registro)
    total = len(_diarios[session_id])
    return f'''📔 **Entrada registrada:**

📅 {registro['data']}
✍️ {registro['texto']}

Sua jornada está sendo registrada. Cada marco importa. 🌺 *(Total: {total} entrada(s))*'''

  entradas = _diarios.get(session_id, [])
  if not entradas:
    return '''📔 **Seu diário de transição está vazio ainda.**

Quer registrar sua primeira entrada? Me conte como você está se sentindo hoje, um marco recente, ou qualquer pensamento que queira guardar. 🌸'''

  ultimas = entradas[-5:]
  texto = '📔 **Seu Diário de Transição:**\n\n'
  for e in reversed(ultimas):
    texto += f'---\n📅 {e["data"]}\n{e["texto"]}\n\n'

  if len(entradas) > 5:
    texto += f'*(Mostrando as 5 entradas mais recentes de {len(entradas)} no total)*'

  return texto


@tool
def rastreador_humor(session_id: str, humor: str = '', intensidade: int = 5) -> str:
  """Rastreador de humor — registra como a pessoa está se sentindo ao longo do tempo.
  Args:
      session_id: ID da sessão/usuário.
      humor: Estado emocional atual (ex: 'feliz', 'ansiosa', 'disfórica', 'empoderada').
      intensidade: Intensidade de 1 a 10.
  """
  if session_id not in _humores:
    _humores[session_id] = []

  if humor:
    registro = {
      'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
      'humor': humor,
      'intensidade': intensidade,
    }
    _humores[session_id].append(registro)

    respostas = {
      'feliz': 'Que maravilha! Fico tão feliz por você. 🌟',
      'empoderada': 'Você merece sentir isso. Você é incrível! ✨',
      'empoderado': 'Você merece sentir isso. Você é incrível! ✨',
      'ansiosa': 'A ansiedade é difícil. Quer uma meditação guiada? 🫁',
      'ansioso': 'A ansiedade é difícil. Quer uma meditação guiada? 🫁',
      'disfórica': 'A disforia é muito pesada. Você não precisa carregar isso sozinha. Estou aqui. 💙',
      'disfórico': 'A disforia é muito pesada. Você não precisa carregar isso sozinha. Estou aqui. 💙',
      'triste': 'Tudo bem estar triste. Quer conversar sobre o que está acontecendo? 💙',
      'cansada': 'Descanso é sagrado. Cuide-se. 🌙',
      'cansado': 'Descanso é sagrado. Cuide-se. 🌙',
    }

    feedback = respostas.get(humor.lower(), 'Obrigada por compartilhar como você está. 💙')
    total = len(_humores[session_id])
    return f'''📊 **Humor registrado:**
🎭 Estado: **{humor}** (intensidade {intensidade}/10)
📅 {registro['data']}

{feedback} *(Total: {total} registros)*'''

  historico = _humores.get(session_id, [])
  if not historico:
    return '''📊 **Rastreador de Humor**

Ainda não registrei nenhum humor seu.
Como você está se sentindo agora? (feliz, ansiosa, disfórica, empoderada, triste, cansada...)'''

  texto = '📊 **Seu histórico de humor:**\n\n'
  for h in reversed(historico[-10:]):
    barra = '█' * h['intensidade'] + '░' * (10 - h['intensidade'])
    texto += f'📅 {h["data"]} — **{h["humor"]}** [{barra}] {h["intensidade"]}/10\n'

  return texto


@tool
def afirmacao_positiva(contexto: str = 'geral') -> str:
  """Oferece afirmações positivas e trans-afirmativas personalizadas.
  Args:
      contexto: 'disforia', 'familia', 'trabalho', 'solidao', 'coragem' ou 'geral'.
  """
  afirmacoes = {
    'disforia': [
      'Sua identidade é real, mesmo quando seu corpo parece não refletir isso ainda. A jornada tem seu tempo — e você está nela. 💙',
      'A disforia é real e é pesada. E também é temporária. Cada dia é um passo. 🌺',
      'Você não precisa amar cada parte do seu corpo hoje. Gentileza consigo mesma também é trans-afirmativo. ✨',
    ],
    'familia': [
      'Você não precisa de validação da sua família para ser quem você é. Sua identidade existe com ou sem a aprovação deles. 💙',
      'Algumas famílias precisam de tempo. Isso não é reflexo do seu valor — é reflexo da ignorância deles. Você merece amor. 🌸',
      'Você pode criar sua própria família de escolha. A comunidade trans está aqui. 🏳️‍⚧️',
    ],
    'trabalho': [
      'Você tem o direito de existir autenticamente no trabalho. Sua identidade não é um fardo. 💙',
      'Cada vez que você existe abertamente, você abre caminho para quem vem depois. Você é pioneira. ✨',
    ],
    'solidao': [
      'Solidão não é a mesma coisa que estar sozinha. Você tem a comunidade trans, mesmo que ainda não a tenha encontrado. 💙',
      'Você é uma em mais de 250 mil pessoas trans no Brasil. Não está sozinha, mesmo que pareça. 🌺',
      'Este momento vai passar. A conexão é possível. Você merece amizade e afeto. 💜',
    ],
    'coragem': [
      'Existir como pessoa trans no Brasil exige coragem extraordinária. Você é extraordinária. 🦁',
      'Cada dia que você vive sendo quem você é, você resiste. Resistir é amor próprio radical. 💙',
      'Você não pediu para ser trans — mas escolhe, todos os dias, viver com autenticidade. Isso é belíssimo. 🏳️‍⚧️',
    ],
    'geral': [
      'Você existe. Você importa. Sua identidade é válida. 💙',
      'Ser trans é parte de quem você é — mas não é tudo. Você é multidimensional e extraordinária. 🌟',
      'Você merece amor, comunidade, saúde e alegria. Nada disso precisa ser conquistado — você já merece. 🌺',
      'Sua presença no mundo é um presente. Obrigada por existir. 🏳️‍⚧️💙🌸',
    ],
  }

  lista = afirmacoes.get(contexto, afirmacoes['geral'])
  return random.choice(lista)
