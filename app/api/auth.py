from fastapi import APIRouter
from fastapi import Request, Depends
from fastapi.responses import HTMLResponse, Response
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from app.adapters.sqlalchemy_db.models import UserDB
from app.application.auth.fastapi_users import fastapi_users

auth_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@auth_router.get("/register", response_class=Response)
async def register_page(
        request: Request,
        user: UserDB = Depends(fastapi_users.current_user(optional=True))
) -> Response:
    if user:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("register.html", {"request": request})


@auth_router.get("/login", response_class=Response)
async def login_page(
        request: Request,
        user: UserDB = Depends(fastapi_users.current_user(optional=True))
) -> Response:
    if user:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("login.html", {"request": request})
