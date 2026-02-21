from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routers import pages, api

app = FastAPI(title="My First Web App")

# Подключение шаблонов и статики
templates = Jinja2Templates(directory="app/templates")


# Подключение роутеров
app.include_router(pages.router)  # HTML-страницы
app.include_router(api.router, prefix="/api")  # API с префиксом /api

@app.get("/health")
async def health():
    return {"status": "ok"}