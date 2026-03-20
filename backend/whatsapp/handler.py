import logging

from agent.graph import build_graph
from settings import settings
from whatsapp.tts import generate_audio
from whatsapp.client import send_audio, send_text

logger = logging.getLogger(__name__)

# Histórico de conversa em memória: from_number → lista de mensagens
# Limitado a 20 mensagens por número para não estourar o contexto
_conversation_history: dict[str, list] = {}
MAX_HISTORY = 20


def _get_history(from_number: str) -> list:
  '''Retorna o histórico de conversa para um número, iniciando se necessário.'''
  if from_number not in _conversation_history:
    _conversation_history[from_number] = []
  return _conversation_history[from_number]


def _add_to_history(from_number: str, role: str, content: str) -> None:
  '''Adiciona uma mensagem ao histórico, truncando se ultrapassar o limite.'''
  history = _get_history(from_number)
  history.append({'role': role, 'content': content})
  if len(history) > MAX_HISTORY:
    # Remove as mais antigas mantendo sempre MAX_HISTORY mensagens
    _conversation_history[from_number] = history[-MAX_HISTORY:]


def _extract_response(result: dict) -> str:
  '''Extrai o conteúdo de texto da última mensagem do resultado do grafo.'''
  messages = result.get('messages', [])
  for msg in reversed(messages):
    # Suporte a objetos LangChain e dicionários simples
    content = getattr(msg, 'content', None) or msg.get('content', '')
    role = getattr(msg, 'type', None) or msg.get('role', '')
    if content and role in ('ai', 'assistant'):
      return content
  return 'Desculpa, não consegui gerar uma resposta. Tente novamente. 💙'


async def handle_message(
  from_number: str,
  text: str,
  request_audio: bool = False,
) -> None:
  '''Processa uma mensagem de WhatsApp, chama o agente e envia a resposta.
  Args:
      from_number: Número do remetente (usado como session_id).
      text: Texto da mensagem recebida.
      request_audio: Se True, gera e envia áudio além do texto.
  '''
  try:
    # Adiciona a mensagem do usuário ao histórico
    _add_to_history(from_number, 'user', text)

    # Constrói o grafo usando o número como session_id
    # para persistir sessões de diário e rastreador de humor
    graph = build_graph(
      model_name=settings.model_name,
      session_id=from_number,
    )

    config = {'configurable': {'thread_id': from_number}}

    # Monta input com histórico completo
    history = _get_history(from_number)
    result = graph.invoke({'messages': history}, config=config)

    response_text = _extract_response(result)
    logger.info("RESPOSTA GERADA: %s", response_text)

    # Adiciona resposta ao histórico
    _add_to_history(from_number, 'assistant', response_text)

    # Envia texto
    await send_text(to=from_number, text=response_text)

    # Envia áudio se solicitado
    if request_audio:
      try:
        audio_bytes = await generate_audio(response_text)
        await send_audio(to=from_number, audio_bytes=audio_bytes)
      except Exception as e:
        logger.error('Erro ao gerar/enviar áudio: %s', e)

  except Exception as e:
    logger.error('Erro ao processar mensagem de %s: %s', from_number, e)
    try:
      await send_text(
        to=from_number,
        text='Desculpa, tive um problema técnico. Tente novamente em instantes. 💙',
      )
    except Exception:
      pass
