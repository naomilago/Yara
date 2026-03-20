'''
Ferramentas de Identidade
Guia de pronomes, gerador de nomes, músicas e artistas afirmativos.
'''

from duckduckgo_search import DDGS
from langchain_core.tools import tool


@tool
def guia_pronomes(pronome: str = 'geral') -> str:
  """Guia personalizado sobre pronomes e linguagem de gênero no português brasileiro.
  Args:
      pronome: 'ela', 'ele', 'elu', 'neutro', 'neopronomens' ou 'geral'.
  """
  guias = {
    'ela': '''🏳️‍⚧️ **Guia de Pronomes — Ela/Dela**

**Uso correto:**
• "Ela foi ao mercado" ✅
• "Ela trouxe o livro dela" ✅
• "Gostei muito dela" ✅

**Ao apresentar:**
• "Esta é [nome], ela é [profissão]."

**Dica:** Se alguém errar, uma correção gentil: "Prefiro o pronome 'ela', obrigada."

Pronomes importam porque reconhecem quem a pessoa é. 💙''',

    'ele': '''🏳️‍⚧️ **Guia de Pronomes — Ele/Dele**

**Uso correto:**
• "Ele foi ao mercado" ✅
• "Ele trouxe o livro dele" ✅
• "Gostei muito dele" ✅

**Ao apresentar:**
• "Este é [nome], ele é [profissão]."

**Dica:** Se alguém errar: "Prefiro o pronome 'ele', obrigado."

Pronomes corretos são um gesto de respeito fundamental. 💙''',

    'elu': '''🏳️‍⚧️ **Guia de Pronomes — Elu/Delu (neutro)**

**Uso correto:**
• "Elu foi ao mercado" ✅
• "Trouxe o livro delu" ✅
• "Gostei muito delu" ✅

**Adjetivos neutros:**
• "Elu está cansadu" / "Elu é bonitu" / "Elu é meu amigx"

**Ao apresentar:**
• "Estu é [nome], elu é [profissão]."

Pronomes neutros em português ainda estão em construção pela comunidade — há variações e muita riqueza nessa criação. 🌱''',

    'neopronomes': '''🌈 **Neopronomes em Português Brasileiro**

O português está em evolução. Alguns neopronomes usados:

| Sistema | Sujeito | Objeto | Possessivo |
|---|---|---|---|
| Neutro -u | elu | delu | seu/sua |
| Neutro -e | ile | dile | seu/sua |
| Neutro -x | ex | dex | seu/sua |
| Neutro -@ | el@ | del@ | seu/sua |

**Na prática:** Pergunte sempre qual pronome a pessoa prefere.
"Qual pronome você usa?" é sempre a pergunta certa.''',

    'geral': '''🏳️‍⚧️ **Guia de Pronomes — Visão Geral**

**Pronomes comuns em português:**
• **Ela/Dela** — para mulheres trans e pessoas femininas
• **Ele/Dele** — para homens trans e pessoas masculinas
• **Elu/Delu** — pronome neutro, usado por pessoas não-binárias

**Boas práticas:**
• Sempre pergunte: "Qual pronome você usa?"
• Se errar, corrija sem drama e siga em frente
• Não é preciso entender a identidade de alguém para respeitar o pronome

**Linguagem neutra no dia a dia:**
• "Bom dia a todos" → "Bom dia a todxs" ou "Bom dia a todes"
• "Obrigado" → "Obrigade" (neutro)

Quer saber sobre um pronome específico? Me diz! 💙''',
  }

  return guias.get(pronome, guias['geral'])


@tool
def gerador_nomes(
  genero: str = 'feminino',
  origem: str = '',
  significado: str = '',
) -> str:
  """Sugere nomes com seus significados para pessoas trans em processo de renomeação.
  Args:
      genero: 'feminino', 'masculino' ou 'neutro'.
      origem: Origem cultural preferida (ex: 'tupi', 'grego', 'hebraico', 'latino').
      significado: Tema de significado desejado (ex: 'água', 'luz', 'força', 'liberdade').
  """
  nomes_base = {
    'feminino': {
      'tupi': [
        ('Iara', 'senhora das águas — protetora e poderosa'),
        ('Jaci', 'deusa da lua'),
        ('Uiara', 'mãe d\'água, protetora dos rios'),
        ('Cauã', 'falcão — associado à liberdade'),
        ('Araci', 'aurora, início do dia'),
      ],
      'grego': [
        ('Iris', 'deusa do arco-íris — ponte entre mundos'),
        ('Zoe', 'vida'),
        ('Sofia', 'sabedoria'),
        ('Calypso', 'que oculta — misteriosa e profunda'),
        ('Lyra', 'instrumento da harmonia'),
      ],
      'geral': [
        ('Luna', 'lua — mudança e ciclos'),
        ('Aurora', 'amanhecer — novos começos'),
        ('Valentina', 'força e saúde'),
        ('Marina', 'do mar — profundidade'),
        ('Serena', 'tranquilidade e paz'),
        ('Stella', 'estrela'),
      ],
    },
    'masculino': {
      'tupi': [
        ('Cauã', 'falcão — símbolo de liberdade'),
        ('Ayrton', 'filho da terra'),
        ('Arã', 'pombo — paz e recomeço'),
      ],
      'grego': [
        ('Orion', 'caçador — determinação'),
        ('Theo', 'dom divino'),
        ('Leon', 'leão — coragem'),
        ('Phoenix', 'renascimento — transformação'),
      ],
      'geral': [
        ('Enzo', 'governante do lar'),
        ('Lucas', 'luz'),
        ('Mateus', 'dom de Deus'),
        ('Luan', 'guerreiro — força e bravura'),
        ('Ícaro', 'ousadia — aquele que se atreve a voar'),
      ],
    },
    'neutro': {
      'geral': [
        ('Ari', 'leão / águia — força'),
        ('Luca', 'luz'),
        ('Sasha', 'protetor/protetora'),
        ('Robin', 'brilhante de fama'),
        ('Sol', 'energia, calor, vitalidade'),
        ('Blue', 'profundidade e calma'),
        ('River', 'fluir — transformação constante'),
      ],
    },
  }

  lista = nomes_base.get(genero, nomes_base['feminino'])

  # Tenta encontrar pela origem
  if origem:
    sublista = lista.get(origem.lower())
    if not sublista:
      sublista = lista.get('geral', [])
  else:
    # Mescla tudo
    sublista = []
    for v in lista.values():
      sublista.extend(v)

  # Filtra por significado se fornecido
  if significado:
    filtrados = [(n, s) for (n, s) in sublista if significado.lower() in s.lower()]
    if filtrados:
      sublista = filtrados

  # Busca online para enriquecer
  sugestoes_online = ''
  try:
    with DDGS() as ddgs:
      results = list(ddgs.text(
        f'nomes {genero} {origem} significado {significado} bonitos 2024',
        max_results=3,
      ))
    if results:
      sugestoes_online = '\n💡 **Mais inspirações online:**\n'
      sugestoes_online += '\n'.join([f'• {r["title"]}: {r["body"][:150]}' for r in results])
  except Exception:
    pass

  texto = f'✨ **Sugestões de nomes {genero}s{" de origem " + origem if origem else ""}:**\n\n'
  for nome, sig in sublista[:8]:
    texto += f'• **{nome}** — {sig}\n'

  if sugestoes_online:
    texto += sugestoes_online

  texto += '\n\nEscolher um nome é um ato profundo de autoconhecimento. Não há pressa. 🌸'
  return texto


@tool
def musicas_afirmativas(humor: str = 'empoderamento') -> str:
  """Sugere músicas e artistas trans e afirmativos de acordo com o humor.
  Args:
      humor: 'empoderamento', 'calma', 'alegria', 'choro', 'resistência' ou 'geral'.
  """
  playlists = {
    'empoderamento': '''🎵 **Músicas para Empoderamento Trans:**

🌺 **Linn da Quebrada** — "Bixa Travesty", "Deus Feita Gente", "Pajubá"
🎙️ **Liniker** — "Zero", "Carioca", "Baby 95"
💃 **Gloria Groove** — "Coisa Boa", "Você Vai Se Arrepender"
🎤 **Ludmilla** — "Rainha da Favela"
🌟 **Duda Beat** — "Amor Bossanova"
⚡ **LÉSBICAS A LA VISTA** — pop trans-afirmativo nacional''',

    'calma': '''🎵 **Músicas para Calmar e Acolher:**

🎶 **Liniker** — "Ocupei" (voz suave, presença total)
🍃 **Emicida** — "AmarElo", "Principia"
🌊 **Céu** — "Malemolência"
🌙 **Maria Gadú** — "Shimbalaiê"
☁️ **Criolo** — "Não Existe Amor em SP" (reflexiva)''',

    'resistência': '''🎵 **Músicas de Resistência Trans:**

✊ **Linn da Quebrada** — "Bixa Travesty", "Enviadescer"
🔥 **MC Xuxú** — trap trans-afirmativa
🌈 **Bia Ferreira** — "Cota Não É Esmola" (interseccional)
💜 **Pabllo Vittar** — "Problema Seu", "K.O."
🗣️ **Rico Dalasam** — rap LGBTQIA+''',

    'geral': '''🎵 **Artistas Afirmativos para Conhecer:**

**Brasileiras/os:**
• 🌺 **Linn da Quebrada** — performer revolucionária
• 🎤 **Liniker** — soul com identidade
• 💃 **Gloria Groove** — drag queen pop
• 🌈 **Pabllo Vittar** — maior drag brasileira
• 🎸 **Duda Beat** — indie pop afirmativo

**Internacionais:**
• **Kim Petras** — pop trans feminino
• **SOPHIE** — vanguarda eletrônica trans (in memoriam)
• **Arca** — experimental trans venezolana
• **Jake Wesley Rogers** — soul queer

Qual humor você está? Posso montar uma playlist mais personalizada! 💙''',
  }

  try:
    resposta_base = playlists.get(humor, playlists['geral'])
    with DDGS() as ddgs:
      results = list(ddgs.text(
        f'artistas trans músicas afirmativas {humor} 2024 2025 Brasil',
        max_results=3,
      ))
    if results:
      extra = '\n\n🔍 **Descobertas recentes:**\n'
      extra += '\n'.join([f'• {r["title"]}: {r["body"][:150]}' for r in results])
      return resposta_base + extra
  except Exception:
    pass

  return playlists.get(humor, playlists['geral'])
