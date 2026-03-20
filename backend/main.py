import asyncio
import json
from typing import AsyncGenerator

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import os

from settings import settings
from agent.graph import build_graph
from whatsapp.router import router as whatsapp_router

app = FastAPI(
  title='Yara API',
  description='Assistente trans-afirmativa da comunidade trans e não-binária brasileira',
  version='1.0.0',
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=settings.cors_origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

app.include_router(whatsapp_router, prefix='/webhook')


@app.get('/api/health')
async def health_check():
  return {'status': 'ok', 'service': 'Yara API', 'version': '1.0.0'}

# Se a pasta static existir (no Docker), serve o Frontend React
static_path = os.path.join(os.path.dirname(__file__), 'static')
if os.path.exists(static_path):
  app.mount('/', StaticFiles(directory=static_path, html=True), name='static')

  @app.exception_handler(404)
  async def catch_all_for_react(request: Request, exc):
    index_path = os.path.join(static_path, 'index.html')
    return FileResponse(index_path)


async def stream_agent_response(message: str, session_id: str) -> AsyncGenerator[str, None]:
  '''Stream agent responses as Server-Sent Events.'''
  graph = build_graph(model_name=settings.model_name, session_id=session_id)
  config = {'configurable': {'thread_id': session_id}}

  try:
    async for event in graph.astream_events(
      {'messages': [{'role': 'user', 'content': message}]},
      config=config,
      version='v2',
    ):
      kind = event.get('event', '')
      if kind == 'on_chat_model_stream':
        chunk = event.get('data', {}).get('chunk')
        if chunk and hasattr(chunk, 'content') and chunk.content:
          data = json.dumps({'type': 'text', 'content': chunk.content})
          yield f'data: {data}\n\n'
      elif kind == 'on_tool_start':
        tool_name = event.get('name', '')
        data = json.dumps({'type': 'tool_start', 'tool': tool_name})
        yield f'data: {data}\n\n'
      elif kind == 'on_tool_end':
        tool_name = event.get('name', '')
        data = json.dumps({'type': 'tool_end', 'tool': tool_name})
        yield f'data: {data}\n\n'
  except Exception as e:
    error_data = json.dumps({'type': 'error', 'content': str(e)})
    yield f'data: {error_data}\n\n'
  finally:
    yield 'data: {"type": "done"}\n\n'


@app.post('/chat')
async def chat(request: Request):
  '''SSE streaming chat endpoint.'''
  body = await request.json()
  message = body.get('message', '')
  session_id = body.get('session_id', 'web-default')

  if not message:
    return {'error': 'message is required'}

  return StreamingResponse(
    stream_agent_response(message, session_id),
    media_type='text/event-stream',
    headers={
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'X-Accel-Buffering': 'no',
    },
  )
