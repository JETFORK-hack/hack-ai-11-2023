from app.core.config import settings
from app.lifespan import global_objs


index = settings.ELASTICSEARCH_INDEX


async def query_es(query: str, page: int, page_size: int):
    body = {
        "from": page_size / page,
        "size": page_size,
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "processed_video_title": {
                                "query": query,
                                "boost": 3,  # Большой boost для точных совпадений
                            }
                        }
                    },
                    {
                        "match": {
                            "processed_video_title.ngram": {
                                "query": query,
                                "boost": 2,  # Умеренный boost для n-gram совпадений
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
                                "boost": 1,  # Низкий boost для каналов
                            }
                        }
                    },
                ]
            }
        },
        "_source": ["id", "source_video_title", "source_channel_title", "v_category", "v_channel_type", "processed_video_title", "processed_channel_title"],
    }
    response = await global_objs.es.search(index=index, body=body)
    total = response["hits"]["total"]["value"]

    return total, [hit["_source"] for hit in response["hits"]["hits"]]
