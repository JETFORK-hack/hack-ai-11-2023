from typing import Any, List

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.deps.elastic import query_es

# from app.lifespan import spell_checker, nearest_queries
from app.lifespan import global_objs


router = APIRouter(prefix="/items")


class InfoSchema(BaseModel):
    status: str
    query: str
    data: List[Any]
    count: int
    on_processed_search: Any


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

    a = query_es(search_str, 1, 5)
    count, data = await a
    return {
        "status": "ok",
        "query": search_str,
        "data": data,
        "count": count,
        "on_processed_search": on_processed_search,
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
