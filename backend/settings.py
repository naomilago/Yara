from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  model_config = SettingsConfigDict(
    env_file='.env',
    env_file_encoding='utf-8',
    extra='ignore',
  )

  # Groq / LLM
  groq_api_key: str = ''
  model_name: str = 'llama-3.1-8b-instant'

  # WhatsApp Cloud API
  whatsapp_token: str = ''
  whatsapp_phone_id: str = ''
  whatsapp_verify_token: str = ''

  # ElevenLabs TTS
  elevenlabs_api_key: str = ''
  elevenlabs_voice_id: str = ''

  # App
  cors_origins: list[str] = ['http://localhost:5173', 'http://localhost:3000']


settings = Settings()
