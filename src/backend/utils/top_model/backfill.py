import pickle
import random
from pathlib import Path
from typing import List
from pydantic import BaseModel, Field, TypeAdapter

path = Path(__file__).parent.absolute()


backfill_path = path / "resources" / "backfill.pickle"


class VideoDetailTopIn(BaseModel):
    id: str = Field(..., alias="video_id")
    source_video_title: str = Field(..., alias="video_title")
    source_channel_title: str = Field(..., alias="channel_title")
    v_category: str
    v_channel_type: str


ta = TypeAdapter(List[VideoDetailTopIn])


def get_default_top():
    with open(backfill_path, "rb") as handle:
        d = pickle.load(handle)

    return ta.validate_python(random.choices(d, k=5))
