from django.contrib import admin
from .models import Product

# 1. Создаем кастомное действие (например, скрыть товары)
@admin.action(description="Снять с публикации")
def unpublish_products(modeladmin, request, queryset):
    # queryset - это выбранные товары. Мы меняем у них галочку is_published на False
    queryset.update(is_published=False)

# 2. Настраиваем, как выглядит страница товаров в админке
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Какие колонки показывать в таблице
    list_display = ('name', 'price', 'is_published')
    
    # Фильтр справа (например, показать только опубликованные)
    list_filter = ('is_published',)
    
    # Поле для поиска по названию или описанию
    search_fields = ('name', 'description')
    
    # Подключаем наше кастомное действие
    actions = [unpublish_products]