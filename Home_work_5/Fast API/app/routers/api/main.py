from fastapi import APIRouter

from app.routers.api import contacts

router = APIRouter()
router.include_router(contacts.router, prefix="/contacts", tags=["Контакты"])
