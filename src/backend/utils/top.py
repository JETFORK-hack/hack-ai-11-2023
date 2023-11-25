import pickle
import random
from pathlib import Path
from typing import List
from pydantic import BaseModel, Field, TypeAdapter

# from app.lifespan import global_objs


path = Path(__file__).parent.absolute()
path = path / "backfill.pickle"


def match_dates(query: str, video: str) -> float:
    res_query = date_parser.es.findall(query)
    spans_query = [_.span for _ in res_query]

    res_video = date_parser.es.findall(video)
    spans_video = [_.span for _ in res_video]

    if (not spans_query and spans_video) or (spans_query and not spans_video):
        return 0.0

    if not spans_query and not spans_video:
        return -1.0

    spans_query = query[spans_query[0].start : spans_query[0].stop]
    spans_video = video[spans_video[0].start : spans_video[0].stop]

    if spans_query == spans_video:
        return 1.0

    return len(set(spans_query) & set(spans_video)) / max(
        len(set(spans_query)), len(set(spans_query))
    )


def match_episodes(query: str, video: str) -> float:
    res_query = episode_re.search(query)
    res_video = episode_re.search(query)

    if (not res_query and res_video) or (res_query and not res_video):
        return 0.0

    if not res_query and not res_video:
        return -1.0

    res_query = number_re.findall(res_query.group(0))[0]
    res_video = number_re.findall(res_video.group(0))[0]

    if res_query == res_video:
        return 1.0

    return 0.0


def match_season(query: str, video: str) -> float:
    res_query = season_re.search(query)
    res_video = season_re.search(query)

    if (not res_query and res_video) or (res_query and not res_video):
        return 0.0

    if not res_query and not res_video:
        return -1.0

    res_query = number_re.findall(res_query.group(0))[0]
    res_video = number_re.findall(res_video.group(0))[0]

    if res_query == res_video:
        return 1.0

    return 0.0


class VideoDetailTopIn(BaseModel):
    id: str = Field(..., alias="video_id")
    source_video_title: str = Field(..., alias="video_title")
    source_channel_title: str = Field(..., alias="channel_title")
    v_category: str
    v_channel_type: str


ta = TypeAdapter(List[VideoDetailTopIn])


def get_default_top():
    with open(path, "rb") as handle:
        d = pickle.load(handle)

    return ta.validate_python(random.choices(d, k=5))
