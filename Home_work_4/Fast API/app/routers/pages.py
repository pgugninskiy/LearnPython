from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Главная"})

@router.get("/about/")
async def about(request: Request):
    context = {
        "request": request,
        "title": "О сайте",
        "site_info": "Это учебное веб-приложение на FastAPI",
        "developer": "Разработчик: pgugninskiy"
    }
    return templates.TemplateResponse("about.html", context)