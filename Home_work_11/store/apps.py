# store/apps.py
from django.apps import AppConfig

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    def ready(self):
        # Импортируем сигналы, чтобы они зарегистрировались при старте Django
        import store.signals 