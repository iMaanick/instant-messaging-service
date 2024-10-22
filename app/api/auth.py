from fastapi import APIRouter
from fastapi import Request, Depends
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from app.adapters.sqlalchemy_db.models import UserDB
from app.application.auth.fastapi_users import fastapi_users

auth_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@auth_router.get("/check-login-status")
async def check_login_status(user: UserDB = Depends(fastapi_users.current_user(optional=True))):
    if user:
        return {"status": "User is logged in", "username": user.username}
    else:
        return {"status": "User is not logged in"}


@auth_router.get("/register", response_class=HTMLResponse)
async def register_form(
        request: Request,
        user: UserDB = Depends(fastapi_users.current_user(optional=True))
):
    if user:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("register.html", {"request": request})


@auth_router.get("/login", response_class=HTMLResponse)
async def login_form(
        request: Request,
        user: UserDB = Depends(fastapi_users.current_user(optional=True))
):
    if user:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("login.html", {"request": request})


@auth_router.get("/logout", response_class=HTMLResponse)
async def logout_form(
        request: Request,
        user: UserDB = Depends(fastapi_users.current_user(optional=True))
):
    if user:
        return templates.TemplateResponse("logout.html", {"request": request})
    return RedirectResponse(url="/")
