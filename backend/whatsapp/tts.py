import asyncio
import io
import logging

import httpx
from pydub import AudioSegment

from settings import settings

logger = logging.getLogger(__name__) 

ELEVENLABS_TTS_URL = 'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'
MAX_CHARS = 500


def _truncate_text(text: str, max_chars: int = MAX_CHARS) -> str:
  '''Trunca o texto no último ponto final antes de max_chars para não cortar palavras.
  Args:
      text: Texto original.
      max_chars: Limite máximo de caracteres.
  '''
  if len(text) <= max_chars:
    return text

  # Encontra o último ponto antes do limite
  truncated = text[:max_chars]
  last_period = max(
    truncated.rfind('.'),
    truncated.rfind('!'),
    truncated.rfind('?'),
  )

  if last_period > 0:
    return truncated[:last_period + 1]

  # Sem ponto encontrado, corta na última palavra completa
  last_space = truncated.rfind(' ')
  return truncated[:last_space] + '...' if last_space > 0 else truncated


def _mp3_to_ogg(mp3_bytes: bytes) -> bytes:
  '''Converte bytes MP3 para OGG Opus usando pydub + ffmpeg.
  O WhatsApp exige OGG com codec Opus para mensagens de áudio.
  Args:
      mp3_bytes: Bytes do arquivo MP3 retornado pela ElevenLabs.
  Returns:
      Bytes do arquivo OGG Opus.
  '''
  audio = AudioSegment.from_file(io.BytesIO(mp3_bytes), format='mp3')
  ogg_buffer = io.BytesIO()
  audio.export(ogg_buffer, format='ogg', codec='libopus')
  return ogg_buffer.getvalue()


async def generate_audio(text: str) -> bytes:
  '''Gera áudio a partir de texto usando ElevenLabs e converte para OGG Opus.
  Args:
      text: Texto a ser convertido em fala.
  Returns:
      Bytes do arquivo OGG Opus pronto para envio ao WhatsApp.
  '''
  truncated = _truncate_text(text)

  url = ELEVENLABS_TTS_URL.format(voice_id=settings.elevenlabs_voice_id)

  payload = {
    'text': truncated,
    'model_id': 'eleven_multilingual_v2',
    'voice_settings': {
      'stability': 0.5,
      'similarity_boost': 0.75,
    },
  }

  headers = {
    'xi-api-key': settings.elevenlabs_api_key,
    'Content-Type': 'application/json',
    'Accept': 'audio/mpeg',
  }

  async with httpx.AsyncClient(timeout=30.0) as client:
    response = await client.post(url, json=payload, headers=headers)
    response.raise_for_status()
    mp3_bytes = response.content

  # Conversão de bloqueio (CPU-bound) em thread separada
  ogg_bytes = await asyncio.to_thread(_mp3_to_ogg, mp3_bytes)

  logger.info(
    'Áudio gerado: %d chars → %d bytes OGG',
    len(truncated),
    len(ogg_bytes),
  )

  return ogg_bytes
