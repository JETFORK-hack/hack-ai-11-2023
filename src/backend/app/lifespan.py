import logging
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
from app.core.config import settings
from contextlib import asynccontextmanager
from elasticsearch import AsyncElasticsearch
from utils.nearest_queries import NearestQueries

from utils.spelling_checker.sym_spell_servicer import SymSpellRouterServicer

# Elastice
index = settings.ELASTICSEARCH_INDEX


class GlobalContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    es: AsyncElasticsearch | None = None
    spell_checker: SymSpellRouterServicer | None = None
    nearest_queries: NearestQueries | None = None


global_objs = GlobalContext()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info(f"Loading ElasticSearch connect ({settings.ELASTICSEARCH_INDEX=})")
    global global_objs
    global_objs.es = AsyncElasticsearch(settings.ELASTICSEARCH_URL)
    # Models
    logging.info("Loading SpellChecker sources")
    global_objs.spell_checker = SymSpellRouterServicer()
    logging.info("Loading NearestQueries models")
    global_objs.nearest_queries = NearestQueries()
    logging.info("SERVER STARTED")
    yield
    await global_objs.es.close()
    del global_objs


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logging.info("Loading ElasticSearch connect")
#     global global_objs
#     global_objs["es"] = AsyncElasticsearch(settings.ELASTICSEARCH_URL)
#     # Models
#     logging.info("Loading SpellChecker sources")
#     global_objs["spell_checker"] = SymSpellRouterServicer()
#     logging.info("Loading NearestQueries models")
#     global_objs["nearest_queries"] = NearestQueries()
#     logging.info("SERVER STARTED")
#     yield
#     await global_objs["es"].close()
#     global_objs.clear()
