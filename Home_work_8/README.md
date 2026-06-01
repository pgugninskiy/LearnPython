# 🛒 Django Store Project

Домашнее задание по курсу Python/Django: создание интернет-магазина с использованием Django ORM, кастомных команд и продвинутой настройки админ-панели.

## 🎯 Цель проекта

Закрепить навыки:
- Создания проекта и приложения в Django
- Работы с моделями через ORM
- Настройки админ-панели для удобного управления данными
- Генерации тестовых данных через кастомные команды

## 🚀 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/pgugninskiy/LearnPython.git
cd LearnPython/Home_work_8


### 2. Создание виртуального окружения
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Применение миграций
```bash
python manage.py migrate
```

### 5. Создание суперпользователя
```bash
python manage.py createsuperuser
```

### 6. Генерация тестовых данных (опционально)
```bash
python manage.py seed_data --categories 5 --products 20
```

### 7. Запуск сервера разработки
```bash
python manage.py runserver
```

## 🌐 Доступные страницы

| Страница | Адрес | Описание |
|----------|-------|----------|
| 🔐 Админ-панель | `/admin/` | Управление товарами и категориями |
| 🛍️ Каталог товаров | `/store/` | Публичная страница со списком товаров |
| 📁 Категория | `/store/category/<id>/` | Фильтрация товаров по категории |

## 🗄️ Структура моделей

### Category
| Поле | Тип | Описание |
|------|-----|----------|
| `name` | CharField | Название категории (уникальное) |
| `description` | TextField | Описание категории |
| `created_at` | DateTimeField | Дата создания (авто) |

### Product
| Поле | Тип | Описание |
|------|-----|----------|
| `name` | CharField | Название товара |
| `description` | TextField | Описание товара |
| `price` | DecimalField | Цена (10 знаков, 2 после запятой) |
| `category` | ForeignKey | Связь с категорией (CASCADE) |
| `created_at` | DateTimeField | Дата создания (авто) |

## ⚙️ Кастомные команды

### `seed_data` — генерация тестовых данных
```bash
# Базовый запуск
python manage.py seed_data

# С параметрами
python manage.py seed_data --categories 10 --products 50
```


## 📁 Структура проекта

```
Home_work_8/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── db.sqlite3                 # ❌ не коммитить в продакшен!
├── django_store/              # настройки проекта
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── store/                     # приложение магазина
    ├── models.py              # модели данных
    ├── admin.py               # настройка админки
    ├── views.py               # представления
    ├── urls.py                # маршруты приложения
    ├── management/commands/   # кастомные команды
    │   └── seed_data.py
    └── templates/store/       # HTML-шаблоны
        ├── base.html
        └── product_list.html
```

## 🔧 Полезные команды

```bash
# Создать миграции после изменения моделей
python manage.py makemigrations store

# Применить миграции
python manage.py migrate

# Открыть Django shell
python manage.py shell

# Проверить проект на ошибки
python manage.py check

# Собрать статику (для production)
python manage.py collectstatic
```

## 👤 Автор

**Павел Гугнинский**
- GitHub: [@pgugninskiy](https://github.com/pgugninskiy)
- Проект выполнен в рамках обучения по направлению "Python-разработка"

---

## ✅ Чек-лист: что сделать прямо сейчас

```bash
# 1. Перейдите в корень проекта
cd Home_work_8

# 2. Создайте файлы
touch .gitignore requirements.txt README.md

# 3. Скопируйте в них содержимое из примеров выше

# 4. Уберите из репозитория лишние файлы (если уже закоммичены)
git rm --cached db.sqlite3
git rm -r --cached __pycache__ */__pycache__ */*/__pycache__

# 5. Закоммитьте изменения
git add .gitignore requirements.txt README.md
git commit -m "docs: add project documentation and gitignore"

# 6. Отправьте на GitHub
git push origin main
```

---

## 🔍 Как проверить, что всё работает?

1. **Клонировать проект «с нуля»** в другую папку:
   ```bash
   git clone https://github.com/pgugninskiy/LearnPython.git test_clone
   cd test_clone/Home_work_8
   ```

2. **Создать окружение и установить зависимости**:
   ```bash
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Запустить проект**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

Если всё запустилось без ошибок — ваш проект полностью самодостаточен! 🎯

---

> 💡 **Профессиональный совет**: В реальных проектах базу данных (`db.sqlite3`) и медиафайлы не хранят в репозитории. Вместо этого:
> - Используют `.env` для секретов (пароли, ключи)
> - Настраивают `MEDIA_ROOT` и `STATIC_ROOT` для продакшена
> - Используют миграции как единственный источник изменений схемы БД

Нужна помощь с настройкой деплоя, тестов или добавлением новых фич? Пишите — помогу! 🚀