from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(tags=['BAZA'])

templates = Jinja2Templates(directory="app/templates")


@router.get('/', response_class=HTMLResponse)
async def home(request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,  # Обязательный параметр!
            "title": "Главная",
            "username": "Иван",
            "is_admin": True
        }
    )
