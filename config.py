import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    atlas_host: str = os.environ['ATLAS_HOST']
    openai_api_key: str = os.environ['OPENAI_API_KEY']
    database: str = 'search-tutorial'
    collection: str = 'test-01'
    index_name: str = 'vsearch_index'
