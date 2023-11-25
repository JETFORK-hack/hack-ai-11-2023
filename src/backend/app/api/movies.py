from typing import Any, List

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.deps.elastic import query_es, query_es_get_best

# from app.lifespan import spell_checker, nearest_queries
from app.lifespan import global_objs
from utils.top import get_default_top


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
    on_processed_search: Any
    backfill: List[VideoDetailOut] = []


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
    return {
        "status": "ok",
        "query": search_str,
        "data": data,
        "count": count,
        "on_processed_search": on_processed_search,
        "backfill": [] if len(data) else get_default_top(),
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
