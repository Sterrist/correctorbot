from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from textwrap import dedent

class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    ADMIN_IDS: set[int]

    OPENAI_BASE_URL: str = 'https://api.openai.com/v1'
    OPENAI_API_KEY: SecretStr
    OPENAI_MODEL: str = 'gpt-5.4-nano-2026-03-17'

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore" 
    )

settings = Settings()
