from typing import List
from pydantic_settings import BaseSettings
from pydantic.networks import AnyHttpUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "jetfork_hack"
    API_PATH: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    ELASTICSEARCH_INDEX: str = "videos_index__v6"


settings = Settings()
