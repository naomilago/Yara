import io
import logging

import httpx

from settings import settings

logger = logging.getLogger(__name__)

GRAPH_API_BASE = 'https://graph.facebook.com/v25.0'


def _auth_headers() -> dict:
  '''Retorna os headers de autenticação para a WhatsApp Cloud API.'''
  return {'Authorization': f'Bearer {settings.whatsapp_token}'}


async def send_text(to: str, text: str) -> None:
  '''Envia uma mensagem de texto via WhatsApp Cloud API.
  Args:
      to: Número de destino no formato internacional sem + (ex: 5511999999999).
      text: Conteúdo da mensagem.
  '''
  url = f'{GRAPH_API_BASE}/{settings.whatsapp_phone_id}/messages'
  payload = {
    'messaging_product': 'whatsapp',
    'to': to,
    'type': 'text',
    'text': {'body': text},
  }

  async with httpx.AsyncClient() as client:
    response = await client.post(url, json=payload, headers=_auth_headers())
    response.raise_for_status()
    logger.info('Texto enviado para %s — status %s', to, response.status_code)


async def upload_media(audio_bytes: bytes) -> str:
  '''Faz upload de um arquivo de áudio OGG para a Media API da Meta.
  Args:
      audio_bytes: Bytes do arquivo OGG Opus.
  Returns:
      media_id: ID do arquivo enviado para usar em send_audio.
  '''
  url = f'{GRAPH_API_BASE}/{settings.whatsapp_phone_id}/media'

  files = {
    'file': ('audio.ogg', io.BytesIO(audio_bytes), 'audio/ogg'),
    'type': (None, 'audio/ogg'),
    'messaging_product': (None, 'whatsapp'),
  }

  async with httpx.AsyncClient() as client:
    response = await client.post(url, files=files, headers=_auth_headers())
    response.raise_for_status()
    data = response.json()
    media_id = data['id']
    logger.info('Mídia enviada — media_id: %s', media_id)
    return media_id


async def download_media(media_id: str) -> bytes:
  '''Recupera a URL do arquivo de mídia e faz o download.
  Args:
      media_id: ID da mídia recebido pelo Webhook.
  Returns:
      Bytes do arquivo de áudio.
  '''
  url_info = f'{GRAPH_API_BASE}/{media_id}'
  async with httpx.AsyncClient() as client:
    resp = await client.get(url_info, headers=_auth_headers())
    resp.raise_for_status()
    media_url = resp.json().get('url')

    if not media_url:
      raise ValueError('URL de mídia não encontrada.')

    media_resp = await client.get(media_url, headers=_auth_headers())
    media_resp.raise_for_status()
    logger.info('Mídia baixada com sucesso — [%d] bytes', len(media_resp.content))
    return media_resp.content


async def send_audio(to: str, audio_bytes: bytes) -> None:
  '''Faz upload do áudio OGG e envia como mensagem de áudio no WhatsApp.
  Args:
      to: Número de destino no formato internacional.
      audio_bytes: Bytes do arquivo OGG Opus.
  '''
  media_id = await upload_media(audio_bytes)

  url = f'{GRAPH_API_BASE}/{settings.whatsapp_phone_id}/messages'
  payload = {
    'messaging_product': 'whatsapp',
    'to': to,
    'type': 'audio',
    'audio': {'id': media_id},
  }

  async with httpx.AsyncClient() as client:
    response = await client.post(url, json=payload, headers=_auth_headers())
    response.raise_for_status()
    logger.info('Áudio enviado para %s — status %s', to, response.status_code)
