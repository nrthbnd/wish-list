from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from api.endpoints.user import get_wishes_by_user_first_name  #, get_user_name_by_id

from constants import USER_WISHES

router = APIRouter()


templates = Jinja2Templates(directory='templates')


@router.get('/index')
def get_base_page(request: Request):
    return templates.TemplateResponse(
        'base.html',
        {'request': request},
    )


@router.get('/users/{user_first_name}/wishes')
def get_wish_list_page(
    request: Request,
    user_first_name: str,
    # username=Depends(get_user_name_by_id),
    wishes=Depends(get_wishes_by_user_first_name)
):
    return templates.TemplateResponse(
        'wish-list.html',
        {"request": request, "username": user_first_name, "wishes": wishes},
    )


# @router.get('/auth/jwt/login')
# def get_login_page(
#     request: Request,
#     login: str,
#     username=Depends(get_user_name_by_id),
#     wishes=Depends(get_wishes_by_user)
# ):
#     return templates.TemplateResponse(
#         'wish-list.html',
#         {"request": request, "username": username, "wishes": wishes},
#     )


@router.get('/auth/jwt/login', response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("users/login.html", {"request": request})
