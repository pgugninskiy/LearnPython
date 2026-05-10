import asyncio
from typing import List, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from jsonplaceholder_requests import fetch_users_data, fetch_posts_data
from models import Base, engine, AsyncSessionLocal, User, Post


async def create_tables():
    """Создаёт таблицы в БД, если их нет."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def add_users_to_db(session: AsyncSession, users_data: List[Dict[str, Any]]) -> List[User]:
    """
    Добавляет пользователей в БД.
    Возвращает список созданных объектов User.
    """
    users = []
    for user_dict in users_data:  # ← исправлено: двоеточие после for
        user = User(
            id=user_dict["id"],
            name=user_dict["name"],
            username=user_dict["username"],
            email=user_dict["email"]
        )
        users.append(user)

    session.add_all(users)
    await session.commit()
    # Refresh objects to get any DB-generated values (if needed)
    for user in users:
        await session.refresh(user)
    return users


async def add_posts_to_db(session: AsyncSession, posts_data: List[Dict[str, Any]]) -> List[Post]:
    """
    Добавляет посты в БД.
    Возвращает список созданных объектов Post.
    """
    posts = []
    for post_dict in posts_data:  # ← исправлено: двоеточие после for
        post = Post(
            id=post_dict["id"],
            user_id=post_dict["userId"],  # API возвращает camelCase
            title=post_dict["title"],
            body=post_dict["body"]
        )
        posts.append(post)

    session.add_all(posts)
    await session.commit()
    for post in posts:
        await session.refresh(post)
    return posts


async def async_main():
    """
    Основная асинхронная функция: полный цикл программы.
    """
    # 1. Инициализация БД
    await create_tables()

    # 2. Параллельная загрузка данных из API
    users_data, posts_data = await asyncio.gather(
        fetch_users_data(),
        fetch_posts_data(),
    )

    # 3. Добавление данных в БД через сессию
    async with AsyncSessionLocal() as session:
        await add_users_to_db(session, users_data)
        await add_posts_to_db(session, posts_data)

        # Опционально: проверка количества записей
        users_result = await session.execute(select(User))
        posts_result = await session.execute(select(Post))
        print(f"✓ Добавлено пользователей: {len(users_result.scalars().all())}")
        print(f"✓ Добавлено постов: {len(posts_result.scalars().all())}")

    # 4. Корректное закрытие соединений
    await engine.dispose()


def main():
    """Точка входа в программу."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()