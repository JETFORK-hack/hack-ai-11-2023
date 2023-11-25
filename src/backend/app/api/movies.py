from typing import List

from fastapi import APIRouter, Query
from pydantic import BaseModel, TypeAdapter

from app.deps.elastic import query_es_get_best

# from app.lifespan import spell_checker, nearest_queries
from app.lifespan import global_objs
from utils.top_model.backfill import get_default_top


router = APIRouter(prefix="/items")


class VideoDetailOut(BaseModel):
    id: str
    source_video_title: str
    source_channel_title: str
    v_category: str
    v_channel_type: str


class InfoSchema(BaseModel):
    status: str
    query: str
    data: List[VideoDetailOut] = []
    count: int
    backfill: List[VideoDetailOut] = []


class VideoRankValidator(BaseModel):
    id: str
    source_channel_title: str
    processed_video_title: str
    processed_channel_title: str


rvm = TypeAdapter(List[VideoRankValidator])


@router.get("/info", response_model=InfoSchema)
async def info(search_str: str = Query(..., alias="q")):
    search_str, clear_search_str = global_objs.spell_checker.predict_single_correction(
        search_str,
        use_preprocessing=True,
        use_keyboard_inverter=False,
        use_correction=True,
    )

    on_processed_search = tuple(
        set(
            [
                *global_objs.nearest_queries.get_knn_query(clear_search_str),
                clear_search_str,
            ]
        )
    )

    condidats = query_es_get_best(search_str, page=1, page_size=150)
    count, data = await condidats

    # try:
    if len(data) < 5:
        return {
            "status": "ok",
            "query": search_str,
            "data": data if len(data) else [],
            "count": count,
            "backfill": [] if len(data) else get_default_top(),
        }
    
    try:
        top = global_objs.ranker.rerank(
            search_str, [item.model_dump() for item in rvm.validate_python(data)], k=5
        )

        return {
            "status": "ok",
            "query": search_str,
            "data": list(filter(lambda x: x.get("id") in top, data)),
            "count": count,
            "backfill": [] if len(data) else get_default_top(),
        }
    except Exception:
        return {
            "status": "ok",
            "query": search_str,
            "data": [],
            "count": count,
            "backfill": get_default_top(),
        }


# @router.get("", response_model=List[ItemSchema])
# async def get_items(
#     response: Response,
#     session: AsyncSession = Depends(get_async_session),
#     request_params: RequestParams = Depends(parse_react_admin_params(Item)),
#     user: User = Depends(current_user),
# ) -> Any:
#     total = await session.scalar(
#         select(func.count(Item.id).filter(Item.user_id == user.id))
#     )
#     items = (
#         (
#             await session.execute(
#                 select(Item)
#                 .offset(request_params.skip)
#                 .limit(request_params.limit)
#                 .order_by(request_params.order_by)
#                 .filter(Item.user_id == user.id)
#             )
#         )
#         .scalars()
#         .all()
#     )
#     response.headers[
#         "Content-Range"
#     ] = f"{request_params.skip}-{request_params.skip + len(items)}/{total}"
#     return items
