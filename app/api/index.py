from typing import Annotated

from fastapi import APIRouter, Request, Depends
from starlette.responses import RedirectResponse

from app.adapters.sqlalchemy_db.gateway.user_sql_gateway import UserSqlaGateway
from app.adapters.sqlalchemy_db.models import UserDB
from app.api.auth import templates
from app.api.depends_stub import Stub
from app.application.auth.fastapi_users import fastapi_users
from app.application.index.index import get_users_excluding_current

index_router = APIRouter()


@index_router.get("/")
async def index_page(
        request: Request,
        database: Annotated[UserSqlaGateway, Depends(Stub(UserSqlaGateway))],
        user: UserDB = Depends(fastapi_users.current_user(optional=True)),
):
    if user is None:
        return RedirectResponse(url="/auth/login")

    users = await get_users_excluding_current(database, user.id)
    return templates.TemplateResponse(
        "users_list.html",
        {
            "request": request,
            "users": users
        }
    )

