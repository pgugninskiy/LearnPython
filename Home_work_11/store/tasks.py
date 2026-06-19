# store/tasks.py
from celery import shared_task
import logging
import time

logger = logging.getLogger(__name__)

# Используем shared_task, чтобы не привязываться жестко к экземпляру app
@shared_task
def notify_new_product(product_name, product_price):
    """
    Фоновая задача: логирование/уведомление о добавлении нового товара.
    """
    # Имитация долгой операции (например, отправка email или запись во внешнюю систему)
    time.sleep(3) 
    
    logger.info(f"🔔 УВЕДОМЛЕНИЕ: В магазин добавлен новый товар!")
    logger.info(f"📦 Название: {product_name}")
    logger.info(f"💰 Цена: {product_price} руб.")
    
    return f"Товар {product_name} успешно обработан"