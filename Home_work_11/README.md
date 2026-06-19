# README для проекта интернет-магазина с Celery

## 📋 Описание проекта

Учебный проект интернет-магазина на Django с реализацией фоновых задач через Celery и Redis. Демонстрирует паттерн асинхронной обработки событий при добавлении новых товаров в каталог.

### 🎯 Цель проекта
Освоить использование Celery для выполнения фоновых задач и настройку Redis как брокера задач в Django-приложении.

## 🛠 Технологии

- **Python 3.13** — основной язык
- **Django 6.0.6** — веб-фреймворк
- **Celery 5.6.3** — распределенная очередь задач
- **Redis** — брокер сообщений (запущен через Podman)
- **SQLite** — база данных (по умолчанию в Django)

## 📁 Структура проекта

```
Home_work_11/
├── django_store/              # Основной проект Django
│   ├── __init__.py           # Инициализация Celery
│   ├── celery.py             # Конфигурация Celery
│   ├── settings.py           # Настройки Django + Celery
│   ├── urls.py
│   └── wsgi.py
├── store/                     # Приложение магазина
│   ├── migrations/
│   ├── templates/
│   ├── __init__.py
│   ├── admin.py              # Админка с кастомными полями
│   ├── apps.py               # Подключение сигналов
│   ├── models.py             # Модели Category, Product
│   ├── signals.py            # Обработчики событий Django
│   ├── tasks.py              # Фоновые задачи Celery
│   └── views.py
├── manage.py
└── README.md
```

## 🚀 Установка и настройка

### 1. Клонирование и установка зависимостей

```bash
# Перейдите в папку проекта
cd Home_work_11

# Создайте виртуальное окружение
python -m venv .venv

# Активируйте виртуальное окружение
# Windows PowerShell:
.venv\Scripts\Activate.ps1

# Установите зависимости
pip install django celery redis
```

### 2. Запуск Redis через Podman

```bash
# Запустите контейнер Redis в фоновом режиме
podman run -d -p 6379:6379 --name redis redis

# Проверьте, что контейнер запущен
podman ps
```

### 3. Настройка базы данных

```bash
# Примените миграции
python manage.py migrate

# Создайте суперпользователя для доступа к админке
python manage.py createsuperuser
```

## ⚙️ Конфигурация Celery

### Файл `django_store/celery.py`

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_store.settings')

app = Celery('django_store')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

### Настройки в `django_store/settings.py`

```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'
```

## 🎯 Реализованные функции

### 1. Модели данных

**Category** — категория товаров:
- `name` — название категории
- `description` — описание
- `created_at` — дата создания
- `products` — связанные товары (reverse relation)

**Product** — товар:
- `name` — название товара
- `category` — категория (ForeignKey)
- `price` — цена
- `description` — описание
- `created_at` — дата создания

### 2. Фоновая задача `notify_new_product`

Файл `store/tasks.py`:

```python
from celery import shared_task
import logging
import time

logger = logging.getLogger(__name__)

@shared_task
def notify_new_product(product_name, product_price):
    """
    Фоновая задача: логирование/уведомление о добавлении нового товара.
    Имитирует долгую операцию (отправка email, интеграция с внешними системами).
    """
    time.sleep(3)  # Имитация длительной операции
    
    logger.info(f"🔔 УВЕДОМЛЕНИЕ: В магазин добавлен новый товар!")
    logger.info(f"📦 Название: {product_name}")
    logger.info(f"💰 Цена: {product_price} руб.")
    
    return f"Товар {product_name} успешно обработан"
```

### 3. Автоматический запуск через Django Signals

Файл `store/signals.py`:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from .tasks import notify_new_product

@receiver(post_save, sender=Product)
def handle_new_product(sender, instance, created, **kwargs):
    """
    Сигнал срабатывает при создании нового товара.
    Отправляет задачу в очередь Celery для асинхронной обработки.
    """
    if created:
        print(f"🚀 [Signal] Товар '{instance.name}' создан. Отправляем в очередь Celery...")
        notify_new_product.delay(instance.name, instance.price)
```

### 4. Кастомизация админки

Файл `store/admin.py`:

```python
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at', 'is_expensive')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price',)
    
    def is_expensive(self, obj):
        """Кастомное поле с цветовой индикацией цены"""
        return format_html(
            '<span style="color: {};">{}</span>',
            'red' if obj.price > 1000 else 'green',
            'Дорого' if obj.price > 1000 else 'Доступно'
        )
    is_expensive.short_description = 'Статус цены'
```

## 🏃 Запуск проекта

### Терминал 1: Redis (если не запущен как служба)

```bash
podman start redis
```

### Терминал 2: Celery Worker

```bash
# Для Windows обязательно использовать --pool=solo
celery -A django_store worker -l info --pool=solo
```

Ожидаемый вывод:
```
 -------------- celery@NTB59621 v5.6.3 (recovery)
--- ***** -----
-- ******* ---- Windows-11-10.0.26200-SP0
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         django_store:0x1ef0d54dfd0
- ** ---------- .> transport:   redis://localhost:6379/0
- ** ---------- .> results:     redis://localhost:6379/0
- *** --- * --- .> concurrency: 12 (solo)
-- ******* ---- .> task events: OFF
--- ***** -----
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery

[tasks]
  . store.tasks.notify_new_product

[INFO] Connected to redis://localhost:6379/0
[INFO] celery@NTB59621 ready.
```

### Терминал 3: Django Server

```bash
python manage.py runserver 8001
```

Откройте браузер: `http://127.0.0.1:8001/admin/`

## 📊 Примеры работы

### Сценарий 1: Добавление товара через админку

1. Войдите в админку: `http://127.0.0.1:8001/admin/`
2. Перейдите в раздел **Products** → **Add Product**
3. Заполните форму:
   - Name: `Морковка`
   - Category: выберите категорию
   - Price: `5`
4. Нажмите **Save**

**Результат в консоли Django:**
```
🚀 [Signal] Товар 'Морковка' создан. Отправляем в очередь Celery...
```

**Результат в консоли Celery Worker (через 3 секунды):**
```
[INFO] Received task: store.tasks.notify_new_product[c9af1439-e5a1-4ecb-b7fe-086ae87b2529]
[INFO] 🔔 УВЕДОМЛЕНИЕ: В магазин добавлен новый товар!
[INFO] 📦 Название: Морковка
[INFO] 💰 Цена: 5 руб.
[INFO] Task store.tasks.notify_new_product[c9af1439-...] succeeded in 3.01s: 'Товар Морковка успешно обработан'
```

### Сценарий 2: Прямой вызов задачи через Django Shell

```bash
python manage.py shell
```

```python
from store.tasks import notify_new_product

result = notify_new_product.delay("Тестовый товар", 9999)
print(f"Task ID: {result.id}")
```

**Результат в консоли Celery Worker:**
```
[INFO] Received task: store.tasks.notify_new_product[7b99bd9f-b03a-4bdb-90c6-a13194d7d7b1]
[INFO] 🔔 УВЕДОМЛЕНИЕ: В магазин добавлен новый товар!
[INFO] 📦 Название: Тестовый товар
[INFO] 💰 Цена: 9999 руб.
[INFO] Task store.tasks.notify_new_product[7b99bd9f-...] succeeded in 3.01s
```

## 🏗 Архитектура решения

### Поток данных

```
┌─────────────────┐
│  Django Admin   │
│  (HTTP запрос)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Product.save() │
│  (запись в БД)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  post_save      │
│  signal         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│  Celery.delay() │─────▶│   Redis      │
│  (отправка в    │      │  (брокер)    │
│   очередь)      │      └──────┬───────┘
└─────────────────┘             │
                                │
                                ▼
                         ┌──────────────┐
                         │ Celery       │
                         │ Worker       │
                         │ (выполнение  │
                         │  задачи)     │
                         └──────────────┘
```

### Ключевые принципы

1. **Разделение ответственности**
   - Django отвечает за HTTP-запросы и работу с БД
   - Celery отвечает за фоновые задачи
   - Redis служит посредником между ними

2. **Асинхронность**
   - Пользователь получает мгновенный ответ от сервера
   - Тяжелые задачи выполняются в фоне

3. **Масштабируемость**
   - Можно запустить несколько воркеров Celery
   - Redis обрабатывает тысячи сообщений в секунду

4. **Надежность**
   - Задачи не теряются при перезапуске сервера
   - Поддержка retry при ошибках

## ✅ Критерии выполнения задания

- [x] **Настроен Celery с Redis**
  - Создан файл `django_store/celery.py` с конфигурацией
  - В `settings.py` указаны `CELERY_BROKER_URL` и `CELERY_RESULT_BACKEND`
  - Celery успешно подключается к Redis на порту 6379

- [x] **Реализована фоновая задача**
  - Создана задача `notify_new_product` в `store/tasks.py`
  - Задача выводит информацию о товаре в консоль
  - Используется декоратор `@shared_task`

- [x] **Протестирована работа Celery**
  - Задачи корректно ставятся в очередь через `.delay()`
  - Воркер Celery принимает и выполняет задачи
  - Основной поток Django не блокируется


## 📝 Полезные команды

```bash
# Проверить статус Redis
podman ps

# Остановить Redis
podman stop redis

# Удалить контейнер Redis
podman rm redis

# Перезапустить Celery worker
# Ctrl+C в терминале воркера, затем:
celery -A django_store worker -l info --pool=solo

# Очистить очередь задач
celery -A django_store purge
```

## 🐛 Решение проблем

### Ошибка: `ModuleNotFoundError: No module named 'django'`

**Решение:** Установите Django:
```bash
pip install django celery redis
```

### Ошибка: `redis-server: command not found`

**Решение:** Запустите Redis через Podman:
```bash
podman run -d -p 6379:6379 --name redis redis
```

### Celery worker зависает на Windows

**Решение:** Используйте флаг `--pool=solo`:
```bash
celery -A django_store worker -l info --pool=solo
```

### Ошибка: `AlreadyRegistered: The model Product is already registered`

**Решение:** Проверьте, что в `admin.py` нет дублирующихся декораторов `@admin.register(Product)`.

## 📚 Полезные ссылки

- [Документация Celery](https://docs.celeryq.dev/en/stable/)
- [Документация Redis](https://redis.io/docs/)
- [Celery с Django](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html)
- [Django Signals](https://docs.djangoproject.com/en/stable/topics/signals/)

