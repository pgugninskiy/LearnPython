import aiohttp
from typing import List, Dict, Any

# Константы с ресурсами API
USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"


async def fetch_json(session: aiohttp.ClientSession, url: str) -> List[Dict[str, Any]]:
    """
    Базовая функция для получения JSON-данных по URL.
    Переиспользуется для разных эндпоинтов.
    """
    async with session.get(url) as response:
        response.raise_for_status()  # выбросит ошибку при статусе 4xx/5xx
        return await response.json()


async def fetch_users_data() -> List[Dict[str, Any]]:
    """Получает список пользователей с API."""
    async with aiohttp.ClientSession() as session:
        return await fetch_json(session, USERS_DATA_URL)


async def fetch_posts_data() -> List[Dict[str, Any]]:
    """Получает список постов с API."""
    async with aiohttp.ClientSession() as session:
        return await fetch_json(session, POSTS_DATA_URL)