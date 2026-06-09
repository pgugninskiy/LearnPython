from django.db import models

class Product(models.Model):
    # Поле для названия (текст, максимум 200 символов)
    name = models.CharField(max_length=200, verbose_name="Название товара")
    
    # Поле для описания (длинный текст)
    description = models.TextField(verbose_name="Описание")
    
    # Поле для цены (число: максимум 10 знаков, 2 знака после запятой)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    
    # Галочка: опубликован товар или нет (по умолчанию True)
    is_published = models.BooleanField(default=True, verbose_name="Опубликован")

    def __str__(self):
        # Это то, как товар будет называться в админке (например, "Ноутбук")
        return self.name 
