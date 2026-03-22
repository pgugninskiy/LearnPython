from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter()


# ==================== Модели данных ====================


class ContactBase(BaseModel):
    """Базовая модель контакта"""

    name: str = Field(..., min_length=1, max_length=100, description="Имя контакта")
    phone: str = Field(..., min_length=10, max_length=20, description="Номер телефона")
    email: Optional[str] = Field(None, description="Email адрес")
    notes: Optional[str] = Field(None, max_length=500, description="Заметки")


class ContactCreate(ContactBase):
    """Модель для создания контакта"""

    pass


class Contact(ContactBase):
    """Модель контакта с ID и датой создания"""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Временное хранилище ====================

contacts_db: List[Contact] = []
next_id = 1


# ==================== API Endpoints ====================


@router.get("/", response_model=List[Contact], tags=["Контакты"])
async def get_all_contacts():
    """
    📋 Получить список всех контактов

    Возвращает полный список контактов из справочника.
    """
    return contacts_db


@router.get("/{contact_id}", response_model=Contact, tags=["Контакты"])
async def get_contact(contact_id: int):
    """
    👤 Получить контакт по ID

    Возвращает подробную информацию о конкретном контакте.
    """
    contact = next((c for c in contacts_db if c.id == contact_id), None)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Контакт с ID {contact_id} не найден",
        )
    return contact


@router.post(
    "/", response_model=Contact, status_code=status.HTTP_201_CREATED, tags=["Контакты"]
)
async def create_contact(contact_data: ContactCreate):
    """
    ➕ Создать новый контакт

    Добавляет новый контакт в телефонный справочник.
    """
    global next_id

    new_contact = Contact(
        id=next_id,
        name=contact_data.name,
        phone=contact_data.phone,
        email=contact_data.email,
        notes=contact_data.notes,
        created_at=datetime.now(),
    )

    contacts_db.append(new_contact)
    next_id += 1

    return new_contact
