from typing import List, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.networks import AnyHttpUrl


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    PROJECT_NAME: str = "jetfork_hack"
    API_PATH: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl | Literal['*']] = ['*']
    ELASTICSEARCH_URL: str = "http://elasticsearch:9200"
    ELASTICSEARCH_INDEX: str = "videos_index__v1"


settings = Settings()
