# store/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product  # ⚠️ ЗАМЕНИТЕ Product на название вашей модели товара, если оно другое (например, Item)
from .tasks import notify_new_product

@receiver(post_save, sender=Product)
def handle_new_product(sender, instance, created, **kwargs):
    """
    Сигнал срабатывает каждый раз при сохранении объекта Product.
    Нас интересует только момент создания (created=True).
    """
    if created:
        print(f"🚀 [Signal] Товар '{instance.name}' создан. Отправляем в очередь Celery...")
        
        # ⚠️ ЗАМЕНИТЕ поля name и price на актуальные названия полей в вашей модели
        notify_new_product.delay(instance.name, instance.price)