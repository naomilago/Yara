import logging

from agent.graph import build_graph
from settings import settings
from whatsapp.tts import generate_audio
from whatsapp.client import send_audio, send_text, download_media
from groq import AsyncGroq

logger = logging.getLogger(__name__)




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
  audio_id: str = '',
) -> None:
  '''Processa uma mensagem de WhatsApp, chama o agente e envia a resposta.
  Args:
      from_number: Número do remetente (usado como session_id).
      text: Texto da mensagem recebida.
      request_audio: Se True, gera e envia áudio além do texto.
      audio_id: ID do áudio se a mensagem for de voz.
  '''
  try:
    if audio_id:
      try:
        audio_bytes = await download_media(audio_id)
        client = AsyncGroq(api_key=settings.groq_api_key)
        transcription = await client.audio.transcriptions.create(
          file=('audio.ogg', audio_bytes),
          model=settings.groq_whisper_model,
          language='pt',
        )
        text = transcription.text
        logger.info('Áudio recebido e transcrito: %s', text)
      except Exception as e:
        logger.error('Erro na transcrição de áudio: %s', e)
        text = 'Eu recebi um áudio seu, mas tive problemas técnicos para ouvir agora. Pode digitar?'
    # Constrói o grafo usando o número como session_id
    # para persistir sessões de diário e rastreador de humor
    graph = build_graph(
      model_name=settings.model_name,
      session_id=from_number,
    )

    config = {'configurable': {'thread_id': from_number}}

    # Lógica de limpar histórico/resetar memória
    clear_keywords = ['!limpar', 'reset', 'faxina', 'esqueça tudo', 'reiniciar']
    if any(keyword in text.lower() for keyword in clear_keywords):
      logger.info("Limpando histórico para %s", from_number)
      # No LangGraph, podemos "limpar" o estado enviando uma lista vazia de mensagens 
      # ou usando update_state para sobrescrever.
      # A forma mais garantida de resetar o fio (thread) é sobrescrever as mensagens.
      graph.update_state(config, {"messages": []})
      await send_text(to=from_number, text="Entendido! Faxina feita. 🧹 Minha memória sobre nossa conversa foi resetada. Como posso te ajudar agora? 💙")
      return

    # O checkpointer (MemorySaver) nativo do LangGraph cuidará do histórico.
    # Passamos apenas a mensagem mais recente.
    result = graph.invoke({'messages': [{'role': 'user', 'content': text}]}, config=config)

    response_text = _extract_response(result)
    logger.info("RESPOSTA GERADA: %s", response_text)

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
    logger.exception('Erro crítico ao processar mensagem de %s:', from_number)
    try:
      error_msg = f'Desculpa, tive um problema técnico ({type(e).__name__}: {str(e)}). Tente novamente em instantes. 💙'
      await send_text(
        to=from_number,
        text=error_msg,
      )
    except Exception:
      pass
