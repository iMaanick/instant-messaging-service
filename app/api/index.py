from fastapi import APIRouter, Request, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.adapters.sqlalchemy_db.models import UserDB
from app.api.auth import templates
from app.api.depends_stub import Stub
from app.application.auth.fastapi_users import fastapi_users

index_router = APIRouter()


@index_router.get("/")
async def index(
        request: Request,
        session: AsyncSession = Depends(Stub(AsyncSession)),
        user: UserDB = Depends(fastapi_users.current_user(optional=True))
):
    if user is None:
        return RedirectResponse(url="/login")

    result = await session.execute(select(UserDB).where(UserDB.id != user.id).order_by(UserDB.username))
    users = result.scalars().all()
    return templates.TemplateResponse("users_list.html", {"request": request, "users": users})

