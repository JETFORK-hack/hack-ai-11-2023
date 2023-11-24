from fastapi import FastAPI
from app.core.config import settings
from contextlib import asynccontextmanager
from elasticsearch import AsyncElasticsearch

client = AsyncElasticsearch(hosts=settings.ELASTICSEARCH_URL)
index = settings.ELASTICSEARCH_INDEX

es = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global es
    es = AsyncElasticsearch(settings.ELASTICSEARCH_URL)
    yield
    await es.close()


async def query_es(query: str, page: int, page_size: int):
    body = {
        "from": page_size / page,
        "size": page_size,
        # "query": {
        #     "bool": {
        #     "should": [
        #         {
        #         "match": {
        #             "processed_video_title": {
        #             "query": query,
        #             "boost": 2,
        #             "fuzziness": "AUTO",
        #             "prefix_length": 0,
        #             "max_expansions": 50,
        #             "operator": "and",  # Уточнение, чтобы все слова из запроса были в результирующих документах
        #             "minimum_should_match": "75%"  # Устанавливаем минимальное количество совпадающих терминов
        #             }
        #         }
        #         },
        #         {
        #         "match": {
        #             "processed_channel_title": {
        #             "query": query,
        #             "boost": 1,
        #             "fuzziness": "AUTO",
        #             "prefix_length": 0,
        #             "max_expansions": 50,
        #             "operator": "and",
        #             "minimum_should_match": "75%"
        #             }
        #         }
        #         }
        #     ]
        #     }
        # }
        "query": {
            "bool": {
            "should": [
                {
                "match": {
                    "processed_video_title": {
                    "query": query,
                    "boost": 3  # Большой boost для точных совпадений
                    }
                }
                },
                {
                "match": {
                    "processed_video_title.ngram": {
                    "query": query,
                    "boost": 2  # Умеренный boost для n-gram совпадений
                    }
                }
                },
                {
                "fuzzy": {
                    "processed_video_title.fuzzy": {
                    "value": query,
                    "fuzziness": "AUTO",
                    "prefix_length": 0,
                    "max_expansions": 50,
                    "transpositions": True,
                    "rewrite": "constant_score_blended",
                    "boost": 1,  # Небольшой boost для fuzzy-поиска
                    }
                }
                },
                {
                "match": {
                    "processed_channel_title": {
                    "query": query,
                    "boost": 1  # Низкий boost для каналов
                    }
                }
                }
            ]
            }
        }
    }
    response = await es.search(index=index, body=body)
    total = response["hits"]["total"]["value"]

    return total, [hit["_source"] for hit in response["hits"]["hits"]]
