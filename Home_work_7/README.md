# 📝 Notes App (Flask + Docker)

Простое веб-приложение для управления заметками, разработанное в рамках учебного курса по Python.

## 🚀 Технологии

| Компонент | Версия / Описание |
|-----------|------------------|
| **Backend** | Python 3.11, Flask 3.0 |
| **ORM** | SQLAlchemy 3.1 |
| **База данных** | PostgreSQL 15 (Alpine) |
| **Контейнеризация** | Docker, Docker Compose |
| **Web Server** | Gunicorn + Nginx (reverse proxy) |
| **Шаблоны** | Jinja2 (HTML) |

## 📁 Структура проекта
Home_work_7/
├── app/
│ ├── init.py # Фабрика приложения, инициализация DB
│ ├── models.py # Модель Note (заметка)
│ ├── routes.py # Маршруты: / и /add
│ └── wsgi.py # Точка входа для Gunicorn
├── templates/
│ ├── index.html # Список заметок
│ └── add.html # Форма добавления заметки
├── nginx/
│ └── nginx.conf # Конфигурация Nginx
├── docker-compose.yml # Оркестрация: db + web + nginx
├── Dockerfile # Сборка Python-приложения
├── requirements.txt # Зависимости Python
├── run.py # Локальный запуск (для разработки)
├── .gitignore # Исключения для git
└── README.md # Этот файл