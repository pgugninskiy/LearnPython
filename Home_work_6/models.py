# === ИМПОРТЫ: берём нужные инструменты ===
from sqlalchemy.ext.declarative import declarative_base  # шаблон для моделей
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine  # асинхронная работа с БД
from sqlalchemy import Column, Integer, String, Text, ForeignKey  # типы полей
from sqlalchemy.orm import relationship, sessionmaker  # связи и фабрика сессий

# === ПОДКЛЮЧЕНИЕ К БД === 
# Адрес базы: используем SQLite + асинхронный драйвер
DATABASE_URL = "sqlite+aiosqlite:///./homework.db"

# Создаём "мотор" — он управляет соединениями с БД
# echo=True покажет все SQL-запросы в консоли (удобно при отладке)
engine = create_async_engine(DATABASE_URL, echo=False)

# === БАЗОВЫЙ КЛАСС ===
# От него будут наследоваться все наши модели
Base = declarative_base()

# === ФАБРИКА СЕССИЙ ===
# AsyncSessionLocal() — вызовет эту "фабрику" и выдаст новую сессию
AsyncSessionLocal = sessionmaker(
    bind=engine,              # привязываем к нашему мотору
    class_=AsyncSession,      # используем асинхронную сессию
    expire_on_commit=False    # после сохранения данные остаются в объектах
)

# === МОДЕЛЬ: ПОЛЬЗОВАТЕЛЬ ===
class User(Base):
    __tablename__ = "users"  # имя таблицы в БД

    # Поля = колонки в таблице
    id = Column(Integer, primary_key=True)  # уникальный ID
    name = Column(String, nullable=False)               # имя (обязательно)
    username = Column(String, nullable=False, unique=True)  # логин (уникальный)
    email = Column(String, nullable=False, unique=True, index=True)    # email (уникальный)

    # Связь: у пользователя есть список постов
    posts = relationship(
        "Post",                    # с какой моделью связываем
        back_populates="user",     # как называется обратная связь в Post
        cascade="all, delete-orphan"  # удалять посты при удалении пользователя
    )

    # Для удобного вывода в консоль
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
    

# === МОДЕЛЬ: ПОСТ ===
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    # Внешний ключ: ссылается на id в таблице users
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)   # заголовок (обязательно)
    body = Column(Text, nullable=False)      # текст поста (обязательно, длинный)

    # Обратная связь: у поста есть один пользователь-автор
    user = relationship("User", back_populates="posts")

    def __repr__(self):
        # Обрезаем заголовок до 30 символов, чтобы не засорять консоль
        return f"<Post(id={self.id}, title='{self.title[:30]}...')>"