# django_store/celery.py
import os
from celery import Celery

# Указываем стандартный модуль настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_store.settings')

app = Celery('django_store')

# Загружаем настройки из settings.py, используя префикс CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически ищем задачи (tasks.py) во всех установленных приложениях (INSTALLED_APPS)
app.autodiscover_tasks()