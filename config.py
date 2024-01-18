from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    openai_api_key: str = os.environ['OPENAI_API_KEY']
    atlas_host: str = ''
