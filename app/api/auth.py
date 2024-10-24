from fastapi import APIRouter
from fastapi import Request, Depends
from fastapi.responses import HTMLResponse, Response
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from app.adapters.sqlalchemy_db.models import UserDB
from app.application.auth.fastapi_users import fastapi_users

auth_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@auth_router.get("/register", response_class=Response)
async def register_page(
        request: Request,
        user: UserDB = Depends(fastapi_users.current_user(optional=True))
) -> Response:
    """
       Renders the registration page for new users.

       This endpoint checks if the user is already authenticated. If the user is
       authenticated, he is redirected to the index page. If not, the registration
       page is rendered.

       Returns:
           Response: The rendered registration page or a redirect response to the index page.
   """
    if user:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("register.html", {"request": request})


@auth_router.get("/login", response_class=Response)
async def login_page(
        request: Request,
        user: UserDB = Depends(fastapi_users.current_user(optional=True))
) -> Response:
    """
       Renders the login page.

       This endpoint checks if the user is already authenticated. If the user is
       authenticated, they are redirected to the index page. If not, the login
       page is rendered.

       Returns:
           Response: The rendered login page or a redirect response to the index page.
       """
    if user:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("login.html", {"request": request})
