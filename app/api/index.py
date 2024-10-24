from typing import Annotated

from fastapi import APIRouter, Request, Depends
from starlette.responses import RedirectResponse, Response

from app.adapters.sqlalchemy_db.models import UserDB
from app.api.auth import templates
from app.api.depends_stub import Stub
from app.application.auth.fastapi_users import fastapi_users
from app.application.index.index import get_users_excluding_current
from app.application.protocols.database.user_database_gateway import UserDataBaseGateway

index_router = APIRouter()


@index_router.get("/", response_class=Response)
async def index_page(
        request: Request,
        database: Annotated[UserDataBaseGateway, Depends(Stub(UserDataBaseGateway))],
        user: UserDB = Depends(fastapi_users.current_user(optional=True)),
) -> Response:
    """
    Renders the main index page displaying a list of users.

    This endpoint checks if the user is authenticated. If the user is not
    authenticated, they are redirected to the login page. If the user is
    authenticated, it retrieves a list of users excluding the current user
    and renders the users list page.

    Returns:
        Response: The rendered users list page or a redirect response to the login page.
    """
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

