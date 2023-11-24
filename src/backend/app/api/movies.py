from typing import Any, List

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.deps.elastic import query_es
from utils.nearest_queries import path

# from utils.spelling_checker.sym_spell_servicer import SymSpellRouterServicer


# spell_checker = SymSpellRouterServicer()
router = APIRouter(prefix="/items")


class InfoSchema(BaseModel):
    status: str
    query: str
    data: List[Any]
    count: int


@router.get("/info", response_model=InfoSchema)
async def info(search_str: str = Query(..., alias="q")):
    # b = spell_checker.predict_single_correction(
    #     search_str,
    #     use_preprocessing=True,
    #     use_keyboard_inverter=False,
    #     use_correction=True,
    # )

    a = query_es(search_str, 1, 5)
    count, data = await a
    return {"status": "ok", "query": search_str, "data": data, "count": count}


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
