from fastapi.background import BackgroundTasks
from fastapi.responses import PlainTextResponse
from fastapi import APIRouter, Request

from settings import settings
from whatsapp.handler import handle_message

router = APIRouter()


@router.get('/whatsapp')
async def whatsapp_verify(request: Request):
  '''Verificação do webhook pela Meta.
  Recebe hub.mode, hub.verify_token e hub.challenge.
  Retorna hub.challenge como texto plano se o token bater.
  '''
  params = request.query_params
  mode = params.get('hub.mode')
  token = params.get('hub.verify_token')
  challenge = params.get('hub.challenge')

  if mode == 'subscribe' and token == settings.whatsapp_verify_token:
    return PlainTextResponse(content=challenge, status_code=200)

  return PlainTextResponse(content='Forbidden', status_code=403)


@router.post('/whatsapp')
async def whatsapp_webhook(request: Request, background_tasks: BackgroundTasks):
  '''Recebe notificações da Meta.
  Retorna 200 imediatamente e processa a mensagem em background
  para não dar timeout na Meta (limite: 20s).
  '''
  try:
    data = await request.json()
    entry = data.get('entry', [])

    for e in entry:
      for change in e.get('changes', []):
        value = change.get('value', {})
        messages = value.get('messages', [])

        for msg in messages:
          msg_type = msg.get('type', '')

          if msg_type == 'text':
            from_number = msg.get('from', '')
            text = msg.get('text', {}).get('body', '')

            if from_number and text:
              # Detecta se o usuário quer resposta em áudio
              audio_keywords = ('áudio', 'audio', 'voz', 'falar', 'ouvir')
              request_audio = any(kw in text.lower() for kw in audio_keywords)

              background_tasks.add_task(
                handle_message,
                from_number=from_number,
                text=text,
                request_audio=request_audio,
              )

  except Exception:
    # Sempre retorna 200 para a Meta não desativar o webhook
    pass

  return {'status': 'ok'}
